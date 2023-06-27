import random

import sys, os
root_path = os.getcwd()
print(f'root path : {root_path}')
sys.path.append(root_path)

from utils.file_processing import save_file, load_file
from data_check.sub_infos.category import cate
from utils.translate import translate_to_korean_local, translate_to_korean
from utils.compare import find_different_words, find_deleted_words, highlight_given_word, replace_word
from utils.show_image import show_image

origin_filename, new_filename = 'data_check/origin_caps/original_caps_fixed.txt', 'data_check/new_caps/final_same_caps_ver2.txt'
start_idx_path = 'data_check/start_idx.txt'
pass_pairs_path = 'data_check/different_pairs.json'
local_dict_path = 'utils/translator.json'
keep_idxes_path = 'data_check/keep_idxes.txt'

def save_results(checked_lines, next_idx, myDict, pass_pairs, keep_idxes):
    checked_data = "\n".join(checked_lines)
    save_file(checked_data, new_filename)
    save_file([str(next_idx)], start_idx_path)
    save_file(myDict, local_dict_path)
    save_file(pass_pairs, pass_pairs_path)
    save_file("\n".join(map(str, sorted(keep_idxes))), keep_idxes_path)

def call_words_by_category(word, category_type = 'same'):
    new_words = []
    categories = cate()
    for category in categories.keys():
        if (category_type == 'same' and word in categories[category]) \
            or (category_type == 'diff' and word not in categories[category]):
            new_words += categories[category]
    if word in new_words:
        new_words.remove(word)

    random.shuffle(new_words)
    return new_words

def add_in_pair(origin_word, new_word, pair):
    if origin_word in pair.keys():
        pair[origin_word].append(new_word)
    else:
        pair[origin_word] = [new_word]
    return pair

def check_in_pair(origin_word, new_words, pairs):
    in_pairs_idxes = []
    for idx, new_word in enumerate(new_words):
        if origin_word in pairs.keys() and new_word in pairs[origin_word]:
            in_pairs_idxes.append(idx)
    return in_pairs_idxes

def call_word_similarities(line_idx):
    sim_list = load_file(os.path.join("data_check/sub_infos/analysis", f'{line_idx}.txt'))

    origin_capt = sim_list[0].split(', ')[0]
    origin_words = origin_capt.split(' ')
    word_sims = {origin_word : -1 for origin_word in origin_words}

    line_idx = 1
    while -1 in word_sims.values() and line_idx < len(sim_list):
        sim_info = sim_list[line_idx].split(', ')
        sim_capt, euclidean, inner = sim_info
        diff_word = find_deleted_words(origin_capt, sim_capt)
        word_sims[diff_word] = float(inner)
        line_idx += 1
    
    word_sims = {key: value for key, value in word_sims.items() if len(key) != 1}
    return word_sims


def check_lines(origin_data, new_data, start_idx, myDict, pass_pairs, keep_idxes):

    if len(origin_data) != len(new_data):
        print('[wrong inputs] different length')
        return new_data, start_idx, myDict, pass_pairs, keep_idxes
    
    line_idx = start_idx
    while line_idx < len(new_data):
        # read lines
        origin_capt = origin_data[line_idx]
        new_line = new_data[line_idx]
        if new_line[:5] == 'none,':
            result_key = 'none'
            new_capts = [new_line.lstrip('none, ')]
        elif new_line[:4] == 'new,':
            result_key = 'new '
            new_capts = [new_line.lstrip('new, ')]
        else:
            result_key = ' +  '
            new_capts = new_line.split('+')[:-1]

        print(f'\n[line {line_idx}]')

        # find different word and print
        diff_word_idxes, origin_capt_print, new_capts_print = find_different_words(origin_capt, new_capts)        
        diff_word = origin_capt.split(' ')[diff_word_idxes[0]]
        myDict, diff_word_trans = translate_to_korean_local(myDict, diff_word)
        print(f'[origin] {origin_capt_print} ({diff_word_trans})')
        for capt_idx, new_capt in enumerate(new_capts_print):
            myDict, new_word_trans = translate_to_korean_local(myDict, new_capt.split(' ')[diff_word_idxes[0]].lstrip('{').rstrip('}'))
            print(f'[{result_key} {capt_idx+1}] {new_capt} ({new_word_trans})')
        
        # pass if there is a new word which is in diff pair
        new_words = [new_capt.split(' ')[diff_word_idxes[0]] for new_capt in new_capts]
        in_pair_idxes = check_in_pair(diff_word, new_words, pass_pairs)
        if len(in_pair_idxes) != 0:
            new_data[line_idx] = new_capts[random.choice(in_pair_idxes)]
            print(f'(Pass) {new_data[line_idx]}')
            line_idx += 1
            continue

        # pick sentence
        work_key = '-1'
        str_idxes = [str(i) for i in range(len(new_capts)+1)]
        str_idxes += ['a'+i for i in str_idxes]
        while work_key not in ['q', 'e', 'w', 'd', 'k'] + str_idxes:
            work_key = input('Pick caption idx (add-in-pair(a*), change origin word(w), change new word(e), show_image(r), translate all(t), fix translation(f), fix typo(d), keep(k), quit(q) ')
            if work_key == 'r': # show image
                show_image(origin_capt)
            elif work_key == 't': # translate all sentences
                print(f'[origin] {translate_to_korean(origin_capt)}')
                for new_capt_idx, new_capt in enumerate(new_capts):
                    print(f'[{result_key} {capt_idx+1}] {translate_to_korean(new_capt)}')
            elif work_key == 'f': # fix local dictionary
                capt_idx_str = ["0"] + [str(i+1) for i in range(len(new_capts))]
                new_trans_key = -1
                while new_trans_key not in capt_idx_str:
                    new_trans_key = input("Which caption's word? (origin(0)) ")
                trans_word = new_capts[int(new_trans_key)-1].split(" ")[diff_word_idxes[0]] if new_trans_key != '0' else diff_word
                myDict[trans_word] = input(f"{trans_word} : ")

        if work_key == 'q': # save and quit
            return new_data, line_idx, myDict, pass_pairs, keep_idxes
        elif work_key == 'e':  # call other new word
            if diff_word in pass_pairs.keys() and len(pass_pairs[diff_word]) > 4: # auto pick if the origin word's diff pair is already more then 4
                new_word = random.choice(pass_pairs[diff_word])
            else: # ask user about new word
                new_words = call_words_by_category(diff_word, category_type = 'same')
                choiced = 'e'
                while choiced not in ['1', 'a']:
                    if choiced == 'q':
                        return new_data, line_idx, myDict, pass_pairs, keep_idxes
                    new_word = new_words.pop()
                    myDict, new_word_trans = translate_to_korean_local(myDict, new_word)
                    choiced = input(f'[{diff_word} -> {new_word} ({new_word_trans})] choose(1), add-in-pair(a), other(e), quit(q) ')
                if choiced == 'a': # add in pair
                    pass_pairs = add_in_pair(diff_word, new_word, pass_pairs)

            new_data[line_idx] = replace_word(origin_capt, diff_word, new_word)
            print(f'(Fixed!) {new_data[line_idx]}')
            line_idx += 1
        elif work_key == 'w':  # pick new origin word to change
            word_sims = call_word_similarities(line_idx)
            word_sims = sorted(word_sims.items(), key = lambda item: item[1], reverse=True)
            
            diff_word = None
            for word_idx, (word, sim) in enumerate(word_sims):
                if diff_word == None:
                    highlighted_capt = highlight_given_word(origin_capt, word)
                    diff_word_key = input(f'[{word_idx+1}/{len(word_sims)} {round(sim, 4)}] {highlighted_capt} (choose(1), other(w), quit(q)) ')
                    if diff_word_key == 'q':
                        return new_data, line_idx, myDict, pass_pairs, keep_idxes
                    elif diff_word_key == '1':
                        diff_word = word
                        new_word = random.choice(call_words_by_category(diff_word, category_type = 'same'))
                        new_data[line_idx] = 'new, '+replace_word(origin_capt, diff_word, new_word)
        elif work_key == 'k': # keep
            print('(keep!)')
            keep_idxes.update([line_idx])
            line_idx += 1
        elif work_key == 'd': # fix typo
            capt_idx_str = ["0"] + [str(i+1) for i in range(len(new_capts))]
            fix_key = -1
            while fix_key not in capt_idx_str:
                fix_key = input("Which caption do you want to change? (origin(0), new(1)) ")
            if fix_key == '0':
                origin_data[line_idx] = input("Enter new : ")
                continue
            else:
                new_data[line_idx] = 'none, ' + input("Enter new : ")
                continue
        else: # pick 1 sentence & pass
            if work_key[0] == 'a':
                work_key = work_key[1]
                new_word = new_capts[int(work_key)-1].split(' ')[diff_word_idxes[0]]
                pass_pairs = add_in_pair(diff_word, new_word, pass_pairs)
            new_data[line_idx] = new_capts[int(work_key)-1]
            line_idx += 1

    return new_data, line_idx, myDict, pass_pairs, keep_idxes
        

        


if __name__=='__main__':
    origin_data = load_file(origin_filename)
    new_data = load_file(new_filename)

    start_idx = int(load_file(start_idx_path)[0])
    myDict = load_file(local_dict_path)
    pass_pairs = load_file(pass_pairs_path)
    keep_idxes = set([int(line) for line in load_file(keep_idxes_path)])

    checked_data, next_idx, myDict, pass_pairs, keep_idxes = check_lines(origin_data, new_data, start_idx, myDict, pass_pairs, keep_idxes)
    save_results(checked_data, next_idx, myDict, pass_pairs, keep_idxes)

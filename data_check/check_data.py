import random

import sys, os
root_path = os.getcwd()
print(f'root path : {root_path}')
sys.path.append(root_path)

from utils.file_processing import increment_filename, save_file, load_file
from data_check.sub_infos.category import cate
from utils.translate import translate_to_korean_local, translate_to_korean
from utils.compare import find_diff_flags, word_count, find_different_words, find_deleted_words
from utils.user_io import ask_key_to_user
from utils.show_image import show_image

origin_filename, new_filename = 'data_check/origin_caps/original_caps_fixed.txt', 'data_check/new_caps/final_same_caps_ver2.txt'
start_idx_path = 'data_check/start_idx.txt'
diff_pairs_path = 'data_check/different_pairs.json'
# sim_pairs_path = 'data_check/similar_pairs.json'
local_dict_path = 'utils/translator.json'
# strange_idxes_path = 'data_check/strange_idxes.txt'

def save_results(checked_lines, next_idx, myDict, diff_pairs):
    checked_data = "\n".join(checked_lines)
    save_file(checked_data, new_filename)
    save_file([str(next_idx)], start_idx_path)
    save_file(myDict, local_dict_path)
    save_file(diff_pairs, diff_pairs_path)

def call_same_category_words(word):
    new_words = []
    categories = cate()
    for category in categories.keys():
        if word in categories[category]:
            new_words += categories[category]
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


def check_lines(origin_data, new_data, start_idx, myDict, diff_pairs):

    if len(origin_data) != len(new_data):
        print('[wrong inputs] different length')
        return new_data, start_idx, myDict, diff_pairs
    
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
        in_pair_idxes = check_in_pair(diff_word, new_words, diff_pairs)
        if len(in_pair_idxes) != 0:
            new_data[line_idx] = new_capts[random.choice(in_pair_idxes)]
            print(f'(Pass) {new_data[line_idx]}')
            line_idx += 1
            continue

        # pick sentence
        work_key = '-1'
        str_idxes = [str(i) for i in range(len(new_capts)+1)]
        str_idxes += ['a'+i for i in str_idxes]
        while work_key not in ['q', 'e', 'w'] + str_idxes:
            work_key = input('Pick caption idx (quit(q), change origin word(w), change new word(e), show_image(r), translate all(t)) ')
            if work_key == 'r': # show image
                show_image(origin_capt)
            elif work_key == 't': # translate all sentences
                print(f'[origin] {translate_to_korean(origin_capt)}')
                for new_capt_idx, new_capt in enumerate(new_capts):
                    print(f'[{result_key} {capt_idx+1}] {translate_to_korean(new_capt)}')


        if work_key == 'q': # save and quit
            return new_data, line_idx, myDict, diff_pairs
        elif work_key == 'e':  # call other new word
            if diff_word in diff_pairs.keys() and len(diff_pairs[diff_word]) > 4: # auto pick if the origin word's diff pair is already more then 4
                new_word = random.choice(diff_pairs[diff_word])
            else: # ask user about new word
                new_words = call_same_category_words(diff_word)
                choiced = '0'
                while choiced not in ['1', '2']:
                    if choiced == 'q':
                        return new_data, line_idx, myDict, diff_pairs
                    elif choiced == 'e':
                        new_word = new_words.pop()
                    myDict, new_word_trans = translate_to_korean_local(myDict, new_word)
                    choiced = input(f'[{diff_word} -> {new_word} ({new_word_trans})] choose(1), add-in-pair(2), other(e), quit(q) ')
                if choiced == '2': # add in pair
                    diff_pairs = add_in_pair(diff_word, new_word, diff_pairs)

            new_data[line_idx] = origin_capt.replace(diff_word, new_word)
            print(f'(Fixed!) {new_data[line_idx]}')
            line_idx += 1
        elif work_key == 'w':  # pick new origin word to change
            word_sims = call_word_similarities(line_idx)
            word_sims = sorted(word_sims.items(), key = lambda item: item[1])
            
            diff_word = None
            for word_idx, (word, sim) in enumerate(word_sims):
                if diff_word == None:
                    highlighted_capt = origin_capt.replace(word, '{'+word+'}')
                    diff_word_key = input(f'[{word_idx+1}/{len(word_sims)} {sim}] {highlighted_capt} (choose(1), other(w), quit(q)) ')
                    if diff_word_key == 'q':
                        return new_data, line_idx, myDict, diff_pairs
                    elif diff_word_key == '1':
                        diff_word = word
                        new_word = random.choice(call_same_category_words(diff_word))
                        new_data[line_idx] = 'new, '+origin_capt.replace(diff_word, new_word)
        else: # pick 1 sentence & pass
            if work_key[0] == 'a':
                work_key = work_key[1]
                new_word = new_capts[int(work_key)-1].split(' ')[diff_word_idxes[0]]
                diff_pairs = add_in_pair(diff_word, new_word, diff_pairs)
            new_data[line_idx] = new_capts[int(work_key)-1]
            line_idx += 1

    return new_data, line_idx, myDict, diff_pairs
        

        


if __name__=='__main__':
    origin_data = load_file(origin_filename)
    new_data = load_file(new_filename)

    start_idx = int(load_file(start_idx_path)[0])
    myDict = load_file(local_dict_path)
    diff_pairs = load_file(diff_pairs_path)

    checked_data, next_idx, myDict, diff_pairs = check_lines(origin_data, new_data, start_idx, myDict, diff_pairs)
    save_results(checked_data, next_idx, myDict, diff_pairs)

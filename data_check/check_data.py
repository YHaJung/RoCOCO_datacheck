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
# diff_pairs_path = 'data_check/different_pairs.json'
# sim_pairs_path = 'data_check/similar_pairs.json'
# local_dict_path = 'utils/translator.json'
# strange_idxes_path = 'data_check/strange_idxes.txt'

def save_results(checked_lines, next_idx):
    checked_data = "\n".join(checked_lines)
    save_file(checked_data, new_filename)
    save_file([str(next_idx)], start_idx_path)

def call_same_category_words(word):
    new_words = []
    categories = cate()
    for category in categories.keys():
        if word in categories[category]:
            new_words += categories[category]
            new_words.remove(word)

    random.shuffle(new_words)
    return new_words

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


def check_lines(origin_data, new_data, start_idx=0):

    if len(origin_data) != len(new_data):
        print('[wrong inputs] different length')
        return new_data, start_idx
    
    checked_data = new_data
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
        print(f'[origin] {origin_capt_print}')
        for capt_idx, new_capt in enumerate(new_capts_print):
            print(f'[{result_key} {capt_idx+1}] {new_capt}')

        # pick sentence
        work_key = '-1'
        str_idxes = [str(i) for i in range(len(new_capts)+1)]
        while work_key not in ['s', 'e', 'w'] + str_idxes:
            work_key = input('Pick caption idx (save(s), change origin word(w), change new word(e), show_image(r)) ')
            if work_key == 'r':
                show_image(origin_capt)

        if work_key == 's': # save and quit
            return checked_data, line_idx
        elif work_key == 'e':  # call other new word
            diff_word = origin_capt.split(' ')[diff_word_idxes[0]]
            new_words = call_same_category_words(diff_word)

            choiced = '2'
            while choiced not in ['1']:
                if choiced == 's':
                    return checked_data, line_idx
                elif choiced == '2':
                    new_word = new_words.pop()
                choiced = input(f'[{diff_word} -> {new_word}] choose(1), other(2), save(s) ')
            checked_data[line_idx] = origin_capt.replace(diff_word, new_word)
            line_idx += 1
        elif work_key == 'w':  # pick new origin word to change
            word_sims = call_word_similarities(line_idx)
            word_sims = sorted(word_sims.items(), key = lambda item: item[1])
            
            diff_word = None
            for word_idx, (word, sim) in enumerate(word_sims):
                if diff_word == None:
                    highlighted_capt = origin_capt.replace(word, '{'+word+'}')
                    diff_word_key = input(f'[{word_idx+1}/{len(word_sims)} {sim}] {highlighted_capt} (choose(1), other(w)) ')
                    if diff_word_key == '1':
                        diff_word = word
                        new_word = random.choice(call_same_category_words(diff_word))
                        new_data[line_idx] = 'new, '+origin_capt.replace(diff_word, new_word)
        else: # pick 1 sentence & pass
            checked_data[line_idx] = new_capts[int(work_key)-1]
            line_idx += 1

    return checked_data, line_idx
        

        


if __name__=='__main__':
    origin_data = load_file(origin_filename)
    new_data = load_file(new_filename)

    start_idx = int(load_file(start_idx_path)[0])

    checked_data, next_idx = check_lines(origin_data, new_data, start_idx)
    save_results(checked_data, next_idx)

import pandas as pd
import cv2
import random

import sys, os
root_path = os.getcwd()
print(f'root path : {root_path}')
sys.path.append(root_path)

from utils.file_processing import increment_filename, save_file, load_file
from data_check.sub_infos.category import cate
from utils.translate import translate_to_korean_local, translate_to_korean
from utils.compare import find_diff_flags, word_count, find_different_words
from utils.user_io import ask_key_to_user

origin_filename, new_filename = 'data_check/origin_caps/original_caps_fixed.txt', 'data_check/new_caps/final_same_caps_ver2.txt'
start_idx_path = 'data_check/start_idx.txt'
# diff_pairs_path = 'data_check/different_pairs.json'
# sim_pairs_path = 'data_check/similar_pairs.json'
# local_dict_path = 'utils/translator.json'
# strange_idxes_path = 'data_check/strange_idxes.txt'

def save_results(checked_lines, next_idx):
    checked_data = "\n".join(checked_lines)
    save_file(checked_data, new_filename)

def check_lines(origin_data, new_data, start_idx=0):

    if len(origin_data) != len(new_data):
        print('[wrong inputs] different length')
        return new_data, start_idx
    
    checked_data = new_data
    for line_idx, (origin_capt, new_line) in enumerate(zip(origin_data, new_data)):
        if line_idx < start_idx:
            continue

        if new_line[:5] == 'none,':
            result_key = 'none'
            new_capts = [new_line.lstrip('none, ')]
        else:
            result_key = ' +  '
            new_capts = new_line.split('+')[:-1]

        print(f'\n[line {line_idx}]')

        # find and print different word
        diff_word_idxes, origin_capt_print, new_capts_print = find_different_words(origin_capt, new_capts)        
        print(f'[origin] {origin_capt_print}')
        for capt_idx, new_capt in enumerate(new_capts_print):
            print(f'[{result_key} {capt_idx+1}] {new_capt}')

        # pick sentence
        work_key = '-1'
        while (not work_key.isdigit() or int(work_key) not in range(len(new_capts)+1)) and work_key not in ['s']:
            work_key = input('[save(s)]\nPick caption idx ')
        if work_key == 's':
            return checked_data, line_idx
        checked_data[line_idx] = new_capts[int(work_key)-1]

    return checked_data, line_idx
        

        


if __name__=='__main__':
    origin_data = load_file(origin_filename)
    new_data = load_file(new_filename)

    start_idx = int(load_file(start_idx_path)[0])

    checked_data, next_idx = check_lines(origin_data, new_data, start_idx)
    save_results(checked_data, next_idx)

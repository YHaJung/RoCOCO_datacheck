import pandas as pd
import cv2
import random

import sys, os
root_path = os.getcwd()
sys.path.append(root_path)

from utils.file_processing import increment_filename, save_file, load_file
from data_check.downloaded.category import cate
from utils.translate import translate_to_korean_local, translate_to_korean
from utils.compare import find_diff_flags

origin_filename, new_filename = 'data_check/origin_caps/original_caps_fixed.txt', 'data_check/new_caps/same_caps_mod_fixed.txt'
diff_pairs_path = 'data_check/different_pairs.json'
sim_pairs_path = 'data_check/similar_pairs.json'
start_idx_path = 'data_check/last_idx.txt'
local_dict_path = 'utils/translator.json'

def fix_sentence_by_user(first_line, second_line):
    print(f'[1] [{first_line}]')
    print(f'[2] [{second_line}]')
    key = input("While sentence will you fix? first(1), second(2), keep(3), break(0) ")
    while key not in ['0', '1', '2', '3']:
        key = input("While sentence will you fix? first(1), second(2), break(0) ")
    if key == '1':
        fixed_line = input("Enter fixed sentence: ")
        return 1, fixed_line
    elif key == '2':
        fixed_line = input("Enter fixed sentence: ")
        return 2, fixed_line
    elif key == '3':
        return 3, None
    else:
        return 0, None

def fix_lines_length(origin_data, new_data, strange_idxes):

    fixed_origin_lines = origin_data
    fixed_new_lines = new_data

    keep_idxes = []
    
    for line_idx, (origin_line, new_line) in enumerate(zip(origin_data, new_data)):
        origin_words = origin_line.split(' ')
        new_words = new_line.split(' ')

        # make sentence length same
        while len(origin_words) != len(new_words):
            print(f'\n[line {line_idx+1}] sentence length is differenct({len(origin_words)}, {len(new_words)})')
            fix_key, fixed_line = fix_sentence_by_user(origin_line, new_line)
            if fix_key == 1:
                fixed_origin_lines[line_idx] = fixed_line
                origin_words = fixed_line.split(' ')
            elif fix_key == 2:
                fixed_new_lines[line_idx] = fixed_line
                new_words = fixed_line.split(' ')
            elif fix_key == 3:
                keep_idxes.append(line_idx)
            else:
                print(f'[line {line_idx}] stop working...')
                return fixed_origin_lines, fixed_new_lines

    if len(keep_idxes) !=0:
        print(f'\nstrange length keep idxes : {keep_idxes}')

    strange_idxes.update(keep_idxes)
            
    return fixed_origin_lines, fixed_new_lines, strange_idxes
            
def fix_multiple_or_no_change(origin_data, new_data, strange_idxes):  # fix multiple diff word and find not change sentence
    fixed_origin_lines = origin_data
    fixed_new_lines = new_data

    not_change_idxes = []
    keep_idxes = []
    
    for line_idx, (origin_line, new_line) in enumerate(zip(origin_data, new_data)):
        if line_idx in strange_idxes:
            continue

        line_flag = 1 # {0: finish, 1: again, 2: keep(strange)}

        fixed_origin_line = origin_line
        fixed_new_line = new_line

        while line_flag == 1:
            line_flag = 0
            origin_words = fixed_origin_line.split(' ')
            new_words = fixed_new_line.split(' ')

            diff_flag_list = find_diff_flags(origin_words, new_words)

            if diff_flag_list.count(1) == 0:
                not_change_idxes.append(line_idx)
            elif diff_flag_list.count(1) == 1:
                continue
            else:  # multiple changed words
                diff_key_idx = diff_flag_list.index(1)
                for diff_idx, diff_flag in enumerate(diff_flag_list):   # find diff key word
                    if diff_flag == 1:
                        if origin_words[diff_key_idx] in origin_words[diff_idx] and new_words[diff_key_idx] in new_words[diff_idx]:
                            continue
                        elif origin_words[diff_idx] in origin_words[diff_key_idx] and new_words[diff_idx] in new_words[diff_key_idx]:
                            diff_key_idx = diff_idx

                for diff_idx, diff_flag in enumerate(diff_flag_list):    # deal with strange cases
                    if diff_flag == 1:
                        if origin_words[diff_key_idx] not in origin_words[diff_idx] and origin_words[diff_idx] not in origin_words[diff_key_idx]:
                            print(f'\n[line {line_idx}, Word {diff_idx}] Strange! More then two is different. Please check & fix.')
                            fix_key, fixed_line = fix_sentence_by_user(fixed_origin_line, fixed_new_line)
                            if fix_key == 1:
                                fixed_origin_line = fixed_line
                                fixed_origin_lines[line_idx] = fixed_origin_line
                                line_flag = 1
                            elif fix_key == 2:
                                fixed_new_line = fixed_line
                                fixed_new_lines[line_idx] = fixed_new_line
                                line_flag = 1
                            elif fix_key == 3:
                                keep_idxes.append(line_idx)
                                line_flag = 3
                            else:
                                print(f'[line {line_idx}] stop working...')
                                return fixed_origin_lines, fixed_new_lines
                            break
                
                if line_flag == 1:
                    continue
                elif line_flag == 2:
                    break
                else:
                    diff_key = origin_words[diff_key_idx]
                    for diff_idx, diff_flag in enumerate(diff_flag_list):
                        if diff_flag == 1 and diff_key != origin_words[diff_idx]:
                            new_words[diff_idx] = origin_words[diff_idx]
                    fixed_new_line = " ".join(new_words)
                    fixed_new_lines[line_idx] = fixed_new_line
                    
    if len(not_change_idxes) !=0:
        print(f'\nnot changed idxes : {not_change_idxes}\n')
    if len(keep_idxes) !=0:
        print(f'multiple words keep idxes : {keep_idxes}\n')

    strange_idxes.update(not_change_idxes + keep_idxes)

    return fixed_origin_lines, fixed_new_lines, strange_idxes

def show_image(origin_words):
    img_info_list = load_file('data_check/downloaded/coco_karpathy_test.json')
    origin_line = " ".join(origin_words)
    for img_info in img_info_list:
        img_captions = [ img_cap.rstrip('\n').rstrip(' \.').lower().replace(',', ' ,').replace('\'', ' \'').replace('  ', ' ').replace("\"", "") for img_cap in img_info['caption']]
        origin_line = origin_line.replace("`` ", "").replace("'' ", "")
        if origin_line in img_captions:
            img_path = img_info['image']
            img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
            img = cv2.resize(img, (400, 300)) 
            cv2.namedWindow("window1")   # create a named window
            cv2.imshow("window1", img)            
            cv2.moveWindow("window1", 400, 50)   # Move it to (40, 30)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def add_in_pair(origin_word, new_word, pair):
    if origin_word in pair.keys():
        pair[origin_word].append(new_word)
    else:
        pair[origin_word] = [new_word]
    return pair

def check_similarity(diff_key_idx, origin_words, new_words, diff_pairs, sim_pairs, local_dict):
    origin_diff_word, new_diff_word = origin_words[diff_key_idx], new_words[diff_key_idx]

    print_origin_line = ''
    print_new_line = ''
    for word_idx in range(len(origin_words)):
        if origin_words[word_idx] == origin_diff_word:
            print_origin_line += f'[{origin_words[word_idx]}] '
            print_new_line += f'[{new_words[word_idx]}] '
        else:
            print_origin_line += f'{origin_words[word_idx]} '
            print_new_line += f'{new_words[word_idx]} '
    

    local_dict, kor_origin_word = translate_to_korean_local(local_dict, origin_diff_word)
    local_dict, kor_new_word = translate_to_korean_local(local_dict, new_diff_word)
    print_origin_line += f' ({kor_origin_word})'
    print_new_line += f' ({kor_new_word})'

    print(f'\n{print_origin_line}')
    print(print_new_line)
    
    if origin_diff_word in diff_pairs.keys() and new_diff_word in diff_pairs[origin_diff_word]:
        return "different", diff_pairs, sim_pairs, local_dict
    elif origin_diff_word in sim_pairs.keys() and new_diff_word in sim_pairs[origin_diff_word]:
        return "similar", diff_pairs, sim_pairs, local_dict
    else:
        # ask judgeability (can judge only with the words)
        judgeability = input("Can you judge it only with the words? Yes(1), No-Show Image(2), Translate Sentence(3), Fix-Translatation(4, 5) ")

        while judgeability not in ['1', '2']:
            if judgeability == '3':
                origin_sentence = " ".join(origin_words)
                new_sentence = " ".join(new_words)
                print(f'{origin_sentence} -> {translate_to_korean(origin_sentence)}')
                print(f'{new_sentence} -> {translate_to_korean(new_sentence)}')
            elif judgeability == '4':
                local_dict[origin_diff_word] = input(f'[{origin_diff_word}] : ')
            elif judgeability == '5':
                local_dict[new_diff_word] = input(f'[{new_diff_word}] : ')
            judgeability = input("Can you judge it only with the words? Yes(1), No-Show Image(2), Translate Sentence(3), Fix-Translatation(4, 5) ")
        
        if judgeability == '2':
            show_image(origin_words)

        # ask differency
        key = input("Are they different? Yes(1), No(2), Keep(3), exit(0) ")
        while key not in ['0', '1', '2', '3']:
            key = input("Are they different? Yes(1), No(2), Keep(3), exit(0) ")

        if key == '1':
            if judgeability == '1':
                diff_pairs = add_in_pair(origin_diff_word, new_diff_word, diff_pairs)
            return "different", diff_pairs, sim_pairs, local_dict
        elif key == '2':
            if judgeability == '1':
                sim_pairs = add_in_pair(origin_diff_word, new_diff_word, sim_pairs)
            return "similar", diff_pairs, sim_pairs, local_dict
        elif key == '3':
            return "keep", diff_pairs, sim_pairs, local_dict
        else:
            return "exit", diff_pairs, sim_pairs, local_dict

def call_new_keyword(origin_word, diff_pairs, sim_pairs, local_dict):
    if origin_word in diff_pairs.keys() and len(diff_pairs[origin_word]) > 4:
        fixed_new_word = random.choice(diff_pairs[origin_word])
        print(f'[fixed] {origin_word} -> {fixed_new_word}')
        return fixed_new_word, diff_pairs, local_dict

    categories = cate()
    for category in categories.keys():
        if origin_word in categories[category]:
            user_ok = '2'
            checked_words = [origin_word]
            fixed_new_word = random.choice(categories[category])
            while (fixed_new_word in checked_words) or (origin_word in sim_pairs.keys() and fixed_new_word in sim_pairs[origin_word]):
                checked_words.append(fixed_new_word)
                fixed_new_word = random.choice(categories[category])            
            local_dict, kor_new_word = translate_to_korean_local(local_dict, fixed_new_word)
            user_ok = input(f'{origin_word} -> {fixed_new_word} ({kor_new_word}): Add in Pair(1), Only for this sentence(2), Other Word(3), Pick myself(4), exit(0) ')
            while user_ok not in ['0', '1', '2', '4']:
                if user_ok == '3':
                    checked_words.append(fixed_new_word)
                    fixed_new_word = random.choice(categories[category])
                    while (fixed_new_word in checked_words) or (origin_word in sim_pairs.keys() and fixed_new_word in sim_pairs[origin_word]):
                        checked_words.append(fixed_new_word)
                        fixed_new_word = random.choice(categories[category])      
                    local_dict, kor_new_word = translate_to_korean_local(local_dict, fixed_new_word)
                user_ok = input(f'{origin_word} -> {fixed_new_word} ({kor_new_word}): Add in Pair(1), Only for this sentence(2), Other Word(3), Pick myself(4), exit(0) ')                                                        
            if user_ok == '1':
                diff_pairs = add_in_pair(origin_word, fixed_new_word, diff_pairs)
                return fixed_new_word, diff_pairs, local_dict
            elif user_ok == '2':
                return fixed_new_word, diff_pairs, local_dict
            elif user_ok == '4':
                print(f'origin word : {origin_word}')
                print(f'{category} category : {categories[category]}')
                fixed_new_word = input('fixed new word(exit(0)) : ')
                while fixed_new_word not in fixed_new_word and fixed_new_word != '0':
                    fixed_new_word = input('fixed new word(exit(0)) : ')
                if fixed_new_word == '0':
                    return '0', diff_pairs, local_dict
                else:
                    diff_pairs = add_in_pair(origin_word, fixed_new_word, diff_pairs)
                    return fixed_new_word, diff_pairs, local_dict
            else:
                return '0', diff_pairs, local_dict


def check_similar_words(origin_data, new_data, local_dict, strange_idxes, start_idx=0):
    fixed_new_lines = new_data

    sim_pairs = load_file(sim_pairs_path)
    diff_pairs = load_file(diff_pairs_path)
    
    for line_idx, (origin_line, new_line) in enumerate(zip(origin_data, new_data)):
        if line_idx < start_idx or line_idx in strange_idxes:
            continue
        origin_words = origin_line.split(' ')
        new_words = new_line.split(' ')

        diff_key_idx = find_diff_flags(origin_words, new_words).index(1)

        key, diff_pairs, sim_pairs, local_dict = check_similarity(diff_key_idx, origin_words, new_words, diff_pairs, sim_pairs, local_dict)
        print(f'[line {line_idx}] ({key})')

        if key == "different":
            continue
        elif key == "similar":
            fixed_new_word, diff_pairs, local_dict = call_new_keyword(origin_words[diff_key_idx], diff_pairs, sim_pairs, local_dict)
            if fixed_new_word == '0': # exit
                print(f'[line {line_idx}] stop working...')
                return fixed_new_lines, diff_pairs, sim_pairs, strange_idxes, line_idx, local_dict
            new_words[diff_key_idx] = fixed_new_word
            fixed_new_lines[line_idx] = " ".join(new_words)
        elif key == "keep":
            strange_idxes.update([line_idx])
        else: # exit
            print(f'[line {line_idx}] stop working...')
            return fixed_new_lines, diff_pairs, sim_pairs, strange_idxes, line_idx, local_dict

    return fixed_new_lines, diff_pairs, sim_pairs, strange_idxes, line_idx, local_dict

if __name__== '__main__':
    origin_data = load_file(origin_filename)
    new_data = load_file(new_filename)
    local_dict = load_file(local_dict_path)
    strange_idxes = set([int(line) for line in load_file('strange_idxes.txt')])
    print(f'start strange idxes : {sorted(list(strange_idxes))}\n')
    # print(new_data)

    fixed_origin_lines, fixed_new_lines, strange_idxes = fix_lines_length(origin_data, new_data, strange_idxes)
    fixed_origin_lines, fixed_new_lines, strange_idxes = fix_multiple_or_no_change(fixed_origin_lines, fixed_new_lines, strange_idxes)

    start_idx = int(load_file(start_idx_path)[0])
    print(f'start with line {start_idx}')
    fixed_new_lines, diff_pairs, sim_pairs, strange_idxes, line_idx, local_dict = check_similar_words(fixed_origin_lines, fixed_new_lines, local_dict, strange_idxes, start_idx)
    print(f'last strange idxes : {strange_idxes}')

    # save results
    fixed_origin_lines = [line + ' .\n' for line in fixed_origin_lines]
    fixed_new_lines = [line + ' .\n' for line in fixed_new_lines]
    save_file(fixed_origin_lines, origin_filename)
    save_file(fixed_new_lines, new_filename)
    print(f'saved results in \n{origin_filename}, \n{new_filename}')

    strange_idxes_string = "\n".join(map(str, sorted(strange_idxes)))
    save_file(strange_idxes_string, 'strange_idxes.txt')
    print('saved strange idxes')

    
    for sim_key in sim_pairs.keys():
        sim_pairs[sim_key] = sorted(list(set(sim_pairs[sim_key])))
    for diff_key in diff_pairs.keys():
        diff_pairs[diff_key] = sorted(list(set(diff_pairs[diff_key])))
    save_file(diff_pairs, diff_pairs_path)
    save_file(sim_pairs, sim_pairs_path)
    print('saved diff & sim pairs')

    save_file([str(line_idx)], start_idx_path)
    print(f'saved last idx {line_idx} at {start_idx_path}')

    save_file(local_dict, local_dict_path)
    print(f'saved local dict at {local_dict_path}')


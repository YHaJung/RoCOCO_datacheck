import pandas as pd

import sys, os
root_path = os.getcwd()
sys.path.append(os.path.join(root_path, '..'))

from utils.file_processing import increment_filename, save_file, load_file

def read_txt_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    lines = [ line.rstrip('\n').rstrip(' \.').lower() for line in lines]
    return lines

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
        print('quit working...')
        return 0, None

def fix_lines_length(origin_data, new_data):

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
                return fixed_origin_lines, fixed_new_lines

    if len(keep_idxes) !=0:
        print(f'\nstrange length keep idxes : {keep_idxes}')
            
    return fixed_origin_lines, fixed_new_lines, keep_idxes

def find_diff_flags(origin_words, new_words):
    diff_flag_list = [0]*len(origin_words)
    for word_idx in range(len(origin_words)):
        if origin_words[word_idx] != new_words[word_idx]:
            diff_flag_list[word_idx] = 1
    return diff_flag_list
            
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
        print(f'\nnot changed idxes : {not_change_idxes}')
    if len(keep_idxes) !=0:
        print(f'multiple words keep idxes : {keep_idxes}')
    strange_idxes = strange_idxes + not_change_idxes + keep_idxes

    return fixed_origin_lines, fixed_new_lines, strange_idxes

def check_similarity(diff_key_idx, origin_words, new_words, diff_pairs, similar_pairs):
    origin_diff_word, new_diff_word = origin_words[diff_key_idx], new_words[diff_key_idx]
    if origin_diff_word in diff_pairs.keys() and new_diff_word in diff_pairs[origin_diff_word]:
        return "different", similar_pairs, diff_pairs
    elif origin_diff_word in similar_pairs.keys() and new_diff_word in similar_pairs[origin_diff_word]:
        return "similar", similar_pairs, diff_pairs
    else:
        print_origin_line = ''
        print_new_line = ''
        for word_idx in range(len(origin_words)):
            if origin_words[word_idx] == origin_diff_word:
                print_origin_line += f'({origin_words[word_idx]}) '
                print_new_line += f'({new_words[word_idx]}) '
            else:
                print_origin_line += f'{origin_words[word_idx]} '
                print_new_line += f'{new_words[word_idx]} '
        print('\n', print_origin_line)
        print(print_new_line)
        key = input("Are they different? Yes(1), No(2), Check(3), exit(0)")
        while key not in ['0', '1', '2', '3']:
            key = input("Are they different? Yes(1), No(2), Check(3), exit(0)")
        if key == '1':
            if origin_diff_word in diff_pairs.keys():
                diff_pairs[origin_diff_word].append(new_diff_word)
            else:
                diff_pairs[origin_diff_word] = [new_diff_word]
            return "different", similar_pairs, diff_pairs
        elif key == '2':
            if origin_diff_word in similar_pairs.keys():
                similar_pairs[origin_diff_word].append(new_diff_word)
            else:
                similar_pairs[origin_diff_word] = [new_diff_word]
            return "similar", similar_pairs, diff_pairs
        elif key == '3':
            return "check", similar_pairs, diff_pairs
        else:
            return "exit", similar_pairs, diff_pairs

def check_similar_words(origin_data, new_data, strange_idxes):
    keep_idxes = []

    checked_lines = []
    fixed_new_lines = new_data

    similar_pairs = load_file('similar_pairs.json')
    diff_pairs = load_file('different_pairs.json')
    
    for line_idx, (origin_line, new_line) in enumerate(zip(origin_data, new_data)):
        if line_idx in strange_idxes:
            continue
        origin_words = origin_line.split(' ')
        new_words = new_line.split(' ')

        diff_key_idx = find_diff_flags(origin_words, new_words).index(1)

        key = check_similarity(diff_key_idx, origin_words, new_words, diff_pairs, similar_pairs)
        if key == "check":
            print(f'[line {line_idx}] check')

        if key == "different":
            continue
        elif key == "similar":
            # change_keyword()
            print(f'[line {line_idx}] similar')
        # else:

    return fixed_new_lines, similar_pairs, diff_pairs, strange_idxes

if __name__=='__main__':
    # origin_filename, new_filename = 'origin_caps/original_caps_fixed_1.txt', 'new_caps/same_caps_mod_fixed_1.txt'
    # _, save_origin_filename = increment_filename('origin_caps/original_caps_fixed.txt')
    # _, save_new_filename = increment_filename('new_caps/same_caps_mod_fixed.txt')
    origin_filename, save_origin_filename = increment_filename('origin_caps/original_caps_fixed.txt')
    new_filename, save_new_filename = increment_filename('new_caps/same_caps_mod_fixed.txt')

    origin_data = read_txt_file(origin_filename)
    new_data = read_txt_file(new_filename)
    # print(new_data)

    fixed_origin_lines, fixed_new_lines, strange_idxes = fix_lines_length(origin_data, new_data)
    fixed_origin_lines, fixed_new_lines, strange_idxes = fix_multiple_or_no_change(fixed_origin_lines, fixed_new_lines, strange_idxes)
    fixed_new_lines, similar_pairs, diff_pairs, strange_idxes = check_similar_words(fixed_origin_lines, fixed_new_lines, strange_idxes)

    # save results
    fixed_origin_lines = [line + ' .\n' for line in fixed_origin_lines]
    fixed_new_lines = [line + ' .\n' for line in fixed_new_lines]
    save_file(fixed_origin_lines, save_origin_filename)
    save_file(fixed_new_lines, save_new_filename)
    print(f'saved results in \n{save_origin_filename}, \n{save_new_filename}')

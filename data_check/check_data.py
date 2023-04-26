import pandas as pd

import sys, os
root_path = os.getcwd()
sys.path.append(os.path.join(root_path, '..'))

from utils.file_processing import increment_filename, save_file

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
        print(f'strange length keep idxes : {keep_idxes}')
            
    return fixed_origin_lines, fixed_new_lines
                
# def find_diff_lines():
#     for word_idx in range(len(origin_words)):
#         if origin_words[word_idx] != new_words[word_idx]:
#             diff_flag_list[word_idx] = 1
    
#     if diff_flag_list.count(1) != 1:
#         print(diff_flag_list.count(1))


#     # if diff_word_origin not in origin_word and origin_word not in diff_word_origin:
#     #     strange_idxes.append(idx+1)

#     return 0, 0
#     # df = pd.DataFrame({'origin word':origin_word_types, 'new word':new_word_types, 'origin data':origin_data, 'new data':new_data})
            

if __name__=='__main__':
    # origin_filename, new_filename = 'origin_caps/original_caps_fixed.txt', 'new_caps/same_caps_mod_fixed.txt'
    # _, save_origin_filename = increment_filename('origin_caps/original_caps_fixed.txt')
    # _, save_new_filename = increment_filename('new_caps/same_caps_mod_fixed.txt')
    origin_filename, save_origin_filename = increment_filename('origin_caps/original_caps_fixed.txt')
    new_filename, save_new_filename = increment_filename('new_caps/same_caps_mod_fixed.txt')

    origin_data = read_txt_file(origin_filename)
    new_data = read_txt_file(new_filename)
    # print(new_data)

    fixed_origin_lines, fixed_new_lines= fix_lines_length(origin_data, new_data)
    # save results
    fixed_origin_lines = [line + ' .\n' for line in fixed_origin_lines]
    fixed_new_lines = [line + ' .\n' for line in fixed_new_lines]

    save_file(fixed_origin_lines, save_origin_filename)
    save_file(fixed_new_lines, save_new_filename)
    print(f'saved results in \n{save_origin_filename}, \n{save_new_filename}')

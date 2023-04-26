import pandas as pd

import sys
sys.path.append('/home/hajung/psg-iccv')
from utils.file_processing import increment_filename, save_file

def read_txt_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    lines = [ line.rstrip('\n').rstrip(' \.') for line in lines]
    return lines

def find_diff_words(origin_data, new_data):
    if len(origin_data) != len(new_data):
        print('The files\' lengths are different. Please check them.')
        return 0
    df = pd.DataFrame()
    strange_idxes = []
    null_idxes = []

    fixed_origin_lines = origin_data
    fixed_new_lines = new_data
    
    for line_idx, (origin_line, new_line) in enumerate(zip(origin_data, new_data)):
        origin_words = origin_line.split(' ')
        new_words = new_line.split(' ')
        fixed_new_line = new_line

        diff_flag_list = [0]*len(origin_words)

        # make sentence length same
        while len(origin_words) != len(new_words):
            print(f'<line {line_idx+1}>')
            print(f'sentence length is differenct({len(origin_words)}, {len(new_words)})')
            print(f'origin sentence : {origin_line}')
            print(f'new sentence : {new_line}')
            key = input("While sentence will you fix? origin(1), new(2), break(0) ")
            while key != '1' and key != '2' and key != '0':
                print('please press 1 or 2')
                key = input("While sentence will you fix? origin(1), new(2), break(0) ")
            if key == '1':
                fixed_origin_line = input("Enter fixed sentence: ")
                fixed_origin_lines[line_idx] = fixed_origin_line
                origin_words = fixed_origin_line.split(' ')
            elif key == '2':
                fixed_new_line = input("Enter fixed sentence: ")
                fixed_new_lines[line_idx] = fixed_new_line
                new_words = fixed_new_line.split(' ')
            else:
                print('quit and saving working...')
                return fixed_origin_lines, fixed_new_lines
                

        for word_idx in range(len(origin_words)):
            if origin_words[word_idx] != new_words[word_idx]:
                diff_flag_list[word_idx] = 1
        
        if diff_flag_list.count(1) != 1:
            print(diff_flag_list.count(1))


                        # if diff_word_origin not in origin_word and origin_word not in diff_word_origin:
                        #     strange_idxes.append(idx+1)

        # df.append({'origin word':diff_word_origin, 'new word':diff_word_new, 'origin_data':origin_line, 'new_data':new_line}, ignore_index=True)
    print(f'strange idxes : {sorted(set(strange_idxes))}')
    print(f'null idxes : {null_idxes}')

    return 0, 0
    # df = pd.DataFrame({'origin word':origin_word_types, 'new word':new_word_types, 'origin data':origin_data, 'new data':new_data})
            

if __name__=='__main__':
    origin_filename = 'origin_caps/original_caps_fixed_2.txt'
    new_filename = 'new_caps/same_caps_mod_fixed_2.txt'

    origin_data = read_txt_file(origin_filename)
    new_data = read_txt_file(new_filename)
    # print(new_data)
    fixed_origin_lines, fixed_new_lines = find_diff_words(origin_data, new_data)

    fixed_origin_lines = [line + ' .\n' for line in fixed_origin_lines]
    fixed_new_lines = [line + ' .\n' for line in fixed_new_lines]
    save_file(fixed_origin_lines, increment_filename(origin_filename))
    save_file(fixed_new_lines, increment_filename(new_filename))


    # dog slice , cord and simple red digital camera
    # A flip up cellphone with keypad on top of a book
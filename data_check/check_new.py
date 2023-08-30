# check a line whether it is already checked
import sys, os
root_path = os.getcwd()
sys.path.append(root_path)

from utils.file_processing import save_file, load_file
from utils.show_image import refine_string

def check_refined(ver2s, line_idx):
    ver1_start = load_file('data_check/ver1/fianl_same_caps_ver1_start.txt')
    ver1 = ver1_start[line_idx].strip(' .')
    if  str(line_idx) in load_file('data_check/ver1/strange_idxes.txt'): # strange idx
        return 0, ver1
    if len(ver2s) != 1: # multiple caption
        return 1, ver1
    if ver1 != ver2s[0].strip(' .'): # different caption
        return 2, ver1
    else: # pass
        ver1_checked = load_file('data_check/ver1/same_caps_mod_fixed_ver1.txt')
        return 3, ver1_checked[line_idx]
    
def check_refined_count(ver1, ver2s, line_idx):
    if  str(line_idx) in load_file('data_check/ver1/strange_idxes.txt'): # strange idx
        return 0
    if len(ver2s) != 1: # multiple caption
        return 1
    if ver1 != ver2s[0].strip(' .'): # different caption
        return 2
    else: # pass
        return 3


if __name__=='__main__':
    ver2_checked = load_file('data_check/new_caps/final_same_caps_ver2.txt')
    
    strange_idx_count = 0
    multiple_capt_count = 0
    diff_count = 0
    diff_count_done = 0
    same_count = 0

    ver1_start = load_file('data_check/ver1/fianl_same_caps_ver1_start.txt')

    done_idx = int(load_file('data_check/start_idx.txt')[0])
    for line_idx in range(16000):
        ver2_line = refine_string(ver2_checked[line_idx])
        if ver2_line[:4] == 'none':
            ver2s = [ver2_line[4:]]
        elif ver2_line[:3] == 'new':
            ver2s = [ver2_line[3:]]
        else:
            result_key = ' +  '
            ver2s = ver2_line.split('+')
            if len(ver2s) > 1:
                ver2s = ver2s[:-1]
        ver2s = [ver2.strip(' ') for ver2 in ver2s]

        ver1 = ver1_start[line_idx].strip(' .')
        key = check_refined_count(ver1, ver2s, line_idx)   
        if key in [0, 1, 2] and line_idx < done_idx:
            diff_count_done += 1
        elif key in [0, 1, 2] and line_idx >= done_idx:
            diff_count += 1
        else:
            same_count +=1

    print(diff_count_done, diff_count, same_count)
    print(diff_count_done + diff_count + same_count)
        # else:
        #     print(f'line {line_idx}')
        #     print([ver1])
        #     print(ver2s, '\n')
        
    # print(count_same)
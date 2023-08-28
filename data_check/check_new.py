# check a line whether it is already checked
import sys, os
root_path = os.getcwd()
sys.path.append(root_path)

from utils.file_processing import save_file, load_file
from utils.show_image import refine_string

def check_refined(ver1, ver2s, line_idx):
    if str(line_idx) in load_file('data_check/ver1/strange_idxes.txt'):
        return 0
    elif len(ver2s) != 1 or ver1 != ver2s[0]:
        return 0
    else:
        return 1


if __name__=='__main__':
    ver1_start = load_file('data_check/ver1/fianl_same_caps_ver1_start.txt')
    ver1_checked = load_file('data_check/ver1/same_caps_mod_fixed_ver1.txt')
    ver2_checked = load_file('data_check/new_caps/final_same_caps_ver2.txt')
    
    count_same = 0
    for line_idx in range(16000):
        ver1 = refine_string(ver1_start[line_idx])
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
                
        if check_refined(ver1, ver2s, line_idx):
            count_same += 1
        else:
            print(f'line {line_idx}')
            print([ver1])
            print(ver2s, '\n')
        
    print(count_same)
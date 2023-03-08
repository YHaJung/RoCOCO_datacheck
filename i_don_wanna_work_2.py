from glob import glob
import pandas as pd
import os

'''
경로 : file_path(default : "/disk2/pseulki/coco_retrieval_results/*/*/*/*.txt")
내용물 : 오른 쪽 형태의 txt. {"txt_r1": 44.62, "txt_r5": 80.78, "txt_r10": 89.52, "txt_r_mean": 71.64, "false_rate": 37.88}

위 형태로 저장된 모든 결과물을 csv로 출력한다.
경로 폴더에 따라 coloumn을 구분하여 표시한다.

출력할 정보 : values(default : {'r1':'x', 'r5':'x', 'false_rate':'x'})
'''

def read_txt(file_path):
    glob_list = glob(file_path, recursive=True)
    final_line_list = []
    for file in glob_list:
        with open(file, 'r') as f:
            for line in f:   # 결과물이 여러줄일 경우, 마지막 줄만 읽는다.
                pass
            values = {'r1':'x', 'r5':'x', 'false_rate':'x'}
            for score_key in values.keys():
                if f'{score_key}":' in line:
                    value = line.split(f'{score_key}":')[1]
                    value = value.split('}')[0]
                    value = value.split(',')[0]
                    values[score_key] = value
            final_line_list.append(values)
    return glob_list, final_line_list

def make_csv(glob_list, final_line_list):
    df = pd.DataFrame()
    for glob_one, final_line in zip(glob_list, final_line_list):
        path_list = glob_one.split('/')
        for i, path_one in enumerate(path_list[4:]):
            final_line[f'path_{i}']=path_one
        df = df.append(final_line, ignore_index=True)
            
    df.to_csv(f'./result.csv', index=True)

if __name__ == '__main__':
    file_path = "/disk2/pseulki/coco_retrieval_results/*/*/*/*.txt"
    glob_list, final_line_list = read_txt(file_path)
    make_csv(glob_list, final_line_list)
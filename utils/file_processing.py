import os
import json, pickle

def increment_filename(filename):
    pure_filename = filename.split('.')[0]
    file_type = filename.split('.')[-1]
    last_idx = 0
    while os.path.exists(filename):
        last_idx +=1
        filename = pure_filename+'_'+str(last_idx)+'.'+file_type

    return filename


def make_path(filepath):
    file_dirs = filepath.split('/')[:-1]

    file_dir = '/' if filepath[0] == '/'else ''
    for dir in file_dirs:
        file_dir = os.path.join(file_dir, dir)

    os.makedirs(file_dir, exist_ok=True)

def save_file(data, filepath):
    make_path(filepath)

    extension = filepath.split('.')[-1]
    if extension == 'json':
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent="\t")
    elif extension == 'pickle' or extension=='pkl':
        with open(filepath, 'wb') as f:
            pickle.dump(data, f, protocol=4)
    elif extension == 'txt':
        with open(filepath, 'w') as f:
            f.writelines(data)
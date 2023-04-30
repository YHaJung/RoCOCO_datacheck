import os
import json, pickle

def increment_filename(filename):
    pure_filename = filename.split('.')[0]
    file_type = filename.split('.')[-1]
    
    next_idx = 1
    next_file_name = pure_filename+'_'+str(next_idx)+'.'+file_type
    while os.path.exists(next_file_name):
        next_idx +=1
        next_file_name = pure_filename+'_'+str(next_idx)+'.'+file_type

    last_file_name = pure_filename+'_'+str(next_idx-1)+'.'+file_type

    return last_file_name, next_file_name


def make_path(filepath):
    file_dirs = filepath.split('/')[:-1]

    file_dir = '/' if filepath[0] == '/'else ''
    for dir in file_dirs:
        file_dir = os.path.join(file_dir, dir)

    if file_dir not in ['', '/']:
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

def load_file(filepath):
    extension = filepath.split('.')[-1]
    extensions = {'json':json, 'pickle':pickle, 'pkl':pickle}
    if extension in extensions.keys():
        with open(filepath, 'rb') as file:
            results = extensions[extension].load(file)
    else: # txt
        with open(filepath, 'r') as file:
            results = file.readlines()
    
    return results
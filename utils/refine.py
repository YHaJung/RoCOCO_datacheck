

from file_processing import load_file, save_file

def remove_none_and_plus(start_path, result_path):
    new_data_lines = load_file(start_path)
    for idx, new_line in enumerate(new_data_lines):
        if new_line[:6] == "none, ":
            new_data_lines[idx] = new_line[6:]
        elif new_line[-1] == '+':
            new_data_lines[idx] = new_line[:-1]
    checked_new_data = "\n".join(new_data_lines)
    save_file(checked_new_data, result_path)

if __name__=='__main__':
    remove_none_and_plus('data_check/new_caps/final_same_caps_ver2_start.txt', 'data_check/new_caps/final_same_caps_reformed.txt')
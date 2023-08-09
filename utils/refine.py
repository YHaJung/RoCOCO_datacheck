

from file_processing import load_file, save_file

new_data_lines = load_file('data_check/new_caps/final_same_caps_ver2_start.txt')
# print(new_data_lines)
for idx, new_line in enumerate(new_data_lines):
    if new_line[:6] == "none, ":
        new_data_lines[idx] = new_line[6:]
    elif new_line[-1] == '+':
        new_data_lines[idx] = new_line[:-1]
# print(new_data_lines[:10])
checked_new_data = "\n".join(new_data_lines)
save_file(checked_new_data, 'data_check/new_caps/final_same_caps_reformed.txt')
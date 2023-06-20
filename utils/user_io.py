

def ask_key_to_user(question, key_dict):

    key_dict_string = ''
    for key in key_dict.keys():
        if key != '0':
            key_dict_string += f'{key_dict[key]}({key}), '
    key_dict_string += 'exit(0) '

    key = input(f"{question} {key_dict_string} ")
    while key not in key_dict.keys():
        key = input(f"{question} {key_dict_string} ")

    return key

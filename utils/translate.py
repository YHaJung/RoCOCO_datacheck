
import googletrans

def translate_to_korean(word):
    translator = googletrans.Translator()
    again_flag = True
    while again_flag:
        try:
            new_word = translator.translate(word, src='en', dest='ko').text
            again_flag = False
        except:
            again_flag = True
    return new_word

def translate_to_korean_local(myDict, word):
    if word in myDict.keys():
        return myDict[word]
    else:
        print(f'The word [{word}] is not in local dict. Lets use google translater.')
        return translate_to_korean(word)
    
def translate_all_to_korean(list):
    myDict = {}
    dict_len = len(list)
    for idx, item in enumerate(list):
        myDict[item] = translate_to_korean(item)
        print(f'[{idx}/{dict_len}] {item} -> {myDict[item]}')
    return myDict

if __name__=='__main__':
    from file_processing import save_file


    # category file 속 모든 단어 번역 & 저장
    import sys, os
    root_path = os.getcwd()
    sys.path.append(os.path.join(root_path, '..'))

    from data_check.downloaded.category import cate
    word_category = cate()

    dict_file = '../data_check/translator.json'
    all_words = set(word_category.keys())
    for word_key in word_category.keys():
        all_words.update(word_category[word_key])
    print(all_words)
    translate_dict = translate_all_to_korean(all_words)

    save_file(translate_dict, dict_file)

    # start_idx, end_idx = 858, 860
    # first_lines = load_file('../data_check/origin_caps/original_caps_fixed.txt')[start_idx:end_idx]
    # second_lines = load_file('../data_check/new_caps/same_caps_mod_fixed.txt')[start_idx:end_idx]

    # translate_dict = {}
    # # input_words = load_file(dict_file)
    # for line_idx in range(len(first_lines)):
    #     first_words = first_lines[line_idx].split(' ')
    #     second_words = second_lines[line_idx].split(' ')
    #     diff_flags = find_diff_flags(first_words, second_words)
    #     for word_idx, diff_flag in enumerate(diff_flags):
    #         if diff_flag == 1:
    #             if first_words[word_idx] not in translate_dict.keys():
    #                 translate_dict[first_words[word_idx]] = translate_to_korean(first_words[word_idx])
    #             if second_words[word_idx] not in translate_dict.keys():
    #                 translate_dict[second_words[word_idx]] = translate_to_korean(second_words[word_idx])
    #     print(f'done line {start_idx+line_idx}')


def find_diff_flags(origin_words, new_words):
    diff_flag_list = [0]*len(origin_words)
    for word_idx in range(len(origin_words)):
        if origin_words[word_idx] != new_words[word_idx]:
            diff_flag_list[word_idx] = 1
    return diff_flag_list


def word_count(line):
    words = line.split(' ')
    return len(words)
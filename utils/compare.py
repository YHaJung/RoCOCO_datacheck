def highlight_given_word(sentence, given_word):
    words = sentence.split(' ')
    for word_idx, word in enumerate(words):
        if word == given_word:
            words[word_idx] = '{'+word+'}'
    return " ".join(words)

def replace_word(sentence, origin_word, new_word):
    words = sentence.split(' ')
    for word_idx, word in enumerate(words):
        if word == origin_word:
            words[word_idx] = new_word
    return " ".join(words)

def find_diff_flags(origin_words, new_words):
    diff_flag_list = [0]*len(origin_words)
    for word_idx in range(len(origin_words)):
        if origin_words[word_idx] != new_words[word_idx]:
            diff_flag_list[word_idx] = 1
    return diff_flag_list

def find_different_words(sentence, sentence_list):
    words = sentence.split()
    different_words = []
    highlighted_sentences = []

    for i, s in enumerate(sentence_list):
        curr_words = s.split()
        highlighted_sentence = s

        for j in range(len(words)):
            if j < len(curr_words):
                if words[j] != curr_words[j]:
                    different_words.append(j)
                    curr_words[j] = '{' + curr_words[j] + '}'
        highlighted_sentences.append(" ".join(curr_words))

    for j in range(len(words)):
        if j in different_words:
            words[j] = '{'+words[j]+'}'
    highlighted_sentence = " ".join(words)

    return different_words, highlighted_sentence, highlighted_sentences

def find_deleted_words(first_sentence, second_sentence):
    first_words = first_sentence.split()
    second_words = second_sentence.split()

    for i, word in enumerate(first_words):
        if i >= len(second_words) or word != second_words[i]:
            return word




def word_count(line):
    words = line.split(' ')
    return len(words)
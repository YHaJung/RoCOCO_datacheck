import random

import sys, os
root_path = os.getcwd()
print(f'root path : {root_path}')
sys.path.append(root_path)

from utils.file_processing import save_file, load_file

categories_path = 'data_check/sub_infos/category.json'

def call_words_by_category(word, category_type = 'same'):
    new_words = []
    categories = load_file(categories_path)
    for category in categories.keys():
        if (category_type == 'same' and word in categories[category]) \
            or (category_type == 'diff' and word not in categories[category]):
            new_words += categories[category]

    if len(new_words) == 0:
        print('(Warning!) This word does not contained in any category.')
        print(f'[categories] {categories.keys()}')
        category = input('choose category name : ')
        new_words = categories[category]
        categories[category].append(word)
        save_file(categories, categories_path)
    
    if word in new_words:
        new_words.remove(word)

    random.shuffle(new_words)
    return new_words

def call_word_by_bart():
    bert_words_path = 'data_check/sub_infos/bert_words.json'
    if os.path.exists(bert_words_path):
        vocab = load_file(bert_words_path)
    else:
        from transformers import BertTokenizer
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        vocab = list(tokenizer.get_vocab().keys())
        vocab = [v for v in vocab if v[0] != '#' and 'unused' not in v]
        random.shuffle(vocab)
        save_file(vocab, bert_words_path)

    random.shuffle(vocab)
    return vocab
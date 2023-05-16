
import googletrans

def translate_to_korean(word):
    translator = googletrans.Translator()
    again_flag = True
    while again_flag:
        try:
            new_word = translator.translate(word, dest='ko').text
            again_flag = False
        except:
            again_flag = True
    return new_word
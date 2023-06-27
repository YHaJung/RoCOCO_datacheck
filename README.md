# Data Check for RoCOCO

- This is a python program which help DATA review
- It is made for a RoCOCO

## Setting

```
pip install -r requirements.txt
```

- you can change where do you call new words
  - you can change `call_words_by_category` in `data_check/main.py` with one of these
  ```python
  call_words_by_category(diff_word, category_type = 'same') # call same category words
  call_words_by_category(diff_word, category_type = 'diff') # call different category words
  call_word_by_bart() # call bert words
  ```

## Start

```
python datacheck/main.py
```

## Caution
- Periodically enter `q` and save results. If not, you can lose all works.
- If you want to go back to previous captions, set `data_check/start_idx.txt`
- If some input does not work and show you the same question, this means your input is not in the right key list. Check what can be input or not again.



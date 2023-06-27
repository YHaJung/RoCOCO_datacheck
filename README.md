# Data Check for RoCOCO

- This is a python program which help DATA review
- It is made for a RoCOCO

## Setting
- data
  - put val2014 dataset in `data_check/val2014`
  - put analysis txt files in `data_check/sub_infos/analysis`
  
- install requirements
  ```shell
  pip install -r requirements.txt
  ```

- you can change where do you call new words
  - change `call_words_by_category` in `data_check/main.py` with one of these if you want
    
    ```python
    call_words_by_category(diff_word, category_type = 'same') # call same category words
    call_words_by_category(diff_word, category_type = 'diff') # call different category words
    call_word_by_bart() # call bert words
    ```

- you can change which type of words will you pass
  - change `pass_pairs_path` in `data_check/main.py` according to which pair do you want to pass
    
    ```python
    pass_pairs_path = 'data_check/different_pairs.json'
    ```

## Start

```
python datacheck/main.py
```

## Caution
- Periodically enter `q` and save results. If not, you can lose all works.
- If you want to go back to previous captions, set `data_check/start_idx.txt`
- If some input does not work and show you the same question, this means your input is not in the right key list. Check what can be input or not again.



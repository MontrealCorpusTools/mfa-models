import os
import hangul_jamo

from montreal_forced_aligner.command_line.model import inspect_model

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dictionary_dir = os.path.join(root_dir, 'dictionary')
skip_words_dir = os.path.join(dictionary_dir, 'filter_lists')
staging_dir = os.path.join(dictionary_dir, 'training')

for fn in os.listdir(staging_dir):
    if not fn.endswith('.dict'):
        continue
    if fn.endswith("_cv.dict"):
        continue
    if fn.endswith("prosodylab.dict"):
        continue
    language = fn.split('_')[0]
    skip_words_path = os.path.join(skip_words_dir, language+'.txt')
    skip_word_set = set()
    if os.path.exists(skip_words_path):
        with open(skip_words_path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if language == 'korean' and 'jamo' in fn:
                    line = hangul_jamo.compose(line)
                skip_word_set.add(line.lower())
    print(skip_word_set)
    dict_path = os.path.join(staging_dir, fn)
    inspect_model(dict_path)
    line_set = set()
    line_counter = 0
    with open(dict_path, 'r', encoding='utf8') as f:
        for line in f:
            line_counter +=1
            line = line.strip()
            if not line:
                continue
            word = line.split('\t')[0].lower()
            if word in skip_word_set:
                continue
            line_set.add(line)
    if line_counter == len(line_set):
        continue
    with open(dict_path, 'w', encoding='utf8') as f:
        for line in sorted(line_set):
            f.write(line + '\n')
    print(f"Reduced {fn} from {line_counter} to {len(line_set)}")

import os
import hangul_jamo

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dictionary_dir = os.path.join(root_dir, 'dictionary')
staging_dir = os.path.join(dictionary_dir, 'training')

jamo_dict = os.path.join(staging_dir, 'korean_jamo_mfa.dict')
hangul_dict= os.path.join(staging_dir, 'korean_mfa.dict')

phone_set = set()
with open(jamo_dict, 'r', encoding='utf8') as jamo_f, \
    open(hangul_dict, 'w', encoding='utf8') as hangul_f:
    for line in jamo_f:
        line = line.strip()
        line = line.split()
        word = line.pop(0)
        pronunciation = ' '.join(line)
        phone_set.update(line)
        hangul_word = hangul_jamo.compose(word)
        hangul_f.write(f'{hangul_word}\t{pronunciation}\n')

print(sorted(phone_set))

import os.path
import re

from montreal_forced_aligner.command_line.train_g2p import run_train_g2p

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dictionary_dir = os.path.join(root_dir, 'dictionary', 'training')
output_dir = os.path.join(root_dir, 'g2p', 'staging')
temp_dir = os.path.join(root_dir, 'scripts', 'temp')
os.makedirs(output_dir, exist_ok=True)

class DefaultArgs:
    def __init__(self, dictionary_path, output_model_path, temporary_directory):
        self.dictionary_path = dictionary_path
        self.output_model_path = output_model_path
        self.temporary_directory = temporary_directory
        self.config_path = None
        self.evaluation_mode = True
        self.num_jobs = 10
        self.debug = True
        self.clean = True


lang_codes = ['czech', 'russian',
              'french', 'german',
              'portuguese_brazil', 'portuguese_portugal',
              'spanish_spain', 'spanish_latin_america',
              'swedish',
              #'tamil',
              'thai',
              'turkish',
              'english_us','english_us_arpa','english_uk','english_nigeria',
              'korean_jamo', 'korean',
              #'mandarin_hani'
              'hausa', 'swahili',
              'vietnamese_hanoi', 'vietnamese_hue', 'vietnamese_ho_chi_minh_city',
               'ukrainian', 'polish', 'croatian', 'bulgarian',
              #'japanese',
              ]


def get_error_rates(lang):
    train_temp_dir = os.path.join(temp_dir, f'{lang}_mfa_pynini_train_g2p')
    log_file = os.path.join(train_temp_dir, 'pynini_train_g2p.log')
    if not os.path.exists(log_file):
        return 1, 1
    wer_pattern = re.compile(r'WER:\s+([\d.]+)')
    ler_pattern = re.compile(r'LER:\s+([\d.]+)')
    wer, ler = None, None
    with open(log_file, 'r', encoding='utf8') as f:
        for line in f:
            m = wer_pattern.search(line)
            if m:
                wer = m.groups()[0]
            m = ler_pattern.search(line)
            if m:
                ler = m.groups()[0]
    return wer, ler

error_metrics = {}

for lang in lang_codes:
    print(lang)
    if lang.endswith('arpa'):
        dict_path = os.path.join(dictionary_dir, lang + '.dict')
        model_path = os.path.join(output_dir, lang + '.zip')
    else:
        dict_path = os.path.join(dictionary_dir, lang + '_mfa.dict')
        model_path = os.path.join(output_dir, lang + '_mfa.zip')
    args = DefaultArgs(dict_path, model_path, temp_dir)
    if os.path.exists(args.output_model_path):
        error_metrics[lang] = get_error_rates(lang)
        continue
    if lang == 'mandarin':
        args.evaluate = False
    elif lang == 'japanese':
        import pykakasi
        kks = pykakasi.kakasi()
        os.makedirs(temp_dir, exist_ok=True)
        new_path = os.path.join(temp_dir, 'converted_japanese.dict')
        with open(dict_path, 'r', encoding='utf8') as inf, open(new_path, 'w', encoding='utf8') as outf:
            for line in inf:
                line = line.strip()
                if not line:
                    continue
                try:
                    word, rest = line.split(maxsplit=1)
                except ValueError:
                    print(line)
                    raise
                kana_word = ''.join(x['kana'] for x in kks.convert(word))
                new_word = ''.join(x['hira'] for x in kks.convert(word))
                if not new_word:
                    continue
                if kana_word != word and new_word != word:
                    continue
                outf.write(f'{word}\t{rest}\n')
        args.dictionary_path = new_path
    unknown= []
    if not os.path.exists(args.dictionary_path):
        continue
    run_train_g2p(args, unknown)
    if lang == 'mandarin_hani':
        continue

    error_metrics[lang] = get_error_rates(lang)

for k, v in error_metrics.items():
    print(f"{k}: {v[0]}% WER, {v[1]}% LER")

import os.path
import re

from montreal_forced_aligner.command_line.train_g2p import run_train_g2p

cleaned_dir = r'/mnt/c/Users/michael/Documents/Dev/mfa-models/dictionary'
output_dir = r'/mnt/c/Users/michael/Documents/Dev/mfa-models/g2p/staging'
temp_dir = r'/mnt/d/temp/g2p_mfa_models_temp'
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


lang_codes = [
              'french', 'german',
              'portuguese_brazil', 'portuguese_portugal',
              'spanish_castilian', 'spanish_latin_america',
              'swedish',
              'tamil', 'thai',
              'turkish',
              'english_us','english_uk',
              'korean_jamo', 'korean',
              #'mandarin_hani'
              'hausa', 'swahili',
              'japanese',
              'vietnamese_hanoi', 'vietnamese_hue', 'vietnamese_hochiminhcity',
              'russian', 'ukrainian', 'polish', 'croatian', 'czech', 'bulgarian',
              ]
#lang_codes = ['japanese']

def get_error_rates(lang):
    train_temp_dir = os.path.join(temp_dir, f'{lang}_ipa_pynini_train_g2p')
    log_file = os.path.join(train_temp_dir, 'pynini_train_g2p.log')
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
    args = DefaultArgs(os.path.join(cleaned_dir, lang + '_ipa.dict'), os.path.join(output_dir, lang + '_ipa.zip'), temp_dir)
    if os.path.exists(args.output_model_path):
        error_metrics[lang] = get_error_rates(lang)
        continue
    if lang == 'mandarin_hani':
        args.evaluate = False
    unknown= []
    if lang == 'japanese':
        unknown.extend(['--num_pronunciations', '1'])
    run_train_g2p(args, unknown)
    if lang == 'mandarin_hani':
        continue

    error_metrics[lang] = get_error_rates(lang)

for k, v in error_metrics.items():
    print(f"{k}: {v[0]}% WER, {v[1]}% LER")

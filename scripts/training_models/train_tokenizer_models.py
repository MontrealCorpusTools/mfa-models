import os.path
import re
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli


if sys.platform == 'win32':
    training_root = 'D:/Data/speech/model_training_corpora'
    dictionary_dir = 'C:/Users/michael/Documents/Dev/mfa-models/dictionary/training'
    groups_dir = 'C:/Users/michael/Documents/Dev/mfa-models/config/acoustic/phone_groups'
    rules_dir = 'C:/Users/michael/Documents/Dev/mfa-models/config/acoustic/rules'
    config_dir = 'C:/Users/michael/Documents/Dev/mfa-models/config/acoustic'
    model_output_directory = 'D:/Data/models/final_training'
    temp_dir = r'D:/temp/model_training_temp2/'
else:
    training_root = '/mnt/d/Data/speech/model_training_corpora'
    dictionary_dir = '/mnt/c/Users/michael/Documents/Dev/mfa-models/dictionary/training'
    groups_dir = '/mnt/c/Users/michael/Documents/Dev/mfa-models/config/acoustic/phone_groups'
    rules_dir = '/mnt/c/Users/michael/Documents/Dev/mfa-models/config/acoustic/rules'
    config_dir = '/mnt/c/Users/michael/Documents/Dev/mfa-models/config/acoustic'
    model_output_directory = '/mnt/d/Data/models/final_training'
    temp_dir = r'/mnt/d/temp/model_training_temp2/'

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_dir = os.path.join(root_dir, 'tokenizer', 'staging')
os.makedirs(output_dir, exist_ok=True)




lang_codes = [
              'japanese',
              #'thai',
                #'mandarin_china', 'mandarin_erhua', 'mandarin_taiwan'
              ]


def get_error_rates(lang):
    train_temp_dir = os.path.join(temp_dir, f'{lang}_mfa')
    log_file = os.path.join(train_temp_dir, f'{lang}_mfa.log')
    print("Parsing:", log_file)
    if not os.path.exists(log_file):
        return 1, 1
    wer_pattern = re.compile(r'WER:\s+([\d.]+)$')
    ler_pattern = re.compile(r'LER:\s+([\d.]+)$')
    wer, ler = None, None
    with open(log_file, 'r', encoding='utf8') as f:
        for line in f:
            m = wer_pattern.search(line)
            if m:
                wer = m.group(0)
            m = ler_pattern.search(line)
            if m:
                ler = m.group(0)
    return wer, ler

error_metrics = {}

if __name__ == '__main__':

    for lang in lang_codes:
        print(lang)
        model_path = os.path.join(output_dir, lang + '_mfa.zip')
        print(model_path)
        if os.path.exists(model_path):
            error_metrics[lang] = get_error_rates(lang)
            continue
        unknown= []
        corpus_path = os.path.join(training_root, lang)
        command = ['train_tokenizer',
                   corpus_path,
                   model_path,
                   '-t', temp_dir,
                   '-j', '10',
                   '--use_mp',
                   '--debug',
                   '--phonetisaurus',
                   '--no_clean',
                   '--evaluate',
                   ]
        mfa_cli(command, standalone_mode=False)

        error_metrics[lang] = get_error_rates(lang)

    for k, v in error_metrics.items():
        print(f"{k}: {v[0]}% WER, {v[1]}% LER")

import os.path
import re
import sys
from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dictionary_dir = os.path.join(root_dir, 'dictionary', 'training')
output_dir = os.path.join(root_dir, 'acoustic', 'staging')
temp_dir = r'D:\temp\MFA'
config_dir = os.path.join(root_dir, 'config', 'acoustic')
groups_dir = os.path.join(config_dir, 'phone_groups')
rules_dir = os.path.join(config_dir, 'rules')

if sys.platform == 'win32':
    training_root = 'D:/Data/speech/model_training_corpora'
else:
    training_root = '/mnt/d/Data/speech/model_training_corpora'

languages = [

    'english',
    'korean',
    'bulgarian',
    'vietnamese',
             'croatian',
    'hausa',
    'ukrainian',
'thai',
'swahili',
     'turkish',
    'spanish',
             'swedish',
             'portuguese', 'polish',
             'french',
             'czech', #'japanese',
             'russian',
    'german',
     'mandarin', #'tamil',
             ]
languages = [
    'english'
#'japanese', #'hausa', 'bulgarian'
             ]


if __name__ == '__main__':
    for lang in languages:
        print(lang)
        model_path = os.path.join(output_dir, f'{lang}_mfa.zip')
        if os.path.exists(model_path):
            continue
        lang_corpus_dir = os.path.join(training_root, lang)
        dictionary_path = os.path.join(lang_corpus_dir, lang+'_speaker_dictionaries.yaml')
        command = ['train', lang_corpus_dir.format(lang), dictionary_path,
                         model_path, '-t', os.path.join(temp_dir, lang), '-j',
                   '10', '--oov_count_threshold', "1",
                   '--use_cutoff_model',
                   '--clean', '--no_debug'
                   ]
        groups_path = os.path.join(groups_dir, f'{lang}_mfa.yaml')
        if os.path.exists(groups_path):
            command += ['--groups_path', groups_path]

        rules_path = os.path.join(rules_dir, f'{lang}_mfa.yaml')
        if os.path.exists(rules_path):
            command += ['--rules_path', rules_path]
        config_path = os.path.join(config_dir, lang +".yaml")
        if os.path.exists(config_path):
            command += ['--config_path', config_path]
        print(command)
        mfa_cli(command, standalone_mode=False)

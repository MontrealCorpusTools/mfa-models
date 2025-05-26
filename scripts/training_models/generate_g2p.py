import os.path
import re
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli
from montreal_forced_aligner.config import TEMPORARY_DIRECTORY

MODEL_VERSION = "3.0.0"

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dictionary_dir = os.path.join(root_dir, "dictionary", "training")
g2p_dir = os.path.join(root_dir, "g2p", "staging")
output_dir = os.path.join(root_dir, "dictionary", "training", "g2pped")
config_dir = os.path.join(root_dir, "config", "acoustic")
temp_dir = TEMPORARY_DIRECTORY
os.makedirs(output_dir, exist_ok=True)

if sys.platform == "win32":
    training_root = "D:/Data/speech/model_training_corpora"
else:
    training_root = "/mnt/d/Data/speech/model_training_corpora"


lang_codes = [
    "czech",
    "russian",
    "french",
    "german",
    "portuguese_brazil",
    "portuguese_portugal",
    "spanish_spain",
    "spanish_latin_america",
    "swedish",
    "thai",
    "turkish",
    "english_us",
    "english_us_arpa",
    "english_uk",
    "english_nigeria",
    "korean_jamo",
    "korean",
    "hausa",
    "swahili",
    "vietnamese_hanoi",
    "vietnamese_hue",
    "vietnamese_ho_chi_minh_city",
    "ukrainian",
    "polish",
    "croatian",
    "bulgarian",
    "japanese",
    "japanese_katakana",
    #'mandarin_china', 'mandarin_erhua', 'mandarin_taiwan'
    "tamil",
    "hindi",
    "urdu",
]

lang_codes = [
    "hindi-urdu",
    #'vietnamese_hanoi', 'vietnamese_hue', 'vietnamese_ho_chi_minh_city',
]

corpus_variety_mapping = {
    "hindi-urdu": {
        "shrutilipi_hindi": "hindi",
        "common_voice_hindi": "hindi",
        "musc2021_cs_hindi": "hindi",
        "musc2021_hindi": "hindi",
        "common_voice_urdu": "urdu",
        "shrutilipi_urdu": "urdu",
    }
}

if __name__ == "__main__":
    for lang in lang_codes:
        print(lang)
        lang_corpus_dir = os.path.join(training_root, lang)
        config_path = os.path.join(config_dir, lang + ".yaml")
        if lang in corpus_variety_mapping:
            for subcorpus, dialect in corpus_variety_mapping[lang].items():
                print(subcorpus, dialect)
                dictionary_path = os.path.join(dictionary_dir, f"{dialect}_mfa.dict")
                model_path = os.path.join(g2p_dir, f"{dialect}_mfa.zip")
                if not os.path.exists(model_path):
                    continue
                output_file = os.path.join(output_dir, f"{dialect}_{subcorpus}_mfa.dict")
                command = [
                    "g2p",
                    lang_corpus_dir,
                    model_path,
                    output_file,
                    "--clean",
                    "-j",
                    "10",
                    "--dictionary_path",
                    dictionary_path,
                    "--oov_count_threshold",
                    "3",
                    "--use_mp",
                    "--no_use_postgres",
                    "--num_pronunciations",
                    "1",
                ]
                if os.path.exists(config_path):
                    command += ["--config_path", config_path]
                mfa_cli(command, standalone_mode=False)
                error
        else:
            dictionary_path = os.path.join(dictionary_dir, f"{lang}_mfa.dict")
            model_path = os.path.join(g2p_dir, f"{lang}_mfa.zip")
            if not os.path.exists(model_path):
                continue
            output_file = os.path.join(output_dir, f"{lang}_mfa.dict")
            command = [
                "g2p",
                lang_corpus_dir,
                model_path,
                output_file,
                "--clean",
                "-j",
                "10",
                "--dictionary_path",
                dictionary_path,
                "--use_mp",
                "--evaluate",
                "--num_pronunciations",
                "1",
            ]
            config_path = os.path.join(config_dir, lang + ".yaml")
            if os.path.exists(config_path):
                command += ["--config_path", config_path]
            mfa_cli(command, standalone_mode=False)

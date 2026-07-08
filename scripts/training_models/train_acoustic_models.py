import os.path
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli

MODEL_VERSION = "3.3.0"

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dictionary_dir = os.path.join(root_dir, "dictionary", "training")
g2p_staging_dir = os.path.join(root_dir, "g2p", "staging")
output_dir = os.path.join(root_dir, "staging")
temp_dir = r"D:\temp\MFA"
config_dir = os.path.join(root_dir, "config", "acoustic")
metadata_dir = os.path.join(root_dir, "config", "metadata")
groups_dir = os.path.join(config_dir, "phone_groups")
rules_dir = os.path.join(config_dir, "rules")
topology_dir = os.path.join(config_dir, "topologies")

if sys.platform == "win32":
    training_root = r"C:\Users\micha\Documents\Data\model_training_corpora"
else:
    training_root = "/mnt/d/Data/speech/model_training_corpora"

languages = [
    "english",
    "korean",
    "bulgarian",
    "vietnamese",
    "croatian",
    "hausa",
    "ukrainian",
    "thai",
    "swahili",
    "turkish",
    "spanish",
    "swedish",
    "portuguese",
    "polish",
    "french",
    "czech",  #'japanese',
    "russian",
    "german",
    "mandarin",  #'tamil',
]
languages = [
    # "english",
    # "english_us_arpa",
    "portuguese",
    #'swahili',
    "serbocroatian",
    "czech",
    "russian",
    "japanese",
    "spanish",
    #'hindi',
    #'urdu',
    "korean",
    "bulgarian",
    "hausa",
    "polish",
    "thai",
    "turkish",
    "ukrainian",
    "swahili",
    "swedish",
    "german",
    "french",
    "mandarin",
    "vietnamese",
]

extra_arguments = {
    "japanese": [
        "--language",
        "japanese",
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "japanese_katakana_mfa.zip"),
    ],
    "korean": [
        "--language",
        "korean",
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "korean_mfa.zip"),
    ],
    "mandarin": [
        "--language",
        "chinese",
        "--g2p_model_path",
        os.path.join(training_root, "mandarin", "mandarin_g2p_models.yaml"),
    ],
    "spanish": [
        "--g2p_model_path",
        os.path.join(training_root, "spanish", "spanish_g2p_models.yaml"),
    ],
    "thai": [
        "--language",
        "thai",
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "thai_mfa.zip"),
    ],
    "turkish": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "turkish_mfa.zip"),
    ],
    "russian": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "russian_mfa.zip"),
    ],
    "polish": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "polish_mfa.zip"),
    ],
    "bulgarian": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "bulgarian_mfa.zip"),
    ],
    "german": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "german_mfa.zip"),
    ],
    "swedish": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "swedish_mfa.zip"),
    ],
    "swahili": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "swahili_mfa.zip"),
    ],
    "ukrainian": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "ukrainian_mfa.zip"),
    ],
}

if __name__ == "__main__":
    for lang in languages:
        print(lang)
        model_path = os.path.join(output_dir, lang)
        is_arpa = "arpa" in lang
        if "arpa" not in lang:
            model_path += "_mfa"
        lang = lang.replace("_us_arpa", "")
        if os.path.exists(model_path):
            continue
        if lang in {"hindi", "urdu"}:
            lang_corpus_dir = os.path.join(training_root, "hindi-urdu", lang)
        elif is_arpa:
            lang_corpus_dir = os.path.join(training_root, lang, "librispeech_english")
        else:
            lang_corpus_dir = os.path.join(training_root, lang)
        dictionary_path = os.path.join(lang_corpus_dir, lang + "_speaker_dictionaries.yaml")
        if not os.path.exists(dictionary_path):
            dictionary_path = os.path.join(dictionary_dir, f"{lang}_mfa.dict")
        if is_arpa:
            dictionary_path = os.path.join(dictionary_dir, f"{lang}_us_arpa.dict")
        oov_count_threshold = "1"
        if lang in {"serbocroatian", "spanish", "russian", "portuguese"}:
            oov_count_threshold = "0"
        command = [
            "train",
            lang_corpus_dir.format(lang),
            dictionary_path,
            model_path,
            "-t",
            temp_dir,
            "-j",
            "10",
            "--oov_count_threshold",
            oov_count_threshold,
            "--model_version",
            MODEL_VERSION,
            "--use_cutoff_model",
            "--clean",
            "--no_debug",
            "--no_verbose",
            "--use_mp",
            "--no_use_threading",
            "--use_postgres",
            "--subset_word_count",
            "6",
            "--final_clean",
        ]
        if lang in {"hindi", "urdu"}:
            lang = "hindi-urdu"
        groups_path = os.path.join(groups_dir, f"{lang}_mfa.yaml")
        rules_path = os.path.join(rules_dir, f"{lang}_mfa.yaml")
        topology_path = os.path.join(topology_dir, f"{lang}_mfa.yaml")
        config_path = os.path.join(config_dir, lang + ".yaml")
        metadata_path = os.path.join(metadata_dir, lang + ".json")
        if is_arpa:
            groups_path = os.path.join(groups_dir, f"{lang}_arpa.yaml")
            rules_path = os.path.join(rules_dir, f"{lang}_arpa.yaml")
            topology_path = os.path.join(topology_dir, f"{lang}_arpa.yaml")
            metadata_path = os.path.join(metadata_dir, lang + "_arpa.json")
            config_path = os.path.join(config_dir, lang + "_arpa.yaml")
        if os.path.exists(groups_path):
            command += ["--phone_groups_path", groups_path]
        if os.path.exists(rules_path):
            command += ["--rules_path", rules_path]
        if os.path.exists(topology_path):
            command += ["--topology_path", topology_path]
        if os.path.exists(config_path):
            command += ["--config_path", config_path]
        if os.path.exists(metadata_path):
            command += ["--metadata_path", metadata_path]
        command += extra_arguments.get(lang, [])
        print(command)
        mfa_cli(command, standalone_mode=False)

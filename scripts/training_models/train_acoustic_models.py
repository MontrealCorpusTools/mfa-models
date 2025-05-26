import os.path
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli

MODEL_VERSION = "3.3.0"

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dictionary_dir = os.path.join(root_dir, "dictionary", "training")
g2p_staging_dir = os.path.join(root_dir, "g2p", "staging")
output_dir = os.path.join(root_dir, "acoustic", "staging")
temp_dir = r"D:\temp\MFA"
config_dir = os.path.join(root_dir, "config", "acoustic")
groups_dir = os.path.join(config_dir, "phone_groups")
rules_dir = os.path.join(config_dir, "rules")
topology_dir = os.path.join(config_dir, "topologies")

if sys.platform == "win32":
    training_root = "D:/Data/speech/model_training_corpora"
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
    "spanish",
    #'swahili',
    #'serbo-croatian',
    #'czech',
    #'hindi',
    #'urdu',
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
        os.path.join(g2p_staging_dir, "korean_jamo_mfa.zip"),
    ],
    "mandarin": [
        "--language",
        "chinese",
        "--g2p_model_path",
        os.path.join(training_root, "mandarin", "mandarin_g2p_models.yaml"),
    ],
    #'spanish': [
    #    '--g2p_model_path', os.path.join(training_root, "spanish", "spanish_g2p_models.yaml"),
    # ],
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
    "ukrainian": [
        "--g2p_model_path",
        os.path.join(g2p_staging_dir, "ukrainian_mfa.zip"),
    ],
}

if __name__ == "__main__":
    for lang in languages:
        print(lang)
        model_path = os.path.join(output_dir, f"{lang}_mfa.zip")
        if os.path.exists(model_path):
            continue
        if lang in {"hindi", "urdu"}:
            lang_corpus_dir = os.path.join(training_root, "hindi-urdu", lang)
        else:
            lang_corpus_dir = os.path.join(training_root, lang)
        dictionary_path = os.path.join(lang_corpus_dir, lang + "_speaker_dictionaries.yaml")
        if not os.path.exists(dictionary_path):
            dictionary_path = os.path.join(dictionary_dir, f"{lang}_mfa.dict")
        oov_count_threshold = "1"
        if lang in {"serbo-croatian"}:
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
        ]
        if lang in {"hindi", "urdu"}:
            lang = "hindi-urdu"
        groups_path = os.path.join(groups_dir, f"{lang}_mfa.yaml")
        if os.path.exists(groups_path):
            command += ["--phone_groups_path", groups_path]

        rules_path = os.path.join(rules_dir, f"{lang}_mfa.yaml")
        if os.path.exists(rules_path):
            command += ["--rules_path", rules_path]

        topology_path = os.path.join(topology_dir, f"{lang}_mfa.yaml")
        if os.path.exists(topology_path):
            command += ["--topology_path", topology_path]
        config_path = os.path.join(config_dir, lang + ".yaml")
        if os.path.exists(config_path):
            command += ["--config_path", config_path]
        command += extra_arguments.get(lang, [])
        print(command)
        mfa_cli(command, standalone_mode=False)

import os.path

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
staging_dir = os.path.join(root_dir, "staging")

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
    "english_us_arpa",
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
    "czech",
    "japanese",
    "russian",
    "german",
    "mandarin",  #'tamil',
    #'hindi',
    #'urdu',
]

if __name__ == "__main__":
    for lang in languages:
        if not lang.endswith("_arpa"):
            lang = f"{lang}_mfa"
        print(lang)
        model_path = os.path.join(staging_dir, lang)
        if not os.path.exists(model_path):
            print(f"skipping {lang}!")
            continue
        command = [
            "model",
            "upload",
            str(model_path),
            f"MontrealCorpusTools/{lang}",
            "--version",
            "v3.3.0",
        ]
        print(command)
        mfa_cli(command, standalone_mode=False)

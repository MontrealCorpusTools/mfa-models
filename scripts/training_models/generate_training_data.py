import json
import os.path
import sys
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape
from montreal_forced_aligner.helper import mfa_open
from montreal_forced_aligner.models.hf_functions import LICENSES

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
    "english",
    # "english_us_arpa",
    "portuguese",
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
    "vietnamese",
    "mandarin",
]

if __name__ == "__main__":
    for lang in languages:
        print(lang)
        is_arpa = "arpa" in lang
        lang = lang.replace("_us_arpa", "")
        if lang in {"hindi", "urdu"}:
            training_root_directory = os.path.join(training_root, "hindi-urdu", lang)
        elif is_arpa:
            training_root_directory = os.path.join(training_root, lang, "librispeech_english")
        else:
            training_root_directory = os.path.join(training_root, lang)

        env = Environment(
            loader=PackageLoader("montreal_forced_aligner.models"), autoescape=select_autoescape()
        )
        corpus_template = env.get_template("corpus_template.md")
        corpus_data = {}
        for corpus_directory in Path(training_root_directory).iterdir():
            if not corpus_directory.is_dir():
                continue
            corpus_name = corpus_directory.name

            corpus_data_path = corpus_directory / "corpus_data.json"
            if corpus_data_path.exists():
                with mfa_open(corpus_data_path, "r") as f:
                    data = json.load(f)
            else:
                data = {
                    "name": corpus_name,
                    "link": "",
                    "dialects": [],
                    "license": "",
                    "citation": "",
                    "version": "",
                }
            with mfa_open(corpus_data_path, "w") as f:
                json.dump(data, f)
            if data["license"] in LICENSES:
                data["license"] = f"[{data['license']}]({LICENSES[data['license']]})"
            corpus_data[corpus_name] = data
        training_details = []
        for d in corpus_data.values():
            print(d["name"])
            training_details.append(corpus_template.render(**d))
        with mfa_open(os.path.join(training_root_directory, "training_data.md"), "w") as f:
            f.write("\n\n".join(training_details))

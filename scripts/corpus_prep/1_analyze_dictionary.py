import collections
import os
import unicodedata
from pathlib import Path

import yaml

languages = [
    "english",
    "korean",
    "bulgarian",
    "vietnamese",
    "serbocroatian",
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
    "mandarin",
    "tamil",
    "hindi-urdu",
    "italian",
]

languages = [
    "italian",
]
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMP_DIR = ROOT_DIR.joinpath("scripts", "corpus_prep", "temp")
TRAINING_DIR = ROOT_DIR.joinpath("dictionary", "training")
ACOUSTIC_CONFIG_DIR = ROOT_DIR.joinpath("config", "acoustic")


def read_source(lang):
    graphemes = set()
    phones = set()
    dictionary = []
    path = os.path.join(TRAINING_DIR, f"{lang}_mfa.dict")
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = line.split()
            word = unicodedata.normalize("NFKC", line[0])
            pronunciation = line[1:]
            graphemes.update(word)
            phones.update(pronunciation)
            dictionary.append((word, pronunciation))
    return dictionary, graphemes, phones


def process_language(lang):
    print("Processing", lang)
    dictionary, input_graphemes, input_phones = read_source(lang)

    print("Graphemes", sorted(input_graphemes))
    save_dictionary(dictionary, lang)


def create_phone_group_file(lang, phones):
    phones_path = ACOUSTIC_CONFIG_DIR.joinpath("phone_groups", f"{lang}_mfa.yaml")
    if not phones_path.exists():
        phone_groups = {}
        for p in phones:
            base_phone = p.replace("ː", "")
            if base_phone not in phone_groups:
                phone_groups[base_phone] = []
            phone_groups[base_phone].append(p)
        print(phone_groups)
        with open(phones_path, "w", encoding="utf8") as f:
            yaml.safe_dump(list(phone_groups.values()), f, allow_unicode=True)


def save_dictionary(dictionary, lang):
    deduplication = set()
    final_phones = collections.Counter()
    path = os.path.join(TEMP_DIR, f"{lang}_mfa.dict")
    with open(path, "w", encoding="utf8") as f:
        for w, p in sorted(dictionary):
            final_phones.update(p)
            p = " ".join(p)
            if (w, p) in deduplication:
                continue
            f.write("{}\t{}\n".format(w, p))
            deduplication.add((w, p))
    print("Final phones:", sorted(final_phones))
    print("Final phone counts:", sorted(final_phones.items(), key=lambda x: -x[1]))
    create_phone_group_file(lang, sorted(final_phones))


if __name__ == "__main__":
    for lang in languages:
        process_language(lang)

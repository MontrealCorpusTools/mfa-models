import collections
import pathlib

import yaml

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
DICTIONARY_DIR = ROOT_DIR.joinpath("dictionary", "training", "cleaned")
OUTPUT_DIR = ROOT_DIR.joinpath("config", "acoustic", "phone_groups")

language = "portuguese"


def create_phone_groups():
    found_phones = set()
    counts = collections.Counter()
    output_path = OUTPUT_DIR.joinpath(f"{language}_mfa.yaml")
    for dictionary_path in DICTIONARY_DIR.iterdir():
        if not dictionary_path.name.startswith(language):
            continue
        with open(dictionary_path, "r", encoding="utf8") as f:
            for line in f:
                _, phones = line.split(maxsplit=1)
                found_phones.update(phones.split())
                counts.update(phones.split())
    print(language)
    print(sorted(counts.items(), key=lambda x: -x[-1]))
    if output_path.exists():
        return
    with open(output_path, "w", encoding="utf8") as f:
        yaml.dump(sorted(found_phones), f, Dumper=yaml.SafeDumper, allow_unicode=True)


if __name__ == "__main__":
    create_phone_groups()

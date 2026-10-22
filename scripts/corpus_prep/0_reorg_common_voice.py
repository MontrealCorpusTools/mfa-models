import csv
import os
import shutil
from collections import Counter

import tqdm

try:
    import hanziconv
except ImportError:
    pass
ignore = []


def nonzero(a):
    return [i for i, e in enumerate(a) if e != 0]


def split(s, indices):
    return [s[i:j] for i, j in zip(indices, indices[1:] + [None])]


languages = [
    "bulgarian",
    "german",
    "french",
    "portuguese",
    "serbian",
    "swedish",
    "tamil",
    "turkish",
    "ukrainian",
    "vietnamese",
    "swahili",
    "spanish",
    "polish",
    "czech",
    "english",
    "russian",
    "hausa",
    "arabic",
    "korean",
    "hindi",
    "urdu",
    "japanese",
    "thai",
    "mandarin_china",
    "mandarin_taiwan",
]
languages = [
    "italian",
]

root_directory = r"C:\Users\micha\Documents\Data\model_training_corpora"


language_partitions = [
    "validated",
    "other",
    "invalidated"
    #'dev', 'test', 'train'
]

bad_chars = {
    "，",
    "。",
    "、",
    "「",
    "」",
    "・・・",
    "。",
    "：",
    " ",
    "-",
    "--",
    "──",
    "─",
    "）",
    "（",
    "――",
    "───",
    "……",
    "_",
    "－",
    "＆",
    "・",
    "＋",
    ";",
    "<",
    "〈",
    "〉",
    "-",
    ">",
    "“",
    "”",
    "―",
    "／",
    "─",
    "…",
    "！",
    "　",
    "『",
    "』",
    "；",
    "’",
    "‘",
    "（",
    "）",
    "《",
    "》",
    "？",
    "(",
    ")",
}

for lang in languages:
    if lang in ignore:
        print("IGNORING", lang)
        continue
    root_lang = lang
    if lang in ["mandarin_china", "mandarin_taiwan"]:
        root_lang = "mandarin"
    if lang in ["serbian"]:
        root_lang = "serbo-croatian"
    lang_dir = os.path.join(root_directory, root_lang, "common_voice_{}".format(lang))
    if not os.path.exists(lang_dir):
        print("IGNORING", lang)
        continue
    print(lang)
    clip_dir = os.path.join(lang_dir, "clips")
    clip_info = {}
    speaker_counts = Counter()
    count = 0
    speaker_information = {}
    bad_files = set()
    bad_sentences = set()
    with open(os.path.join(lang_dir, "invalidated.tsv"), "r", encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar="|")
        for line in reader:
            bad_files.add(line["path"])
    with open(os.path.join(lang_dir, "other.tsv"), "r", encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar="|")
        for line in reader:
            bad_files.add(line["path"])
    with open(os.path.join(lang_dir, "reported.tsv"), "r", encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter="\t", quotechar="|")
        for line in reader:
            text = line["sentence"]
            if lang == "mandarin_china":
                text = hanziconv.HanziConv.toSimplified(text)
            elif lang == "mandarin_taiwan":
                text = hanziconv.HanziConv.toTraditional(text)
            bad_sentences.add(text)
    print(f"bad files: {len(bad_files)}")
    print(f"bad sentences: {len(bad_sentences)}")
    for p in language_partitions:
        print(f"Partition {p}")
        path = os.path.join(lang_dir, p + ".tsv")
        with open(path, "r", encoding="utf8") as f:
            line_count = sum(1 for line in f)
        with open(path, "r", encoding="utf8") as f:
            reader = csv.DictReader(f, delimiter="\t", quotechar="|")

            for line in tqdm.tqdm(reader, total=line_count):
                speaker = line["client_id"]
                path = line["path"]
                text = line["sentence"]
                if lang == "mandarin_china":
                    text = hanziconv.HanziConv.toSimplified(text)
                elif lang == "mandarin_taiwan":
                    text = hanziconv.HanziConv.toTraditional(text)
                if path in bad_files or text in bad_sentences:
                    speaker_dir = os.path.join(lang_dir, speaker)
                    mp3_path = os.path.join(speaker_dir, path)
                    if not os.path.exists(speaker_dir):
                        continue
                    if os.path.exists(mp3_path):
                        os.remove(mp3_path)
                    if os.path.exists(mp3_path.replace(".mp3", ".lab")):
                        os.remove(mp3_path.replace(".mp3", ".lab"))
                    if os.path.exists(mp3_path.replace(".mp3", ".TextGrid")):
                        os.remove(mp3_path.replace(".mp3", ".TextGrid"))
                    if not os.listdir(speaker_dir):
                        os.rmdir(speaker_dir)
                    continue
                if text in bad_sentences:
                    continue
                if speaker not in speaker_information:
                    speaker_information[speaker] = {
                        "age": line["age"],
                        "gender": line["gender"],
                        "accents": line["accents"],
                        "locale": line["locale"],
                    }
                if path not in clip_info and not os.path.exists(
                    os.path.join(lang_dir, speaker, path)
                ):
                    clip_info[line["path"]] = {"speaker": line["client_id"], "text": text}
                    speaker_counts[line["client_id"]] += 1
                    count += 1
                else:
                    continue
                    if (
                        clip_info[line["path"]]["speaker"] != line["client_id"]
                        or clip_info[line["path"]]["text"] != line["sentence"]
                    ):
                        print(clip_info[line["path"]])
                        print(line)
                        error

    print(len(speaker_counts))
    print(count)
    print(len(clip_info))

    with open(os.path.join(lang_dir, "speaker_info.tsv"), "w", encoding="utf8") as f:
        for speaker, info in speaker_information.items():
            f.write(
                f'{speaker}\t{info["age"]}\t{info["gender"]}\t{info["accents"]}\t{info["locale"]}\n'
            )

    for k, v in tqdm.tqdm(clip_info.items()):
        speaker = v["speaker"]
        out_dir = os.path.join(lang_dir, speaker)
        os.makedirs(out_dir, exist_ok=True)
        text = v["text"]
        mp3_path = k
        lab_path = k.replace(".mp3", ".lab")
        if False:
            if os.path.exists(os.path.join(out_dir, lab_path)):
                continue
            if os.path.exists(os.path.join(out_dir, k.replace(".mp3", ".TextGrid"))):
                continue
        if os.path.exists(clip_dir) and os.path.exists(os.path.join(clip_dir, mp3_path)):
            os.rename(os.path.join(clip_dir, mp3_path), os.path.join(out_dir, mp3_path))
        with open(os.path.join(out_dir, lab_path), "w", encoding="utf8") as f:
            f.write(text)

    shutil.rmtree(clip_dir, ignore_errors=True)

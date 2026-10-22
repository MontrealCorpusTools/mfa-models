import csv
import os

import soundfile as sf
from praatio import textgrid as tgio
from praatio.utilities.constants import Interval

corpus_root = r"C:\Users\micha\Documents\Data\model_training_corpora\italian\Italian_Conversational_Speech_Corpus"

audio_dir = os.path.join(corpus_root, "WAV")
text_dir = os.path.join(corpus_root, "TXT")

with open(os.path.join(corpus_root, "SPKINFO.txt"), "r", encoding="utf8") as f, open(
    os.path.join(corpus_root, "speaker_info.tsv"), "w", encoding="utf8"
) as outf:
    reader = csv.DictReader(f, delimiter="\t")
    writer = csv.DictWriter(
        outf, delimiter="\t", fieldnames=["SPEAKER_ID", "AGE", "GENDER", "REGION,CITY"]
    )
    for line in reader:
        print(line)
        line["GENDER"] = "female" if line["GENDER"] == "F" else "male"
        del line["CHANNEL"]
        del line["DEVICE"]
        writer.writerow(line)

for file_name in os.listdir(audio_dir):
    if not file_name.endswith(".wav"):
        continue
    text_path = os.path.join(text_dir, file_name.replace(".wav", ".txt"))
    output_path = os.path.join(audio_dir, file_name.replace(".wav", ".TextGrid"))
    utterances = []
    speaker = None
    info = sf.info(os.path.join(audio_dir, file_name))
    duration = info.duration
    with open(text_path, "r", encoding="utf8") as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            begin, end = [float(x) for x in line[0][1:-1].split(",")]
            speaker_id = line[1]
            text = line[-1]
            if speaker_id == "0":
                continue
            speaker = speaker_id
            print(line)
            print(begin, end, speaker_id, text)
            utterances.append(Interval(begin, end, text))
    tg = tgio.Textgrid(maxTimestamp=duration)
    tier = tgio.IntervalTier(speaker, utterances, minT=0, maxT=duration)
    tg.addTier(tier)
    tg.save(output_path, includeBlankSpaces=True, format="short_textgrid", reportingMode="error")

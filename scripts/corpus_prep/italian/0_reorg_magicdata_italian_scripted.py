import csv
import os
import shutil

root = (
    r"C:\Users\micha\Documents\Data\model_training_corpora\italian\Italian_Scripted_Speech_Corpus"
)

audio_dir = os.path.join(root, "WAV")

utt_file = os.path.join(root, "UTTRANSINFO.txt")

with open(utt_file, "r", encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for line in reader:
        print(line)
        file = line["UTTRANS_ID"]
        speaker = file.split("_", maxsplit=1)[0]
        transcript = line["SPEAKER_ID"]
        speaker_dir = os.path.join(root, speaker)
        os.makedirs(speaker_dir, exist_ok=True)
        with open(
            os.path.join(speaker_dir, file.replace(".wav", ".lab")), "w", encoding="utf8"
        ) as outf:
            outf.write(transcript)
        wavpath = os.path.join(audio_dir, speaker, file)
        if os.path.exists(wavpath):
            shutil.move(wavpath, os.path.join(speaker_dir, file))

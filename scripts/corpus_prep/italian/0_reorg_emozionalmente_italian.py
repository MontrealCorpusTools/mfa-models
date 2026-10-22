import csv
import os
import shutil

root_dir = r"C:\Users\micha\Documents\Data\model_training_corpora\italian\emozionalmente"

if __name__ == "__main__":
    wav_dir = os.path.join(root_dir, "audio")
    metadata_dir = os.path.join(root_dir, "metadata")
    with open(os.path.join(metadata_dir, "samples.csv"), "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            print(line)
            speaker = line["actor"]
            file_name = line["file_name"]
            text = line["sentence"]
            emotion = line["emotion_expressed"]
            speaker_directory = os.path.join(root_dir, speaker)
            os.makedirs(speaker_directory, exist_ok=True)
            out_file_path = os.path.join(
                speaker_directory, file_name.replace(".wav", f"_{emotion}.wav")
            )
            original_file_path = os.path.join(wav_dir, file_name)
            if os.path.exists(original_file_path):
                os.rename(original_file_path, out_file_path)
            with open(
                os.path.join(speaker_directory, file_name.replace(".wav", ".lab")),
                "w",
                encoding="utf8",
            ) as out_f:
                out_f.write(text)
    with (
        open(os.path.join(metadata_dir, "users.csv"), "r", encoding="utf8") as f,
        open(
            os.path.join(root_dir, "speaker_info.tsv"), "w", encoding="utf8", newline=""
        ) as out_f,
    ):
        reader = csv.DictReader(f)
        writer = csv.DictWriter(
            out_f, ["username", "age", "gender", "mother_tongue"], delimiter="\t"
        )
        for line in reader:
            writer.writerow(line)

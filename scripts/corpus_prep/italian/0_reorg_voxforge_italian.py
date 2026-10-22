import os
import shutil

root_dir = r"C:\Users\micha\Documents\Data\model_training_corpora\italian\voxforge-it"

if __name__ == "__main__":
    for speaker in os.listdir(root_dir):
        speaker_directory = os.path.join(root_dir, speaker)
        wav_dir = os.path.join(speaker_directory, "wav")
        etc_dir = os.path.join(speaker_directory, "etc")
        with open(os.path.join(etc_dir, "prompts-original"), "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(line)
                file_name, text = line.strip().split(" ", maxsplit=1)
                original_wav_path = os.path.join(wav_dir, f"{file_name}.wav")
                if os.path.exists(original_wav_path):
                    os.rename(
                        original_wav_path, os.path.join(speaker_directory, f"{file_name}.wav")
                    )
                with open(
                    os.path.join(speaker_directory, f"{file_name}.lab"), "w", encoding="utf8"
                ) as out_f:
                    out_f.write(text)
        shutil.rmtree(wav_dir, ignore_errors=True)
        shutil.rmtree(etc_dir, ignore_errors=True)

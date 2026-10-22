import os.path
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli

if sys.platform == "win32":
    root_dir = r"C:\Users\micha\Documents\Data\model_training_corpora\italian\mls_italian"
    output_dir = (
        r"C:\Users\micha\Documents\Data\model_training_corpora\italian\mls_italian_transcribed"
    )
else:
    root_dir = r"/mnt/d/Data/speech/model_training_corpora/italian/mls_italian"
    output_dir = r"/mnt/d/Data/speech/model_training_corpora/italian/mls_italian_transcribed"


if __name__ == "__main__":
    speakers = os.listdir(root_dir)
    for i, speaker in enumerate(speakers):
        speaker_dir = os.path.join(root_dir, speaker)
        if not os.path.isdir(speaker_dir):
            continue
        if speaker.startswith("."):
            continue
        output_speaker_dir = os.path.join(output_dir, speaker)
        if os.path.exists(output_speaker_dir) and len(os.listdir(speaker_dir)) / 2 == len(
            os.listdir(output_speaker_dir)
        ):
            continue
        print(speaker, i, len(speakers), "Files:", len(os.listdir(speaker_dir)))
        if False and len(os.listdir(speaker_dir)) > 10000:
            for f in os.listdir(speaker_dir):
                new_speaker = "_".join(f.split("_")[:2])
                new_speaker_directory = os.path.join(root_dir, new_speaker)
                os.makedirs(new_speaker_directory, exist_ok=True)
                os.rename(os.path.join(speaker_dir, f), os.path.join(new_speaker_directory, f))
            os.rmdir(speaker_dir)
            continue
        print(speaker, i, len(speakers))
    command = [
        "transcribe_whisper",
        root_dir,
        output_dir,
        "--language",
        "italian",
        "--no_clean",
        "--use_postgres",
        "-j",
        "20",
        "--architecture",
        "large-v3",
        "--cuda",
        "--incremental",
        "--vad",
        "--no_verbose",
        "--no_debug",
        "--overwrite",
    ]
    mfa_cli(command, standalone_mode=False)

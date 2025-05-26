import os.path
import sys

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\transcription_benchmarking"

models_dir = r"D:\Data\models"

if sys.platform == "win32":
    training_root = "D:/Data/speech/model_training_corpora"
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
    "spanish",
]

if __name__ == "__main__":
    for lang in languages:
        language_model_root = os.path.join(models_dir, lang)
        os.makedirs(language_model_root, exist_ok=True)
        versions = os.listdir(language_model_root)
        corpus_directory = os.path.join(training_root, lang, f"globalphone_{lang}")

        output_directory = os.path.join(root_dir, "transcriptions", lang, "whisper")
        if not os.path.exists(output_directory):
            command = [
                "transcribe_whisper",
                corpus_directory,
                output_directory,
                "--language",
                lang,
                "--clean",
                "--use_postgres",
                "-j",
                "10",
                "--architecture",
                "large-v3",
                "--cuda",
                "--vad",
                "--no_verbose",
                "--evaluate",
                "--no_debug",
                "--overwrite",
            ]
            print(command)
            mfa_cli(command, standalone_mode=False)

        for version in versions:
            version_root = os.path.join(language_model_root, version)
            os.makedirs(version_root, exist_ok=True)
            files = os.listdir(version_root)
            acoustic_model_path = None
            dictionary_path = None
            for f in files:
                if f.endswith("_lm.zip"):
                    pass
                elif f.endswith(".zip"):
                    acoustic_model_path = os.path.join(version_root, f)
                else:
                    dictionary_path = os.path.join(version_root, f)
            if acoustic_model_path is None:
                continue
            language_model_path = os.path.join(version_root, f"globalphone_{lang}_lm.zip")
            output_directory = os.path.join(root_dir, "transcriptions", lang, version)
            if not os.path.exists(language_model_path):
                command = [
                    "train_lm",
                    corpus_directory,
                    language_model_path,
                    "--dictionary_path",
                    dictionary_path,
                    "-j",
                    "10",
                    "--clean",
                    "--no_verbose",
                    "--no_debug",
                    "--use_mp" "--use_postgres",
                    "--oov_count_threshold",
                    "0",
                    "--order",
                    "5",
                ]
                print(command)
                mfa_cli(command, standalone_mode=False)
            if os.path.exists(output_directory):
                continue
            command = [
                "transcribe",
                corpus_directory,
                dictionary_path,
                acoustic_model_path,
                language_model_path,
                output_directory,
                "-j",
                "10",
                "--clean",
                "--no_verbose",
                "--no_debug",
                "--use_mp",
                "--use_cutoff_model",
                "--evaluate",
                "--output_type",
                "alignment",
                "--include_original_text",
                "--use_postgres",
                "--cleanup_textgrids",
                "--beam",
                "10",
                "--retry_beam",
                "40",
            ]
            print(command)
            mfa_cli(command, standalone_mode=False)

from pathlib import Path

from montreal_forced_aligner import config

config.USE_POSTGRES = False
config.CLEAN = True
config.QUIET = True
config.TEMPORARY_DIRECTORY = Path(__file__).parent.joinpath("temp")

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = Path(r"D:\Data\speech\model_training_corpora")


languages = [
    #'english',
    "korean",
    "bulgarian",
    "vietnamese",
    "serbo-croatian",
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
]

languages = [
    "spanish",
]

dictionary_mapping = {
    #'mls_spanish': r"C:\Users\micha\Documents\Dev\mfa-models\dictionary\training\spanish_spain_mfa.dict"
}

if __name__ == "__main__":
    for language_directory in root_dir.iterdir():
        if not language_directory.is_dir():
            continue
        if language_directory.name not in languages:
            continue
        print(language_directory.name)
        dictionary_path = language_directory.joinpath(
            f"{language_directory.name}_speaker_dictionaries.yaml"
        )
        output_directory = config.TEMPORARY_DIRECTORY.joinpath(language_directory.name)
        output_directory.mkdir(exist_ok=True, parents=True)
        command = [
            "validate",
            str(language_directory),
            str(dictionary_path),
            "--output_directory",
            str(output_directory),
            "-j",
            "10",
            "--clean",
            "--no_debug",
            "--no_verbose",
            "--use_mp",
            "--no_use_threading",
            "--use_postgres",
            "--skip_acoustics",
            "--no_final_clean",
        ]
        print(command)
        mfa_cli(command, standalone_mode=False)
        for corpus_directory in language_directory.iterdir():
            if not corpus_directory.is_dir():
                continue
            if corpus_directory.name not in dictionary_mapping:
                continue
            output_directory = config.TEMPORARY_DIRECTORY.joinpath(corpus_directory.name)
            output_directory.mkdir(exist_ok=True, parents=True)
            command = [
                "validate",
                str(corpus_directory),
                dictionary_mapping[corpus_directory.name],
                "--output_directory",
                str(output_directory),
                "-j",
                "10",
                "--clean",
                "--no_debug",
                "--no_verbose",
                "--use_mp",
                "--no_use_threading",
                "--use_postgres",
                "--skip_acoustics",
                "--no_final_clean",
            ]
            print(command)
            mfa_cli(command, standalone_mode=False)

from pathlib import Path

from montreal_forced_aligner.command_line.mfa import mfa_cli

repo_root = Path(__file__).parent.parent.parent.parent

experiment_dir = Path(r"D:\Data\experiments\mfa_model_benchmarks\huggingface_models")
training_data_root = Path(r"C:\Users\micha\Documents\Data\model_training_corpora")
benchmark_data_root = Path(r"C:\Users\micha\Documents\Data\benchmarks")
hf_trained_model_directory = repo_root.joinpath("staging")
reference_model_directory = hf_trained_model_directory.joinpath("backup")

model_specific_arguments = {
    "english_mfa": ["--dialect", "english_us"],
    "portuguese_mfa": ["--dialect", "portuguese_brazil"],
    "spanish_mfa": ["--dialect", "spanish_latin_america"],
    "serbocroatian_mfa": ["--dialect", "serbocroatian_croatian"],
    "vietnamese_mfa": ["--dialect", "vietnamese_hanoi"],
    "mandarin_mfa": ["--dialect", "mandarin_china"],
}

if __name__ == "__main__":
    benchmark_datasets = {
        "english_mfa": benchmark_data_root.joinpath(
            r"aligned-librispeech", "librispeech_test_clean"
        ),
        "english_us_arpa": benchmark_data_root.joinpath(
            r"aligned-librispeech", "librispeech_test_clean"
        ),
    }

    globalphone_languages = [
        "bulgarian",
        "czech",
        "french",
        "german",
        "hausa",
        "korean",
        "mandarin",
        "japanese",
        "polish",
        "portuguese",
        "russian",
        "serbocroatian",
        "spanish",
        "swahili",
        "thai",
        "turkish",
        "ukrainian",
        "swedish",
        "vietnamese",
    ]
    for lang in globalphone_languages:
        globalphone_name = f"globalphone_{lang}"
        if lang == "serbocroatian":
            globalphone_name = globalphone_name.replace("serbocroatian", "croatian")
        benchmark_datasets[f"{lang}_mfa"] = training_data_root.joinpath(lang, globalphone_name)
    for model_path in hf_trained_model_directory.iterdir():
        model_name = model_path.name
        if model_name == "backup":
            continue
        print(model_name)
        reference_model_path = reference_model_directory.joinpath(model_name)
        if not reference_model_path.exists():
            print(f"Couldn't find {reference_model_path}, skipping!")
            continue
        corpus_directory = benchmark_datasets[model_name]
        output_directory = experiment_dir.joinpath("hf_alignments", model_name)
        if not output_directory.exists():
            command = [
                "align_hf",
                str(corpus_directory),
                str(model_path),
                str(output_directory),
                "-j",
                "10",
                "--clean",
                "--no_debug",
                "--use_mp",
                "--use_cutoff_model",
                "--use_postgres",
                "--cleanup_textgrids",
                "--beam",
                "10",
                "--retry_beam",
                "40",
                "--use_g2p",
                "--oov_count_threshold",
                "0",
            ]
            if model_name in model_specific_arguments:
                command += model_specific_arguments[model_name]
            print(command)
            mfa_cli(command, standalone_mode=False)
        output_directory = experiment_dir.joinpath("old_model_alignments", model_name)
        if not output_directory.exists():
            command = [
                "align_hf",
                str(corpus_directory),
                str(reference_model_path),
                str(output_directory),
                "-j",
                "10",
                "--clean",
                "--no_debug",
                "--use_mp",
                "--use_cutoff_model",
                "--use_postgres",
                "--cleanup_textgrids",
                "--beam",
                "10",
                "--retry_beam",
                "40",
                "--use_g2p",
                "--oov_count_threshold",
                "0",
            ]
            if model_name in model_specific_arguments:
                command += model_specific_arguments[model_name]
            print(command)
            mfa_cli(command, standalone_mode=False)

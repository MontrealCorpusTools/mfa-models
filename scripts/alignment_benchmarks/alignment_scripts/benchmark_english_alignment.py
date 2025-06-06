import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\alignment_benchmarking"
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\2.0.0a_archived"
mfa21_dir = r"D:\Data\models\2.1_trained"
mfa22_dir = r"D:\Data\models\2.2_trained"
mfa30_dir = r"D:\Data\models\3.0_trained"
mfa31_dir = r"D:\Data\models\3.1_trained"
trained22_dir = r"D:\Data\models\2.2_trained\buckeye"
trained30_dir = r"D:\Data\models\3.0_trained\buckeye"
mapping_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mapping_files"
)

corpus_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\benchmark",
    "buckeye": r"D:\Data\speech\Buckeye\buckeye_corpus_benchmark",
}

reference_directories = {
    "timit": r"D:\Data\speech\benchmark_datasets\timit\reference",
    "buckeye": r"D:\Data\speech\Buckeye\buckeye_reference_alignments",
}

conditions = {
    "arpa_1.0": (os.path.join(mfa10_dir, "english.dict"), os.path.join(mfa10_dir, "english.zip")),
    "arpa_2.0": (
        os.path.join(mfa20_dir, "english_us_arpa.dict"),
        os.path.join(mfa20_dir, "english_us_arpa.zip"),
    ),
    "arpa_2.0a": (
        os.path.join(mfa20a_dir, "english_us_arpa.dict"),
        os.path.join(mfa20a_dir, "english_us_arpa.zip"),
    ),
    "mfa_2.0": (
        os.path.join(mfa20_dir, "english_us_mfa.dict"),
        os.path.join(mfa20_dir, "english_mfa.zip"),
    ),
    "mfa_2.0a": (
        os.path.join(mfa20a_dir, "english_us_mfa.dict"),
        os.path.join(mfa20a_dir, "english_mfa.zip"),
    ),
    "mfa_2.1": (
        os.path.join(mfa21_dir, "english_us_mfa.dict"),
        os.path.join(mfa21_dir, "english_mfa.zip"),
    ),
    "mfa_2.2": (
        os.path.join(mfa22_dir, "english_us_mfa.dict"),
        os.path.join(mfa22_dir, "english_mfa.zip"),
    ),
    "mfa_3.0": (
        os.path.join(mfa30_dir, "english_us_mfa.dict"),
        os.path.join(mfa30_dir, "english_mfa.zip"),
    ),
    "mfa_3.0_finetune": (
        os.path.join(mfa30_dir, "english_us_mfa.dict"),
        os.path.join(mfa30_dir, "english_mfa.zip"),
    ),
    "mfa_3.1": (
        os.path.join(mfa31_dir, "english_us_mfa.dict"),
        os.path.join(mfa31_dir, "english_mfa.zip"),
    ),
    "arpa_3.0": (
        os.path.join(mfa30_dir, "english_us_arpa.dict"),
        os.path.join(mfa30_dir, "english_us_arpa.zip"),
    ),
    "trained_2.2": (
        os.path.join(trained22_dir, "english_us_mfa.dict"),
        os.path.join(trained22_dir, "english_mfa.zip"),
    ),
    "trained_3.0": (
        os.path.join(trained30_dir, "english_us_mfa.dict"),
        os.path.join(trained30_dir, "english_mfa.zip"),
    ),
    "arpa_2.2": (
        os.path.join(mfa20a_dir, "english_us_arpa.dict"),
        os.path.join(mfa20a_dir, "english_us_arpa.zip"),
    ),
}
mapping_files = {}
for k in conditions.keys():
    for corpus in corpus_directories:
        if "arpa" in k:
            phone_set = "arpa"
        else:
            phone_set = "mfa"
        mapping_files[(k, corpus)] = os.path.join(
            mapping_directory, f"{phone_set}_{corpus}_mapping.yaml"
        )

if __name__ == "__main__":
    for condition, (dictionary_path, model_path) in conditions.items():
        print(condition)
        for corpus, root in corpus_directories.items():
            output_directory = os.path.join(root_dir, "alignments", condition, corpus)
            if os.path.exists(output_directory):
                continue
            if not os.path.exists(model_path):
                continue
            if not os.path.exists(dictionary_path):
                continue
            command = [
                "align",
                root,
                dictionary_path,
                model_path,
                output_directory,
                "-j",
                "10",
                "--clean",
                "--no_debug",
                "--use_mp",
                "--use_cutoff_model",
                "--use_postgres",
                "--cleanup_textgrids",
                "--reference_directory",
                reference_directories[corpus],
                "--custom_mapping_path",
                mapping_files[(condition, corpus)],
                "--beam",
                "10",
                "--retry_beam",
                "40",
            ]
            if "finetune" in condition:
                command += ["--fine_tune"]
            print(command)
            mfa_cli(command, standalone_mode=False)

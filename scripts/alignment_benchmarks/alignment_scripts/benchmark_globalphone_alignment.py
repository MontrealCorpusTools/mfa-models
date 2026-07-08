import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r"D:\Data\experiments\mfa_model_benchmarks"
model_dir = os.path.join(root_dir, "models")
alignment_dir = os.path.join(root_dir, "alignments")
mapping_directory = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mapping_files"
)

benchmark_dir = (
    r"C:\Users\micha\Documents\Data\model_training_corpora\portuguese\globalphone_portuguese"
)
temp_dir = r"D:\temp\align_evaluation_temp"

mapping_files = {
    #'mfa': os.path.join(mapping_directory, "mfa_csj_mapping.yaml")
}


if __name__ == "__main__":
    conditions = {
        x: (
            os.path.join(model_dir, x, "portuguese_brazil_mfa.dict"),
            os.path.join(model_dir, x, "portuguese_mfa.zip"),
        )
        for x in os.listdir(model_dir)
    }
    for condition, (dictionary_path, model_path) in conditions.items():
        output_directory = os.path.join(root_dir, condition, "globalphone_portuguese")
        if os.path.exists(output_directory):
            continue
        command = [
            "align",
            benchmark_dir,
            dictionary_path,
            model_path,
            output_directory,
            "-j",
            "10",
            "--clean",
            "--debug",
            "--use_cutoff_model",
            #'--custom_mapping_path',
            # mapping_files[condition.split('_')[0]],
            "--beam",
            "10",
            "--retry_beam",
            "40",
        ]
        print(command)
        mfa_cli(command, standalone_mode=False)
    baseline_version = "v2.0.0a"
    for condition, (dictionary_path, model_path) in conditions.items():
        if condition == baseline_version:
            continue
        reference_directory = os.path.join(root_dir, baseline_version, "globalphone_portuguese")
        test_directory = os.path.join(root_dir, condition, "globalphone_portuguese")
        output_directory = os.path.join(
            root_dir, "comparisons", condition, "globalphone_portuguese"
        )
        if os.path.exists(output_directory):
            continue
        command = [
            "compare_alignments",
            reference_directory,
            test_directory,
            output_directory,
            # "--custom_mapping_path",
            # mapping_file,
            "--audio_directory",
            benchmark_dir,
            "--clean",
            "-j",
            "10",
            "--use_mp",
            "--no_final_clean",
        ]
        print(command)
        mfa_cli(command, standalone_mode=False)

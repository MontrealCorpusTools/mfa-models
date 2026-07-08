import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

old_alignments_directory = (
    r"D:\Data\experiments\mfa_model_benchmarks\huggingface_models\old_model_alignments"
)
hf_alignment_directory = (
    r"D:\Data\experiments\mfa_model_benchmarks\huggingface_models\hf_alignments"
)
comparison_directory = (
    r"D:\Data\experiments\mfa_model_benchmarks\huggingface_models\alignment_comparison"
)


if __name__ == "__main__":
    for model_name in os.listdir(old_alignments_directory):
        reference_directory = os.path.join(old_alignments_directory, model_name)
        hf_directory = os.path.join(hf_alignment_directory, model_name)
        comparison_output_directory = os.path.join(comparison_directory, model_name)
        if not os.path.exists(comparison_output_directory):
            command = [
                "compare_alignments",
                reference_directory,
                hf_directory,
                comparison_output_directory,
                "--clean",
                "-j",
                "10",
                "--no_use_mp",
                "--use_threading",
                "--no_final_clean",
            ]
            print(command)
            mfa_cli(command, standalone_mode=False)

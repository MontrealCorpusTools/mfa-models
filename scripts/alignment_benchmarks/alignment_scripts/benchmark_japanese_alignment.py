import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r'D:\Data\experiments\alignment_benchmarking\alignments'
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\final_training"
mfa30_dir = r"D:\Data\models\3.0_trained"
mapping_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mapping_files')

benchmark_dir = r'D:\Data\speech\benchmark_datasets\csj\csj_benchmark'
original_dir = r'D:\Data\speech\benchmark_datasets\csj\original'
reference_dir = r'D:\Data\speech\benchmark_datasets\csj\csj_reference'
temp_dir = r'D:\temp\align_evaluation_temp'

mapping_files = {
    'mfa': os.path.join(mapping_directory, "mfa_csj_mapping.yaml")
}

conditions = {
    'mfa_3.0': (os.path.join(mfa30_dir, 'japanese_mfa.dict'), os.path.join(mfa30_dir, "japanese_mfa.zip")),

}


if __name__ == '__main__':
    for condition, (dictionary_path, model_path) in conditions.items():
        output_directory = os.path.join(root_dir, condition, 'csj')
        if os.path.exists(output_directory):
            continue
        command = ['align',
                   benchmark_dir,
                   dictionary_path,
                   model_path,
                   output_directory,
                   '-j', '10',
                   '--clean',
                   '--debug',
                    '--use_cutoff_model',
                   '--reference_directory',
                   reference_dir,
                   '--audio_directory',
                   original_dir,
                   '--custom_mapping_path',
                    mapping_files[condition.split('_')[0]],
                   '--beam', '10', '--retry_beam', '40'
                   ]
        print(command)
        mfa_cli(command, standalone_mode=False)

import os

from montreal_forced_aligner.command_line.mfa import mfa_cli

root_dir = r'D:\Data\experiments\alignment_benchmarking'
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\final_training"
mfa30_dir = r"D:\Data\models\3.0_trained"
evaluation_dir = os.path.join(root_dir, 'alignments')
benchmark_script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

mapping_directory = os.path.join(benchmark_script_dir, 'mapping_files')
g2p_staging_dir = os.path.join(os.path.dirname(os.path.dirname(benchmark_script_dir)), 'g2p', 'staging')

models = [x for x in os.listdir(root_dir) if x.endswith('.zip')]

benchmark_dir = r'D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_corpus_benchmark'
reference_dir = r'D:\Data\speech\benchmark_datasets\seoul_corpus\seoul_reference_alignments'
temp_dir = r'D:\temp\align_evaluation_temp'

mapping_files = {
    'gp': os.path.join(mapping_directory, "korean_gp_mapping.yaml"),
    'mfa': os.path.join(mapping_directory, "korean_mfa_mapping.yaml")
}

conditions = {
    'gp_1.0': (os.path.join(mfa10_dir, 'KO_dictionary.txt'), os.path.join(mfa10_dir, "korean.zip")),
    'mfa_2.0': (os.path.join(mfa20_dir, 'korean_mfa.dict'), os.path.join(mfa20_dir, "korean_mfa.zip")),
    'mfa_2.0a': (os.path.join(mfa20a_dir, 'korean_mfa.dict'), os.path.join(mfa20a_dir, "korean_mfa.zip")),
    'mfa_3.0': (os.path.join(mfa30_dir, 'korean_mfa.dict'), os.path.join(mfa30_dir, "korean_mfa.zip")),

}


if __name__ == '__main__':
    for condition, (dictionary_path, model_path) in conditions.items():

        if not os.path.exists(model_path):
            continue
        output = os.path.join(evaluation_dir, condition, "seoul")
        if os.path.exists(output):
            continue
        print(condition)
        command = ['align',
                   benchmark_dir,
                   dictionary_path,
                   model_path,
                   output,
                   '-j', '10',
                   '--clean',
                   '--debug',
                   '--use_mp',
                   '--use_cutoff_model',
                   '--use_postgres',
                   '--cleanup_textgrids',
                   '--reference_directory',
                   reference_dir,
                   '--custom_mapping_path',
                    mapping_files[condition.split('_')[0]],
                   '--beam', '10', '--retry_beam', '40',
        '--g2p_model_path', os.path.join(g2p_staging_dir, "korean_jamo_mfa.zip"),
                   ]
        mfa_cli(command, standalone_mode=False)

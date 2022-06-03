import os
import subprocess

root_dir = r'D:\Data\experiments\alignment_benchmarking'
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\final_training"

corpus_directories = {
    'buckeye': r'D:\Data\speech\Buckeye',
    'timit': r'D:\Data\speech\benchmark_datasets\timit'
}

conditions = {
    'arpa_1.0': (os.path.join(mfa10_dir, 'english.dict'), os.path.join(mfa10_dir, 'english.zip')),
    'arpa_2.0': (os.path.join(mfa20_dir, 'english_us_arpa.dict'), os.path.join(mfa20_dir, "english_us_arpa.zip")),
    'arpa_2.0a': (os.path.join(mfa20a_dir, 'english_us_arpa.dict'), os.path.join(mfa20a_dir, "english_us_arpa.zip")),
    'mfa_2.0': (os.path.join(mfa20_dir, 'english_us_mfa.dict'), os.path.join(mfa20_dir, "english_mfa.zip")),
    'mfa_2.0a': (os.path.join(mfa20a_dir, 'english_us_mfa.dict'), os.path.join(mfa20a_dir, "english_mfa.zip")),
}
mapping_files = {}
for k in conditions.keys():
    for corpus in corpus_directories:
        if 'arpa' in k:
            phone_set = 'arpa'
        else:
            phone_set = 'mfa'
        mapping_files[k] = os.path.join(root_dir, f"{phone_set}_{corpus}_mapping.yaml")

for condition, (dictionary_path, model_path) in conditions.items():
    for corpus, root in corpus_directories.items():
        output_directory = os.path.join(root_dir, 'alignments', condition, corpus)
        if os.path.exists(output_directory):
            continue
        subprocess.check_call(['mfa', 'align',
                               os.path.join(root, 'benchmark'),
                               dictionary_path,
                               model_path,
                               output_directory,
                               '-j', '10',
                               '--clean',
                               '-t',
                               os.path.join(root_dir, f'temp_{condition}_{corpus}'),
                               '--reference_directory',
                               os.path.join(root, 'reference'),
                               '--custom_mapping_path',
                                mapping_files[condition],
                               '--beam', '20', '--retry_beam', '80'
                               ], env=os.environ)

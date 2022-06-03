import os

from montreal_forced_aligner.command_line.align import run_align_corpus

root_dir = r'D:\Data\experiments\korean'
mfa10_dir = r"D:\Data\models\1.0_archived"
mfa20_dir = r"D:\Data\models\2.0_archived"
mfa20a_dir = r"D:\Data\models\final_training"
evaluation_dir = os.path.join(root_dir, 'evaluations')

models = [x for x in os.listdir(root_dir) if x.endswith('.zip')]

benchmark_dir = r'D:\Data\speech\korean_corpora\seoul_corpus\seoul_corpus_benchmark'
reference_dir = r'D:\Data\speech\korean_corpora\seoul_corpus\seoul_reference_alignments'
temp_dir = r'D:\temp\align_evaluation_temp'

mapping_files = {
    'gp': os.path.join(root_dir, "korean_gp_mapping.yaml"),
    'mfa': os.path.join(root_dir, "korean_mfa_mapping.yaml")
}

conditions = {
    'gp_1.0': (os.path.join(mfa10_dir, 'KO_dictionary.txt'), os.path.join(mfa10_dir, "korean.zip")),
    'mfa_2.0': (os.path.join(mfa20_dir, 'korean_mfa.dict'), os.path.join(mfa20_dir, "korean_mfa.zip")),
    'mfa_2.0a': (os.path.join(mfa20a_dir, 'korean_mfa.dict'), os.path.join(mfa20a_dir, "korean_mfa.zip")),

}

class AlignDummyArgs(object):
    def __init__(self):
        self.num_jobs = 5
        self.speaker_characters = 0
        self.verbose = False
        self.clean = True
        self.debug = False
        self.corpus_directory = benchmark_dir
        self.reference_directory = reference_dir
        self.acoustic_model_path = 'english'
        self.dictionary_path = 'english'
        self.temporary_directory = temp_dir
        self.output_directory = None
        self.custom_mapping_path = None
        self.config_path = None

if __name__ == '__main__':
    for condition, (dictionary_path, model_path) in conditions.items():
        if not os.path.exists(model_path):
            continue
        output = os.path.join(evaluation_dir, condition)
        if os.path.exists(output):
            continue
        print(condition)
        args = AlignDummyArgs()
        args.custom_mapping_path = mapping_files[condition.split('_')[0]]
        args.dictionary_path = dictionary_path
        args.acoustic_model_path = model_path
        args.output_directory = output
        run_align_corpus(args)

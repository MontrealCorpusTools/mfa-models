import sqlalchemy
from pathlib import Path
from montreal_forced_aligner import config

config.USE_POSTGRES = False
config.CLEAN = True
config.QUIET = True
config.TEMPORARY_DIRECTORY = Path(__file__).parent.joinpath('temp')

from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpus
from montreal_forced_aligner.db import Utterance
root_dir = Path(r'D:\Data\speech\model_training_corpora')


languages = [

    #'english',
    'korean',
    'bulgarian',
    'vietnamese',
             'croatian',
    'hausa',
    'ukrainian',
'thai',
'swahili',
     'turkish',
    'spanish',
             'swedish',
             'portuguese', 'polish',
             'french',
             'czech', 'japanese',
             'russian',
    'german',
     'mandarin', 'tamil', 'hindi-urdu'
             ]

languages = ['japanese']

for language_directory in root_dir.iterdir():
    if not language_directory.is_dir():
        continue
    if language_directory.name not in languages:
        continue
    print(language_directory.name)
    for corpus_directory in language_directory.iterdir():
        if not corpus_directory.is_dir():
            continue
        corpus_name = corpus_directory.name
        print(corpus_name)
        print('='*len(corpus_name))
        c = AcousticCorpus(corpus_directory=corpus_directory)
        c._load_corpus()
        print("Num utterances:", c.num_utterances)
        print("Num files:", c.num_files)
        print("Num speakers:", c.num_speakers)
        with c.session() as session:
            total_duration = session.query(sqlalchemy.func.sum(Utterance.duration)).filter(Utterance.text != '').first()[0]/3600
        print("Num hours:", total_duration)
        print()

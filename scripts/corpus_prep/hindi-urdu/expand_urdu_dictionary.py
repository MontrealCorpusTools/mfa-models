import collections
import pathlib

root_dir = pathlib.Path(__file__).parents[3]

training_directory = pathlib.Path(r"D:\Data\speech\model_training_corpora\hindi-urdu")

urdu_corpora = ["common_voice_urdu", "shrutilipi_urdu"]

# g2p_model = G2PModel(root_dir.joinpath('dictionary', 'training', 'urdu_to_hindi_g2p.zip'))

urdu_dictionary_path = root_dir.joinpath("dictionary", "training", "urdu_mfa.dict")
urdu_to_hindi_dictionary_path = root_dir.joinpath("dictionary", "training", "urdu_to_hindi.dict")
urdu_words_path = root_dir.joinpath("dictionary", "training", "urdu_mfa_new.dict")
output_urdu_dictionary_path = root_dir.joinpath(
    "dictionary", "training", "urdu_mfa_new_output.dict"
)
hindi_dictionary_path = root_dir.joinpath("dictionary", "training", "hindi_mfa.dict")


def transliterate():
    from ai4bharat.transliteration import XlitEngine

    urdu_to_e = XlitEngine(src_script_type="indic", beam_width=10, rescore=True)
    e_to_hindi = XlitEngine("hi", beam_width=10, rescore=True)

    with open(urdu_words_path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            rom = urdu_to_e.translit_word(line, lang_code="ur", topk=1)[0]
            hindi_word = e_to_hindi.translit_word(rom, topk=1)["hi"][0]
            if hindi_word in hindi_dict and line not in new_urdu_prons:
                new_urdu_prons[line] = hindi_dict[hindi_word]

    with open(output_urdu_dictionary_path, "w", encoding="utf8") as f:
        for k, v in new_urdu_prons.items():
            for p in v:
                f.write(f"{k}\t{p}\n")


def collect_oovs():
    from montreal_forced_aligner import config

    config.USE_POSTGRES = False
    config.CLEAN = True
    config.QUIET = True
    config.TEMPORARY_DIRECTORY = pathlib.Path(__file__).parent.parent.joinpath("temp")

    from montreal_forced_aligner.corpus.acoustic_corpus import AcousticCorpusWithPronunciations
    from montreal_forced_aligner.data import WordType
    from montreal_forced_aligner.db import Word

    oovs = []
    for c in urdu_corpora:
        corpus_dir = training_directory.joinpath(c)

        c = AcousticCorpusWithPronunciations(
            corpus_directory=corpus_dir,
            dictionary_path=urdu_dictionary_path,
        )
        if not c.text_normalized:
            c.initialize_database()
            c.dictionary_setup()
            c._load_corpus()
            c.initialize_jobs()
            c.normalize_text()
        with c.session() as session:
            query = (
                session.query(Word)
                .filter(Word.word_type == WordType.oov)
                .order_by(Word.count.desc())
            )
            for w in query:
                urdu_word = w.word
                if urdu_word in urdu_to_hindi:
                    hindi_word = urdu_to_hindi[urdu_word]
                else:
                    oovs.append(urdu_word)
                    continue
                # print(urdu_word)
                # print(hindi_word, hindi_word in hindi_dict)
                if hindi_word in hindi_dict and urdu_word not in new_urdu_prons:
                    new_urdu_prons[urdu_word] = hindi_dict[hindi_word]

    with open(urdu_words_path, "w", encoding="utf8") as f:
        for k in oovs:
            f.write(f"{k}\n")


if __name__ == "__main__":
    hindi_dict = collections.defaultdict(list)
    with open(hindi_dictionary_path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            word, pron = line.split("\t")
            hindi_dict[word].append(pron)

    new_urdu_prons = {}
    urdu_to_hindi = {}
    with open(urdu_to_hindi_dictionary_path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            urdu, hindi = line.split("\t")
            urdu_to_hindi[urdu] = hindi
            if hindi in hindi_dict:
                new_urdu_prons[urdu] = hindi_dict[hindi]
    # collect_oovs()
    transliterate()

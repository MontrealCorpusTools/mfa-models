import collections
import json
import os
import random
import shutil
import re
import pathlib
import typing
from line_profiler_pycharm import profile
from datetime import datetime
import numpy as np
import sqlalchemy
from sqlalchemy.orm import subqueryload
from montreal_forced_aligner import config

config.TEMPORARY_DIRECTORY = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
config.USE_POSTGRES = False
import montreal_forced_aligner.utils
from montreal_forced_aligner.models import MODEL_TYPES
from montreal_forced_aligner.db import Word, Phone, PhoneType, Pronunciation
from montreal_forced_aligner.dictionary.multispeaker import MultispeakerDictionary
from montreal_forced_aligner.data import voiced_variants, voiceless_variants, PhoneSetType

rng = np.random.default_rng(1234)
random.seed(1234)

root_dir = pathlib.Path(__file__).resolve().parent
template_dir = root_dir.joinpath('templates')

CURRENT_MODEL_VERSION = '3.0.0'

# Get corpus information

current_corpora = {'english': ['Common Voice English v8_0', 'LibriSpeech English',
                                          'Corpus of Regional African American Language v2021_07',
                                          "Google Nigerian English", "Google UK and Ireland English",
                                          "NCHLT English", "ARU English corpus", "ICE-Nigeria",
                               "A Scripted Pakistani English Daily-use Speech Corpus",
                               "L2-ARCTIC"],
                   'czech': ['Common Voice Czech v9_0', 'GlobalPhone Czech v3_1',
                                        "Large Corpus of Czech Parliament Plenary Hearings", "Czech Parliament Meetings"],
                   'hausa': ['Common Voice Hausa v9_0', 'GlobalPhone Hausa v3_1'],
                   'swahili': ['Common Voice Swahili v9_0', 'ALFFA Swahili', 'GlobalPhone Swahili v3_1'],
                   'korean': ['GlobalPhone Korean v3_1',
                                         'Deeply Korean read speech corpus public sample',
                                         'Pansori TEDxKR', 'Zeroth Korean', 'Seoul Corpus',
                              "ASR-KCSC: A Korean Conversational Speech Corpus",
"ASR-SKDuSC: A Scripted Korean Daily-use Speech Corpus",
"Korean Single Speaker Speech Dataset",
"Common Voice Korean v16_1",
                              ],
                   'mandarin': ['Common Voice Chinese (China) v9_0', 'Common Voice Chinese (Taiwan) v9_0',
                                           'AI-DataTang Corpus', 'AISHELL-3', 'THCHS-30',
                                           'GlobalPhone Chinese-Mandarin v3_1'],
                   'japanese': ['Common Voice Japanese v9_0', 'GlobalPhone Japanese v3_1',
                                           'Microsoft Speech Language Translation Japanese',
                                            'Japanese Versatile Speech', 'TEDxJP-10K v1_1'],
                   'thai': ['Common Voice Thai v9_0', 'GlobalPhone Thai v3_1'],
                   'vietnamese': ['Common Voice Vietnamese v9_0', 'VIVOS', 'GlobalPhone Vietnamese v3_1'],
                   }

model_corpus_mapping = {
    "Abkhaz CV acoustic model v2_0_0": ['Common Voice Abkhaz v7_0'],
    "Armenian CV acoustic model v2_0_0": ['Common Voice Armenian v7_0'],
    "Bashkir CV acoustic model v2_0_0": ['Common Voice Bashkir v7_0'],
    "Basque CV acoustic model v2_0_0": ['Common Voice Basque v7_0'],
    "Belarusian CV acoustic model v2_0_0": ['Common Voice Belarusian v7_0'],
    "Bulgarian CV acoustic model v2_0_0": ['Common Voice Bulgarian v7_0'],
    "Chuvash CV acoustic model v2_0_0": ['Common Voice Chuvash v7_0'],
    "Czech CV acoustic model v2_0_0": ['Common Voice Czech v7_0'],
    "Dutch CV acoustic model v2_0_0": ['Common Voice Dutch v7_0'],
    "Georgian CV acoustic model v2_0_0": ['Common Voice Georgian v7_0'],
    "Greek CV acoustic model v2_0_0": ['Common Voice Greek v7_0'],
    "Guarani CV acoustic model v2_0_0": ['Common Voice Guarani v7_0'],
    "Hausa CV acoustic model v2_0_0": ['Common Voice Hausa v7_0'],
    "Hungarian CV acoustic model v2_0_0": ['Common Voice Hungarian v7_0'],
    "Italian CV acoustic model v2_0_0": ['Common Voice Italian v7_0'],
    "Kazakh CV acoustic model v2_0_0": ['Common Voice Kazakh v7_0'],
    "Kurmanji CV acoustic model v2_0_0": ['Common Voice Kurmanji v7_0'],
    "Kyrgyz CV acoustic model v2_0_0": ['Common Voice Kyrgyz v7_0'],
    "Polish CV acoustic model v2_0_0": ['Common Voice Polish v7_0'],
    "Portuguese CV acoustic model v2_0_0": ['Common Voice Portuguese v7_0'],
    "Romanian CV acoustic model v2_0_0": ['Common Voice Romanian v7_0'],
    "Russian CV acoustic model v2_0_0": ['Common Voice Russian v7_0'],
    "Sorbian (Upper) CV acoustic model v2_0_0": ['Common Voice Sorbian Upper v7_0'],
    "Swedish CV acoustic model v2_0_0": ['Common Voice Swedish v7_0'],
    "Tamil CV acoustic model v2_0_0": ['Common Voice Tamil v7_0'],
    "Tatar CV acoustic model v2_0_0": ['Common Voice Tatar v7_0'],
    "Thai CV acoustic model v2_0_0": ['Common Voice Thai v7_0'],
    "Turkish CV acoustic model v2_0_0": ['Common Voice Turkish v7_0'],
    "Ukrainian CV acoustic model v2_0_0": ['Common Voice Ukrainian v7_0'],
    "Uyghur CV acoustic model v2_0_0": ['Common Voice Uyghur v7_0'],
    "Uzbek CV acoustic model v2_0_0": ['Common Voice Uzbek v7_0'],
    "Vietnamese CV acoustic model v2_0_0": ['Common Voice Vietnamese v7_0'],
    "English (US) ARPA acoustic model v2_0_0": ['LibriSpeech English'],
    "English (US) ARPA acoustic model v2_0_0a": ['LibriSpeech English'],
    "English (US) ARPA acoustic model v3_0_0": ['LibriSpeech English'],
    "English MFA acoustic model v2_0_0": ['Common Voice English v8_0', 'LibriSpeech English',
                                          'Corpus of Regional African American Language v2021_07',
                                          "Google Nigerian English", "Google UK and Ireland English",
                                          "NCHLT English", "ARU English corpus"],
    "English MFA acoustic model v2_0_0a": ['Common Voice English v8_0', 'LibriSpeech English',
                                          'Corpus of Regional African American Language v2021_07',
                                          "Google Nigerian English", "Google UK and Ireland English",
                                          "NCHLT English", "ARU English corpus"],
    "English MFA acoustic model v2_2_1": ['Common Voice English v8_0', 'LibriSpeech English',
                                          'Corpus of Regional African American Language v2021_07',
                                          "Google Nigerian English", "Google UK and Ireland English",
                                          "NCHLT English", "ARU English corpus", "ICE-Nigeria",
                               "A Scripted Pakistani English Daily-use Speech Corpus",
                               "L2-ARCTIC"],
    "English MFA acoustic model v3_0_0": ['Common Voice English v8_0', 'LibriSpeech English',
                                          'Corpus of Regional African American Language v2021_07',
                                          "Google Nigerian English", "Google UK and Ireland English",
                                          "NCHLT English", "ARU English corpus", "ICE-Nigeria",
                               "A Scripted Pakistani English Daily-use Speech Corpus",
                               "L2-ARCTIC"],
    "English MFA ivector extractor v2_1_0": current_corpora['english'],
    "Multilingual MFA ivector extractor v2_1_0": [x for k in ['english', 'czech', 'hausa', 'swahili', 'thai', 'vietnamese', 'japanese', 'mandarin'] for x in current_corpora[k]],
    "French MFA acoustic model v2_0_0": ['Common Voice French v8_0', 'Multilingual LibriSpeech French', 'GlobalPhone French v3_1',
                                         'African-accented French'],
    "French MFA acoustic model v2_0_0a": ['Common Voice French v8_0', 'Multilingual LibriSpeech French', 'GlobalPhone French v3_1',
                                         'African-accented French'],
    "German MFA acoustic model v2_0_0": ['Common Voice German v8_0', 'Multilingual LibriSpeech German', 'GlobalPhone German v3_1'],
    "German MFA acoustic model v2_0_0a": ['Common Voice German v8_0', 'Multilingual LibriSpeech German', 'GlobalPhone German v3_1'],
    "Japanese MFA acoustic model v2_0_1a": ['Common Voice Japanese v12_0', 'GlobalPhone Japanese v3_1',
                                           'Microsoft Speech Language Translation Japanese',
                                            'Japanese Versatile Speech', 'TEDxJP-10K v1_1'],
    "Japanese MFA acoustic model v3_0_0": ['Common Voice Japanese v12_0', 'GlobalPhone Japanese v3_1',
                                           'Microsoft Speech Language Translation Japanese',
                                            'Japanese Versatile Speech', 'TEDxJP-10K v1_1'],
    "Hausa MFA acoustic model v2_0_0": ['Common Voice Hausa v8_0', 'GlobalPhone Hausa v3_1'],
    "Hausa MFA acoustic model v2_0_0a": ['Common Voice Hausa v9_0', 'GlobalPhone Hausa v3_1'],
    "Hausa MFA acoustic model v3_0_0": ['Common Voice Hausa v9_0', 'GlobalPhone Hausa v3_1'],
    "Mandarin MFA acoustic model v2_0_0": ['Common Voice Chinese (China) v8_0', 'Common Voice Chinese (Taiwan) v8_0',
                                           'AI-DataTang Corpus', 'AISHELL-3', 'THCHS-30'],
    "Mandarin MFA acoustic model v2_0_0a": ['Common Voice Chinese (China) v9_0', 'Common Voice Chinese (Taiwan) v9_0',
                                           'AI-DataTang Corpus', 'AISHELL-3', 'THCHS-30',
                                           'GlobalPhone Chinese-Mandarin v3_1'],
    "Korean MFA acoustic model v2_0_0": ['GlobalPhone Korean v3_1',
                                         'Deeply Korean read speech corpus public sample',
                                         'Pansori TEDxKR', 'Zeroth Korean', 'Seoul Corpus'],
    "Korean MFA acoustic model v2_0_0a": ['GlobalPhone Korean v3_1',
                                         'Deeply Korean read speech corpus public sample',
                                         'Pansori TEDxKR', 'Zeroth Korean', 'Seoul Corpus'],
    "Korean MFA acoustic model v3_0_0": ['GlobalPhone Korean v3_1',
                                         'Deeply Korean read speech corpus public sample',
                                         'Pansori TEDxKR', 'Zeroth Korean',
                                          "ASR-KCSC A Korean Conversational Speech Corpus",
                                        "ASR-SKDuSC A Scripted Korean Daily-use Speech Corpus",
                                        "Korean Single Speaker Speech Dataset",
                                        "Common Voice Korean v16_1",],
    "Polish MFA acoustic model v2_0_0": ['Common Voice Polish v8_0', 'Multilingual LibriSpeech Polish', 'M-AILABS Polish', 'GlobalPhone Polish v3_1'],
    "Polish MFA acoustic model v2_0_0a": ['Common Voice Polish v8_0', 'Multilingual LibriSpeech Polish', 'M-AILABS Polish', 'GlobalPhone Polish v3_1'],
    "Portuguese MFA acoustic model v2_0_0": ['Common Voice Portuguese v8_0', 'Multilingual LibriSpeech Portuguese',
                                             'GlobalPhone Portuguese (Brazilian) v3_1'],
    "Portuguese MFA acoustic model v2_0_0a": ['Common Voice Portuguese v8_0', 'Multilingual LibriSpeech Portuguese',
                                             'GlobalPhone Portuguese (Brazilian) v3_1'],
    "Russian MFA acoustic model v2_0_0": ['Common Voice Russian v8_0', 'Russian LibriSpeech', 'M-AILABS Russian', 'GlobalPhone Russian v3_1'],
    "Russian MFA acoustic model v2_0_0a": ['Common Voice Russian v9_0', 'Russian LibriSpeech', 'M-AILABS Russian', 'GlobalPhone Russian v3_1'],
    "Spanish MFA acoustic model v2_0_0": ['Common Voice Spanish v8_0', 'Multilingual LibriSpeech Spanish',
                                          "Google i18n Chile","Google i18n Columbia","Google i18n Peru","Google i18n Puerto Rico","Google i18n Venezuela",
                                          "M-AILABS Spanish", 'GlobalPhone Spanish (Latin American) v3_1'],
    "Spanish MFA acoustic model v2_0_0a": ['Common Voice Spanish v8_0', 'Multilingual LibriSpeech Spanish',
                                          "Google i18n Chile","Google i18n Columbia","Google i18n Peru","Google i18n Puerto Rico","Google i18n Venezuela",
                                          "M-AILABS Spanish", 'GlobalPhone Spanish (Latin American) v3_1'],
    "Swahili MFA acoustic model v2_0_0": ['Common Voice Swahili v8_0', 'ALFFA Swahili', 'GlobalPhone Swahili v3_1'],
    "Swahili MFA acoustic model v2_0_0a": ['Common Voice Swahili v9_0', 'ALFFA Swahili', 'GlobalPhone Swahili v3_1'],
    "Swedish MFA acoustic model v2_0_0": ['Common Voice Swedish v8_0', 'NST Swedish', 'GlobalPhone Swedish v3_1'],
    "Swedish MFA acoustic model v2_0_0a": ['Common Voice Swedish v8_0', 'NST Swedish', 'GlobalPhone Swedish v3_1'],
    "Thai MFA acoustic model v2_0_0": ['Common Voice Thai v8_0', 'GlobalPhone Thai v3_1'],
    "Thai MFA acoustic model v2_0_0a": ['Common Voice Thai v9_0', 'GlobalPhone Thai v3_1'],
    "Thai MFA acoustic model v3_0_0": ['Common Voice Thai v16_1', 'GlobalPhone Thai v3_1',
                                       "Lotus Corpus v1_0", "Gowajee Corpus v0_9_3",
                                       "Thai Elderly Speech dataset by Data Wow and VISAI v1_0_0",],
    "Bulgarian MFA acoustic model v2_0_0": ['Common Voice Bulgarian v8_0', 'GlobalPhone Bulgarian v3_1'],
    "Bulgarian MFA acoustic model v2_0_0a": ['Common Voice Bulgarian v9_0', 'GlobalPhone Bulgarian v3_1'],
    "Croatian MFA acoustic model v2_0_0": ['Common Voice Serbian v8_0', 'GlobalPhone Croatian v3_1'],
    "Croatian MFA acoustic model v2_0_0a": ['Common Voice Serbian v9_0', 'GlobalPhone Croatian v3_1'],
    "Czech MFA acoustic model v2_0_0": ['Common Voice Czech v8_0', 'GlobalPhone Czech v3_1',
                                        "Large Corpus of Czech Parliament Plenary Hearings", "Czech Parliament Meetings"],
    "Czech MFA acoustic model v2_0_0a": ['Common Voice Czech v9_0', 'GlobalPhone Czech v3_1',
                                        "Large Corpus of Czech Parliament Plenary Hearings", "Czech Parliament Meetings"],
    "Turkish MFA acoustic model v2_0_0": ['Common Voice Turkish v8_0', 'MediaSpeech Turkish v1_1', 'GlobalPhone Turkish v3_1'],
    "Turkish MFA acoustic model v2_0_0a": ['Common Voice Turkish v8_0', 'MediaSpeech Turkish v1_1', 'GlobalPhone Turkish v3_1'],
    "Ukrainian MFA acoustic model v2_0_0": ['Common Voice Ukrainian v8_0', 'M-AILABS Ukrainian', 'GlobalPhone Ukrainian v3_1'],
    "Ukrainian MFA acoustic model v2_0_0a": ['Common Voice Ukrainian v9_0', 'M-AILABS Ukrainian', 'GlobalPhone Ukrainian v3_1'],
    "Vietnamese MFA acoustic model v2_0_0": ['Common Voice Vietnamese v8_0', 'VIVOS', 'GlobalPhone Vietnamese v3_1'],
    "Vietnamese MFA acoustic model v2_0_0a": ['Common Voice Vietnamese v9_0', 'VIVOS', 'GlobalPhone Vietnamese v3_1'],
}

model_dictionary_mapping = {
    "English MFA acoustic model v2_0_0": ["English (US) MFA dictionary v2_0_0",
                                      "English (UK) MFA dictionary v2_0_0",
                                          "English (Nigeria) MFA dictionary v2_0_0"],
    "English MFA acoustic model v3_0_0": ["English (US) MFA dictionary v3_0_0",
                                      "English (UK) MFA dictionary v3_0_0",
                                          "English (Nigeria) MFA dictionary v3_0_0",
                                          "English (India) MFA dictionary v3_0_0"],
    "Vietnamese MFA acoustic model v2_0_0": ["Vietnamese (Hanoi) MFA dictionary v2_0_0",
                                         "Vietnamese (Ho Chi Minh City) MFA dictionary v2_0_0",
                                         "Vietnamese (Hue) MFA dictionary v2_0_0",
                                         "Vietnamese MFA dictionary v2_0_0"],
    "Spanish MFA acoustic model v2_0_0": ["Spanish (Latin America) MFA dictionary v2_0_0",
                                         "Spanish (Spain) MFA dictionary v2_0_0",
                                         "Spanish MFA dictionary v2_0_0"],
    "Portuguese MFA acoustic model v2_0_0": ["Portuguese (Brazil) MFA dictionary v2_0_0",
                                         "Portuguese (Portugal) MFA dictionary v2_0_0",
                                         "Portuguese MFA dictionary v2_0_0"],
    "Mandarin MFA acoustic model v2_0_0": ["Mandarin (China) MFA dictionary v2_0_0",
                                         "Mandarin (Erhua) MFA dictionary v2_0_0",
                                         "Mandarin (Taiwan) MFA dictionary v2_0_0"],
}

def make_path_safe(string):
    s = re.sub(r"[- .:()]+", '_', string.lower())
    if s.endswith('_'):
        s = s[:-1]
    return s


def get_model_card_directory(model_type, meta_data):
    model_directory = os.path.join(mfa_model_root, model_type)
    if model_type == 'language_model':
        language, version = meta_data['language'], meta_data['version']
        directory = os.path.join(model_directory, language.lower(), 'mfa', f"v{version}")
    elif model_type in {'ivector', 'tokenizer'}:
        language, version = meta_data['language'], meta_data['version']
        directory = os.path.join(model_directory, language.lower(), f"v{version}")
    elif model_type == 'corpus':
        language, name = meta_data['language'], meta_data['name']
        name = make_path_safe(name)
        if 'version' in meta_data:
            version = meta_data['version']
            directory = os.path.join(model_directory, language.lower(), name, f"{version}")
        else:
            directory = os.path.join(model_directory, language.lower(), name)
    else:
        language, phone_set, dialect, version = meta_data['language'], meta_data['phone_set'], meta_data['dialect'], meta_data['version']
        if dialect:
            phoneset_folder = f'{dialect}_{phone_set}'.replace(' ', '_').lower()
        else:
            phoneset_folder = phone_set.lower()
        directory = os.path.join(model_directory, language.lower(), phoneset_folder, f"v{version}")

    return directory


mfa_model_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OVERWRITE_METADATA = False
OVERWRITE_MD = False

mfa_citation_template = "@techreport{{{id},\n\tauthor={{{extra_authors}McAuliffe, Michael and Sonderegger, Morgan}}," \
                        "\n\ttitle={{{title}}}," \
                        "\n\taddress={{\\url{{https://mfa-models.readthedocs.io/{model_type}/{language}/{link_safe_title}.html}}}}," \
                        "\n\tyear={{{year}}},\n\tmonth={{{month}}}," \
                        "\n}}"
cv_citation = "@misc{Ahn_Chodroff_2022,\n\tauthor={Ahn, Emily and Chodroff, Eleanor}," \
                        "\n\ttitle={VoxCommunis Corpus}," \
                        "\n\taddress={\\url{https://osf.io/t957v}}," \
                        "\n\tpublisher={OSF}," \
                        "\n\tyear={2022}, \n\tmonth={Jan}\n}"
prosodylab_citation = "@article{gorman2011prosodylab,\n\tauthor={Gorman, Kyle and Howell, Jonathan and Wagner, Michael}," \
                        "\n\ttitle={Prosodylab-aligner: A tool for forced alignment of laboratory speech}," \
                        "\n\tjournal={Canadian Acoustics}," \
                        "\n\tvolume={39},\n\tnumber={3},\n\tpages={192--193},\n\tyear={2011}\n}"

language_link_template = "[{}]({})"

license_links = {
    'CC-0': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/',
    'CC BY-SA-NC 3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/',
    'CC BY-NC-SA 4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC BY-NC-SA 3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/',
    'CC BY-NC 4.0': 'https://creativecommons.org/licenses/by-nc/4.0/',
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC BY-NC-ND 4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY-NC 2.0': 'https://creativecommons.org/licenses/by-nc/2.0/',
    'CC BY-NC-ND 3.0': 'https://creativecommons.org/licenses/by-nc-nd/3.0/',
    'Microsoft Research Data License': 'https://msropendata-web-api.azurewebsites.net/licenses/2f933be3-284d-500b-7ea3-2aa2fd0f1bb2/view',
    'Apache 2.0': 'https://www.apache.org/licenses/LICENSE-2.0',
    'O-UDA v1.0': 'https://msropendata-web-api.azurewebsites.net/licenses/f1f352a6-243f-4905-8e00-389edbca9e83/view',
    'MIT': 'https://opensource.org/licenses/MIT',
    'Public domain in the USA': 'https://creativecommons.org/share-your-work/public-domain/cc0/',
    'M-AILABS License': 'https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/',
    'ELRA': 'https://www.elra.info/en/services-around-lrs/distribution/licensing/',
    'Buckeye License': 'https://buckeyecorpus.osu.edu/php/registration.php',
    'LDC License': 'https://www.ldc.upenn.edu/data-management/using/licensing',
    'LaboroTV Non-commercial': 'https://laboro.ai/activity/column/engineer/eg-laboro-tv-corpus-jp/',

}

mfa_maintainer = "[Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)"
cv_maintainer = "[Vox Communis](https://osf.io/t957v/)"

corpus_detail_template="""
   * {link}:
     * **Hours:** `{num_hours:.2f}`
     * **Speakers:** `{num_speakers:,}`
     * **Utterances:** `{num_utterances:,}`"""

g2p_training_detail_template="""
* **Words:** `{num_words:,}`
* **Phones:** `{num_phones:,}`
* **Graphemes:** `{num_graphemes:,}`"""

g2p_evaluation_detail_template="""
* **Words:** `{num_words:,}`
* **WER:** `{word_error_rate:.2f}%`
* **PER:** `{phone_error_rate:.2f}%`"""

tokenizer_training_detail_template="""
* **Utterances:** `{num_utterances:,}`
* **Graphemes:** `{num_graphemes:,}`"""

tokenizer_evaluation_detail_template="""
* **Utterances:** `{num_utterances:,}`
* **UER:** `{utterance_error_rate:.2f}%`
* **CER:** `{character_error_rate:.2f}%`"""

lm_training_detail_template="""
* **Words:** `{num_words:,}`
* **OOVs:** `{num_oovs:,}`"""

lm_evaluation_detail_template="""
* **Large model:** `{large_perplexity:.2f}`
* **Medium model:** `{medium_perplexity:.2f}`
* **Small model:** `{small_perplexity:.2f}`"""

link_template = '* {{ref}}`{}`'

see_also_template = """```{{admonition}} {model_type_name}
   {links}
   ```"""

mfa_acoustic_model_card_template = template_dir.joinpath('mfa_acoustic_model_card_template.md').read_text('utf8')
ivector_card_template = template_dir.joinpath('ivector_card_template.md').read_text('utf8')
other_acoustic_model_card_template = template_dir.joinpath('other_acoustic_model_card_template.md').read_text('utf8')
g2p_model_card_template = template_dir.joinpath('g2p_model_card_template.md').read_text('utf8')
language_model_card_template = template_dir.joinpath('language_model_card_template.md').read_text('utf8')
mfa_dictionary_card_template = template_dir.joinpath('mfa_dictionary_card_template.md').read_text('utf8')
other_dictionary_card_template = template_dir.joinpath('other_dictionary_card_template.md').read_text('utf8')
corpus_card_template = template_dir.joinpath('corpus_card_template.md').read_text('utf8')
tokenizer_model_card_template = template_dir.joinpath('tokenizer_model_card_template.md').read_text('utf8')


corpus_docs_md_template = template_dir.joinpath('corpus_docs_md_template.md').read_text('utf8')
acoustic_docs_md_template = template_dir.joinpath('acoustic_docs_md_template.md').read_text('utf8')
ivector_docs_md_template = template_dir.joinpath('ivector_docs_md_template.md').read_text('utf8')
g2p_docs_md_template = template_dir.joinpath('g2p_docs_md_template.md').read_text('utf8')
lm_docs_md_template = template_dir.joinpath('lm_docs_md_template.md').read_text('utf8')
tokenizer_docs_md_template = template_dir.joinpath('tokenizer_docs_md_template.md').read_text('utf8')
mfa_dictionary_docs_md_template = template_dir.joinpath('mfa_dictionary_docs_md_template.md').read_text('utf8')
other_dictionary_docs_md_template = template_dir.joinpath('other_dictionary_docs_md_template.md').read_text('utf8')

language_links = {
    'Abkhaz': ('Abkhaz', 'https://en.wikipedia.org/wiki/Abkhaz_language'),
    'Arabic': ('Arabic', 'https://en.wikipedia.org/wiki/Arabic'),
    'Armenian': ('Armenian', 'https://en.wikipedia.org/wiki/Armenian_language'),
    'Bashkir': ('Bashkir', 'https://en.wikipedia.org/wiki/Bashkir_language'),
    'Basque': ('Basque', 'https://en.wikipedia.org/wiki/Basque_language'),
    'Belarusian': ('Belarusian', 'https://en.wikipedia.org/wiki/Belarusian_language'),
    'Bulgarian': ('Bulgarian', 'https://en.wikipedia.org/wiki/Bulgarian_language'),
    'Chuvash': ('Chuvash', 'https://en.wikipedia.org/wiki/Chuvash_language'),
    'Croatian': ('Serbo-Croatian', 'https://en.wikipedia.org/wiki/Serbo-Croatian'),
    'Czech': ('Czech', 'https://en.wikipedia.org/wiki/Czech_language'),
    'Dutch': ('Dutch', 'https://en.wikipedia.org/wiki/Dutch_language'),
    'English': ('English', 'https://en.wikipedia.org/wiki/English_language'),
    ('English', 'US'): ('General American English', 'https://en.wikipedia.org/wiki/General_American_English'),
    ('English', 'UK'): ('British English', 'https://en.wikipedia.org/wiki/British_English'),
    ('English', 'Nigeria'): ('Nigerian English', 'https://en.wikipedia.org/wiki/Nigerian_English'),
    ('English', 'India'): ('Indian English', 'Japanese tokenizer v2_1_0.md'),
    'French': ('French', 'https://en.wikipedia.org/wiki/French_language'),
    'Georgian': ('Georgian', 'https://en.wikipedia.org/wiki/Georgian_language'),
    'German': ('German', 'https://en.wikipedia.org/wiki/German_language'),
    'Greek': ('Greek', 'https://en.wikipedia.org/wiki/Greek_language'),
    'Guarani': ('Guarani', 'https://en.wikipedia.org/wiki/Guarani_language'),
    'Hungarian': ('Hungarian', 'https://en.wikipedia.org/wiki/Hungarian_language'),
    'Italian': ('Italian', 'https://en.wikipedia.org/wiki/Italian_language'),
    'Indonesian': ('Indonesian', 'https://en.wikipedia.org/wiki/Indonesian_language'),
    'Hausa': ('Hausa', 'https://en.wikipedia.org/wiki/Hausa_language'),
    'Kazakh': ('Kazakh', 'https://en.wikipedia.org/wiki/Kazakh_language'),
    'Kyrgyz': ('Kyrgyz', 'https://en.wikipedia.org/wiki/Kyrgyz_language'),
    'Kurmanji': ('Kurmanji', 'https://en.wikipedia.org/wiki/Kurmanji'),
    'Maltese': ('Maltese', 'https://en.wikipedia.org/wiki/Maltese_language'),
    'Uzbek': ('Uzbek', 'https://en.wikipedia.org/wiki/Uzbek_language'),
    'Uyghur': ('Uyghur', 'https://en.wikipedia.org/wiki/Uyghur_language'),
    'Punjabi': ('Punjabi', 'https://en.wikipedia.org/wiki/Punjabi_language'),
    'Hindi': ('Hindi', 'https://en.wikipedia.org/wiki/Hindi_language'),
    'Hindi-Urdu': ('Hindi-Urdu', 'https://en.wikipedia.org/wiki/Hindustani_language'),
    'Japanese': ('Japanese', 'https://en.wikipedia.org/wiki/Japanese_language'),
    'Korean': ('Korean', 'https://en.wikipedia.org/wiki/Korean_language'),
    'Polish': ('Polish', 'https://en.wikipedia.org/wiki/Polish_language'),
    'Portuguese': ('Portuguese', 'https://en.wikipedia.org/wiki/Portuguese_language'),
    ('Portuguese', 'Brazil'): ('Brazilian Portuguese', 'https://en.wikipedia.org/wiki/Brazilian_Portuguese'),
    ('Portuguese', 'Portugal'): ('European Portuguese', 'https://en.wikipedia.org/wiki/European_Portuguese'),
    'Romanian': ('Romanian', 'https://en.wikipedia.org/wiki/Romanian_language'),
    'Russian': ('Russian', 'https://en.wikipedia.org/wiki/Russian_language'),
    'Spanish': ('Spanish', 'https://en.wikipedia.org/wiki/Spanish_language'),
    ('Spanish', 'Latin America'): ('Spanish in the Americas', 'https://en.wikipedia.org/wiki/Spanish_language_in_the_Americas'),
    ('Spanish', 'Spain'): ('Peninsular Spanish', 'https://en.wikipedia.org/wiki/Peninsular_Spanish'),
    'Swahili': ('Swahili', 'https://en.wikipedia.org/wiki/Swahili_language'),
    'Swedish': ('Swedish', 'https://en.wikipedia.org/wiki/Swedish_language'),
    'Tamil': ('Tamil', 'https://en.wikipedia.org/wiki/Tamil_language'),
    'Tatar': ('Tatar', 'https://en.wikipedia.org/wiki/Tatar_language'),
    'Thai': ('Thai', 'https://en.wikipedia.org/wiki/Thai_language'),
    'Turkish': ('Turkish', 'https://en.wikipedia.org/wiki/Turkish_language'),
    'Ukrainian': ('Ukrainian', 'https://en.wikipedia.org/wiki/Ukrainian_language'),
    'Vietnamese': ('Vietnamese', 'https://en.wikipedia.org/wiki/Vietnamese_language'),
    ('Vietnamese', 'Ho Chi Minh City'): ('Southern Vietnamese', 'https://en.wikipedia.org/wiki/Vietnamese_language#Language_variation'),
    ('Vietnamese', 'Hanoi'): ('Northern Vietnamese', 'https://en.wikipedia.org/wiki/Vietnamese_language#Language_variation'),
     'Sorbian': ('Sorbian', 'https://en.wikipedia.org/wiki/Sorbian_languages'),
     ('Sorbian','Upper'): ('Upper Sorbian', 'https://en.wikipedia.org/wiki/Upper_Sorbian_language'),
    'Mandarin': ('Mandarin Chinese', 'https://en.wikipedia.org/wiki/Mandarin_Chinese'),
    ('Mandarin', 'Taiwan'): ('Taiwanese Mandarin', 'https://en.wikipedia.org/wiki/Taiwanese_Mandarin'),
    ('Mandarin', 'Erhua'): ('Beijing Mandarin', 'https://en.wikipedia.org/wiki/Beijing_dialect'),
    ('Mandarin', 'China'): ('Standard Mandarin Chinese', 'https://en.wikipedia.org/wiki/Standard_Chinese'),
    'Urdu': ('Urdu', 'https://en.wikipedia.org/wiki/Urdu'),
}

cv_phone_set_mapping = {
    'abkhaz': 'XPF',
    'armenian': 'XPF',
    'bashkir': 'XPF',
    'basque': 'XPF',
    'belarusian': 'XPF',
    'bulgarian': 'XPF',
    'chuvash': 'XPF',
    'czech': 'XPF',
    'dutch': 'Epitran',
    'georgian': 'XPF',
    'greek': 'XPF',
    'guarani': 'XPF',
    'hausa': 'Epitran',
    'hindi': 'Epitran',
    'hungarian': 'XPF',
    'indonesian': 'Epitran',
    'italian': 'Epitran',
    'kazakh': 'Epitran',
    'kurmanji': 'Epitran',
    'kyrgyz': 'Epitran',
    'maltese': 'Epitran',
    'polish': 'Epitran',
    'punjabi': 'Epitran',
    'portuguese': 'Epitran',
    'romanian': 'XPF',
    'russian': 'Epitran',
    'sorbian_upper': 'XPF',
    'sorbian': 'XPF',
    'swedish': 'XPF',
    'tamil': 'XPF',
    'tatar': 'Epitran',
    'thai': 'XPF',
    'turkish': 'XPF',
    'ukrainian': 'XPF',
    'uyghur': 'Epitran',
    'uzbek': 'Epitran',
    'urdu': 'Epitran',
    'vietnamese': 'XPF',
}

phone_set_templates = {
    'Epitran': '[Epitran](https://github.com/dmort27/epitran)',
    'XPF': '[XPF](https://github.com/CohenPr-XPF/XPF)',
    'ARPA': '[ARPA](https://en.wikipedia.org/wiki/ARPABET)',
    'PINYIN': '[PINYIN](https://en.wikipedia.org/wiki/Pinyin)',
    'PROSODYLAB': '[PROSODYLAB](https://github.com/prosodylab/prosodylab.dictionaries)',
    'MFA': '[MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#{language})'
}

model_id_templates = {
    'acoustic': '{language}{dialect_title_string} {phone_set} acoustic model{version_string}',
    'dictionary': '{language}{dialect_title_string} {phone_set} dictionary{version_string}',
    'g2p': '{language}{dialect_title_string} {phone_set} G2P model{version_string}',
    'language_model': '{language}{dialect_title_string} language model{version_string}',
    'corpus': '{corpus_name}{version_string}',
    'ivector': '{language} {phone_set} ivector extractor{version_string}',
    'tokenizer': '{language} tokenizer{version_string}',
}

pronunciation_dictionaries = {}

def load_dict(dictionary_path, dict_name, phone_set_type) -> MultispeakerDictionary:
    if dict_name not in pronunciation_dictionaries:
        pronunciation_dictionaries[dict_name] = MultispeakerDictionary(dictionary_path,
                                                                        phone_set_type=phone_set_type,
                                                                        position_dependent_phones=False)
        if os.path.exists(pronunciation_dictionaries[dict_name].output_directory):
            shutil.rmtree(pronunciation_dictionaries[dict_name].output_directory)
        pronunciation_dictionaries[dict_name].dictionary_setup()
    return pronunciation_dictionaries[dict_name]

def generate_id(meta_data, model_type):
    if "dialect" in meta_data and meta_data["dialect"]:
        dialect_title_string = f' ({meta_data["dialect"]})'
    else:
        dialect_title_string = ''
    if "version" in meta_data and meta_data["version"]:
        version_string = f' v{meta_data["version"]}'
    else:
        version_string = ''
    template = model_id_templates[model_type]
    if model_type == 'corpus':
        fields = {'corpus_name': meta_data['name'], 'version_string':version_string}
    else:
        fields = {'language':meta_data['language'].title(), 'dialect_title_string':dialect_title_string,
                           'version_string':version_string}
        if model_type not in {'language_model'}:
            fields['phone_set'] = meta_data['phone_set']
        if model_type == 'ivector':
            fields['phone_set'] = 'MFA'
    return template.format(**fields).replace('.', '_')

def generate_meta_data(model, model_type, language, dialect, version, phone_set):
    citation_details = {'model_name': model.name,
                        'version': version,
                        'extra_authors': '',
                        'model_type': model_type,
                        'language': language.title(),
                        'phone_set': phone_set.upper(),
                        }
    citation_template = mfa_citation_template
    if language in {'Arabic'}:
        citation_details['extra_authors'] = 'Shmueli, Natalia and '
    maintainer = mfa_maintainer
    if dialect:
        phone_set_folder = f'{dialect}_{phone_set}'.replace(' ', '_').lower()
        citation_details['dialect'] = dialect
    else:
        phone_set_folder = phone_set.lower()
    license = 'CC BY 4.0'
    license_link = f'[CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/{model_type}/{language.lower()}/{phone_set_folder}/v{version}/LICENSE)'
    if model_type == 'acoustic':
        if model.source.name.endswith('_cv.zip'):
            citation = cv_citation
            maintainer = cv_maintainer
            license = 'CC-0'
            license_link = "[CC-0](https://creativecommons.org/publicdomain/zero/1.0/)"
            train_date = '02-11-2022'
        else:
            train_date = datetime.fromisoformat(model.meta['train_date']).date()
            citation_details['year'] = train_date.year
            citation_details['month'] = train_date.strftime('%b')
            citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
            citation_details['link_safe_title'] = generate_id(citation_details, model_type)
            citation_details['id'] = f'mfa_{model.name}_acoustic_{citation_details["year"]}'
            citation = mfa_citation_template.format(**citation_details)
        features = 'MFCC'
        if model.meta['features'].get('use_pitch', False):
            features += ' + pitch'
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'phone_set': phone_set,
            'version': version,
            'maintainer': maintainer,
            'citation': citation,
            'license': license,
            'license_link': license_link,
            'architecture': model.meta['architecture'],
            'features': features,
            'evaluation': {},
            'decode': {},
            'train_date': str(train_date),
        }
    if model_type == 'dictionary':
        train_date = datetime.today().date()
        citation_details['model_type'] = 'pronunciation dictionary'
        citation_details['year'] = train_date.year
        citation_details['month'] = train_date.strftime('%b')
        citation_details['link_safe_title'] = generate_id(citation_details, model_type)
        citation_details['id'] = f'mfa_{model.name}_dictionary_{train_date.year}'
        citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
        citation = citation_template.format(**citation_details)
        phone_set = phone_set.upper()
        if model.path.name.endswith('_cv.dict'):
            citation = cv_citation
            maintainer = cv_maintainer
            license_link = "[CC-0](https://creativecommons.org/publicdomain/zero/1.0/)"
            dictionary_phone_set = 'IPA'
        elif model.path.name.endswith('_mfa.dict'):
            dictionary_phone_set = 'IPA'
        else:
            if model.path.name.endswith('_prosodylab.dict') or model.path.name.endswith('us_arpa.dict'):
                citation = prosodylab_citation
            try:
                dictionary_phone_set = montreal_forced_aligner.data.PhoneSetType[phone_set].name
            except KeyError:
                dictionary_phone_set = 'UNKNOWN'
        dictionary = load_dict(model.path, model.name, phone_set_type=dictionary_phone_set)
        word_count = len(dictionary.actual_words)
        data = {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'maintainer': maintainer,
            'license_link': license_link,
            'license': license,
            'phone_set': phone_set,
            'phones': sorted(dictionary.non_silence_phones),
            'word_count': word_count,
            'train_date': str(train_date),
            'version': version,
            'citation': citation,
        }
        output_path = os.path.join(os.path.dirname(get_model_card_directory('dictionary', data)), dictionary.name + '.dict')
        dictionary.export_lexicon(1, output_path)
        return data
    if model_type == 'g2p':
        train_date = datetime.fromisoformat(model.meta['train_date']).date()
        citation_details['model_type'] = 'G2P model'
        citation_details['year'] = train_date.year
        citation_details['month'] = train_date.strftime('%b')
        citation_details['link_safe_title'] = generate_id(citation_details, model_type)
        citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
        citation_details['id'] = f'mfa_{model.name}_g2p_{train_date.year}'
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'maintainer': maintainer,
            'license_link': license_link,
            'license': license,
            'architecture': model.meta['architecture'],
            'training': model.meta['training'],
            'evaluation': {k: v if v is not None else 100 for k,v in model.meta['evaluation'].items()},
            'phone_set': phone_set,
            'phones': sorted(model.meta['phones']),
            'version': version,
            'train_date': str(train_date),
            'citation': citation_template.format(**citation_details),
        }
    if model_type == 'language_model':
        train_date = datetime.fromisoformat(model.meta['train_date']).date()
        citation_details['model_type'] = 'language model'
        citation_details['year'] = train_date.year
        citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
        citation_details['link_safe_title'] = generate_id(citation_details, model_type)
        citation_details['month'] = train_date.strftime('%b')
        citation_details['id'] = f'mfa_{model.name}_lm_{train_date.year}'
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'phone_set': 'MFA',
            'maintainer': maintainer,
            'license_link': license_link,
            'license': license,
            'architecture': model.meta['architecture'],
            'version': version,
            'train_date': str(train_date),
            'training': {
                'num_words': model.meta['training']['num_words'],
                'num_oovs': model.meta['training']['num_oovs'],
            },
            'evaluation': {
                'large_perplexity': model.meta['evaluation_training']['large_perplexity'],
                'medium_perplexity': model.meta['evaluation_training']['medium_perplexity'],
                'small_perplexity': model.meta['evaluation_training']['small_perplexity'],
            },
            'citation': citation_template.format(**citation_details),
        }
    if model_type == 'tokenizer':
        train_date = datetime.fromisoformat(model.meta['train_date']).date()
        citation_details['model_type'] = 'tokenizer'
        citation_details['year'] = train_date.year
        citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
        citation_details['link_safe_title'] = generate_id(citation_details, model_type)
        citation_details['month'] = train_date.strftime('%b')
        citation_details['id'] = f'mfa_{model.name}_tokenizer_{train_date.year}'
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'phone_set': 'MFA',
            'maintainer': maintainer,
            'license_link': license_link,
            'license': license,
            'architecture': model.meta['architecture'],
            'version': version,
            'train_date': str(train_date),
            'training': {
                'num_utterances': model.meta['training']['num_utterances'],
                'num_graphemes': model.meta['training']['num_graphemes'],
            },
            'evaluation': {k: v if v is not None else 100 for k,v in model.meta['evaluation'].items()},
            'citation': citation_template.format(**citation_details),
        }
    if model_type == 'ivector':
        print(model.meta)
        if 'train_date' in model.meta:
            train_date = datetime.fromisoformat(model.meta['train_date']).date()
        else:
            train_date = datetime.now().date()
        citation_details['model_type'] = 'ivector'
        citation_details['year'] = train_date.year
        citation_details['title'] = generate_id(citation_details, model_type).replace('_', '.')
        citation_details['link_safe_title'] = generate_id(citation_details, model_type)
        citation_details['month'] = train_date.strftime('%b')
        citation_details['id'] = f'mfa_{model.name}_ivector_{train_date.year}'
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'phone_set': 'MFA',
            'maintainer': maintainer,
            'license_link': license_link,
            'license': license,
            'version': version,
            'train_date': str(train_date),
            'citation': citation_template.format(**citation_details),
        }
    return {}

def extract_model_card_fields(meta_data, model_type):
    dialect_link = 'N/A'
    if "dialect" in meta_data and meta_data["dialect"]:
        key = (meta_data['language'], meta_data["dialect"])
        if key in language_links:
            dialect_link = language_link_template.format(*language_links[key])
    if meta_data['language'] != 'Multilingual':
        language_link = language_link_template.format(*language_links[meta_data['language']])
    else:
        language_link = meta_data['language']
    if "dialects" in meta_data and meta_data["dialects"]:
        dialect_links = []
        for d in meta_data["dialects"]:
            key = (meta_data['language'], d)
            if key in language_links:
                dialect_links.append(language_link_template.format(*language_links[key]))
        dialect_link = ', '.join(dialect_links)
    if 'phone_set' in meta_data:
        phone_set = meta_data['phone_set']
        if phone_set == 'CV':
            phone_set = cv_phone_set_mapping[language.lower()]
        phone_set_link = phone_set_templates[phone_set]
        if phone_set == 'MFA':
            phone_set_link = phone_set_link.format(language=meta_data['language'].lower())
    name = generate_id(meta_data, model_type)
    discussion_title = name.replace(' ', '+').replace(')', '').replace('(', '').replace('_', '.')
    if model_type == 'acoustic':
        corpora_details = ''
        if 'corpus' in meta_data:
            for corpus in meta_data['corpus']:
                if 'version' in corpus and corpus['version']:
                    corpus_link_template = '[{name}](../../../../corpus/{language}/{corpus_safe_name}/{version}/README.md)'
                    link = corpus_link_template.format(name=corpus['name'],
                                                        language= make_path_safe(corpus['language']),
                                                        corpus_safe_name = make_path_safe(corpus['name']),
                                                        version=corpus['version'])
                else:
                    corpus_link_template = '[{name}](../../../../corpus/{language}/{corpus_safe_name}/README.md)'
                    link = corpus_link_template.format(name=corpus['name'],
                                                        language= make_path_safe(corpus['language']),
                                                        corpus_safe_name = make_path_safe(corpus['name']))

                data = {
                    'name': corpus['name'],
                    'link': link,
                    'num_hours': corpus['num_hours'],
                    'num_speakers': corpus['num_speakers'],
                    'num_utterances': corpus['num_utterances'],
                }
                corpora_details += '\n' + corpus_detail_template.format(**data)
        return {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'discussion_title': discussion_title,
                'language': meta_data['language'],
                'language_link': language_link,
                'dialect': meta_data['dialect'],
                'dialect_link': dialect_link,
                'version': meta_data['version'],
                'maintainer': meta_data['maintainer'],
                'features': meta_data['features'],
                'architecture': meta_data['architecture'],
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'license_link': meta_data['license_link'],
                'corpora_details': corpora_details,
                'phone_set_link': phone_set_link,
            }
    if model_type == 'ivector':
        corpora_details = ''
        if 'corpus' in meta_data:
            for corpus in meta_data['corpus']:
                if 'version' in corpus and corpus['version']:
                    corpus_link_template = '[{name}](../../../corpus/{language}/{corpus_safe_name}/{version}/README.md)'
                    link = corpus_link_template.format(name=corpus['name'],
                                                        language= make_path_safe(corpus['language']),
                                                        corpus_safe_name = make_path_safe(corpus['name']),
                                                        version=corpus['version'])
                else:
                    corpus_link_template = '[{name}](../../../corpus/{language}/{corpus_safe_name}/README.md)'
                    link = corpus_link_template.format(name=corpus['name'],
                                                        language= make_path_safe(corpus['language']),
                                                        corpus_safe_name = make_path_safe(corpus['name']))

                data = {
                    'name': corpus['name'],
                    'link': link,
                    'num_hours': corpus['num_hours'],
                    'num_speakers': corpus['num_speakers'],
                    'num_utterances': corpus['num_utterances'],
                }
                corpora_details += '\n' + corpus_detail_template.format(**data)
        return {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'discussion_title': discussion_title,
                'language': meta_data['language'],
                'language_link': language_link,
                'version': meta_data['version'],
                'maintainer': meta_data['maintainer'],
                'features': meta_data.get('features','MFCC'),
                'architecture': meta_data.get('architecture', 'ivector'),
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'license_link': meta_data['license_link'],
                'corpora_details': corpora_details,
            }
    if model_type == 'corpus':
        citation = meta_data.get('citation', '')
        version = meta_data.get('version', '')
        dialects = meta_data.get('dialects', [])
        if dialects:
            dialects = ', '.join(dialects)
        else:
            dialects ='N/A'
        if version:
            version = f'- **Version:** `{version}`'
        return {
            'corpus_name': meta_data['name'],
            'title': meta_data['id'].replace('_', '.'),
            'corpus_id': meta_data['id'],
            'language': meta_data['language'],
                'language_link': language_link,
                'discussion_title': discussion_title,
            'corpus_link': f"[{meta_data['name']}]({meta_data['link']})",
                'dialects': dialects,
                'dialect_link': dialect_link,
            'num_hours': meta_data['num_hours'],
            'num_utterances': meta_data['num_utterances'],
            'num_speakers': meta_data['num_speakers'],
            'num_female': meta_data.get('num_female', 0),
            'num_male': meta_data.get('num_male', 0),
            'num_other': meta_data.get('num_other', meta_data['num_speakers']),
            'license_link': meta_data['license_link'],
            'version': version,
            'citation': citation,
        }
    if model_type == 'dictionary':
        data = {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'language': meta_data['language'],
                'language_link': language_link,
                'dialect': meta_data['dialect'],
                'dialect_link': dialect_link,
                'discussion_title': discussion_title,
                'version': meta_data['version'],
                'maintainer': meta_data['maintainer'],
                'license_link': meta_data['license_link'],
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'phone_set': meta_data['phone_set'],
                'phones': ' '.join(sorted(meta_data['phones'])),
                'word_count': meta_data['word_count'],
                'phone_set_link': phone_set_link,
            }
        if meta_data['phone_set'] in {'MFA', 'ARPA'}:
            data['plain_link'] = f'https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/{language.lower()}/mfa/{model_name}.dict'
        return data
    if model_type == 'g2p':
        training_details = g2p_training_detail_template.format(**meta_data['training'])
        evaluation_details = g2p_evaluation_detail_template.format(**meta_data['evaluation'])
        return {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'language': meta_data['language'],
                'language_link': language_link,
                'dialect': meta_data['dialect'],
                'dialect_link': dialect_link,
                'discussion_title': discussion_title,
                'architecture': meta_data['architecture'],
                'maintainer': meta_data['maintainer'],
                'version': meta_data['version'],
                'license_link': meta_data['license_link'],
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'phone_set': meta_data['phone_set'],
                'phones': ', '.join(f"{{ipa_inline}}`{x}`" for x in meta_data['phones']),
                'training_details': training_details,
                'evaluation_details': evaluation_details,
                'phone_set_link': phone_set_link,
            }
    if model_type == 'tokenizer':
        training_details = tokenizer_training_detail_template.format(**meta_data['training'])
        evaluation_details = tokenizer_evaluation_detail_template.format(**meta_data['evaluation'])
        return {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'language': meta_data['language'],
                'language_link': language_link,
                'discussion_title': discussion_title,
                'architecture': meta_data['architecture'],
                'maintainer': meta_data['maintainer'],
                'version': meta_data['version'],
                'license_link': meta_data['license_link'],
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'training_details': training_details,
                'evaluation_details': evaluation_details,
            }
    if model_type == 'language_model':
        training_details = lm_training_detail_template.format(**meta_data['training'])
        evaluation_details = lm_evaluation_detail_template.format(**meta_data['evaluation'])
        return {
                'model_name': meta_data['name'],
            'title': name.replace('_', '.'),
                'language': meta_data['language'],
                'language_link': language_link,
                'dialect': meta_data['dialect'],
                'dialect_link': dialect_link,
                'discussion_title': discussion_title,
                'architecture': meta_data['architecture'],
                'maintainer': meta_data['maintainer'],
                'version': meta_data['version'],
                'license_link': meta_data['license_link'],
                'mfa_version': CURRENT_MODEL_VERSION,
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'training_details': training_details,
                'evaluation_details': evaluation_details,
            }


def extract_doc_card_fields(meta_data, model_type):
    tags = [meta_data['language']]
    if model_type not in  {'language_model', 'corpus'}:
        tags.append(meta_data['phone_set'].upper())

    see_also = ''
    links = []
    for k in ['corpus', 'dictionary', 'g2p', 'acoustic', 'language_model', 'tokenizer']:
        if k == 'corpus' and model_type in {'acoustic', 'ivector'}:
            continue
        if k in meta_data:
            if k == 'corpus':
                links.append( see_also_template.format(links='\n'.join(link_template.format(x['id'].lower().replace(' ', '_')) for x in meta_data[k]),
                                                   model_type_name=model_type_names[k]))
            else:
                print(meta_data[k])
                links.append( see_also_template.format(links='\n'.join(link_template.format(x.lower().replace(' ', '_')) for x in meta_data[k]),
                                                   model_type_name=model_type_names[k]))

    if links:
        see_also = '\n\n'.join(links)
    try:
        license_link = f"[{meta_data['license']}]({license_links[meta_data['license']]})"
    except KeyError:
        license_link = meta_data['license']
    layout_type = 'not_mfa'
    if 'phone_set' in meta_data:
        phone_set = meta_data['phone_set']
        if phone_set == 'CV':
            phone_set = cv_phone_set_mapping[meta_data['language'].lower()]
        elif phone_set in {'MFA', 'ARPA', 'PROSODYLAB'}:
            layout_type = 'mfa'
        try:
            phone_set_link = phone_set_templates[phone_set]
            if phone_set == 'MFA':
                phone_set_link = phone_set_link.format(language=meta_data['language'].lower())
        except KeyError:
            phone_set_link = phone_set
        if "dialect" in meta_data and meta_data["dialect"]:
            language_sub_folder = f"{meta_data['dialect']}_{meta_data['phone_set']}".replace(' ', '_').lower()
            dialect_title_string = f" ({meta_data['dialect']})"
        else:
            language_sub_folder = meta_data['phone_set'].lower()
            dialect_title_string = ''
    name = generate_id(meta_data, model_type)
    if model_type == 'acoustic':
        corpora_details = ''
        corpus_link_template = '{{ref}}`{corpus_id}`'
        dialects = []
        if 'corpus' in meta_data:
            for corpus in meta_data['corpus']:
                if 'dialects' in corpus:
                    dialects.extend(corpus['dialects'])
                data = {
                    'name': corpus['name'],
                    'link': corpus_link_template.format(corpus_id=corpus["id"].replace(' ','_')),
                    'num_hours': corpus['num_hours'],
                    'num_speakers': corpus['num_speakers'],
                    'num_utterances': corpus['num_utterances'],
                }
                corpora_details += '\n' + corpus_detail_template.format(**data)
        if not dialects and 'dialect' in meta_data and meta_data['dialect']:
            dialects = [meta_data['dialect']]
        if meta_data['phone_set'] in {'CV', 'MFA'}:
            tags.append('IPA')
        return {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'architecture': meta_data['architecture'],
            'version': meta_data['version'],
            'corpora_details': corpora_details,
            'see_also': see_also,
            'tags': ';'.join(tags),
            'dialects': ';'.join(sorted(set(dialects))) if dialects else 'N/A',
            'language': meta_data['language'].lower(),
            'language_name': meta_data['language'].title(),
                'license': meta_data['license'],
            'phone_set': phone_set,
            'layout_type': layout_type,
            'license_link': license_link,
            'phone_set_link': phone_set_link,
            'dialect_title_string': dialect_title_string,
            'language_sub_folder': language_sub_folder,
            'phone_set_name': meta_data['phone_set'].upper(),
        }
    if model_type == 'ivector':
        corpora_details = ''
        corpus_link_template = '{{ref}}`{corpus_id}`'
        if 'corpus' in meta_data:
            for corpus in meta_data['corpus']:
                data = {
                    'name': corpus['name'],
                    'link': corpus_link_template.format(corpus_id=corpus["id"].replace(' ','_')),
                    'num_hours': corpus['num_hours'],
                    'num_speakers': corpus['num_speakers'],
                    'num_utterances': corpus['num_utterances'],
                }
                corpora_details += '\n' + corpus_detail_template.format(**data)
        return {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'architecture': meta_data.get('architecture', 'ivector'),
            'version': meta_data['version'],
            'corpora_details': corpora_details,
            'see_also': see_also,
            'tags': ';'.join(tags),
            'language': meta_data['language'].lower(),
            'language_name': meta_data['language'].title(),
                'license': meta_data['license'],
            'layout_type': layout_type,
            'license_link': license_link,
        }
    if model_type == 'corpus':
        if 'tags' in meta_data:
            tags.extend(meta_data['tags'])
        dialects = []
        if 'dialects' in meta_data:
            dialects = meta_data['dialects']
        version_subdirectory = meta_data.get('version', '')
        if version_subdirectory:
            version_subdirectory = f'/{version_subdirectory}'
        return {
            'corpus_id': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'corpus_name': meta_data['name'],
            'corpus_name_safe': make_path_safe(meta_data['name']),
                'license': meta_data['license'],
            'see_also': see_also,
            'layout_type': layout_type,
            'tags': ';'.join(tags),
            'version_subdirectory': version_subdirectory,
            'language': meta_data['language'].lower(),
            'dialects': ';'.join(sorted(set(dialects))) if dialects else 'N/A',
            'language_name': meta_data['language'].title(),
        }
    if model_type == 'dictionary':
        if meta_data['name'].endswith('_cv') or meta_data['name'].endswith('_mfa'):
            tags.append('IPA')
        elif meta_data['name'].endswith('_prosodylab') or meta_data['name'].endswith('us_arpa'):
            tags.append('PROSODYLAB')
            tags.append('MFA')
        data = {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'version': meta_data['version'],
            'see_also': see_also,
            'tags': ';'.join(tags),
            'layout_type': layout_type,
            'language': meta_data['language'].lower(),
                'license': meta_data['license'],
            'language_name': meta_data['language'].title(),
            'dialects': meta_data['dialect'] if meta_data['dialect'] else 'N/A',
            'phone_set': phone_set,
            'language_sub_folder': language_sub_folder,
            'dialect_title_string': dialect_title_string,
            'phone_set_name': meta_data['phone_set'].upper(),
        }
        if meta_data['name'] in phone_charts:
            charts = phone_charts[meta_data['name']]
            data['consonant_chart'] = charts['consonant_chart']
            data['vowel_section'] = charts['oral_vowel_chart']
            if charts['nasal_vowel_chart']:
                data['vowel_section'] = "#### Oral Vowels\n\n" + data['vowel_section']
                data['vowel_section'] += "\n\n#### Nasal Vowels\n\n" + charts['nasal_vowel_chart']
            if charts['diphthongs']:
                data['vowel_section'] += '\n\n#### Diphthongs\n\n* ' + '\n* '.join(f'{{ipa_inline}}`{x}`' for x in sorted(charts['diphthongs']))
            if charts['triphthongs']:
                data['vowel_section'] += '\n\n#### Triphthongs\n\n* ' + '\n* '.join(f'{{ipa_inline}}`{x}`' for x in sorted(charts['triphthongs']))
            if 'tones' in charts and charts['tones']:
                data['vowel_section'] += '\n\n#### Tones\n\n* ' + '\n* '.join(f'{{ipa_inline}}`{x}`' for x in sorted(charts['tones']))
            if 'stress' in charts and charts['stress']:
                data['vowel_section'] += '\n\n#### Stress\n\n* ' + '\n* '.join(f'{{ipa_inline}}`{x}`' for x in sorted(charts['stress']))
            if 'other' in charts and charts['other']:
                data['vowel_section'] += '\n\n### Other phones\n\n* ' + '\n* '.join(f'{{ipa_inline}}`{x}`' for x in sorted(charts['other']))

        return data
    if model_type == 'g2p':
        if meta_data['phone_set'] in {'CV', 'MFA'}:
            tags.append('IPA')
        return {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'architecture': meta_data['architecture'],
            'version': meta_data['version'],
            'see_also': see_also,
            'layout_type': layout_type,
            'language_sub_folder': language_sub_folder,
            'dialect_title_string': dialect_title_string,
            'tags': ';'.join(tags),
                'license': meta_data['license'],
            'language': meta_data['language'].lower(),
            'dialects': meta_data['dialect'] if meta_data['dialect'] else 'N/A',
            'language_name': meta_data['language'].title(),
            'phone_set': phone_set,
            'phone_set_name': meta_data['phone_set'].upper(),
        }
    if model_type == 'language_model':
        tags = ['MFA']
        return {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'layout_type': layout_type,
            'language': meta_data['language'].lower(),
            'dialects': meta_data['dialect'] if meta_data['dialect'] else 'N/A',
            'architecture': meta_data['architecture'],
            'language_name': meta_data['language'].title(),
            'dialect_title_string': dialect_title_string,
                'license': meta_data['license'],
            'version': meta_data['version'],
            'source': 'mfa',
            'see_also': see_also,
            'tags': ';'.join(tags),
        }
    if model_type == 'tokenizer':
        tags = ['MFA']
        return {
            'model_name': name,
            'ref': name.replace(' ','_'),
            'title': name.replace('_', '.'),
            'model_type': model_type,
            'layout_type': layout_type,
            'language': meta_data['language'].lower(),
            'architecture': meta_data['architecture'],
            'language_name': meta_data['language'].title(),
                'license': meta_data['license'],
            'version': meta_data['version'],
            'source': 'mfa',
            'see_also': see_also,
            'tags': ';'.join(tags),
        }

model_card_templates ={
    'acoustic': {'mfa':mfa_acoustic_model_card_template, 'other': other_acoustic_model_card_template},
    'dictionary': {'mfa':mfa_dictionary_card_template, 'other': other_dictionary_card_template},
    'g2p': {'mfa':g2p_model_card_template, 'other': g2p_model_card_template},
    'language_model': {'mfa':language_model_card_template, 'other': language_model_card_template},
    'corpus': {'mfa': corpus_card_template, 'other': corpus_card_template},
    'ivector': {'mfa': ivector_card_template, 'other': ivector_card_template},
    'tokenizer': {'mfa': tokenizer_model_card_template, 'other': tokenizer_model_card_template},
}
docs_card_templates ={
    'acoustic': {'mfa':acoustic_docs_md_template, 'other': acoustic_docs_md_template},
    'dictionary': {'mfa':mfa_dictionary_docs_md_template, 'other': other_dictionary_docs_md_template},
    'g2p': {'mfa':g2p_docs_md_template, 'other': g2p_docs_md_template},
    'language_model': {'mfa':lm_docs_md_template, 'other': lm_docs_md_template},
    'corpus': {'mfa': corpus_docs_md_template, 'other': corpus_docs_md_template},
    'ivector': {'mfa': ivector_docs_md_template, 'other': ivector_docs_md_template},
    'tokenizer': {'mfa': tokenizer_docs_md_template, 'other': tokenizer_docs_md_template},
}
model_type_names ={
    'acoustic': 'Acoustic models',
    'dictionary': 'Pronunciation dictionaries',
    'g2p': 'G2P models',
    'language_model': 'Language models',
    'corpus': 'Corpora',
    'ivector': 'Ivector extractors',
    'tokenizer': 'Tokenizer models',
}
model_type_columns ={
    'acoustic': 'ID;language;dialect;phoneset;license',
    'ivector': 'ID;language;license',
    'dictionary': 'ID;language;dialect;phoneset;license',
    'g2p': 'ID;language;dialect;phoneset;license',
    'language_model': 'ID;language;dialect;license',
    'corpus': 'ID;language;dialect;license',
    'tokenizer': 'ID;language;license',
}
model_type_column_widths ={
    'acoustic': '40;20;20;10;10',
    'dictionary': '40;20;20;10;10',
    'g2p': '40;20;20;10;10',
    'language_model': '50;20;20;10',
    'ivector': '50;25;25',
    'tokenizer': '50;25;25',
    'corpus': '40;20;25;15',
}

meta_datas = {}

chart_template = """``````{{list-table}}
:header-rows: 1
:stub-columns: {stub_column_count}
:class: {type}_chart table-striped table-bordered

* - {header_data}
* - {row_data}
``````
"""

def generate_extra_data(dictionary, base_indent):
    lines = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            lines.append(f"{base_indent}* {key}")
            if len(value) > 4:
                value = {k: value[k] for k in rng.choice(list(value.keys()),4,replace=False)}
            lines.extend(generate_extra_data(value, base_indent='  ' + base_indent))
        else:
            lines.append(f"{base_indent}* {key}: {value}")
    return lines


def format_ipa_cell(phone_data: dict[str, list[str]],
                    extra_data:dict[str,dict[str,typing.Any]] =None, base_indent: typing.Optional[str]='') -> str:
    cell_lines = [f"```{{ipa_cell}}"]
    for phone_class, v in phone_data.items():
        if not v:
            continue
        cell_lines.append(f'{base_indent}* {phone_class}')
        for phone in v:
            cell_lines.append(f'{base_indent}  * {phone}')
            if phone in extra_data:
                cell_lines.extend(generate_extra_data(extra_data[phone],base_indent=base_indent+'    '))
    cell_lines.append(f'{base_indent}```')
    cell_content = '\n'.join(cell_lines)
    return cell_content


def check_phone(phone, feature_set, phone_set_type):
    if phone_set_type is PhoneSetType.ARPA:
        return phone in feature_set
    else:
        return any(x in phone for x in feature_set)

@profile
def analyze_dictionary(dictionary_path, name, phone_set_type):
    d = load_dict(dictionary_path, name, phone_set_type=phone_set_type)
    dictionary_mapping = collections.defaultdict(set)
    if d.phone_set_type is PhoneSetType.ARPA:
        super_segmentals = {'stress': re.compile(r'[0-2]+')}
        ipa_mapping = {
            "stops": d.phone_set_type.stops,
            "voiced": d.phone_set_type.voiced_obstruents,
            "voiceless": d.phone_set_type.voiceless_obstruents,
            "fricative": d.phone_set_type.fricatives,
            "affricates": d.phone_set_type.affricates,
            "sibilant": d.phone_set_type.sibilants,
            "lateral": d.phone_set_type.laterals,
            "nasal": d.phone_set_type.nasals,
            "approximant": d.phone_set_type.approximants,
            "labial": d.phone_set_type.labials,
            "labiodental": d.phone_set_type.labiodental,
            "dental": d.phone_set_type.dental,
            "alveolar": d.phone_set_type.alveolar,
            "alveopalatal": d.phone_set_type.alveopalatal,
            "velar": d.phone_set_type.velar,
            "glottal": d.phone_set_type.glottal,
            "implosive": set(),
            "lateral_tap": set(),
            "tap": set(),
            "palatal": d.phone_set_type.palatal,
            "trill": set(),
            "pharyngeal": set(),
            "epiglottal": set(),
            "uvular": set(),
            "retroflex": set(),
            "lateral_fricative": set(),
            "close": d.phone_set_type.close_vowels,
            "close-mid": d.phone_set_type.close_mid_vowels,
            "open-mid": d.phone_set_type.open_mid_vowels,
            "open": d.phone_set_type.open_vowels,
            "front": d.phone_set_type.front_vowels - {'IH'},
            "near-front": {'IH'},
            "central": d.phone_set_type.central_vowels,
            "back": d.phone_set_type.back_vowels - {'UH'},
            "near-back": {'UH'},
            "rounded": d.phone_set_type.rounded_vowels,
            "unrounded": d.phone_set_type.unrounded_vowels,
            "lax": {'IH', 'UH', 'AH', 'AE', 'ER'},
            "other": set()
        }
    else:
        ipa_mapping = {

            "stops": d.phone_set_type.stops,
        "voiced": d.phone_set_type.voiced_obstruents,
        "voiceless": d.phone_set_type.voiceless_obstruents,
        "implosive": d.phone_set_type.implosive_obstruents,
        "fricative": d.phone_set_type.fricatives,
        "sibilant": d.phone_set_type.sibilants,
        "lateral": d.phone_set_type.laterals,
        "lateral_fricative": d.phone_set_type.lateral_fricatives,
        "nasal": d.phone_set_type.nasals,
        "nasal_approximants": d.phone_set_type.nasal_approximants,
        "trill": d.phone_set_type.trills,
        "tap": d.phone_set_type.taps,
        "lateral_tap": d.phone_set_type.lateral_taps,
        "approximant": d.phone_set_type.approximants - d.phone_set_type.nasal_approximants,
        "labial": d.phone_set_type.labials,
        "labiodental": d.phone_set_type.labiodental,
        "dental": d.phone_set_type.dental,
        "alveolar": d.phone_set_type.alveolar,
        "retroflex": d.phone_set_type.retroflex,
        "alveopalatal": d.phone_set_type.alveopalatal,
        "palatal": d.phone_set_type.palatal,
        "velar": d.phone_set_type.velar,
        "uvular": d.phone_set_type.uvular,
        "pharyngeal": d.phone_set_type.pharyngeal,
        "epiglottal": d.phone_set_type.epiglottal,
        "glottal": d.phone_set_type.glottal,
            "close": d.phone_set_type.close_vowels,
            "close-mid": d.phone_set_type.close_mid_vowels,
            "open-mid": d.phone_set_type.open_mid_vowels,
            "open": d.phone_set_type.open_vowels,
            "front": d.phone_set_type.front_vowels - {'ɪ', 'ʏ', 'ɛ̈', 'ʏ̈'},
            "near-front": {'ɪ', 'ʏ', 'ɛ̈', 'ʏ̈'},
            "central": d.phone_set_type.central_vowels,
            "back": d.phone_set_type.back_vowels - {'ʊ', 'ɔ̈'},
            "near-back": {'ʊ', 'ɔ̈'},
            "rounded": d.phone_set_type.rounded_vowels,
            "unrounded": d.phone_set_type.unrounded_vowels,
            "lax": {'ɪ', 'ʏ', 'ʊ', 'ə', 'ɐ', 'æ', 'ɚ'},
            "nasalized": {'ã', 'õ', 'ĩ', 'ũ', 'ẽ'},
            "other": {'kp', 'ɧ', 'ŋm'}
        }
        super_segmentals = {'tones': re.compile(r'[˩˨˧˦˥ˀ]+')}
        for k, v in ipa_mapping.items():
            voiceless = [x for x in v if x in ipa_mapping['voiceless']]
            voiced = [x for x in v if x not in ipa_mapping['voiceless']]
            mod_phones = set()
            for p in voiceless:
                mod_phones |= voiceless_variants(p)
            for p in voiced:
                mod_phones |= voiced_variants(p)
            ipa_mapping[k] = mod_phones | v
    extra_data = {}
    with d.session() as session:
        phones = session.query(Phone).filter(Phone.phone_type == PhoneType.non_silence)
        phone_counts = collections.Counter()
        pronunciations = session.query(Pronunciation.pronunciation)
        for p, in pronunciations:
            p = p.split()
            phone_counts.update(p)

    total_phones = set()
    triphthongs = d.phone_set_type.triphthong_phones
    diphthongs = d.phone_set_type.diphthong_phones
    for phone in phones:
        words = session.query(
            Word.word, Pronunciation.pronunciation
        ).join(
            Word.pronunciations
        ).filter(
            sqlalchemy.func.length(Word.word) > 2,
            sqlalchemy.func.length(Word.word) < 6,
            Pronunciation.probability != None,  # noqa
            Pronunciation.pronunciation.regexp_match(rf'\b{phone.phone}(?=\s|$)')
        ).distinct().order_by(sqlalchemy.func.random()).limit(4)
        for super_seg, pattern in super_segmentals.items():
            phone_m = pattern.search(phone.phone)
            if phone_m:
                dictionary_mapping[super_seg].add(phone_m.group(0))
                counts = phone_counts[phone.phone]
                examples = {}
                for w, pron in words:
                    examples[w] = f"[{pron}]"
                phone = phone.phone.replace(phone_m.group(0), '')
                if phone not in extra_data:
                    extra_data[phone] = {'Occurrences': 0, 'Examples': {}}
                if isinstance(extra_data[phone]['Occurrences'], str):
                    try:
                        extra_data[phone]['Occurrences'] = int(extra_data[phone]['Occurrences'])
                    except ValueError:
                        extra_data[phone]['Occurrences'] = 0
                extra_data[phone]['Occurrences'] += counts
                extra_data[phone]['Examples'].update(examples)
                break
        else:
            extra_data[phone.phone] = {'Occurrences': phone_counts[phone.phone], 'Examples': {}}
            phone = phone.phone
            for w, pron in words:
                extra_data[phone]['Examples'][w] = f"[{pron}]"
        base_phone = d.get_base_phone(phone)
        query_set = {phone, base_phone}
        if base_phone in ipa_mapping['other']:
            dictionary_mapping['other'].add(phone)
            continue
        if 'ʲ' in phone:
            dictionary_mapping["palatalized"].add(phone)
        if 'ʷ' in phone:
            dictionary_mapping["labialized"].add(phone)
        if '̃' in phone:
            dictionary_mapping["nasalized"].add(phone)
            base_phone = base_phone.replace('̃', '')
        if '͈' in phone:
            dictionary_mapping["tense"].add(phone)
            dictionary_mapping["voiceless"].add(phone)
        if '̪' in phone:
            dictionary_mapping["dental"].add(phone)
        if any(x in phone for x in ['ⁿ', 'ᵑ', 'ᵐ']):
            dictionary_mapping["prenasalized"].add(phone)
            dictionary_mapping["voiced"].add(phone)
        elif 'ʱ' in phone or '̤' in phone:
            dictionary_mapping["aspirated"].add(phone)
            dictionary_mapping["voiced"].add(phone)
        elif check_phone(phone, ipa_mapping['voiced'], d.phone_set_type):
            dictionary_mapping["voiced"].add(phone)
        elif check_phone(phone, ipa_mapping['implosive'], d.phone_set_type):
            dictionary_mapping["implosive"].add(phone)
            dictionary_mapping["voiced"].add(phone)
        elif 'ʰ' in phone:
            dictionary_mapping["aspirated"].add(phone)
            dictionary_mapping["voiceless"].add(phone)
        elif 'ʼ' in phone:
            dictionary_mapping["ejective"].add(phone)
            dictionary_mapping["voiceless"].add(phone)
        elif check_phone(phone, ipa_mapping['voiceless'], d.phone_set_type):
            dictionary_mapping["voiceless"].add(phone)
        if '̚' in phone:
            dictionary_mapping["unreleased"].add(phone)
        if any(x in diphthongs for x in query_set):
            dictionary_mapping["diphthong"].add(phone)
        elif any(x in triphthongs for x in query_set):
            dictionary_mapping["triphthong"].add(phone)
        elif any(x in d.phone_set_type.affricates for x in query_set):
            dictionary_mapping["affricate"].add(phone)
        elif any(x in d.phone_set_type.stops for x in query_set):
            dictionary_mapping["stop"].add(phone)
        for k, v in ipa_mapping.items():
            if base_phone in v:
                dictionary_mapping[k].add(phone)
        total_phones.add(phone)
        for v in dictionary_mapping.values():
            if phone in v:
                break
        else:
            dictionary_mapping['other'].add(phone)
    places = ['labial', 'labiodental', 'dental', 'alveolar', 'alveopalatal', 'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'epiglottal', 'glottal']
    columns = []
    for p in places:
        if p in dictionary_mapping:
            columns.append(p)
    sub_manners = ['tense', 'aspirated', 'implosive', 'ejective', 'unreleased', 'prenasalized']

    rows = []
    plotted = set()
    for manner in ['nasal', 'stop', 'affricate', 'sibilant', 'fricative', 'approximant',
                   'tap', 'trill','lateral_fricative', 'lateral', 'lateral_tap']:
        if manner not in dictionary_mapping:
            continue
        realized_submanner_rows = {}
        for x in sub_manners:
            if dictionary_mapping[manner] & dictionary_mapping[x]:
                realized_submanner_rows[x] = [f'{{submanner}}`{x.title()}`']
        row_title = f"{{manner}}`{manner.replace('_',' ').title()}`"
        if realized_submanner_rows:
            row_title += ' {submanner}`Plain`'
        row = [row_title]
        for place in columns:
            cell_set = dictionary_mapping[manner] & dictionary_mapping[place]
            base_set = dictionary_mapping[manner] & dictionary_mapping[place]
            for x in sub_manners:
                cell_set -= dictionary_mapping[x]
                base_set -= dictionary_mapping[x]
            voiced_set = base_set & dictionary_mapping['voiced']
            voiceless_set = base_set & dictionary_mapping['voiceless']
            other_set = base_set - dictionary_mapping['voiceless'] - dictionary_mapping['voiced']
            plotted.update(voiceless_set)
            plotted.update(voiced_set)
            plotted.update(other_set)
            cell_data = {
                'voiceless': sorted(voiceless_set),
                'voiced': sorted(voiced_set),
                'other': sorted(other_set),
            }
            cell_contents = format_ipa_cell(cell_data, extra_data, base_indent='    ')
            row.append(cell_contents)
        rows.append(row)
        if realized_submanner_rows:
            for place in columns:
                for sub_manner in realized_submanner_rows.keys():
                    cell_set = dictionary_mapping[manner] & dictionary_mapping[place] & dictionary_mapping[sub_manner]
                    for s in realized_submanner_rows.keys():
                        if s == sub_manner:
                            continue
                        cell_set -= dictionary_mapping[s]
                    voiced_set = cell_set & dictionary_mapping['voiced']
                    voiceless_set = cell_set & dictionary_mapping['voiceless']
                    other_set = cell_set - dictionary_mapping['voiceless'] - dictionary_mapping['voiced']
                    plotted.update(voiceless_set)
                    plotted.update(voiced_set)
                    plotted.update(other_set)
                    cell_data = {
                        'voiceless': sorted(voiceless_set),
                        'voiced': sorted(voiced_set),
                        'other': sorted(other_set),
                    }
                    cell_contents = format_ipa_cell(cell_data, extra_data, base_indent='    ')
                    realized_submanner_rows[sub_manner].append(cell_contents)
            rows.extend(realized_submanner_rows.values())
    row_headers = ['Manner']
    columns = row_headers + columns
    consonants = {'header': columns, 'rows': rows}


    oral_rows = []
    nasal_rows = []
    headers = ['front', 'near-front', 'central', 'near-back', 'back']
    has_nasal = False
    for height in ['close', 'close-mid', 'open-mid', 'open']:
        for on in ['nasalized', 'oral']:
            main_row = [height.title()]
            lax_row = ['']
            for column in headers:
                cell_set = dictionary_mapping[height] & dictionary_mapping[column]
                if on in dictionary_mapping: # nasalized
                    cell_set &= dictionary_mapping['nasalized']
                    if cell_set and not has_nasal:
                        has_nasal = True
                else:
                    cell_set -= dictionary_mapping['nasalized']
                if height == 'close' and column in {'front', 'back'}:
                    lax_set = set()
                    tense_set = cell_set - dictionary_mapping['lax']
                elif height == 'close' and column in {'near-front', 'near-back'}:
                    tense_set = set()
                    lax_set = cell_set & dictionary_mapping['lax']
                else:
                    tense_set = cell_set - dictionary_mapping['lax']
                    lax_set = cell_set & dictionary_mapping['lax']

                tense_rounded = tense_set & dictionary_mapping['rounded']
                tense_unrounded = tense_set & dictionary_mapping['unrounded']
                cell_data = {
                    'unrounded': sorted(tense_unrounded),
                    'rounded': sorted(tense_rounded),
                }
                plotted.update(tense_unrounded)
                plotted.update(tense_rounded)
                tense_cell_contents = format_ipa_cell(cell_data, extra_data, base_indent='    ')

                lax_rounded = lax_set & dictionary_mapping['rounded']
                lax_unrounded = lax_set & dictionary_mapping['unrounded']
                plotted.update(lax_rounded)
                plotted.update(lax_unrounded)
                cell_data = {
                    'unrounded': sorted(lax_unrounded),
                    'rounded': sorted(lax_rounded),
                }
                lax_cell_contents = format_ipa_cell(cell_data, extra_data, base_indent='    ')

                main_row.append(tense_cell_contents)
                lax_row.append(lax_cell_contents)
            if on in dictionary_mapping: # nasalized
                nasal_rows.append(main_row)
                if height != 'open':
                    nasal_rows.append(lax_row)
            else:
                oral_rows.append(main_row)
                if height != 'open':
                    oral_rows.append(lax_row)

    headers = [''] + [x.title() for x in headers]
    if not has_nasal:
        nasal_rows = None

    header_row_string = '\n  - '.join(x.title() for x in consonants['header'])
    row_strings = '\n* - '.join('\n  - '.join(x) for x in consonants['rows'])
    stub_column_count = 1
    consonant_chart = chart_template.format(header_data=header_row_string,
                                            row_data= row_strings, type='consonant',
                                            stub_column_count=stub_column_count)
    vowels = {'oral_rows': oral_rows, 'nasal_rows': nasal_rows, 'header': headers,
              }
    header_row_string = '\n  - '.join(vowels['header'])
    row_strings = '\n* - '.join('\n  - '.join(x) for x in vowels['oral_rows'])

    oral_chart = chart_template.format(header_data=header_row_string,
                                       row_data= row_strings, type='vowel',
                                       stub_column_count=1)
    nasal_chart = None
    if nasal_rows:
        header_row_string = '\n  - '.join(vowels['header'])
        row_strings = '\n* - '.join('\n  - '.join(x) for x in vowels['nasal_rows'])

        nasal_chart = chart_template.format(header_data=header_row_string,
                                            row_data= row_strings, type='vowel',
                                       stub_column_count=1)

    data = {'consonant_chart': consonant_chart, 'oral_vowel_chart': oral_chart, 'nasal_vowel_chart': nasal_chart,
     'diphthongs': dictionary_mapping['diphthong'], 'other': dictionary_mapping['other'] & (total_phones- plotted),
     'triphthongs': dictionary_mapping['triphthong']}
    for k in super_segmentals.keys():
        if k in dictionary_mapping:
            data[k] = dictionary_mapping[k]
    return data

phone_charts = {}
model_mappings = {}
for model_type, model_class in MODEL_TYPES.items():
    #if model_type != 'ivector':
    #    continue
    meta_datas[model_type] = {}
    model_mappings[model_type] = {}
    model_directory = os.path.join(mfa_model_root, model_type)
    staging_directory = os.path.join(model_directory, 'staging')

    models_to_stage = os.listdir(staging_directory)
    for file_name in models_to_stage:
        if model_type == 'dictionary' and not file_name.endswith('.dict'):
            continue
        print(file_name)
        model = model_class(os.path.join(staging_directory, file_name))
        print(model.meta)
        s = model.name.split('_')
        dialect = ''
        if model_type == 'language_model':
            if '_mfa' in model.name:
                s = model.name.replace('_mfa', '').split('_')
            language = '_'.join(s[:-1])
            dialect = ' '.join(s[1:-1])
            phone_set = 'MFA'
        elif model_type == 'ivector':
            language = model.name.replace('_mfa', '')
            dialect = ''
            phone_set = ''
        elif model_type == 'tokenizer':
            language = model.name.replace('_mfa', '')
            dialect = ''
            phone_set = ''
        elif len(s) == 1:
            language = s[0]
            phone_set = 'Unknown'
            dialect = ''
        elif len(s) == 2:
            language, phone_set = s
            phone_set = phone_set.upper()
            dialect = ''
        else:
            language = s[0]
            phone_set = s[-1].upper()
            dialect = ' '.join(s[1:-1])
        try:
            version = model.meta['version']
        except KeyError:
            version = montreal_forced_aligner.utils.get_mfa_version()
        if version.startswith('2.') or version.startswith('3.'):
            version = CURRENT_MODEL_VERSION
        language = language.title()
        if len(dialect) == 2:
            dialect = dialect.upper()
        else:
            dialect = dialect.title()
        print(model_directory, language, phone_set, version)
        if dialect:
            phone_set_folder = f'{dialect}_{phone_set}'.replace(' ', '_').lower()
        else:
            phone_set_folder = phone_set.lower()
        if phone_set_folder:
            output_directory = os.path.join(model_directory, language.lower(), phone_set_folder, f"v{version}")
        else:
            output_directory = os.path.join(model_directory, language.lower(), f"v{version}")
        os.makedirs(output_directory, exist_ok=True)
        license_path = os.path.join(output_directory, "LICENSE")
        if phone_set != 'CV' and  not os.path.exists(license_path):
            shutil.copyfile(os.path.join(mfa_model_root, "LICENSE"), license_path)
        meta_path = os.path.join(output_directory, 'meta.json')
        if OVERWRITE_METADATA or not os.path.exists(meta_path):
            meta_data = generate_meta_data(model, model_type, language, dialect, version, phone_set)
            with open(meta_path, 'w', encoding='utf8') as f:
                json.dump(meta_data, f, indent=4, ensure_ascii=False)
        else:
            with open(meta_path, 'r', encoding='utf8') as f:
                meta_data = json.load(f)
        meta_datas[model_type][generate_id(meta_data, model_type)] = meta_data
        keys = [language]
        if model_type in {'language_model', 'ivector', 'tokenizer'}:
            if dialect:
                keys.append((language, dialect))
                key = (language, dialect)
        else:
            if dialect:
                keys.append((language, dialect))
                keys.append((language, dialect, phone_set))
                key = (language, dialect, phone_set)
                dialect_key = (language, dialect)
            else:
                keys.append((language, phone_set))
        for key in keys:
            if key not in model_mappings[model_type]:
                model_mappings[model_type][key] = []
            model_mappings[model_type][key].append(generate_id(meta_data, model_type))
        if model_type == 'dictionary' and phone_set in {'MFA', 'CV', 'ARPA'}:
            phone_set_type = 'IPA'
            if phone_set == 'ARPA':
                phone_set_type = 'ARPA'
            phone_charts[meta_data['name']] = analyze_dictionary(model.path, model.name, phone_set_type)
            #if language == 'hindi':
            #    err
    existing_models = []
    for language in os.listdir(model_directory):
        if language in {'staging', 'training', 'filter_lists', '1.0'}:
            continue
        language_directory = os.path.join(model_directory, language)
        if not os.path.isdir(language_directory):
            continue
        language = language.title()
        if model_type in {'ivector', 'tokenizer'}:
            for version in os.listdir(language_directory):
                meta_path = os.path.join(language_directory, version, 'meta.json')
                if not os.path.exists(meta_path):
                    continue
                with open(meta_path, 'r', encoding='utf8') as f:
                    meta_data = json.load(f)
                meta_datas[model_type][generate_id(meta_data, model_type)] = meta_data
                keys = [language]
                for key in keys:
                    if key not in model_mappings[model_type]:
                        model_mappings[model_type][key] = []
                    model_mappings[model_type][key].append(generate_id(meta_data, model_type))

        else:
            for phone_set in os.listdir(language_directory):
                print(phone_set)
                phone_set_dir = os.path.join(language_directory, phone_set)
                if '_' in phone_set:
                    dialect, phone_set = phone_set.rsplit('_', maxsplit=1)
                else:
                    dialect = ''
                for version in os.listdir(phone_set_dir):
                    meta_path = os.path.join(phone_set_dir, version, 'meta.json')
                    if not os.path.exists(meta_path):
                        continue
                    with open(meta_path, 'r', encoding='utf8') as f:
                        meta_data = json.load(f)
                    meta_datas[model_type][generate_id(meta_data, model_type)] = meta_data
                    keys = [language]
                    if model_type == 'language_model':
                        if dialect:
                            keys.append((language, dialect))
                            key = (language, dialect)
                    else:
                        if dialect:
                            keys.append((language, dialect))
                            keys.append((language, dialect, phone_set))
                            key = (language, dialect, phone_set)
                            dialect_key = (language, dialect)
                        else:
                            keys.append((language, phone_set))
                    for key in keys:
                        if key not in model_mappings[model_type]:
                            model_mappings[model_type][key] = []
                        model_mappings[model_type][key].append(generate_id(meta_data, model_type))



if 'dictionary' in meta_datas:
    for k in model_corpus_mapping.keys():
        dict_id = k.replace('acoutic model', 'dictionary')
        if dict_id in meta_datas['dictionary']:
            model_dictionary_mapping[k] = [dict_id]

if 'g2p' in meta_datas:
    for v in model_corpus_mapping.values():
        for d_id in v:
            g2p_id = d_id.replace('dictionary', 'G2P model')
            if g2p_id in meta_datas['g2p']:
                model_dictionary_mapping[g2p_id] = [d_id]


if 'language_model' in meta_datas:
    for k,v in model_dictionary_mapping.items():
            lm_id = k.replace('acoustic', 'language')
            if lm_id in meta_datas['language_model']:
                model_dictionary_mapping[lm_id] = v


if 'tokenizer' in meta_datas:
    for k,v in model_dictionary_mapping.items():
            tokenizer_id = k.replace('tokenizer', 'language')
            if tokenizer_id in meta_datas['tokenizer']:
                model_dictionary_mapping[tokenizer_id] = v


corpora_metadata = {}
model_mappings['corpus'] = {}
corpus_metadata_file = os.path.join(mfa_model_root, 'corpus', 'staging', 'corpus_data.json')
if os.path.exists(corpus_metadata_file):
    with open(corpus_metadata_file, 'r', encoding='utf8') as f:
        data = json.load(f)
    for language, c_list in data.items():
        if language == "Hindi-Urdu":
            continue
        for c in c_list:
            name = c['name']
            if 'version' in c:
                name += f'_{c["version"]}'
            id = make_path_safe(name)
            c['language'] = language
            c['id'] = generate_id(c, 'corpus')

            c['license_link'] = f"[{c['license']}]({license_links[c['license']]})"
            if 'dialects' not in c:
                c['dialects'] = []
            c['dialects'] = [x.title() if len(x)>2 else x.upper() for x in c['dialects']]
            corpora_metadata[c['id']] = c
            print(c)
            print(generate_id(c, 'corpus'))
            language_key = language
            if language_key not in model_mappings['corpus']:
                model_mappings['corpus'][language_key] = []
            model_mappings['corpus'][language_key].append(c['id'])
            if c['dialects']:
                for d in c['dialects']:
                    key = (language, d)
                    if key not in model_mappings['corpus']:
                        model_mappings['corpus'][key] = []
                    model_mappings['corpus'][key].append(c['id'])

    meta_datas['corpus'] = corpora_metadata

# Add links
for model_type, data in meta_datas.items():

    for model_name, meta_data in data.items():
        model_id = generate_id(meta_data, model_type)
        if model_type in {'acoustic','language_model', 'ivector', 'tokenizer'}:
            print("HELLO!?", model_id, model_corpus_mapping.keys())
            if model_id in model_corpus_mapping:
                print(model_corpus_mapping[model_id])
                print(corpora_metadata.keys())
                meta_data['corpus'] = [corpora_metadata[x] for x in model_corpus_mapping[model_id]]
                for corpus_id in model_corpus_mapping[model_id]:
                    if model_type not in meta_datas['corpus'][corpus_id]:
                        meta_datas['corpus'][corpus_id][model_type] = []
                    meta_datas['corpus'][corpus_id][model_type].append(model_id)
        if model_type in {'language_model', 'corpus', 'ivector'}:
            if "dialect" in meta_data and meta_data['dialect']:
                key = (meta_data['language'], meta_data['dialect'])
            else:
                key = meta_data['language']
        else:
            if "dialect" in meta_data and meta_data['dialect']:
                key = (meta_data['language'], meta_data['dialect'], meta_data['phone_set'])
            else:
                key = (meta_data['language'], meta_data['phone_set'])
        if model_type in {'acoustic','language_model', 'g2p'}:
            print(meta_data['name'])
            print(key)
            print(model_mappings['dictionary'])
            if key in model_mappings['dictionary']:
                if 'dictionary' not in meta_data:
                    meta_data['dictionary'] = []
                meta_data['dictionary'].extend(model_mappings['dictionary'][key])
            if model_id in model_dictionary_mapping:
                if 'dictionary' not in meta_data:
                    meta_data['dictionary'] = []
                meta_data['dictionary'].extend([x for x in model_dictionary_mapping[model_id] if x not in meta_data['dictionary']])
        elif model_type == 'dictionary':
            for t in ['acoustic', 'g2p','language_model', 'corpus']:
                if key in model_mappings[t]:
                    if t not in meta_data:
                        meta_data[t] = []
                    meta_data[t].extend(model_mappings[t][key])
        elif model_type == 'corpus':
            meta_data['dictionary'] = []
            if "dialects" in meta_data and meta_data['dialects']:
                for dialect in meta_data['dialects']:
                    key = (meta_data['language'], dialect)
                    if key in model_mappings['dictionary']:
                        meta_data['dictionary'].extend(model_mappings['dictionary'][key])
            else:
                print(meta_data['language'], model_mappings['dictionary'], meta_data['language'] in model_mappings['dictionary'])
                if meta_data['language'] in model_mappings['dictionary']:
                    for dictionary_id in model_mappings['dictionary'][meta_data['language']]:
                        m = meta_datas['dictionary'][dictionary_id]
                        meta_data['dictionary'].append(dictionary_id)

for model_type, data in meta_datas.items():
    docs_dir = os.path.join(mfa_model_root, 'docs', 'source', model_type)
    os.makedirs(docs_dir, exist_ok=True)
    language_model_doc_mds = {}
    for model_name, meta_data in data.items():
        print(model_name, meta_data)
        if model_type not in {'language_model', 'corpus'} and meta_data['phone_set'] in {'PROSODYLAB', 'PINYIN'}:
            model_card_template = model_card_templates[model_type]['other']
            docs_md_template = docs_card_templates[model_type]['other']
        elif model_type not in {'language_model', 'corpus'} and meta_data['phone_set'] in {'CV'}:
            model_card_template = model_card_templates[model_type]['other']
            docs_md_template = docs_card_templates[model_type]['mfa']
        else:
            model_card_template = model_card_templates[model_type]['mfa']
            docs_md_template = docs_card_templates[model_type]['mfa']
        if model_type == 'language_model':
            language, version = meta_data['language'], meta_data['version']
        elif model_type == 'corpus':
            language, name = meta_data['language'], meta_data['name']
            name = make_path_safe(name)
        else:
            language, phone_set, dialect, version = meta_data['language'], meta_data['phone_set'], meta_data['dialect'], meta_data['version']
        output_directory = get_model_card_directory(model_type, meta_data)
        os.makedirs(output_directory, exist_ok=True)
        model_card_path = os.path.join(output_directory, 'README.md')
        rst_path = model_name+ '.md'
        docs_language_dir = os.path.join(docs_dir, language)
        if language not in language_model_doc_mds:
            language_model_doc_mds[language] = []
        os.makedirs(docs_language_dir, exist_ok=True)
        docs_card_path = os.path.join(docs_language_dir, rst_path)
        language_model_doc_mds[language].append(rst_path)
        if (OVERWRITE_MD or not os.path.exists(model_card_path)):
            with open(model_card_path, 'w', encoding='utf8') as f:
                print(meta_data)
                fields = extract_model_card_fields(meta_data, model_type)
                f.write(model_card_template.format(**fields))
        if (OVERWRITE_MD or not os.path.exists(docs_card_path)):
            with open(docs_card_path, 'w', encoding='utf8') as f:
                print(meta_data)
                fields = extract_doc_card_fields(meta_data, model_type)
                f.write(docs_md_template.format(**fields))
    index_path = os.path.join(docs_dir, 'index.rst')
    rst_string = "   "+'\n   '.join(f"{x}/index.rst" for x in sorted(language_model_doc_mds.keys()))
    if model_type == 'dictionary':
        rst_string = '   ../mfa_phone_set.md\n' + rst_string
    model_type_name = model_type_names[model_type]
    columns = model_type_columns[model_type]
    widths = model_type_column_widths[model_type]
    with open(index_path, 'w', encoding='utf8') as f:
        f.write(f"""

.. _{model_type}:

{model_type_name}
{'='* len(model_type_name)}

.. needtable::
   :types: {model_type}
   :style: datatable
   :columns: {columns}
   :class: table-striped
   :colwidths: {widths}

.. toctree::
   :hidden:

{rst_string}
""")
    for language, model_doc_mds in sorted(language_model_doc_mds.items()):
        index_path = os.path.join(docs_dir, language, 'index.rst')
        rst_string = "   "+'\n   '.join(model_doc_mds)
        with open(index_path, 'w', encoding='utf8') as f:
            f.write(f"""

.. _{model_type}_{language.lower()}:

{language.title()}
{'='* len(language)}

.. needtable::
   :types: {model_type}
   :filter: language == "{language.title()}"
   :style: datatable
   :columns: {columns}
   :class: table-striped
   :colwidths: {widths}

.. toctree::
   :hidden:

{rst_string}
""")

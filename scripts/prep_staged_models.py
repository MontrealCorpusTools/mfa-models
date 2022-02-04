import json
import os
import shutil
from datetime import datetime

import montreal_forced_aligner.utils
from montreal_forced_aligner.models import MODEL_TYPES

mfa_model_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OVERWRITE_METADATA = False
OVERWRITE_MD = True

mfa_citation_template = "@techreport{{MFA_{model_name}_{model_type}_{year}, author={{McAuliffe, Michael and Sonderegger, Morgan}}, " \
                        "title={{{language} {phone_set} MFA {model_type} v{version}}}, " \
                        "address={{\\url{{https://mfa-models.readthedocs.io/}}, " \
                        "year={{{year}}}, month={{{month}}}, " \
                        "number={{{language}-{phone_set}-{version}}}"
cv_citation = "@misc{Ahn_Chodroff_2022, author={Ahn, Emily and Chodroff, Eleanor}, " \
                        "title={VoxCommunis Corpus}, " \
                        "address={\\url{https://osf.io/t957v}, " \
                        "publisher={OSF}, " \
                        "year={2022}, month={Jan}}"
prosodylab_citation = "@article{gorman2011prosodylab, author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael}, " \
                        "title={Prosodylab-aligner: A tool for forced alignment of laboratory speech}, " \
                        "journal={Canadian Acoustics}, " \
                        "volume={39}, number={3}, pages={192--193}, year={2011}}"

mfa_maintainer = "[Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)"
cv_maintainer = "[Vox Communis](https://osf.io/t957v/)"

corpus_detail_template="""
* {name}:
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

lm_training_detail_template="""
* **Words:** `{num_words:,}`
* **OOVs:** `{num_oovs:,}`"""

lm_evaluation_detail_template="""
* **Large model:** `{large_perplexity:.2f}`
* **Medium model:** `{medium_perplexity:.2f}`
* **Small model:** `{small_perplexity:.2f}`"""

link_template = '* {{need}}`{}`'

see_also_template = """
   ```{{admonition}} See also
   {links}
   ```"""

mfa_acoustic_model_card_template = """
# {model_name} acoustic model v{version}

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Training data](#training-data)
- [Evaluation data](#evaluation-data)
- [Metrics](#metrics)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** {maintainer}
- **Language:** `{language}`
- **Trained date:** `{date}`
- **Model type: `Acoustic`
- **Architecture:** `{architecture}`
- **Phone set:** `{phone_set}`
- **Model version:** `v{version}`
- **Compatible MFA version:** `v{mfa_version}`
- **License:** {license_link}
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download acoustic {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/acoustic-{model_name}-v{version})

## Intended use

This model is intended for forced alignment of [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

This model uses the {phone_set} phone set for {language}, and was trained with the [{model_name} dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/dictionary/{language}/{phone_set}/{model_name}).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

As forced alignment is a relatively well-constrained problem (given accurate transcripts), this model should be applicable to a range of recording conditions and speakers.
However, please note that it was trained on read speech in low-noise environments, so as your data diverges from that,
you may run into alignment issues or need to [increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands) or see other recommendations in the [troubleshooting section below](#troubleshooting-issues).

Please note as well that MFA does not use state-of-the-art models for forced alignment.
You may get better performance (especially on speech-to-text tasks) using other frameworks like [Coqui](https://coqui.ai/).

## Training data

This model was trained on the following corpora:

{corpora_details}

Training across corpora:
  * **Number of OOV tokens:** `{num_oovs:,}`
  * **Final alignment log-likelihood:** `{average_log_likelihood:.2f}`

## Evaluation data

The same data used to train the models was used to provide ballpark evaluation.

## Metrics

Acoustic models are typically generated as one component of a larger ASR system where the metric is word error rate (WER).
For forced alignment, there is typically not the same sort of gold standard measure for most languages.

As a rough approximation of the acoustic model quality, we evaluated it against the corpus it was trained on alongside a language model
trained from the same data.  Key caveat here is that this is not a typical WER measure on held out data, so it should not be taken
as a hard measure of how well an acoustic model will generalize to your data, but rather is more of a sanity check that the training data quality was sufficiently high.

Using the [{model_name} dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/{language}/{phone_set}/{model_name}) and [{model_name} language_model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/language_model/{language}/{phone_set}/{model_name}):

- **WER:** `0%`
- **CER:** `0%`

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For STT models, it is often the case that transcription accuracy is better for men than it is for women. If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text may be mis-used to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in may countries. You should not assume consent to record and analyze private speech.


## Troubleshooting issues

Machine learning models (like this acoustic model) perform best on data that is similar to the data on which they were trained.

The primary sources of variability in forced alignment will be the applicability of the pronunciation dictionary and how similar the speech,
demographics, and recording conditions are. If you encounter issues in alignment, there are couple of avenues to improve performance:

1. [Increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands)

   * MFA defaults to a narrow beam to ensure quick alignment and also as a way to detect potential issues in your dataset, but depending on your data, you might benefit from boosting the beam to 100 or higher.

2. Add pronunciations to the pronunciation dictionary

   * This model was trained a particular dialect/style, and so adding pronunciations more representative of the variety spoken in your dataset will help alignment

3. Check the quality of your data

   * MFA includes a [validator utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/data_validation.html), which aims to detect issues in the dataset
   * Use MFA's [anchor utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/anchor.html) to visually inspect your data as MFA sees it and correct issues in transcription or OOV items.

4. Adapt the model to your data

   * MFA has an [adaptation command](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/adapt_acoustic_model.html) to adapt some of the model to your data based on an initial alignment, and then run another alignment with the adapted model.
"""

other_acoustic_model_card_template = """
# {model_name} acoustic model v{version}

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Training data](#training-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** {maintainer}
- **Language:** `{language}`
- **Trained date:** `{date}`
- **Model type:** `Acoustic model`
- **Phone set:** `{phone_set}`
- **Model version:** `v{version}`
- **Architecture:** `{architecture}`
- **Compatible MFA version:** `v{mfa_version}`
- **License:** {license_link}
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, please contact the maintainers, or file an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download acoustic {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/acoustic-{model_name}-v{version})

## Intended use

This model is intended for forced alignment of [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

This model uses the {phone_set} phone set for {language}, and was trained with the [{model_name} dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/dictionary/{language}/{phone_set}/{model_name}).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

As forced alignment is a relatively well-constrained problem (given accurate transcripts), this model should be applicable to a range of recording conditions and speakers.
However, please note that it was trained on read speech in low-noise environments, so as your data diverges from that,
you may run into alignment issues or need to [increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands) or see other recommendations in the [troubleshooting section below](#troubleshooting-issues).

Please note as well that MFA does not use state-of-the-art models for forced alignment.
You may get better performance (especially on speech-to-text tasks) using other frameworks like [Coqui](https://coqui.ai/).

## Training data

This model was trained on the following corpora:

{corpora_details}

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For STT models, it is often the case that transcription accuracy is better for men than it is for women. If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text may be mis-used to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in may countries. You should not assume consent to record and analyze private speech.

## Troubleshooting issues

Machine learning models (like this acoustic model) perform best on data that is similar to the data on which they were trained.

The primary sources of variability in forced alignment will be the applicability of the pronunciation dictionary and how similar the speech,
demographics, and recording conditions are. If you encounter issues in alignment, there are couple of avenues to improve performance:

1. [Increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands)

   * MFA defaults to a narrow beam to ensure quick alignment and also as a way to detect potential issues in your dataset, but depending on your data, you might benefit from boosting the beam to 100 or higher.

2. Add pronunciations to the pronunciation dictionary

   * This model was trained a particular dialect/style, and so adding pronunciations more representative of the variety spoken in your dataset will help alignment

3. Check the quality of your data

   * MFA includes a [validator utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/data_validation.html), which aims to detect issues in the dataset
   * Use MFA's [anchor utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/anchor.html) to visually inspect your data as MFA sees it and correct issues in transcription or OOV items.

4. Adapt the model to your data

   * MFA has an [adaptation command](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/adapt_acoustic_model.html) to adapt some of the model to your data based on an initial alignment, and then run another alignment with the adapted model.
"""

g2p_model_card_template = """
# {model_name} G2P model v{version}

Jump to section:

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Evaluation data](#evaluation-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** {maintainer}
- **Language:** `{language}`
- **Trained date:** `{date}`
- **Model type:** `G2P model`
- **Architecture:** `{architecture}`
- **Phone set:** `{phone_set}`
- **Model version:** `v{version}`
- **Compatible MFA version:** `v{mfa_version}`
- **License:** {license_link}
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download g2p {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/g2p-{model_name}-v{version})

## Intended use

This model is intended for generating pronunciations of [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

This model uses the {phone_set} phone set for {language}, and was trained from the [{model_name} dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/{model_name}.dict).
Pronunciations generated with this G2P model can be appended and used when aligning or transcribing.

## Performance Factors

The trained G2P models should be relatively quick and accurate, however the model may struggle when dealing with less common orthographic characters or word types outside of what it was trained on.
If so, you may need to supplement the dictionary through generating, correcting, and re-training the G2P model as necessary.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with word error rate and phone error rate.

## Training

This model was trained on the following data set:

{training_details}

## Evaluation

This model was evaluated on the following data set:

{evaluation_details}

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For G2P models, the model will only process the types of tokens that it was trained on, and will not represent the full range of text or spoken words that
native speakers will produce.
If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text may be mis-used to invade the privacy of others by recording and mining information from private conversations.
This kind of individual privacy is protected by law in may countries.
You should not assume consent to record and analyze private speech.
"""

language_model_card_template = """
# {model_name} language model v{version}

Jump to section:

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer: {maintainer}
- **Language:** `{language}`
- **Trained date:** `{date}`
- **Model type:** `Language model`
- **Architecture:** `{architecture}`
- **Model version:** `v{version}`
- **Compatible MFA version:** `v{mfa_version}`
- **License:** {license_link}
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download language_model {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/language_model-{model_name}-v{version})

## Intended use

This model is intended for very basic language modeling [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

These ngram models are far from ideal and trained on the same corpus as the acoustic models, and are provided only for completeness
and in the off chance that they're useful in bootstrapping corpus development.

This language was model trained with words from the [{model_name} dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/{model_name}.dict).

## Performance Factors

MFA language model archives contain the main large ngram model, along with two pruned versions that are used in initial decoding
for performance reasons, and then later the large model is used to rescore.  If the initial decoding with the
small version is causing perfomance issues, you can train a new language model with more aggressive pruning.

You should also consider training a language model on your own domain, as that will be much more representative and
useful to use in decoding.

## Metrics

Perplexity for each of three component models was calculated over the training data to give a sense of its performance, but this certainly not be taken as
an absolute measure of model good-ness.

### Perplexity

The following metrics were obtained on evaluation:

{evaluation_details}

## Training data

This model was trained on the following data set:

{training_details}

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For this language model, this model was trained on a very specific subset of {language} at the time it was collected that will typically not represent spontaneous speech in the current time.
Do not use this model in production, but if you do so, you should acknowledge bias as a potential issue.

### Surveillance

Speech-to-Text may be mis-used to invade the privacy of others by recording and mining information from private conversations.
This kind of individual privacy is protected by law in may countries.
You should not assume consent to record and analyze private speech.
"""

mfa_dictionary_card_template = """
# {language} {phone_set}

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** {maintainer}
- **Language:** `{language}`
- **Number of words:** `{word_count:,}`
- **Phones:** `{phones}`
- **License:** {license_link}
- **Compatible MFA version:** `v{mfa_version}`
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-{model_name}-v{version})

## Intended use

This dictionary is intended for forced alignment of [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

This dictionary uses the {phone_set} phone set for {language}, and was used in training the
[{language} {phone_set} acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/{language}/{phone_set}/v{version}/).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation, and each phone has
a minimum duration (by default 30ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.
"""

other_dictionary_card_template = """
# {language} {phone_set}

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** {maintainer}
- **Language: `{language}`
- **Number of words:** `{word_count:,}`
- **Phones:** `{phones}`
- **License:** {license_link}
- **Compatible MFA version: `v{mfa_version}`
- **Citation:**
  - `{citation}`
- If you have comments or questions about this model, please contact the maintainers, or file an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-{model_name}-v{version})

## Intended use

This dictionary is intended for forced alignment of [{language} Language](https://en.wikipedia.org/wiki/{language}_language) transcripts.

This dictionary uses the {phone_set} phone set for {language}, and was used in training the
[{language} {phone_set} acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/{language}/{phone_set}/v{version}/).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation, and each phone has
a minimum duration (by default 30ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.
"""

acoustic_docs_md_template = """
# {language_name} {phone_set} acoustic model

``````{{acoustic}} {language_name} {phone_set} acoustic model
:id: {model_name}_acoustic
:layout: {model_type}
:template: {model_type}_template
:tags: {tags}
:language: {language_name}
:phoneset: {phone_set}
:architecture: {architecture}

   ```{{include}} ../../../{model_type}/{language}/{phone_set}/v{version}/README.md
    :start-line: {start_line}
    :end-line: {end_line}
   ```

   {see_also}
``````

```{{include}} ../../../{model_type}/{language}/{phone_set}/v{version}/README.md
:start-line: {end_line}
```"""

g2p_docs_md_template = """
# {language_name} {phone_set} G2P model

``````{{g2p}} {language_name} {phone_set} G2P model
:id: {model_name}_g2p
:tags: {tags}
:layout: {model_type}
:language: {language_name}
:phoneset: {phone_set}
:architecture: {architecture}

   ```{{include}} ../../../g2p/{language}/{phone_set}/v{version}/README.md
    :start-line: {start_line}
    :end-line: {end_line}
   ```

   {see_also}
``````

```{{include}} ../../../g2p/{language}/{phone_set}/v{version}/README.md
:start-line: {end_line}
```"""

lm_docs_md_template = """
# {language_name} language model

``````{{language_model}} {language_name} language model
:id: {model_name}_language_model
:layout: {model_type}
:tags: {tags}
:language: {language_name}
:architecture: {architecture}

   ```{{include}} ../../../language_model/{language}/{source}/v{version}/README.md
    :start-line: {start_line}
    :end-line: {end_line}
   ```

   {see_also}

``````

```{{include}} ../../../language_model/{language}/{source}/v{version}/README.md
:start-line: {end_line}
```"""

dictionary_docs_md_template = """
# {language_name} {phone_set} dictionary

``````{{dictionary}} {language_name} {phone_set} dictionary
:id: {model_name}_dictionary
:tags: {tags}
:language: {language_name}
:layout: {model_type}
:template: dictionary_template
:phoneset: {phone_set}

   ```{{include}} ../../../dictionary/{language}/{phone_set}/v{version}/README.md
    :start-line: {start_line}
    :end-line: {end_line}
   ```

   {see_also}

``````

```{{include}} ../../../dictionary/{language}/{phone_set}/v{version}/README.md
:start-line: {end_line}
```"""

global_phone_ids = {
    'arabic': 'S0192',
    'bulgarian': 'S0319',
    'croatian': 'S0195',
    'czech': 'S0196',
    'french': 'S0197',
    'german': 'S0198',
    'hausa': 'S0347',
    'japanese': 'S0199',
    'korean': 'S0200',
    'mandarin': 'S0193',
    'polish': 'S0320',
    'portuguese': 'S0201',
    'russian': 'S0202',
    'spanish': 'S0203',
    'swahili': 'S0375',
    'swedish': 'S0205',
    'tamil': 'S0205',
    'thai': 'S0321',
    'turkish': 'S0206',
    'ukrainian': 'S0377',
    'vietnamese': 'S0322',
    'wu': 'S0194',
}

def generate_id(meta_data):
    return meta_data['name']+ '_'+meta_data['version'].replace('.', '_')

def generate_meta_data(model, model_type, language, version, phone_set, dialect=None):
    citation_details = {'model_name': model.name,
                        'version': version,
                        'language': language,
                        'phone_set': phone_set,
                        }
    citation_template = mfa_citation_template
    maintainer = mfa_maintainer
    license_link = f'[MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/{model_type}/{language}/{phone_set}/v{version}/LICENSE)'
    if model_type == 'acoustic':
        train_date = datetime.fromisoformat(model.meta['train_date']).date()
        citation_details['model_type'] = 'acoustic model'
        citation_details['year'] = train_date.year
        citation_details['month'] = train_date.strftime('%b')
        citation = mfa_citation_template.format(**citation_details)
        if model.source.endswith('_cv.zip'):
            citation = cv_citation
            maintainer = cv_maintainer
            license_link = "[CC-0](https://creativecommons.org/publicdomain/zero/1.0/)"
            training_data = {
                'corpus_name': f'[Common Voice 7.0](https://voice.mozilla.org/en/datasets) {language.title()}',
                'num_oovs': 0,
                'num_hours': 0,
                'num_speakers': 0,
                'num_utterances': 0,
                'average_log_likelihood': 0,
            }
        elif language in global_phone_ids:
            training_data = {
                'corpus_name': f'[GlobalPhone {language.title()}](https://catalogue.elra.info/en-us/repository/browse/ELRA-{global_phone_ids[language]}/)',
                'num_oovs': model.meta['training']['num_oovs'],
                'average_log_likelihood': model.meta['training']['average_log_likelihood'],
                'num_hours': model.meta['training']['audio_duration'] / 3600,
                'num_speakers': model.meta['training']['num_speakers'],
                'num_utterances': model.meta['training']['num_utterances'],

            }
        else:
            training_data = {
                'corpus_name': '',
                'num_oovs': model.meta['training']['num_oovs'],
                'average_log_likelihood': model.meta['training']['average_log_likelihood'],
                'num_hours': model.meta['training']['audio_duration'] / 3600,
                'num_speakers': model.meta['training']['num_speakers'],
                'num_utterances': model.meta['training']['num_utterances'],

            }
        return {
            'name': model.name,
            'language': language.title(),
            'phone_set': phone_set,
            'version': version,
            'maintainer': maintainer,
            'citation': citation,
            'license_link': license_link,
            'architecture': model.meta['architecture'],
            'training':
                {
                    'num_oovs': training_data['num_oovs'],
                    'average_log_likelihood': training_data['average_log_likelihood'],
                    'corpora': [
                        {
                            'name': training_data['corpus_name'],
                            'num_hours': training_data['num_hours'],
                            'num_speakers': training_data['num_speakers'],
                            'num_utterances': training_data['num_utterances'],
                        }
                    ]
                 },
            'features': model.meta['features'],
            'evaluation': {},
            'decode': {},
            'train_date': str(train_date),
        }
    if model_type == 'dictionary':
        train_date = datetime.today().date()
        citation_details['model_type'] = 'pronunciation dictionary'
        citation_details['year'] = train_date.year
        citation_details['month'] = train_date.strftime('%b')
        citation = citation_template.format(**citation_details)
        phone_set = phone_set.upper()
        if model.path.endswith('_cv.dict'):
            citation = cv_citation
            maintainer = cv_maintainer
            license_link = "[CC-0](https://creativecommons.org/publicdomain/zero/1.0/)"
            dictionary_phone_set = 'IPA'
        else:
            if model.path.endswith('_prosodylab.dict') or model.path.endswith('us_arpa.dict'):
                citation = prosodylab_citation
            try:
                dictionary_phone_set = montreal_forced_aligner.data.PhoneSetType[phone_set].name
            except KeyError:
                dictionary_phone_set = 'UNKNOWN'
        dictionary = montreal_forced_aligner.dictionary.pronunciation.PronunciationDictionary(model.path, phone_set_type=dictionary_phone_set)
        word_count = len(dictionary.actual_words)
        phones = ' '.join(sorted(dictionary.non_silence_phones))
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'maintainer': maintainer,
            'license_link': license_link,
            'phone_set': phone_set,
            'phones': phones,
            'word_count': word_count,
            'train_date': str(train_date),
            'version': version,
            'citation': citation,
        }
    if model_type == 'g2p':
        train_date = datetime.fromisoformat(model.meta['train_date']).date()
        citation_details['model_type'] = 'G2P model'
        citation_details['year'] = train_date.year
        citation_details['month'] = train_date.strftime('%b')
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'maintainer': maintainer,
            'license_link': license_link,
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
        citation_details['month'] = train_date.strftime('%b')
        print(model.meta['evaluation_training'])
        return {
            'name': model.name,
            'language': language.title(),
            'dialect': dialect,
            'maintainer': maintainer,
            'license_link': license_link,
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
    return {}

def extract_model_card_fields(meta_data, model_type):
    if model_type == 'acoustic':
        print(meta_data['training']['corpora'])
        corpora_details = '\n'.join([corpus_detail_template.format(**x) for x in meta_data['training']['corpora']])
        return {
                'model_name': meta_data['name'],
                'language': meta_data['language'],
                'version': meta_data['version'],
                'maintainer': meta_data['maintainer'],
                'architecture': meta_data['architecture'],
                'mfa_version': '2.0.0',
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'license_link': meta_data['license_link'],
                'corpora_details': corpora_details,
                'phone_set': meta_data['phone_set'],
                'num_oovs': meta_data['training']['num_oovs'],
                'average_log_likelihood': meta_data['training']['average_log_likelihood'],
            }
    if model_type == 'dictionary':
        return {
                'model_name': meta_data['name'],
                'language': meta_data['language'],
                'dialect': meta_data['dialect'],
                'version': meta_data['version'],
                'maintainer': meta_data['maintainer'],
                'license_link': meta_data['license_link'],
                'mfa_version': '2.0.0',
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'phone_set': meta_data['phone_set'],
                'phones': meta_data['phones'],
                'word_count': meta_data['word_count'],
            }
    if model_type == 'g2p':
        training_details = g2p_training_detail_template.format(**meta_data['training'])
        evaluation_details = g2p_evaluation_detail_template.format(**meta_data['evaluation'])
        return {
                'model_name': meta_data['name'],
                'language': meta_data['language'],
                'dialect': meta_data['dialect'],
                'architecture': meta_data['architecture'],
                'maintainer': meta_data['maintainer'],
                'version': meta_data['version'],
                'license_link': meta_data['license_link'],
                'mfa_version': '2.0.0',
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'phone_set': meta_data['phone_set'],
                'phones': meta_data['phones'],
                'training_details': training_details,
                'evaluation_details': evaluation_details,
            }
    if model_type == 'language_model':
        training_details = lm_training_detail_template.format(**meta_data['training'])
        evaluation_details = lm_evaluation_detail_template.format(**meta_data['evaluation'])
        return {
                'model_name': meta_data['name'],
                'language': meta_data['language'],
                'dialect': meta_data['dialect'],
                'architecture': meta_data['architecture'],
                'maintainer': meta_data['maintainer'],
                'version': meta_data['version'],
                'license_link': meta_data['license_link'],
                'mfa_version': '2.0.0',
                'date': meta_data['train_date'],
                'citation': meta_data['citation'],
                'training_details': training_details,
                'evaluation_details': evaluation_details,
            }

def extract_doc_card_fields(meta_data, model_type):
    print(model_type, meta_data)
    if model_type != 'language_model':
        tags = [meta_data['phone_set'].upper()]
    see_also = ''
    if 'dictionary' in meta_data:
        see_also = see_also_template.format(links=link_template.format(meta_data["dictionary"]))
    elif 'related_models' in meta_data:
        links = [link_template.format(x) for x in meta_data['related_models']]
        see_also = see_also_template.format(links='\n'.join(links))

    if model_type == 'acoustic':
        start_line = 16
        end_line = 29
        if meta_data['phone_set'] == 'cv':
            tags.append('IPA')
            start_line -= 1
            end_line -= 1
        else:
            tags.append('MFA')
        return {
            'model_name': generate_id(meta_data),
            'model_type': model_type,
            'language': meta_data['language'],
            'architecture': meta_data['architecture'],
            'language_name': meta_data['language'].title(),
            'version': meta_data['version'],
            'start_line': start_line,
            'end_line': end_line,
            'see_also': see_also,
            'tags': '; '.join(tags),
            'phone_set': meta_data['phone_set'].upper(),
        }
    if model_type == 'dictionary':
        start_line = 11
        end_line = 21
        if  meta_data['name'].endswith('_cv'):
            tags.append('IPA')
        elif meta_data['name'].endswith('_prosodylab') or meta_data['name'].endswith('us_arpa'):
            tags.append('prosodylab')
            tags.append('MFA')
        else:
            tags.append('MFA')
        return {
            'model_name': generate_id(meta_data),
            'model_type': model_type,
            'language': meta_data['language'],
            'language_name': meta_data['language'].title(),
            'version': meta_data['version'],
            'start_line': start_line,
            'end_line': end_line,
            'see_also': see_also,
            'tags': '; '.join(tags),
            'phone_set': meta_data['phone_set'].upper(),
        }
    if model_type == 'g2p':
        start_line = 17
        end_line = 29
        tags.append('MFA')
        return {
            'model_name': generate_id(meta_data),
            'model_type': model_type,
            'language': meta_data['language'],
            'architecture': meta_data['architecture'],
            'language_name': meta_data['language'].title(),
            'version': meta_data['version'],
            'start_line': start_line,
            'end_line': end_line,
            'see_also': see_also,
            'tags': '; '.join(tags),
            'phone_set': meta_data['phone_set'].upper(),
        }
    if model_type == 'language_model':
        start_line = 16
        end_line = 27
        tags = ['MFA']
        return {
            'model_name': generate_id(meta_data),
            'model_type': model_type,
            'language': meta_data['language'],
            'architecture': meta_data['architecture'],
            'language_name': meta_data['language'].title(),
            'version': meta_data['version'],
            'source': 'mfa',
            'start_line': start_line,
            'end_line': end_line,
            'see_also': see_also,
            'tags': '; '.join(tags),
        }
    return {}

model_card_templates ={
    'acoustic': {'mfa':mfa_acoustic_model_card_template, 'other': other_acoustic_model_card_template},
    'dictionary': {'mfa':mfa_dictionary_card_template, 'other': other_dictionary_card_template},
    'g2p': {'mfa':g2p_model_card_template, 'other': g2p_model_card_template},
    'language_model': {'mfa':language_model_card_template, 'other': language_model_card_template},
}
docs_card_templates ={
    'acoustic': acoustic_docs_md_template,
    'dictionary': dictionary_docs_md_template,
    'g2p': g2p_docs_md_template,
    'language_model': lm_docs_md_template,
}
model_type_names ={
    'acoustic': 'Acoustic models',
    'dictionary': 'Pronunciation dictionaries',
    'g2p': 'G2P models',
    'language_model': 'Language models',
}

meta_datas = {}

for model_type, model_class in MODEL_TYPES.items():
    if model_type == 'ivector':
        continue
    meta_datas[model_type] = {}
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
        if model_type == 'language_model':
            language = '_'.join(s[:-1])
            phone_set = 'mfa'
        elif len(s) == 1:
            language = s[0]
            phone_set = 'Unknown'
        elif len(s) == 2:
            language, phone_set = s
        else:
            language = s[0]
            phone_set = s[-1]
            dialect = ' '.join(s[1:-1])
            language = f'{language}_{dialect}'
        try:
            version = model.meta['version']
        except KeyError:
            version = montreal_forced_aligner.utils.get_mfa_version()
        if version.startswith('2.0.0'):
            version = '2.0.0'
        print(model_directory, language, phone_set, version)
        output_directory = os.path.join(model_directory, language, phone_set, f"v{version}")
        os.makedirs(output_directory, exist_ok=True)
        license_path = os.path.join(output_directory, "LICENSE")
        if phone_set != 'cv' and  not os.path.exists(license_path):
            shutil.copyfile(os.path.join(mfa_model_root, "LICENSE"), license_path)
        meta_path = os.path.join(output_directory, 'meta.json')
        if OVERWRITE_METADATA or not os.path.exists(meta_path):
            meta_data = generate_meta_data(model, model_type, language, version, phone_set)
            with open(meta_path, 'w', encoding='utf8') as f:
                json.dump(meta_data, f, indent=4)
        else:
            with open(meta_path, 'r', encoding='utf8') as f:
                meta_data = json.load(f)
        meta_datas[model_type][meta_data['name']] = meta_data

# Add links
print(meta_datas.keys())
for model_type, data in meta_datas.items():

    for model_name, meta_data in data.items():
        if model_type in {'acoustic','language_model', 'g2p'} and model_name in meta_datas['dictionary']:
            meta_data['dictionary'] = generate_id(meta_data) + '_dictionary'
        elif  model_type == 'dictionary':
            meta_data['related_models'] = []
            for t in ['acoustic', 'g2p','language_model']:
                if model_name in meta_datas[t]:
                    meta_data['related_models'].append( f'{generate_id(meta_data)}_{t}')

for model_type, data in meta_datas.items():
    model_doc_mds = []
    docs_dir = os.path.join(mfa_model_root, 'docs', 'source', model_type)
    model_directory = os.path.join(mfa_model_root, model_type)
    os.makedirs(docs_dir, exist_ok=True)
    docs_md_template = docs_card_templates[model_type]
    for model_name, meta_data in data.items():
        print(model_name, meta_data)
        if model_type != 'language_model' and meta_data['phone_set'] in {'cv'}:
            model_card_template = model_card_templates[model_type]['other']
        else:
            model_card_template = model_card_templates[model_type]['mfa']
        if model_type == 'language_model':
            language, phone_set, version = meta_data['language'], 'mfa', meta_data['version']
        else:
            language, phone_set, version = meta_data['language'], meta_data['phone_set'], meta_data['version']
        output_directory = os.path.join(model_directory, language, phone_set, f"v{version}")
        model_card_path = os.path.join(output_directory, 'README.md')
        rst_path = model_name+ '.md'
        docs_card_path = os.path.join(docs_dir, rst_path)
        model_doc_mds.append(rst_path)
        if OVERWRITE_MD or not os.path.exists(model_card_path):
            with open(model_card_path, 'w', encoding='utf8') as f:
                fields = extract_model_card_fields(meta_data, model_type)
                f.write(model_card_template.format(**fields))
        if OVERWRITE_MD or not os.path.exists(docs_card_path):
            with open(docs_card_path, 'w', encoding='utf8') as f:
                fields = extract_doc_card_fields(meta_data, model_type)
                f.write(docs_md_template.format(**fields))

    index_path = os.path.join(docs_dir, 'index.rst')
    rst_string = "   "+'\n   '.join(model_doc_mds)
    model_type_name = model_type_names[model_type]
    with open(index_path, 'w', encoding='utf8') as f:
        f.write(f"""

.. _{model_type}:

{model_type_name} models
{'='* len(model_type_name)}=======

.. needtable:: {model_type_name}
   :types: {model_type}
   :style: datatable

.. toctree::
   :hidden:

{rst_string}
""")

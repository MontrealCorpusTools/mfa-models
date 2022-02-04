
# portuguese_cv acoustic model v2.0.0

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Training data](#training-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** `Portuguese`
- **Trained date:** `2021-12-23`
- **Model type:** `Acoustic model`
- **Phone set:** `cv`
- **Model version:** `v2.0.0`
- **Architecture:** `gmm-hmm`
- **Compatible MFA version:** `v2.0.0`
- **License:** [CC-0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Citation:**
  - `@misc{Ahn_Chodroff_2022, author={Ahn, Emily and Chodroff, Eleanor}, title={VoxCommunis Corpus}, address={\url{https://osf.io/t957v}, publisher={OSF}, year={2022}, month={Jan}}`
- If you have comments or questions about this model, please contact the maintainers, or file an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download acoustic portuguese_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/acoustic-portuguese_cv-v2.0.0)

## Intended use

This model is intended for forced alignment of [Portuguese Language](https://en.wikipedia.org/wiki/Portuguese_language) transcripts.

This model uses the cv phone set for Portuguese, and was trained with the [portuguese_cv dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/dictionary/Portuguese/cv/portuguese_cv).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

As forced alignment is a relatively well-constrained problem (given accurate transcripts), this model should be applicable to a range of recording conditions and speakers.
However, please note that it was trained on read speech in low-noise environments, so as your data diverges from that,
you may run into alignment issues or need to [increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands) or see other recommendations in the [troubleshooting section below](#troubleshooting-issues).

Please note as well that MFA does not use state-of-the-art models for forced alignment.
You may get better performance (especially on speech-to-text tasks) using other frameworks like [Coqui](https://coqui.ai/).

## Training data

This model was trained on the following corpora:


* [Common Voice 7.0](https://voice.mozilla.org/en/datasets) Portuguese:
  * **Hours:** `84.00`
  * **Speakers:** `1,638`
  * **Utterances:** `7,115`

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


# Japanese MFA acoustic model v2.0.1a

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/acoustic/japanese_mfa.html)

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)
- [Training data](#training-data)
- [Evaluation data](#evaluation-data)

## Model details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Japanese](https://en.wikipedia.org/wiki/Japanese_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#japanese)
- **Model type:** `Acoustic`
- **Features:** `MFCC`
- **Architecture:** `gmm-hmm`
- **Model version:** `v2.0.1a`
- **Trained date:** `2023-01-19`
- **Compatible MFA version:** `v2.1.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/acoustic/japanese/mfa/v2.0.1a/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_japanese_mfa_acoustic_2023,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Japanese MFA acoustic model v2.0.1a},
	address={\url{https://mfa-models.readthedocs.io/acoustic/Japanese/Japanese MFA acoustic model v2_0_1a.html}},
	year={2023},
	month={Jan},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Japanese+MFA+acoustic+model+v2.0.1a) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download acoustic japanese_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/acoustic-japanese_mfa-v2.0.1a).

## Intended use

This model is intended for forced alignment of [Japanese](https://en.wikipedia.org/wiki/Japanese_language) transcripts.

This model uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#japanese) phone set for Japanese, and was trained with the pronunciation dictionaries above. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

As forced alignment is a relatively well-constrained problem (given accurate transcripts), this model should be applicable to a range of recording conditions and speakers. However, please note that it was trained on read speech in low-noise environments, so as your data diverges from that, you may run into alignment issues or need to [increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands) or see other recommendations in the [troubleshooting section below](#troubleshooting-issues).

Please note as well that MFA does not use state-of-the-art ASR models for forced alignment. You may get better performance (especially on speech-to-text tasks) using other frameworks like [Coqui](https://coqui.ai/).

## Metrics

Acoustic models are typically generated as one component of a larger ASR system where the metric is word error rate (WER). For forced alignment, there is typically not the same sort of gold standard measure for most languages.

As a rough approximation of the acoustic model quality, we evaluated it against the corpus it was trained on alongside a language model trained from the same data.  Key caveat here is that this is not a typical WER measure on held out data, so it should not be taken as a hard measure of how well an acoustic model will generalize to your data, but rather is more of a sanity check that the training data quality was sufficiently high.

Using the pronunciation dictionaries and language models above:

- **WER:** `0%`
- **CER:** `0%`

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For STT models, it is often the case that transcription accuracy is better for men than it is for women. If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.


## Troubleshooting issues

Machine learning models (like this acoustic model) perform best on data that is similar to the data on which they were trained.

The primary sources of variability in forced alignment will be the applicability of the pronunciation dictionary and how similar the speech, demographics, and recording conditions are. If you encounter issues in alignment, there are couple of avenues to improve performance:

1. [Increase the beam size of MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/configuration/#configuring-specific-commands)

   * MFA defaults to a narrow beam to ensure quick alignment and also as a way to detect potential issues in your dataset, but depending on your data, you might benefit from boosting the beam to 100 or higher.

2. Add pronunciations to the pronunciation dictionary

   * This model was trained a particular dialect/style, and so adding pronunciations more representative of the variety spoken in your dataset will help alignment.

3. Check the quality of your data

   * MFA includes a [validator utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/data_validation.html), which aims to detect issues in the dataset.
   * Use MFA's [anchor utility](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/anchor.html) to visually inspect your data as MFA sees it and correct issues in transcription or OOV items.

4. Adapt the model to your data

   * MFA has an [adaptation command](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/adapt_acoustic_model.html) to adapt some of the model to your data based on an initial alignment, and then run another alignment with the adapted model.

## Training data

This model was trained on the following corpora:



   * [Common Voice Japanese](../../../../corpus/japanese/common_voice_japanese/12.0/README.md):
     * **Hours:** `71.54`
     * **Speakers:** `1,364`
     * **Utterances:** `56,631`

   * [GlobalPhone Japanese](../../../../corpus/japanese/globalphone_japanese/3.1/README.md):
     * **Hours:** `33.88`
     * **Speakers:** `144`
     * **Utterances:** `13,103`

   * [Microsoft Speech Language Translation Japanese](../../../../corpus/japanese/microsoft_speech_language_translation_japanese/README.md):
     * **Hours:** `9.85`
     * **Speakers:** `112`
     * **Utterances:** `7,338`

   * [Japanese Versatile Speech](../../../../corpus/japanese/japanese_versatile_speech/README.md):
     * **Hours:** `30.25`
     * **Speakers:** `100`
     * **Utterances:** `14,994`

   * [TEDxJP-10K](../../../../corpus/japanese/tedxjp_10k/1.1/README.md):
     * **Hours:** `8.85`
     * **Speakers:** `271`
     * **Utterances:** `9,962`

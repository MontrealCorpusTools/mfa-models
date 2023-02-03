
# English MFA ivector extractor v2.1.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/ivector/english_mfa.html)

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Ethical considerations](#ethical-considerations)
- [Training data](#training-data)

## Model details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [English](https://en.wikipedia.org/wiki/English_language)
- **Model type:** `Ivector extractor`
- **Features:** `MFCC`
- **Architecture:** `ivector`
- **Model version:** `v2.1.0`
- **Trained date:** `2023-01-04`
- **Compatible MFA version:** `v2.1.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/ivector/english//v2.1.0/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_english_mfa_ivector_2023,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={English MFA ivector extractor v2.1.0},
	address={\url{https://mfa-models.readthedocs.io/ivector/English/English MFA ivector extractor v2_1_0.html}},
	year={2023},
	month={Jan},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=English+MFA+ivector+extractor+v2.1.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download ivector english_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/ivector-english_mfa-v2.1.0).

## Intended use

This model is intended for speaker diarization and clustering.

## Performance Factors

As ivector extractors are trained on a large amount of data and without reference to language-specific resources, they **may** be useful outside of the specific language variety being trained, however, differences in the languages may impact performance. Particularly sociolinguistic aspects related to identity presentation, the linguistic status voice quality (breathy, creaky modal), and non-linguistic factors like recording conditions and microphone response may affect diarization performance across languages.

## Metrics

Speaker diarization systems are evaluated through Equal Error Rate (EER), the error when false accept rate is equal to the false rejection rate.

- **EER:** `0%`

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For ivector extraction models, diarization of male speakers generally has better performance than diarization of female speakers, even with equal amounts of training data.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

## Training data

This model was trained on the following corpora:



   * [Common Voice English](../../../../corpus/english/common_voice_english/8.0/README.md):
     * **Hours:** `2479.95`
     * **Speakers:** `74,811`
     * **Utterances:** `1,781,717`

   * [LibriSpeech English](../../../../corpus/english/librispeech_english/README.md):
     * **Hours:** `982.10`
     * **Speakers:** `2,484`
     * **Utterances:** `292,367`

   * [Corpus of Regional African American Language](../../../../corpus/english/corpus_of_regional_african_american_language/2021.07/README.md):
     * **Hours:** `124.31`
     * **Speakers:** `193`
     * **Utterances:** `236,792`

   * [Google Nigerian English](../../../../corpus/english/google_nigerian_english/README.md):
     * **Hours:** `5.77`
     * **Speakers:** `31`
     * **Utterances:** `3,359`

   * [Google UK and Ireland English](../../../../corpus/english/google_uk_and_ireland_english/README.md):
     * **Hours:** `31.29`
     * **Speakers:** `120`
     * **Utterances:** `17,877`

   * [NCHLT English](../../../../corpus/english/nchlt_english/README.md):
     * **Hours:** `56.43`
     * **Speakers:** `210`
     * **Utterances:** `77,412`

   * [ARU English corpus](../../../../corpus/english/aru_english_corpus/README.md):
     * **Hours:** `7.13`
     * **Speakers:** `12`
     * **Utterances:** `8,640`

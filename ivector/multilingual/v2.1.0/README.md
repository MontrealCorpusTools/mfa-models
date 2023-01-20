
# Multilingual MFA ivector extractor v2.1.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/acoustic/ivector_mfa.html)

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
- **Language:** Multilingual
- **Model type:** `Ivector extractor`
- **Features:** `MFCC`
- **Architecture:** `ivector`
- **Model version:** `v2.1.0`
- **Trained date:** `2023-01-04`
- **Compatible MFA version:** `v2.1.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/ivector/multilingual//v2.1.0/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_ivector_mfa_ivector_2023,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Multilingual MFA ivector extractor v2.1.0},
	address={\url{https://mfa-models.readthedocs.io/ivector/Multilingual/Multilingual MFA ivector extractor v2_1_0.html}},
	year={2023},
	month={Jan},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Multilingual+MFA+ivector+extractor+v2.1.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download ivector ivector_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/ivector-ivector_mfa-v2.1.0).

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

   * [Common Voice Czech](../../../../corpus/czech/common_voice_czech/9.0/README.md):
     * **Hours:** `66.33`
     * **Speakers:** `523`
     * **Utterances:** `55,391`

   * [GlobalPhone Czech](../../../../corpus/czech/globalphone_czech/3.1/README.md):
     * **Hours:** `31.67`
     * **Speakers:** `101`
     * **Utterances:** `12,322`

   * [Large Corpus of Czech Parliament Plenary Hearings](../../../../corpus/czech/large_corpus_of_czech_parliament_plenary_hearings/README.md):
     * **Hours:** `450.95`
     * **Speakers:** `84`
     * **Utterances:** `194,181`

   * [Czech Parliament Meetings](../../../../corpus/czech/czech_parliament_meetings/README.md):
     * **Hours:** `88.81`
     * **Speakers:** `67`
     * **Utterances:** `51,494`

   * [Common Voice Hausa](../../../../corpus/hausa/common_voice_hausa/9.0/README.md):
     * **Hours:** `10.47`
     * **Speakers:** `23`
     * **Utterances:** `8,699`

   * [GlobalPhone Hausa](../../../../corpus/hausa/globalphone_hausa/3.1/README.md):
     * **Hours:** `8.74`
     * **Speakers:** `103`
     * **Utterances:** `7,895`

   * [Common Voice Swahili](../../../../corpus/swahili/common_voice_swahili/9.0/README.md):
     * **Hours:** `702.69`
     * **Speakers:** `570`
     * **Utterances:** `473,364`

   * [ALFFA Swahili](../../../../corpus/swahili/alffa_swahili/README.md):
     * **Hours:** `11.75`
     * **Speakers:** `36`
     * **Utterances:** `12,171`

   * [GlobalPhone Swahili](../../../../corpus/swahili/globalphone_swahili/3.1/README.md):
     * **Hours:** `11.12`
     * **Speakers:** `70`
     * **Utterances:** `7,728`

   * [Common Voice Thai](../../../../corpus/thai/common_voice_thai/9.0/README.md):
     * **Hours:** `158.88`
     * **Speakers:** `4,656`
     * **Utterances:** `137,401`

   * [GlobalPhone Thai](../../../../corpus/thai/globalphone_thai/3.1/README.md):
     * **Hours:** `28.17`
     * **Speakers:** `98`
     * **Utterances:** `14,039`

   * [Common Voice Vietnamese](../../../../corpus/vietnamese/common_voice_vietnamese/9.0/README.md):
     * **Hours:** `16.80`
     * **Speakers:** `211`
     * **Utterances:** `15,314`

   * [VIVOS](../../../../corpus/vietnamese/vivos/README.md):
     * **Hours:** `15.67`
     * **Speakers:** `65`
     * **Utterances:** `12,420`

   * [GlobalPhone Vietnamese](../../../../corpus/vietnamese/globalphone_vietnamese/3.1/README.md):
     * **Hours:** `19.72`
     * **Speakers:** `129`
     * **Utterances:** `18,842`

   * [Common Voice Japanese](../../../../corpus/japanese/common_voice_japanese/9.0/README.md):
     * **Hours:** `45.83`
     * **Speakers:** `574`
     * **Utterances:** `34,792`

   * [GlobalPhone Japanese](../../../../corpus/japanese/globalphone_japanese/3.1/README.md):
     * **Hours:** `33.91`
     * **Speakers:** `144`
     * **Utterances:** `13,067`

   * [Microsoft Speech Language Translation Japanese](../../../../corpus/japanese/microsoft_speech_language_translation_japanese/README.md):
     * **Hours:** `9.86`
     * **Speakers:** `112`
     * **Utterances:** `7,339`

   * [Japanese Versatile Speech](../../../../corpus/japanese/japanese_versatile_speech/README.md):
     * **Hours:** `26.37`
     * **Speakers:** `100`
     * **Utterances:** `13,007`

   * [TEDxJP-10K](../../../../corpus/japanese/tedxjp_10k/1.1/README.md):
     * **Hours:** `0.00`
     * **Speakers:** `0`
     * **Utterances:** `0`

   * [Common Voice Chinese (China)](../../../../corpus/mandarin/common_voice_chinese_china/9.0/README.md):
     * **Hours:** `84.67`
     * **Speakers:** `3,577`
     * **Utterances:** `56,862`

   * [Common Voice Chinese (Taiwan)](../../../../corpus/mandarin/common_voice_chinese_taiwan/9.0/README.md):
     * **Hours:** `100.71`
     * **Speakers:** `1,965`
     * **Utterances:** `112,047`

   * [AI-DataTang Corpus](../../../../corpus/mandarin/ai_datatang_corpus/README.md):
     * **Hours:** `200.38`
     * **Speakers:** `600`
     * **Utterances:** `237,265`

   * [AISHELL-3](../../../../corpus/mandarin/aishell_3/README.md):
     * **Hours:** `160.88`
     * **Speakers:** `360`
     * **Utterances:** `127,274`

   * [THCHS-30](../../../../corpus/mandarin/thchs_30/README.md):
     * **Hours:** `34.16`
     * **Speakers:** `60`
     * **Utterances:** `13,388`

   * [GlobalPhone Chinese-Mandarin](../../../../corpus/mandarin/globalphone_chinese_mandarin/3.1/README.md):
     * **Hours:** `31.16`
     * **Speakers:** `132`
     * **Utterances:** `10,225`

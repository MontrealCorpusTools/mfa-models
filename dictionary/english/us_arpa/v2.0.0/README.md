
# English (US) ARPA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/english_us_arpa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [English](https://en.wikipedia.org/wiki/English_language)
- **Dialect:** [General American English](https://en.wikipedia.org/wiki/General_American_English)
- **Phone set:** [ARPA](https://en.wikipedia.org/wiki/ARPABET)
- **Number of words:** `199,858`
- **Phones:** `AA0 AA1 AA2 AE0 AE1 AE2 AH0 AH1 AH2 AO0 AO1 AO2 AW0 AW1 AW2 AY0 AY1 AY2 B CH D DH EH0 EH1 EH2 ER0 ER1 ER2 EY0 EY1 EY2 F G HH IH0 IH1 IH2 IY0 IY1 IY2 JH K L M N NG OW0 OW1 OW2 OY0 OY1 OY2 P R S SH T TH UH0 UH1 UH2 UW0 UW1 UW2 V W Y Z ZH`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/english/us_arpa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@article{gorman2011prosodylab,
	author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael},
	title={Prosodylab-aligner: A tool for forced alignment of laboratory speech},
	journal={Canadian Acoustics},
	volume={39},
	number={3},
	pages={192--193},
	year={2011}
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=English+US+ARPA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary english_us_arpa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-english_us_arpa-v2.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/english/us_arpa/english_us_arpa.dict).

## Intended use

This dictionary is intended for forced alignment of [English](https://en.wikipedia.org/wiki/English_language) transcripts.

This dictionary uses the [ARPA](https://en.wikipedia.org/wiki/ARPABET) phone set for English, and was used in training the English [ARPA](https://en.wikipedia.org/wiki/ARPABET) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

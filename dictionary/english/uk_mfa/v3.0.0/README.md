# English (UK) MFA dictionary v3.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/english_uk_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [English](https://en.wikipedia.org/wiki/English_language)
- **Dialect:** [British English](https://en.wikipedia.org/wiki/British_English)
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#english)
- **Number of words:** `74,993`
- **Phones:** `a aj aw b bʲ c cʰ cʷ d dʒ dʲ d̪ e ej f fʲ fʷ h i iː j k kʰ kʷ l m mʲ m̩ n n̩ p pʰ pʲ pʷ s t tʃ tʰ tʲ tʷ t̪ v vʲ vʷ w z ç ð ŋ ɐ ɑ ɑː ɒ ɒː ɔj ə əw ɛ ɛː ɜ ɜː ɟ ɟʷ ɡ ɡʷ ɪ ɫ ɫ̩ ɱ ɲ ɹ ʃ ʉ ʉː ʊ ʎ ʒ ʔ θ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/english/uk_mfa/v3.0.0/LICENSE)
- **Compatible MFA version:** `v3.0.0`
- **Citation:**

```bibtex
@techreport{mfa_english_uk_mfa_dictionary_2024,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={English (UK) MFA dictionary v3.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/English/English (UK) MFA dictionary v3_0_0.html}},
	year={2024},
	month={Feb},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=English+UK+MFA+dictionary+v3.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary english_uk_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-english_uk_mfa-v3.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/english/mfa/English (UK) MFA dictionary v3_0_0.dict).

## Intended use

This dictionary is intended for forced alignment of [English](https://en.wikipedia.org/wiki/English_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#english) phone set for English, and was used in training the English [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#english) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

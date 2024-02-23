# Korean MFA dictionary v3.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/korean_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Korean](https://en.wikipedia.org/wiki/Korean_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean)
- **Number of words:** `17,968`
- **Phones:** `b bʲ bʷ c cʰ cʰː c͈ d dʑ dʑʷ dʲ dʷ e eː h i iː j k kʰ kʰː kʷ kʷː k̚ k͈ k͈ʷ k͈ː m mʲ mʲː mː n nː o oː p pʰ pʰː pʲ pʲː pʷ p̚ p͈ p͈ʲ s sʰ sʰː sʷ sː s͈ s͈ʷ t tɕ tɕʰ tɕʰː tɕʷ tɕʷː tɕː tɕ͈ tɕ͈ʷ tɕ͈ː tʰ tʰː tʲ tʷ tʷː t̚ t͈ t͈ʲ t͈ː u uː w x ç ŋ ɐ ɕʰ ɕ͈ ɛ ɛː ɟ ɡ ɡʷ ɣ ɥ ɦ ɨ ɨː ɭ ɭː ɰ ɲ ɸ ɸʷ ɾ ɾʲ ɾʷ ʌ ʌː ʎ ʎː ʝ β βʷ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/korean/mfa/v3.0.0/LICENSE)
- **Compatible MFA version:** `v3.0.0`
- **Citation:**

```bibtex
@techreport{mfa_korean_mfa_dictionary_2024,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Korean MFA dictionary v3.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Korean/Korean MFA dictionary v3_0_0.html}},
	year={2024},
	month={Feb},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Korean+MFA+dictionary+v3.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary korean_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-korean_mfa-v3.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/korean/mfa/Korean MFA dictionary v3_0_0.dict).

## Intended use

This dictionary is intended for forced alignment of [Korean](https://en.wikipedia.org/wiki/Korean_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean) phone set for Korean, and was used in training the Korean [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

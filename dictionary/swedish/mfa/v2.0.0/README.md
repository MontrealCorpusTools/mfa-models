
# Swedish MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/swedish_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Swedish](https://en.wikipedia.org/wiki/Swedish_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish)
- **Number of words:** `59,521`
- **Phones:** `a a˥˧ a˥˩ a˧˩ a˩ b d̪ eː eː˥˧ eː˥˩ eː˧˩ eː˩ f h iː iː˥˧ iː˥˩ iː˧˩ j k kʰ l m n̪ oː oː˥˧ oː˥˩ oː˧˩ oː˩ p pʰ r s̪ t̪ t̪ʰ uː uː˥˧ uː˥˩ uː˧˩ yː yː˥˧ yː˥˩ yː˧˩ yː˩ øː øː˥˧ øː˥˩ øː˧˩ øː˩ ŋ œ œ˥˩ œ˧˩ ɑː ɑː˥˧ ɑː˥˩ ɑː˧˩ ɑː˩ ɔ ɔ˥˧ ɔ˥˩ ɔ˧˩ ɔ˩ ɕ ɖ ɛ ɛː ɛː˥˧ ɛː˥˩ ɛː˧˩ ɛ˥˧ ɛ˥˩ ɛ˧˩ ɛ˩ ɡ ɧ ɪ ɪ˥˧ ɪ˥˩ ɪ˧˩ ɪ˩ ɭ ɳ ɵ ɵ˥˧ ɵ˥˩ ɵ˧˩ ɵ˩ ʂ ʈ ʈʰ ʉː ʉː˥˧ ʉː˥˩ ʉː˧˩ ʊ ʊ˥˩ ʊ˧˩ ʊ˩ ʋ ʏ ʏ˥˧ ʏ˥˩ ʏ˧˩ ʏ˩`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/swedish/mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{mfa_swedish_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Swedish MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Swedish/Swedish MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Swedish+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary swedish_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-swedish_mfa-v2.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/swedish/mfa/swedish_mfa.dict).

## Intended use

This dictionary is intended for forced alignment of [Swedish](https://en.wikipedia.org/wiki/Swedish_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish) phone set for Swedish, and was used in training the Swedish [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

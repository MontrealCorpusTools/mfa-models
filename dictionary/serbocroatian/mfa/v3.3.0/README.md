# Serbocroatian MFA dictionary v3.3.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/serbocroatian_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Serbo-Croatian](https://en.wikipedia.org/wiki/Serbo-Croatian)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#serbocroatian)
- **Number of words:** `69,307`
- **Phones:** `a aː aː˦˨ aː˨˦ a˦˨ a˨˦ b d dʑ dʒ e eː eː˦˨ eː˨˦ e˦˨ e˨˦ f i iː iː˦˨ iː˨˦ i˦˨ i˨˦ j k l m n o oː oː˦˨ oː˨˦ o˦˨ o˨˦ p r rː r̩ r̩ː˦˨ r̩ː˨˦ r̩˦˨ r̩˨˦ s t ts tɕ tʃ u uː uː˦˨ uː˨˦ u˦˨ u˨˦ v x z ɡ ɲ ʃ ʎ ʒ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/serbocroatian/mfa/v3.3.0/LICENSE)
- **Compatible MFA version:** `v3.3.0`
- **Citation:**

```bibtex
@techreport{mfa_serbocroatian_mfa_dictionary_2025,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Serbocroatian MFA dictionary v3.3.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Serbocroatian/Serbocroatian MFA dictionary v3_3_0.html}},
	year={2025},
	month={Oct},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Serbocroatian+MFA+dictionary+v3.3.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary serbocroatian_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-serbocroatian_mfa-v3.3.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/serbocroatian/mfa/Serbocroatian MFA dictionary v3_3_0.dict).

## Intended use

This dictionary is intended for forced alignment of [Serbo-Croatian](https://en.wikipedia.org/wiki/Serbo-Croatian) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#serbocroatian) phone set for Serbocroatian, and was used in training the Serbocroatian [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#serbocroatian) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.


# Vietnamese (Ho Chi Minh City) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/vietnamese_ho_chi_minh_city_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese)
- **Number of words:** `4,810`
- **Phones:** `aː˦˥ aː˨˨ aː˨˩ aː˨˩˦ aː˨˩˨ a˦˥ a˨˨ a˨˩ a˨˩˦ a˨˩˨ c eː˦˥ eː˨˨ eː˨˩ eː˨˩˦ eː˨˩˨ f h iə˦˥ iə˨˨ iə˨˩ iə˨˩˦ iə˨˩˨ iː˦˥ iː˨˨ iː˨˩ iː˨˩˦ iː˨˩˨ i˦˥ i˨˨ i˨˩ i˨˩˦ i˨˩˨ j k kp l m n oː˦˥ oː˨˨ oː˨˩ oː˨˩˦ oː˨˩˨ o˦˥ o˨˨ o˨˩ o˨˩˦ o˨˩˨ p r s t tʰ uə˦˥ uə˨˨ uə˨˩ uə˨˩˦ uə˨˩˨ uː˦˥ uː˨˨ uː˨˩ uː˨˩˦ uː˨˩˨ u˦˥ u˨˨ u˨˩ u˨˩˦ u˨˩˨ v w x ŋ ŋm ɓ ɔː˦˥ ɔː˨˨ ɔː˨˩ ɔː˨˩˦ ɔː˨˩˨ ɔ˦˥ ɔ˨˨ ɔ˨˩ ɔ˨˩˦ ɔ˨˩˨ ɗ əː˦˥ əː˨˨ əː˨˩ əː˨˩˦ əː˨˩˨ ə˦˥ ə˨˨ ə˨˩ ə˨˩˦ ə˨˩˨ ɛː˦˥ ɛː˨˨ ɛː˨˩ ɛː˨˩˦ ɛː˨˩˨ ɡ ɨə˦˥ ɨə˨˨ ɨə˨˩ ɨə˨˩˦ ɨə˨˩˨ ɨː˦˥ ɨː˨˨ ɨː˨˩ ɨː˨˩˦ ɨː˨˩˨ ɨ˦˥ ɨ˨˨ ɨ˨˩ ɨ˨˩˦ ɨ˨˩˨ ɲ ʈ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/vietnamese/ho_chi_minh_city_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{mfa_vietnamese_ho_chi_minh_city_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Vietnamese (Ho Chi Minh City) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Vietnamese/Vietnamese (Ho Chi Minh City) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Vietnamese+Ho+Chi+Minh+City+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary vietnamese_ho_chi_minh_city_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_ho_chi_minh_city_mfa-v2.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/vietnamese/ho_chi_minh_city_mfa/vietnamese_ho_chi_minh_city_mfa.dict).

## Intended use

This dictionary is intended for forced alignment of [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) phone set for Vietnamese, and was used in training the Vietnamese [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

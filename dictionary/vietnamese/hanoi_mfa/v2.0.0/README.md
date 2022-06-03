
# Vietnamese (Hanoi) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/vietnamese_hanoi_mfa.html)

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
- **Phones:** `aː˦˥ aː˨ˀ˥ aː˨˦ aː˨˨ aː˨˩ aː˨˩ˀ aː˨˩˨ a˦˥ a˨ˀ˥ a˨˦ a˨˨ a˨˩ a˨˩ˀ a˨˩˨ c eː˦˥ eː˨ˀ˥ eː˨˦ eː˨˨ eː˨˩ eː˨˩ˀ eː˨˩˨ e˦˥ e˨ˀ˥ e˨˨ e˨˩ e˨˩ˀ e˨˩˨ f h iə˦˥ iə˨ˀ˥ iə˨˦ iə˨˨ iə˨˩ iə˨˩ˀ iə˨˩˨ iː˦˥ iː˨ˀ˥ iː˨˦ iː˨˨ iː˨˩ iː˨˩ˀ iː˨˩˨ i˦˥ i˨ˀ˥ i˨˦ i˨˨ i˨˩ i˨˩ˀ i˨˩˨ j k kp l m n oː˦˥ oː˨ˀ˥ oː˨˦ oː˨˨ oː˨˩ oː˨˩ˀ oː˨˩˨ o˦˥ o˨ˀ˥ o˨˦ o˨˨ o˨˩ o˨˩ˀ o˨˩˨ p s t tɕ tʰ uə˦˥ uə˨ˀ˥ uə˨˦ uə˨˨ uə˨˩ uə˨˩ˀ uə˨˩˨ uː˦˥ uː˨ˀ˥ uː˨˦ uː˨˨ uː˨˩ uː˨˩ˀ uː˨˩˨ u˦˥ u˨ˀ˥ u˨˦ u˨˨ u˨˩ u˨˩ˀ u˨˩˨ v w x z ŋ ŋm ɓ ɔː˦˥ ɔː˨ˀ˥ ɔː˨˦ ɔː˨˨ ɔː˨˩ ɔː˨˩ˀ ɔː˨˩˨ ɔ˦˥ ɔ˨ˀ˥ ɔ˨˦ ɔ˨˨ ɔ˨˩ ɔ˨˩ˀ ɔ˨˩˨ ɗ əː˦˥ əː˨ˀ˥ əː˨˦ əː˨˨ əː˨˩ əː˨˩ˀ əː˨˩˨ ə˦˥ ə˨ˀ˥ ə˨˦ ə˨˨ ə˨˩ ə˨˩ˀ ə˨˩˨ ɛː˦˥ ɛː˨ˀ˥ ɛː˨˦ ɛː˨˨ ɛː˨˩ ɛː˨˩ˀ ɛː˨˩˨ ɣ ɨə˦˥ ɨə˨ˀ˥ ɨə˨˦ ɨə˨˨ ɨə˨˩ ɨə˨˩ˀ ɨə˨˩˨ ɨː˨ˀ˥ ɨː˨˦ ɨː˨˨ ɨː˨˩ˀ ɨː˨˩˨ ɨ˦˥ ɨ˨ˀ˥ ɨ˨˦ ɨ˨˨ ɨ˨˩ ɨ˨˩ˀ ɨ˨˩˨ ɲ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/vietnamese/hanoi_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{mfa_vietnamese_hanoi_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Vietnamese (Hanoi) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Vietnamese/Vietnamese (Hanoi) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Vietnamese+Hanoi+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_hanoi_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_hanoi_mfa-v2.0.0).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/vietnamese/hanoi_mfa/vietnamese_hanoi_mfa.dict).

## Intended use

This dictionary is intended for forced alignment of [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) phone set for Vietnamese, and was used in training the Vietnamese [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

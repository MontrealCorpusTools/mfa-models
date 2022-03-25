
# Vietnamese (Hue) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/vietnamese_hue_mfa.html)

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
- **Number of words:** `4,811`
- **Phones:** `aː˦˥ aː˦˨ aː˨ˀ˦ aː˨˥ aː˨˨ˀ aː˨˩ a˦˥ a˦˨ a˨ˀ˦ a˨˥ a˨˨ˀ a˨˩ c eː˦˥ eː˦˨ eː˨ˀ˦ eː˨˥ eː˨˨ˀ eː˨˩ f h iə˦˨ iə˨ˀ˦ iə˨˥ iə˨˨ˀ iə˨˩ iː˦˥ iː˦˨ iː˨ˀ˦ iː˨˥ iː˨˨ˀ iː˨˩ i˦˥ i˦˨ i˨ˀ˦ i˨˥ i˨˨ˀ i˨˩ j k kp l m n oː˦˥ oː˦˨ oː˨ˀ˦ oː˨˥ oː˨˨ˀ oː˨˩ o˦˥ o˦˨ o˨ˀ˦ o˨˥ o˨˨ˀ o˨˩ p r s t tʰ uə˦˨ uə˨ˀ˦ uə˨˥ uə˨˨ˀ uə˨˩ uː˦˥ uː˦˨ uː˨ˀ˦ uː˨˥ uː˨˨ˀ uː˨˩ u˦˥ u˦˨ u˨ˀ˦ u˨˥ u˨˨ˀ u˨˩ v w x ŋ ŋm ɓ ɔː˦˥ ɔː˦˨ ɔː˨ˀ˦ ɔː˨˥ ɔː˨˨ˀ ɔː˨˩ ɔ˦˥ ɔ˦˨ ɔ˨ˀ˦ ɔ˨˥ ɔ˨˨ˀ ɔ˨˩ ɗ əː˦˥ əː˦˨ əː˨ˀ˦ əː˨˥ əː˨˨ˀ əː˨˩ ə˦˥ ə˦˨ ə˨ˀ˦ ə˨˥ ə˨˨ˀ ə˨˩ ɛː˦˥ ɛː˦˨ ɛː˨ˀ˦ ɛː˨˥ ɛː˨˨ˀ ɛː˨˩ ɡ ɨə˦˨ ɨə˨ˀ˦ ɨə˨˥ ɨə˨˨ˀ ɨə˨˩ ɨː˦˥ ɨː˦˨ ɨː˨ˀ˦ ɨː˨˥ ɨː˨˨ˀ ɨː˨˩ ɨ˦˥ ɨ˦˨ ɨ˨ˀ˦ ɨ˨˥ ɨ˨˨ˀ ɨ˨˩ ɲ ʈ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/vietnamese/hue_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_vietnamese_hue_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Vietnamese (Hue) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Vietnamese/Vietnamese (Hue) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Vietnamese+Hue+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_hue_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_hue_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) phone set for Vietnamese, and was used in training the Vietnamese [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#vietnamese) acoustic model.
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.
The most impactful improvements will generally be felt when adding reduced variants that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has
a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

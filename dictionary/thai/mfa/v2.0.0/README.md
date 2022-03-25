
# Thai MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/thai_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Thai](https://en.wikipedia.org/wiki/Thai_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#thai)
- **Number of words:** `29,860`
- **Phones:** `aː˥˩ aː˦˥ aː˧ aː˨˩ aː˩˩˦ a˥˩ a˦˥ a˧ a˨˩ a˩˩˦ b d eː˥˩ eː˦˥ eː˧ eː˨˩ eː˩˩˦ e˥˩ e˦˥ e˧ e˨˩ e˩˩˦ f h ia˥˩ ia˦˥ ia˧ ia˨˩ ia˩˩˦ iː˥˩ iː˦˥ iː˧ iː˨˩ iː˩˩˦ i˥˩ i˦˥ i˧ i˨˩ i˩˩˦ j k kʰ k̚ l m n oː˥˩ oː˦˥ oː˧ oː˨˩ oː˩˩˦ o˥˩ o˦˥ o˧ o˨˩ o˩˩˦ p pʰ p̚ r s t tɕ tɕʰ tʰ t̚ ua˥˩ ua˦˥ ua˧ ua˨˩ ua˩˩˦ uː˥˩ uː˦˥ uː˧ uː˨˩ uː˩˩˦ u˥˩ u˦˥ u˧ u˨˩ u˩˩˦ w ŋ ɔː˥˩ ɔː˦˥ ɔː˧ ɔː˨˩ ɔː˩˩˦ ɔ˥˩ ɔ˦˥ ɔ˧ ɔ˨˩ ɔ˩˩˦ ɛː˥˩ ɛː˦˥ ɛː˧ ɛː˨˩ ɛː˩˩˦ ɛ˥˩ ɛ˦˥ ɛ˧ ɛ˨˩ ɛ˩˩˦ ɤː˥˩ ɤː˦˥ ɤː˧ ɤː˨˩ ɤː˩˩˦ ɤ˥˩ ɤ˦˥ ɤ˧ ɤ˨˩ ɤ˩˩˦ ɯa˥˩ ɯa˦˥ ɯa˧ ɯa˨˩ ɯa˩˩˦ ɯː˥˩ ɯː˦˥ ɯː˧ ɯː˨˩ ɯː˩˩˦ ɯ˥˩ ɯ˦˥ ɯ˧ ɯ˨˩ ɯ˩˩˦ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/thai/mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_thai_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Thai MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Thai/Thai MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Thai+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary thai_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-thai_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Thai](https://en.wikipedia.org/wiki/Thai_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#thai) phone set for Thai, and was used in training the Thai [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#thai) acoustic model.
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.
The most impactful improvements will generally be seen when adding reduced variants that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has
a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.


# Mandarin (China) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/mandarin_china_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese)
- **Dialect:** [Standard Mandarin Chinese](https://en.wikipedia.org/wiki/Standard_Chinese)
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin)
- **Number of words:** `119,455`
- **Phones:** `ai˥˥ ai˥˩ ai˦ ai˧˥ ai˨ ai˨˩˦ ai˩ au˥˥ au˥˩ au˦ au˧˥ au˨ au˨˩˦ au˩ a˥˥ a˥˩ a˦ a˧˥ a˨ a˨˩˦ a˩ ei˥˥ ei˥˩ ei˦ ei˧˥ ei˨ ei˨˩˦ ei˩ e˥˥ e˥˩ e˦ e˧˥ e˨ e˨˩˦ e˩ f i˥˥ i˥˩ i˦ i˧˥ i˨ i˨˩˦ i˩ j k kʰ l m n ou˥˥ ou˥˩ ou˦ ou˧˥ ou˨ ou˨˩˦ ou˩ o˥˥ o˥˩ o˦ o˧˥ o˨ o˨˩˦ o˩ p pʰ s t ts tsʰ tɕ tɕʰ tʰ u˥˥ u˥˩ u˦ u˧˥ u˨ u˨˩˦ u˩ w x y˥˥ y˥˩ y˦ y˧˥ y˨ y˨˩˦ y˩ z̩˥˥ z̩˥˩ z̩˦ z̩˧˥ z̩˨ z̩˨˩˦ z̩˩ ŋ ŋ̍˧˥ ɕ ə˥˥ ə˥˩ ə˦ ə˧˥ ə˨ ə˨˩˦ ə˩ ɥ ɻ ʂ ʈʂ ʈʂʰ ʐ ʐ̩˥˥ ʐ̩˥˩ ʐ̩˦ ʐ̩˧˥ ʐ̩˨ ʐ̩˨˩˦ ʐ̩˩ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/mandarin/china_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_mandarin_china_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Mandarin (China) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Mandarin/Mandarin (China) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Mandarin+China+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary mandarin_china_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-mandarin_china_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin) phone set for Mandarin, and was used in training the Mandarin [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin) acoustic model.
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

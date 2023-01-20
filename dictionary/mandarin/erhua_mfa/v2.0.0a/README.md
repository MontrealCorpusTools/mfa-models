
# Mandarin (Erhua) MFA dictionary v2.0.0a

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/mandarin_erhua_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese)
- **Dialect:** [Beijing Mandarin](https://en.wikipedia.org/wiki/Beijing_dialect)
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin)
- **Number of words:** `75,258`
- **Phones:** `ai˥˥ ai˥˩ ai˦ ai˧˥ ai˨ ai˨˩˦ ai˩ au˥˥ au˥˩ au˦ au˧˥ au˨ au˨˩˦ au˩ a˥˥ a˥˩ a˦ a˧˥ a˨ a˨˩˦ a˩ ei˥˥ ei˥˩ ei˦ ei˧˥ ei˨ ei˨˩˦ ei˩ e˥˥ e˥˩ e˦ e˧˥ e˨ e˨˩˦ e˩ f i˥˥ i˥˩ i˦ i˧˥ i˨ i˨˩˦ i˩ j k kʰ l m n ou˥˥ ou˥˩ ou˦ ou˧˥ ou˨ ou˨˩˦ ou˩ o˥˥ o˥˩ o˦ o˧˥ o˨ o˨˩˦ o˩ p pʰ s t ts tsʰ tɕ tɕʰ tʰ u˥˥ u˥˩ u˦ u˧˥ u˨ u˨˩˦ u˩ w x y˥˥ y˥˩ y˦ y˧˥ y˨ y˨˩˦ y˩ z̩˥˥ z̩˥˩ z̩˦ z̩˧˥ z̩˨ z̩˨˩˦ z̩˩ ŋ ŋ̍˧˥ ɕ ə˥˥ ə˥˩ ə˦ ə˧˥ ə˨ ə˨˩˦ ə˩ ɥ ɻ ʂ ʈʂ ʈʂʰ ʐ ʐ̩˥˥ ʐ̩˥˩ ʐ̩˦ ʐ̩˧˥ ʐ̩˨ ʐ̩˨˩˦ ʐ̩˩ ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/mandarin/erhua_mfa/v2.0.0a/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{mfa_mandarin_erhua_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Mandarin (Erhua) MFA dictionary v2.0.0a},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Mandarin/Mandarin (Erhua) MFA dictionary v2_0_0a.html}},
	year={2022},
	month={May},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Mandarin+Erhua+MFA+dictionary+v2.0.0a) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download dictionary mandarin_erhua_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-mandarin_erhua_mfa-v2.0.0a).

The dictionary available from the release page and command line installation has pronunciation and silence probabilities estimated as part acoustic model training (see [Silence probability format](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/dictionary.html#silence-probabilities) and [training pronunciation probabilities](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/training_dictionary.html) for more information.  If you would like to use the version of this dictionary without probabilities, please see the [plain dictionary](https://raw.githubusercontent.com/MontrealCorpusTools/mfa-models/main/dictionary/mandarin/erhua_mfa/mandarin_erhua_mfa.dict).

## Intended use

This dictionary is intended for forced alignment of [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin) phone set for Mandarin, and was used in training the Mandarin [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#mandarin) acoustic model. Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, especially for different styles and dialects. The most impactful improvements will generally be seen when adding reduced variants that involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in, so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants. If you are using this dictionary in production, you should acknowledge this as a potential issue.

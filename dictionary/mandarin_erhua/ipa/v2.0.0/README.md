
# Mandarin_Erhua IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Mandarin_Erhua`
- **Number of words:** `75,255`
- **Phones:** `ai˥˥ ai˥˩ ai˦ ai˧˥ ai˨ ai˨˩˦ ai˩ au˥˥ au˥˩ au˦ au˧˥ au˨ au˨˩˦ au˩ a˥˥ a˥˩ a˦ a˧˥ a˨ a˨˩˦ a˩ ei˥˥ ei˥˩ ei˦ ei˧˥ ei˨ ei˨˩˦ ei˩ e˥˥ e˥˩ e˦ e˧˥ e˨ e˨˩˦ e˩ f io˥˥ io˥˩ io˧˥ io˨ io˨˩˦ io˩ iə˥˥ iə˥˩ iə˧˥ iə˨˩˦ i˥˥ i˥˩ i˦ i˧˥ i˨ i˨˩˦ i˩ j k kʰ l m n ou˥˥ ou˥˩ ou˦ ou˧˥ ou˨ ou˨˩˦ ou˩ o˥˥ o˥˩ o˦ o˧˥ o˨ o˨˩˦ o˩ p pʰ s t ts tsʰ tɕ tɕʰ tʰ u˥˥ u˥˩ u˦ u˧˥ u˨ u˨˩˦ u˩ w x yə˥˩ yə˧˥ yə˨ yə˨˩˦ y˥˥ y˥˩ y˦ y˧˥ y˨ y˨˩˦ y˩ z̩˥˥ z̩˥˩ z̩˦ z̩˧˥ z̩˨ z̩˨˩˦ z̩˩ ŋ ŋ̍˧˥ ɕ əi˥˥ ə˥˥ ə˥˩ ə˦ ə˧˥ ə˨ ə˨˩˦ ə˩ ɥ ɻ ʂ ʈʂ ʈʂʰ ʐ ʐ̩˥˥ ʐ̩˥˩ ʐ̩˦ ʐ̩˧˥ ʐ̩˨ ʐ̩˨˩˦ ʐ̩˩ ʔ`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/mandarin_erhua/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_mandarin_erhua_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={mandarin_erhua ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={mandarin_erhua-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary mandarin_erhua_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-mandarin_erhua_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Mandarin_Erhua Language](https://en.wikipedia.org/wiki/Mandarin_Erhua_language) transcripts.

This dictionary uses the IPA phone set for Mandarin_Erhua, and was used in training the
[Mandarin_Erhua IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Mandarin_Erhua/IPA/v2.0.0/).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation, and each phone has
a minimum duration (by default 30ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

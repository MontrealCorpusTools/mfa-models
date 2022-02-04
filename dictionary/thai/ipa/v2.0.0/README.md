
# Thai IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Thai`
- **Number of words:** `18,978`
- **Phones:** `aː˥˩ aː˦˥ aː˧ aː˨˩ aː˩˩˦ a˥˩ a˦˥ a˧ a˨˩ a˩˩˦ b d eː˥˩ eː˦˥ eː˧ eː˨˩ eː˩˩˦ e˥˩ e˦˥ e˧ e˨˩ e˩˩˦ f h ia˥˩ ia˦˥ ia˧ ia˨˩ ia˩˩˦ iː˥˩ iː˦˥ iː˧ iː˨˩ iː˩˩˦ i˥˩ i˦˥ i˧ i˨˩ i˩˩˦ j k kʰ k̚ l m n oː˥˩ oː˦˥ oː˧ oː˨˩ oː˩˩˦ o˥˩ o˦˥ o˧ o˨˩ o˩˩˦ p pʰ p̚ r s t tɕ tɕʰ tʰ t̚ ua˥˩ ua˦˥ ua˧ ua˨˩ ua˩˩˦ uː˥˩ uː˦˥ uː˧ uː˨˩ uː˩˩˦ u˥˩ u˦˥ u˧ u˨˩ u˩˩˦ w ŋ ɔː˥˩ ɔː˦˥ ɔː˧ ɔː˨˩ ɔː˩˩˦ ɔ˥˩ ɔ˦˥ ɔ˧ ɔ˨˩ ɔ˩˩˦ ɛː˥˩ ɛː˦˥ ɛː˧ ɛː˨˩ ɛː˩˩˦ ɛ˥˩ ɛ˦˥ ɛ˧ ɛ˨˩ ɛ˩˩˦ ɤː˥˩ ɤː˦˥ ɤː˧ ɤː˨˩ ɤː˩˩˦ ɤ˥˩ ɤ˦˥ ɤ˧ ɤ˨˩ ɤ˩˩˦ ɯa˥˩ ɯa˦˥ ɯa˧ ɯa˨˩ ɯa˩˩˦ ɯː˥˩ ɯː˦˥ ɯː˧ ɯː˨˩ ɯː˩˩˦ ɯ˥˩ ɯ˦˥ ɯ˧ ɯ˨˩ ɯ˩˩˦ ʔ`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/thai/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_thai_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={thai ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={thai-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary thai_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-thai_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Thai Language](https://en.wikipedia.org/wiki/Thai_language) transcripts.

This dictionary uses the IPA phone set for Thai, and was used in training the
[Thai IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Thai/IPA/v2.0.0/).
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

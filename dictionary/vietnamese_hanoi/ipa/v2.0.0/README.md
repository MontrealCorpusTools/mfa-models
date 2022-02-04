
# Vietnamese_Hanoi IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Vietnamese_Hanoi`
- **Number of words:** `15,487`
- **Phones:** `aː˦ˀ˥ aː˧˦ aː˧˧ aː˧˨ aː˧˨ˀ aː˧˩ aː˨˩ a˦ˀ˥ a˧˦ a˧˧ a˧˨ˀ a˧˩ a˨˩ e˦ˀ˥ e˧˦ e˧˧ e˧˨ˀ e˧˩ e˨˩ f h iə˦ˀ˥ iə˧˦ iə˧˧ iə˧˨ˀ iə˧˩ iə˨˩ i˦ˀ˥ i˧˦ i˧˧ i˧˨ˀ i˧˩ i˨˩ j k kp̚ k̚ l m n oː˧˧ oː˨˩ o˦ˀ˥ o˧˦ o˧˧ o˧˨ˀ o˧˩ o˨˩ p p̚ s tɕ t̪ t̪ʰ t̪̚ uə˦ˀ˥ uə˧˦ uə˧˧ uə˧˨ˀ uə˧˩ uə˨˩ u˦ˀ˥ u˧˦ u˧˧ u˧˨ˀ u˧˩ u˨˩ v w x z ŋ ŋm ɓ ɔ˦ˀ˥ ɔ˧˦ ɔ˧˧ ɔ˧˨ˀ ɔ˧˩ ɔ˨˩ ɗ əː˦ˀ˥ əː˧˦ əː˧˧ əː˧˨ˀ əː˧˩ əː˨˩ ə˦ˀ˥ ə˧˦ ə˧˧ ə˧˨ˀ ə˧˩ ə˨˩ ɛ˦ˀ˥ ɛ˧˦ ɛ˧˧ ɛ˧˨ˀ ɛ˧˩ ɛ˨˩ ɣ ɨə˦ˀ˥ ɨə˧˦ ɨə˧˧ ɨə˧˨ˀ ɨə˧˩ ɨə˨˩ ɨ˦ˀ˥ ɨ˧˦ ɨ˧˧ ɨ˧˨ˀ ɨ˧˩ ɨ˨˩ ɲ ɺ ʔ`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/vietnamese_hanoi/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_vietnamese_hanoi_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={vietnamese_hanoi ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={vietnamese_hanoi-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_hanoi_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_hanoi_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Vietnamese_Hanoi Language](https://en.wikipedia.org/wiki/Vietnamese_Hanoi_language) transcripts.

This dictionary uses the IPA phone set for Vietnamese_Hanoi, and was used in training the
[Vietnamese_Hanoi IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Vietnamese_Hanoi/IPA/v2.0.0/).
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

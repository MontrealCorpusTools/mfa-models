
# Vietnamese_Hue IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Vietnamese_Hue`
- **Number of words:** `15,483`
- **Phones:** `aː˦˧˥ aː˦˩ aː˧˧ aː˧˨ aː˨˩ˀ aː˨˩˦ a˦˧˥ a˦˩ a˧˧ a˧˨ a˨˩ˀ a˨˩˦ e˦˧˥ e˦˩ e˧˧ e˧˨ e˨˩ˀ e˨˩˦ f h iə˦˧˥ iə˦˩ iə˧˧ iə˧˨ iə˨˩ˀ iə˨˩˦ i˦˧˥ i˦˩ i˧˧ i˧˨ i˨˩ˀ i˨˩˦ j k kp̚ kʰ k̚ l m n o˦˧˥ o˦˩ o˧˧ o˧˨ o˨˩ˀ o˨˩˦ p p̚ s tɕ t̪ t̪ʰ t̪̚ uə˦˧˥ uə˦˩ uə˧˧ uə˧˨ uə˨˩ˀ uə˨˩˦ u˦˧˥ u˦˩ u˧˧ u˧˨ u˨˩ˀ u˨˩˦ v w z ŋ ŋm ɓ ɔ˦˧˥ ɔ˦˩ ɔ˧˧ ɔ˧˨ ɔ˨˩ˀ ɔ˨˩˦ ɗ əː˦˧˥ əː˦˩ əː˧˧ əː˧˨ əː˨˩ˀ əː˨˩˦ ə˦˧˥ ə˦˩ ə˧˧ ə˧˨ ə˨˩ˀ ə˨˩˦ ɛ˦˧˥ ɛ˦˩ ɛ˧˧ ɛ˧˨ ɛ˨˩ˀ ɛ˨˩˦ ɣ ɨə˦˧˥ ɨə˦˩ ɨə˧˧ ɨə˧˨ ɨə˨˩ˀ ɨə˨˩˦ ɨ˦˧˥ ɨ˦˩ ɨ˧˧ ɨ˧˨ ɨ˨˩ˀ ɨ˨˩˦ ɲ ɺ ʂ ʈ ʐ ʔ`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/vietnamese_hue/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_vietnamese_hue_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={vietnamese_hue ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={vietnamese_hue-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_hue_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_hue_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Vietnamese_Hue Language](https://en.wikipedia.org/wiki/Vietnamese_Hue_language) transcripts.

This dictionary uses the IPA phone set for Vietnamese_Hue, and was used in training the
[Vietnamese_Hue IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Vietnamese_Hue/IPA/v2.0.0/).
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

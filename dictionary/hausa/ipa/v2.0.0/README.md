
# Hausa IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Hausa`
- **Number of words:** `4,904`
- **Phones:** `aː˥ aː˥˦ aː˩ a˥ a˥˦ a˩ b c cʼ d dʒ eː˥ eː˥˦ eː˩ e˥ e˥˦ e˩ h i iː˥ iː˥˦ iː˩ i˥ i˩ j j̰ k kʷ kʷʼ kʼ l m n oː˥ oː˥˦ oː˩ o˥ o˩ p r s sʼ t tʃ u uː˥ uː˥˦ uː˩ w z ŋ ɓ ɔ˥ ɔ˩ ɗ ə˥ ə˩ ɛ˥ ɛ˥˦ ɛ˩ ɟ ɡ ɡʷ ɪ˥ ɪ˥˦ ɪ˩ ɲ ɸ ɽ ʃ ʊ˥ ʊ˥˦ ʊ˩ ʔ`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/hausa/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_hausa_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={hausa ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={hausa-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary hausa_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-hausa_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Hausa Language](https://en.wikipedia.org/wiki/Hausa_language) transcripts.

This dictionary uses the IPA phone set for Hausa, and was used in training the
[Hausa IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Hausa/IPA/v2.0.0/).
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

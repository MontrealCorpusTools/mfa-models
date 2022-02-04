
# Swedish IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Swedish`
- **Number of words:** `26,421`
- **Phones:** `a a˥˧ a˥˩ a˧˩ a˩ b dʒ d̪ eː eː˥˧ eː˥˩ eː˧˩ eː˩ f h iː iː˥˧ iː˥˩ iː˧˩ j k kʰ l m n̪ oː oː˥˧ oː˥˩ oː˧˩ oː˩ p pʰ r s̪ t̪ t̪ʰ uː uː˥˧ uː˥˩ uː˧˩ w yː yː˥˧ yː˥˩ yː˧˩ yː˩ z øː øː˥˧ øː˥˩ øː˧˩ øː˩ ŋ œ œ˥˩ œ˧˩ ɑː ɑː˥˧ ɑː˥˩ ɑː˧˩ ɑː˩ ɔ ɔ˥˧ ɔ˥˩ ɔ˧˩ ɔ˩ ɕ ɖ ɛ ɛː ɛː˥˧ ɛː˥˩ ɛː˧˩ ɛ˥˧ ɛ˥˩ ɛ˧˩ ɛ˩ ɡ ɧ ɪ ɪ˥˧ ɪ˥˩ ɪ˧˩ ɪ˩ ɭ ɳ ɵ ɵ˥˧ ɵ˥˩ ɵ˧˩ ɵ˩ ʂ ʈ ʈʰ ʉː ʉː˥˧ ʉː˥˩ ʉː˧˩ ʊ ʊ˥˩ ʊ˧˩ ʊ˩ ʋ ʏ ʏ˥˧ ʏ˥˩ ʏ˧˩ ʏ˩`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/swedish/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_swedish_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={swedish ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={swedish-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary swedish_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-swedish_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Swedish Language](https://en.wikipedia.org/wiki/Swedish_language) transcripts.

This dictionary uses the IPA phone set for Swedish, and was used in training the
[Swedish IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Swedish/IPA/v2.0.0/).
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


# Russian IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Russian`
- **Number of words:** `396,300`
- **Phones:** `a b bʲ bʲː bː c cː dzʲ dʐ dʲ dʲː d̪ d̪z̪ d̪ː e f fʲ fʲː i j jː k kː m mʲ mʲː mː n̪ n̪ː o p pʲ pʲː pː r rʲ rʲː rː sʲ sʲː s̪ s̪ː tsʲ tɕ tɕː tʂ tʲ tʲː t̪ t̪s̪ t̪s̪ː t̪ː u v vʲ vʲː vː x zʲ zʲː z̪ z̪ː æ ç ɐ ɕ ɕː ə ɛ ɟ ɡ ɡː ɣ ɨ ɪ ɫ ɫː ɲ ɲː ɵ ʂ ʂː ʉ ʊ ʎ ʎː ʐ ʐː ʑː`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/russian/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_russian_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={russian ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={russian-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary russian_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-russian_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Russian Language](https://en.wikipedia.org/wiki/Russian_language) transcripts.

This dictionary uses the IPA phone set for Russian, and was used in training the
[Russian IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Russian/IPA/v2.0.0/).
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

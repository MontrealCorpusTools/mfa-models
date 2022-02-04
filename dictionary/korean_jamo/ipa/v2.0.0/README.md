
# Korean_Jamo IPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Korean_Jamo`
- **Number of words:** `25,788`
- **Phones:** `a b d dʑ e eː h i iː j k kʰ k̚ k͈ m n o oː p pʰ p̚ p͈ s sʰ s͈ t tɕ tɕʰ tɕ͈ tʰ t̚ t͈ u uː w x ç ŋ ɕʰ ɕ͈ ɛː ɡ ɣ ɥ ɭ ɯ ɯː ɰ ɲ ɸ ɾ ʌ ʌː ʎ ʝ β`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/korean_jamo/ipa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_korean_jamo_ipa_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={korean_jamo ipa MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={korean_jamo-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary korean_jamo_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-korean_jamo_ipa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Korean_Jamo Language](https://en.wikipedia.org/wiki/Korean_Jamo_language) transcripts.

This dictionary uses the IPA phone set for Korean_Jamo, and was used in training the
[Korean_Jamo IPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Korean_Jamo/IPA/v2.0.0/).
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

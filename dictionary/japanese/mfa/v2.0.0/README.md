
# Japanese MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/japanese_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Japanese](https://en.wikipedia.org/wiki/Japanese_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#japanese)
- **Number of words:** `77,695`
- **Phones:** {ipa_inline}`a`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`bʲ`, {ipa_inline}`bː`, {ipa_inline}`c`, {ipa_inline}`cː`, {ipa_inline}`d`, {ipa_inline}`dz`, {ipa_inline}`dzː`, {ipa_inline}`dʑ`, {ipa_inline}`dʑː`, {ipa_inline}`dʲ`, {ipa_inline}`dː`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`h`, {ipa_inline}`hː`, {ipa_inline}`i`, {ipa_inline}`iː`, {ipa_inline}`i̥`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`m`, {ipa_inline}`mʲ`, {ipa_inline}`mʲː`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`nː`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`pʲ`, {ipa_inline}`pʲː`, {ipa_inline}`pː`, {ipa_inline}`s`, {ipa_inline}`sː`, {ipa_inline}`t`, {ipa_inline}`ts`, {ipa_inline}`tsː`, {ipa_inline}`tɕ`, {ipa_inline}`tɕː`, {ipa_inline}`tʲ`, {ipa_inline}`tː`, {ipa_inline}`v`, {ipa_inline}`vʲ`, {ipa_inline}`w`, {ipa_inline}`z`, {ipa_inline}`ç`, {ipa_inline}`çː`, {ipa_inline}`ŋ`, {ipa_inline}`ɕ`, {ipa_inline}`ɕː`, {ipa_inline}`ɟ`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɨ`, {ipa_inline}`ɨː`, {ipa_inline}`ɨ̥`, {ipa_inline}`ɯ`, {ipa_inline}`ɯː`, {ipa_inline}`ɯ̥`, {ipa_inline}`ɰ̃`, {ipa_inline}`ɲ`, {ipa_inline}`ɲː`, {ipa_inline}`ɴ`, {ipa_inline}`ɴː`, {ipa_inline}`ɸ`, {ipa_inline}`ɸʲ`, {ipa_inline}`ɸː`, {ipa_inline}`ɾ`, {ipa_inline}`ɾʲ`, {ipa_inline}`ɾː`, {ipa_inline}`ʑ`, {ipa_inline}`ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/japanese/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_japanese_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Japanese MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Japanese/Japanese MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Japanese+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary japanese_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-japanese_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Japanese](https://en.wikipedia.org/wiki/Japanese_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#japanese) phone set for Japanese, and was used in training the Japanese [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#japanese) acoustic model.
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

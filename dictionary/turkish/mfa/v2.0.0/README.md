
# Turkish MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/turkish_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Turkish](https://en.wikipedia.org/wiki/Turkish_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#turkish)
- **Number of words:** `43,306`
- **Phones:** {ipa_inline}`a`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`bː`, {ipa_inline}`c`, {ipa_inline}`cː`, {ipa_inline}`dʒ`, {ipa_inline}`dʒː`, {ipa_inline}`d̪`, {ipa_inline}`d̪ː`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`f`, {ipa_inline}`fː`, {ipa_inline}`h`, {ipa_inline}`hː`, {ipa_inline}`i`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`jː`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n̪`, {ipa_inline}`n̪ː`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`pː`, {ipa_inline}`s̪`, {ipa_inline}`s̪ː`, {ipa_inline}`tʃ`, {ipa_inline}`tʃː`, {ipa_inline}`t̪`, {ipa_inline}`t̪ː`, {ipa_inline}`u`, {ipa_inline}`uː`, {ipa_inline}`v`, {ipa_inline}`vː`, {ipa_inline}`y`, {ipa_inline}`yː`, {ipa_inline}`z̪`, {ipa_inline}`z̪ː`, {ipa_inline}`ç`, {ipa_inline}`çː`, {ipa_inline}`ø`, {ipa_inline}`øː`, {ipa_inline}`ŋ`, {ipa_inline}`œ`, {ipa_inline}`ɛ`, {ipa_inline}`ɟ`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɨ`, {ipa_inline}`ɪ`, {ipa_inline}`ɪː`, {ipa_inline}`ɫ`, {ipa_inline}`ɫː`, {ipa_inline}`ɯ`, {ipa_inline}`ɯː`, {ipa_inline}`ɰ`, {ipa_inline}`ɲ`, {ipa_inline}`ɾ`, {ipa_inline}`ɾː`, {ipa_inline}`ʃ`, {ipa_inline}`ʃː`, {ipa_inline}`ʊ`, {ipa_inline}`ʎ`, {ipa_inline}`ʎː`, {ipa_inline}`ʏ`, {ipa_inline}`ʒ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/turkish/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_turkish_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Turkish MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Turkish/Turkish MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Turkish+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary turkish_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-turkish_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Turkish](https://en.wikipedia.org/wiki/Turkish_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#turkish) phone set for Turkish, and was used in training the Turkish [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#turkish) acoustic model.
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

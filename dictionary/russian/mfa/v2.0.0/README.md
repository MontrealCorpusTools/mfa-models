
# russian.mfa

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/russian_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [IPA charts](#ipa-charts)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Russian](https://en.wikipedia.org/wiki/Russian_language)
- **Dialect:** N/A
- **Number of words:** `412,668`
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#russian)
- **Phones:** {ipa_inline}`a`, {ipa_inline}`b`, {ipa_inline}`bʲ`, {ipa_inline}`bʲː`, {ipa_inline}`bː`, {ipa_inline}`c`, {ipa_inline}`cː`, {ipa_inline}`dzʲː`, {ipa_inline}`dʐː`, {ipa_inline}`dʲ`, {ipa_inline}`dʲː`, {ipa_inline}`d̪`, {ipa_inline}`d̪z̪`, {ipa_inline}`d̪z̪ː`, {ipa_inline}`d̪ː`, {ipa_inline}`e`, {ipa_inline}`f`, {ipa_inline}`fʲ`, {ipa_inline}`fʲː`, {ipa_inline}`fː`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`jː`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`m`, {ipa_inline}`mʲ`, {ipa_inline}`mʲː`, {ipa_inline}`mː`, {ipa_inline}`n̪`, {ipa_inline}`n̪ː`, {ipa_inline}`o`, {ipa_inline}`p`, {ipa_inline}`pʲ`, {ipa_inline}`pʲː`, {ipa_inline}`pː`, {ipa_inline}`r`, {ipa_inline}`rʲ`, {ipa_inline}`rʲː`, {ipa_inline}`rː`, {ipa_inline}`sʲ`, {ipa_inline}`sʲː`, {ipa_inline}`s̪`, {ipa_inline}`s̪ː`, {ipa_inline}`tsʲ`, {ipa_inline}`tɕ`, {ipa_inline}`tɕː`, {ipa_inline}`tʂ`, {ipa_inline}`tʂː`, {ipa_inline}`tʲ`, {ipa_inline}`tʲː`, {ipa_inline}`t̪`, {ipa_inline}`t̪s̪`, {ipa_inline}`t̪s̪ː`, {ipa_inline}`t̪ː`, {ipa_inline}`u`, {ipa_inline}`v`, {ipa_inline}`vʲ`, {ipa_inline}`vʲː`, {ipa_inline}`vː`, {ipa_inline}`x`, {ipa_inline}`xː`, {ipa_inline}`zʲ`, {ipa_inline}`zʲː`, {ipa_inline}`z̪`, {ipa_inline}`z̪ː`, {ipa_inline}`æ`, {ipa_inline}`ç`, {ipa_inline}`ɐ`, {ipa_inline}`ɕ`, {ipa_inline}`ɕː`, {ipa_inline}`ə`, {ipa_inline}`ɛ`, {ipa_inline}`ɟ`, {ipa_inline}`ɟː`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɣ`, {ipa_inline}`ɨ`, {ipa_inline}`ɪ`, {ipa_inline}`ɫ`, {ipa_inline}`ɫː`, {ipa_inline}`ɲ`, {ipa_inline}`ɲː`, {ipa_inline}`ɵ`, {ipa_inline}`ʂ`, {ipa_inline}`ʂː`, {ipa_inline}`ʉ`, {ipa_inline}`ʊ`, {ipa_inline}`ʎ`, {ipa_inline}`ʎː`, {ipa_inline}`ʐ`, {ipa_inline}`ʐː`, {ipa_inline}`ʑː`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/russian/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_russian_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Russian MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Russian/Russian MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Russian+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary russian_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-russian_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Russian](https://en.wikipedia.org/wiki/Russian_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#russian) phone set for Russian, and was used in training the Russian [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#russian) acoustic model.
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has
a minimum duration (by default 10ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

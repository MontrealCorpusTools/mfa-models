
# Chuvash CV dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/chuvash_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Chuvash](https://en.wikipedia.org/wiki/Chuvash_language)
- **Dialect:** N/A
- **Phone set:** [XPF](https://github.com/CohenPr-XPF/XPF)
- **Number of words:** `7,302`
- **Phones:** {ipa_inline}`b`, {ipa_inline}`d`, {ipa_inline}`e`, {ipa_inline}`f`, {ipa_inline}`g`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`jː`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`l`, {ipa_inline}`lː`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`nː`, {ipa_inline}`o`, {ipa_inline}`p`, {ipa_inline}`pː`, {ipa_inline}`r`, {ipa_inline}`rː`, {ipa_inline}`s`, {ipa_inline}`sː`, {ipa_inline}`t`, {ipa_inline}`ts`, {ipa_inline}`tsː`, {ipa_inline}`tʃ`, {ipa_inline}`tː`, {ipa_inline}`u`, {ipa_inline}`v`, {ipa_inline}`vː`, {ipa_inline}`y`, {ipa_inline}`ɑ`, {ipa_inline}`ɕ`, {ipa_inline}`ɕː`, {ipa_inline}`ɛ`, {ipa_inline}`ɯ`, {ipa_inline}`ʃ`, {ipa_inline}`ʃː`, {ipa_inline}`ʌ`, {ipa_inline}`ʒ`, {ipa_inline}`χ`, {ipa_inline}`χː`
- **License:** [CC-0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@misc{
	Ahn_Chodroff_2022,
	author={Ahn, Emily and Chodroff, Eleanor},
	title={VoxCommunis Corpus},
	address={\url{https://osf.io/t957v}},
	publisher={OSF},
	year={2022},
	month={Jan}
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Chuvash+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary chuvash_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-chuvash_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Chuvash](https://en.wikipedia.org/wiki/Chuvash_language) transcripts.

This dictionary uses the [XPF](https://github.com/CohenPr-XPF/XPF) phone set for Chuvash, and was used in training the Chuvash [XPF](https://github.com/CohenPr-XPF/XPF) acoustic model.
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


# Punjabi CV dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/punjabi_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Punjabi](https://en.wikipedia.org/wiki/Punjabi_language)
- **Dialect:** N/A
- **Phone set:** [Epitran](https://github.com/dmort27/epitran)
- **Number of words:** `3,231`
- **Phones:** {ipa_inline}`b`, {ipa_inline}`bː`, {ipa_inline}`d̪`, {ipa_inline}`d̪ː`, {ipa_inline}`d͡ʒ`, {ipa_inline}`d͡ʒː`, {ipa_inline}`e`, {ipa_inline}`f`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`kʰ`, {ipa_inline}`kː`, {ipa_inline}`l`, {ipa_inline}`lː`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`o`, {ipa_inline}`p`, {ipa_inline}`pʰ`, {ipa_inline}`pː`, {ipa_inline}`s`, {ipa_inline}`sː`, {ipa_inline}`t̪`, {ipa_inline}`t̪ʰ`, {ipa_inline}`t̪ː`, {ipa_inline}`t͡ʃ`, {ipa_inline}`t͡ʃʰ`, {ipa_inline}`t͡ʃː`, {ipa_inline}`u`, {ipa_inline}`x`, {ipa_inline}`z`, {ipa_inline}`õ`, {ipa_inline}`ĩ`, {ipa_inline}`ũ`, {ipa_inline}`ɑ`, {ipa_inline}`ɑ̃`, {ipa_inline}`ɔ`, {ipa_inline}`ɔ̃`, {ipa_inline}`ɖ`, {ipa_inline}`ɖː`, {ipa_inline}`ə`, {ipa_inline}`ə̃`, {ipa_inline}`ɛ`, {ipa_inline}`ɛ̃`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɣ`, {ipa_inline}`ɦ`, {ipa_inline}`ɦː`, {ipa_inline}`ɪ`, {ipa_inline}`ɪ̃`, {ipa_inline}`ɭ`, {ipa_inline}`ɳ`, {ipa_inline}`ɳː`, {ipa_inline}`ɽ`, {ipa_inline}`ɾ`, {ipa_inline}`ʃ`, {ipa_inline}`ʃː`, {ipa_inline}`ʈ`, {ipa_inline}`ʈʰ`, {ipa_inline}`ʈː`, {ipa_inline}`ʊ`, {ipa_inline}`ʊ̃`, {ipa_inline}`ʋ`, {ipa_inline}`ʋː`, {ipa_inline}`ẽ`
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

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Punjabi+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary punjabi_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-punjabi_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Punjabi](https://en.wikipedia.org/wiki/Punjabi_language) transcripts.

This dictionary uses the [Epitran](https://github.com/dmort27/epitran) phone set for Punjabi, and was used in training the Punjabi [Epitran](https://github.com/dmort27/epitran) acoustic model.
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

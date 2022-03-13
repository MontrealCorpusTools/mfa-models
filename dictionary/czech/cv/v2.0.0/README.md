
# czech.cv

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/czech_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Czech](https://en.wikipedia.org/wiki/Czech_language)
- **Number of words:** `35,317`
- **Phone set:** [XPF](https://github.com/CohenPr-XPF/XPF)
- **Phones:** {ipa_inline}`a`, {ipa_inline}`au`, {ipa_inline}`auː`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`c`, {ipa_inline}`d`, {ipa_inline}`f`, {ipa_inline}`g`, {ipa_inline}`i`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`l`, {ipa_inline}`m`, {ipa_inline}`n`, {ipa_inline}`o`, {ipa_inline}`ou`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`r`, {ipa_inline}`r̝`, {ipa_inline}`s`, {ipa_inline}`t`, {ipa_inline}`ts`, {ipa_inline}`tʃ`, {ipa_inline}`u`, {ipa_inline}`uː`, {ipa_inline}`v`, {ipa_inline}`x`, {ipa_inline}`z`, {ipa_inline}`ŋ`, {ipa_inline}`ɛ`, {ipa_inline}`ɛu`, {ipa_inline}`ɛuː`, {ipa_inline}`ɛː`, {ipa_inline}`ɟ`, {ipa_inline}`ɡ`, {ipa_inline}`ɦ`, {ipa_inline}`ɲ`, {ipa_inline}`ʃ`, {ipa_inline}`ʒ`
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

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Czech+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary czech_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-czech_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Czech](https://en.wikipedia.org/wiki/Czech_language) transcripts.

This dictionary uses the [XPF](https://github.com/CohenPr-XPF/XPF) phone set for Czech, and was used in training the Czech [XPF](https://github.com/CohenPr-XPF/XPF) acoustic model.
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

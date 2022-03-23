
# Maltese CV dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/maltese_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Maltese](https://en.wikipedia.org/wiki/Maltese_language)
- **Dialect:** N/A
- **Phone set:** [Epitran](https://github.com/dmort27/epitran)
- **Number of words:** `12,252`
- **Phones:** {ipa_inline}`b`, {ipa_inline}`bˤː`, {ipa_inline}`c`, {ipa_inline}`d`, {ipa_inline}`dˤː`, {ipa_inline}`d͡ʒ`, {ipa_inline}`d͡ʒˤː`, {ipa_inline}`f`, {ipa_inline}`fˤː`, {ipa_inline}`h`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`jˤː`, {ipa_inline}`k`, {ipa_inline}`l`, {ipa_inline}`lˤː`, {ipa_inline}`m`, {ipa_inline}`mˤː`, {ipa_inline}`n`, {ipa_inline}`nˤː`, {ipa_inline}`p`, {ipa_inline}`r`, {ipa_inline}`rˤː`, {ipa_inline}`s`, {ipa_inline}`sˤː`, {ipa_inline}`t`, {ipa_inline}`tˤː`, {ipa_inline}`t͡s`, {ipa_inline}`t͡sˤː`, {ipa_inline}`t͡ʃ`, {ipa_inline}`v`, {ipa_inline}`w`, {ipa_inline}`y`, {ipa_inline}`z`, {ipa_inline}`zˤː`, {ipa_inline}`ħ`, {ipa_inline}`ħː`, {ipa_inline}`ɐ`, {ipa_inline}`ɐˤː`, {ipa_inline}`ɔ`, {ipa_inline}`ɔˤː`, {ipa_inline}`ɛ`, {ipa_inline}`ɛˤː`, {ipa_inline}`ɡ`, {ipa_inline}`ɪ`, {ipa_inline}`ɪˤː`, {ipa_inline}`ʃ`, {ipa_inline}`ʃː`, {ipa_inline}`ʃˤː`, {ipa_inline}`ʊ`, {ipa_inline}`ʊˤː`, {ipa_inline}`ʔ`, {ipa_inline}`ʔˤː`, {ipa_inline}`ˤː`
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

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Maltese+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary maltese_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-maltese_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Maltese](https://en.wikipedia.org/wiki/Maltese_language) transcripts.

This dictionary uses the [Epitran](https://github.com/dmort27/epitran) phone set for Maltese, and was used in training the Maltese [Epitran](https://github.com/dmort27/epitran) acoustic model.
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


# italian.cv

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/italian_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Italian](https://en.wikipedia.org/wiki/Italian_language)
- **Number of words:** `143,780`
- **Phone set:** [Epitran](https://github.com/dmort27/epitran)
- **Phones:** {ipa_inline}`_`, {ipa_inline}`a`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`bː`, {ipa_inline}`d`, {ipa_inline}`dː`, {ipa_inline}`d͡ʒ`, {ipa_inline}`d͡ʒː`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`f`, {ipa_inline}`fː`, {ipa_inline}`g`, {ipa_inline}`hː`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`l`, {ipa_inline}`lː`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`nː`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`pː`, {ipa_inline}`r`, {ipa_inline}`rː`, {ipa_inline}`s`, {ipa_inline}`sː`, {ipa_inline}`t`, {ipa_inline}`tː`, {ipa_inline}`t͡s`, {ipa_inline}`t͡ʃ`, {ipa_inline}`t͡ʃː`, {ipa_inline}`u`, {ipa_inline}`v`, {ipa_inline}`vː`, {ipa_inline}`w`, {ipa_inline}`x`, {ipa_inline}`y`, {ipa_inline}`z`, {ipa_inline}`µ`, {ipa_inline}`º`, {ipa_inline}`ß`, {ipa_inline}`á`, {ipa_inline}`ã`, {ipa_inline}`å`, {ipa_inline}`æ`, {ipa_inline}`ë`, {ipa_inline}`ï`, {ipa_inline}`ð`, {ipa_inline}`ñ`, {ipa_inline}`ö`, {ipa_inline}`ø`, {ipa_inline}`ü`, {ipa_inline}`þ`, {ipa_inline}`ÿ`, {ipa_inline}`ą`, {ipa_inline}`đ`, {ipa_inline}`ė`, {ipa_inline}`ę`, {ipa_inline}`ě`, {ipa_inline}`ħ`, {ipa_inline}`ī`, {ipa_inline}`ı`, {ipa_inline}`ľ`, {ipa_inline}`ł`, {ipa_inline}`ń`, {ipa_inline}`ň`, {ipa_inline}`ō`, {ipa_inline}`ő`, {ipa_inline}`œ`, {ipa_inline}`ř`, {ipa_inline}`ś`, {ipa_inline}`ş`, {ipa_inline}`š`, {ipa_inline}`ū`, {ipa_inline}`ŭ`, {ipa_inline}`ǩ`, {ipa_inline}`ș`, {ipa_inline}`ț`, {ipa_inline}`ɔ`, {ipa_inline}`ə`, {ipa_inline}`ɛ`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɲ`, {ipa_inline}`ʃ`, {ipa_inline}`ʎ`, {ipa_inline}`ʹ`, {ipa_inline}`ʻ`, {ipa_inline}`ʼ`, {ipa_inline}`ʾ`, {ipa_inline}`ʿ`, {ipa_inline}`а`, {ipa_inline}`б`, {ipa_inline}`д`, {ipa_inline}`е`, {ipa_inline}`л`, {ipa_inline}`н`, {ipa_inline}`о`, {ipa_inline}`с`, {ipa_inline}`у`, {ipa_inline}`ц`, {ipa_inline}`ъ`, {ipa_inline}`ё`, {ipa_inline}`љ`, {ipa_inline}`ң`, {ipa_inline}`ד`, {ipa_inline}`ה`, {ipa_inline}`ו`, {ipa_inline}`ة`, {ipa_inline}`ر`, {ipa_inline}`س`, {ipa_inline}`ص`, {ipa_inline}`غ`, {ipa_inline}`ل`, {ipa_inline}`ي`, {ipa_inline}`ḱ`, {ipa_inline}`ṛ`, {ipa_inline}`ṡ`, {ipa_inline}`ṣ`, {ipa_inline}`ṭ`, {ipa_inline}`ạ`, {ipa_inline}`ẽ`, {ipa_inline}`ụ`, {ipa_inline}`家`, {ipa_inline}`ꞌ`
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

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Italian+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary italian_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-italian_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Italian](https://en.wikipedia.org/wiki/Italian_language) transcripts.

This dictionary uses the [Epitran](https://github.com/dmort27/epitran) phone set for Italian, and was used in training the Italian [Epitran](https://github.com/dmort27/epitran) acoustic model.
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

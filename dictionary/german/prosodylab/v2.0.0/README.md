
# German PROSODYLAB dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/german_prosodylab.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [German](https://en.wikipedia.org/wiki/German_language)
- **Dialect:** N/A
- **Phone set:** [PROSODYLAB](https://github.com/prosodylab/prosodylab.dictionaries)
- **Number of words:** `310,951`
- **Phones:** `$1 &0 &1 )0 )1 + /0 /1 = @0 A0 A1 B0 B1 E0 E1 I0 I1 J N O0 O1 S U0 U1 V1 W0 W1 X0 X1 Y0 Y1 Z ^1 _ a0 a1 b c0 d drei0 e0 e1 f g h i0 i1 j k l m n null0 null1 o0 o1 p q0 q1 r s sechs1 t u0 u1 v w x y0 y1 z zwei0 zwei1 {0 {1 |0 |1 ~1`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/german/PROSODYLAB/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@article{
	gorman2011prosodylab,
	author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael},
	title={Prosodylab-aligner: A tool for forced alignment of laboratory speech},
	journal={Canadian Acoustics},
	volume={39},
	number={3},
	pages={192--193},
	year={2011}
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=German+PROSODYLAB+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary german_prosodylab
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-german_prosodylab-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [German](https://en.wikipedia.org/wiki/German_language) transcripts.

This dictionary uses the [PROSODYLAB](https://github.com/prosodylab/prosodylab.dictionaries) phone set for German, and was used in training the German [PROSODYLAB](https://github.com/prosodylab/prosodylab.dictionaries) acoustic model.
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

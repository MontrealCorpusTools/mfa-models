
# Mandarin PINYIN dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/mandarin_pinyin.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese)
- **Dialect:** N/A
- **Phone set:** [PINYIN](https://en.wikipedia.org/wiki/Pinyin)
- **Number of words:** `2,004`
- **Phones:** {ipa_inline}`a1`, {ipa_inline}`a2`, {ipa_inline}`a3`, {ipa_inline}`a4`, {ipa_inline}`a5`, {ipa_inline}`ai1`, {ipa_inline}`ai2`, {ipa_inline}`ai3`, {ipa_inline}`ai4`, {ipa_inline}`ai5`, {ipa_inline}`ao1`, {ipa_inline}`ao2`, {ipa_inline}`ao3`, {ipa_inline}`ao4`, {ipa_inline}`ao5`, {ipa_inline}`b`, {ipa_inline}`c`, {ipa_inline}`ch`, {ipa_inline}`d`, {ipa_inline}`e1`, {ipa_inline}`e2`, {ipa_inline}`e3`, {ipa_inline}`e4`, {ipa_inline}`e5`, {ipa_inline}`ei1`, {ipa_inline}`ei2`, {ipa_inline}`ei3`, {ipa_inline}`ei4`, {ipa_inline}`f`, {ipa_inline}`g`, {ipa_inline}`h`, {ipa_inline}`i1`, {ipa_inline}`i2`, {ipa_inline}`i3`, {ipa_inline}`i4`, {ipa_inline}`i5`, {ipa_inline}`ia1`, {ipa_inline}`ia2`, {ipa_inline}`ia3`, {ipa_inline}`ia4`, {ipa_inline}`ia5`, {ipa_inline}`iao1`, {ipa_inline}`iao2`, {ipa_inline}`iao3`, {ipa_inline}`iao4`, {ipa_inline}`ie1`, {ipa_inline}`ie2`, {ipa_inline}`ie3`, {ipa_inline}`ie4`, {ipa_inline}`ie5`, {ipa_inline}`ii1`, {ipa_inline}`ii2`, {ipa_inline}`ii3`, {ipa_inline}`ii4`, {ipa_inline}`ii5`, {ipa_inline}`io1`, {ipa_inline}`io2`, {ipa_inline}`io3`, {ipa_inline}`io4`, {ipa_inline}`iou1`, {ipa_inline}`iou2`, {ipa_inline}`iou3`, {ipa_inline}`iou4`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`l`, {ipa_inline}`m`, {ipa_inline}`n`, {ipa_inline}`ng`, {ipa_inline}`o1`, {ipa_inline}`o2`, {ipa_inline}`o3`, {ipa_inline}`o4`, {ipa_inline}`o5`, {ipa_inline}`ou1`, {ipa_inline}`ou2`, {ipa_inline}`ou3`, {ipa_inline}`ou4`, {ipa_inline}`ou5`, {ipa_inline}`p`, {ipa_inline}`q`, {ipa_inline}`r`, {ipa_inline}`s`, {ipa_inline}`sh`, {ipa_inline}`t`, {ipa_inline}`u1`, {ipa_inline}`u2`, {ipa_inline}`u3`, {ipa_inline}`u4`, {ipa_inline}`u5`, {ipa_inline}`ua1`, {ipa_inline}`ua2`, {ipa_inline}`ua3`, {ipa_inline}`ua4`, {ipa_inline}`ua5`, {ipa_inline}`uai1`, {ipa_inline}`uai2`, {ipa_inline}`uai3`, {ipa_inline}`uai4`, {ipa_inline}`ue1`, {ipa_inline}`ue2`, {ipa_inline}`ue3`, {ipa_inline}`ue4`, {ipa_inline}`ue5`, {ipa_inline}`uei1`, {ipa_inline}`uei2`, {ipa_inline}`uei3`, {ipa_inline}`uei4`, {ipa_inline}`uei5`, {ipa_inline}`uo1`, {ipa_inline}`uo2`, {ipa_inline}`uo3`, {ipa_inline}`uo4`, {ipa_inline}`uo5`, {ipa_inline}`v1`, {ipa_inline}`v2`, {ipa_inline}`v3`, {ipa_inline}`v4`, {ipa_inline}`v5`, {ipa_inline}`va1`, {ipa_inline}`va2`, {ipa_inline}`va3`, {ipa_inline}`va4`, {ipa_inline}`ve1`, {ipa_inline}`ve2`, {ipa_inline}`ve3`, {ipa_inline}`ve4`, {ipa_inline}`x`, {ipa_inline}`z`, {ipa_inline}`zh`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/mandarin/PINYIN/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_mandarin_pinyin_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Mandarin PINYIN dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Mandarin/Mandarin PINYIN dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Mandarin+PINYIN+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary mandarin_pinyin
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-mandarin_pinyin-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Mandarin Chinese](https://en.wikipedia.org/wiki/Mandarin_Chinese) transcripts.

This dictionary uses the [PINYIN](https://en.wikipedia.org/wiki/Pinyin) phone set for Mandarin, and was used in training the Mandarin [PINYIN](https://en.wikipedia.org/wiki/Pinyin) acoustic model.
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

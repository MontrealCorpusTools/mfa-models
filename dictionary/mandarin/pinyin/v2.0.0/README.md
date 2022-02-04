
# Mandarin PINYIN

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Mandarin`
- **Number of words:** `2,003`
- **Phones:** `a1 a2 a3 a4 a5 ai1 ai2 ai3 ai4 ai5 ao1 ao2 ao3 ao4 ao5 b c ch d e1 e2 e3 e4 e5 ei1 ei2 ei3 ei4 f g h i1 i2 i3 i4 i5 ia1 ia2 ia3 ia4 ia5 iao1 iao2 iao3 iao4 ie1 ie2 ie3 ie4 ie5 ii1 ii2 ii3 ii4 ii5 io1 io2 io3 io4 iou1 iou2 iou3 iou4 j k l m n ng o1 o2 o3 o4 o5 ou1 ou2 ou3 ou4 ou5 p q r s sh t u1 u2 u3 u4 u5 ua1 ua2 ua3 ua4 ua5 uai1 uai2 uai3 uai4 ue1 ue2 ue3 ue4 ue5 uei1 uei2 uei3 uei4 uei5 uo1 uo2 uo3 uo4 uo5 v1 v2 v3 v4 v5 va1 va2 va3 va4 ve1 ve2 ve3 ve4 x z zh`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/mandarin/pinyin/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@techreport{MFA_mandarin_pinyin_pronunciation dictionary_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={mandarin pinyin MFA pronunciation dictionary v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={mandarin-pinyin-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary mandarin_pinyin
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-mandarin_pinyin-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Mandarin Language](https://en.wikipedia.org/wiki/Mandarin_language) transcripts.

This dictionary uses the PINYIN phone set for Mandarin, and was used in training the
[Mandarin PINYIN acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Mandarin/PINYIN/v2.0.0/).
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation, and each phone has
a minimum duration (by default 30ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

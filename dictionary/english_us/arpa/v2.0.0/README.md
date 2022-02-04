
# English_Us ARPA

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `English_Us`
- **Number of words:** `199,911`
- **Phones:** `AA0 AA1 AA2 AE0 AE1 AE2 AH0 AH1 AH2 AO0 AO1 AO2 AW0 AW1 AW2 AY0 AY1 AY2 B CH D DH EH0 EH1 EH2 ER0 ER1 ER2 EY0 EY1 EY2 F G HH IH0 IH1 IH2 IY0 IY1 IY2 JH K L M N NG OW0 OW1 OW2 OY0 OY1 OY2 P R S SH T TH UH0 UH1 UH2 UW0 UW1 UW2 V W Y Z ZH`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/english_us/arpa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@article{gorman2011prosodylab, author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael}, title={Prosodylab-aligner: A tool for forced alignment of laboratory speech}, journal={Canadian Acoustics}, volume={39}, number={3}, pages={192--193}, year={2011}}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary english_us_arpa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-english_us_arpa-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [English_Us Language](https://en.wikipedia.org/wiki/English_Us_language) transcripts.

This dictionary uses the ARPA phone set for English_Us, and was used in training the
[English_Us ARPA acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/English_Us/ARPA/v2.0.0/).
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

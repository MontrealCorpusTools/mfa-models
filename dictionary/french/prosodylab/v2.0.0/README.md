
# French PROSODYLAB

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `French`
- **Number of words:** `125,372`
- **Phones:** `@ E G N O R S Z ^ a b cinq d deux e f g huit i j k l m n neuf o p s t to u un v w x y z`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/french/prosodylab/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@article{gorman2011prosodylab, author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael}, title={Prosodylab-aligner: A tool for forced alignment of laboratory speech}, journal={Canadian Acoustics}, volume={39}, number={3}, pages={192--193}, year={2011}}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary french_prosodylab
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-french_prosodylab-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [French Language](https://en.wikipedia.org/wiki/French_language) transcripts.

This dictionary uses the PROSODYLAB phone set for French, and was used in training the
[French PROSODYLAB acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/French/PROSODYLAB/v2.0.0/).
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

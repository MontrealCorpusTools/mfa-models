
# Belarusian CV

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** `Belarusian`
- **Number of words:** `115,936`
- **Phones:** `a b bʲ d dz dzʲ dzʲː dʒ f fʲ i j k kʲ l lʲ lʲː m mʲ n nʲ nʲː nː o p pʲ r s sʲ sʲː sː t ts tsʲ tsʲː tsː tʃ tʃː tː u v vʲ x xʲ z zʲ zʲː zː ɛ ɣ ɣʲ ʃ ʃː ʒ ʒː`
- **License:** [CC-0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@misc{Ahn_Chodroff_2022, author={Ahn, Emily and Chodroff, Eleanor}, title={VoxCommunis Corpus}, address={\url{https://osf.io/t957v}, publisher={OSF}, year={2022}, month={Jan}}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary belarusian_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-belarusian_cv-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Belarusian Language](https://en.wikipedia.org/wiki/Belarusian_language) transcripts.

This dictionary uses the CV phone set for Belarusian, and was used in training the
[Belarusian CV acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Belarusian/CV/v2.0.0/).
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

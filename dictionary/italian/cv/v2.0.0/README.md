
# Italian CV

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** `Italian`
- **Number of words:** `143,766`
- **Phones:** `_ a aː b bː d dː d͡ʒ d͡ʒː e eː f fː g hː i j k kː l lː m mː n nː o oː p pː r rː s sː t tː t͡s t͡ʃ t͡ʃː u v vː w x y z µ º ß á ã å æ ë ï ð ñ ö ø ü þ ÿ ą đ ė ę ě ħ ī ı ľ ł ń ň ō ő œ ř ś ş š ū ŭ ǩ ș ț ɔ ə ɛ ɡ ɡː ɲ ʃ ʎ ʹ ʻ ʼ ʾ ʿ а б д е л н о с у ц ъ ё љ ң ד ה ו ة ر س ص غ ل ي ḱ ṛ ṡ ṣ ṭ ạ ẽ ụ 家 ꞌ`
- **License:** [CC-0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@misc{Ahn_Chodroff_2022, author={Ahn, Emily and Chodroff, Eleanor}, title={VoxCommunis Corpus}, address={\url{https://osf.io/t957v}, publisher={OSF}, year={2022}, month={Jan}}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary italian_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-italian_cv-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Italian Language](https://en.wikipedia.org/wiki/Italian_language) transcripts.

This dictionary uses the CV phone set for Italian, and was used in training the
[Italian CV acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Italian/CV/v2.0.0/).
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

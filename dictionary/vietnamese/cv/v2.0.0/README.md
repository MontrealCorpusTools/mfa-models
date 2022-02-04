
# Vietnamese CV

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** `Vietnamese`
- **Number of words:** `2,185`
- **Phones:** `:˧ :˧˥ :˧˥ˀ :˧˩˧ :˨˩ :˨˩ˀ aː˧ aː˧˥ aː˧˥ˀ aː˧˩˧ aː˨˩ aː˨˩ˀ a˧ a˧˥ a˧˥ˀ a˧˩˧ a˨˩ a˨˩ˀ e˧ e˧˥ e˧˥ˀ e˧˩˧ e˨˩ e˨˩ˀ f h ie˧˥ˀ˧ ie˧˥˧ ie˧˧ ie˧˧˥ ie˧˧˥ˀ ie˧˧˩˧ ie˧˨˩ ie˧˨˩ˀ ie˧˩˧˧ ie˨˩ˀ˧ ie˨˩˧ i˧ i˧˥ i˧˥ˀ i˧˩˧ i˨˩ i˨˩ˀ j k l m n̪ o˧ o˧˥ o˧˥ˀ o˧˩˧ o˨˩ o˨˩ˀ p s s˧ tɕ t̪ t̪ʰ uo˧˥˧ uo˧˧ uo˧˧˥ uo˧˧˥ˀ uo˧˧˩˧ uo˧˨˩ uo˧˨˩ˀ uo˧˩˧˧ uo˨˩˧ u˧ u˧˥ u˧˥ˀ u˧˩˧ u˨˩ u˨˩ˀ v w x z ŋ ɓ ɔ˧ ɔ˧˥ ɔ˧˥ˀ ɔ˧˩˧ ɔ˨˩ ɔ˨˩ˀ ɗ ɛ˧ ɛ˧˥ ɛ˧˥ˀ ɛ˧˩˧ ɛ˨˩ ɛ˨˩ˀ ɣ ɤ ɤ˧ ɤ˧˥ ɤ˧˥ˀ ɤ˧˩˧ ɤ˨˩ ɤ˨˩ˀ ɯɤ˧˥ˀ˧ ɯɤ˧˥˧ ɯɤ˧˧ ɯɤ˧˧˥ ɯɤ˧˧˥ˀ ɯɤ˧˧˩˧ ɯɤ˧˨˩ ɯɤ˧˨˩ˀ ɯɤ˧˩˧˧ ɯɤ˨˩ˀ˧ ɯɤ˨˩˧ ɯ˧ ɯ˧˥ ɯ˧˥ˀ ɯ˧˩˧ ɯ˨˩ ɯ˨˩ˀ ɲ ʔ`
- **License:** [CC-0](https://creativecommons.org/publicdomain/zero/1.0/)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**
  - `@misc{Ahn_Chodroff_2022, author={Ahn, Emily and Chodroff, Eleanor}, title={VoxCommunis Corpus}, address={\url{https://osf.io/t957v}, publisher={OSF}, year={2022}, month={Jan}}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_cv-v2.0.0)

## Intended use

This dictionary is intended for forced alignment of [Vietnamese Language](https://en.wikipedia.org/wiki/Vietnamese_language) transcripts.

This dictionary uses the CV phone set for Vietnamese, and was used in training the
[Vietnamese CV acoustic model](https://github.com/MontrealCorpusTools/mfa-models/blob/main/acoustic/Vietnamese/CV/v2.0.0/).
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

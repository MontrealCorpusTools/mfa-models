
# Vietnamese CV dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/vietnamese_cv.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Vox Communis](https://osf.io/t957v/)
- **Language:** [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language)
- **Dialect:** N/A
- **Phone set:** [XPF](https://github.com/CohenPr-XPF/XPF)
- **Number of words:** `2,188`
- **Phones:** `aː˧ aː˧˥ aː˧˥ˀ aː˧˩˧ aː˨˩ aː˨˩ˀ a˧ a˧˥ a˧˥ˀ a˧˩˧ a˨˩ a˨˩ˀ e˧ e˧˥ e˧˥ˀ e˧˩˧ e˨˩ e˨˩ˀ f h ie˧˥ˀ˧ ie˧˥˧ ie˧˧ ie˧˧˥ ie˧˧˥ˀ ie˧˧˩˧ ie˧˨˩ ie˧˨˩ˀ ie˧˩˧˧ ie˨˩ˀ˧ ie˨˩˧ i˧ i˧˥ i˧˥ˀ i˧˩˧ i˨˩ i˨˩ˀ j k l m n̪ o˧ o˧˥ o˧˥ˀ o˧˩˧ o˨˩ o˨˩ˀ p s s˧ tɕ t̪ t̪ʰ uo˧˥˧ uo˧˧ uo˧˧˥ uo˧˧˥ˀ uo˧˧˩˧ uo˧˨˩ uo˧˨˩ˀ uo˧˩˧˧ uo˨˩˧ u˧ u˧˥ u˧˥ˀ u˧˩˧ u˨˩ u˨˩ˀ v w x z ŋ ɓ ɔ˧ ɔ˧˥ ɔ˧˥ˀ ɔ˧˩˧ ɔ˨˩ ɔ˨˩ˀ ɗ ɛ˧ ɛ˧˥ ɛ˧˥ˀ ɛ˧˩˧ ɛ˨˩ ɛ˨˩ˀ ɣ ɤː˧ ɤː˧˥ ɤː˧˥ˀ ɤː˧˩˧ ɤː˨˩ ɤː˨˩ˀ ɤ˧ ɤ˧˥ ɤ˧˥ˀ ɤ˧˩˧ ɤ˨˩ ɤ˨˩ˀ ɯɤ˧˥ˀ˧ ɯɤ˧˥˧ ɯɤ˧˧ ɯɤ˧˧˥ ɯɤ˧˧˥ˀ ɯɤ˧˧˩˧ ɯɤ˧˨˩ ɯɤ˧˨˩ˀ ɯɤ˧˩˧˧ ɯɤ˨˩ˀ˧ ɯɤ˨˩˧ ɯ˧ ɯ˧˥ ɯ˧˥ˀ ɯ˧˩˧ ɯ˨˩ ɯ˨˩ˀ ɲ ʔ`
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

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Vietnamese+CV+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary vietnamese_cv
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-vietnamese_cv-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Vietnamese](https://en.wikipedia.org/wiki/Vietnamese_language) transcripts.

This dictionary uses the [XPF](https://github.com/CohenPr-XPF/XPF) phone set for Vietnamese, and was used in training the Vietnamese [XPF](https://github.com/CohenPr-XPF/XPF) acoustic model.
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.
The most impactful improvements will generally be seen when adding reduced variants that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has
a minimum duration (by default 10ms). If a speaker pronounces a multisyllabic word with just a single syllable, it can be hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

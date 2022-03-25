
# Ukrainian MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/ukrainian_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Ukrainian](https://en.wikipedia.org/wiki/Ukrainian_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#ukrainian)
- **Number of words:** `64,017`
- **Phones:** `b bʲ bʲː bː c cː dzʲ dʒ dʲ dʲː d̪ d̪z̪ d̪z̪ː d̪ː e f fʲ i j k kː l lː m mʲ mʲː n̪ n̪ː o p pʲ pʲː sʲ sʲː s̪ s̪ː tsʲ tsʲː tʃ tʃʲ tʃʲː tʃː tʲ tʲː t̪ t̪s̪ t̪s̪ː t̪ː u x zʲ zʲː z̪ z̪ː ç ɐ ɑ ɔ ɛ ɡ ɡː ɦ ɦː ɪ ɲ ɲː ɾ ɾʲ ɾʲː ɾː ʃ ʃʲ ʃʲː ʊ ʋ ʋʲ ʋʲː ʋː ʎ ʎː ʒ ʒʲ ʒʲː ʝ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/ukrainian/mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{mfa_ukrainian_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Ukrainian MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Ukrainian/Ukrainian MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Ukrainian+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary ukrainian_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-ukrainian_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Ukrainian](https://en.wikipedia.org/wiki/Ukrainian_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#ukrainian) phone set for Ukrainian, and was used in training the Ukrainian [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#ukrainian) acoustic model.
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

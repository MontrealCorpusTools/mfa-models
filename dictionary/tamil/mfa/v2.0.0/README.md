
# Tamil MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/tamil_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Tamil](https://en.wikipedia.org/wiki/Tamil_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#tamil)
- **Number of words:** `2,482`
- **Phones:** {ipa_inline}`a`, {ipa_inline}`aj`, {ipa_inline}`aw`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`dʑ`, {ipa_inline}`d̪`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`i`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`jː`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`l`, {ipa_inline}`lː`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`nː`, {ipa_inline}`n̪`, {ipa_inline}`n̪ː`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`pː`, {ipa_inline}`r`, {ipa_inline}`s`, {ipa_inline}`tɕ`, {ipa_inline}`tɕː`, {ipa_inline}`tː`, {ipa_inline}`t̪`, {ipa_inline}`t̪ː`, {ipa_inline}`u`, {ipa_inline}`uː`, {ipa_inline}`ŋ`, {ipa_inline}`ŋː`, {ipa_inline}`ɖ`, {ipa_inline}`ɡ`, {ipa_inline}`ɦ`, {ipa_inline}`ɭ`, {ipa_inline}`ɭː`, {ipa_inline}`ɲ`, {ipa_inline}`ɲː`, {ipa_inline}`ɳ`, {ipa_inline}`ɳː`, {ipa_inline}`ɻ`, {ipa_inline}`ɾ`, {ipa_inline}`ʂ`, {ipa_inline}`ʈ`, {ipa_inline}`ʈː`, {ipa_inline}`ʋ`, {ipa_inline}`ʋː`, {ipa_inline}`ʔ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/tamil/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_tamil_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Tamil MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Tamil/Tamil MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Tamil+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary tamil_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-tamil_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Tamil](https://en.wikipedia.org/wiki/Tamil_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#tamil) phone set for Tamil, and was used in training the Tamil [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#tamil) acoustic model.
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

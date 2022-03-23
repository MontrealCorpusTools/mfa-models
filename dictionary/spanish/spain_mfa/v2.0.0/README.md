
# Spanish (Spain) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/spanish_spain_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Spanish](https://en.wikipedia.org/wiki/Spanish_language)
- **Dialect:** [Peninsular Spanish](https://en.wikipedia.org/wiki/Peninsular_Spanish)
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#spanish)
- **Number of words:** `82,355`
- **Phones:** {ipa_inline}`a`, {ipa_inline}`b`, {ipa_inline}`c`, {ipa_inline}`d̪`, {ipa_inline}`e`, {ipa_inline}`f`, {ipa_inline}`i`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`l`, {ipa_inline}`m`, {ipa_inline}`n`, {ipa_inline}`o`, {ipa_inline}`p`, {ipa_inline}`r`, {ipa_inline}`s`, {ipa_inline}`tʃ`, {ipa_inline}`t̪`, {ipa_inline}`u`, {ipa_inline}`w`, {ipa_inline}`x`, {ipa_inline}`ç`, {ipa_inline}`ð`, {ipa_inline}`ŋ`, {ipa_inline}`ɟ`, {ipa_inline}`ɟʝ`, {ipa_inline}`ɡ`, {ipa_inline}`ɣ`, {ipa_inline}`ɲ`, {ipa_inline}`ɾ`, {ipa_inline}`ʃ`, {ipa_inline}`ʎ`, {ipa_inline}`ʝ`, {ipa_inline}`β`, {ipa_inline}`θ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/spanish/spain_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_spanish_spain_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Spanish (Spain) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Spanish/Spanish (Spain) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Spanish+Spain+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary spanish_spain_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-spanish_spain_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Spanish](https://en.wikipedia.org/wiki/Spanish_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#spanish) phone set for Spanish, and was used in training the Spanish [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#spanish) acoustic model.
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

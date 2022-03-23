
# Czech MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/czech_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Czech](https://en.wikipedia.org/wiki/Czech_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#czech)
- **Number of words:** `94,012`
- **Phones:** {ipa_inline}`a`, {ipa_inline}`aw`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`c`, {ipa_inline}`d`, {ipa_inline}`dʒ`, {ipa_inline}`ew`, {ipa_inline}`f`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`l`, {ipa_inline}`l̩`, {ipa_inline}`m`, {ipa_inline}`m̩`, {ipa_inline}`n`, {ipa_inline}`n̩`, {ipa_inline}`o`, {ipa_inline}`ow`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`r`, {ipa_inline}`r̝`, {ipa_inline}`r̩`, {ipa_inline}`s`, {ipa_inline}`t`, {ipa_inline}`ts`, {ipa_inline}`tʃ`, {ipa_inline}`u`, {ipa_inline}`uː`, {ipa_inline}`v`, {ipa_inline}`x`, {ipa_inline}`z`, {ipa_inline}`ŋ`, {ipa_inline}`ɛ`, {ipa_inline}`ɛː`, {ipa_inline}`ɟ`, {ipa_inline}`ɡ`, {ipa_inline}`ɦ`, {ipa_inline}`ɪ`, {ipa_inline}`ɱ`, {ipa_inline}`ɲ`, {ipa_inline}`ʃ`, {ipa_inline}`ʒ`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/czech/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_czech_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Czech MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Czech/Czech MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Czech+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary czech_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-czech_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Czech](https://en.wikipedia.org/wiki/Czech_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#czech) phone set for Czech, and was used in training the Czech [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#czech) acoustic model.
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

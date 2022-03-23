
# Korean (Jamo) MFA dictionary v2.0.0

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/korean_jamo_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Korean](https://en.wikipedia.org/wiki/Korean_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean)
- **Number of words:** `54,093`
- **Phones:** {ipa_inline}`b`, {ipa_inline}`d`, {ipa_inline}`dʑ`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`h`, {ipa_inline}`i`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`kʰ`, {ipa_inline}`k̚`, {ipa_inline}`k͈`, {ipa_inline}`m`, {ipa_inline}`n`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`pʰ`, {ipa_inline}`p̚`, {ipa_inline}`p͈`, {ipa_inline}`s`, {ipa_inline}`sʰ`, {ipa_inline}`s͈`, {ipa_inline}`t`, {ipa_inline}`tɕ`, {ipa_inline}`tɕʰ`, {ipa_inline}`tɕ͈`, {ipa_inline}`tʰ`, {ipa_inline}`t̚`, {ipa_inline}`t͈`, {ipa_inline}`u`, {ipa_inline}`uː`, {ipa_inline}`w`, {ipa_inline}`x`, {ipa_inline}`ç`, {ipa_inline}`ŋ`, {ipa_inline}`ɐ`, {ipa_inline}`ɕʰ`, {ipa_inline}`ɕ͈`, {ipa_inline}`ɡ`, {ipa_inline}`ɣ`, {ipa_inline}`ɥ`, {ipa_inline}`ɦ`, {ipa_inline}`ɨ`, {ipa_inline}`ɨː`, {ipa_inline}`ɭ`, {ipa_inline}`ɰ`, {ipa_inline}`ɲ`, {ipa_inline}`ɸ`, {ipa_inline}`ɾ`, {ipa_inline}`ʌ`, {ipa_inline}`ʌː`, {ipa_inline}`ʎ`, {ipa_inline}`ʝ`, {ipa_inline}`β`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/korean/jamo_mfa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_korean_jamo_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Korean (Jamo) MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Korean/Korean (Jamo) MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Korean+Jamo+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary korean_jamo_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-korean_jamo_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Korean](https://en.wikipedia.org/wiki/Korean_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean) phone set for Korean, and was used in training the Korean [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#korean) acoustic model.
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

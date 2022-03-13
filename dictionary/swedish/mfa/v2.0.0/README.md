
# swedish.mfa

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/swedish_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [IPA charts](#ipa-charts)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Swedish](https://en.wikipedia.org/wiki/Swedish_language)
- **Dialect:** N/A
- **Number of words:** `50,195`
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish)
- **Phones:** {ipa_inline}`a`, {ipa_inline}`a˥˧`, {ipa_inline}`a˥˩`, {ipa_inline}`a˧˩`, {ipa_inline}`a˩`, {ipa_inline}`b`, {ipa_inline}`d̪`, {ipa_inline}`eː`, {ipa_inline}`eː˥˧`, {ipa_inline}`eː˥˩`, {ipa_inline}`eː˧˩`, {ipa_inline}`eː˩`, {ipa_inline}`f`, {ipa_inline}`h`, {ipa_inline}`iː`, {ipa_inline}`iː˥˧`, {ipa_inline}`iː˥˩`, {ipa_inline}`iː˧˩`, {ipa_inline}`j`, {ipa_inline}`k`, {ipa_inline}`kʰ`, {ipa_inline}`l`, {ipa_inline}`m`, {ipa_inline}`n̪`, {ipa_inline}`oː`, {ipa_inline}`oː˥˧`, {ipa_inline}`oː˥˩`, {ipa_inline}`oː˧˩`, {ipa_inline}`oː˩`, {ipa_inline}`p`, {ipa_inline}`pʰ`, {ipa_inline}`r`, {ipa_inline}`s̪`, {ipa_inline}`t̪`, {ipa_inline}`t̪ʰ`, {ipa_inline}`uː`, {ipa_inline}`uː˥˧`, {ipa_inline}`uː˥˩`, {ipa_inline}`uː˧˩`, {ipa_inline}`yː`, {ipa_inline}`yː˥˧`, {ipa_inline}`yː˥˩`, {ipa_inline}`yː˧˩`, {ipa_inline}`yː˩`, {ipa_inline}`øː`, {ipa_inline}`øː˥˧`, {ipa_inline}`øː˥˩`, {ipa_inline}`øː˧˩`, {ipa_inline}`øː˩`, {ipa_inline}`ŋ`, {ipa_inline}`œ`, {ipa_inline}`œ˥˩`, {ipa_inline}`œ˧˩`, {ipa_inline}`ɑː`, {ipa_inline}`ɑː˥˧`, {ipa_inline}`ɑː˥˩`, {ipa_inline}`ɑː˧˩`, {ipa_inline}`ɑː˩`, {ipa_inline}`ɔ`, {ipa_inline}`ɔ˥˧`, {ipa_inline}`ɔ˥˩`, {ipa_inline}`ɔ˧˩`, {ipa_inline}`ɔ˩`, {ipa_inline}`ɕ`, {ipa_inline}`ɖ`, {ipa_inline}`ɛ`, {ipa_inline}`ɛː`, {ipa_inline}`ɛː˥˧`, {ipa_inline}`ɛː˥˩`, {ipa_inline}`ɛː˧˩`, {ipa_inline}`ɛ˥˧`, {ipa_inline}`ɛ˥˩`, {ipa_inline}`ɛ˧˩`, {ipa_inline}`ɛ˩`, {ipa_inline}`ɡ`, {ipa_inline}`ɧ`, {ipa_inline}`ɪ`, {ipa_inline}`ɪ˥˧`, {ipa_inline}`ɪ˥˩`, {ipa_inline}`ɪ˧˩`, {ipa_inline}`ɪ˩`, {ipa_inline}`ɭ`, {ipa_inline}`ɳ`, {ipa_inline}`ɵ`, {ipa_inline}`ɵ˥˧`, {ipa_inline}`ɵ˥˩`, {ipa_inline}`ɵ˧˩`, {ipa_inline}`ɵ˩`, {ipa_inline}`ʂ`, {ipa_inline}`ʈ`, {ipa_inline}`ʈʰ`, {ipa_inline}`ʉː`, {ipa_inline}`ʉː˥˧`, {ipa_inline}`ʉː˥˩`, {ipa_inline}`ʉː˧˩`, {ipa_inline}`ʊ`, {ipa_inline}`ʊ˥˩`, {ipa_inline}`ʊ˧˩`, {ipa_inline}`ʊ˩`, {ipa_inline}`ʋ`, {ipa_inline}`ʏ`, {ipa_inline}`ʏ˥˧`, {ipa_inline}`ʏ˥˩`, {ipa_inline}`ʏ˧˩`, {ipa_inline}`ʏ˩`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/swedish/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_swedish_mfa_dictionary_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Swedish MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Swedish/Swedish MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Swedish+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary swedish_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-swedish_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Swedish](https://en.wikipedia.org/wiki/Swedish_language) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish) phone set for Swedish, and was used in training the Swedish [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#swedish) acoustic model.
Pronunciations can be added on top of the dictionary, as long as no additional phones are introduced.

## Performance Factors

When trying to get better alignment accuracy, adding pronunciations is generally helpful, espcially for different styles and dialects.  The most impactful will be reductions that
involve deleting segments/syllables common in spontaneous speech.  Alignment must include all phones specified in the pronunciation of a word, and each phone has
a minimum duration (by default 10ms). If you have a multisyllable word going to a single syllable, it will be very hard for MFA to fit all the segments in,
so it will lead to alignment errors on adjacent words as well.

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For pronunciation dictionaries, it is often the case that transcription accuracy and lexicon coverage for the prestige variety modeled in this dictionary compared to other variants.
If you are using this dictionary in production, you should acknowledge this as a potential issue.

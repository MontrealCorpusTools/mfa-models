
# arabic.mfa

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/arabic_mfa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [IPA charts](#ipa-charts)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Arabic](https://en.wikipedia.org/wiki/Arabic)
- **Dialect:** N/A
- **Number of words:** `10,774`
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#arabic)
- **Phones:** {ipa_inline}`a`, {ipa_inline}`aː`, {ipa_inline}`b`, {ipa_inline}`bː`, {ipa_inline}`d`, {ipa_inline}`dʒ`, {ipa_inline}`dʒː`, {ipa_inline}`dː`, {ipa_inline}`dˤ`, {ipa_inline}`dˤː`, {ipa_inline}`e`, {ipa_inline}`eː`, {ipa_inline}`f`, {ipa_inline}`fː`, {ipa_inline}`h`, {ipa_inline}`iː`, {ipa_inline}`j`, {ipa_inline}`jː`, {ipa_inline}`k`, {ipa_inline}`kː`, {ipa_inline}`l`, {ipa_inline}`m`, {ipa_inline}`mː`, {ipa_inline}`n`, {ipa_inline}`nː`, {ipa_inline}`o`, {ipa_inline}`oː`, {ipa_inline}`p`, {ipa_inline}`q`, {ipa_inline}`qː`, {ipa_inline}`r`, {ipa_inline}`rː`, {ipa_inline}`s`, {ipa_inline}`sː`, {ipa_inline}`sˤ`, {ipa_inline}`sˤː`, {ipa_inline}`t`, {ipa_inline}`tʃ`, {ipa_inline}`tː`, {ipa_inline}`tˤ`, {ipa_inline}`tˤː`, {ipa_inline}`uː`, {ipa_inline}`v`, {ipa_inline}`w`, {ipa_inline}`wː`, {ipa_inline}`z`, {ipa_inline}`zː`, {ipa_inline}`æ`, {ipa_inline}`ð`, {ipa_inline}`ðː`, {ipa_inline}`ðˤ`, {ipa_inline}`ðˤː`, {ipa_inline}`ħ`, {ipa_inline}`ħː`, {ipa_inline}`ɑ`, {ipa_inline}`ɑː`, {ipa_inline}`ɡ`, {ipa_inline}`ɡː`, {ipa_inline}`ɣ`, {ipa_inline}`ɣː`, {ipa_inline}`ɪ`, {ipa_inline}`ɫː`, {ipa_inline}`ʃ`, {ipa_inline}`ʃː`, {ipa_inline}`ʊ`, {ipa_inline}`ʒ`, {ipa_inline}`ʒː`, {ipa_inline}`ʔ`, {ipa_inline}`ʕ`, {ipa_inline}`θ`, {ipa_inline}`θː`, {ipa_inline}`χ`, {ipa_inline}`χː`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/arabic/MFA/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@techreport{
	mfa_arabic_mfa_dictionary_2022,
	author={Shmueli, Natalia and McAuliffe, Michael and Sonderegger, Morgan},
	title={Arabic MFA dictionary v2.0.0},
	address={\url{https://mfa-models.readthedocs.io/pronunciation dictionary/Arabic/Arabic MFA dictionary v2_0_0.html}},
	year={2022},
	month={Mar},
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Arabic+MFA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary arabic_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-arabic_mfa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [Arabic](https://en.wikipedia.org/wiki/Arabic) transcripts.

This dictionary uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#arabic) phone set for Arabic, and was used in training the Arabic [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#arabic) acoustic model.
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


# english.us.arpa

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/dictionary/english_us_arpa.html)

Jump to section:

- [Dictionary details](#dictionary-details)
- [Intended use](#intended-use)
- [IPA charts](#ipa-charts)
- [Performance Factors](#performance-factors)
- [Ethical considerations](#ethical-considerations)

## Dictionary details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [English](https://en.wikipedia.org/wiki/English_language)
- **Dialect:** [General American English](https://en.wikipedia.org/wiki/General_American_English)
- **Number of words:** `199,880`
- **Phone set:** [ARPA](https://en.wikipedia.org/wiki/ARPABET)
- **Phones:** {ipa_inline}`AA0`, {ipa_inline}`AA1`, {ipa_inline}`AA2`, {ipa_inline}`AE0`, {ipa_inline}`AE1`, {ipa_inline}`AE2`, {ipa_inline}`AH0`, {ipa_inline}`AH1`, {ipa_inline}`AH2`, {ipa_inline}`AO0`, {ipa_inline}`AO1`, {ipa_inline}`AO2`, {ipa_inline}`AW0`, {ipa_inline}`AW1`, {ipa_inline}`AW2`, {ipa_inline}`AY0`, {ipa_inline}`AY1`, {ipa_inline}`AY2`, {ipa_inline}`B`, {ipa_inline}`CH`, {ipa_inline}`D`, {ipa_inline}`DH`, {ipa_inline}`EH0`, {ipa_inline}`EH1`, {ipa_inline}`EH2`, {ipa_inline}`ER0`, {ipa_inline}`ER1`, {ipa_inline}`ER2`, {ipa_inline}`EY0`, {ipa_inline}`EY1`, {ipa_inline}`EY2`, {ipa_inline}`F`, {ipa_inline}`G`, {ipa_inline}`HH`, {ipa_inline}`IH0`, {ipa_inline}`IH1`, {ipa_inline}`IH2`, {ipa_inline}`IY0`, {ipa_inline}`IY1`, {ipa_inline}`IY2`, {ipa_inline}`JH`, {ipa_inline}`K`, {ipa_inline}`L`, {ipa_inline}`M`, {ipa_inline}`N`, {ipa_inline}`NG`, {ipa_inline}`OW0`, {ipa_inline}`OW1`, {ipa_inline}`OW2`, {ipa_inline}`OY0`, {ipa_inline}`OY1`, {ipa_inline}`OY2`, {ipa_inline}`P`, {ipa_inline}`R`, {ipa_inline}`S`, {ipa_inline}`SH`, {ipa_inline}`T`, {ipa_inline}`TH`, {ipa_inline}`UH0`, {ipa_inline}`UH1`, {ipa_inline}`UH2`, {ipa_inline}`UW0`, {ipa_inline}`UW1`, {ipa_inline}`UW2`, {ipa_inline}`V`, {ipa_inline}`W`, {ipa_inline}`Y`, {ipa_inline}`Z`, {ipa_inline}`ZH`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/dictionary/english/us_arpa/v2.0.0/LICENSE)
- **Compatible MFA version:** `v2.0.0`
- **Citation:**

```bibtex
@article{
	gorman2011prosodylab,
	author={Gorman, Kyle and Howell, Jonathan and Wagner, Michael},
	title={Prosodylab-aligner: A tool for forced alignment of laboratory speech},
	journal={Canadian Acoustics},
	volume={39},
	number={3},
	pages={192--193},
	year={2011}
}
```

- If you have comments or questions about this dictionary or its phone set, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=English+US+ARPA+dictionary+v2.0.0) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download dictionary english_us_arpa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/dictionary-english_us_arpa-v2.0.0).

## Intended use

This dictionary is intended for forced alignment of [English](https://en.wikipedia.org/wiki/English_language) transcripts.

This dictionary uses the [ARPA](https://en.wikipedia.org/wiki/ARPABET) phone set for English, and was used in training the English [ARPA](https://en.wikipedia.org/wiki/ARPABET) acoustic model.
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

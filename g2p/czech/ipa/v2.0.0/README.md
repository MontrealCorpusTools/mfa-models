
# czech_ipa G2P model v2.0.0

Jump to section:

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Evaluation data](#evaluation-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** `Czech`
- **Trained date:** `2022-02-03`
- **Model type:** `G2P model`
- **Architecture:** `pynini`
- **Phone set:** `ipa`
- **Model version:** `v2.0.0`
- **Compatible MFA version:** `v2.0.0`
- **License:** [MIT](https://github.com/MontrealCorpusTools/mfa-models/tree/main/g2p/czech/ipa/v2.0.0/LICENSE)
- **Citation:**
  - `@techreport{MFA_czech_ipa_G2P model_2022, author={McAuliffe, Michael and Sonderegger, Morgan}, title={czech ipa MFA G2P model v2.0.0}, address={\url{https://mfa-models.readthedocs.io/}, year={2022}, month={Feb}, number={czech-ipa-2.0.0}`
- If you have comments or questions about this model, you can create an issue on [`mfa-models` issues](https://github.com/MontrealCorpusTools/mfa-models/issues).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa models download g2p czech_ipa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/g2p-czech_ipa-v2.0.0)

## Intended use

This model is intended for generating pronunciations of [Czech Language](https://en.wikipedia.org/wiki/Czech_language) transcripts.

This model uses the ipa phone set for Czech, and was trained from the [czech_ipa dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/czech_ipa.dict).
Pronunciations generated with this G2P model can be appended and used when aligning or transcribing.

## Performance Factors

The trained G2P models should be relatively quick and accurate, however the model may struggle when dealing with less common orthographic characters or word types outside of what it was trained on.
If so, you may need to supplement the dictionary through generating, correcting, and re-training the G2P model as necessary.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with word error rate and phone error rate.

## Training

This model was trained on the following data set:


* **Words:** `48,227`
* **Phones:** `47`
* **Graphemes:** `41`

## Evaluation

This model was evaluated on the following data set:


* **Words:** `5,358`
* **WER:** `0.91%`
* **PER:** `0.16%`

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise.
For G2P models, the model will only process the types of tokens that it was trained on, and will not represent the full range of text or spoken words that
native speakers will produce.
If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text may be mis-used to invade the privacy of others by recording and mining information from private conversations.
This kind of individual privacy is protected by law in may countries.
You should not assume consent to record and analyze private speech.

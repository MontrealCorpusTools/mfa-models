# English (India) MFA G2P model v2.2.1

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/g2p/english_india_mfa.html)

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
- **Language:** [English](https://en.wikipedia.org/wiki/English_language)
- **Dialect:** [Indian English](Japanese tokenizer v2_1_0.md)
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#english)
- **Model type:** `G2P model`
- **Architecture:** `phonetisaurus`
- **Model version:** `v2.2.1`
- **Trained date:** `2023-05-07`
- **Compatible MFA version:** `v2.1.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/g2p/english/india_mfa/v2.2.1/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_english_india_mfa_g2p_2023,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={English (India) MFA G2P model v2.2.1},
	address={\url{https://mfa-models.readthedocs.io/G2P model/English/English (India) MFA G2P model v2_2_1.html}},
	year={2023},
	month={May},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=English+India+MFA+G2P+model+v2.2.1) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download g2p english_india_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/g2p-english_india_mfa-v2.2.1).

## Intended use

This model is intended for generating pronunciations of [English](https://en.wikipedia.org/wiki/English_language) transcripts.

This model uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#english) phone set for English, and was trained from the pronunciation dictionaries above. Pronunciations generated with this G2P model can be appended and used when aligning or transcribing.

## Performance Factors

The trained G2P models should be relatively quick and accurate, however the model may struggle when dealing with less common orthographic characters or word types outside of what it was trained on. If so, you may need to supplement the dictionary through generating, correcting, and re-training the G2P model as necessary.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with word error rate and phone error rate.

## Training

This model was trained on the following data set:


* **Words:** `67,432`
* **Phones:** `61`
* **Graphemes:** `29`

## Evaluation

This model was evaluated on the following data set:


* **Words:** `7,493`
* **WER:** `100.00%`
* **PER:** `100.00%`

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For G2P models, the model will only process the types of tokens that it was trained on, and will not represent the full range of text or spoken words that native speakers will produce. If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

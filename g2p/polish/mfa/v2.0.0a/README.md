
# Polish MFA G2P model v2.0.0a

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/g2p/polish_mfa.html)

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
- **Language:** [Polish](https://en.wikipedia.org/wiki/Polish_language)
- **Dialect:** N/A
- **Phone set:** [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#polish)
- **Model type:** `G2P model`
- **Architecture:** `pynini`
- **Model version:** `v2.0.0a`
- **Trained date:** `2022-06-02`
- **Compatible MFA version:** `v2.0.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/g2p/polish/mfa/v2.0.0a/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_polish_mfa_g2p_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Polish MFA G2P model v2.0.0a},
	address={\url{https://mfa-models.readthedocs.io/G2P model/Polish/Polish MFA G2P model v2_0_0a.html}},
	year={2022},
	month={Jun},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Polish+MFA+G2P+model+v2.0.0a) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download g2p polish_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/g2p-polish_mfa-v2.0.0a).

## Intended use

This model is intended for generating pronunciations of [Polish](https://en.wikipedia.org/wiki/Polish_language) transcripts.

This model uses the [MFA](https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html#polish) phone set for Polish, and was trained from the pronunciation dictionaries above. Pronunciations generated with this G2P model can be appended and used when aligning or transcribing.

## Performance Factors

The trained G2P models should be relatively quick and accurate, however the model may struggle when dealing with less common orthographic characters or word types outside of what it was trained on. If so, you may need to supplement the dictionary through generating, correcting, and re-training the G2P model as necessary.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with word error rate and phone error rate.

## Training

This model was trained on the following data set:


* **Words:** `140,919`
* **Phones:** `50`
* **Graphemes:** `36`

## Evaluation

This model was evaluated on the following data set:


* **Words:** `15,657`
* **WER:** `0.77%`
* **PER:** `0.07%`

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For G2P models, the model will only process the types of tokens that it was trained on, and will not represent the full range of text or spoken words that native speakers will produce. If you are using this model in production, you should acknowledge this as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

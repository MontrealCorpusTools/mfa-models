
# Czech language model v2.0.0a

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/language_model/czech_mfa_lm.html)

Jump to section:

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/)
- **Language:** [Czech](https://en.wikipedia.org/wiki/Czech_language)
- **Model type:** `Language model`
- **Architecture:** `ngram`
- **Model version:** `v2.0.0a`
- **Trained date:** `2022-05-30`
- **Compatible MFA version:** `v2.0.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/language_model/czech/mfa/v2.0.0a/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_czech_mfa_lm_2022,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Czech language model v2.0.0a},
	address={\url{https://mfa-models.readthedocs.io/language model/Czech/Czech language model v2_0_0a.html}},
	year={2022},
	month={May},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Czech+language+model+v2.0.0a) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download language_model czech_mfa_lm
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/language_model-czech_mfa_lm-v2.0.0a).

## Intended use

This model is intended for very basic language modeling [Czech](https://en.wikipedia.org/wiki/Czech_language) transcripts.

These ngram models are far from ideal and trained on the same corpus as the acoustic models, and are provided only for completeness and in the off chance that they're useful in bootstrapping corpus development.

This language model trained with words from the pronunciation dictionaries above.

## Performance Factors

MFA language model archives contain the main large ngram model, along with two pruned versions that are used in initial decoding for performance reasons, and then later the large model is used to rescore.  If the initial decoding with the small version is causing perfomance issues, you can train a new language model with more aggressive pruning.

You should also consider training a language model on your own domain, as that will be much more representative and useful to use in decoding.

## Metrics

Perplexity for each of three component models was calculated over the training data to give a sense of its performance, but this certainly not be taken as an absolute measure of model good-ness.

### Perplexity

The following metrics were obtained on evaluation:


* **Large model:** `26.59`
* **Medium model:** `76.86`
* **Small model:** `147.04`

## Training data

This model was trained on the following data set:


* **Words:** `0`
* **OOVs:** `0`

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For this language model, this model was trained on a very specific subset of Czech at the time it was collected that will typically not represent spontaneous speech in the current time. Do not use this model in production, but if you do so, you should acknowledge bias as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

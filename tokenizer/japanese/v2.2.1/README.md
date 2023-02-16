# Japanese tokenizer v2.2.1

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/tokenizer/japanese_mfa.html)

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
- **Language:** [Japanese](https://en.wikipedia.org/wiki/Japanese_language)
- **Model type:** `Tokenizer`
- **Architecture:** `phonetisaurus`
- **Model version:** `v2.2.1`
- **Trained date:** `2023-02-16`
- **Compatible MFA version:** `v2.2.0`
- **License:** [CC BY 4.0](https://github.com/MontrealCorpusTools/mfa-models/tree/main/tokenizer/japanese//v2.2.1/LICENSE)
- **Citation:**

```bibtex
@techreport{mfa_japanese_mfa_tokenizer_2023,
	author={McAuliffe, Michael and Sonderegger, Morgan},
	title={Japanese tokenizer v2.2.1},
	address={\url{https://mfa-models.readthedocs.io/tokenizer/Japanese/Japanese tokenizer v2_2_1.html}},
	year={2023},
	month={Feb},
}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q=Japanese+tokenizer+v2.2.1) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download tokenizer japanese_mfa
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/tokenizer-japanese_mfa-v2.2.1).

## Intended use

This model is intended for very basic tokenization of [Japanese](https://en.wikipedia.org/wiki/Japanese_language) transcripts.

These tokenization models just use an ngram model for predicting word boundaries based on input text, and are provided only for completeness and in the off chance that they're useful in bootstrapping corpus development.

## Performance Factors

Third party dedicated tokenizers are likely to be more robust, but this tokenizer is more likely to work well with MFA dictionaries and acoustic models.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with utterance error rate and character error rate.

## Training data

This model was trained on the following data set:


* **Utterances:** `0`
* **Graphemes:** `0`

## Evaluation

This model was evaluated on the following data set:


* **Utterances:** `0`
* **UER:** `31.78%`
* **CER:** `1.15%`

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For this tokenizer, this model was trained on a very specific subset of Japanese at the time it was collected that will typically not represent spontaneous speech in the current time. Do not use this model in production, but if you do so, you should acknowledge bias as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

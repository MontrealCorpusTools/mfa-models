# {title}

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/tokenizer/{model_name}.html)

Jump to section:

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Ethical considerations](#ethical-considerations)
- [Troubleshooting issues](#troubleshooting-issues)

## Model details

- **Maintainer:** {maintainer}
- **Language:** {language_link}
- **Model type:** `Tokenizer`
- **Architecture:** `{architecture}`
- **Model version:** `v{version}`
- **Trained date:** `{date}`
- **Compatible MFA version:** `v{mfa_version}`
- **License:** {license_link}
- **Citation:**

```bibtex
{citation}
```

- If you have comments or questions about this model, you can check [previous MFA model discussion posts](https://github.com/MontrealCorpusTools/mfa-models/discussions?discussions_q={discussion_title}) or create [a new one](https://github.com/MontrealCorpusTools/mfa-models/discussions/new).

## Installation

Install from the [MFA command line](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/models/index.html):

```
mfa model download tokenizer {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/tokenizer-{model_name}-v{version}).

## Intended use

This model is intended for very basic tokenization of {language_link} transcripts.

These tokenization models just use an ngram model for predicting word boundaries based on input text, and are provided only for completeness and in the off chance that they're useful in bootstrapping corpus development.

## Performance Factors

Third party dedicated tokenizers are likely to be more robust, but this tokenizer is more likely to work well with MFA dictionaries and acoustic models.

## Metrics

The model was trained on 90% of the dictionary and evaluated on a held-out 10% and evaluated with utterance error rate and character error rate.

## Training data

This model was trained on the following data set:

{training_details}

## Evaluation

This model was evaluated on the following data set:

{evaluation_details}

## Ethical considerations

Deploying any model involving language into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For this tokenizer, this model was trained on a very specific subset of {language} at the time it was collected that will typically not represent spontaneous speech in the current time. Do not use this model in production, but if you do so, you should acknowledge bias as a potential issue.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

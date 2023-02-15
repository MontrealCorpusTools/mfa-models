# {title}

[Link to documentation on mfa-models](https://mfa-models.readthedocs.io/en/main/ivector/{model_name}.html)

Jump to section:

- [Model details](#model-details)
- [Installation](#installation)
- [Intended use](#intended-use)
- [Performance Factors](#performance-factors)
- [Metrics](#metrics)
- [Ethical considerations](#ethical-considerations)
- [Training data](#training-data)

## Model details

- **Maintainer:** {maintainer}
- **Language:** {language_link}
- **Model type:** `Ivector extractor`
- **Features:** `{features}`
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
mfa model download ivector {model_name}
```

Or download from [the release page](https://github.com/MontrealCorpusTools/mfa-models/releases/tag/ivector-{model_name}-v{version}).

## Intended use

This model is intended for speaker diarization and clustering.

## Performance Factors

As ivector extractors are trained on a large amount of data and without reference to language-specific resources, they **may** be useful outside of the specific language variety being trained, however, differences in the languages may impact performance. Particularly sociolinguistic aspects related to identity presentation, the linguistic status voice quality (breathy, creaky modal), and non-linguistic factors like recording conditions and microphone response may affect diarization performance across languages.

## Metrics

Speaker diarization systems are evaluated through Equal Error Rate (EER), the error when false accept rate is equal to the false rejection rate.

- **EER:** `0%`

## Ethical considerations

Deploying any Speech-to-Text model into any production setting has ethical implications. You should consider these implications before use.

### Demographic Bias

You should assume every machine learning model has demographic bias unless proven otherwise. For ivector extraction models, diarization of male speakers generally has better performance than diarization of female speakers, even with equal amounts of training data.

### Surveillance

Speech-to-Text technologies may be misused to invade the privacy of others by recording and mining information from private conversations. This kind of individual privacy is protected by law in many countries. You should not assume consent to record and analyze private speech.

## Training data

This model was trained on the following corpora:

{corpora_details}

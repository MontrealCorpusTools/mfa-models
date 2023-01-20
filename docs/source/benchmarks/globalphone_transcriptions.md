
(gp_transcription_benchmarks=)
# GlobalPhone transcription benchmarks


MFA has some simple language model training and transcription capabilities in addition to its alignment functionalities.  The Word Error Rate (WER) and Character Error Rate was calculated over the Buckeye and TIMIT corpora below.  Note that unlike the [English transcription benchmarks](english_transcriptions.md), these datasets were included in the training data, and hence will not be representative of use on your own datasets. The reason for training on GlobalPhone is that many of the languages here have very little data outside of it, and so sacrificing user's alignment performance for the benefit of cleaner benchmark metrics does not seem worth it to me.

## Datasets

The following datasets were used in evaluation:

* {need}`GlobalPhone Bulgarian v3_1`
* {need}`GlobalPhone Croatian v3_1`
* {need}`GlobalPhone Czech v3_1`
* {need}`GlobalPhone French v3_1`
* {need}`GlobalPhone German v3_1`
* {need}`GlobalPhone Hausa v3_1`
* {need}`GlobalPhone Korean v3_1`
* {need}`GlobalPhone Chinese-Mandarin v3_1`
* {need}`GlobalPhone Polish v3_1`
* {need}`GlobalPhone Portuguese (Brazilian) v3_1`
* {need}`GlobalPhone Russian v3_1`
* {need}`GlobalPhone Spanish (Latin American) v3_1`
* {need}`GlobalPhone Swahili v3_1`
* {need}`GlobalPhone Swedish v3_1`
* {need}`GlobalPhone Thai v3_1`
* {need}`GlobalPhone Turkish v3_1`
* {need}`GlobalPhone Ukrainian v3_1`
* {need}`GlobalPhone Vietnamese v3_1`

Please note that there were a number of fixes for these corpora to clean them up and ensure that they worked properly.  See [Aanchan Mohan](https://www.khoury.northeastern.edu/people/aanchan-mohan/)'s [write up of GlobalPhone corpus fixes](https://wiki.inf.ed.ac.uk/CSTR/GlobalPhone).  Also note that the evaluations here use the version of GlobalPhone from 2015 (listed in the manual as 3.1), not the 2017 version (listed on ELRA as 1.0).

```{warning}

The evaluation data here was included in the training for all models, and so it not likely to be fully representative of performance on your data.  See [English transcription benchmarks](english_transcriptions.md) for a transcription evaluation on unseen data.
```

## Experimental set up

* Each language had a trained language model on just the GlobalPhone data using the MFA lexicons as input to make them maximally comparable (as the GlobalPhone lexicons are tailored to this particular corpus)
  * Mandarin was trained on Pinyin romanization and Pinyin phones in 1.0 following GlobalPhone's lexicon, so a separate language model was trained on the romanized transcripts for the 1.0 Mandarin GP evaluation
* Models
  * Bulgarian
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/bulgarian.zip)
    * {need}`Bulgarian MFA acoustic model v2_0_0`
    * {need}`Bulgarian MFA acoustic model v2_0_0a`
  * Croatian
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/croatian.zip)
    * {need}`Croatian MFA acoustic model v2_0_0`
    * {need}`Croatian MFA acoustic model v2_0_0a`
  * Czech
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/czech.zip)
    * {need}`Czech MFA acoustic model v2_0_0`
    * {need}`Czech MFA acoustic model v2_0_0a`
  * French
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/french.zip)
    * {need}`French MFA acoustic model v2_0_0`
    * {need}`French MFA acoustic model v2_0_0a`
  * German
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/german.zip)
    * {need}`German MFA acoustic model v2_0_0`
    * {need}`German MFA acoustic model v2_0_0a`
  * Hausa
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/hausa.zip)
    * {need}`Hausa MFA acoustic model v2_0_0`
    * {need}`Hausa MFA acoustic model v2_0_0a`
  * Korean
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/korean.zip)
    * {need}`Korean MFA acoustic model v2_0_0`
    * {need}`Korean MFA acoustic model v2_0_0a`
  * Mandarin
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/mandarin.zip)
    * {need}`Mandarin MFA acoustic model v2_0_0`
    * {need}`Mandarin MFA acoustic model v2_0_0a`
  * Polish
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/polish.zip)
    * {need}`Polish MFA acoustic model v2_0_0`
    * {need}`Polish MFA acoustic model v2_0_0a`
  * Portuguese
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/portuguese.zip)
    * {need}`Portuguese MFA acoustic model v2_0_0`
    * {need}`Portuguese MFA acoustic model v2_0_0a`
  * Russian
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/russian.zip)
    * {need}`Russian MFA acoustic model v2_0_0`
    * {need}`Russian MFA acoustic model v2_0_0a`
  * Spanish
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/spanish.zip)
    * {need}`Spanish MFA acoustic model v2_0_0`
    * {need}`Spanish MFA acoustic model v2_0_0a`
  * Swahili
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/swahili.zip)
    * {need}`Swahili MFA acoustic model v2_0_0`
    * {need}`Swahili MFA acoustic model v2_0_0a`
  * Swedish
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/swedish.zip)
    * {need}`Swedish MFA acoustic model v2_0_0`
    * {need}`Swedish MFA acoustic model v2_0_0a`
  * Thai
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/thai.zip)
    * {need}`Thai MFA acoustic model v2_0_0`
    * {need}`Thai MFA acoustic model v2_0_0a`
  * Turkish
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/turkish.zip)
    * {need}`Turkish MFA acoustic model v2_0_0`
    * {need}`Turkish MFA acoustic model v2_0_0a`
  * Ukrainian
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/ukrainian.zip)
    * {need}`Ukrainian MFA acoustic model v2_0_0`
    * {need}`Ukrainian MFA acoustic model v2_0_0a`
  * Vietnamese
    * [GP 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/vietnamese.zip)
    * {need}`Vietnamese MFA acoustic model v2_0_0`
    * {need}`Vietnamese MFA acoustic model v2_0_0a`

## Benchmarks

### Word error rate

In general we see improvements from the GlobalPhone lexicon-based models to the 2.0 MFA phone sets, particularly for East Asian character based models (Thai, Vietnamese, Korean), along with big improvements for Ukrainian and Bulgarian.  Mandarin is better under GlobalPhone's approach, however, suggesting that there's likely gaps in the Hanzi-based lexicon used in the latest versions.  We can also a increase error rate for some languages using the 2.0 trained models due to a bug in silence estimation, but 2.0a improves performance to below the 1.0 baseline.

```{note}

To make the points easier to see, Korean 1.0 GP results have been excluded.  For word error rate, it was much higher than any other model, at 28.3%. The primary factor going into its poor performance is likely the lexicon, that often has plain stops for tense ones.
```

```{image} ../_static/benchmarks/mfa2_gp_transcription_wer.svg
:alt: Word error rate of models from 1.0 based on GlobalPhone lexicons and 2.0 MFA systems.
:align: center
```

### Character error rate

Character error rate shows similar patterns to the word error rate analysis, but it does exacerbate the discrepancies for Mandarin between Pinyin and Hanzi-based lexicons, as Hanzi character substitutions will be more costly than Pinyin substitutions.

```{note}

As above, Korean 1.0 GP results have been excluded.  For character error rate, it was much higher than any other model, at 23.1%, for the same reasons above.
```

```{image} ../_static/benchmarks/mfa2_gp_transcription_cer.svg
:alt: Character error rate of models from 1.0 based on GlobalPhone lexicons and 2.0 MFA systems.
:align: center
```

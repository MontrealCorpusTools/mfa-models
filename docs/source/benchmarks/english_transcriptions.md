
(english_transcription_benchmarks=)
# English transcription benchmarks

MFA has some simple language model training and transcription capabilities in addition to its alignment functionalities.  The Word Error Rate (WER) and Character Error Rate was calculated over the Buckeye and TIMIT corpora below.  Note that unlike the [](globalphone_transcriptions.md#gp-transcription-benchmarks), these datasets are unseen.


```{seealso}

For more details, please see the [docs for the aligner's transcription mode](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/transcribing.html#transcribe-audio-files-mfa-transcribe).
```

## Datasets

### Buckeye

The first dataset used for this benchmark is the {need}`Buckeye Corpus`.  The Buckeye Corpus is spontaneous speech from speakers in Columbus, Ohio collected in the summer of 2000.  There are 20 male speakers, 20 female speakers, with equal numbers of "old" and "young" speakers.  Socio-economic class was not controlled for, but most speakers are reported to be middle class to upper working class.

```{warning}

No details on the race of participants are reported anywhere in the Buckeye Corpus literature, suggesting that all participants are white. As this corpus is tailored to an extremely specific variation of American English, please use caution in interpreting the results as they may relate to other languages.
```

The Buckeye Corpus can be obtained through [their website](https://buckeyecorpus.osu.edu/) once you agree to their license.  The state that is downloadable has a number of transcription errors and formatting issues. A {download}`git patch <../_static/benchmarks/buckeye.patch>` addresses these, which fixes inconsistencies in their transcription (the occasional ``nx``, ``h`` phones, lines missing phone/word entries, etc), removing any transcriptions beyond the end of the sound file, and some reannotations of gross errors (i.e., transcripts appearing more than a second before they are said in the audio, words annotated as laughter or vocnoise even though they're largely intelligible and have phones annotated).  Once the transcription files are patched, you can use [the scripts on Github](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks).

The phoneset mapping files for the Buckeye phoneset are available for [ARPA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_brtenchmarks/mapping_files/arpa_buckeye_mapping.yaml) and [MFA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/mfa_buckeye_mapping.yaml).

### TIMIT

The first dataset used in the benchmark is the {need}`TIMIT`.

```{warning}

It is strongly recommended that you do not use TIMIT benchmarking to inform your decisions regarding model performance.  It was constructed to be "phonetically balanced" at the sacrifice of naturalistic speech, and so the sentences are extremely convoluted with odd syntax. Speakers have an extremely slow speech rate and tend much more towards citation form than even other read speech corpora of sentences from newspapers. Newspaper text is also not suited for speech, but it is better than TIMIT's sentences.

There is also only 5 hours of data and it is heavily skewed towards male voices (438 male speakers, 192 female speakers), leaving aside the racial and dialectal selection bias present (578 speakers were marked as White, 26 as Black, 3 as Asian, 2 as Native American, 4 as Hispanic, and 17 as Unknown).

TIMIT is presented here solely completeness because there has historically been a odd fascination with benchmarking on it.  You should be wary of any model that reports only TIMIT results, as it is not representative of American English speech, let alone speech in general.
```

The phoneset mapping files for the TIMIT phoneset are available for [ARPA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/arpa_timit_mapping.yaml) and [MFA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/mfa_timit_mapping.yaml).

```{note}

I do not know at this point how to reformat TIMIT to usable.  I know that the version that is downloadable does not have properly formatted WAV files, and as I recall, requires modifying the headers to work, but SoX might be able to read them.
```

## Experimental set up

* All models used either a language model trained the Buckeye corpus or on the TIMIT corpus
* Models
  * ARPA 1.0
    * Used the `english` acoustic model and `english` pronunciation dictionary distributed with MFA 1.0 that were trained on {need}`LibriSpeech English` using the [Prosodylab ARPA dictionary](https://github.com/MontrealCorpusTools/mfa-models/blob/main/dictionary/english.dict?raw=true)
  * {need}`English (US) ARPA acoustic model v2_0_0`
  * {need}`English (US) ARPA acoustic model v2_0_0a`
  * {need}`English MFA acoustic model v2_0_0`
  * {need}`English MFA acoustic model v2_0_0a`

## Benchmarks

### Word error rate

Both 2.0 MFA English models show the best performance on Buckeye, with slightly worse performance on TIMIT.  The ARPA models are trained on read General American speech ({need}`LibriSpeech English`), which aligns more closely with the TIMIT format.  The MFA models are trained on A) more dialects of English, and B) more spontaneous speech, so the increased Buckeye performance at the cost of TIMIT performance is not surprising.

```{image} ../_static/benchmarks/mfa2_english_transcription_wer.svg
:alt: Word error rate of models from 1.0 and 2.0 MFA systems.
:align: center
```

### Character error rate

Character error rate shows similar performance as word error rate, except that the CER is lower across the board for Buckeye than WER, while TIMIT is basically at floor and doesn't show much difference.

```{image} ../_static/benchmarks/mfa2_english_transcription_cer.svg
:alt: Character error rate of models from 1.0 and 2.0 MFA systems.
:align: center
```

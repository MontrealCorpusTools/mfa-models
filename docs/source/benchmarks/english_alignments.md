
(english_alignment_benchmarks=)
# English alignment benchmarks

## Datasets

### Buckeye

The first dataset used for this benchmark is the {need}`Buckeye Corpus`.  The Buckeye Corpus is spontaneous speech from speakers in Columbus, Ohio collected in the summer of 2000.  There are 20 male speakers, 20 female speakers, with equal numbers of "old" and "young" speakers.  Socio-economic class was not controlled for, but most speakers are reported to be middle class to upper working class.

```{warning}

No details on the race of participants are reported anywhere in the Buckeye Corpus literature, suggesting that all participants are white. As this corpus is tailored to an extremely specific variation of American English, please use caution in interpreting the results as they may relate to other languages.
```

The Buckeye Corpus can be obtained through [their website](https://buckeyecorpus.osu.edu/) once you agree to their license.  The state that is downloadable has a number of transcription errors and formatting issues. A {download}`git patch <../_static/benchmarks/buckeye.patch>` addresses these, which fixes inconsistencies in their transcription (the occasional ``nx``, ``h`` phones, lines missing phone/word entries, etc), removing any transcriptions beyond the end of the sound file, and some re-annotations of gross errors (i.e., transcripts appearing more than a second before they are said in the audio, words annotated as "laughter" or "vocnoise" even though they're largely intelligible and have phones annotated).  Once the transcription files are patched, you can use [the scripts on Github](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks).

The phoneset mapping files for the Buckeye phoneset are available for [ARPA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_brtenchmarks/mapping_files/arpa_buckeye_mapping.yaml) and [MFA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/mfa_buckeye_mapping.yaml).

(timit=)
### TIMIT

The second dataset used in the benchmark is the {need}`TIMIT`.

```{warning}

It is strongly recommended that you do not use TIMIT benchmarking to inform your decisions regarding model performance.  It was constructed to be "phonetically balanced" at the sacrifice of naturalistic speech, and so the sentences are extremely convoluted with odd syntax. Speakers have an extremely slow speech rate and tend much more towards citation form than even other read speech corpora of sentences from newspapers. Newspaper text is also not suited for speech, but it is better than TIMIT's sentences.

There is also only 5 hours of data and it is heavily skewed towards male voices (438 male speakers, 192 female speakers), leaving aside the racial and dialectal selection bias present (578 speakers were marked as White, 26 as Black, 3 as Asian, 2 as Native American, 4 as Hispanic, and 17 as Unknown).

TIMIT is presented here solely completeness because there has historically been a odd fascination with benchmarking on it.  You should be wary of any model that reports only TIMIT results, as it is not representative of American English speech, let alone speech in general.
```

The phoneset mapping files for the TIMIT phoneset are available for [ARPA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/arpa_timit_mapping.yaml) and [MFA](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/mfa_timit_mapping.yaml).

```{note}

I do not know at this point how to reformat TIMIT to usable.  I know that the version that is downloadable does not have properly formatted WAV files, and as I recall, requires modifying the headers to work, but SoX might be able to read them.
```

## Benchmarks

These benchmarks were performed using [MFA v2.0.0rc8](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v2.0.0rc8), which was used to train the latest {need}`English MFA acoustic model v2_0_0a` and {need}`English (US) ARPA acoustic model v2_0_0a`.  The 1.0 models were trained and released as part of [MFA v1.0.1](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v1.0.1).  The older {need}`English MFA acoustic model v2_0_0` and {need}`English (US) ARPA acoustic model v2_0_0` were trained as part of the [MFA v2.0.0rc5](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v2.0.0rc5) release.

### Alignment score

Alignment score represents the average boundary error between the reference alignment and the aligner's output. The two phone sequences are aligned with [BioPython's pairwise2 module](https://biopython.org/docs/1.75/api/Bio.pairwise2.html) using the [mapping files](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files) to establish "identical" phones across the different phone sets.  Then alignment score is calculated as the average distance of the average start and end boundary distance to the reference phone's start and end. Thus, it can be interpreted as the average error in seconds per boundary.

After bug fixes in [MFA v2.0.0rc8](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v2.0.0rc8) that improved both the performance of 2.0+ models and 1.0 models, we can see the effect of a bug in silence calculation in 2.0 models that was affecting performance.  MFA 2.0a models show a significant improvement over their 2.0 counterparts.  For TIMIT, the ARPA 2.0a performs better than the MFA 2.0a model, but see [my caveats above](#timit) for not considering this a big deal, considering that MFA 2.0a outperforms ARPA 2.0a by a similar margin for the larger corpus of spontaneous speech.

```{seealso}

For more details, please see the [docs for the aligner's evaluation mode](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/alignment.html#evaluation-mode), and the [original blog post on alignment score](https://memcauliffe.com/update-on-montreal-forced-aligner-performance.html).
```

```{image} ../_static/benchmarks/mfa2_english_alignment_score.svg
:alt: English alignment scores across model versions. The MFA 1.0 model using the ARPA lexicon has a mean error of 20.7 ms on Buckeye and 17.8 ms on TIMIT.  English ARPA 2.0 model has a mean error of 21.5 ms on Buckeye and 18.7 ms on TIMIT, which improves using the 2.0a models to 19.9 ms on Buckeye and 17.0 ms on TIMIT. Finally, English MFA 2.0 model using the US MFA dictionary has a mean error of 20.6 ms on Buckeye and 19.2 ms on TIMIT, whihch improves using the 2.0a models to 19.4 ms on Buckeye and 17.6 ms on TIMIT.
:align: center
```

### Phone error rate

Phone error rate uses the alignment between reference phones and the aligner's phone output from the [BioPython's pairwise2 module](https://biopython.org/docs/1.75/api/Bio.pairwise2.html) using the [mapping files](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files) to establish "identical" phones across the different phone sets.  Phone error rate for an utterance is the number of "identical" phones aligned divided by the number of phones in the reference alignment.

```{seealso}

For more details, please see the [docs for the aligner's evaluation mode](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/alignment.html#evaluation-mode).
```

In general, phone error rate is higher on the Buckeye Corpus than TIMIT, due to the conversational nature of Buckeye and the closer transcription (see [Montreal-Forced-Aligner #440](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/issues/440) for examples of TIMIT's annotation not being fully phonetic with respect to {ipa_inline}`/ð/`).  Models with MFA phone set have lower phone error rates across corpora than ARPA based models, because MFA has more pronunciation variants and phonetic forms.  As an example, syllabic sonorants are not represented in ARPA, but then are in MFA, TIMIT, and Buckeye phone sets. For instance, the word "bottle" is represented as {ipa_inline}`[B AA1 T AH0 L]` in ARPA, but {ipa_inline}`[b ɑ t ɫ̩]` in MFA and {ipa_inline}`[b aa dx el]` in both Buckeye and TIMIT.

```{image} ../_static/benchmarks/mfa2_english_phone_error_rate.svg
:alt: English phone error rates across model versions. The MFA 1.0 model using the ARPA lexicon has a phone error rate of 37.9% on Buckeye and 26.8% on TIMIT.  English ARPA 2.0 model has a phone error rate of 38.2% on Buckeye and 27.3% on TIMIT, which stays consistent using the 2.0a models to 38.1% on Buckeye and 27.3% on TIMIT. Finally, English MFA 2.0 model using the US MFA dictionary has a phone error rate of 37.0% on Buckeye and 25.7% on TIMIT, which likewise stays consistent using the 2.0a models to 37.2% on Buckeye and 25.5% on TIMIT.
:align: center
```

### Word alignment comparison with SOTA ASR models

There are several state of the art ASR models that support generating word-level alignments:

1. {xref}`whisperx`
   * Model used in alignment is [WAV2VEC2_ASR_BASE_960H](https://pytorch.org/audio/stable/generated/torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H.html)
2. {xref}`nemo`
    * Model used in alignment is [stt_en_fastconformer_hybrid_large](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_fastconformer_hybrid_large_streaming_1040ms)
3. {xref}`wav2vec2`
   * Model used in alignment is [MMS_FA](https://pytorch.org/audio/main/generated/torchaudio.pipelines.MMS_FA.html#torchaudio.pipelines.MMS_FA)

As WhisperX uses a Wav2Vec2 model for alignments and we're evaluating based on ground truth transcripts rather than the transcription output of Whisper, technically "WhisperX" will refer to the performance of the English Wav2Vec2 model.  The Wav2Vec2 model that WhisperX uses was trained on {need}`Librispeech English`, whereas the {xref}`wav2vec2` model was trained on a large multilingual dataset.

The MFA conditions being compared are:

1. [ARPA 1.0](https://github.com/MontrealCorpusTools/mfa-models/releases/download/acoustic-archive-v1.0/english.zip) with {need}`English (US) ARPA dictionary v3_0_0`
   * Trained on {need}`Librispeech English` like WhisperX's alignment model
2. {need}`English (US) ARPA acoustic model v3_0_0` with {need}`English (US) ARPA dictionary v3_0_0`
   * Trained on {need}`Librispeech English` like WhisperX's alignment model
3. {need}`English MFA acoustic model v3_0_0` with {need}`English (US) MFA dictionary v3_0_0`
   * Trained on a larger multi-dialectal English dataset

All MFA evaluations were run using MFA 3.1.0.

```{image} ../_static/benchmarks/word_alignment.svg
:alt: English word-level alignment scores across multiple SOTA ASR systems compared to MFA.
:align: center
```

The following table has the mean word boundary errors in milliseconds from the plot above.

```{csv-table} Average word boundary error (ms)
:file: ../_static/benchmarks/word_alignment.csv
:header-rows: 1
:stub-columns: 2
:align: center
```

Recent ASR models are not particularly accurate for alignment, even at the word level.  Any conformer architecture is going to introduce more time alignment errors as it is less anchored to linear time than Wav2Vec2/RNN-based architectures.  Additionally, all SOTA models are end-to-end models that generate English orthography which does not map transparently to pronounced sounds (i.e., "gh" characters in "cough" vs "though" or "through"). ASR models in general are trained to optimize word error rate (WER), however the transcripts they are trained on are often not particularly accurate from a signal perspective, with hesitations, filler words, and restarts removed, so generally the better WER performance by conformer models in recent years is likely due to being better able to predict the inaccurate transcripts.

All these factors lead to better alignment accuracy by MFA models, even those trained in version 1.0.  The ARPA 3.0 model shows the best performance across both corpora, as it was trained solely on the same dialects as both corpora.  All models show better performance on TIMIT over Buckeye, owing to TIMIT's more constructed utterances.

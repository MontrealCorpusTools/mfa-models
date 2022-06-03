
(korean_alignment_benchmarks=)
# Korean alignment benchmarks

## Dataset

The dataset used for this benchmark is the {need}`Seoul Corpus`.  The Seoul Corpus was modeled off of the {need}`Buckeye Corpus` to create a phonetically/phonemically hand-aligned corpus of Seoul Korean.  The corpus consists of 40 speakers of Seoul Korean with 20 male speakers and 20 female speakers, along with 10 speakers each in their teens, twenties, thirties and forties.  Similar to the Buckeye Corpus, socio-economic class was also not controlled, but the setting of academic sociolinguistic interviews will bias towards middle to upper class.

The corpus was transribed in Hangul and aligned in HTK, and then corrected by hand.  The transcription is more phonemic than the Buckeye Corpus's phone set (though, even the final Buckeye phone set is not as as phonetic as the original TIMIT-based set they used).

The dataset is freely available on [OpenSLR](http://www.openslr.org/113/).  The [reorganization script here](https://github.com/mmcauliffe/corpus-creation-scripts/blob/main/korean_corpora/reorg_seoul_corpus.py) is the basis of the testing data, and creates input TextGrids to align and reference textgrids to compare against in [the alignment evaluation script](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/benchmark_korean_alignment.py), along with the necessary mapping files to the Seoul Corpus phone set from [MFA's phone set](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/korean_mfa_mapping.yaml) and [GlobalPhone's phone set](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files/korean_gp_mapping.yaml).


## Benchmarks

These benchmarks were performed using [MFA v2.0.0rc8](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v2.0.0rc8), which was used to train the latest {need}`Korean MFA acoustic model v2_0_0a`.  The Korean 1.0 models were trained and released as part of [MFA v1.0.1](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v1.0.1) and used the GlobalPhone Korean lexicon.  The {need}`Korean MFA acoustic model v2_0_0` was trained as part of the [MFA v2.0.0rc5](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/tag/v2.0.0rc5) release.

```{note}

This benchmark is not particularly great, because the Seoul Corpus is used as training data for the Korean MFA models.  The reason for this choice is due to the limited data for Korean speech over all, so the Seoul Corpus accounts for 36% of the training hours in the Korean MFA model.

I'd rather have a better model with 119 hours of training data for Korean than a more accurate benchmark for a model with 76 hours of training data in this case, but see [](english_alignments.md#english-alignment-benchmarks) for an alignment benchmark on unseen data for American English.
```

### Alignment score

Alignment score represents the average boundary error between the reference alignment and the aligner's output. The two phone sequences are aligned with [BioPython's pairwise2 module](https://biopython.org/docs/1.75/api/Bio.pairwise2.html) using the [mapping files](https://github.com/MontrealCorpusTools/mfa-models/tree/main/scripts/alignment_benchmarks/mapping_files) to establish "identical" phones across the different phone sets.  Then alignment score is calculated as the average distance of the average start and end boundary distance to the reference phone's start and end. Thus, it can be interpreted as the average error in seconds per boundary.

Korean 2.0 MFA models vastly outperform 1.0 GlobalPhone models for several reasons:

1. 1.0 GlobalPhone model was not trained on the Seoul Corpus, but MFA models were.  However, original testing of the alignment scores for MFA 2.0 had alignment scores ~30ms, so the later versions still would outperform the 1.0 GlobalPhone without cheating by training on the test data.
2. The GlobalPhone lexicon does not have great coverage of the Seoul Corpus, as it was created for the GlobalPhone corpus specifically, so a number of unknown words affect its performance.
3. Additionally, there are a number of errors in the GlobalPhone lexicon that lead to reduced performance:
   1. Some tense stops {ipa_inline}`ㅃ /p͈/`, {ipa_inline}`ㄸ /t͈/`, and {ipa_inline}`ㄲ /k͈/` transcribed as {ipa_inline}`B`, {ipa_inline}`D`, and {ipa_inline}`G` instead of {ipa_inline}`BB`, {ipa_inline}`DD`, and {ipa_inline}`GG`, respectively, based on their documentation.
   2. The grapheme {ipa_inline}`ㄹ /l~ɾ/` is sometimes transcribed in GlobalPhone as {ipa_inline}`[N]` instead of {ipa_inline}`[L]` or {ipa_inline}`[R]` (regardless of phonological context, like at the beginning of a word).
   3. Some characteristics of the vowels in their documentation are not accurate. There's no length distinction, and the closest examples in English don't align ("IPA" {ipa_inline}`e` -> GP {ipa_inline}`E` -> English "bet" {ipa_inline}`/b ε t/`, "IPA" {ipa_inline}`ε` -> GP {ipa_inline}`AE` -> English "cat" {ipa_inline}`/k æ t/`).

```{seealso}

For more details, please see the [docs for the aligner's evaluation mode](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/alignment.html#evaluation-mode), and the [original blog post on alignment score](https://memcauliffe.com/update-on-montreal-forced-aligner-performance.html).
```

```{image} ../_static/benchmarks/mfa2_korean_alignment_score.svg
:alt: Korean alignment scores across model versions.  The MFA 1.0 model using the GlobalPhone lexicon has a mean error of 42.3 ms per boundary.  Korean MFA 2.0 model has a mean error of 21.9 ms per boundary, and Korean MFA 2.0a model has a mean error of 19.6 ms per boundary.
:align: center
```

### Phone error rate

```{image} ../_static/benchmarks/mfa2_korean_phone_error_rate.svg
:alt: Korean phone error rates across model versions.  The MFA 1.0 model using the GlobalPhone lexicon has a mean phone error rate of 43.2%.  Korean MFA 2.0 model has a mean phone error rate of 13.3%, and Korean MFA 2.0a model has a mean phone error rate of 10.7%.
:align: center
```

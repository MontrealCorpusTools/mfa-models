# Data preparation scripts

## Buckeye

The Buckeye Corpus is available from https://buckeyecorpus.osu.edu/, which requires an account to download zip files.  Once you download and extract the files in a flat structure, apply the git patch provided in this directory.

The workflow would be something like:

```commandline
cd /path/to/buckeye/corpus
git init
git add .
git commit -m "Initial commit"
git apply /path/to/buckeye.patch
```

At this point you will have all the corrections that I've made to the Buckeye Corpus.  These are things like fixing errors in line formatting, misaligned sections, typos, etc.  However, it's important to note that these corrections are optimized for alignment training/evaluation and not for phonetic analysis.  One crucial change is that if a speaker is laughing during speaking, the original Buckeye puts all words into a single `<LAUGH-laughed-through-these-words`, however, since the phone labels are intact for these sections, I have split those into the relevant word tags.  For alignment, variation in production is important, especially given the more casual style in the Buckeye Corpus, while for phonetic analysis there can be arguments made for excluding these tokens.  The same logic applies to recognizable tokens that were excised in the original via `<NOISE>`, `<EXT>` or some other tag (but these are typically taken care of in `create_buckeye_benchmark.py`)

Once the patch is applied, you can run the `create_buckeye_benchmark.py` via:

```commandline
conda create -n buckeye_reorg python=3.11 pysoundfile praatio
conda activate buckeye_reorg
python create_buckeye_benchmark.py /path/to/buckeye/corpus /path/to/new/benchmark /path/to/new/reference
```

You can omit the conda environment creation if you have pysoundfile and praatio installed for your python already.  The newly created benchmark and reference directories will have the following files:

```
benchmark
    - s01
        - s0101a.TextGrid
        - s0101a.wav
        - s0101b.TextGrid
        - s0101b.wav
        ...
    - s02
        - s0201a.TextGrid
        - s0201a.wav
        ...
    ...
reference
    - s01
        - s0101a.TextGrid
        - s0101b.TextGrid
        ...
    - s02
        - s0201a.TextGrid
        ...
    ...
```

The benchmark folder contains the sound files and TextGrids with utterances that have been created, but no word or phone alignments.  Instead, these alignments are in the TextGrid files in the reference directory.  These can be used as inputs to [evaluating alignments in MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/implementations/alignment_evaluation.html#alignment-evaluation).


# Montreal Forced Aligner Models

::::{grid} 2
:::{grid-item-card}  Dictionaries
:text-align: center
:class-card: sd-text-dark

{fas}`spell-check;fa-6x i-navigation`
^^^

Pronunciation dictionaries for use with MFA
+++
```{button-ref} dictionary
:expand:
:color: primary
Browse dictionaries
```
:::

:::{grid-item-card}  Grapheme-to-phoneme models
:text-align: center
:class-card: sd-text-dark

{fas}`tower-cell;fa-6x i-navigation`
^^^
G2P models can supplement dictionaries with new pronunciations

+++
```{button-ref} g2p
:expand:
:color: primary
Browse G2P models
```
:::

:::{grid-item-card}  Acoustic models
:text-align: center
:class-card: sd-text-dark

{fas}`microphone-alt;fa-6x i-navigation`
^^^
Pretrained acoustic models trained on ASR corpora

+++
```{button-ref} acoustic
:expand:
:color: primary
Browse acoustic models
```
:::

:::{grid-item-card}  Language models
:text-align: center
:class-card: sd-text-dark

{fas}`language;fa-6x i-navigation`
^^^
Language models alongside the acoustic models

+++
```{button-ref} language_model
:expand:
:color: primary
Browse language models
```
:::

:::{grid-item-card}  Ivector extractors
:text-align: center
:class-card: sd-text-dark

{fas}`arrows-down-to-people;fa-6x i-navigation`
^^^
Ivector extractors for speaker diarization

+++
```{button-ref} ivector
:expand:
:color: primary
Browse ivector extractors
```
:::

:::{grid-item-card}  Tokenizers
:text-align: center
:class-card: sd-text-dark

{fas}`text-width;fa-6x i-navigation`
^^^
Tokenizers for generating word boundaries

+++
```{button-ref} tokenizer
:expand:
:color: primary
Browse tokenizers
```
:::

:::{grid-item-card}  Corpora
:text-align: center
:class-card: sd-text-dark

{fas}`globe;fa-6x i-navigation`
^^^
Corpora used in model training

+++
```{button-ref} corpus
:expand:
:color: primary
Browse training corpora
```
:::
::::

```{toctree}
:hidden:

Dictionaries <dictionary/index.rst>
G2P models <g2p/index.rst>
Acoustic models <acoustic/index.rst>
Language models <language_model/index.rst>
Ivector extractors <ivector/index.rst>
Tokenizers <tokenizer/index.rst>
Benchmarks <benchmarks/index.rst>
Corpora <corpus/index.rst>
```

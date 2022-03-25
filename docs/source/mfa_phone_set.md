# MFA IPA phone set

For its IPA models, MFA uses an opinionated IPA phone set.  This page will cataloge the way that phones are represented across languages (and note any deviations from them).  The guiding principle is to have general consistency in phones across languages, but allow for phonetic specification where it A) matters for the language and B) aids the aligner in assigning HMM states to phones.

For most languages, dictionaries were constructed from the [Wikipron](https://github.com/CUNY-CL/wikipron/tree/master/data/scrape) scraped dictionaries.  However, given that they are crowd-sourced transcriptions from [Wiktionary](https://en.wiktionary.org/), there was a fair bit of noise to clean up.

```{warning}
This page is under heavy construction as more languages get trained, so many languages are missing or have incomplete entries below.
```

## General notes

* **Diacritic ordering:** The ordering of diacritics is {ipa_inline}`(prenasalization) symbol (secondary place) (glottal settings) (length)`
  * {ipa_inline}`pʰː`
  * {ipa_inline}`pʷʼ`
  * {ipa_inline}`pʲ̚`
  * {ipa_inline}`ⁿd̪ʷʱː`
* **Removal of narrow transcription diacritics:**
  * Height markers on vowels and consonants
    * {ipa_inline}`[o̞]` {ipa_icon}`right-arrow` {ipa_inline}`[o]` in various languages
    * {ipa_inline}`[ɾ̝̊]` {ipa_icon}`right-arrow` {ipa_inline}`[ɾ]` in Turkish
    * {ipa_inline}`[ɯ̟̃ᵝ ɨ̥ᵝ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɯ]` or {ipa_inline}`[ɨ]` depending on surrounding context in Japanese
  * Removal of nasality in languages where it's not phonemic
  * Merging some non-phonemic or dialectal contrasts
    * {ipa_inline}`[ʍ]` {ipa_icon}`right-arrow`  {ipa_inline}`[w]` in English
    * {ipa_inline}`[r]` {ipa_icon}`right-arrow` {ipa_inline}`[ʁ]` in French
    * {ipa_inline}`[ʁ ɹ ɻ χ ɦ h r]` {ipa_icon}`right-arrow` {ipa_inline}`[x]` in Brazilian Portuguese
  * Standardizing diphthongs, afficates, etc
    * Merging sequences of {ipa_inline}`[a ʊ]` into a single {ipa_inline}`[aw]` phone
    * Merging sequences of vowels in Mandarin to single nucleus
  * Standardizing tones
    * Transforming all tones to Chao system (i.e. Mandarin: {ipa_inline}`[k w a²¹⁴ n]` {ipa_icon}`right-arrow` {ipa_inline}`[k w a˨˩˦ n]`)
    * Placing tone diacritics on the vowel nucleus rather than on the final segment in the syllable
  * Fixing up character glyphs
    * {ipa_inline}`[õ ẽ ũ ĩ ã]` {ipa_icon}`right-arrow` {ipa_inline}`[õ ẽ ũ ĩ ɐ̃]` in Portuguese (single glyph to compound characters with nasality diacritic)
  * Correcting many mistranscriptions
    * {ipa_inline}`[r]` {ipa_icon}`right-arrow` {ipa_inline}`[ɹ]` in US English
    * {ipa_inline}`[cʰ]` {ipa_icon}`right-arrow` {ipa_inline}`[tɕʰ]` in Thai
    * {ipa_inline}`[tʃ]` {ipa_icon}`right-arrow` {ipa_inline}`[tɕ]` in Tamil
    * {ipa_inline}`[ç]` {ipa_icon}`right-arrow` {ipa_inline}`[ɕ]` in Swedish

```{note}

I am unfamiliar with many of the languages and dialects below, and have largely based my systems on publicly available resources, relying heavily on any phonology information on {xref}`wikipedia`, as well as {xref}`phoible` and {xref}`xpf`. If you have any suggestions for improvements, please open [a discussion topic](https://github.com/MontrealCorpusTools/mfa-models/discussions/categories/pronunciation-dictionaries).

```
## Consonants

* **Palatalized consonants:** If a language has palatalized consonants, these have been replaced by palatal consonats:
  * {ipa_inline}`[lʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ʎ]`
  * {ipa_inline}`[nʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[kʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[c]`
  * {ipa_inline}`[ɡʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɟ]`
  * {ipa_inline}`[xʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ç]`
  * {ipa_inline}`[ɣʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ʝ]`
* **Place representation:** In general, if a consonant is listed as dental in descriptions of its typical realization, it is represented with the dental diacritic
  * {ipa_inline}`[t̪ d̪ t̪s̪ n̪]`
* **Homorganic nasal place assimilation:** If a language has this (and let's be real, which ones don't?[^except_maybe_Russian]), then the following transformations are done:
  * {ipa_inline}`[m]` {ipa_icon}`right-arrow` {ipa_inline}`[ɱ]` before labiodental consonants
  * {ipa_inline}`[n ŋ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]` before palatal consonants

## Vowels

* **Diphthongs** with high on-glides or off-glide have been standardized to use glides rather than full vowels or marked with brevis diacritics
  * {ipa_inline}`[au aʊ aʊ̯]` {ipa_icon}`right-arrow` {ipa_inline}`[aw]`
  * {ipa_inline}`[ou oʊ oʊ̯]` {ipa_icon}`right-arrow` {ipa_inline}`[ow]`
  * {ipa_inline}`[ai aɪ aɪ̯]` {ipa_icon}`right-arrow` {ipa_inline}`[aj]`
  * {ipa_inline}`[ei eɪ eɪ̯]` {ipa_icon}`right-arrow` {ipa_inline}`[ej]`

## Specific language notes

### Arabic

The Arabic MFA dictionary was created by [Natalia Shmueli](https://twitter.com/NataliaShmueli).

```{admonition} Pronunciation dictionaries
   See {ref}`arabic_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Arabic consonants

* **Gemination:** Multiple or geminated consonants are represented as long consonants
  * {ipa_inline}`[l l]` {ipa_icon}`right-arrow` {ipa_inline}`[ɫː]`

#### Arabic vowels

* **Short vowel laxing:** Short vowels are represented with their lax variants, while long vowels retain their tense variants
  * {ipa_inline}`[a]` {ipa_icon}`right-arrow` {ipa_inline}`[æ]`, except before {ipa_inline}`[q sˁ tˁ dˁ ðˁ ɫ r]` where it is realized as {ipa_inline}`[ɑ]`
    * Long {ipa_inline}`[a]` is {ipa_inline}`[aː]`, except before {ipa_inline}`[q sˁ tˁ dˁ ðˁ ɫ r]` where it is realized as {ipa_inline}`[ɑː]`
  * {ipa_inline}`[i]` {ipa_icon}`right-arrow` {ipa_inline}`[ɪ]`, but not for {ipa_inline}`[iː]`
  * {ipa_inline}`[u]` {ipa_icon}`right-arrow` {ipa_inline}`[ʊ]`, but not for {ipa_inline}`[uː]`

### Bulgarian

```{admonition} Pronunciation dictionaries
   See {ref}`bulgarian_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Bulgarian consonants

* **Dental consonants:** Alveolar  obstruents and nasals are represented with dentals {ipa_inline}`[t̪ d̪ t̪s̪ s̪ z̪ n̪]`, except when palatalized

#### Bulgarian vowels

Unchanged from their representation in [Wikipron](https://github.com/CUNY-CL/wikipron/blob/master/data/scrape/tsv/bul_cyrl_broad_filtered.tsv).

### English

The primary deviations from standard symbols have been to bring English more in line with other languages.

```{admonition} Pronunciation dictionaries
   See {ref}`english_(nigeria)_mfa_dictionary_v2_0_0`, {ref}`english_(uk)_mfa_dictionary_v2_0_0`, and {ref}`english_(us)_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### English consonants

* **Palatalization:** Changed {ipa_inline}`[n k ɡ l  h]` tokens to {ipa_inline}`[ɲ c ʎ ɟ ç]` before front vowels {ipa_inline}`[i(ː) ɪ ej ɛ æ]`, as well as before other palatal consonants
* **Yod coalescence:** Combined some sequences involving {ipa_inline}`[j]` to a single palatal symbol
  * {ipa_inline}`[n j]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[k j]` {ipa_icon}`right-arrow` {ipa_inline}`[c]`
  * {ipa_inline}`[l j]` {ipa_icon}`right-arrow` {ipa_inline}`[ʎ]`
  * {ipa_inline}`[ɡ j]` {ipa_icon}`right-arrow` {ipa_inline}`[ɟ]`
  * {ipa_inline}`[h j]` {ipa_icon}`right-arrow` {ipa_inline}`[ç]`
* **Aspiration:** Added aspiraton to voiceless stops before stressed vowels and at the beginning of words, except after sibilants
  * {ipa_inline}`[p]` {ipa_icon}`right-arrow` {ipa_inline}`[pʰ]`
  * {ipa_inline}`[t]` {ipa_icon}`right-arrow` {ipa_inline}`[tʰ]`
  * {ipa_inline}`[c]` {ipa_icon}`right-arrow` {ipa_inline}`[cʰ]`
  * {ipa_inline}`[k]` {ipa_icon}`right-arrow` {ipa_inline}`[kʰ]`
* **Flapping (US only):** Changed {ipa_inline}`[t d]` tokens to {ipa_inline}`[ɾ]` in unstressed syllables, except after nasals
  * {ipa_inline}`rapidity [ɹ ə pʰ ɪ ɾ ɪ ɾ i]`
* **Intervocalic {ipa_inline}`/t/` glottalization (UK only):** Added pronunciation variants for {ipa_inline}`[t]` {ipa_icon}`right-arrow`  {ipa_inline}`[ʔ]` in unstressed syllables, except after nasals and obstrucents
  * {ipa_inline}`butter [b ɐ t ə] ~ [b ɐ ʔ ə]`
* **Word-final {ipa_inline}`/t/` glottalization (all dialects):** Added pronunciation variants for word-final {ipa_inline}`[ʔ]` after vowels and liquids
  * {ipa_inline}`right [ɹ aj t] ~ [ɹ aj ʔ]`
* **Initial glottals:** Added pronunciation variants with initial {ipa_inline}`[ʔ]` for common vowel-initial words
* **Dental stopping (all dialects):** Added pronunciation variants for realizations of {ipa_inline}`[ð θ]` as {ipa_inline}`[d t]` for frequent words

#### English vowels

* **{lexical_set}`goose`-fronting (US and UK):** Changed {ipa_inline}`[u]` tokens to the more fronted {ipa_inline}`[ʉ]`, Nigerian English retains {ipa_inline}`[u]`
  * {ipa_inline}`dude [dʲ ʉː d]`
* **{lexical_set}`lot, cloth, thought`-lowering (US and UK):** Changed {ipa_inline}`[ɔ]` tokens to the lower {ipa_inline}`[ɒ]`
  * {ipa_inline}`caught [kʰ ɒː t]`
* **{lexical_set}`strut`-centering (US and UK):** Changed {ipa_inline}`[ʌ]` tokens to the more central {ipa_inline}`[ɐ]`, Nigerian English has these tokens as {ipa_inline}`[ɔ]`
  * {ipa_inline}`but [b ɐ t]`
* **{lexical_set}`merry`/{lexical_set}`marry`/{lexical_set}`mary` merger (US only):** {ipa_inline}`[ej æ ɛ]` are merged to {ipa_inline}`[ɛ]` before {ipa_inline}`[ɹ]`
* **Diphthong standardization (all dialects):** Changed diphthongs to use glides rather than extra short lax vowels
  * {ipa_inline}`[aʊ]` {ipa_icon}`right-arrow` {ipa_inline}`[aw]`
  * {ipa_inline}`[aɪ]` {ipa_icon}`right-arrow` {ipa_inline}`[aj]`
  * {ipa_inline}`[oʊ]` {ipa_icon}`right-arrow` {ipa_inline}`[ow]`
  * {ipa_inline}`[eɪ]` {ipa_icon}`right-arrow` {ipa_inline}`[ej]`
  * {ipa_inline}`[ɔɪ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɔj]`
* **Unstressed vowels (US and UK):** I have tried to limit the variation of {ipa_inline}`[ɪ]` and {ipa_inline}`[ə]` in unstressed syllables by confining it to {ipa_inline}`[ɪ]` in the {ipa_inline}`-ed` (verb past tense) and {ipa_inline}`-es` (plurals and third person present tense).  Elsewhere it's harder to limit, but if two variants only differ in quality between {ipa_inline}`[ɪ]` and {ipa_inline}`[ə]`, I've only kept one of them
* **Diphthong + rhotic standardization:**  In most words that have a diphthong plus rhotic, these have been standardized to use {ipa_inline}`[ɹ]` rather than {ipa_inline}`[ɚ]`, except when there is an {ipa_inline}`-er` affix
  * {ipa_inline}`fire [f aj ɚ]` {ipa_icon}`right-arrow` {ipa_inline}`fire [f aj ɹ]`
  * But {ipa_inline}`higher [h aj ɹ]` {ipa_icon}`right-arrow` {ipa_inline}`higher [h aj ɚ]`

#### Nigerian English

The Nigerian English was based on the UK dictionary, with some significant modifications. I have tried to largely follow Ulrike B. Gut's book chapter on Nigerian English phonology[^Gut_2008], as that is what is predominately cited in other resources like the [OED](https://public.oed.com/how-to-use-the-oed/key-to-pronunciation/pronunciations-for-world-englishes/pronunciation-model-west-african-english/).

```{admonition} Pronunciation dictionaries
   See {ref}`english_(nigeria)_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Nigerian English consonants

* **Silent consonants:** Silent consonants in words like {ipa_inline}`bomb`, {ipa_inline}`numb`, etc are realized, i.e. {ipa_inline}`[b ɔ m b]`
* **Realization of unstressed {ipa_inline}`[t]`:** Realized as {ipa_inline}`[t]` rather than {ipa_inline}`[ʔ]` in the UK dictionary

##### Nigerian English vowels

* **{ipa_inline}`[ɔ]`:** {lexical_set}`lot`, {lexical_set}`strut`, {lexical_set}`cloth`, {lexical_set}`north`, {lexical_set}`force`, {lexical_set}`thought`
  * {ipa_inline}`lot [l ɔ t]`
  * {ipa_inline}`strut [s t ɹ ɔ t]`
  * {ipa_inline}`cloth [k l ɔ θ]`
  * {ipa_inline}`north [n ɔ θ]`
  * {ipa_inline}`force [f ɔ s]`
  * {ipa_inline}`thought [θ ɔ t]`
* **{ipa_inline}`[a]`:** {lexical_set}`trap`, {lexical_set}`bath`, {lexical_set}`palm`, {lexical_set}`start`, {lexical_set}`letter` (unstressed rhotic), unstressed {ipa_inline}`[ə]` for orthographic {ipa_inline}`a`
  * {ipa_inline}`trap [t ɹ a p]`
  * {ipa_inline}`bath [b a θ]`
  * {ipa_inline}`palm [pʰ a m]`
  * {ipa_inline}`start [s t a t]`
  * {ipa_inline}`letter [l ɛ t a]`
  * {ipa_inline}`about [a b aw t]`
* **{ipa_inline}`[i]`:** {lexical_set}`kit`, {lexical_set}`fleece`, unstressed {ipa_inline}`[ə]` or {ipa_inline}`[ɪ]` for orthographic {ipa_inline}`i`
  * {ipa_inline}`kit [cʰ i t]`
  * {ipa_inline}`fleece [f ʎ iː s]`
  * {ipa_inline}`singing [s i ŋ i ŋ ɡ]`
* **{ipa_inline}`[u]`:** {lexical_set}`goose`
  * {ipa_inline}`goose  [ɡ uː s]`
* **{ipa_inline}`[e]`:** {lexical_set}`face`
  * {ipa_inline}`face [f e s]`
* **{ipa_inline}`[o]`:** {lexical_set}`goat`
  * {ipa_inline}`goat [ɡ o t]`
* **{ipa_inline}`[ɛ]`:** {lexical_set}`dress`, unstressed {ipa_inline}`[ə]` or {ipa_inline}`[ɪ]` for orthographic {ipa_inline}`e`, especially {ipa_inline}`-ed` and {ipa_inline}`-es` suffixes
  * {ipa_inline}`dresses [d ɹ ɛ s ɛ z]`
  * {ipa_inline}`granted [ɡ ɹ a n t ɛ d]`
* **{ipa_inline}`[ʊ]`:** {lexical_set}`foot`, {lexical_set}`cure`, unstressed syllables with syllabic {ipa_inline}`[ɫ̩]`, especially {ipa_inline}`-ful` and {ipa_inline}`-able` suffixes
  * {ipa_inline}`foot [f ʊ t]`
  * {ipa_inline}`cure [cʰ ʊ a]`
  * {ipa_inline}`wonderful  [w ɔ n d a f ʊ ɫ]`
  * {ipa_inline}`legible [l ɛ dʒ i b ʊ ɫ]`

### Hausa

Largely followed the [Hausa phonology wiki](https://en.wikipedia.org/wiki/Hausa_language#Phonology).

```{admonition} Pronunciation dictionaries
   See {ref}`hausa_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Hausa vowels

* **Tone:** Changed tone makers to use tone level symbols following vowels rather than accent diacritics
  * {ipa_inline}`abacada [ʔ àː b àː t͡ʃ àː d âː]` {ipa_icon}`right-arrow` {ipa_inline}`abacada [ʔ aː˩ b aː˩ tʃ aː˩ d aː˥˦]`
* **Diphthongs:** Merged instances of {ipa_inline}`[i]` and {ipa_inline}`[u]` without tone following {ipa_inline}`[a]` and {ipa_inline}`[e]` into diphthongs {ipa_inline}`[aj]` and {ipa_inline}`[aw]`

### Japanese

```{admonition} Pronunciation dictionaries
   See {ref}`japanese_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Japanese consonants

* **Gemination:** Geminate consonants are uniformly represented with length marking
  * {ipa_inline}`[tː ɸː pʲː mʲː]`
* **Palatalized consonants:** Palatalized velar consonants, as well as those before * {ipa_inline}`[i]` were coded as fully palatal
  * {ipa_inline}`がっきゅう [ɡ a cː ɨː]`
  * {ipa_inline}`ちょうき [tɕ oː c i]`
  * {ipa_inline}`きぎょう [c i ɟ oː]`
  * {ipa_inline}`ぎゅうにゅう [ɟ ɨː ɲ ɨː]`
* **Voiced fricative stopping:** {ipa_inline}`[z]` and {ipa_inline}`[ʑ]` are affricates {ipa_inline}`[dz]` and {ipa_inline}`[dʑ]` word-initially, following nasals, or when geminated
  * {ipa_inline}`じょうでき [dʑ oː d e c i]`
  * {ipa_inline}`マッジ [m a dʑː i]`
  * {ipa_inline}`あんぜん [a n dz e ɴ]`
* **Realizations of {ipa_inline}`ん`:** Coda nasal is realized as:
  * {ipa_inline}`[m]` before {ipa_inline}`[p b]` (and their palatalized/geminate variants)
  * {ipa_inline}`[n]` before {ipa_inline}`[t ts dz d ɾ]` (and their palatalized/geminate variants)
  * {ipa_inline}`[ɰ̃]` before {ipa_inline}`[s ɕ ɸ ç h]` (and their palatalized/geminate variants) and vowels
  * {ipa_inline}`[ɲ]` before {ipa_inline}`[c ɟ tɕ dʑ ɕ ʑ]` (and their geminate variants)
  * {ipa_inline}`[ŋ]` before {ipa_inline}`[k ɡ]` (and their geminate variants)
  * {ipa_inline}`[ɴ]` word-finally
  * Long nasal before other nasals, i.e. {ipa_inline}`うんめい [ɯ mː eː]`
* **Realizations of /h/:**
  * {ipa_inline}`[ɸ]` before {ipa_inline}`[ɯ]` (and its long variant)
  * {ipa_inline}`[ç]` before {ipa_inline}`[i]` (and its long variant) and in palalized cases like {ipa_inline}`ひゃく [ç a k ɯ]`
  * {ipa_inline}`[h]` elsewhere
* **Borrowed sounds:** The kana {ipa_inline}`ヴ` is transcribed with {ipa_inline}`[v]`
  * {ipa_inline}`アヴェニュー [a v e ɲ ɨː]`
* **Final glottals:** Words ending in {ipa_inline}`っ` that are pronounced with audible stops are transcribed with a final {ipa_inline}`[ʔ]`
  * {ipa_inline}`あっ [a ʔ]`
  * {ipa_inline}`いてっ [i t e ʔ]`

#### Japanese vowels

* **{ipa_inline}`[ɯ]`-fronting:** Following alveolar obstruents or palatal(ized) consonants, {ipa_inline}`[ɯ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɨ]`
* **High vowel devoicing:** Between voiceless obstruents, the high short vowels {ipa_inline}`[i ɨ ɯ]` are represented as voiceless {ipa_inline}`[i̥ ɨ̥ ɯ̥]`
  * {ipa_inline}`すき [s ɨ̥ c i]`
  * High frequency words like {ipa_inline}`です`, {ipa_inline}`ます`, etc. have a pronunciation variant with devoiced final vowel {ipa_inline}`です [d e s ɨ̥] ~ [d e s ɨ]`

### Korean

I have largely followed the [Korean Phonology Wikipedia page](https://en.wikipedia.org/wiki/Korean_phonology).

```{admonition} Pronunciation dictionaries
   See {ref}`korean_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Korean consonants

* **Palatalization:** {ipa_inline}`ㅅ [s sʰ]` and {ipa_inline}`ㅆ [s͈]` {ipa_icon}`right-arrow` {ipa_inline}`[ɕ ɕʰ]` and {ipa_inline}`[ɕ͈ ]` before {ipa_inline}`[i j]`
* **Realizations of {ipa_inline}`ㅎ /h/`**:
  * {ipa_inline}`[ç]` word-initially before {ipa_inline}`[i j]`
  * {ipa_inline}`[ʝ]` intervocalically before {ipa_inline}`[i j]`
  * {ipa_inline}`[x]` word-initially before {ipa_inline}`[ɯ]`
  * {ipa_inline}`[ɣ]` intervocalically before {ipa_inline}`[ɯ]`
  * {ipa_inline}`[ɸ]` word-initially before {ipa_inline}`[o u w]`
  * {ipa_inline}`[β]` intervocalically before {ipa_inline}`[o u w]`
  * {ipa_inline}`[h]` word-initially before {ipa_inline}`[o u w]`
  * {ipa_inline}`[ɦ]` intervocalically before {ipa_inline}`[ɐ ʌ e]`
* **Realizations of {ipa_inline}`ㄹ /l/`:**
  * {ipa_inline}`[ɾ]` word-initially, intervocalically, or between vowels and {ipa_inline}`/h/`
  * {ipa_inline}`[ʎ]` before {ipa_inline}`[i j]` or palatal consonants
  * {ipa_inline}`[ɭ]` elsewhere

#### Korean vowels

* **{ipa_inline}`[a]`-raising:** Open vowels are transcribed with as {ipa_inline}`[ɐ]`
* **{ipa_inline}`/ɯ/`-fronting:** {ipa_inline}`/ɯ/` is transcribed as {ipa_inline}`/ɨ/`
* **{ipa_inline}`/e/`-{ipa_inline}`/ɛ/` merger:** Instances of {ipa_inline}`[e]` and {ipa_inline}`[ɛ]` have been merged to {ipa_inline}`[e]`
* **Vowel length:** Vowel length marking is retained as sourced from [Wikipron](https://github.com/CUNY-CL/wikipron/blob/master/data/scrape/tsv/kor_hang_narrow_filtered.tsv); however, it seems like it's completely neutralized in modern Korean
* **Diphthongs:** Diphthongs are transcribed as sequences of independent glide + vowel combinations
  * {ipa_inline}`가격의 [k ɐ ɡ j ʌ ɡ ɰ i]`
  * {ipa_inline}`가는쥐 [k ɐ n ɨ ɲ dʑ ɥ i]`
  * {ipa_inline}`가두녀성 [k ɐ d u ɲ j ʌ sʰ ʌ ŋ]`
  * {ipa_inline}`가시화될 [k ɐ ɕʰ i β w ɐ d w e ɭ]`

### Polish

```{admonition} Pronunciation dictionaries
   See {ref}`polish_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Polish consonants

* **Dental consonants:** Coronal consonants are represented with dental diacritics, except when palatalized
  * {ipa_inline}`[t̪ tʲ d̪ dʲ t̪s̪ tsʲ n̪ ɲ]`
* **Nasal approximation:** Palatal nasal {ipa_inline}`[ɲ]` becomes {ipa_inline}`[j̃]` before fricatives

#### Polish vowels

### Portuguese

```{admonition} Pronunciation dictionaries
   See {ref}`portuguese_(brazil)_mfa_dictionary_v2_0_0` and {ref}`portuguese_(portugal)_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Portuguese consonants

* **Palatal nasal approximation (Brazilian Portuguese only):** Converted all {ipa_inline}`nh [ɲ]` to {ipa_inline}`[j̃]`
* **Palatalization before high vowels/glides:**
  * {ipa_inline}`[l]` {ipa_icon}`right-arrow` {ipa_inline}`[ʎ]` and {ipa_inline}`[n]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]` before {ipa_inline}`[i]` and {ipa_inline}`[ĩ]`
  * {ipa_inline}`[l j]` {ipa_icon}`right-arrow` {ipa_inline}`[ʎ]` and  {ipa_inline}`[n j]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[d]` {ipa_icon}`right-arrow` {ipa_inline}`[dʒ]` and {ipa_inline}`[t]` {ipa_icon}`right-arrow` {ipa_inline}`[tʃ]` before front vowels


#### Portuguese vowels

* Diphthongs are treated as sequences of vowel + glide, i.e., {ipa_inline}`limão [ʎ i m ɐ̃ w̃] (Brazilian)`
  * Rationale is that there is a high degree of combinations between vowels and glides, with some combinations only represented a handful of times in the lexicons

### Russian

```{admonition} Pronunciation dictionaries
   See {ref}`russian_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Russian consonants

* **Dental consonants:** Hard coronal consonants are represented with dental diacritics, but not soft coronal cosonants
  * {ipa_inline}`[t̪ tʲ d̪ dʲ t̪s̪ tsʲ n̪ ɲ]`

#### Russian vowels

Unedited from [Wikipron](https://github.com/CUNY-CL/wikipron/blob/master/data/scrape/tsv/rus_cyrl_narrow.tsv).

### Spanish

```{admonition} Pronunciation dictionaries
   See {ref}`spanish_(latin_america)_mfa_dictionary_v2_0_0` and {ref}`spanish_(spain)_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Spanish consonants

* **Voiced stop lenition (all dialects):** Voiced stops are represented as fricatives in all places except word-initially, after a nasal consonant, and after a lateral consonant (for {ipa_inline}`/d ʝ/` only)
  * {ipa_inline}`[#n] [b d̪ ɡ ɟʝ]` {ipa_icon}`right-arrow` {ipa_inline}`[^#n] [β ð ɣ ʝ]`
* **Palatalization (all dialects):** Following other languages, velars  {ipa_inline}`[k ɡ x ɣ]` {ipa_icon}`right-arrow` {ipa_inline}`[c ɟ ç ʝ]` before {ipa_inline}`[i e]`
* **Dental obstruents (all dialects):** Coronal stops are represented with a dental diacritic (other manners for coronals are represented as alveolar)
  * {ipa_inline}`[t̪ d̪ s n]`
* **Yeísmo:** {ipa_inline}`ll [ʎ]` and {ipa_inline}`y [ʝ]` are merged in the Latin American dictionary, but remain split in the European one.  However, it might be worth merging them for European as well as that is a sound change in progress.

#### Spanish vowels

Unedited from [Wikipron](https://github.com/CUNY-CL/wikipron/tree/master/data/scrape).

### Swahili

```{admonition} Pronunciation dictionaries
   See {ref}`swahili_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Swahili consonants

* **Prenasalized obstruents:** Treated as sequences of nasal + obstruent
* **Implosives:** Voiced stops that are not following nasals are represented as implosives
* **Aspiration:** Voiceless stops are all unaspirated, as it is not reflected in the orthography and I do not have a definitive source for which words contain aspirated stops vs plain
* **Trills:** All instances of {ipa_inline}`/r/` are represented with a tap {ipa_inline}`[ɾ]`

#### Swahili vowels

* **Vowel length:** Sequences of vowels are treated as long vowels

### Thai

```{admonition} Pronunciation dictionaries
   See {ref}`thai_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Thai consonants

* **Unreleased final stops:** Coda stops are transcribed as unreleased {ipa_inline}`[p̚ t̚ k̚]`
  * {ipa_inline}`คร้าบ [kʰ r aː˥˩ p̚]`

#### Thai vowels

* **Tones:** Tones have been attached to the vowel of the syllable
  * {ipa_inline}`คลอก [kʰ l ɔː˥˩ k̚]`
* **Diphthongs:** Glides have been analyzed as separate segments
  * {ipa_inline}`กบไสไม้ [k o˨˩ p̚ s a˩˩˦ j m aː˦˥ j]`
  * {ipa_inline}`จุดไข่ปลา [tɕ u˨˩ t̚ kʰ a˨˩ j p l aː˧]`

### Turkish

Largely followed the [Turkish phonology Wikipedia page](https://en.wikipedia.org/wiki/Turkish_phonology), following their list of phonetic realizations.

```{admonition} Pronunciation dictionaries
   See {ref}`turkish_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Turkish consonants

* **Palatalization:** Velar obstruents are palatal {ipa_inline}`[c ɟ ç]` before front vowels {ipa_inline}`[i e œ y]`, as well as the alveolar lateral {ipa_inline}`[ʎ]`
* **Homorganic nasal place assimilation:** Nasals agree in place with following obstruents, transcribed as one of {ipa_inline}`[m n̪ ɲ ŋ]`
* **Dental consonants:** Alveolar stops and nasals are transcribed as dental {ipa_inline}`[t̪ d̪ s̪ z̪ n̪]`
* **Gemination:** Sequences of two consonants in the orthography are represented as a long consonant
  * {ipa_inline}`minnettar [m i n̪ː e t̪ː a ɾ]`
  * Geminated {ipa_inline}`[ɾ]` is represented as {ipa_inline}`[ɾː]`, but maybe should be trilled {ipa_inline}`[r]`
* **Realizations of {ipa_inline}`ğ /ɰ/`:** Given its quasi-phonemic status, I've followed the description of its phonetic distribution:
  * Before a consonant or word boundary, it is realized as length on the previous vowel
  * Between front vowels, it is realized as {ipa_inline}`[j]`
  * Words with {ipa_inline}`ğ /ɰ/` between back vowels have two pronunciation variants, one with {ipa_inline}`[ɰ]` realized and one with it deleted {ipa_inline}`sağol [s̪ a ɰ o ɫ] ~ [s̪ a o ɫ]`

#### Turkish vowels

* **Phonetic realizations:** The primary realization of front vowels is {ipa_inline}`[i y e ø]`, but for word-final open  syllables, these are represented with {ipa_inline}`[ɪ ʏ ɛ œ]`.  Back vowels are generally represented as {ipa_inline}`[ɯ u a o]`, with word-final open realizations for the high back vowels are {ipa_inline}`[ɨ ʊ]`
* **Closed syllable {ipa_inline}`[e]` lowering:** In syllables with coda {ipa_inline}`[m ʎ ɲ ɾ ŋ ɫ n̪]`, {ipa_inline}`[e]` {ipa_icon}`right-arrow` {ipa_inline}`[ɛ]`

### Ukrainian

```{admonition} Pronunciation dictionaries
   See {ref}`ukrainian_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Ukrainian consonants

* **Palatalization:** Velar and aleovlar soft consonants are represented as palatal
  * {ipa_inline}`[kʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[c]`
  * {ipa_inline}`[ɦʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ç]`
  * {ipa_inline}`[xʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ʝ]`
  * {ipa_inline}`[nʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[lʲ]` {ipa_icon}`right-arrow` {ipa_inline}`[ʎ]`
* **Trill realization:** The trill {ipa_inline}`/ʝ/` is represented as {ipa_inline}`[ɾ]`
* **Dental consonants:** Alveolar consonants are dental {ipa_inline}`[t̪ s̪ t̪s̪ d̪ z̪ d̪z̪ n̪]` except when palatalized

#### Ukrainian vowels

Largely unchanged from their [Wikipron](https://github.com/CUNY-CL/wikipron/blob/master/data/scrape/tsv/ukr_cyrl_narrow.tsv) counterparts.

### Vietnamese

Generally I have followed James Kirby's [vPhon](https://github.com/kirbyj/vPhon) for generating transcriptions of Vietnamese words across three dialects.  The points where I have diverged from Kirby's system are below.

```{admonition} Pronunciation dictionaries
   See {ref}`vietnamese_(hanoi)_mfa_dictionary_v2_0_0`, {ref}`vietnamese_(ho_chi_minh_city)_mfa_dictionary_v2_0_0`, and {ref}`vietnamese_(hue)_mfa_dictionary_v2_0_0` for full IPA charts.
```

#### Vietnamese consonants

* **Palatalization:** Converted palatalized segments in Hanoi dialect to palatal consonants
  * {ipa_inline}`đánh [ɗ a˨˦ ʲŋ]` {ipa_icon}`right-arrow` {ipa_inline}`[ɗ a˨˦ ɲ]`
  * {ipa_inline}`thạch [tʰ a˨˩ ʲk]` {ipa_icon}`right-arrow` {ipa_inline}`[tʰ a˨˩ c]`
* Changing final consonants to be unreleased
  * {ipa_inline}`bạc [ɓ aː˨˩ k]` {fas}`long-arrow-alt-right` {ipa_inline}`[ɓ aː˨˩ k̚]`
* **IPA cleanup:** Removed ligatures in diphones and normalized bilabial onglides
  * {ipa_inline}`hóc [h ɔ˦˥ k͡p]` {ipa_icon}`right-arrow` {ipa_inline}`[h ɔ˦˥ kp]`
  * {ipa_inline}`đông [ɗ o˨˨ ŋ͡m]` {ipa_icon}`right-arrow` {ipa_inline}`[ɗ o˨˨ ŋm]`
  * {ipa_inline}`hoan [h ʷ aː˨˨ n]` {ipa_icon}`right-arrow` {ipa_inline}`[h w aː˨˨ n]`

#### Vietnamese vowels

* **Tones:** Converted Chao numbers into IPA levels and placed them always on the vowel rather than at the end of the syllable
  * {ipa_inline}`chải [tɕ aː j ²¹²]` {ipa_icon}`right-arrow` {ipa_inline}`[tɕ aː˨˩˨ j]`

[^Gut_2008]: [Gut, U. B. (2008). Nigerian English: Phonology. Varieties of English, 4, 35-54.](https://books.google.com/books?hl=en&lr=&id=L1VhZHGupMUC&oi=fnd&pg=PA35&dq=ulrike+gut+nigerian+english&ots=TfokeOEyC-&sig=BJKonoVIpo59B19lWhioiyHc7xE#v=onepage&q=ulrike%20gut%20nigerian%20english&f=false)

[^except_maybe_Russian]: According to [a footnote on the Russian phonology wikipedia](https://en.wikipedia.org/wiki/Russian_phonology#cite_ref-56), the hard {ipa_inline}`[n̪]` does not assimilate in place.

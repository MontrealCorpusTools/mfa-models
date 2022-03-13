# MFA IPA phone set

For its IPA models, MFA uses an opinionated IPA phone set.  This page will cataloge the way that phones are represented across languages (and note any deviations from them).  The guiding principle is to have general consistency in phones across languages, but allow for phonetic specification where it A) matters for the language and B) aids the aligner in assigning HMM states to phones.

For most languages, dictionaries were constructed from the [wikipron](https://github.com/CUNY-CL/wikipron/tree/master/data/scrape) scraped dictionaries.  However, given that they are crowd-sourced transcriptions from [Wiktionary](https://en.wiktionary.org/), there was a fair bit of noise to clean up.

## General notes

* **Diacritic ordering:** The ordering of diacritics is {ipa_inline}`(prenasalization) symbol (secondary place) (glottal settings) (length)
  * {ipa_inline}`pʰː`
  * {ipa_inline}`pʷʼ`
  * {ipa_inline}`pʲ̚`
  * {ipa_inline}`ⁿd̪ʷʱː`

## Consonants

* **Palatalized consonants:** If a language has palatalized consonants, these have been replaced by palatal consonats:
  * {ipa_inline}`[lʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʎ]`
  * {ipa_inline}`[nʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[kʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[c]`
  * {ipa_inline}`[ɡʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɟ]`
  * {ipa_inline}`[xʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ç]`
  * {ipa_inline}`[ɣʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʝ]`
* **Place representation:** In general, if a consonant is listed as dental in descriptions of its typical realization, it is represented with the dental diacritic
  * {ipa_inline}`[t̪ d̪ t̪s̪ n̪]`
* **Homorganic nasal place assimilation:** If a language has this (and let's be real, which ones don't?[^except maybe Russian?]), then the following transformations are done:
  * {ipa_inline}`[m]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɱ]` before labiodental consonants
  * {ipa_inline}`[n]` and {ipa_inline}`[ŋ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɲ]` before palatal consonants

## Vowels

* **Diphthongs** with high on-glides or off-glide have been standardized to use glides rather than full vowels or marked with brevis diacritics
  * {ipa_inline}`[au]`, {ipa_inline}`[aʊ]`, {ipa_inline}`[aʊ̯]` {fa}`long-arrow-alt-right` {ipa_inline}`[aw]`
  * {ipa_inline}`[ou]`, {ipa_inline}`[oʊ]`, {ipa_inline}`[oʊ̯]` {fa}`long-arrow-alt-right` {ipa_inline}`[ow]`
  * {ipa_inline}`[ai]`, {ipa_inline}`[aɪ]`, {ipa_inline}`[aɪ̯]` {fa}`long-arrow-alt-right` {ipa_inline}`[aj]`
  * {ipa_inline}`[ei]`, {ipa_inline}`[eɪ]`, {ipa_inline}`[eɪ̯]` {fa}`long-arrow-alt-right` {ipa_inline}`[ej]`

## Specific language notes

### Arabic

The Arabic MFA dictionary was created by Natalia Shmueli.

#### Arabic consonants

* **Gemination:** Multiple or geminated consonants are represented as long consonants
  * {ipa_inline}`[l l]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɫː]`

#### Arabic vowels

* **Short vowel laxing:** Short vowels are represented with their lax variants, while long vowels retain their tense variants
* {ipa_inline}`[a]` {fa}`long-arrow-alt-right` {ipa_inline}`[æ]`, except before {ipa_inline}`[q,sˁ,tˁ,dˁ,ðˁ,ɫ,r]` where it is realized as {ipa_inline}`[ɑ]`
  * Long {ipa_inline}`[a]` is {ipa_inline}`[aː]`, except before ipa_inline}`[q,sˁ,tˁ,dˁ,ðˁ,ɫ,r]` where it is realized as {ipa_inline}`[ɑː]`
* {ipa_inline}`[i]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɪ]`, but {ipa_inline}`[iː]`
* {ipa_inline}`[u]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʊ]`, but {ipa_inline}`[uː]`

### English

The primary deviations from standard symbols have been to bring English more in line with other languages.

#### English consonants

* **Palatalization:** Changed {ipa_inline}`[n]`, {ipa_inline}`[k]`, {ipa_inline}`[ɡ]`, {ipa_inline}`[l]`, and {ipa_inline}`[h]` tokens to {ipa_inline}`[ɲ]`, {ipa_inline}`[c]`, {ipa_inline}`[ʎ]`, {ipa_inline}`[ɟ]`, and {ipa_inline}`[ç]` before front vowels {ipa_inline}`[i(ː)]`, {ipa_inline}`[ɪ]`, {ipa_inline}`[ej]`, {ipa_inline}`[ɛ]`, and {ipa_inline}`[æ]`, as well as before other palatal consonants
* **Yod coalescensence:** Changed {ipa_inline}`[n j]`, {ipa_inline}`[k j]`, {ipa_inline}`[l j]`, {ipa_inline}`[ɡ j]`, and {ipa_inline}`[h j]` sequences to {ipa_inline}`[ɲ]`, {ipa_inline}`[c]`, {ipa_inline}`[ʎ]`, {ipa_inline}`[ɟ]`, and {ipa_inline}`[ç]`
* **Aspiration:** Changed {ipa_inline}`[p]`, {ipa_inline}`[t]`, {ipa_inline}`[c]` and {ipa_inline}`[k]` to aspirated variants {ipa_inline}`[pʰ]`, {ipa_inline}`[tʰ]`, {ipa_inline}`[cʰ]` and {ipa_inline}`[kʰ]` before stressed vowels and at the beginning of words, except after sibilants
* **Flapping (US only):** Changed {ipa_inline}`[t]` and {ipa_inline}`[d]` tokens to {ipa_inline}`[ɾ]` in unstressed syllables, except after nasals
* **Glottalization (UK only):** Added pronunciation variants for {ipa_inline}`[t]` {fa}`long-arrow-alt-right`  {ipa_inline}`[ʔ]` in unstressed syllables, except after nasals and obstrucents
* **Glottalization (US and UK):** Added pronunciation variants for word-final {ipa_inline}`[t]` before vowels and liquids
* **Initial glottals:** Added pronunciation variants with initial {ipa_inline}`[t]` for common vowel-initial words
* **Dental stopping (all dialects):** Added pronunciation variants for realizations of {ipa_inline}`[ð θ]` as {ipa_inline}`[d t]` for frequent words

#### English vowels

* **{lexical_set}`goose`-fronting (US and UK):** Changed {ipa_inline}`[u]` tokens to the more fronted {ipa_inline}`[ʉ]`, Nigerian english retains {ipa_inline}`[u]`
* **{lexical_set}`lot, cloth, thought`-lowering (US and UK):** Changed {ipa_inline}`[ɔ]` tokens to the lower {ipa_inline}`[ɒ]`
* **{lexical_set}`strut`-centering (US and UK):** Changed {ipa_inline}`[ʌ]` tokens to the more central {ipa_inline}`[ɐ]`, Nigerian English has these tokens as {ipa_inline}`[ɔ]`
* **{lexical_set}`merry`/{lexical_set}`marry`/{lexical_set}`mary` merger (US)
* **Diphthong standardization (all dialects):** Changed {ipa_inline}`[aʊ]`, {ipa_inline}`[aɪ]`, {ipa_inline}`[oʊ]`, {ipa_inline}`[eɪ]`, and {ipa_inline}`[ɔɪ]` tokens to {ipa_inline}`[aw]`, {ipa_inline}`[aj]`, {ipa_inline}`[ow]`, {ipa_inline}`[ej]`, and {ipa_inline}`[ɔj]`
* **Unstressed vowels (US and UK):** I have tried to limit the variation of {ipa_inline}`[ɪ]` and {ipa_inline}`[ə]` in unstressed syllables by confining it to {ipa_inline}`[ɪ]` in the {ipa_inline}`-ed` (verb past tense) and {ipa_inline}`-es` (plurals and third person present tense).  Elsewhere it's harder to limit, but if two variants only differ in quality between {ipa_inline}`[ɪ]` and {ipa_inline}`[ə]`, I've only kept one of them
* **Diphthong + rhotic standardization:**  In most words that have a diphthong plus rhotic, these have been standardized to use {ipa_inline}`[ɹ]` rather than {ipa_inline}`[ɚ]`, except when there is an {ipa_inline}`-er` affix
  * {ipa_inline}`fire [f aj ɚ]` {fa}`long-arrow-alt-right` {ipa_inline}`fire [f aj ɹ]`
  * But {ipa_inline}`higher [h aj ɹ]` {fa}`long-arrow-alt-right` {ipa_inline}`higher [h aj ɚ]`

#### Nigerian English

The Nigerian English was based on the UK dictionary, with some significant modifications. I have tried to largely follow Ulrike B. Gut's book chapter on Nigerian English phonology[^Gut (2008)], as that is what is predominately cited in other resources like the [OED](https://public.oed.com/how-to-use-the-oed/key-to-pronunciation/pronunciations-for-world-englishes/pronunciation-model-west-african-english/).

#### Nigerian English consonants

* **Silent consonants:** Silent consonants in {ipa_inline}`bomb` are realized, i.e. {ipa_inline}`[b ɔ m b]`
* **Realization of unstressed {ipa_inline}`[t]`:** Realized as {ipa_inline}`[t]` rather than {ipa_inline}`[ʔ]` in the UK dictionary

##### Nigerian English vowels

* **{ipa_inline}`[ɔ]`:** {lexical_set}`lot`, {lexical_set}`strut`, {lexical_set}`cloth`, {lexical_set}`north`, {lexical_set}`force`, {lexical_set}`thought`
* **{ipa_inline}`[a]`:** {lexical_set}`trap`, {lexical_set}`bath`, {lexical_set}`palm`, {lexical_set}`start`, {lexical_set}`letter` (unstressed rhotic), unstressed {ipa_inline}`[ə]` for orthographic {ipa_inline}`a`
* **{ipa_inline}`[i]`:** {lexical_set}`kit`, {lexical_set}`fleece`, unstressed {ipa_inline}`[ə]` or {ipa_inline}`[ɪ]` for orthographic {ipa_inline}`i`
* **{ipa_inline}`[u]`:** {lexical_set}`goose`, {lexical_set}`foot`
* **{ipa_inline}`[e]`:** {lexical_set}`face`
* **{ipa_inline}`[o]`:** {lexical_set}`goat`
* **{ipa_inline}`[ɛ]`:** {lexical_set}`dress`, {lexical_set}`fleece`, unstressed {ipa_inline}`[ə]` or {ipa_inline}`[ɪ]` for orthographic {ipa_inline}`e`, especially {ipa_inline}`-ed` and {ipa_inline}`-es` suffixes
* **{ipa_inline}`[ʊ]`:** {lexical_set}`cure`, unstressed syllables with syllabic {ipa_inline}`[ɫ̩]`, especially {ipa_inline}`-ful` and {ipa_inline}`-able` suffixes

### Hausa

Largely followed the [Hausa phonology wiki](https://en.wikipedia.org/wiki/Hausa_language#Phonology)

#### Hausa vowels

* Changed tone makers to use tone level symbols following vowels rather than accent diacritics
  * {ipa_inline}`abacada [ʔ àː b àː t͡ʃ àː d âː]` {fa}`long-arrow-alt-right` {ipa_inline}`abacada [ʔ aː˩ b aː˩ tʃ aː˩ d aː˥˦]`
* Merged instances of {ipa_inline}`[i]` and {ipa_inline}`[u]` without tone following {ipa_inline}`[a]` and {ipa_inline}`[e]` into diphthongs {ipa_inline}`[ai]` and {ipa_inline}`[aw]`

### Polish

#### Polish consonants

* **Dental consonants:** Coronal consonants are represented with dental diacritics, except when palatalized
  * {ipa_inline}`[t̪ tʲ d̪ dʲ t̪s̪ tsʲ n̪ ɲ]`
* **Nasal approximation:** Palatal nasal {ipa_inline}`[ɲ]` becomes {ipa_inline}`[j̃]` before fricatives

#### Polish vowels

### Portuguese

#### Portuguese consonants

* (Brazilian Portuguese) Converted all {ipa_inline}`nh [ɲ]` to {ipa_inline}`[j̃]`
* **Palatalization before high vowels/glides:** (Brazilian Portuguese)
  * {ipa_inline}`[l]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʎ]` and {ipa_inline}`[n]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɲ]` before {ipa_inline}`[i]` and {ipa_inline}`[ĩ]`
  * {ipa_inline}`[l j]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʎ]` and  {ipa_inline}`[n j]` {fa}`long-arrow-alt-right` {ipa_inline}`[ɲ]`
  * {ipa_inline}`[d]` {fa}`long-arrow-alt-right` {ipa_inline}`[dʒ]` and {ipa_inline}`[t]` {fa}`long-arrow-alt-right` {ipa_inline}`[tʃ]` before front vowels


#### Portuguese vowels

* Diphthongs are treated as sequences of vowel + glide, i.e., {ipa_inline}`limão [ʎ i m ɐ̃ w̃] (Brazilian)`
  * Rationale is that there is a high degree of combinations between vowels and glides, with some combinations only represented a handful of times in the lexicons

### Russian

#### Russian consonants

* **Dental consonants:** Hard coronal consonants are represented with dental diacritics, but not soft coronal cosonants
  * {ipa_inline}`[t̪ tʲ d̪ dʲ t̪s̪ tsʲ n̪ ɲ]`

#### Russian vowels

### Ukrainian

#### Ukrainian consonants

* {ipa_inline}`[ɦʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʝ]`

#### Ukrainian vowels

* {ipa_inline}`[ɦʲ]` {fa}`long-arrow-alt-right` {ipa_inline}`[ʝ]`

### Vietnamese

Generally I have followed James Kirby's [vPhon](https://github.com/kirbyj/vPhon) for generating transcriptions of Vietnamese words across three dialects.  The points where I have diverged from Kirby's system are:

* Converting Chao numbers into IPA levels and placing them always on the vowel
  * {ipa_inline}`chải [tɕ aː j ²¹²]` -> {ipa_inline}`[tɕ aː˨˩˨ j]`
* Removing ligatures in diphones
  * {ipa_inline}`hóc [h ɔ˦˥ k͡p]` -> {ipa_inline}`[h ɔ˦˥ kp]`
  * {ipa_inline}`đông [ɗ o˨˨ ŋ͡m]` -> {ipa_inline}`[ɗ o˨˨ ŋm]`
* Normalizing bilabial onglides:
  * {ipa_inline}`hoan [h ʷ aː˨˨ n]` -> {ipa_inline}`[h w aː˨˨ n]`
* Converting palatalized segments in Hanoi dialect to palatal consonants
  * {ipa_inline}`đánh [ɗ a˨˦ ʲŋ]` -> {ipa_inline}`[ɗ a˨˦ ɲ]`
  * {ipa_inline}`thạch [tʰ a˨˩ ʲk]` -> {ipa_inline}`[tʰ a˨˩ c]`
* Changing final consonants to be unreleased
  * {ipa_inline}`bạc [ɓ aː˨˩ k]` -> {ipa_inline}`[ɓ aː˨˩ k̚]`

[^Gut (2008)]: [Gut, U. B. (2008). Nigerian English: Phonology. Varieties of English, 4, 35-54.](https://books.google.com/books?hl=en&lr=&id=L1VhZHGupMUC&oi=fnd&pg=PA35&dq=ulrike+gut+nigerian+english&ots=TfokeOEyC-&sig=BJKonoVIpo59B19lWhioiyHc7xE#v=onepage&q=ulrike%20gut%20nigerian%20english&f=false)
[^except maybe Russian?]: According to [a footnote on the Russian phonology wikipedia](https://en.wikipedia.org/wiki/Russian_phonology#cite_ref-56), the hard {ipa_inline}`[n̪]` does not assimilate in place

Dictionaries
============

Recently added dictionaries use IPA transcriptions sourced from [wikipron](https://github.com/CUNY-CL/wikipron/tree/master/data), and manually cleaned to consolidate phones, remove orthographic characters from other systems (i.e. ones with <10 occurrences in thousands of entries), and apply some cross-linguistic logic.

The basics are as follows:

1. Removal of narrow diacritics

    * Height markers on vowels and consonants
      * /o̞/ &rarr; /o/ in various languages
      * /ɾ̝̊/ &rarr; /ɾ/ in Turkish
      * /ɯ̟̃ᵝ ɨ̥ᵝ etc/ &rarr; /ɯ/ or /ɨ/ depending on surrounding context in Japanese
    * Removal of nasality in languages where it's not phonemic
    * Merging some non-phonemic or dialectal contrasts
      * /ɫ/ &rarr; /l/, /ʍ/ &rarr; /w/ in English
      * /r/ &rarr; /ʁ/ in French
      * /ʁ ɹ ɻ χ ɦ h r/ &rarr; /x/ in Brazilian Portuguese
    * Standardizing diphthongs, afficates, etc
      * Merging sequences of /a ʊ/ into a single /aʊ/ phone
      * Merging sequences of vowels in Mandarin to single nucleus
    * Standardizing tones
      * Transforming all tones to Chao system (i.e. Mandarin /k w a˨˩˦ n/ goes to /k w a˨˩˦ n/)
      * Placing tone diacritics on the vowel nucleus rather than on the final segment in the syllable
    * Fixing up character glyphs
      * /õ ẽ ũ ĩ ã/ &rarr; /õ ẽ ũ ĩ ɐ̃/ in Portuguese (single character to compound with nasality diacritic)
    * Correcting many mistranscriptions (**NB**: This may be because I'm unfamiliar with the language or dialectal variation or it wasn't noted in the sources below.  Either way, feel free to let me know of any reversions I should do.)
      * /r/ &rarr; /ɹ/ in US English
      * /cʰ/ &rarr; /tɕʰ/ in Thai
      * /tʃ/ &rarr; /tɕ/ in Tamil
      * /ç/ &rarr; /ɕ/ in Swedish
      * /ï/ &rarr; /ɨ/ in Hanoi Vietnamese
      * etc

I am not familiar with most of the languages in this set, so if you have any corrections to the analysis present in them, please do let me know ([michael.e.mcauliffe@gmail.com](mailto:michael.e.mcauliffe@gmail.com)) or submit a [GitHub issue](https://github.com/MontrealCorpusTools/mfa-models/issues/new) or [PR](https://github.com/MontrealCorpusTools/mfa-models/compare). Most are also currently in an unfinished state and quite small, so expect them to be updated with some more entries from G2P models in the near future.

References
----------

* Bulgarian
 * [XPF Corpus - Bulgarian](https://cohenpr-xpf.github.io/XPF/conv_resources/info/bg.html)
  * [Bulgarian Phonology Wikipedia](https://en.wikipedia.org/wiki/Bulgarian_phonology)
* Croatian
  * [Serbo-Croatian Phonology Wikipedia](https://en.wikipedia.org/wiki/Serbo-Croatian_phonology)
* Czech
  * [XPF Corpus - Czech](https://cohenpr-xpf.github.io/XPF/conv_resources/info/cs.html)
  * [Czech Phonology Wikipedia](https://en.wikipedia.org/wiki/Czech_phonology)
* French
  * [Standard French Phonology Wikipedia](https://en.wikipedia.org/wiki/French_phonology)
* German
  * [Standard German Phonology Wikipedia](https://en.wikipedia.org/wiki/Standard_German_phonology)
* Hausa
  * [Hausa Language Wikipedia](https://en.wikipedia.org/wiki/Hausa_language#Phonology)
  * [Phoible](https://phoible.org/inventories/view/124#tipa) as reference for tone levels
* Japanese
  * [Japanese Phonology Wikipedia](https://en.wikipedia.org/wiki/Japanese_phonology)
* Korean
  * [Korean Phonology Wikipedia](https://en.wikipedia.org/wiki/Korean_phonology)
  * [jamo package for converting Hangul to Jamo](https://pypi.org/project/jamo/)
* Mandarin
  * [Standard Chinese Phonology Wikipedia](https://en.wikipedia.org/wiki/Standard_Chinese_phonology)
* Mandarin_pinyin
  * [MTTS lexicon](https://github.com/Jackiexiao/MTTS/tree/master/misc)
* Polish
  * [Polish Phonology Wikipedia](https://en.wikipedia.org/wiki/Polish_phonology)
* Portuguese
  * [Portuguese Phonology Wikipedia](https://en.wikipedia.org/wiki/Portuguese_phonology)
  * [Brazilian Portuguese Wikipedia](https://en.wikipedia.org/wiki/Brazilian_Portuguese)
* Russian
  * [Russian Phonology Wikipedia](https://en.wikipedia.org/wiki/Russian_phonology)
* Spanish
  * [Spanish Phonology Wikipedia](https://en.wikipedia.org/wiki/Spanish_phonology)
* Swedish
  * [Swedish Phonology Wikipedia](https://en.wikipedia.org/wiki/Swedish_phonology)
* Swahili
  * [XPF Corpus - Swahili](https://cohenpr-xpf.github.io/XPF/conv_resources/info/sw.html)
* Tamil
  * [Tamil Phonology Wikipedia](https://en.wikipedia.org/wiki/Tamil_phonology)
* Thai
  * [Thai Language Wikipedia](https://en.wikipedia.org/wiki/Thai_language#Phonology)
* Turkish
  * [Turkish Phonology Wikipedia](https://en.wikipedia.org/wiki/Turkish_phonology)
* Vietnamese
  * [Vietnamese Phonology Wikipedia](https://en.wikipedia.org/wiki/Vietnamese_phonology)
* Ukrainian
  * [Ukrainian Phonology Wikipedia](https://en.wikipedia.org/wiki/Ukrainian_phonology)

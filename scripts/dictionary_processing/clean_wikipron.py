import collections
import itertools
import os
import pathlib
import re
import unicodedata

import segments

try:
    import jamo
except ImportError:
    jamo = None

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
SCRAPE_DIR = ROOT_DIR.joinpath("dictionary", "training", "scraped")
OUTPUT_DIR = ROOT_DIR.joinpath("dictionary", "training", "cleaned")

LANG_PATHS = {
    "french": "fra_latn_broad_filtered.tsv",
    "portuguese_brazil": "Portuguese.tsv",
    "portuguese_portugal": "Portuguese.tsv",
}

# Full list of languages
# LANG_CODES = ['bulgarian', 'czech', 'french', 'german', 'mandarin_hani', 'polish', 'portuguese_brazil',
#             'portuguese_portugal', 'russian', 'spanish_spain', 'spanish_latin_america', 'swedish',
#              'tamil', 'thai', 'turkish', 'ukrainian', 'mandarin_hani_beijing', 'mandarin_hani_taiwan', 'mandarin_hani_standard',
#              'korean_hangul', 'hausa', 'japanese', 'vietnamese_hanoi', 'vietnamese_hue', 'vietnamese_hochiminhcity',
#              'serbocroatian_croatian', 'serbocroatian_serbian']
LANG_CODES = ["portuguese_brazil", "portuguese_portugal"]

BAD_GRAPHEMES = {
    "english_us": {
        "%",
        "/",
        "@",
        "²",
        "à",
        "á",
        "â",
        "ä",
        "æ",
        "ç",
        "è",
        "é",
        "ê",
        "ë",
        "í",
        "î",
        "ï",
        "ñ",
        "ó",
        "ô",
        "õ",
        "ö",
        "ø",
        "ù",
        "ú",
        "ü",
        "ā",
        "ą",
        "č",
        "ē",
        "ę",
        "ğ",
        "ı",
        "ł",
        "ń",
        "ō",
        "ő",
        "œ",
        "ř",
        "ū",
        "ș",
        "ț",
        "ʼ",
        "ṭ",
        "₂",
    },
    "english_uk": {
        "%",
        "/",
        "@",
        "²",
        "à",
        "á",
        "â",
        "ä",
        "æ",
        "ç",
        "è",
        "é",
        "ê",
        "ë",
        "í",
        "î",
        "ï",
        "ñ",
        "ó",
        "ô",
        "õ",
        "ö",
        "ø",
        "ù",
        "ú",
        "ü",
        "ā",
        "ą",
        "č",
        "ē",
        "ę",
        "ğ",
        "ı",
        "ł",
        "ń",
        "ō",
        "ő",
        "œ",
        "ř",
        "ū",
        "ș",
        "ț",
        "ʼ",
        "ṭ",
        "₂",
        "ã",
        "å",
        "û",
        "ī",
        "ž",
        ".",
    },
    "polish": {"+", ".", "ü", "ö", "ø", "ƶ", "ñ", "ç", "à", "á", "è", "é", "í"},
    "french": {".", "/", "º", "å", "æ", "ÿ", "ș"},
    "japanese": {" ", "&", "+", "、", "〆", "〼", "〼", "＝", "𫡤", "・", "×", "ゞ", "ゟ", "ゑ", "ゐ", "ヲ"},
    "mandarin_hani_beijing": {
        "A",
        "B",
        "C",
        "D",
        "E",
        "G",
        "H",
        "I",
        "K",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "S",
        "T",
        "U",
        "V",
        "X",
        "Y",
        "Z",
        "e",
        "p",
        "u",
        "·",
        "α",
        "β",
        "γ",
        "…",
        "⿰",
        "ㄅ",
        "ㄆ",
        "ㄇ",
        "ㄈ",
        "𰚼",
        "𰯼",
        "𫇦",
    },
    "mandarin_hani_taiwan": {
        "A",
        "B",
        "C",
        "D",
        "E",
        "G",
        "H",
        "I",
        "K",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "S",
        "T",
        "U",
        "V",
        "X",
        "Y",
        "Z",
        "e",
        "p",
        "u",
        "·",
        "α",
        "β",
        "γ",
        "…",
        "⿰",
        "ㄅ",
        "ㄆ",
        "ㄇ",
        "ㄈ",
        "𰚼",
        "𰯼",
        "𫇦",
    },
    "mandarin_hani_standard": {
        "A",
        "B",
        "C",
        "D",
        "E",
        "G",
        "H",
        "I",
        "K",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "S",
        "T",
        "U",
        "V",
        "X",
        "Y",
        "Z",
        "e",
        "p",
        "u",
        "·",
        "α",
        "β",
        "γ",
        "…",
        "⿰",
        "ㄅ",
        "ㄆ",
        "ㄇ",
        "ㄈ",
        "𰚼",
        "𰯼",
        "𫇦",
    },
    "german": {"'", ".", "@", "à", "á", "ç", "è", "é", "ê", "ó", "ø", "œ", "í", "ë"},
    "portuguese_brazil": {".", "🆒"},
    "portuguese_portugal": {".", "🆒"},
    "russian": {"'", ".", "/", "ѳ"},
    "spanish_spain": {"'", ".", "ö", "ꝇ", "î", "ç"},
    "spanish_latin_america": {"'", ".", "ö", "ꝇ", "î", "ç"},
    "thai": {"…", "'", "/"},
    "turkish": {"̇", "'"},
    "tamil": {"ࢳ", "ࢳ", "ࢴ", "ࢴ", "ஃ"},
    "vietnamese_hanoi": {
        "'",
        ".",
        ",",
    },
    "vietnamese_hue": {
        "'",
        ".",
        ",",
    },
    "vietnamese_hochiminhcity": {
        "'",
        ".",
        ",",
    },
}


BAD_PHONES = {
    "english_uk": {"ɪː", "aː", "eː", "a", "o", "oː", "eː", "e"},
    "english_us": {"ɒ", "aː", "a", "o", "oː", "eː", "e", "ɪː", "ɛː"},
    "german": {"ʊɪ"},
    "czech": {"ə"},
    "spanish_latin_america": {"ɹ", "ɚ", "ʒ", "ə", "ɪ"},
    "spanish_spain": {"ɹ", "ɚ", "ʒ", "ə", "ɪ"},
    "mandarin_hani_taiwan": {"ai", "a", "ei", "o", "ə", "z̩", "ʐ̩"},
    "mandarin_hani_standard": {"ai", "a", "ei", "o", "ə", "z̩", "ʐ̩"},
    "mandarin_hani_beijing": {"ai", "a", "ei", "o", "ə", "z̩", "ʐ̩"},
    "portuguese_brazil": {"ɜ", "ǀ", "ɱ", "ə̃", "ə", "y", "ɹ", "dz", "ɐ̃̃", "o̝"},
    "portuguese_portugal": {"ɜ", "ǀ", "ɱ", "ə̃", "ə", "y", "ɹ", "dz", "ɐ̃̃", "o̝"},
}

VOWELS = {
    "english_us": {
        "aɪ",
        "aʊ",
        "eɪ",
        "i",
        "iː",
        "oɪ",
        "oʊ",
        "u",
        "uː",
        "æ",
        "ɑ",
        "ɑː",
        "ɔ",
        "ɔɪ",
        "ɔː",
        "ə",
        "ɚ",
        "ɛ",
        "ɝ",
        "ɝː",
        "ɪ",
        "ʊ",
        "ʌ",
    },
    "english_uk": {
        "aɪ",
        "aʊ",
        "eɪ",
        "i",
        "iː",
        "oɪ",
        "oʊ",
        "u",
        "uː",
        "æ",
        "ɑ",
        "ɑː",
        "ɔ",
        "ɔɪ",
        "ɔː",
        "ə",
        "ɚ",
        "ɛ",
        "ɝ",
        "ɝː",
        "ɪ",
        "ʊ",
        "ʌ",
        "aɪ",
        "aʊ",
        "eɪ",
        "i",
        "iː",
        "oɪ",
        "oʊ",
        "u",
        "uː",
        "æ",
        "ɑ",
        "ɑː",
        "ɒ",
        "ɔ",
        "ɔɪ",
        "ɔː",
        "ɛ",
        "ɛː",
        "ɜ",
        "ɜː",
        "ʊ",
        "ʌ",
    },
    "vietnamese_hanoi": {"a", "aː", "e", "i", "o", "u", "ɔ", "ə", "əː", "ɛ", "ɨ", "ʊ", "ɪ"},
    "vietnamese_hue": {"a", "aː", "e", "i", "o", "u", "ɔ", "ə", "əː", "ɛ", "ɨ", "ʊ", "ɪ"},
    "vietnamese_hochiminhcity": {
        "a",
        "aː",
        "e",
        "i",
        "o",
        "u",
        "ɔ",
        "ə",
        "əː",
        "ɛ",
        "ɨ",
        "ʊ",
        "ɪ",
    },
    "portuguese_portugal": {
        "a",
        "e",
        "o",
        "i",
        "u",
        "i",
        "ɛ",
        "ɐ",
        "ɔ",
        "ĩ",
        "õ",
        "ɐ̃",
        "ẽ",
        "ẽ",
        "ũ",
        "ũ",
        "õ",
        "ĩ",
        "ɨ",
    },
    "portuguese_brazil": {
        "a",
        "e",
        "o",
        "i",
        "u",
        "i",
        "ɛ",
        "ɐ",
        "ɔ",
        "ĩ",
        "õ",
        "ɐ̃",
        "ẽ",
        "ẽ",
        "ũ",
        "ũ",
        "õ",
        "ĩ",
        "ɨ",
    },
    "mandarin_hani": {"a", "e", "o", "i", "u", "y", "ə", "ɚ", "ɤ̃", "ʊ̃"},
    "mandarin_hani_standard": {"a", "e", "o", "i", "u", "y", "ə", "ɚ", "ɤ̃", "ʊ̃"},
    "mandarin_hani_taiwan": {"a", "e", "o", "i", "u", "y", "ə", "ɚ", "ɤ̃", "ʊ̃"},
    "mandarin_hani_beijing": {"a", "e", "o", "i", "u", "y", "ə", "ɚ", "ɤ̃", "ʊ̃"},
    "thai": {
        "a",
        "aː",
        "e",
        "eː",
        "i",
        "iː",
        "o",
        "oː",
        "u",
        "ə",
        "uː",
        "ɔ",
        "ɔː",
        "ɛ",
        "ɛː",
        "ɤ",
        "ɤː",
        "ɯ",
        "ɯː",
    },
    "swedish": {
        "a",
        "aʊ",
        "aː",
        "e",
        "eː",
        "i",
        "iː",
        "o",
        "oː",
        "u",
        "uː",
        "y",
        "yʷ",
        "yː",
        "æ",
        "æː",
        "êː",
        "ø",
        "øː",
        "ø̀ː",
        "œ",
        "œː",
        "œ̞",
        "œ̞ː",
        "ɑ",
        "ɑː",
        "ɒː",
        "ɒ̀ː",
        "ɔ",
        "ə",
        "ɚ",
        "ɛ",
        "ɛɵ",
        "ɛː",
        "ɛ̂",
        "ɛ̄",
        "ɜ",
        "ɝ",
        "ɪ",
        "ɵ",
        "ɵː",
        "ɵ̄",
        "ɶ",
        "ɶː",
        "ʉ",
        "ʉː",
        "ʉ̂ː",
        "ʉ̟ː",
        "ʊ",
        "ʊː",
        "ʏ",
        "ỳː",
        "ỵː",
    },
}

VOWEL_PATTERNS = {
    "swedish": re.compile(r"^[aeiɛøæuoʊêɔɪœɑʉɵɶ̂œ̞ː˧˩ɒyʏʉ̟ː˧˩əː˧˩˥]+$"),
}


LANG_MAPPING = {
    "bulgarian": {
        "d̪": "d",
        "t̪": "t",
        "ɐ": "a",
        "æ": "a",
        "a̟": "a",
        "e": "ɛ",
        "ə": "ɤ",
        "o̝": "ɔ",
        "o̟": "ɔ",
        "u̟": "u",
        "ʉ": "u",
        "ʊ": "u",
        "ɤ̞": "ɤ",
        "ɤ̟": "ɤ",
        "lʲ": "ʎ",
        "l": "ɫ",
        "ɾ": "r",
        "iː": "i j",
        "s̪": "s",
        "n̪": "n",
        "ɾʲ": "rʲ",
        "nʲ": "ɲ",
        "ɡʲ": "ɟ",
        "kʲ": "c",
    },
    "russian": {},
    "czech": {
        "ɫ": "l",
        "ɾ": "r",
        "ɔ": "o",
        "ɔː": "oː",
    },
    "serbocroatian_croatian": {
        "ʋ": "v",
        "ɕ": "ʃ",
        "ʑ": "ʒ",
        "ô": "o˦˨",
        "ôː": "oː˦˨",
        "ûː": "uː˦˨",
        "û": "u˦˨",
        "î": "i˦˨",
        "îː": "iː˦˨",
        "êː": "eː˦˨",
        "ê": "e˦˨",
        "âː": "aː˦˨",
        "â": "a˦˨",
        "r̂": "r̩˦˨",
        "r̂ː": "r̩ː˦˨",
        "řː": "r̩ː˨˦",
        "ř": "r̩˨˦",
        "ěː": "eː˨˦",
        "ě": "e˨˦",
        "ǎ": "a˨˦",
        "ǎː": "aː˨˦",
        "ǐː": "iː˨˦",
        "ǐ": "i˨˦",
        "ǒ": "o˨˦",
        "ǒː": "oː˨˦",
        "ǔː": "uː˨˦",
        "ǔ": "u˨˦",
    },
    "serbocroatian_serbian": {
        "ʋ": "v",
        "ɕ": "ʃ",
        "ʑ": "ʒ",
        "ô": "o˦˨",
        "ôː": "oː˦˨",
        "ûː": "uː˦˨",
        "û": "u˦˨",
        "î": "i˦˨",
        "îː": "iː˦˨",
        "êː": "eː˦˨",
        "ê": "e˦˨",
        "âː": "aː˦˨",
        "â": "a˦˨",
        "r̂": "r̩˦˨",
        "r̂ː": "r̩ː˦˨",
        "řː": "r̩ː˨˦",
        "ř": "r̩˨˦",
        "ěː": "eː˨˦",
        "ě": "e˨˦",
        "ǎ": "a˨˦",
        "ǎː": "aː˨˦",
        "ǐː": "iː˨˦",
        "ǐ": "i˨˦",
        "ǒ": "o˨˦",
        "ǒː": "oː˨˦",
        "ǔː": "uː˨˦",
        "ǔ": "u˨˦",
    },
    "french": {"r": "ʁ", "œ̃": "ɛ̃"},
    "vietnamese_hanoi": {
        "k̟̚": "k̚",
        "ŋ̟": "ŋ",
        "ï": "ɨ",
    },
    "german": {
        "b̥": "b",
        "d̥": "d",
        "ɡ̊": "ɡ",
        "r": "ʁ",
        "ŋ̍": "n̩",
        "ɱ̩": "n̩",
        "ŋ̩": "n̩",
        "ʀ": "ʁ",
        "χ": "x",
        "ʋ": "v",
        "ɘ": "ə",
        "i": "ɪ",
        "ø": "øː",
        "o": "ɔ",
        "u": "ʊ",
        "œː": "øː",
        "y": "ʏ",
        "e": "ɛ",
        "ɛː": "eː",
        "ɔː": "oː",
        "ɑː": "aː",
        "ɒː": "aː",
    },
    "mandarin_hani": {
        "b̥": "p",
        "d̥": "t",
        "g̊": "k",
        "ɡ̊": "k",
        "ɖʐ̥": "ʈʂ",
        "dz̥": "ts",
        "dʑ̥": "tɕ",
        "ä": "a",
        "æ̃": "a",
        "ɤ": "o",
        "ɤ̃": "o",
        "ʊ̃": "o",
        "ɪ": "i",
        "ɻʷ": "ɻ",
        "ʊ": "u",
        "ɛ": "e",
        "ɑ": "a",
        "ɑ̃": "a",
        "ɔ": "o",
        "ɔː": "o",
        "⁵⁵": "˥",
        "⁵¹": "˥˩",
        "³⁵": "˧˥",
        "²¹⁴": "˨˩˦",
    },
    "mandarin_hani_taiwan": {
        "b̥": "p",
        "d̥": "t",
        "g̊": "k",
        "ɡ̊": "k",
        "ɖʐ̥": "ʈʂ",
        "dz̥": "ts",
        "dʑ̥": "tɕ",
        "ä": "a",
        "æ̃": "a",
        "ɤ": "o",
        "ɤ̃": "o",
        "ʊ̃": "o",
        "ɪ": "i",
        "ɻʷ": "ɻ",
        "ʊ": "u",
        "ɛ": "e",
        "ɑ": "a",
        "ɑ̃": "a",
        "ɔ": "o",
        "ɔː": "o",
        "⁵⁵": "˥",
        "⁵¹": "˥˩",
        "³⁵": "˧˥",
        "²¹⁴": "˨˩˦",
    },
    "mandarin_hani_beijing": {
        "b̥": "p",
        "d̥": "t",
        "g̊": "k",
        "ɡ̊": "k",
        "ɖʐ̥": "ʈʂ",
        "dz̥": "ts",
        "dʑ̥": "tɕ",
        "ä": "a",
        "æ̃": "a",
        "ɤ": "o",
        "ɤ̃": "o",
        "ʊ̃": "o",
        "ɪ": "i",
        "ɻʷ": "ɻ",
        "ʊ": "u",
        "ɛ": "e",
        "ɑ": "a",
        "ɑ̃": "a",
        "ɔ": "o",
        "ɔː": "o",
        "⁵⁵": "˥",
        "⁵¹": "˥˩",
        "³⁵": "˧˥",
        "²¹⁴": "˨˩˦",
    },
    "mandarin_hani_standard": {
        "b̥": "p",
        "d̥": "t",
        "g̊": "k",
        "ɡ̊": "k",
        "ɖʐ̥": "ʈʂ",
        "dz̥": "ts",
        "dʑ̥": "tɕ",
        "ä": "a",
        "æ̃": "a",
        "ɤ": "o",
        "ɤ̃": "o",
        "ʊ̃": "o",
        "ɪ": "i",
        "ɻʷ": "ɻ",
        "ʊ": "u",
        "ɛ": "e",
        "ɑ": "a",
        "ɑ̃": "a",
        "ɔ": "o",
        "ɔː": "o",
        "⁵⁵": "˥",
        "⁵¹": "˥˩",
        "³⁵": "˧˥",
        "²¹⁴": "˨˩˦",
    },
    "polish": {
        "s̪": "s",
        "r̥ː": "r",
        "r̥": "r",
        "ɫ": "l",
        "w̃": "n",
    },
    "portuguese_brazil": {
        "ã": "ɐ̃",
        "uː": "u",
        "ɔ̃": "õ",
        "ɛ̃": "ẽ",
        "ø": "e",
        "ɫ": "l",
        # "ɹ": "ɾ",
        "ɻ": "ɾ",
        # "χ": "ɾ",
        "ɣ": "ɡ",
        "ð": "d",
        "β": "b",
        "ɦ": "x",
        "h": "x",
        "r": "ʁ",
        "ɪ": "i",
        "ʊ": "u",
        "ɲ": "j̃",
        "ɪ̯̃": "j̃",
    },
    "portuguese_portugal": {
        "ã": "ɐ̃",
        "uː": "u",
        "ɔ̃": "õ",
        "ɛ̃": "ẽ",
        "ɣ": "ɡ",
        "ð": "d",
        "β": "b",
        "ø": "e",
        "l": "ɫ",
        # "r": "ʁ",
        "ɻ": "ɾ",
        "h": "x",
    },
    "swedish": {
        "ɛ̄": "ɛ̂",
        "ɵ̄": "ɵ̂",
        "ɘ": "ɵ",
        "ə": "ɛ",
        "ʁ": "r",
        "ɾ": "r",
        "ɹ": "r",
        "v": "ʋ",
        "w": "ʋ",
        "ɜ": "ɛ",
        "æː": "ɛː",
        "ø": "øː",
        "æ": "ɛ",
        "ˇl": "l",
        "yʷ": "y",
        "œ̞ː": "øː",
        "œː": "øː",
        "œ̞": "œ",
        "ç": "ɕ",
        "bː": "b",  # removing length in consonants
        "ɖː": "ɖ",
        "ɖˑ": "ɖ",
        "ˈt": "tʰ",
        "ˈk": "kʰ",
        "ˈp": "pʰ",
        "dː": "d",
        "jː": "j",
        "kː": "kʰ",
        "lː": "l",
        "mː": "m",
        "nː": "n",
        "fː": "f",
        "ɧː": "ɧ",
        "pː": "pʰ",
        "rː": "r",
        "sː": "s",
        "tˑ": "t",
        "tʰː": "tʰ",
        "pʰː": "pʰ",
        "kʰː": "kʰ",
        "tː": "tʰ",
        "ŋː": "ŋ",
        "ɲ": "ɳ",
        "ɕː": "ɕ",
        "ɡː": "ɡ",
        "ʈː": "ʈʰ",
        "ʈʰː": "ʈʰ",
        "ʂː": "ʈ",
        "ỵː": "yː",
        "ʉ̟̂": "ʉ̂",
        "ʉ̟ː": "ʉː",
        "ʉ̂": "ʉ̂ː",
        "ɒː": "ɑː",
        "aː": "ɑː",
        "ɑ": "ɑː",
        "e": "eː",
        "o": "oː",
        "u": "uː",
        "i": "iː",
        "y": "yː",
        "ɒ̀ː": "ɑ̀ː",
        "ʊː": "ʊ",
        "ʉ": "ʉː",
        "ɵː": "uː",
        "ɶː": "øː",
    },
    "tamil": {
        "l̪": "l",
        "l̪ː": "lː",
        "r̥": "r",
        "ɾ̪": "ɾ",
        "h": "ɦ",
        "tʃ": "tɕ",
        "ɕ": "tɕ",
        "tʃː": "tɕː",
    },
    "thai": {
        "cʰ": "tɕʰ",
        "c": "tɕ",
        "ɔ̌": "ɔ˩˩˦",
        "ǎː": "aː˩˩˦",
        "áː": "aː˦˥",
        "à": "a˨˩",
        "ì": "i˨˩",
    },
    "ukrainian": {
        "ɫ": "l",
        "ʍ": "ʋ",
        "w": "ʋ",
        "v": "ʋ",
        #'e': 'ɛ',
        #'o': 'ɔ',
        "ɫː": "lː",
    },
    "japanese": {
        "o̞": "o",
        "n̩": "n",
        "ä": "a",
        "ɡ̊": "ɡ",
        "ḁ": "a",
        "ẽ": "e",
        "m̩ː": "mː",
        "e̥": "e",
        "u͍": "ɯ",
        "ɯ̃ᵝ": "ɯ",
        "u͍ː": "ɯː",
        "w͍": "w",
        "y": "j",
        "r": "ɾ",
        "ɽ": "ɾ",
        "ɾ̥": "ɾ",
        "ɯᵝ": "ɯ",
        "ɯᵝː": "ɯː",
        "ɯ̟̃ᵝː": "ɯː",
        "ɯ̥ᵝ": "ɯ̥",
        "ʲkʲ": "kʲ",
        "nʲ": "ɲ",
        "tɕʲ": "tɕ",
        "ɕʲ": "ɕ",
        "ĩː": "iː",
        "õ̞ː": "oː",
        "i̥̥": "i̥",
        "e̞̊": "e",
        "ẽ̞ː": "eː",
        "ã̠ː": "aː",
        "õ̞": "o",
        "d̥": "d",
        "b̥": "b",
        "o̞ː": "oː",
        "e̞ː": "eː",
        "e̞": "e",
        "ẽ̞": "e",
        "ĩ": "i",
        "ɸ̥": "ɸ",
        "ɨ̃ᵝː": "ɨː",
        "ĩ̥": "i",
        "a̠ː": "aː",
        "a̠": "a",
        "o̞̊": "o",
        "dʑʲ": "dʑ",
        "ɾ̠": "ɾ",
        "ã̠": "a",
        "õ̥": "o",
        "dʲ": "dʑ",
        "tʲ": "tɕ",
        # 'ɯ̟ᵝ': 'ɯ',
        "ɰᵝ": "w",
        "ɰᵝː": "wː",
        # 'ɯ̟̊ᵝ': 'ɨ̥',
        # 'ɯ̟ᵝː': 'ɨː',
        # 'ɯ̟̃ᵝ': 'ɨ',
        # 'ɨ̥ᵝ': 'ɨ̥',
        # 'ɨᵝ': 'ɨ',
        # 'ɨ̃ᵝ': 'ɨ',
        # 'ɨᵝː': 'ɨː',
        "ɯ̟̊": "ɯ̥",
        "ɲ̟": "ɲ",
        "ŋʲ": "ɲ",
        "p̚ʲ": "p̚",
        "k̚ʲ": "k̚",
        "t̚ʲ": "t̚",
    },
    "turkish": {
        "ɑ": "a",
        "ɑː": "a",
        "aː": "a",
        "iː": "i",
        "uː": "u",
        "ɛ": "e",
        "e̞": "e",
        "ɔ": "o",
        "ʊ": "u",
        "ʏ": "y",
        "β": "v",
        "o̞": "o",
        "ɪ": "i",
        "ø": "œ",
        "ɾ̝̊": "ɾ",
    },
    "korean_hangul": {
        "a̠": "a",
        "e̞": "e",
        "e̞ː": "eː",
        "a̠ː": "a",
        "o̞": "o",
        "o̞ː": "oː",
        "ʌ̹": "ʌ",
        "ɘː": "ʌː",
        "ɦ": "h",
        "ɸʷ": "ɸ",
        "ʃʰ": "sʰ",
    },
    "english_uk": {
        "ɝː": "ɜː",
        "əː": "ɜː",
        "æː": "æ",
        "ɝ": "ɜ",
        "ɚ": "ə",
        "ɫ": "l",
        "r": "ɹ",
        "ʍ": "w",
    },
    "english_us": {
        "ɫ": "l",
        "r": "ɹ",
        "ʍ": "w",
        "æː": "æ",
    },
    "spanish_spain": {
        "ɣ̞": "ɣ",
        "β̞": "β",
        "ð̞": "ð",
        "θ̬": "θ",
        "w̝": "w",
        "nʲ": "ɲ",
        "n̟": "n",
        "lʲ": "ʎ",
        "l̟": "l",
        "i̯": "j",
        "u̯": "w",
        "h": "x",
        "n̪": "n",
        "d": "d̪",
    },
    "spanish_latin_america": {
        "ɣ̞": "ɣ",
        "β̞": "β",
        "ð̞": "ð",
        "w̝": "w",
        "nʲ": "ɲ",
        "lʲ": "ʎ",
        "i̯": "j",
        "u̯": "w",
        "n̪": "n",
        "l̪": "l",
        "l̟": "l",
        "h": "x",
        "n̟": "n",
        "d": "d̪",
    },
}

GLOBAL_REMAPPING = {
    "õ": "õ",  # Fix glyphs to use diacritics
    "ẽ": "ẽ",
    "ũ": "ũ",
    "ĩ": "ĩ",
    "ã": "ã",
}


def _skip_word(word, lang):
    if lang in BAD_GRAPHEMES:
        if any(x in BAD_GRAPHEMES[lang] for x in word):
            return True
    if word.startswith("-"):
        return True
    # Skips examples containing digits.
    if re.search(r"\d", word):
        return True
    return False


def _process_wiki_pron(phones):
    tokenizer = segments.Tokenizer()
    phones = unicodedata.normalize("NFD", phones)
    phones = re.sub(r"[-ˈˌ.()#]", "", phones)
    phones = tokenizer(phones, ipa=True).split()
    new_phones = []
    for p in phones:
        new_phones.append(p)
    new_pron = " ".join(new_phones)
    new_pron = unicodedata.normalize("NFC", new_pron)
    new_pron = re.sub(r"[-ˈˌ.()#]", "", new_pron)
    return new_pron.split()


def _check_dialect(lang, dialect):
    if not dialect:
        return True
    d = lang.split("_")[-1]
    if dialect.lower() == d:
        return True
    return False


def read_source(lang):
    graphemes = set()
    phones = set()
    dictionary = []
    path = os.path.join(SCRAPE_DIR, LANG_PATHS[lang])
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "\t" in line:
                line = line.split("\t")
                word = line[0]
                dialect = line[1]
                pronunciation = line[2]
            else:
                line = line.split()
                word = line[0]
                pronunciation = line[1:]
            if not _check_dialect(lang, dialect):
                continue
            if _skip_word(word, lang):
                continue
            pronunciation = _process_wiki_pron(pronunciation)
            graphemes.update(word)
            phones.update(pronunciation)
            dictionary.append((word, pronunciation))
    return dictionary, graphemes, phones


def save_dictionary(dictionary, lang):
    deduplication = set()
    final_phones = collections.Counter()
    path = os.path.join(OUTPUT_DIR, f"{lang}_mfa.dict")
    with open(path, "w", encoding="utf8") as f:
        for w, p in sorted(dictionary):
            final_phones.update(p)
            p = " ".join(p)
            if (w, p) in deduplication:
                continue
            f.write("{}\t{}\n".format(w, p))
            deduplication.add((w, p))
    print("Final phones:", sorted(final_phones))
    print("Final phone counts:", sorted(final_phones.items(), key=lambda x: -x[1]))


def convert_language_specific(word, phones, lang):
    new_pron = []
    if lang == "swedish":
        for i, p in enumerate(phones):
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    phones[i] = v
                    break

        for i, p in enumerate(phones):
            if p == "¹":
                found_first = False
                found_second = False
                for j in range(i + 1, len(phones)):
                    if VOWEL_PATTERNS[lang].match(phones[j]):
                        if not found_first:
                            phones[j] += "˥˧"  # Falling tone
                            found_first = True
                        elif not found_second:
                            phones[j] += "˩"  # Low tone
                            found_second = True
                        else:
                            break
                continue
            elif p == "²":
                found_first = False
                found_second = False
                for j in range(i + 1, len(phones)):
                    if phones[j] in VOWELS[lang]:
                        if not found_first:
                            phones[j] += "˧˩"  # Falling tone
                            found_first = True
                        elif not found_second:
                            phones[j] += "˥˩"  # Falling tone
                            found_second = True
                        else:
                            break
                continue
            new_pron.append(p)
        phones = new_pron
    new_pron = []
    for i, p in enumerate(phones):
        if lang == "english_us":
            if lang in LANG_MAPPING:
                for k, v in LANG_MAPPING[lang].items():
                    if p == k:
                        p = v
                        break

            if p == "ʒ" and len(new_pron) and new_pron[-1] == "d":  # fix up affricates being split
                new_pron[-1] = "dʒ"
                continue
            elif (
                p == "ʃ" and len(new_pron) and new_pron[-1] == "t"
            ):  # fix up affricates being split
                new_pron[-1] = "tʃ"
                continue
            elif p in ["ɪ", "j"] and len(new_pron) and new_pron[-1] in {"e", "ɔ", "o"}:
                new_pron[-1] += "ɪ"
                continue
            elif p in {"ʊ", "u"} and len(new_pron) and new_pron[-1] in {"a", "ɑ", "ʌ"}:
                new_pron[-1] = "aʊ"
                continue
            elif p in ["ɪ", "j"] and len(new_pron) and new_pron[-1] in {"a", "ɑ", "ʌ"}:
                new_pron[-1] = "aɪ"
                continue
            elif p in {"ʊ", "u"} and len(new_pron) and new_pron[-1] in {"ə", "o", "ɔ"}:
                new_pron[-1] = "oʊ"
                continue
            elif p in {"ɹ", "ɚ"} and len(new_pron) and new_pron[-1] in {"o", "ɔ"}:
                new_pron[-1] = "ɔ"
                p = "ɹ"
            elif p in {"ɹ", "ɚ"} and len(new_pron) and new_pron[-1] in {"i", "ɪː", "ɪ"}:
                new_pron[-1] = "ɪ"
                p = "ɹ"
            elif p in {"ɹ", "ɚ"} and len(new_pron) and new_pron[-1] in {"u", "ʊ"}:
                new_pron[-1] = "ʊ"
                p = "ɹ"
            elif p in {"ɹ", "ɚ"} and len(new_pron) and new_pron[-1] in {"e", "ɛ", "ɛː", "æ", "æː"}:
                new_pron[-1] = "ɛ"
                p = "ɹ"
            elif p == "ɹ" and len(new_pron) and new_pron[-1] in ["ɜ", "ɜː"]:
                new_pron[-1] = "ɝ"
                continue
            elif (
                p == "ɹ"
                and len(new_pron) > 1
                and new_pron[-1] == "ə"
                and new_pron[-2] in {"ɪ", "i", "ɪː"}
            ):
                new_pron[-1] = "ɹ"
                new_pron[-2] = "ɪ"
                continue
            elif (
                p == "ɹ"
                and len(new_pron) > 1
                and new_pron[-1] == "ə"
                and new_pron[-2] in {"ʊ", "u"}
            ):
                new_pron[-1] = "ɹ"
                new_pron[-2] = "ʊ"
                continue
            elif (
                p == "ɹ"
                and len(new_pron) > 1
                and new_pron[-1] == "ə"
                and new_pron[-2] in {"e", "ɛ", "ɛː"}
            ):
                new_pron[-1] = "ɹ"
                new_pron[-2] = "ɛ"
                continue
            elif p == "w" and len(new_pron) and new_pron[-1] == "h":  # get rid of h w sequences
                new_pron[-1] = "w"
                continue
            elif p in {"k", "ɡ"} and len(new_pron) and new_pron[-1] == "n":
                new_pron[-1] = "ŋ"
                continue
            elif p in {"ɜ", "ɜː"} and (i == len(phones) - 1 or phones[i + 1] != "ɹ"):
                p = "ɝ"
            elif p == "ɪ" and i == len(phones) - 1:
                p = "i"
            elif (
                p == "l" and len(new_pron) and new_pron[-1] == "ə" and i == len(phones) - 1
            ):  # final syllabic l's
                new_pron[-1] = "l̩"
                continue
            elif (
                p == "m" and len(new_pron) and new_pron[-1] == "ə" and i == len(phones) - 1
            ):  # final syllabic m's
                new_pron[-1] = "m̩"
                continue
            elif (
                p == "n" and len(new_pron) and new_pron[-1] == "ə" and i == len(phones) - 1
            ):  # final syllabic n's
                new_pron[-1] = "n̩"
                continue
            elif (
                p == "ɹ" and len(new_pron) and new_pron[-1] == "ə" and i == len(phones) - 1
            ):  # final syllabic r's
                new_pron[-1] = "ɚ"
                continue
            elif p == "ŋ" and i == len(phones) - 1 and new_pron[-1] == "i":
                new_pron[-1] = "ɪ"
                continue
        elif lang == "english_uk":
            if lang in LANG_MAPPING:
                for k, v in LANG_MAPPING[lang].items():
                    if p == k:
                        p = v
                        break
            if p == "ɹ" and i == len(phones) - 1:
                continue
            elif p == "ɪ" and i == len(phones) - 1:
                p = "i"
            elif (
                p in {"l", "m", "n"}
                and i == len(phones) - 1
                and len(new_pron)
                and new_pron[-1] in {"ə", "əː"}
            ):
                new_pron[-1] = p + "̩"
                continue
            elif p == "ɪ" and len(new_pron) and new_pron[-1] in {"e", "a", "ɔ", "o"}:
                new_pron[-1] = new_pron[-1] + p
                continue
            elif p == "ʊ" and len(new_pron) and new_pron[-1] in {"e", "a"}:
                new_pron[-1] = new_pron[-1] + p
                continue
            elif p in {"ʊ", "u"} and len(new_pron) and new_pron[-1] in {"ə", "o", "ɔ"}:
                new_pron[-1] = "oʊ"
                continue
            elif (
                p == "ʒ" and len(new_pron) and new_pron[-1] == "d"
            ):  # fix up affricates being split
                new_pron[-1] = "dʒ"
                continue
            elif (
                p == "ʃ" and len(new_pron) and new_pron[-1] == "t"
            ):  # fix up affricates being split
                new_pron[-1] = "tʃ"
                continue
            elif p == "w" and len(new_pron) and new_pron[-1] == "h":  # get rid of h w sequences
                new_pron[-1] = "w"
                continue
            elif p in {"k", "ɡ"} and len(new_pron) and new_pron[-1] == "n":
                new_pron[-1] = "ŋ"
                continue
            elif p == "ə" and len(new_pron) and new_pron[-1] == "ɛ":
                new_pron[-1] = "ɛː"
                continue
            elif p == "ŋ" and i == len(phones) - 1 and new_pron[-1] == "i":
                new_pron[-1] = "ɪ"
                continue
            elif (
                p == "ɹ"
                and len(new_pron) > 2
                and new_pron[-1] == "ə"
                and new_pron[-2] in {"e", "ɛ", "ʊ", "ɪ", "ɪː", "ɛː"}
            ):
                new_pron[-1] = p
                continue
        elif lang == "bulgarian":
            if p in {"s", "ʃ", "sʲ"} and len(new_pron) and new_pron[-1] == "t":
                new_pron[-1] += p
                continue
            elif p == "ʒ" and len(new_pron) and new_pron[-1] == "d":
                new_pron[-1] = "dʒ"
                continue
            elif p in {"ɡ", "k"} and len(new_pron) and new_pron[-1] in {"n"}:
                new_pron[-1] = "ŋ"
            elif p in {"v", "f"} and len(new_pron) and new_pron[-1] in {"n"}:
                new_pron[-1] = "ɱ"
        elif lang == "czech":
            if p in {"u", "ʊ"} and len(new_pron) and new_pron[-1] in {"o", "ɔ"}:
                new_pron[-1] = "ow"
                continue
            elif p in ["u", "ʊ"] and len(new_pron) and new_pron[-1] in {"a"}:
                new_pron[-1] = "aw"
                continue
            elif p in {"u", "ʊ"} and len(new_pron) and new_pron[-1] in {"e", "ɛ"}:
                new_pron[-1] = "ew"
                continue
            elif p in {"ʃ", "s"} and len(new_pron) and new_pron[-1] in {"t"}:
                new_pron[-1] += p
                continue
            elif p in {"ʒ"} and len(new_pron) and new_pron[-1] in {"d"}:
                new_pron[-1] += p
                continue
            elif p == "ʊ":
                p = "u"
            elif p == "e":
                p = "ɛ"
        elif lang.startswith("serbocroatian"):
            if p in {"ɕ", "ʂ", "ʃ"} and len(new_pron) and new_pron[-1] == "t":
                new_pron[-1] += p
                continue
            elif p in {"ʑ", "ʐ", "ʒ"} and len(new_pron) and new_pron[-1] == "d":
                new_pron[-1] += p
                continue
        elif lang == "german":
            if lang in LANG_MAPPING:
                for k, v in LANG_MAPPING[lang].items():
                    if p == k:
                        p = v
                        break
            if p in {"ʏ", "ɪ"} and len(new_pron) and new_pron[-1] in {"o", "ɔ"}:
                new_pron[-1] = "ɔʏ"
                continue
            elif p == "ɪ" and len(new_pron) and new_pron[-1] == "a":
                new_pron[-1] = "aɪ"
                continue
            elif p == "ɪ" and len(new_pron) and new_pron[-1] == "ʊ":
                new_pron[-1] = "ʊɪ"
                continue
            elif p == "ʊ" and len(new_pron) and new_pron[-1] == "a":
                new_pron[-1] = "aʊ"
                continue
            elif p == "e" and len(new_pron) and new_pron[-1] == "ɐ":
                new_pron[-1] = "ɐ"
                continue
            elif p == "ʔ":
                continue
            elif p in {"tʰ", "kʰ", "pʰ"} and i == len(phones) - 1:
                p = p[0]
            elif (
                p in {"tʰ", "kʰ", "pʰ"}
                and len(new_pron)
                and new_pron[-1] in {"s", "ts", "ʃ", "tʃ"}
            ):
                p = p[0]
            elif p in {"t", "k", "p"} and i == 0:
                p += "ʰ"
            elif p in {"s", "ʃ"} and i == 1 and new_pron[-1] in {"tʰ"}:
                new_pron[-1] = "t" + p
                continue
            elif (
                p in {"v", "s", "x", "ʁ", "l", "j"}
                and len(new_pron)
                and new_pron[-1] in {"tʰ", "kʰ", "pʰ"}
            ):
                new_pron[-1] = new_pron[-1][0]
            elif p == "s" and len(new_pron) and new_pron[-1] == "t":
                if "z" in word or "c" in word:
                    new_pron[-1] = "ts"
                    continue
            elif p == "õ":
                new_pron.append("ɔ")
                new_pron.append("n")
                continue
            elif p == "ɛ̃":
                new_pron.append("eː")
                new_pron.append("n")
                continue
        elif lang.startswith("mandarin_hani"):
            vowel_pattern = re.compile(r"^[ayeiouəɚʊɤ̃]+[²³⁰¹⁴⁵]*$")
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
            if p in {"²", "³", "¹", "⁰", "⁴", "⁵", "⁻", "⁽", "⁾"} and len(new_pron):
                index = -1
                for j in range(len(new_pron) - 1, -1, -1):
                    if vowel_pattern.match(new_pron[j]) or "̩" in new_pron[j]:
                        index = j
                        break
                if new_pron[index].endswith("²¹⁴"):
                    continue
                new_pron[index] += p
                continue
            elif p.startswith("ˀ"):
                new_pron.append("ʔ")
                if p[1] in LANG_MAPPING[lang]:
                    new_pron.append(LANG_MAPPING[lang][p[1]])
                else:
                    new_pron.append(p[1])
                continue
            elif (
                any(p.startswith(x) for x in VOWELS[lang])
                and len(new_pron)
                and re.match(r"^[ayeiouəɚʊɤ̃]+$", new_pron[-1])
            ):
                new_pron[-1] += p
                continue
        elif lang == "portuguese_brazil":
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
            if p.startswith("i") and len(new_pron) and new_pron[-1] == "l":
                new_pron[-1] = "ʎ"
            elif p == "w" and len(new_pron) and new_pron[-1] in {"k", "ɡ"}:
                new_pron[-1] += "ʷ"
                continue
            elif p in {"m", "n"} and len(new_pron) and "̃" in new_pron[-1]:
                new_pron[-1] = new_pron[-1].replace("̃", "")
        elif lang == "portuguese_portugal":
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
            if p == "w" and len(new_pron) and new_pron[-1] in {"k", "ɡ"}:
                new_pron[-1] += "ʷ"
                continue
            elif p in {"m", "n"} and len(new_pron) and "̃" in new_pron[-1]:
                new_pron[-1] = new_pron[-1].replace("̃", "")
            elif p == "o" and i == len(phones) - 1:
                p = "o w"
        elif lang == "swedish":
            if p == "ʒ" and len(new_pron) and new_pron[-1] == "d":
                new_pron[-1] += p
                continue
            elif (
                p in {"k", "kʰ", "ɡ"}
                and len(new_pron)
                and new_pron[-1] in {"m", "n", "ɳ", "ɲ", "ŋ"}
            ):
                new_pron[-1] = "ŋ"
            elif (
                p in {"t", "tʰ", "d"}
                and len(new_pron)
                and new_pron[-1] in {"m", "n", "ɳ", "ɲ", "ŋ"}
            ):
                new_pron[-1] = "n"
            elif (
                p in {"p", "pʰ", "b"}
                and len(new_pron)
                and new_pron[-1] in {"m", "n", "ɳ", "ɲ", "ŋ"}
            ):
                new_pron[-1] = "m"
            elif (
                p in {"ʈ", "ʈʰ", "ɖ", "ʂ"}
                and len(new_pron)
                and new_pron[-1] in {"m", "n", "ɳ", "ɲ", "ŋ"}
            ):
                new_pron[-1] = "ɳ"
            elif p == "s" and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ʂ"
                continue
            elif p in {"t", "ʈ"} and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ʈ"
                continue
            elif p in {"d", "ɖ"} and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ɖ"
                continue
            elif (
                p in {"n", "ɳ"} == "n"
                and len(new_pron)
                and new_pron[-1] == "r"
                and "rr" not in word
            ):
                new_pron[-1] = "ɳ"
                continue
            elif p in {"l", "ɭ"} and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ɭ"
                continue
            elif p in {"tʰ", "ʈʰ"} and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ʈʰ"
                continue
            elif p in {"s", "ʂ"} and len(new_pron) and new_pron[-1] == "r" and "rr" not in word:
                new_pron[-1] = "ʂ"
                continue
            elif p == "aʊ":
                new_pron.append("a")
                new_pron.append("ʊ")
                continue
            elif p in {"r", "n", "l", "t", "k", "ɡ"} and len(new_pron) and new_pron[-1] == "ə":
                new_pron[-1] = "ɛ"
            elif p in {"t", "k", "p", "ʈ"} and not len(new_pron):
                p += "ʰ"
            elif (
                not VOWEL_PATTERNS[lang].match(p)
                and len(new_pron)
                and new_pron[-1] in {"tʰ", "kʰ", "pʰ", "ʈʰ"}
            ):
                new_pron[-1] = new_pron[-1][0]
            elif (
                p in {"tʰ", "kʰ", "pʰ", "ʈʰ"}
                and len(new_pron)
                and (new_pron[-1] in {"ʂ", "s"} or i == len(phones) - 1)
            ):
                p = p[0]
            elif p == "ə" and i == len(phones) - 1:
                p = "e"
            elif p in {"r"} and len(new_pron) and new_pron[-1] == "ɜ":
                new_pron[-1] = "æː"
            elif p == "ɜ" and i == len(phones) - 1:
                p = "e"
        elif lang == "tamil":
            if p in {"ʊ", "ɪ"} and len(new_pron) and new_pron[-1] == "a":
                new_pron[-1] += p
                continue
        elif lang in ["spanish_spain", "spanish_latin_america"]:
            if p in {"n", "m", "ɲ"} and len(new_pron) and new_pron[-1] in {"n", "m", "ɲ"}:
                new_pron[-1] = p
                continue
            if p in {"s", "z"} and len(new_pron) and new_pron[-1] in {"s", "z"}:
                new_pron[-1] = p
                continue
            if p in {"x", "k", "ɡ"} and len(new_pron) and new_pron[-1] == "n":
                new_pron[-1] = "ŋ"
            elif (
                p in {"ɟʝ", "ʝ", "j", "tʃ", "i", "ĩ"} and len(new_pron) and new_pron[-1] in {"n"}
            ):
                new_pron[-1] = "ɲ"
            elif p in {"j", "i", "ĩ", "e", "ẽ"} and len(new_pron) and new_pron[-1] in {"k"}:
                new_pron[-1] = "c"
            elif p in {"j", "i", "ĩ", "e", "ẽ"} and len(new_pron) and new_pron[-1] in {"x"}:
                new_pron[-1] = "ç"
            elif p in {"j", "i", "ĩ", "e", "ẽ"} and len(new_pron) and new_pron[-1] in {"ɡ"}:
                new_pron[-1] = "ɟ"
            elif p in {"j", "i", "ĩ", "e", "ẽ"} and len(new_pron) and new_pron[-1] in {"ɣ"}:
                new_pron[-1] = "ʝ"
            elif (
                p in {"ɟʝ", "ʝ", "j", "tʃ", "i", "ĩ"} and len(new_pron) and new_pron[-1] in {"l"}
            ):
                new_pron[-1] = "ʎ"
            elif (
                p
                in {
                    "β",
                    "b",
                    "p",
                }
                and len(new_pron)
                and new_pron[-1] == "n"
            ):
                new_pron[-1] = "m"
            elif (
                p
                in {
                    "f",
                    "v",
                }
                and len(new_pron)
                and new_pron[-1] in {"n", "m", "n̪"}
            ):
                new_pron[-1] = "ɱ"
        elif lang == "thai":
            if p in {"a"} and len(new_pron) and new_pron[-1] in {"i", "iː", "ɯ", "ɯː", "u", "uː"}:
                new_pron[-1] += p
                continue
        elif lang == "turkish":
            if p == "ʃ" and len(new_pron) and new_pron[-1] in {"t"}:
                new_pron[-1] += p
                continue
            elif p == "ʒ" and len(new_pron) and new_pron[-1] in {"d"}:
                new_pron[-1] += p
                continue
            elif p in {"e", "i", "œ", "y"} and len(new_pron) and new_pron[-1] in {"k"}:
                new_pron[-1] = "c"
            elif p in {"e", "i", "œ", "y"} and len(new_pron) and new_pron[-1] in {"ɡ"}:
                new_pron[-1] = "ɟ"
            elif p in {"a", "ɯ", "o", "u"} and len(new_pron) and new_pron[-1] in {"l"}:
                new_pron[-1] = "ɫ"
            elif p in {"i", "e", "œ", "y"} and len(new_pron) and new_pron[-1] in {"ɫ"}:
                new_pron[-1] = "l"
        elif lang == "russian":
            voiced_set = {
                "v",
                "bʲ",
                "b",
                "bː",
                "d",
                "dz",
                "dzʲ",
                "dʐ",
                "dʲ",
                "dʲː",
                "dː",
                "v",
                "vʲ",
                "vʲː",
                "vː",
                "z",
                "zʲ",
                "zʲː",
                "zː",
                "ɡ",
                "ɡʲ",
                "ɡː",
                "ɣ",
                "ʐ",
                "ʐː",
                "ʑː",
            }
            if p in {"ʔ"}:
                continue

        elif lang == "japanese":
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
            if p in {".", "˕", "}", "˦˨˦", "˥", "˨˩", "˧", "꜔", "˩", "ʔ", "%", "˩˥"}:
                continue
            elif p in {
                "̥",
                "̥̥",
            } and len(new_pron):
                new_pron[-1] += "̥"
                continue
            elif p in {"ᵝ̥"} and len(new_pron):
                if "̥" not in new_pron[-1] and "ː" not in new_pron[-1]:
                    new_pron[-1] += "̥"
                continue
            elif p in {"ː̥"} and len(new_pron):
                new_pron[-1] += "ː"
                continue
            elif (
                p in {"j"}
                and len(new_pron)
                and new_pron[-1] in {"ɾ", "p", "m", "b", "k", "t", "d", "ç", "ɡ"}
            ):
                new_pron[-1] += "ʲ"
                continue
            elif p in {"h"} and len(new_pron) and new_pron[-1] in {"c"}:
                new_pron[-1] = "tɕ"
                continue
            elif p in {"p", "pʲ"} and len(new_pron) and new_pron[-1] in {"p̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"b"} and len(new_pron) and new_pron[-1] in {"b̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"ɾ", "ɾʲ"} and len(new_pron) and new_pron[-1] in {"ɾ̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"k", "kʲ"} and len(new_pron) and new_pron[-1] in {"k̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"t", "tʲ"} and len(new_pron) and new_pron[-1] in {"ʔ̥", "t̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"tɕ", "ts"} and len(new_pron) and new_pron[-1] in {"t̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"ɡ"} and len(new_pron) and new_pron[-1] in {"ɡ̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"d", "dz", "ʑ", "dʑ"} and len(new_pron) and new_pron[-1] in {"d̚"}:
                new_pron[-1] = p + "ː"
                continue
            elif p in {"i", "iː", "i̥"} and len(new_pron) and "ʲ" in new_pron[-1]:
                if len(new_pron) > 2 and "ʲ" in new_pron[-2]:
                    new_pron[-2] = new_pron[-2].replace("ʲ", "")

                new_pron[-1] = new_pron[-1].replace("ʲ", "")
            elif p in {"i"} and len(new_pron) and new_pron[-1] == "n":
                new_pron[-1] = "ɲ"
            elif False and p in {"k", "ɡ"} and len(new_pron) and new_pron[-1] == "ɲ":
                new_pron[-1] = "ŋ"
            elif False and p in {"t", "d"} and len(new_pron) and new_pron[-1] == "ɲ":
                new_pron[-1] = "n"
            elif p in {"dz", "dʑ"} and len(new_pron) and new_pron[-1] not in {"ɲ", "n"}:
                p = p[1]
            elif p in {
                "ɯ̟̃ᵝ",
                "ɯ̟̊ᵝ",
                "ɯ̟ᵝː",
                "ɯ̟ᵝ",
                "ɨ̥ᵝ",
                "ɨᵝ",
                "ɨ̃ᵝ",
                "ɨᵝː",
                "ɨ̥",
                "ɨ̥ː",
                "ɯ̥ː",
                "ɯ̥",
            }:
                if len(new_pron) and new_pron[-1] in {
                    "t",
                    "tː",
                    "s",
                    "sː",
                    "z",
                    "zː",
                    "ɲː",
                    "ɲ",
                    "ç",
                    "çː",
                    "n",
                    "nː",
                    "ts",
                    "tsː",
                    "ɕ",
                    "tɕ",
                    "tɕː",
                    "ʑ",
                    "ɕː",
                    "ʑː",
                    "ɡʲ",
                    "ɡʲː",
                    "kʲ",
                    "kʲː",
                    "bʲ",
                    "bʲː",
                    "pʲ",
                    "pʲː",
                    "mʲ",
                    "mʲː",
                    "ɾʲː",
                    "ɾʲ",
                    "j",
                }:
                    new_p = "ɨ"
                else:
                    new_p = "ɯ"
                if "̥" in p or "̊" in p:
                    new_p += "̥"
                if "ː" in p:
                    new_p += "ː"
                p = new_p
                if len(new_pron) and new_pron[-1] == "n":
                    new_pron[-1] = "ɲ"

        elif lang == "korean_hangul":
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
            # if p in {'e', 'ɛː', 'ɛ', 'a', 'o', 'u', 'ʌ'} and len(new_pron) and new_pron[-1] in {'j'}:
            #    new_pron[-1] += p
            #    continue
            # elif p in {'i'} and len(new_pron) and new_pron[-1] in {'w', 'ɥ'}:
            #    new_pron[-1] = 'ɥi'
            #    continue
            # elif p in {'e', 'ɛː', 'ɛ', 'a', 'o', 'i', 'ʌ'} and len(new_pron) and new_pron[-1] in {'w'}:
            #    new_pron[-1] += p
            #    continue
            # elif p in {'i'} and len(new_pron) and new_pron[-1] in {'ɰ'}:
            #    new_pron[-1] += p
            #    continue
            if p == "t͈" and "ᄄ" not in jamo.h2j(word):
                if len(new_pron) and "̚" in new_pron[-1]:
                    p = "tʰ"
                else:
                    p = "t"
            elif p == "tɕ͈" and "ᄍ" not in jamo.h2j(word):
                if len(new_pron) and "̚" in new_pron[-1]:
                    p = "tɕʰ"
                else:
                    p = "tɕ"
            elif p == "k͈" and "ᄁ" not in jamo.h2j(word):
                if len(new_pron) and "̚" in new_pron[-1]:
                    p = "kʰ"
                else:
                    p = "k"
            elif p == "p͈" and "ᄈ" not in jamo.h2j(word):
                if len(new_pron) and "̚" in new_pron[-1]:
                    p = "pʰ"
                else:
                    p = "p"
            elif p == "s͈" and "ᄊ" not in jamo.h2j(word):
                if len(new_pron) and "̚" in new_pron[-1]:
                    p = "sʰ"
                else:
                    p = "s"
            elif p == "x" and len(new_pron) and new_pron[-1] == "k":
                new_pron[-1] += "ʰ"
                continue

        elif lang in ["vietnamese_hanoi", "vietnamese_hue", "vietnamese_hochiminhcity"]:
            vowel_pattern = re.compile(rf'^[{"".join(VOWELS[lang])}]+$')
            tone_pattern = re.compile(r"^[˥˩˦˥˨˧˨˩˩˩ˀ˦]+$")
            if p in {"j", "w"} and len(new_pron) and vowel_pattern.match(new_pron[-1]):
                new_pron[-1] += p
                continue
            elif vowel_pattern.match(p) and len(new_pron) and vowel_pattern.match(new_pron[-1]):
                new_pron[-1] += p
                continue
            elif p in {"ɗ", "ɓ"} and len(new_pron) and new_pron[-1] == "ʔ":
                new_pron[-1] = p
                continue
            elif (
                p == "ʔ"
                and len(new_pron)
                and tone_pattern.match(new_pron[-1])
                and not (i < len(phones) - 1 and phones[i + 1] in {"ɗ", "ɓ"})
            ):
                new_pron[-1] += "ˀ"
                continue
        if lang in LANG_MAPPING:
            for k, v in LANG_MAPPING[lang].items():
                if p == k:
                    p = v
                    break
        if not p:
            continue
        new_pron.append(p)
    tone_mapping = {
        "⁰": "",
        "¹": "˩",
        "²": "˨",
        "³": "˧",
        "⁴": "˦",
        "⁵": "˥",
        "˧": "˧",
        "˨˩": "˨˩",
        "˥˩": "˥˩",
        "˦˥": "˦˥",
        "˩˩˦": "˩˩˦",
    }
    if lang == "thai":
        phones = new_pron
        new_pron = []
        tone_symbols = {"˥˩", "˦˥", "˧", "˨˩", "˩˩˦"}
        vowel_set = {x for x in VOWELS[lang]}
        vowel_set |= {x + y for x, y in itertools.product(VOWELS[lang], VOWELS[lang])}
        vowel_set |= {
            x + y + z for x, y, z in itertools.product(VOWELS[lang], VOWELS[lang], VOWELS[lang])
        }
        for i, p in enumerate(phones):
            if p in tone_symbols:
                for j in range(len(new_pron) - 1, 0, -1):
                    if new_pron[j] in vowel_set and new_pron[j] not in {"w", "j"}:
                        new_pron[j] += tone_mapping[p]
                        break
            else:
                new_pron.append(p)
        # split off tone for G2P
        # for i, p in enumerate(new_pron):
        #    for tone in tone_mapping:
        #        if p.endswith(tone):
        #            new_pron[i] = p.replace(tone, ' ') + tone

    elif lang in ["vietnamese_hanoi", "vietnamese_hue", "vietnamese_hochiminhcity"]:
        phones = new_pron
        new_pron = []
        vowel_pattern = re.compile(rf'^[{"".join(VOWELS[lang])}]+[wj]?$')
        tone_symbols = {
            "˦ˀ˥",
            "˧˦",
            "˧˧",
            "˧˨",
            "˧˩",
            "˨˩",
            "˦˧˥",
            "˦˩",
            "˧˧",
            "˧˨",
            "˨˩",
            "˨˩˦",
            "˦˥",
            "˨˩˨",
        }
        tone_pattern = re.compile(r"^[˥˩˦˥˨˧˨˩˩˩ˀ˦]+$")
        for i, p in enumerate(phones):
            if tone_pattern.match(p):
                for j in range(len(new_pron) - 1, 0, -1):
                    if vowel_pattern.match(new_pron[j]):
                        new_pron[j] += p
                        break
            else:
                new_pron.append(p)
    elif lang.startswith("mandarin_hani"):
        mapping = {
            "²¹⁴": "˨˩˦",
            "⁵⁵": "˥˥",
            "³⁵": "˧˥",
            "⁵¹": "˥˩",
            "⁰": "",
            "¹": "˩",
            "²": "˨",
            "³": "˨",
            "⁴": "˦",
            "⁵": "˥",
        }
        tone_symbols = {"²", "³", "¹", "⁴", "⁵", "⁰"}
        for i, p in enumerate(new_pron):
            if any(x in p for x in tone_symbols):
                for k, v in mapping.items():
                    if k in new_pron[i]:
                        new_pron[i] = new_pron[i].replace(k, v)
            # if any(x in new_pron[i] for x in tone_symbols):
            #    return None
    elif lang == "swedish":
        for i, p in enumerate(new_pron):
            if p == "êː":
                new_pron[i] = "eː˧˩"
            elif p == "â":
                new_pron[i] = "a˧˩"
            elif p == "ɛ̂":
                new_pron[i] = "ɛ˧˩"
            elif p == "ɑ̂ː":
                new_pron[i] = "ɑː˧˩"
            elif p == "ûː":
                new_pron[i] = "uː˧˩"
            elif p == "ʉ̂ː":
                new_pron[i] = "ʉː˧˩"
            elif p == "ɵ̂":
                new_pron[i] = "ɵ˧˩"
            elif p == "ʉ̂ː":
                new_pron[i] = "ʉː˧˩"
            elif p == "ʉ̟ː˥˩":
                new_pron[i] = "ʉː˥˩"
            elif p == "ǎ":
                new_pron[i] = "a˥˧"
            elif p == "ʉ̟ː˧˩":
                new_pron[i] = "ʉː˧˩"
            elif p == "ø̀ː":
                new_pron[i] = "øː˩"
            elif p == "ɑ̀ː":
                new_pron[i] = "ɑː˩"
            elif p == "ỳː":
                new_pron[i] = "yː˩"
            elif p == "ỳː˧˩":
                new_pron[i] = "yː˧˩"

    elif lang == "hausa":
        phone_mapping = {
            "á": "a",
            "áː": "aː",
            "é": "e",
            "éː": "eː",
            "í": "i",
            "íː": "iː",
            "ó": "o",
            "óː": "oː",
            "úː": "uː",
            "à": "a",
            "àː": "aː",
            "è": "e",
            "èː": "eː",
            "ì": "i",
            "ìː": "iː",
            "ò": "o",
            "òː": "oː",
            "ùː": "uː",
            "â": "a",
            "âː": "aː",
            "ê": "e",
            "êː": "eː",
            "î": "i",
            "îː": "iː",
            "ô": "o",
            "ôː": "oː",
            "ûː": "uː",
        }
        for i, p in enumerate(new_pron):
            if p in {"á", "áː", "é", "éː", "í", "íː", "ó", "óː", "úː"} or "́" in p:  # High tone
                if p in phone_mapping:
                    new_pron[i] = phone_mapping[p]
                else:
                    new_pron[i] = p.replace("́", "")
                new_pron[i] += "˥"
            elif p in {"à", "àː", "è", "èː", "ì", "ìː", "ò", "òː", "ùː"} or "̀" in p:  # Low tone
                if p in phone_mapping:
                    new_pron[i] = phone_mapping[p]
                else:
                    new_pron[i] = p.replace("̀", "")
                new_pron[i] += "˩"
            elif (
                p
                in {
                    "â",
                    "âː",
                    "ê",
                    "êː",
                    "î",
                    "îː",
                    "ôː",
                    "ûː",
                }
                or "̂" in p
            ):  # Falling tone
                if p in phone_mapping:
                    new_pron[i] = phone_mapping[p]
                else:
                    new_pron[i] = p.replace("̂", "")
                new_pron[i] += "˥˦"

    return new_pron


def convert_second_round(word, phones, lang):
    if lang not in ["english_us", "english_uk"]:
        return phones
    new_pron = []
    stressed_vowels = {}
    if lang == "english_uk":
        stressed_vowels = {
            "aɪ",
            "aʊ",
            "eɪ",
            "i",
            "iː",
            "oɪ",
            "oʊ",
            "u",
            "uː",
            "æ",
            "ɑ",
            "ɑː",
            "ɒ",
            "ɔ",
            "ɔɪ",
            "ɔː",
            "ɛ",
            "ɛː",
            "ɜ",
            "ɜː",
            "ʊ",
            "ʌ",
        }
    elif lang == "english_us":
        stressed_vowels = {
            "aɪ",
            "aʊ",
            "eɪ",
            "i",
            "iː",
            "oɪ",
            "oʊ",
            "u",
            "uː",
            "æ",
            "ɑ",
            "ɑː",
            "ɔ",
            "ɔɪ",
            "ɔː",
            "ɛ",
            "ɝ",
            "ɝː",
            "ʊ",
            "ʌ",
        }
    all_syllabics = {"ɪ", "ə", "ɚ", "n̩", "m̩", "l̩", "ɫ̩"} | VOWELS[lang]
    for i, p in enumerate(phones):
        if lang in ["english_us", "english_uk"]:
            if (
                p == "l"
                and 2 < i < len(phones) - 1
                and new_pron[-1] == "ə"
                and phones[i + 1] not in all_syllabics
            ):
                new_pron[-1] = "ɫ̩"
                continue
            elif (
                p == "m"
                and 2 < i < len(phones) - 1
                and new_pron[-1] == "ə"
                and phones[i + 1] not in all_syllabics
            ):
                new_pron[-1] = "m̩"
                continue
            elif (
                p == "n"
                and 2 < i < len(phones) - 1
                and new_pron[-1] == "ə"
                and phones[i + 1] not in all_syllabics
            ):
                new_pron[-1] = "n̩"
                continue
            elif p == "l̩" and 1 < i < len(phones) - 1 and phones[i + 1] in all_syllabics:
                new_pron.append("ə")
                p = "l"
            elif p == "l̩":
                p = "ɫ̩"
            elif p == "l" and i == len(phones) - 1:
                p = "ɫ"
            elif p == "l" and 1 < i < len(phones) - 1 and phones[i + 1] not in all_syllabics:
                p = "ɫ"
            elif (
                p in {"t", "p", "k"}
                and i == 0
                and i < len(phones) - 1
                and phones[i + 1] in stressed_vowels | {"ɪ", "ə", "ɚ"}
            ):
                p += "ʰ"
            elif (
                p == "ə"
                and 1 < i == len(phones) - 2
                and phones[i - 1] in {"d", "t"}
                and phones[i + 1] == "d"
            ):
                p = "ɪ"
            elif (
                p == "ə"
                and 1 < i == len(phones) - 2
                and phones[i - 1] in {"s", "z", "ʃ", "ʒ", "tʃ", "dʒ"}
                and phones[i + 1] == "z"
            ):
                p = "ɪ"
        if lang == "english_us":
            if (
                p == "ɹ"
                and 2 < i < len(phones) - 1
                and new_pron[-1] == "ə"
                and phones[i + 1] not in all_syllabics
            ):
                new_pron[-1] = "ɚ"
                continue
            elif (
                p in {"d", "t"}
                and 1 < i < len(phones) - 1
                and phones[i - 1] in all_syllabics
                and phones[i + 1] in {"n̩", "m̩", "l̩", "ɚ", "ə", "ɫ̩"}
            ):
                p = "ɾ"
            elif (
                p in {"t", "d"}
                and 1 < i < len(phones) - 2
                and phones[i - 1] in all_syllabics
                and phones[i + 1] == "ɪ"
                and phones[i + 2] == "d"
            ):
                p = "ɾ"
            elif (
                p in {"t", "d"}
                and i > 1
                and i == len(phones) - 2
                and phones[i - 1] in all_syllabics
                and phones[i + 1] == "i"
            ):
                p = "ɾ"
            elif (
                p in {"t", "d"}
                and i > 1
                and i == len(phones) - 3
                and phones[i - 1] in all_syllabics
                and phones[i + 1] in {"i", "ɪ"}
                and phones[i + 2] == "z"
            ):
                p = "ɾ"
            elif (
                p in {"t", "d"}
                and i > 1
                and i == len(phones) - 3
                and phones[i - 1] in all_syllabics
                and phones[i + 1] == "ɪ"
                and phones[i + 2] == "ŋ"
            ):
                p = "ɾ"
            elif (
                p in {"t", "p", "k"}
                and i == 0
                and i < len(phones) - 1
                and phones[i + 1] in stressed_vowels | {"ɪ", "ə", "ɚ"}
            ):
                p += "ʰ"
            elif (
                p in {"t", "p", "k"}
                and i > 0
                and phones[i - 1] not in {"s", "ʃ"}
                and i < len(phones) - 1
                and phones[i + 1] in stressed_vowels
            ):
                p += "ʰ"
            elif p == "l̩" and 1 < i < len(phones) - 1 and phones[i + 1] in all_syllabics:
                new_pron.append("ə")
                p = "l"
            elif p == "l̩":
                p = "ɫ̩"
            elif p == "l" and i == len(phones) - 1:
                p = "ɫ"
            elif (
                p == "l"
                and 1 < i < len(phones) - 1
                and phones[i + 1] not in {"ɪ", "ə", "ɚ", "n̩", "m̩", "l̩", "ɫ̩"} | VOWELS[lang]
            ):
                p = "ɫ"
            elif (
                p == "ə"
                and 1 < i == len(phones) - 2
                and phones[i - 1] in {"d", "t", "ɾ"}
                and phones[i + 1] == "d"
            ):
                p = "ɪ"
            elif (
                p == "ə"
                and 1 < i == len(phones) - 2
                and phones[i - 1] in {"s", "z", "ʃ", "ʒ", "tʃ", "dʒ"}
                and phones[i + 1] == "z"
            ):
                p = "ɪ"
            elif (
                p in {"t", "p", "k"}
                and i > 0
                and phones[i - 1] not in {"s", "ʃ"}
                and i < len(phones) - 1
                and phones[i + 1] in stressed_vowels
            ):
                p += "ʰ"
        elif lang == "english_uk":
            if p not in VOWELS[lang] and len(new_pron) and new_pron[-1] == "ɹ":
                new_pron[-1] = p
                continue
            elif (
                p in {"t", "p", "k"}
                and i > 0
                and phones[i - 1] not in {"s", "ʃ"}
                and i < len(phones) - 1
                and phones[i + 1] in stressed_vowels
            ):
                p += "ʰ"
        elif lang == "portuguese_brazil":
            if p == "i" and new_pron and new_pron[-1] == "d":
                new_pron[-1] = "dʒ"
            elif p == "i" and new_pron and new_pron[-1] == "t":
                new_pron[-1] = "tʃ"
            elif p == "i" and new_pron and new_pron[-1] == "l":
                new_pron[-1] = "ʎ"
        new_pron.append(p)
    return new_pron


def fix_pronunciations(dictionary, lang):
    filtered_dictionary = []
    for word, pronunciation in dictionary:
        if lang == "polish":
            if "ü" in word:
                continue
        for i, p in enumerate(pronunciation):
            if p in LANG_MAPPING[lang]:
                continue
            if p in GLOBAL_REMAPPING:
                pronunciation[i] = GLOBAL_REMAPPING[p]
            elif "̯" in p:
                pronunciation[i] = p.replace("̯", "")
            elif "͡" in p:
                pronunciation[i] = p.replace("͡", "")
            elif "‿" in p:
                pronunciation[i] = p.replace("‿", "")
            elif "͜" in p:
                pronunciation[i] = p.replace("͜", "")
            elif "g" in p:
                pronunciation[i] = p.replace("g", "ɡ")
        pronunciation = [x for x in pronunciation if x not in {"‿", ""}]
        if lang in BAD_PHONES and any(x in BAD_PHONES[lang] for x in pronunciation):
            continue
        # Language specific conversions
        new_pron = convert_language_specific(word, pronunciation, lang)
        new_pron = convert_second_round(word, new_pron, lang)
        if new_pron is None:
            continue
        if (word, new_pron) not in filtered_dictionary:
            filtered_dictionary.append((word, new_pron))
    return filtered_dictionary


def process_language(lang):
    print("Processing", lang)
    if lang == "japanese":
        dictionary, input_graphemes, input_phones = read_source(lang + "_hiragana")
        d, g, p = read_source(lang + "_katakana")
        dictionary.extend(d)
        input_graphemes.update(g)
        input_phones.update(p)
        word_set = {x[0] for x in dictionary}
        d, g, p = read_source(lang)
        dictionary.extend([x for x in d if x[0] not in word_set])
        input_graphemes.update(g)
        input_phones.update(p)

    else:
        dictionary, input_graphemes, input_phones = read_source(lang)

    print("Input graphemes", sorted(input_graphemes))
    print("Input phones", sorted(input_phones))
    filtered = fix_pronunciations(dictionary, lang)
    save_dictionary(filtered, lang)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for code in LANG_CODES:
        process_language(code)

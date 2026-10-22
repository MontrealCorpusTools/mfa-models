import collections
import dataclasses
import itertools
import os
import pathlib
import re
import typing
import unicodedata

import jsonlines
import segments

try:
    import jamo
except ImportError:
    jamo = None

REMOVE_STRESS = True


@dataclasses.dataclass
class Word:
    word: str
    enpr: str
    pronunciations: typing.List[typing.Tuple[str, str]]
    part_of_speech: str
    etymology: str
    alternate_forms: str
    derived_forms: str

    def to_json(self):
        return {
            "word": self.word,
            "enpr": self.enpr,
            "pronunciations": self.pronunciations,
            "part_of_speech": self.part_of_speech,
            "etymology": self.etymology,
            "alternate_forms": self.alternate_forms,
            "derived_forms": self.derived_forms,
        }


ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
SCRAPE_DIR = ROOT_DIR.joinpath("dictionary", "training", "scraped")
OUTPUT_DIR = ROOT_DIR.joinpath("dictionary", "training", "cleaned")

parenthetical_regex = re.compile(r"^\((.*)\)")

UNPARSED_DIALECTS = set()

LANGUAGES = [
    "English",
]

DIALECTS = {
    "English": {
        "General American": "us",
        "US": "us",
        "Received Pronunciation": "uk",
        "Standard Southern British": "uk",
        "RP": "uk",
        "UK": "uk",
        "England": "uk",
        "Scotland": "scotland",
        "Scottish": "scotland",
        "Irish": "ireland",
        "Ireland": "ireland",
        "General South African": "south_africa",
        "AU": "australian",
        "Australian": "australian",
        "Australia": "australian",
        "India": "india",
        "South Asia": "india",
        "New Zealand": "nz",
    }
}

FEATURES_TO_DIALECT = {
    "without the wine–whine merger": {"scotland", "ireland"},
    "rhotic": {"us", "india", "scotland", "ireland"},
    "non-rhotic": {"uk", "australian", "nz", "south_africa"},
    "wine–whine merger": {"us", "india", "uk", "australian", "nz", "south_africa"},
    "without the horse–hoarse merger": {"scotland"},
    "horse–hoarse merger": {"us", "india", "uk", "australian", "nz", "south_africa", "ireland"},
}

DIALECT_TAGS = {
    "ireland": {"without the wine–whine merger", "rhotic"},
    "scotland": {"without the wine–whine merger", "rhotic", "without the horse–hoarse merger"},
    "us": {"wine–whine merger", "rhotic"},
    "uk": {"wine–whine merger", "non-rhotic"},
    "australian": {"wine–whine merger", "non-rhotic"},
    "nz": {"wine–whine merger", "non-rhotic"},
    "south_africa": {"wine–whine merger", "non-rhotic"},
    "india": {"wine–whine merger", "rhotic"},
}

BAD_GRAPHEMES = {
    "English": {
        "%",
        "&",
        "い",
        "な",
        "🍇",
        "🦴",
        "🧢",
        "∂",
        "ы",
        "ж",
        "σ",
        "б",
        "ת",
        "λ",
        "ʟ",
        "ה",
        "þ",
        "ð",
        "Ð",
        "Æ",
        "Å",
        "Ø",
        "Ü",
        "ǃ",
        "ʕ",
        "å",
        "̃",
        "ǀ",
        "ǁ",
        "ƹ",
        "Þ",
        "ʔ",
        "/",
        "+",
        "!",
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
}

BAD_PHONES = {
    "English": {
        "b̥",
        "a̯",
        "bᵊ",
        "dːʰ",
        "d̠͡ɹ̠",
        "eːː",
        "f͡s",
        "j̥",
        "kʲ",
        "k͜ǃ",
        "lʲ",
        "lː",
        "l̠ʲ",
        "l͡s",
        "mʲ",
        "nʲ",
        "n̻",
        "o̙",
        "o̯'",
        "pʲ",
        "p͡fː",
        "rː",
        "sʰ",
        "sʲ",
        "sˠ",
        "tʲ",
        "tˀ",
        "t̪ˠ",
        "t̪͆",
        "t͡sʲ",
        "t͡ɕ",
        "t͡ɕʰ",
        "u̯",
        "w̥",
        "x",
        "y",
        "~",
        "ã",
        "æ̃",
        "ç",
        "ü",
        "ēː",
        "ĕ",
    }
}

DIALECT_BAD_PHONES = {
    "English": {
        "uk": {"ɪː", "aː", "eː", "a", "o", "oː", "eː", "e"},
        "us": {"ɒ", "aː", "a", "o", "oː", "eː", "e", "ɪː", "ɛː"},
    }
}


VOWELS = {
    "us": {
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
    "uk": {
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
}


MAPPING = {
    "d̪": "ð",
    "m̩ː": "m̩",
    "nː": "n",
    "p̪": "p",
    "sː": "s",
    "zː": "z",
    "t̪": "t",
    "t̪ʰ": "t",
    "t͡s": "t s",
    "t͡ʃʰ": "t͡ʃ",
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
    # Skips initialisms
    if word.isupper() and len(word) > 1:
        return True
    # Skips examples containing digits.
    if re.search(r"\d", word):
        return True
    return False


def _process_dialects(lang, dialect):
    if not dialect:
        return [""]
    dialects = set()

    possible_dialects = re.split(r"[,(]", dialect)
    for d in possible_dialects:
        d = d.replace("(", "").strip()
        if not d:
            continue
        if d in DIALECTS[lang]:
            dialects.add(DIALECTS[lang][d])
        elif "without the wine–whine merger" in d:
            dialects.update(["scotland", "ireland"])
        elif "enPR" in d:
            continue
        else:
            UNPARSED_DIALECTS.add(d)
    return sorted(dialects)


def _split_pronunciations(pronunciation):
    if ";" in pronunciation:
        possible_pronunciations = pronunciation.split(";")
    else:
        possible_pronunciations = pronunciation.split(",")
    pronunciations = []
    for p in possible_pronunciations:
        if "/" not in p:
            continue
        prons = re.findall(r"/(.+?)/", p)
        if not prons:
            continue
        for pron in prons:
            if pron.startswith("-") or pron.endswith("-"):
                continue
            if "," in pron:
                pron = pron.split(",")[0].strip()
            pronunciations.append(pron)
    return pronunciations


def _process_wiki_pron(phones):
    tokenizer = segments.Tokenizer()
    phones = unicodedata.normalize("NFD", phones)
    if REMOVE_STRESS:
        phones = re.sub(r"[ˈˌ.#]", "", phones)
    # phones = re.sub(r"[-ˈˌ.()#]", "", phones)
    phones = tokenizer(phones, ipa=True).split()
    new_phones = []
    for p in phones:
        new_phones.append(p)
    new_pron = " ".join(new_phones)
    new_pron = unicodedata.normalize("NFC", new_pron)
    # new_pron = re.sub(r"[-ˈˌ.()#]", "", new_pron)
    new_pron = re.sub(r"([ˈˌ])", r"\1 ", new_pron)
    new_pron = re.sub(r"\( (.*?) \)", r"(\1)", new_pron)
    return new_pron.split()


def _read_source(lang):
    path = os.path.join(SCRAPE_DIR, f"{lang}.jsonl")
    with open(path, "r", encoding="utf8") as f:
        reader = jsonlines.Reader(f)
        for line in reader:
            word = Word(**line)
            if _skip_word(word.word, lang):
                continue
            for dialect, pronunciation in word.pronunciations:
                if dialect is None:
                    dialect = ""
                pronunciations = _split_pronunciations(pronunciation)
                for p in pronunciations:
                    if p:
                        yield word, dialect, p


def read_source(lang):
    graphemes = {}
    phones = {}
    dictionary = {}

    path = os.path.join(SCRAPE_DIR, f"{lang}_formatted.tsv")
    enpr_count = 0
    with open(path, "w", encoding="utf8") as f:
        for word, dialect, pronunciation in _read_source(lang):
            if "weak vowel merger" in dialect:
                continue
            if word.enpr:
                enpr_count += 1
            dialects = _process_dialects(lang, dialect)
            if "phoneme" in dialects:
                continue
            if all(d not in {"us"} for d in dialects):
                continue
            f.write(f"{word.word}\t{dialect}\t{word.enpr}\t{pronunciation}\n")
            for d in dialects:
                if d not in {"us"}:
                    continue
                if d not in dictionary:
                    dictionary[d] = {}
                    phones[d] = set()
                    graphemes[d] = set()
            p = _process_wiki_pron(pronunciation)
            if any(x in BAD_PHONES[lang] for x in p):
                print("skipping:", word.word, dialects, " ".join(p))
                continue
            for d in dialects:
                if d not in {"us"}:
                    continue
                graphemes[d].update(word.word)
                phones[d].update(p)
                if word.word not in dictionary[d]:
                    dictionary[d][word.word] = []
                dictionary[d][word.word].append(p)
    print("enPR count:", enpr_count)
    return dictionary, graphemes, phones


def save_dictionary(dictionary, language, dialect):
    deduplication = set()
    final_phones = collections.Counter()
    path = os.path.join(OUTPUT_DIR, f"{language.lower()}_{dialect}_mfa.dict")
    with open(path, "w", encoding="utf8") as f:
        for w in sorted(dictionary.keys()):
            for p in dictionary[w]:
                final_phones.update(p)
                p = " ".join(p)
                if (w, p) in deduplication:
                    continue
                f.write("{}\t{}\n".format(w, p))
                deduplication.add((w, p))
    print("Final phones:", sorted(final_phones))
    print("Final phone counts:", sorted(final_phones.items(), key=lambda x: -x[1]))


def fix_pronunciations(dictionary):
    filtered_dictionary = {}
    for word, pronunciations in dictionary.items():
        for pronunciation in pronunciations:
            for i, p in enumerate(pronunciation):
                if p in MAPPING:
                    continue
                if p in GLOBAL_REMAPPING:
                    pronunciation[i] = GLOBAL_REMAPPING[p]
                elif "̯" in p:
                    pronunciation[i] = p.replace("̯", "")
                elif "͡" in p:
                    pronunciation[i] = p.replace("͡", "")
                elif "‿" in p:
                    pronunciation[i] = p.replace("‿", "")
                # elif "͜" in p:
                #    pronunciation[i] = p.replace("͜", "")
                elif "g" in p:
                    pronunciation[i] = p.replace("g", "ɡ")
            new_pron = [x for x in pronunciation if x not in {"‿", ""}]
            if lang in BAD_PHONES and any(x in BAD_PHONES[lang] for x in pronunciation):
                continue
            # Language specific conversions
            if new_pron is None:
                continue
            if word not in filtered_dictionary:
                filtered_dictionary[word] = []
            if new_pron not in filtered_dictionary[word]:
                filtered_dictionary[word].append(new_pron)
    return filtered_dictionary


def process_language(lang):
    print("Processing", lang)
    dictionary, input_graphemes, input_phones = read_source(lang)

    for dialect in dictionary.keys():
        print(f"{dialect}: {len(dictionary[dialect])} pronunciations")
        print("Input graphemes", sorted(input_graphemes[dialect]))
        print("Input phones", sorted(input_phones[dialect]))

    for dialect in dictionary.keys():
        if dialect not in {"us"}:
            continue
        filtered = fix_pronunciations(dictionary[dialect])
        save_dictionary(filtered, lang, dialect)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for lang in LANGUAGES:
        process_language(lang)

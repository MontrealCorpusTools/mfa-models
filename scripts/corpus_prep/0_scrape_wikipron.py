import csv
import dataclasses
import functools
import json
import pathlib
import re
import time
import typing

import jsonlines
import requests
import requests_html

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT_DIR.joinpath("dictionary", "training", "scraped")

LANGUAGES = [
    # "French",
    # "German",
    # "Italian",
    # "Dutch",
    # "Danish",
    # "Hungarian",
    # "Bulgarian",
    # "Thai",
    # "Korean",
    "English",
    "Emilian",
]

# LANGAUGE = 'Portuguese'

_CATEGORY_TEMPLATE = "Category:{language} terms with IPA pronunciation"
# Http headers for api call
HTTP_HEADERS = {
    "User-Agent": (
        f"Montreal-Forced-Aligner/3.3.0"
        "(https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) "
        f"requests/{requests.__version__}"
    ),
}
_PAGE_TEMPLATE = "https://en.wiktionary.org/wiki/{word}"
_PRON_XPATH_SELECTOR_TEMPLATE = """
(//li|//p)[
  (.|span)[sup[a[
    @title = "Appendix:{language} pronunciation"
    or
    @title = "wikipedia:{language} phonology"
  ]]]
  and
  span[contains(@class, "IPA")]
]
"""

IPA_XPATH_SELECTOR = 'li/ul/li[span[contains(@class, "IPA")]]|li[span[contains(@class, "IPA")]]'
enPR_XPATH_SELECTOR = 'span[contains(@class, "enPR")]|li/ul/li/span[contains(@class, "enPR")]|li/span[contains(@class, "enPR")]'

_PHONEMES_REGEX = [r"/(.+?)/", r"\[(.+?)\]"]

POS_SECTIONS = {
    "Verb",
    "Adjective",
    "Proper noun",
    "Adnominal",
    "Preposition",
    "Noun",
    "Pronoun",
    "Adverb",
    "Interjection",
    "Particle",
    "Numeral",
    "Counter",
    "Conjunction",
    "Determiner",
    "Postposition",
    "Letter",
}
MORPHOLOGICAL_SECTIONS = {"Suffix", "Prefix", "Clitic"}


@dataclasses.dataclass
class Word:
    word: str
    enpr: str
    pronunciations: typing.List[typing.Tuple[str, str, str]]
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


def _skip_word(word: str, skip_spaces: bool) -> bool:
    # Skips reconstructions.
    if word.startswith("*"):
        return True
    # Skips multiword examples.
    if skip_spaces and (" " in word or "\u00A0" in word):
        return True
    # Skips examples containing a dash.
    # if "-" in word:
    #     return True
    # Skips examples containing digits.
    # if re.search(r"\d", word):
    #     return True
    return False


def _get_subtag_text(element, tags):
    if not isinstance(tags, list):
        tags = [tags]
    for tag in tags:
        subtag = element.find(tag)
        if subtag is not None:
            return subtag.text
    return ""


def parse_page_type(elements):
    single_etymology = True
    single_pronunciation = True
    for element in elements:
        if _get_subtag_text(element, "h3") == "Etymology 1":
            single_etymology = False
        if not single_etymology:
            if _get_subtag_text(element, "h4") == "Pronunciation":
                single_pronunciation = False
    return single_etymology, single_pronunciation


def _parse_pronunciation_ul(element):
    pronunciations = []
    enpr_pronunciation = ""
    enpr_elements = element.xpath(enPR_XPATH_SELECTOR)
    for e in enpr_elements:
        enpr_pronunciation = e.text_content()
        break
    pron_elements = element.xpath(IPA_XPATH_SELECTOR)
    for li in pron_elements:
        overall_usage_string = None
        possible_parent = li.getparent().getparent()
        if possible_parent.tag == "li":
            try:
                overall_usage_string = possible_parent.xpath(
                    "span[contains(@class, 'qualifier-content')]"
                )[0].text_content()
            except (AttributeError, IndexError):
                pass
        usage_string = None
        li_usage_string = None
        pronunciation_usage_strings = {}
        parsing_ipa = False
        li_pronunciations = []
        for lie in li.iterchildren():
            if (
                not parsing_ipa
                and lie.tag == "span"
                and "qualifier-content" in lie.attrib["class"].split()
            ):
                if overall_usage_string is None:
                    li_usage_string = lie.text_content()
                else:
                    li_usage_string = f"{overall_usage_string}, {lie.text_content()}"
            if (
                lie.tag == "span"
                and "enPR" in lie.attrib["class"].split()
                and not enpr_pronunciation
            ):
                enpr_pronunciation = lie.text_content()
            if parsing_ipa and lie.tag == "span" and "IPA" in lie.attrib["class"].split():
                pronunciation = lie.text_content()
                if usage_string is not None:
                    pronunciation_usage_strings[pronunciation] = usage_string
                li_pronunciations.append(pronunciation)
                usage_string = None
            if (
                parsing_ipa
                and lie.tag == "span"
                and "qualifier-content" in lie.attrib["class"].split()
            ):
                usage_string = lie.text_content()
            if lie.tag == "a" and lie.text_content() == "IPA":
                parsing_ipa = True

        if usage_string is not None:
            if li_usage_string is None:
                if overall_usage_string is None:
                    li_usage_string = usage_string
                else:
                    li_usage_string = f"{overall_usage_string}, {usage_string}"
            else:
                li_usage_string = f"{li_usage_string}, {usage_string}"
        for pronunciation in li_pronunciations:
            usage_string = li_usage_string
            if pronunciation in pronunciation_usage_strings:
                if usage_string is None:
                    usage_string = pronunciation_usage_strings[pronunciation]
                else:
                    usage_string = f"{usage_string}, {pronunciation_usage_strings[pronunciation]}"
            pronunciations.append((usage_string, pronunciation))
    return enpr_pronunciation, pronunciations


def parse_section(word, elements, single_etymology, single_pronunciation) -> typing.List[Word]:
    words = []
    pronunciations = []
    enpr = ""
    if single_pronunciation:
        parsing = False
        for e in elements:
            if _get_subtag_text(e, "h3") == "Pronunciation":
                parsing = True
                continue
            if parsing and _get_subtag_text(e, "h3"):
                break
            if not parsing:
                continue
            if e.tag != "ul":
                continue
            enpr, prons = _parse_pronunciation_ul(e)
            pronunciations.extend(prons)

    current_etymology = None
    etymology = ""
    alternate_forms = ""
    derived_forms = ""
    part_of_speech = ""
    current_section = None
    if single_etymology:
        etymology = ""
        for e in elements:
            if _get_subtag_text(e, "h3") in POS_SECTIONS | MORPHOLOGICAL_SECTIONS:
                if part_of_speech and _get_subtag_text(e, "h3") != part_of_speech:
                    words.append(
                        Word(
                            word,
                            enpr,
                            pronunciations,
                            part_of_speech,
                            etymology,
                            alternate_forms,
                            derived_forms,
                        )
                    )
                current_section = _get_subtag_text(e, "h3")
                part_of_speech = current_section
                continue
            if _get_subtag_text(e, "h3"):
                current_section = _get_subtag_text(e, "h3")
                continue
            if current_section == "Etymology":
                if e.tag != "p":
                    continue
                etymology += e.text_content()
            elif current_section == "Alternative forms":
                alternate_forms = e.text_content()
            elif current_section in POS_SECTIONS | MORPHOLOGICAL_SECTIONS:
                if _get_subtag_text(e, ["h3", "h4", "h5"]):
                    break
                if e.tag != "p":
                    continue
                try:
                    headword_line = e.xpath("span[contains(@class, 'headword-line')]")[0]
                except IndexError:
                    continue
                derived = headword_line.xpath("*[contains(@class, 'form-of')]")
                derived_forms = ", ".join(
                    [x.text_content() for x in derived if x.text_content() != "word"]
                )

        words.append(
            Word(
                word,
                enpr,
                pronunciations,
                part_of_speech,
                etymology,
                alternate_forms,
                derived_forms,
            )
        )
    else:
        for e in elements:
            if e.tag == "link":
                try:
                    e = list(e.iterchildren())[0]
                except IndexError:
                    pass
            if _get_subtag_text(e, "h3").startswith("Etymology"):
                if (
                    current_etymology is not None
                    and _get_subtag_text(e, "h3") != current_etymology
                ):
                    if pronunciations:
                        words.append(
                            Word(
                                word,
                                enpr,
                                pronunciations,
                                part_of_speech,
                                etymology,
                                alternate_forms,
                                derived_forms,
                            )
                        )
                current_etymology = _get_subtag_text(e, "h3")
                part_of_speech = ""
                etymology = ""
                current_section = "Etymology"
                if not single_pronunciation:
                    pronunciations = []
                continue
            elif _get_subtag_text(e, "h4") in POS_SECTIONS | MORPHOLOGICAL_SECTIONS:
                if part_of_speech and _get_subtag_text(e, "h4") != part_of_speech:
                    if pronunciations:
                        words.append(
                            Word(
                                word,
                                enpr,
                                pronunciations,
                                part_of_speech,
                                etymology,
                                alternate_forms,
                                derived_forms,
                            )
                        )
                current_section = _get_subtag_text(e, "h4")
                part_of_speech = current_section
                continue
            elif _get_subtag_text(e, "h4"):
                current_section = _get_subtag_text(e, "h4")
                continue

            if current_section == "Etymology":
                if e.tag != "p":
                    continue
                etymology += e.text_content()
            elif current_section == "Alternative forms":
                alternate_forms = e.text_content()
            elif current_section == "Pronunciation" and not single_pronunciation:
                if e.tag != "ul":
                    continue
                enpr, prons = _parse_pronunciation_ul(e)
                pronunciations.extend(prons)
            elif current_section in POS_SECTIONS | MORPHOLOGICAL_SECTIONS:
                if e.tag != "p":
                    continue
                headword_line = e.xpath("span[contains(@class, 'headword-line')]")
                if headword_line:
                    derived = headword_line[0].xpath("b")
                    derived_forms = ", ".join(
                        [x.text_content() for x in derived if x.text_content() != word]
                    )

    if not single_pronunciation and pronunciations:
        words.append(
            Word(
                word,
                enpr,
                pronunciations,
                part_of_speech,
                etymology,
                alternate_forms,
                derived_forms,
            )
        )
    return words


def extract_language_section(word: str, language):
    session = requests_html.HTMLSession()
    request = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10, headers=HTTP_HEADERS)
    elements = []
    parsing = True
    element = request.html.find(f"h2#{language}", first=True)
    if element is None:
        return []
    for e in element.element.getparent().itersiblings():
        tag = e.tag
        h2 = e.find("h2")
        if h2 is not None:
            e = h2
            tag = e.tag
        if tag == "h2":
            if e.text == language:
                parsing = True
            else:
                parsing = False
        if not parsing:
            continue
        elements.append(e)
    return elements


def _scrape_word(word: str, language):
    session = requests_html.HTMLSession()
    request = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10, headers=HTTP_HEADERS)
    pron_xpath_selector = _PRON_XPATH_SELECTOR_TEMPLATE.format(language=language)
    dialect_pronunciations = []
    for pron_element in request.html.xpath(pron_xpath_selector):
        text = pron_element.text.split("\n")[0]
        dialect, pronunciation_string = text.split("IPA(key):")
        dialect = dialect.split(")")[0].strip().rstrip(")").strip("(")
        if (
            len(pron_element.findall("span.usage-label-accent")) == 1
            and len(pron_element.find("span.IPA")) == 1
        ):
            pronunciation_string = pron_element.find("span.IPA")[0].text
            dialect = pron_element.find("span.usage-label-accent")[0].text
            if text not in {
                f"IPA(key): {pronunciation_string} ({dialect})",
                f"({dialect}) IPA(key): {pronunciation_string}",
            }:
                continue
        if pron_element.element.getparent().getparent().tag == "li":
            try:
                actual_dialect = (
                    pron_element.element.getparent()
                    .getparent()
                    .find("span")
                    .text_content()
                    .strip()
                    .rstrip(")")
                    .strip("(")
                )
                dialect = f"{actual_dialect}, {dialect}"
            except AttributeError:
                pass
        dialect_pronunciations.append((dialect, pronunciation_string.strip()))

    return dialect_pronunciations


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def scrape(language):
    """Scrapes with a given configuration."""
    global RESTART_KEY
    category = _CATEGORY_TEMPLATE.format(language=language)
    print(category)
    requests_params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": "500",
        "cmprop": "ids|title|timestamp|sortkey",
    }
    if RESTART_KEY is not None:
        requests_params.update({"cmstarthexsortkey": RESTART_KEY})
    output_path = OUTPUT_DIR.joinpath(f"{language}.jsonl")
    with open(output_path, "w", encoding="utf8") as f:
        word_writer = jsonlines.Writer(
            f, dumps=functools.partial(json.dumps, default=set_default, ensure_ascii=False)
        )
        while True:
            resp = requests.get(
                "https://en.wiktionary.org/w/api.php?",
                params=requests_params,
                headers=HTTP_HEADERS,
            )
            try:
                data = resp.json()
            except requests.exceptions.JSONDecodeError:
                print(resp.text)
            # print(f"Processing {requests_params['sroffset']} of {data['query']['searchinfo']['totalhits']}")
            try:
                for member in data["query"]["categorymembers"]:
                    title = member["title"]
                    RESTART_KEY = member["sortkey"]
                    if _skip_word(title, True):
                        continue
                    print(title, RESTART_KEY)
                    # try:
                    #    dialect_pronunciations = _scrape_word(title, language)
                    # except ValueError:
                    #    continue
                    # if dialect_pronunciations:
                    #    for dialect, p in dialect_pronunciations:
                    #        f.write(f"{title}\t{dialect}\t{p}\n")

                    elements = extract_language_section(title, language)
                    single_etymology, single_pronunciation = parse_page_type(elements)
                    words = parse_section(title, elements, single_etymology, single_pronunciation)
                    if words:
                        word_writer.write_all([x.to_json() for x in words])
                # "cmstarthexsortkey" reset so as to avoid competition
                # with "continue_code".
                if "continue" not in data:
                    break
                continue_code = data["continue"]["cmcontinue"]

                requests_params.update({"cmcontinue": continue_code, "cmstarthexsortkey": None})
            except Exception as e:
                print(RESTART_KEY)
                if isinstance(
                    e,
                    (
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError,
                    ),
                ):
                    print("timed out")
                    requests_params.update({"cmstarthexsortkey": RESTART_KEY})
                    # 5 minute timeout. Immediately restarting after the
                    # connection has dropped appears to have led to
                    # 'Connection reset by peer' errors.
                    time.sleep(300)
                else:
                    raise


def functionality_testing():
    elements = extract_language_section("en", "English")
    single_etymology, single_pronunciation = parse_page_type(elements)
    assert not single_etymology
    assert not single_pronunciation
    words = parse_section("en", elements, single_etymology, single_pronunciation)
    assert len(words) == 3
    assert words[0].part_of_speech == "Noun"
    assert words[0].derived_forms == "ens"
    assert words[0].enpr == "ĕn"
    assert words[0].alternate_forms == """"""
    assert words[0].pronunciations == [
        ("UK, US", "/ˈɛn/"),
        ("pin–pen merger", "/ɪn/"),
    ]
    assert words[1].pronunciations == [
        ("imitating the French pronunciation", "[ɑ̃]"),
        ("imitating the French pronunciation", "[õ]"),
        ("anglicised", "/ɒn/"),
        ("anglicised", "/ɑn/"),
    ]
    assert words[2].pronunciations == [
        (None, "/ən/"),
    ]

    elements = extract_language_section("lead", "English")
    single_etymology, single_pronunciation = parse_page_type(elements)
    assert not single_etymology
    assert not single_pronunciation
    words = parse_section("lead", elements, single_etymology, single_pronunciation)
    assert len(words) == 4
    assert words[0].part_of_speech == "Noun"
    assert words[0].derived_forms == "leads"
    assert words[0].enpr == ""
    assert words[0].alternate_forms == """♄ (alchemy)"""
    assert words[0].pronunciations == [
        (None, "/ˈlɛd/"),
        (None, "[ˈlɛd]"),
    ]
    assert words[1].pronunciations == [
        (None, "/ˈlɛd/"),
        (None, "[ˈlɛd]"),
    ]
    assert words[2].pronunciations == [
        (None, "/ˈliːd/"),
        (None, "[ˈlɪi̯d]"),
    ]
    assert words[3].pronunciations == [
        (None, "/ˈliːd/"),
        (None, "[ˈlɪi̯d]"),
    ]

    elements = extract_language_section("head", "English")
    single_etymology, single_pronunciation = parse_page_type(elements)
    assert not single_etymology
    assert single_pronunciation
    words = parse_section("head", elements, single_etymology, single_pronunciation)
    assert len(words) == 3
    assert words[0].part_of_speech == "Noun"
    assert words[0].derived_forms == "heads"
    assert words[0].enpr == "hĕd"
    assert (
        words[0].alternate_forms
        == """'ead (UK, eye dialect)
heead (Yorkshire)
hed (archaic)"""
    )
    gold_pronunciations = [
        ("Received Pronunciation, General American, Canada", "/hɛd/"),
        ("Early Modern", "/hɛd/"),
        ("Early Modern", "/hɛːd/"),
        ("Australian, New Zealand", "/hed/"),
        ("Northumbrian", "/hiːd/"),
    ]
    pronunciations = words[0].pronunciations
    assert len(pronunciations) == len(gold_pronunciations)
    for i in range(len(pronunciations)):
        p = pronunciations[i]
        g = gold_pronunciations[i]
        assert p == g

    # Single etymology, single pronunciation

    elements = extract_language_section("pecan", "English")
    single_etymology, single_pronunciation = parse_page_type(elements)
    assert single_etymology
    assert single_pronunciation
    words = parse_section("pecan", elements, single_etymology, single_pronunciation)
    assert words[0].part_of_speech == "Noun"
    assert words[0].derived_forms == "pecans"
    assert words[0].enpr == ""
    assert words[0].alternate_forms == "paccan, peccan (dated, possibly obsolete)"
    gold_pronunciations = [
        (
            "US, most common US pronunciation except in New York, New England and coastal Southeast",
            "/piːˈkɑːn/",
        ),
        ("US, Midwestern US", "/pɪˈkɑːn/"),
        ("US, New York, New England, coastal southeastern Southern US", "/ˈpiːkæn/"),
        ("US, chiefly Upper Midwestern US", "/ˈpiːkɑːn/"),
        ("US, uncommon coastal New England variant", "/ˈpɪkæn/"),
        ("US, Louisiana", "/pəˈkɔːn/"),
        ("US, Louisiana", "/pɪˈkɔːn/"),
        ("US, occasional US unstressed pronunciation", "/pəˈkɑːn/"),
        ("Commonwealth, UK", "/pɪˈkɑːn/"),
        ("Commonwealth, UK, Australian, Canada", "/ˈpiːkæn/"),
        ("Commonwealth, Canada, Australian, New Zealand, rarely US", "/piːˈkæn/"),
        ("Commonwealth, UK, Canada, very rarely US", "/pɪˈkæn/"),
        ("Commonwealth, UK, Australian, New Zealand", "/ˈpiːkən/"),
        ("Commonwealth, Canada", "/pəˈkɒn/"),
    ]
    pronunciations = words[0].pronunciations
    assert len(pronunciations) == len(gold_pronunciations)
    for i in range(len(pronunciations)):
        p = pronunciations[i]
        g = gold_pronunciations[i]
        assert p == g

    elements = extract_language_section("who", "English")
    single_etymology, single_pronunciation = parse_page_type(elements)
    assert single_etymology
    assert single_pronunciation
    words = parse_section("who", elements, single_etymology, single_pronunciation)
    assert words[0].part_of_speech == "Pronoun"
    assert words[0].derived_forms == ""
    assert words[0].alternate_forms == ""
    assert words[0].enpr == "ho͞o"
    pronunciations = words[0].pronunciations
    gold_pronunciations = [
        ("Received Pronunciation, Wales", "/huː/"),
        ("Standard Southern British", "/hʉw/"),
        ("General American", "/hu/"),
        ("Canada", "/hu/"),
        ("Australian, New Zealand", "/hʉː/"),
        ("Scotland, Northern Ireland", "/hʉ/"),
        ("Early Modern", "/h(w)uː/"),
        ("Early Modern", "/h(w)ɔː/"),
        ("Early Modern, originally unstressed", "/hwɒ/"),
    ]
    assert len(pronunciations) == len(gold_pronunciations)
    for i in range(len(pronunciations)):
        p = pronunciations[i]
        g = gold_pronunciations[i]
        assert p == g


if __name__ == "__main__":
    # functionality_testing()
    # error
    for lang in LANGUAGES:
        output_path = OUTPUT_DIR.joinpath(f"{lang}.jsonl")
        if output_path.exists():
            continue
        RESTART_KEY = None
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # print(_scrape_word("enquadrar"))
        scrape(lang)

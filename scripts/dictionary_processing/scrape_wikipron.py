import pathlib
import re
import time

import requests
import requests_html

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT_DIR.joinpath("dictionary", "training", "scraped")

LANGUAGES = [
    "French",
    "German",
    "Italian",
    "Dutch",
    "Danish",
    "Hungarian",
    "Bulgarian",
    "Thai",
    "Korean",
    "English",
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
IPA_XPATH_SELECTOR = '//li/span[@class = "IPA"]'
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
_PHONEMES_REGEX = [r"/(.+?)/", r"\[(.+?)\]"]


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


def _scrape_word(word: str, language):
    session = requests_html.HTMLSession()
    request = session.get(_PAGE_TEMPLATE.format(word=word), timeout=10, headers=HTTP_HEADERS)
    pron_xpath_selector = _PRON_XPATH_SELECTOR_TEMPLATE.format(language=language)
    dialect_pronunciations = []
    for pron_element in request.html.xpath(pron_xpath_selector):
        text = pron_element.text.split("\n")[0]
        dialect, pronunciation_string = text.split("IPA(key):")
        dialect = dialect.split(")")[0].strip().rstrip(")").strip("(")
        for r in _PHONEMES_REGEX:
            pronunciations = re.findall(r, pronunciation_string)
            for p in pronunciations:
                if (dialect, p) not in dialect_pronunciations:
                    dialect_pronunciations.append((dialect, p))
            if pronunciations:
                break

    return dialect_pronunciations


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
    output_path = OUTPUT_DIR.joinpath(f"{language}.tsv")
    with open(output_path, "a", encoding="utf8") as f:
        while True:
            data = requests.get(
                "https://en.wiktionary.org/w/api.php?",
                params=requests_params,
                headers=HTTP_HEADERS,
            ).json()
            # print(f"Processing {requests_params['sroffset']} of {data['query']['searchinfo']['totalhits']}")
            try:
                for member in data["query"]["categorymembers"]:
                    title = member["title"]
                    RESTART_KEY = member["sortkey"]
                    if _skip_word(title, True):
                        continue
                    print(title, RESTART_KEY)
                    try:
                        dialect_pronunciations = _scrape_word(title, language)
                    except ValueError:
                        continue
                    if dialect_pronunciations:
                        for dialect, p in dialect_pronunciations:
                            f.write(f"{title}\t{dialect}\t{p}\n")
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


if __name__ == "__main__":
    for lang in LANGUAGES:
        output_path = OUTPUT_DIR.joinpath(f"{lang}.tsv")
        if output_path.exists():
            continue
        RESTART_KEY = None
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # print(_scrape_word("enquadrar"))
        scrape(lang)

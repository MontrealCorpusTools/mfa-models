# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from datetime import date
import os
import sys
from montreal_forced_aligner.utils import get_mfa_version  # noqa

# -- Project information -----------------------------------------------------

project = 'MFA Models'
copyright = f"2018-{date.today().year}, Montreal Corpus Tools"
author = 'Montreal Corpus Tools'

version = ".".join(get_mfa_version().split(".", maxsplit=2)[:2])
# The full version, including alpha/beta/rc tags.
release = get_mfa_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

extensions = [
    "sphinxcontrib.needs",
    "sphinx_design",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    'myst_parser',
    'sphinx.ext.autosectionlabel',
    'ipa_charts'
]
myst_enable_extensions = ["colon_fence"]
panels_add_bootstrap_css = False
autosectionlabel_prefix_document = True
needs_include_needs = True

needs_types = [dict(directive="acoustic", title="Acoustic model", prefix="AM_", color="#BFD8D2", style="node"),
               dict(directive="corpus", title="Corpus", prefix="", color="#FEDCD2", style="node"),
               dict(directive="g2p", title="G2P model", prefix="G2P_", color="#FEDCD2", style="node"),
               dict(directive="language_model", title="Language model", prefix="LM_", color="#DF744A", style="node"),
               dict(directive="ivector_extractor", title="Ivector Extractor", prefix="IE_", color="#DCB239", style="node"),
               dict(directive="dictionary", title="Dictionary", prefix="D_", color="#DCB239", style="node"),
           ]

needs_template_folder = '_templates/needs_templates'

needs_layouts = {
    'not_mfa': {
        'grid': 'content',
    },
    'mfa': {
        'grid': 'content_side_right',
        'layout': {
            'side': ['<<image("_static/full_logo_yellow.svg")>>']
        }
    }
}

needs_show_link_title =True
needs_show_link_type =True
needs_role_need_template = "{title}"
needs_extra_options = ['name', 'language', 'dialect', 'architecture', 'phoneset', 'license']
needs_table_style = "datatables"
needs_table_columns = "ID;name;language;dialect;phoneset;tags"
needs_tags = [
    dict(name="MFA", description="Maintained by Montreal Forced Aligner"),
    dict(name="PROSODYLAB", description="Resources developed by Prosodylab"),
    dict(name="PINYIN", description="Pinyin phone set"),
    dict(name="CV", description="Maintained by VoxCommunis"),
    dict(name="IPA", description="Based on the International Phonetic Alphabet"),
    dict(name="Common Voice", description="Corpora in Mozilla's Common Voice collection"),
    dict(name="Google", description="Corpora collected and distributed by Google"),
    dict(name="Microsoft", description="Corpora collected and distributed by Microsoft"),
    dict(name="GlobalPhone", description="Corpora in GlobalPhone collection"),
    dict(name="VoxPopuli", description="Corpora in Vox Populi collection"),
    dict(name="MediaSpeech", description="Corpora in MediaSpeech collection"),
    dict(name="Multilingual Librispeech", description="Corpora in Multilingual Librispeech collection"),
    dict(name="M-AILABS", description="Corpora in M-AILABS's collections"),
    dict(name="Multilingual TEDx", description="Corpora in the Multilingual TEDx collection"),
]

current_languages = ["Abkhaz", "Armenian", "Arabic", "Bashkir", "Basque", "Belarusian", "Bulgarian",
                     "Chuvash", "Croatian", "Czech", "Dutch", "English", "French", "Georgian", "German","Greek",
                     "Guarani", "Hausa", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese", "Kazakh", "Korean", "Kurmanji", "Kyrgyz",
                     "Maltese", "Mandarin", "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Sorbian", "Spanish", "Swahili", "Swedish",
                     "Tamil", "Tatar", "Thai", "Turkish", "Ukrainian", "Urdu",  "Uyghur", "Uzbek", "Vietnamese"]
for lang in current_languages:
    needs_tags.append({'name': lang,'description':f'{lang} language'})

needs_id_regex = '[A-Za-z0-9 .():_]+'
needs_id_required = True
needs_role_need_max_title_length = 0
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


xref_links = {
    "wikipedia": ("Wikipedia", "https://en.wikipedia.org/wiki/Main_Page"),
    "phoible": ("Phoible", "https://phoible.org/"),
    "xpf": ("XPF", "https://cohenpr-xpf.github.io/XPF/"),
    "nagisa": ("Nagisa", "https://github.com/taishi-i/nagisa"),
    "konlpy": ("KoNLPy", "https://konlpy.org/en/latest/"),
    "spacy_pkuseg": ("spacy-pkuseg", "https://github.com/explosion/spacy-pkuseg/"),
    "num2chinese": ("num2chinese.py", "https://gist.github.com/gumblex/0d65cad2ba607fd14de7"),
    "hanziconv": ("hanziconv", "https://github.com/berniey/hanziconv"),
    "num2words": ("hanziconv", "https://github.com/savoirfairelinux/num2words"),
    "thai_word_segmentation": ("thai-word-segmentation", "https://github.com/sertiscorp/thai-word-segmentation"),
    "mecab_ko": ("Mecab-KO", "https://bitbucket.org/eunjeon/mecab-ko/src/master/"),
}

needs_extra_links = [
    {
        "option": "built_with",
        "incoming": "Built with",
        "outgoing": "Built with",
        "allow_dead_links ": True,
}
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"


html_theme_options = {
    "external_links": [
        {
            "url": "https://montreal-forced-aligner.readthedocs.io/",
            "name": "MFA docs",
        },
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MontrealCorpusTools/mfa-models",
            "icon": "fab fa-github",
        },
    ],
    "logo": {
        "text": "Montreal Forced Aligner",
        # "image_dark": "logo-dark.svg",
    },
    "google_analytics_id": "UA-73068199-4",
    "show_nav_level": 1,
    "navigation_depth": 4,
    "show_toc_level": 2,
    "collapse_navigation": False,
}
html_context = {
    "github_user": "MontrealCorpusTools",
    "github_repo": "mfa-models",
    "github_version": "main",
    "doc_path": "docs/source",
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/fontawesome.min.css",
    "css/style.css",
    "css/datatables.css",
]
html_js_files = [
    'main.js',
]
html_sidebars = {"**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]}
rst_prolog = """
.. role:: manner
   :class: manner

.. role:: submanner
   :class: submanner

.. role:: lexical_set
   :class: lexical-set

.. role:: ipa_inline
   :class: ipa-inline ipa-highlight
"""
from sphinxcontrib.needs.api.configuration import add_dynamic_function


license_links = {
    'CC-0': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC BY-NC-SA 4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC BY-NC-ND 4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY-NC 2.0': 'https://creativecommons.org/licenses/by-nc/2.0/',
    'Microsoft Research Data License': 'https://msropendata-web-api.azurewebsites.net/licenses/2f933be3-284d-500b-7ea3-2aa2fd0f1bb2/view',
    'Apache 2.0': 'https://www.apache.org/licenses/LICENSE-2.0',
    'MIT': 'https://opensource.org/licenses/MIT',
    'Public domain in the USA': 'https://creativecommons.org/share-your-work/public-domain/cc0/',
    'M-AILABS License': 'https://www.caito.de/2019/01/the-m-ailabs-speech-dataset/',
    'ELRA': 'https://www.elra.info/en/services-around-lrs/distribution/licensing/',

}

for lic in license_links.keys():
    desc = lic
    if not lic.endswith(' License') and 'Public' not in lic:
        desc += ' License'
    needs_tags.append({'name': lic,'description': desc})

phone_set_links = {
'Epitran': 'https://github.com/dmort27/epitran',
'XPF': 'https://github.com/CohenPr-XPF/XPF',
'ARPA': 'https://en.wikipedia.org/wiki/ARPABET',
'MFA': 'https://mfa-models.readthedocs.io/en/refactor/mfa_phone_set.html',
}

for ps in phone_set_links.keys():
    needs_tags.append({'name': ps,'description':f'{ps} phone set'})


def name_link(app, need, needs, *args, **kwargs):
    target_node = need['target_node']
    print(target_node)
    return str(target_node)

def language_link(app, need, needs, *args, **kwargs):
    target_node = need['target_node']
    return str(target_node)

def license_link(app, need, needs, license):
    return f"[{license}]({license_links[license]})"

def phone_set_link(app, need, needs, phone_set):
    print(need)
    print(need['language'])
    if phone_set not in phone_set_links:
        return phone_set
    return f"[{phone_set}]({phone_set_links[phone_set]})"

needs_string_links = {
    # Adds link to the Sphinx-Needs configuration page
    'external_link': {
        'regex': r'^\[(?P<title>.+)\]\((?P<link>.+)\)$',
        'link_url': '{{link}}',
        'link_name': '{{title}}',
        'options': ['phoneset', 'license']
    },
    # Links to the related github issue
    'github_link': {
        'regex': r'^(?P<value>\w+)$',
        'link_url': 'https://github.com/useblocks/sphinxcontrib-needs/issues/{{value}}',
        'link_name': 'GitHub #{{value}}',
        'options': ['github']
    }
}
def setup(app):
    add_dynamic_function(app, name_link)
    add_dynamic_function(app, language_link)
    add_dynamic_function(app, license_link)
    add_dynamic_function(app, phone_set_link)

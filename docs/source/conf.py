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


# -- Project information -----------------------------------------------------

project = 'MFA Models'
copyright = f"2018-{date.today().year}, Montreal Corpus Tools"
author = 'Montreal Corpus Tools'

# The full version, including alpha/beta/rc tags
release = '2.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [
    "sphinxcontrib.needs",
    "sphinx_panels",
    "sphinx.ext.viewcode",
    "sphinxemoji.sphinxemoji",
    'myst_parser',
    'sphinx.ext.autosectionlabel',
]
panels_add_bootstrap_css = False
autosectionlabel_prefix_document = True
needs_include_needs = True

needs_types = [dict(directive="acoustic", title="Acoustic model", prefix="AM_", color="#BFD8D2", style="node"),
               dict(directive="g2p", title="G2P model", prefix="G2P_", color="#FEDCD2", style="node"),
               dict(directive="language_model", title="Language model", prefix="LM_", color="#DF744A", style="node"),
               dict(directive="ivector_extractor", title="Ivector Extractor", prefix="IE_", color="#DCB239", style="node"),
               dict(directive="dictionary", title="Dictionary", prefix="D_", color="#DCB239", style="node"),
           ]

needs_template_folder = '_templates/needs_templates'

needs_layouts = {
    'acoustic': {
        'grid': 'simple',
        'layout': {
            'head': ['**<<meta("language")>>** **<<meta("phoneset")>>** acoustic model'],
            'meta': [
                '**tags**: <<meta("tags")>>',
            ],
        }
    },
    'dictionary': {
        'grid': 'simple',
        'layout': {
            'head': ['**<<meta("language")>>** **<<meta("phoneset")>>** dictionary'],
            'meta': [
                '**tags**: <<meta("tags")>>',
            ],
        }
    },
    'g2p': {
        'grid': 'simple',
        'layout': {
            'head': ['**<<meta("language")>>** **<<meta("phoneset")>>** G2P model'],
            'meta': [
                '**tags**: <<meta("tags")>>',
            ],
        }
    },
    'language_model': {
        'grid': 'simple',
        'layout': {
            'head': ['**<<meta("language")>>** language model'],
            'meta': [
                '**tags**: <<meta("tags")>>',
            ],
        }
    },
}

needs_show_link_title =True
needs_show_link_type =True
needs_role_need_template = "{title}"
needs_extra_options = ['language', 'architecture', 'phoneset']
needs_table_style = "datatables"
needs_table_columns = "ID;title;language;phoneset;tags"
#needs_tags = [
#    dict(name="MFA", description="Maintained by MFA"),
#]
needs_id_regex = '[A-Za-z0-9_]+'
needs_id_required = True
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


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

html_logo = "_static/logo_long.svg"
html_favicon = "_static/favicon.ico"


html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/MontrealCorpusTools/mfa-models",
            "icon": "fab fa-github",
        },
    ],
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
    "css/style.css",
]
html_sidebars = {"**": ["search-field.html", "sidebar-nav-bs.html", "sidebar-ethical-ads.html"]}

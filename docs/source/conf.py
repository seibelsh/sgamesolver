# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'sGameSolver'
copyright = '2018, Eibelshäuser & Poensgen'
author = 'Steffen Eibelshäuser and David Poensgen'

release = '0.1'
version = '0.1.0'

# -- General configuration

master_doc = 'index'

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.autosectionlabel',
    'sphinx_tabs.tabs',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

numfig = True

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'prev_next_buttons_location': 'bottom',
    'sticky_navigation': True,
    'collapse_navigation': True,
    'navigation_depth': 2,
    'includehidden': True,
    'titles_only': False,
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

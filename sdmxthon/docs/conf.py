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
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
about = {}
with open('../__version__.py', 'r') as f:
    exec(f.read(), about)

project = about['project']
description = about['description']
url = about['url']
version = about['version']
author = about['author']
author_email = about['author_email']
copyright = about['copyright']

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel'
]

autosectionlabel_prefix_document = True

html_show_sourcelink = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'analytics_id': '',
    'analytics_anonymize_ip': True,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': '',
    'style_external_links': True,
    'vcs_pageview_mode': 'blob',
    'collapse_navigation': False,
    'sticky_navigation': False,
    'navigation_depth': 4,
    'includehidden': False,
    'titles_only': False
}
github_url = "https://github.com/Meaningful-Data/sdmxthon"
html_context = {
    'display_github': True,
    'github_user': 'Meaningful-Data',
    'github_repo': 'sdmxthon',
    'github_version': 'master',
    'conf_py_path': '/sdmxthon/docs/',
    'suffix': '.rst'
}

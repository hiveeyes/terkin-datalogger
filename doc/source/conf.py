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
sys.path.insert(0, os.path.abspath('../src/lib'))


# -- Project information -----------------------------------------------------

project = 'Terkin Datalogger'
copyright = '2017-2022, The Terkin Developers'
author = 'The Terkin Developers'

# The full version, including alpha/beta/rc tags
release = '0.13.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.graphviz',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Link with other projects
intersphinx_mapping = {
    'kotori':  ('https://getkotori.org/docs/', None),
    }


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinxdoc'

html_last_updated_fmt = ""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/img/terkin-logo.png'
def setup(app):
    app.add_css_file("css/terkin-sphinx.css")



# -- Custom options -------------------------------------------
import sphinx_material

html_show_sourcelink = True
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Required theme setup
extensions.append('sphinx_material')
html_theme = 'sphinx_material'
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()

# Material theme options (see theme.conf for more information)
html_theme_options = {

    # Set the name of the project to appear in the navigation.
    'nav_title': 'Terkin',

    # Set you GA account ID to enable tracking
    #'google_analytics_account': 'UA-XXXXX',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://terkin.org/docs/',

    # Set the color and the accent color
    'color_primary': 'teal',
    #'color_accent': 'light-green',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/hiveeyes/terkin-datalogger/',
    'repo_name': 'Terkin',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 3,
    # If False, expand all TOC entries
    #'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    #'globaltoc_includehidden': False,

    "master_doc": False,
    "nav_links": [
    ],

    "heroes": {
        "index": "A flexible data logger for MicroPython and CPython.",
    },
}


# -- Autodoc options -------------------------------------------
from terkin_cpython.util import patch_system
patch_system()

from umal import MicroPythonBootloader
bootloader = MicroPythonBootloader()
setattr(sys.modules['__main__'], 'bootloader', bootloader)

#autodoc_mock_imports = ["machine"]

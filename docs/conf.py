import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'sshlab'
copyright = '2023, Thomas Vuillaume'
author = 'Thomas Vuillaume'
release = '0.1.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = []
exclude_patterns = ['build', '_build', 'Thumbs.db', '.DS_Store']

root_doc = 'index'

html_theme = 'furo'

html_static_path = []


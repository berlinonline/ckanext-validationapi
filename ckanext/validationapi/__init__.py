from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()

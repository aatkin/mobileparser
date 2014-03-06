try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Restaurant food parsers for mobilefood project',
    'author': 'Ville & Anssi',
    'url': 'https://github.com/Wiltzu/mobilefood_parser',
    'version': '0.2.1',
    'install_requires': ['nose', 'bs4'],
    'packages': ['mobilefood_parser', 'tests'],
    'scripts': [],
    'name': 'mobilefood_parser'
}

setup(**config)


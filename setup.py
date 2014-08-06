from setuptools import setup
from mobileparser import __version__

packages = [
    'mobileparser',
    'tests'
]

install_requires = [
]

tests_requires = [
]

# config = {
#     'description': 'Restaurant food parsers for mobilefood project',
#     'author': 'Ville & Anssi',
#     'url': 'https://github.com/Wiltzu/mobilefood_parser',
#     'version': '0.2.2',
#     'install_requires': ['nose', 'beautifulsoup4', 'lxml', 'jsonpickle'],
#     'packages': ['mobilefood_parser', 'tests'],
#     'scripts': [],
#     'name': 'mobilefood_parser'
# }

setup(
    name='mobileparser',
    description='Restaurant food list parser for Mobilefood project',
    version=__version__,
    url='https://github.com/aatkin/mobilefood-parser',
    author='Anssi Kinnunen',
    license='MIT'
    packages=packages,
    include_package_data=True,
    zip_save=False,
    install_requires=install_requires,
    tests_requires=tests_requires
    )

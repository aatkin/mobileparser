from setuptools import setup
from mobileparser import __version__

packages = [
    'mobileparser',
    'tests'
]

install_requires = [
]

setup(
    name='mobileparser',
    description='Restaurant food list parser for Mobilefood project',
    version=__version__,
    url='https://github.com/aatkin/mobilefood-parser',
    author='Anssi Kinnunen',
    author='aatkin@utu.fi',
    license='MIT License'
    packages=packages,
    install_requires=install_requires,
    include_package_data=True,
    zip_save=False
    )

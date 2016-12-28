from setuptools import setup, find_packages

setup(
    name = 'pyPit',
    version = '0.1',
    keywords = ('package', 'chinatelecom'),
    description = 'package tools for packup all python source files and dependences',
    license = 'MIT License',
    install_requires = [],

    author = 'astwyg',
    author_email = 'i@ysgh.net',
    
    packages = find_packages(),
    platforms = 'any',

    url = "https://github.com/astwyg/py-pit",
)
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Internet Color Quantizer',
    'author': 'Johan Mickos',
    'author_email': 'johan.mickos@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['icq'],
    'scripts': [],
    'name': 'icq'
}

setup(**config)


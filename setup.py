import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='djangoldp_account',
      version='0.0.6',
      description='djangoldp package for account and chat data models',
      url='http://git.happy-dev.fr/startinblox/djangoldp_account',
      author="Startin'blox",
      author_email='jblemee@happy-dev.fr',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)

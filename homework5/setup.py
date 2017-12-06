#!/usr/bin/env python
from github_extra import VERSION
from setuptools import setup

setup(
   name='pr_stats',
   description='pr_stats get PR(Pull Request) statistics from GitHub',
   version = VERSION,
   packages = ['github_extra'],
   scripts = ['pr_stats'],
   install_requires = [
      'docopt >= 0.6.2, < 0.7',
      'envoy >= 0.0.3',
      'github3.py >= 0.9.5',
      'importlib >= 1.0.4',
      'numpy >= 1.13.3, < 1.14',
      'ordereddict >= 1.1',
      'python-dateutil >= 2.2, < 2.3',
   ],
)

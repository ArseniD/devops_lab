#!/usr/bin/env python
from py_extra import VERSION
from setuptools import setup


setup(
   name='pr_versions',
   description='pr_versions all python and pip info in current system',
   version = VERSION,
   packages = ['py_extra'],
   scripts = ['py_versions'],
   install_requires = [
      'PyYAML >= 3.0.0',
      'argparse >= 1.3.0',
      'unittest2 >= 1.1.0',
   ],
)

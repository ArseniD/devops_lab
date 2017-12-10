#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Collect python and pip versions in current system
via system libs and output info in json or yaml formats

'''

from __future__ import print_function

import sys
import os
import platform
import site
from subprocess import check_output

import json
import yaml


class PythonVersion(object):
    '''
    Get information about python and pip version in current system


    :param format_spec: string, json|yaml|None,
    format of output data
    '''
    def __init__(self, format_spec=None):

        self.__names = self.py_names()
        self.__py_loc = self.py_location()
        self.__v_env = self.is_venv()
        self.__pip_loc = self.pip_location()
        self.__py_path = os.environ.get('PYTHONPATH', '')
        self.__pack = self.pip_packages()

        # Call function to print data in appropriate format (json|yaml|all)
        self.__format__(format_spec)

    def get_data(self):
        '''
        Form data for output

        :return: dict with data
        '''
        data = {'py_ver': platform.python_version(),
                'py_name': self.__names,
                'py_venv': self.__v_env,
                'py_loc': self.__py_loc,
                'pip_loc': self.__pip_loc,
                'py_path': self.__py_path,
                'packages': self.__pack,
                'site_loc': site.getsitepackages(), }
        return data

    def __str__(self):
        return json.dumps(self.get_data())

    def __repr__(self):
        return yaml.dump(self.get_data(),
                         default_flow_style=False, allow_unicode=True)

    def __format__(self, spec=None):
        if spec == 'json':
            return json.dumps(self.get_data())
        elif spec == 'yaml':
            return yaml.dump(self.get_data(),
                             default_flow_style=False, allow_unicode=True)
        else:
            return '{0}\n\n{1}'.format(
                json.dumps(self.get_data()),
                (yaml.dump(self.get_data(),
                           default_flow_style=False,
                           allow_unicode=True)))

    @classmethod
    def py_names(cls):
        '''
        Get all executable python binary names

        :return: collection of unique python names
        '''
        tmp = []
        py_name = check_output(
            r"sudo find / -type f -executable \
            -iname 'python*' -exec file -i '{}' \;"
            " | awk -F: '/x-executable; charset=binary/ {print $1}'",
            shell=True, executable='/bin/bash')
        new_py_name = py_name.splitlines()
        for line in new_py_name:
            tmp.append(line.rsplit('/', 1)[-1])
        p_name = [os.path.splitext(each)[0] for each in tmp]
        return list(set(p_name))

    @classmethod
    def py_location(cls):
        '''
        Get all python location in current system

        :return: paths to python bin files
        '''
        py_data = check_output('which -a python', shell=True)
        py_location = py_data.splitlines()
        return py_location

    @classmethod
    def pip_packages(cls):
        '''
        Get all pip installed packages

        :return: a dict data of the form [package]: version
        '''
        pip_data = check_output('sudo pip freeze', shell=True)
        new_pip_pack = pip_data.splitlines()
        d_pip_pack = dict(s.split('==') for s in new_pip_pack)
        return d_pip_pack

    @classmethod
    def pip_location(cls):
        '''
        Get all pip location in current system

        :return: paths to pip bin files
        '''
        pip_data = check_output('which -a pip', shell=True)
        pip_loc = pip_data.splitlines()
        return pip_loc

    @staticmethod
    def is_venv():
        '''
        Check whether we use virtualenv or not

        :return: virtualenv executable path or 'Not set' value
        '''
        if hasattr(sys, 'real_prefix'):
            return os.environ.get('VIRTUAL_ENV')
        else:
            return 'Not set'


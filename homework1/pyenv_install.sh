#!/bin/bash

# Start by making sure your system is up-to-date:
yum update
# Compilers and related tools:
yum groupinstall -y "development tools"
# Libraries needed during compilation to enable all features of Python:
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel
# If you are on a clean "minimal" install of CentOS you also need the wget tool:
yum install -y wget


# Python 2.7.14:
wget http://python.org/ftp/python/2.7.14/Python-2.7.14.tar.xz
tar xf Python-2.7.14.tar.xz
cd Python-2.7.14
./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make && make altinstall
 
# Python 3.5.4:
wget http://python.org/ftp/python/3.5.4/Python-3.5.4.tar.xz
tar xf Python-3.5.4.tar.xz
cd Python-3.5.4
./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make && make altinstall


# First get the script:
wget https://bootstrap.pypa.io/get-pip.py
 
# Then execute it using Python 2.7 and/or Python 3.6:
python2.7 get-pip.py
python3.5 get-pip.py
 
# With pip installed you can now do things like this:
pip2.7 install [packagename]
pip2.7 install --upgrade [packagename]
pip2.7 uninstall [packagename]

# Install virtualenv for Python 2.7 and create a sandbox called my27project:
pip2.7 install virtualenv
virtualenv my27project
 
# Use the built-in functionality in Python 3.6 to create a sandbox called my36project:
python3.5 -m venv my35project
 
# Check the system Python interpreter version:
python --version
# This will show Python 2.7.14
 
# Activate the my27project sandbox:
source my27project/bin/activate
# Check the Python version in the sandbox (it should be Python 2.7.14):
python --version
# Deactivate the sandbox:
deactivate
 
# Activate the my36project sandbox:
source my36project/bin/activate
# Check the Python version in the sandbox (it should be Python 3.5.4):
python --version
# Deactivate the sandbox:
deactivate

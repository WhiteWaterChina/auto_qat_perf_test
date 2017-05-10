#!/bin/bash
ROOT_DIR=`pwd`
tar -zxf Python-2.7.12.tgz
tar -zxf setuptools-28.8.0.tar.gz
tar -zxf pip-9.0.1.tar.gz
cd Python-2.7.12
./configure
make
make install
python2.7 -V
cd $ROOT_DIR/setuptools-28.8.0
python2.7 setup.py install
cd $ROOT_DIR/pip-9.0.1
python2.7 setup.py install
cd $ROOT_DIR
pip install --no-index --find-links="offline/" -r requirments.txt
echo "Set environment succefully!"


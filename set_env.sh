#!/bin/bash
ROOT_DIR=`pwd`
ip_remote="100.2.36.194"
wget http://${ip_remote}/ks/ali/test_tool/qat/offline.zip
wget http://${ip_remote}/ks/ali/test_tool/qat/openssl-master.zip
wget http://${ip_remote}/ks/ali/test_tool/qat/pip-9.0.1.tar.gz
wget http://${ip_remote}/ks/ali/test_tool/qat/Python-2.7.12.tgz
wget http://${ip_remote}/ks/ali/test_tool/qat/qat-engine-0.5.24.tar.gz
wget http://${ip_remote}/ks/ali/test_tool/qat/requirments.txt
wget http://${ip_remote}/ks/ali/test_tool/qat/setuptools-28.8.0.tar.gz
wget http://${ip_remote}/ks/ali/test_tool/qat/QAT1.7.L.1.0.4-2.tar.gz

tar -zxf Python-2.7.12.tgz
tar -zxf setuptools-28.8.0.tar.gz
tar -zxf pip-9.0.1.tar.gz
tar -zxf qat-engine-0.5.24.tar.gz
unzip offline.zip
unzip openssl-master.zip
if [-d qat]; then
rm -rf qat
fi
mkdir qat
cp QAT1.7.L.1.0.4-2.tar.gz qat/

cd $ROOT_DIR/qat
tar -zxf QAT1.7.L.1.0.4-2.tar.gz
sleep 1

cd $ROOT_DIR/Python-2.7.12
./configure
make
make install
python2.7 -V

cd $ROOT_DIR/setuptools-28.8.0
python2.7 setup.py install

cd $ROOT_DIR/pip-9.0.1
python2.7 setup.py install

cd $ROOT_DIR/openssl-master
./config --prefix=/usr/local/ssl
make depend
make
make install

cd $ROOT_DIR/qat-engine-0.5.24/qat_contig_mem/
make
make load
make test

cd $ROOT_DIR/qat/quickassist/utilities/libusdm_drv
insmod ./usdm_drv.ko

cd $ROOT_DIR/qat-engine-0.5.24/
./configure --with-qat_dir=$ROOT_DIR/qat --with-openssl_dir=$ROOT_DIR/openssl-master --with-openssl_install_dir=/usr/local/ssl --enable-upstream_driver --enable-usdm
make
make install

unalias cp
cp -rf $ROOT_DIR/qat-engine-0.5.24/qat/config/c6xx/multi_process_optimized/*.conf /etc

cat /etc/ld.so.conf|grep "/usr/local/ssl/lib"
if [ $? -ne 0 ]; then
echo "/usr/local/ssl/lib" >> /etc/ld.so.conf
fi
ldconfig -v

pip install --no-index --find-links="offline/" -r requirments.txt
echo "Set environment succefully!"

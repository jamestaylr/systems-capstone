#!/bin/bash
sudo su
apt-get --allow-unauthenticated update
apt-get install -y build-essential
apt-get install -y linux-source

tar xf /usr/src/linux-source-2.6.24.tar.bz2 -C /usr/src/
wget http://www.read.cs.ucla.edu/click/click-2.0.1.tar.gz -P /usr/src
tar xf /usr/src/click-2.0.1.tar.gz -C /usr/src
chmod 755 -R click
chown -R root:root click*

cd /usr/src/linux-source-2.6.24
make defconfig
make
patch -p1 -b < /usr/src/click-2.0.1/etc/linux-2.6.24.7-patch

cd /usr/src/click-2.0.1
./configure --enable-linuxmodule --with-linux=/usr/src/linux-source-2.6.24/
make

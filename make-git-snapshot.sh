#!/bin/sh

DIRNAME=xorg-server-$( date +%Y%m%d )

rm -rf $DIRNAME
git clone git://git.freedesktop.org/git/xorg/xserver $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git log | head -1
else
    git checkout -b $1 origin/$1
fi
git log | head -1 | awk '{ print $2 }' > ../commitid
git repack -a -d
git-config user.email "x@fedoraproject.org"
git-config user.name "Fedora X Ninjas"
cd ..
tar jcf $DIRNAME.tar.bz2 $DIRNAME
rm -rf $DIRNAME

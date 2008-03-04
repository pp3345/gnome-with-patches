#!/bin/sh

DIRNAME=xorg-server-$( date +%Y%m%d )

rm -rf $DIRNAME
git clone -n git://git.freedesktop.org/git/xorg/xserver $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git checkout --track -b server-1.5-branch origin/server-1.5-branch
else
    git checkout $1
fi
git log | head -1 | awk '{ print $2 }' > ../commitid
git repack -a -d
cd ..
tar jcf $DIRNAME.tar.bz2 $DIRNAME
rm -rf $DIRNAME

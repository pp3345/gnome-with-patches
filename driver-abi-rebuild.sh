#!/bin/sh
#
# Trivial script to rebuild drivers for ABI changes in the server
# Run me after a new xserver has hit the buildroot

mkdir -p abi-rebuild
pushd abi-rebuild

fedpkg co xorg-x11-drivers
pushd xorg-x11-drivers
driverlist=$(grep ^Requires *.spec | awk '{ print $2 }')
popd

rm -rf xorg-x11-drivers
echo $driverlist | xargs -n1 fedpkg co

for i in */ ; do
    [ -e $i/dead.package ] && continue
    pushd $i
    rpmdev-bumpspec -c "- ABI rebuild" *.spec
    fedpkg commit -c -p && fedpkg build --nowait
    popd
done

popd



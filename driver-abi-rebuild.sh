#!/bin/sh
#
# Trivial script to rebuild drivers for ABI changes in the server
# Run me after a new xserver has hit the buildroot

builddir="abi-rebuild"

if [ -e "$builddir" ]; then
    echo "Path '$builddir' exists. Move out of the way first"
    exit 1
fi

mkdir -p $builddir
pushd $builddir

if git config --get remote.origin.url | grep -q redhat.com ; then
    pkg=rhpkg
else
    pkg=fedpkg
fi

$pkg co xorg-x11-drivers
pushd xorg-x11-drivers
driverlist=$(grep ^Requires *.spec | awk '{ print $2 }')
popd

# Things not in -drivers for whatever reason...
extradrivers="xorg-x11-drv-ivtv"

rm -rf xorg-x11-drivers
echo $driverlist $extradrivers | xargs -n1 $pkg co

for i in */ ; do
    [ -e $i/dead.package ] && continue
    pushd $i
    rpmdev-bumpspec -c "- ABI rebuild" *.spec
    $pkg commit -c -p && $pkg build --nowait
    popd
done

popd



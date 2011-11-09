#!/bin/sh
#
# Trivial script to rebuild drivers for ABI changes in the server
# Run me after a new xserver has hit the buildroot

mkdir abi-rebuild
pushd abi-rebuild

repoquery --qf="%{name}" --whatrequires xserver-abi\* | xargs -n 1 fedpkg co
for i in */ ; do
    pushd $i
    rpmdev-bumpspec -c "- ABI rebuild"
    fedpkg commit -c -p && fedpkg build --nowait
    popd
done

popd



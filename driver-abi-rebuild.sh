#!/bin/sh
#
# Trivial script to rebuild drivers for ABI changes in the server
# Run me after a new xserver has hit the buildroot

mkdir -p abi-rebuild
pushd abi-rebuild

repoquery --qf="%{name}" --whatrequires xserver-abi\* | xargs -n 1 fedpkg co
for i in */ ; do
    [ -e $i/dead.package ] && continue
    pushd $i
    rpmdev-bumpspec -c "- ABI rebuild" *.spec
    fedpkg commit -c -p && fedpkg build --nowait
    popd
done

popd



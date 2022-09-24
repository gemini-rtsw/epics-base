#!/bin/sh

set -x

## fetch submodules (not needed for submoduleAwareBuilder from tito
#git submodule init
#git submodule update

# create a temporary copy of epics-base submodule to apply config and patches
cp -r vendor/epics-base tmp
cp configure/CONFIG_SITE.local tmp/configure/

pushd tmp

# apply patches
patch -p1 < ../0001-rtems-Close-NTP-socket.patch
patch -p1 < ../v4-0001-rtems-Provide-an-NTP-version-of-osdTime-for-POSIX.patch
patch -p1 < ../v4-0002-rtems-Check-NTP-env-variable-each-NTP-get-if-set-.patch
make distclean uninstall all

popd
rm -rf tmp

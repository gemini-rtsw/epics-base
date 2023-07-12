%define _prefix /gem_base/epics
%define gemopt opt
%define name epics-base
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1) 

# These defines need to be adjusted to point to the git ref
# that is to be built

# vendor/upstream git project
## For now (until merged into upstream) use Chris Johns' repo for added ntpd functionality
## %%define vendor_project https://github.com/epics-base/epics-base.git
%define vendor_project https://github.com/kiwichris/epics-base.git
# vendor git ref (tag or commit hash). Please keep in sync with 'Version' below!
%define vendor_ref 683da46ed

#These global defines are added to prevent stripping
# symbols on vxWorks cross-compiled code
# Getting 'strip' to work is probably only needed for
# building a related debug sub-package
#
# But this prevents all the strip warnings
# mrippa 20120202
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

# some binaries are consideed to have missing build-ids and the build would
# be terminated if not ignoring that problem
# fkraemer 20220927
%global _missing_build_ids_terminate_build 0

#%%global epics_prefix %%{_prefix}/lib/epics
%global epics_prefix %{_prefix}/%{name}

Name: %{name}
Version: 7.0.7
Release: 0
URL: https://epics.anl.gov/
Summary: The Experimental Physics and Industrial Control Systems
License: EPICS Open License
Group: Applications/Engineering
Source0: %{name}-%{version}.tar.gz

BuildRequires: re2c readline-devel ncurses-devel perl rtems gemini-ade
Requires: readline perl
Provides: perl(EPICS::Release) perl(EPICS::Copy) perl(EPICS::Path)

%description
EPICS is a set of Open Source software tools, libraries and applications developed collaboratively and used worldwide to create distributed soft real-time control systems for scientific instruments such as a particle accelerators, telescopes and other large scientific experiments.


%package devel
Requires: epics-base%{?_isa} == %{version}-%{release}
Requires: epics-base rtems re2c readline-devel perl gemini-ade
Group: Development/Libraries
Summary: Files needed to develop new EPICS applications
# some perl modules are missing a package declaration
%description devel
The Experimental Physics and Industrial Control System is a collection of
tools, libraries and applications for creating a distributed soft real-time
control systems.

Libraries, headers, and utilities needed to develop applications
targeted to the host system.

%prep
%autosetup

%build
# the epics makefiles don't have seperate build and install phase.
git clone --recurse-submodules %{vendor_project} vendor_project
cd vendor_project
git checkout %{vendor_ref}
git submodule update --init --recursive

# apply Gemini-specific configuration
cp ../configure/CONFIG_SITE.local configure/

## apply Chris' rtems6 compatibility patch from epics-base PR 375
#git config user.email "user@email.com"
#git config user.name "User Name"
#git am ../upstream-375.patch
# apply patches
git apply ../1000ms_per_tick.patch
#git apply ../0001-rtems-Close-NTP-socket.patch
#git apply ../v4-0001-rtems-Provide-an-NTP-version-of-osdTime-for-POSIX.patch
#git apply ../v4-0002-rtems-Check-NTP-env-variable-each-NTP-get-if-set-.patch

%install
# cd into the directory containing the vendor sources
cd vendor_project

# copy over Gemini-specific configuration file(s)
# cp /gem_base/usr/share/epics/epics-base/configure/CONFIG_SITE.local.RTEMS5 %{_builddir}/%{?buildsubdir}/configure/CONFIG_SITE.local
# don't actually need to export $EPICS_HOST_ARCH, but do so to ensure consistency
export EPICS_HOST_ARCH=`%{_builddir}/%{?buildsubdir}/vendor_project/startup/EpicsHostArch`
# we will disable -rpath, but need code generators (antelope/flex/msi) to work
# during the build.
export LD_LIBRARY_PATH=%{buildroot}%{epics_prefix}/lib/${EPICS_HOST_ARCH}

# find-debuginfo.sh needs binaries under %{buildroot} to be writable.
# /usr/lib/rpm/fileattrs/elf.attr requires that that all ELF files be executable,
# even shared libraries which don't otherwise need to be.
# (debug auto dep. generation with semi-documented 'rpmbuild –rpmfcdebug')
make -C "%{_builddir}/%{?buildsubdir}/vendor_project" \
LINKER_USE_RPATH=NO \
SHRLIB_VERSION=%{version} \
INSTALL_LOCATION="%{buildroot}%{epics_prefix}" \
FINAL_LOCATION=%{epics_prefix} \
BIN_PERMISSIONS=755 \
LIB_PERMISSIONS=644 \
SHRLIB_PERMISSIONS=755

# remove builtroot from various
sed -i -e 's|%{buildroot}||g' \
 %{buildroot}%{epics_prefix}/bin/*/caRepeater.service \
 %{buildroot}%{epics_prefix}/lib/pkgconfig/*.pc

# inject our prefix in case it is different from the patched default
sed -i -e 's|/usr/lib/epics|%{epics_prefix}|g' %{buildroot}%{epics_prefix}/bin/*/makeBase*

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{epics_prefix}/lib/linux-x86_64" >  %{buildroot}/etc/ld.so.conf.d/epics-base.so.conf

cp -r startup %{buildroot}%{epics_prefix}/

# %{_builddir} is still included in several generated files
# in inconsquential places.  eg. bldTop in softIoc_registerRecordDeviceDriver.cpp
# rather than patching/stripping this all out, disable the check.
# Would be nice if this were more granular...
export QA_SKIP_BUILD_ROOT=1

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{epics_prefix}
%{epics_prefix}/bin
%{epics_prefix}/startup
%{epics_prefix}/dbd
%{epics_prefix}/db
%{epics_prefix}/lib
%{epics_prefix}/html
/etc/ld.so.conf.d/epics-base.so.conf

%files devel
%defattr(-,root,root)
%{epics_prefix}/include
%{epics_prefix}/templates
%{epics_prefix}/cfg
%config %{epics_prefix}/configure



%changelog

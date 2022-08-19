%define _prefix /gem_base/epics
%define gemopt opt
%define name epics-base
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1) 

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

#%%global epics_prefix %%{_prefix}/lib/epics
%global epics_prefix %{_prefix}/%{name}

Name: %{name}
Version: 7.0.6.1
Release: 5
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
cd vendor/epics-base
cp ../../configure/CONFIG_SITE.local configure/
git apply ../../0001-rtems-Close-NTP-socket.patch
git apply ../../v2-0001-rtems-Provide-an-NTP-version-of-osdTime-for-POSIX.patch
git apply ../../v2-0002-rtems-Check-NTP-env-variable-each-NTP-get-if-set-.patch

%build
# the epics makefiles don't have seperate build and install phase.

%install
# copy over Gemini-specific configuration file(s)
# cp /gem_base/usr/share/epics/epics-base/configure/CONFIG_SITE.local.RTEMS5 %{_builddir}/%{?buildsubdir}/configure/CONFIG_SITE.local
# don't actually need to export $EPICS_HOST_ARCH, but do so to ensure consistency
export EPICS_HOST_ARCH=`%{_builddir}/%{?buildsubdir}/vendor/epics-base/startup/EpicsHostArch`
# we will disable -rpath, but need code generators (antelope/flex/msi) to work
# during the build.
export LD_LIBRARY_PATH=%{buildroot}%{epics_prefix}/lib/${EPICS_HOST_ARCH}

# find-debuginfo.sh needs binaries under %{buildroot} to be writable.
# /usr/lib/rpm/fileattrs/elf.attr requires that that all ELF files be executable,
# even shared libraries which don't otherwise need to be.
# (debug auto dep. generation with semi-documented 'rpmbuild –rpmfcdebug')
make -C "%{_builddir}/%{?buildsubdir}/vendor/epics-base" \
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
* Thu Aug 18 2022 fkraemer <fkraemer@gemini.edu> 7.0.6.1-5
- new package built with tito

* Thu Mar 17 2022 matt.rippa@noirlab.edu
- tito tag 7.0.6.1-4
- 98717feda - (13 days ago) quiet warnings - Michael Davidsaver (HEAD -> unstable/2022q1, upstream7-gh)
- See https://gitlab.com/nsf-noirlab/gemini/rtsw/epics-base/epics-base/-/issues/18
- [mrippa@hbfswgade-lv1 epics-base]$ git lg --topo-order stable/2021q4^..unstable/2022q1

* Thu Mar 17 2022 matt.rippa@noirlab.edu
- 98717feda - (13 days ago) quiet warnings - Michael Davidsaver (HEAD -> unstable/2022q1, upstream7-gh)
- See https://gitlab.com/nsf-noirlab/gemini/rtsw/epics-base/epics-base/-/issues/18
- [mrippa@hbfswgade-lv1 epics-base]$ git lg --topo-order stable/2021q4^..unstable/2022q1
- tito tag 7.0.6.1-4 

* Thu Mar 17 2022 matt.rippa@noirlab.edu
- 98717feda - (13 days ago) quiet warnings - Michael Davidsaver (HEAD -> unstable/2022q1, upstream7-gh)
- tito tag 7.0.6.1-4 unstable/2022q1
- Squishing comments: See https://gitlab.com/nsf-noirlab/gemini/rtsw/epics-base/epics-base/-/issues/18
- $ git lg --topo-order stable/2021q4^..unstable/2022q1

* Wed Oct 27 2021 fkraemer <fkraemer@gemini.edu> 7.0.6.1-1
- new package built with tito

* Mon Jul 26 2021 Matt Rippa <mrippa@gemini.edu> 7.0.6-2
- Changes name from rtems5 to rtems. We need name:rtems Version:5 Release:1
- Automatic commit of package [epics-base] minor release [7.0.6-1].

* Fri Jul 23 2021 Matt Rippa <mrippa@gemini.edu> 7.0.6-1
- Gemini Test Release of EPICS 7.0.6

* Wed May 05 2021 fkraemer <fkraemer@gemini.edu> 7.0.5-8
- changed specfile with influences from mdavidasver switch off smp compilation
- applied changes to Containerfile because of renaming of gem-rtsw-repos
- updated gem-rtsw-repo submodule to newest hash

* Wed May 05 2021 fkraemer <fkraemer@gemini.edu>
- changed specfile with influences from mdavidasver switch off smp compilation
- applied changes to Containerfile because of renaming of gem-rtsw-repos
- updated gem-rtsw-repo submodule to newest hash

* Wed May 05 2021 fkraemer <fkraemer@gemini.edu>
- changed specfile with influences from mdavidasver switch off smp compilation
- applied changes to Containerfile because of renaming of gem-rtsw-repos
- updated gem-rtsw-repo submodule to newest hash

* Thu Apr 15 2021 Felix Kraemer <fkraemer@gemini.edu> 7.0.5-5
- added gemini-ade dependency for BuildRequires tag in specfile and for
  Requires tag in devel in specfile after fixing dependency chain at lower
  level in tdct
- Update to gem-rtsw-repo submodule for rtems4-epics7
* Fri Apr 09 2021 Felix Kraemer <fkraemer@gemini.edu> 7.0.5-4
- renamed testing-targets to testing-target-repositories
- added language pack to containerfile
- merged UPSTREAM-7.0
* Wed Mar 31 2021 Felix Kraemer <fkraemer@gemini.edu> 7.0.5-3
- removed gemini-ade dependency because of conflicting requests

* Wed Mar 31 2021 Felix Kraemer <fkraemer@gemini.edu> 7.0.5-2
- added gem-rtsw-repo as submodule 
- created Containerfile for creating epics-
  base docker image

* Mon Mar 29 2021 Felix Kraemer <fkraemer@gemini.edu> 7.0.5-1
- new package built with tito


%define _prefix /gem_base/epics
%define gemopt opt
%define version 3.15.8
%define name epics-base
%define release 1
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

Summary: Experimental Physics and Industrial Control System
Name: %{name}
Version: %{version}
Release: %release.%(date +"%Y%m%d")%{checkout}%{?dist}
License: EPICS Open License
Group: Applications/Engineering
Source0: %{name}-%{version}.tar.gz
ExclusiveArch: %{arch}
Prefix: %{_prefix}
BuildRequires: readline-devel perl rtems
Requires: readline perl


## Switch dependency checking off
# AutoReqProv: no
#
# The build creates lib???.so.3.14 and these are "autoprovided" instead of the following:
#
Provides: libCom.so = %{version}-%{release}
Provides: libasIoc.so = %{version}-%{release}
Provides: libasHost.so = %{version}-%{release}
Provides: libca.so = %{version}-%{release}
Provides: libcas.so = %{version}-%{release}
Provides: libdbIoc.so = %{version}-%{release}
Provides: libdbStaticHost.so = %{version}-%{release}
Provides: libdbStaticIoc.so = %{version}-%{release}
Provides: libdbtoolsIoc.so = %{version}-%{release}
Provides: libgdd.so = %{version}-%{release}
Provides: libiocshHost.so = %{version}-%{release}
Provides: libmiscIoc.so = %{version}-%{release}
Provides: librecIoc.so = %{version}-%{release}
Provides: libregistryIoc.so = %{version}-%{release}
Provides: librsrvIoc.so = %{version}-%{release}
Provides: libsoftDevIoc.so = %{version}-%{release}
Provides: perl(EPICS::Copy) = %{version}-%{release}
Provides: perl(EPICS::Release) = %{version}-%{release}
Provides: perl(EPICS::Path) = %{version}-%{release}

%description
EPICS is a set of Open Source software tools, libraries and applications developed collaboratively and used worldwide to create distributed soft real-time control systems for scientific instruments such as a particle accelerators, telescopes and other large scientific experiments.

%package devel
Summary: Experimental Physics and Industrial Control System
Requires: epics-base rtems
%description devel
EPICS is a set of Open Source software tools, libraries and applications developed collaboratively and used worldwide to create distributed soft real-time control systems for scientific instruments such as a particle accelerators, telescopes and other large scientific experiments.

%prep
%setup -q

%build

export EPICS_HOST_ARCH=`startup/EpicsHostArch`
make distclean uninstall
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{name}
#mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{name}/etc/profile.d
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
cp -r bin $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r startup $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r db $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r dbd $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r lib $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r include $RPM_BUILD_ROOT/%{_prefix}/%{name}

cp -r templates $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r configure $RPM_BUILD_ROOT/%{_prefix}/%{name}
echo "%{_prefix}/%{name}/lib/linux-x86_64" >  $RPM_BUILD_ROOT/etc/ld.so.conf.d/epics-base.so.conf
chmod -R u+w $RPM_BUILD_ROOT/%{_prefix}/%{name}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
## Usually you won't do much more here than
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /%{_prefix}/%{name}
   /%{_prefix}/%{name}/bin
   /%{_prefix}/%{name}/startup
   /%{_prefix}/%{name}/db
   /%{_prefix}/%{name}/dbd
   /%{_prefix}/%{name}/lib
   /etc/ld.so.conf.d/epics-base.so.conf

%files devel
%defattr(-,root,root)
   /%{_prefix}/%{name}/include
   /%{_prefix}/%{name}/templates
%config /%{_prefix}/%{name}/configure


%changelog
* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.202007222ecfcdd64
- finally the right Release tag (fkraemer@gemini.edu)
- fix deps (fkraemer@gemini.edu)
- added rtems-4.10.2 dep (fkraemer@gemini.edu)

* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200722.git6ae39e58d
- fix in specfile (fkraemer@gemini.edu)

* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200722.gitb27bf85d1
- bugfix (fkraemer@gemini.edu)

* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200722.git94b626ef8
- readded git hash to Release tag in specfile (fkraemer@gemini.edu)
- changed epics-base.ld.so.conf to be located in /etc/ld.so.conf.d and
  explixitly set dir to linux-x86_64 (fkraemer@gemini.edu)

* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu>
- changed epics-base.ld.so.conf to be located in /etc/ld.so.conf.d and
  explixitly set dir to linux-x86_64 (fkraemer@gemini.edu)

* Wed Jul 22 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200722
- new package built with tito

* Tue Jul 21 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200721
- changed Release string (fkraemer@gemini.edu)

* Sun Jul 19 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200719gitc736b9bd4
- added perl build requirement (fkraemer@gemini.edu)

* Sun Jul 19 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200719git8fbeba17f
- changed .tito/releasers conf to bootstrap from centos8:RTEMS container
  (fkraemer@gemini.edu)

* Sun Jul 19 2020 fkraemer <fkraemer@gemini.edu> 3.15.8-1.20200719gitca0ccc042
- changed .tito/releasers.conf to bootstrap from Gemini centos8:RTEMS container

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1
- 

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200713git964f16799
- Updated the ldconfig in %%post (mrippa@gemini.edu)

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200713git01bc58e88
- new package built with tito

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200713gite6c54efde
- new package built with tito

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200713git4eed08d10
- 

* Mon Jul 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200713git35ecf453f
- Update epics install path to /gem_base/epics-base (mrippa@gemini.edu)

* Sat Jul 11 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200711gitdee16331e
- Added epics-base.so.conf to package (mrippa@gemini.edu)

* Fri Jul 10 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200710gitb02b23b3f
- Disabled INSTALL_LOCATION for rpm build (mrippa@gemini.edu)

* Fri Jul 10 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200710gitc6dcfdf2c
- Build test cleaning up specfile

* Fri Jul 10 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200710git2670d8368
- New build test 

* Fri Jul 10 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200710git8bc35e5db
- Update for gitlab import (mrippa@gemini.edu)

* Sat Jun 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200613gitbfa061ec0
- updated tagger to use release instead of version bump. (mrippa@gemini.edu)

* Sat Jun 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200613git79d7df326
- 

* Sat Jun 13 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-1.20200613git676343fb4
- new package built with tito

## Write changes here, e.g.
 * Fri Mar 2 2012 Mathew Rippa <mrippa@gemini.edu> 3.14.12.1-0
 - r3.14.12.1, rpmlint compliant
 * Fri Feb 4 2011 Matthieu Bec <mbec@gemini.edu> 3.14.12
 - r3.14.12, i686/x86_64 compatible spec file
 * Mon Feb 11 2008 Felix Kraemer <fkraemer@gemini.edu> 3.14.9-8
 - Changed EPICS to point to /gemini/opt/epics
 * Wed Dec 19 2007 Felix Kraemer <fkraemer@gemini.edu> 3.14.9-8
 - added templates to be installed in devel
 * Fri Dec 7 2007 Felix Kraemer <fkraemer@gemini.edu> 3.14.9-7
 - Organize epics under opt
 * Thu Dec 6 2007 Felix Kraemer <fkraemer@gemini.edu> 3.14.9-6
 - Initial release

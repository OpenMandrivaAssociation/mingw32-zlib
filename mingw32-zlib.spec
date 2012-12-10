%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-zlib
Version:        1.2.3
Release:        %mkrel 3
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Other
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch

# From Fedora native package, none is applicable to us.
#Patch3:        zlib-1.2.3-autotools.patch
#Patch4:        minizip-1.2.3-autotools.patch
#Patch5:        zlib-1.2.3-minizip.patch

# MinGW-specific patches.
Patch100:       zlib-win32.patch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
MinGW Windows zlib compression library.


%prep
%setup -q -n zlib-1.2.3

%patch100 -p1


%build
CC=%{_mingw32_cc} \
CFLAGS="%{_mingw32_cflags}" \
RANLIB=%{_mingw32_ranlib} \
./configure

make -f win32/Makefile.gcc \
  CFLAGS="%{_mingw32_cflags}" \
  CC=%{_mingw32_cc} \
  AR=%{_mingw32_ar} \
  RC=i586-pc-mingw32-windres \
  DLLWRAP=i586-pc-mingw32-dllwrap \
  STRIP=%{_mingw32_strip} \
  all


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}

make -f win32/Makefile.gcc \
     INCLUDE_PATH=$RPM_BUILD_ROOT%{_mingw32_includedir} \
     LIBRARY_PATH=$RPM_BUILD_ROOT%{_mingw32_libdir} \
     BINARY_PATH=$RPM_BUILD_ROOT%{_mingw32_bindir} \
     install

# .dll.a file is misnamed for some reason - fix that.
mv $RPM_BUILD_ROOT%{_mingw32_libdir}/libzdll.a \
   $RPM_BUILD_ROOT%{_mingw32_libdir}/libz.dll.a

# Remove static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libz.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_includedir}/zconf.h
%{_mingw32_includedir}/zlib.h
%{_mingw32_libdir}/libz.dll.a
%{_mingw32_bindir}/zlib1.dll


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-3mdv2011.0
+ Revision: 620363
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.2.3-2mdv2010.0
+ Revision: 439984
- rebuild

* Fri Feb 06 2009 Jérôme Soyer <saispo@mandriva.org> 1.2.3-1mdv2009.1
+ Revision: 338187
- Fix compiler
- import mingw32-zlib



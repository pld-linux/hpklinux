#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

Summary:	Linux HPI driver for AudioScience audio adapters
Summary(pl.UTF-8):	Linuksowy sterownik HPI do kart dźwiękowych AudioScience
Name:		hpklinux
Version:	4.20.43
Release:	1
License:	GPL v2
Group:		Applications/Sound
#Source0Download: http://www.audioscience.com/internet/download/linux_drivers.htm
Source0:	http://www.audioscience.com/internet/download/drivers/released/v4/20/43/%{name}_%{version}.tar.gz
# Source0-md5:	b039b650d7c424d311ec0889a293ec86
Patch0:		%{name}-opt.patch
URL:		http://www.audioscience.com/internet/download/linux_drivers.htm
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:1.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux HPI driver for AudioScience audio adapters.

This package contains userspace utilities.

%description -l pl.UTF-8
Linuksowy sterownik HPI do kart dźwiękowych AudioScience.

Ten pakiet zawiera narzędzia przestrzeni użytkownika.

%package libs
Summary:	HPI library for AudioScience audio adapters
Summary(pl.UTF-8):	Biblioteka HPI do kart dźwiękowych AudioScience
Group:		Libraries

%description libs
HPI library for AudioScience audio adapters.

%description libs -l pl.UTF-8
Biblioteka HPI do kart dźwiękowych AudioScience.

%package devel
Summary:	Header files for HPI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HPI
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for HPI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HPI.

%package static
Summary:	Static HPI library
Summary(pl.UTF-8):	Statyczna biblioteka HPI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HPI library.

%description static -l pl.UTF-8
Statyczna biblioteka HPI.

%package -n python-hpi
Summary:	Python Linux HPI library
Summary(pl.UTF-8):	Biblioteka Linux HPI dla Pythona
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-hpi
Python Linux HPI library.

%description -n python-hpi -l pl.UTF-8
Biblioteka Linux HPI dla Pythona.

%package -n python3-hpi
Summary:	Python Linux HPI library
Summary(pl.UTF-8):	Biblioteka Linux HPI dla Pythona
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-hpi
Python Linux HPI library.

%description -n python3-hpi -l pl.UTF-8
Biblioteka Linux HPI dla Pythona.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} -C hpi-lib \
	CC="%{__cc}"

CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} -C hpi-cli-apps \
	CC="%{__cc}"

cd asi-python

%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C hpi-lib install \
	DESTDIR=$RPM_BUILD_ROOT \
	include-install-dir=%{_includedir}/asihpi \
	lib-install-dir=%{_libdir}

%{__make} -C hpi-cli-apps install \
	DESTDIR=$RPM_BUILD_ROOT \
	bin-install-dir=%{_bindir}

%{__make} -C hpi-drv/firmware \
	bin-install-base-path=$RPM_BUILD_ROOT/lib/firmware

cd asi-python

%if %{with python2}
%py_install

%py_postclean
# package only py3 variant
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.py
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/asi_firmware_updater
%attr(755,root,root) %{_bindir}/asihpi*
/lib/firmware/asihpi

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpi.so.10
%attr(755,root,root) %{_libdir}/libhpimux.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpimux.so.10
%attr(755,root,root) %{_libdir}/libhpiudp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpiudp.so.10

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpi.so
%attr(755,root,root) %{_libdir}/libhpimux.so
%attr(755,root,root) %{_libdir}/libhpiudp.so
%{_includedir}/asihpi

%files static
%defattr(644,root,root,755)
%{_libdir}/libhpi.a
%{_libdir}/libhpimux.a
%{_libdir}/libhpiudp.a

%if %{with python2}
%files -n python-hpi
%defattr(644,root,root,755)
%{py_sitescriptdir}/audioscience
%{py_sitescriptdir}/hpi-2.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-hpi
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dab_data.py
%attr(755,root,root) %{_bindir}/dabtest.py
%attr(755,root,root) %{_bindir}/hpicontrol.py
%attr(755,root,root) %{_bindir}/hpimixer.py
%attr(755,root,root) %{_bindir}/hpisave.py
%{py3_sitescriptdir}/audioscience
%{py3_sitescriptdir}/hpi-2.0-py*.egg-info
%endif

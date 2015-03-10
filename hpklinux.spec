Summary:	Linux HPI driver for AudioScience audio adapters
Summary(pl.UTF-8):	Linuksowy sterownik HPI do kart dźwiękowych AudioScience
Name:		hpklinux
Version:	4.06.03
Release:	2
License:	GPL v2
Group:		Applications/Sound
#Source0Download: http://www.audioscience.com/internet/download/linux_drivers.htm
Source0:	http://audioscience.com/internet/download/drivers/released/v4/06/03/%{name}-%{version}.tar.bz2
# Source0-md5:	18b4f3864cdecec5c17ec222ee17f2c7
Patch0:		x32.patch
URL:		http://www.audioscience.com/internet/download/linux_drivers.htm
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-kernel-compile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.hpi drvnotes.txt
%attr(755,root,root) %{_bindir}/asi_firmware_updater
%attr(755,root,root) %{_bindir}/asihpi*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpi.so.9
%attr(755,root,root) %{_libdir}/libhpimux.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpimux.so.9
%attr(755,root,root) %{_libdir}/libhpiudp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhpiudp.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhpi.so
%attr(755,root,root) %{_libdir}/libhpimux.so
%attr(755,root,root) %{_libdir}/libhpiudp.so
%{_libdir}/libhpi.la
%{_libdir}/libhpimux.la
%{_libdir}/libhpiudp.la
%{_includedir}/asihpi

%files static
%defattr(644,root,root,755)
%{_libdir}/libhpi.a
%{_libdir}/libhpimux.a
%{_libdir}/libhpiudp.a

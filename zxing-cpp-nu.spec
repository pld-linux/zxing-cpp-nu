# note: older fork in zxing-cpp.spec (both are parallel-installable)
Summary:	C++ port of ZXing - 1D/2D barcode image processing library
Summary(pl.UTF-8):	Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D
Name:		zxing-cpp-nu
Version:	1.2.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/nu-book/zxing-cpp/releases
Source0:	https://github.com/nu-book/zxing-cpp/archive/v%{version}/zxing-cpp-%{version}.tar.gz
# Source0-md5:	b7265963a766dfc87b60d57e41c56917
URL:		https://github.com/nu-book/zxing-cpp
BuildRequires:	cmake >= 3.10
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ port of ZXing - 1D/2D barcode image processing library.

%description -l pl.UTF-8
Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D

%package devel
Summary:	Header files for ZXing library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ZXing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for ZXing library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ZXing.

%prep
%setup -q -n zxing-cpp-%{version}

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.ZXing NOTICE README.md
%attr(755,root,root) %{_libdir}/libZXing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libZXing.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libZXing.so
%{_includedir}/ZXing
%{_pkgconfigdir}/zxing.pc
%{_libdir}/cmake/ZXing

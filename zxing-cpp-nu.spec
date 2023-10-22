# note: older fork in zxing-cpp.spec (both are parallel-installable)
#
# Conditional build:
%bcond_without	python3	# CPython 3.x module

Summary:	C++ port of ZXing - 1D/2D barcode image processing library
Summary(pl.UTF-8):	Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D
Name:		zxing-cpp-nu
Version:	2.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/nu-book/zxing-cpp/releases
Source0:	https://github.com/nu-book/zxing-cpp/archive/v%{version}/zxing-cpp-%{version}.tar.gz
# Source0-md5:	17289e8cd489cda9d72b30f05e6f007d
URL:		https://github.com/nu-book/zxing-cpp
BuildRequires:	cmake >= 3.15
BuildRequires:	libstdc++-devel >= 6:7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-pybind11
%endif
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

%package -n python3-zxingcpp
Summary:	Python bindings for the zxing-cpp barcode library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki kodów paskowych zxing-cpp
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.6

%description -n python3-zxingcpp
Python bindings for the zxing-cpp barcode library.

%description -n python3-zxingcpp -l pl.UTF-8
Wiązania Pythona do biblioteki kodów paskowych zxing-cpp.

%prep
%setup -q -n zxing-cpp-%{version}

%build
%cmake -B build \
	-DBUILD_BLACKBOX_TESTS=OFF \
	-DBUILD_C_API=ON \
	-DBUILD_EXAMPLES=OFF \
	%{?with_python3:-DBUILD_PYTHON_MODULE=ON} \
	-DBUILD_UNIT_TESTS=OFF \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

# -DBUILD_C_API=ON (experimental now and not installed)

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python3}
install -d $RPM_BUILD_ROOT%{py3_sitedir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/zxingcpp.cpython-*.so $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libZXing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libZXing.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libZXing.so
%{_includedir}/ZXing
%{_pkgconfigdir}/zxing.pc
%{_libdir}/cmake/ZXing

%if %{with python3}
%files -n python3-zxingcpp
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/zxingcpp.cpython-*.so
%endif

Summary:        Google C++ testing framework
Name:           gtest
Version:        1.17.0
Release:        1
# scripts/generator/* are ASL 2.0
License:        BSD and ASL 2.0
URL:            https://github.com/sailfishos/gtest
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  python3-devel

%description
Framework for writing C++ tests on a variety of platforms (GNU/Linux,
Mac OS X, Windows, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%package     devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package     doc
Summary:        gtest documentation
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation files for %{name}.

%package     -n gmock
Summary:        Google C++ Mocking Framework
Requires:       %{name} = %{version}-%{release}

%description -n gmock
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:

 o lets you create mock classes trivially using simple macros,
 o supports a rich set of matchers and actions,
 o handles unordered, partially ordered, or completely ordered
   expectations,
 o is extensible by users, and
 o works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
   Symbian.

%package     -n gmock-devel
Summary:        Development files for libgmock
Requires:       gmock = %{version}-%{release}

%description -n gmock-devel
This package contains development files for libgmock.

%package     -n gmock-doc
Summary:        gtest documentation
Requires:       gmock = %{version}-%{release}

%description -n gmock-doc
Documentation files for libgmock.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%cmake -DBUILD_SHARED_LIBS=ON \
       -DPYTHON_EXECUTABLE=%{__python3}
%cmake_build

%install
%cmake_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n gmock -p /sbin/ldconfig
%postun -n gmock -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files devel
%{_includedir}/gtest/
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_libdir}/cmake/GTest/
%{_libdir}/pkgconfig/gtest.pc
%{_libdir}/pkgconfig/gtest_main.pc

%files doc
%doc googletest/{CHANGES,CONTRIBUTORS,README.md}
%doc googletest/docs/
%doc googletest/samples

%files -n gmock
%license LICENSE
%{_libdir}/libgmock.so.*
%{_libdir}/libgmock_main.so.*

%files -n gmock-devel
%{_includedir}/gmock/
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so
%{_libdir}/pkgconfig/gmock.pc
%{_libdir}/pkgconfig/gmock_main.pc

%files -n gmock-doc
%doc googlemock/{CHANGES,CONTRIBUTORS,README.md}
%doc googlemock/docs/

#
# spec file for package 
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           gtest
Version:        1.7.0
Release:        0
License:        GPL-2.0+
Summary:        Google C++ Testing Framework
Url:            https://code.google.com/p/googletest
Group:          Definition/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Patch0:         gtest-soname.patch

BuildRequires:  cmake
#BuildRequires:  gcc-c++
#BuildRequires:  unzip
BuildRequires:  python
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Google's framework for writing C++ tests on a variety of platforms (Linux, Mac
OS X, Windows, Cygwin, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of assertions,
user-defined assertions, death tests, fatal and non-fatal failures, value- and
type-parameterized tests, various options for running the tests, and XML test
report generation.

%package devel
Summary: Devel files for Google C++ testing framework
Group: Development/Libraries/C and C++
Requires: libgtest0 = %{version}
#BuildRequires: gcc-c++

%description devel
Google's framework for writing C++ tests on a variety of platforms (Linux, Mac
OS X, Windows, Cygwin, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of assertions,
user-defined assertions, death tests, fatal and non-fatal failures, value- and
type-parameterized tests, various options for running the tests, and XML test
report generation.

%package -n libgtest0
Summary: Google C++ testing framework
Group: Development/Libraries

%description -n libgtest0
Google's framework for writing C++ tests on a variety of platforms (Linux, Mac
OS X, Windows, Cygwin, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of assertions,
user-defined assertions, death tests, fatal and non-fatal failures, value- and
type-parameterized tests, various options for running the tests, and XML test
report generation.

%prep
%setup -q -n %{name}-%{version}/%{name}
%patch0 -p1

%build
# this is odd but needed only to generate gtest-config.
%configure
%cmake -DBUILD_SHARED_LIBS=ON \
       -DCMAKE_SKIP_BUILD_RPATH=TRUE \
       -DPYTHON_EXECUTABLE=%{__python2} \
       -Dgtest_build_tests=OFF

make %{?_smp_mflags}

#XXX: 13 tests are markede as failed but nmone of them run!
# % check
# LD_LIBRARY_PATH needed due to cmake_skip_rpath in %%build
#pushd build
#LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/build make test
#popd


%install

# make install doesn't work anymore.
# need to install them manually.
install -d %{buildroot}{%{_includedir}/gtest{,/internal},%{_libdir}}
# just for backward compatibility
install -p -m 0755 libgtest.so.*.* libgtest_main.so.*.* %{buildroot}%{_libdir}/
(cd %{buildroot}%{_libdir};
ln -sf libgtest.so.*.* %{buildroot}%{_libdir}/libgtest.so
ln -sf libgtest_main.so.*.* %{buildroot}%{_libdir}/libgtest_main.so
)
/sbin/ldconfig -n %{buildroot}%{_libdir}
install -D -p -m 0755 scripts/gtest-config %{buildroot}%{_bindir}/gtest-config
install -p -m 0644 include/gtest/*.h %{buildroot}%{_includedir}/gtest/
install -p -m 0644 include/gtest/internal/*.h %{buildroot}%{_includedir}/gtest/internal/
install -D -p -m 0644 m4/gtest.m4 %{buildroot}%{_datadir}/aclocal/gtest.m4

%post -n libgtest0 -p /sbin/ldconfig
%postun -n libgtest0 -p /sbin/ldconfig

%files -n libgtest0
%defattr(-,root,root)
%doc LICENSE
%{_libdir}/libgtest_main.so.0
%{_libdir}/libgtest_main.so.0.0.0
%{_libdir}/libgtest.so.0
%{_libdir}/libgtest.so.0.0.0

%files devel
%defattr(-,root,root,0755)
%dir %{_datadir}/aclocal
%{_includedir}/gtest/
%{_bindir}/gtest-config
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_datadir}/aclocal/gtest.m4


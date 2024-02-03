#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		kirigami
Summary:	Kirigami library
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	37a68cbd30a22d81012178cc1cc8666e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	catdoc
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kirigami library.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang libkirigami6 --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f libkirigami6.lang
%defattr(644,root,root,755)
%{_libdir}/qt6/qml/org/kde/kirigami
%attr(755,root,root) %{_libdir}/libKirigami.so.*.*
%ghost %{_libdir}/libKirigami.so.6
%attr(755,root,root) %{_libdir}/libKirigamiDelegates.so.*.*
%ghost %{_libdir}/libKirigamiDelegates.so.6
%attr(755,root,root) %{_libdir}/libKirigamiPlatform.so.*.*
%ghost %{_libdir}/libKirigamiPlatform.so.6
%{_datadir}/qlogging-categories6/kirigami.categories


%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/Kirigami
%{_libdir}/cmake/KF6Kirigami
%{_libdir}/cmake/KF6Kirigami2
%{_libdir}/cmake/KF6KirigamiPlatform
%{_libdir}/libKirigami.so
%{_libdir}/libKirigamiDelegates.so
%{_libdir}/libKirigamiPlatform.so
%{_datadir}/kdevappwizard/templates/kirigami6.tar.bz2

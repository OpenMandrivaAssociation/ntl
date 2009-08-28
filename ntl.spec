# Correct problem the only way to get sage to not core on some tests is to run:
#	% LD_PRELOAD=/usr/lib/libntl.so.5.5.2:/usr/lib/libgmp.so.3.5.0 sage
%define	_disable_ld_as_needed 1

%define version	5.5.2
%define release	%mkrel 1

%define major	5
%define libname	%mklibname %name %{major}
%define develname %mklibname %name -d
%define sdevelname %mklibname %name -d -s

Summary:	Library for doing number theory
Name:		ntl
Version:	%{version}
Release:	%{release}
URL:		http://www.shoup.net/ntl/index.html
Source0:	http://www.shoup.net/ntl/%{name}-%{version}.tar.gz
License:	GPLv2+
Group:		System/Libraries
BuildRequires:	gmp-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
NTL is a high-performance, portable C++ library providing data structures and
algorithms for manipulating signed, arbitrary length integers, and for vectors,
matrices, and polynomials over the integers and over finite fields.

%package -n %{libname}
Summary:        Main library for NTL (Number Theory Library)
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the libraries needed to run programs dynamically linked
with NTL (Number Theory Library).

%package -n %{develname}
Group:		Development/C++
Summary:	Shared libraries and header files for NTL (Number Theory Library)
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname -d ntl 5

%description -n %{develname}
This package contains the shared libraries and header files needed for
developing NTL (Number Theory Library) applications.

%package -n %{sdevelname}
Group:		Development/C++
Summary:	Static libraries for NTL (Number Theory Library)
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}
Obsoletes:	%mklibname -d -s ntl 5

%description -n %{sdevelname}
This package contains the static libraries needed for developing NTL
(Number Theory Library) applications.

%prep
%setup -q

%build
cd src

CFLAGS=`echo %optflags | sed 's/-O[0-9]/-O1/'`
CXXFLAGS=`echo %optflags "-fno-rtti" | sed 's/-O[0-9]/-O1/'`

./configure \
PREFIX=%{_prefix} \
	LIBDIR=$(echo %{_libdir} | sed 's,^%{_prefix},$${PREFIX},') \
	INCLUDEDIR=$(echo %{_includedir} | sed 's,^%{_prefix},$${PREFIX},') \
	DOCDIR=$(echo %{_docdir} | sed 's,^%{_prefix},$${PREFIX},') \
	NTL_GMP_LIP=on \
	NTL_STD_CXX=on \
	CC="${CC-gcc}" CXX="${CXX-g++}" \
	CPPFLAGS="$CPPFLAGS" \
	CFLAGS="$CFLAGS" \
	CXXFLAGS="$CXXFLAGS"

LD_LIBRARY_PATH=. \
make \
	CPPFLAGS="$CPPFLAGS -DPIC" \
	CFLAGS="$CFLAGS -fPIC" \
	CXXFLAGS="$CXXFLAGS -fPIC" \
	AR='bash -e -c '\''out=$$1; lib=$$(basename $$out .a).so.%{major}; \
	lib=lib$${lib#lib}; set -x; rm -f $$lib; ${CXX} -shared -Wl,-soname,$$lib \
	-o "$$@"; ln -s $$out $$lib'\' \
	RANLIB=: \
	all check

rm -f libntl.so.%{major}
mv -f ntl.a libntl.so.%{version}
ln -sf libntl.so.%{version} libntl.so.%{major}

make clean ntl.a check

%install
rm -rf $RPM_BUILD_ROOT

cd src

make PREFIX=$RPM_BUILD_ROOT%{_prefix} install

install -m 755 libntl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libntl.so.%{version}
ln -sf libntl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libntl.so.%{major}
ln -sf libntl.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libntl.so

rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/NTL

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{libname}
%defattr(-,root,root)
%doc README
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*
%{_includedir}/*
%{_libdir}/*.so

%files -n %{sdevelname}
%defattr(-,root,root)
%{_libdir}/*.a

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

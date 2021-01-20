%define multilib_arches %{ix86} x86_64 ppc ppc64 s390 s390x sparcv9 sparc64
%define _disable_lto 1

%ifarch x86_64
%define __isa_bits	64
%else
%define __isa_bits	32
%endif

%define major	33
%define libname	%mklibname %name %{major}
%define develname %mklibname %name -d

# Epoch required due to downgrade of major
Epoch:   1
Summary: High-performance algorithms for vectors, matrices, and polynomials 
Name:    ntl 
Version: 11.4.3
Release: 1

License: GPLv2+
URL:     http://shoup.net/ntl/ 
Group:   System/Libraries

Source0: http://shoup.net/ntl/%{name}-%{version}.tar.gz
Source1: multilib_template.h

BuildRequires: gf2x-devel
BuildRequires: gmp-devel
BuildRequires: libtool

%description
NTL is a high-performance, portable C++ library providing data structures
and algorithms for arbitrary length integers; for vectors, matrices, and
polynomials over the integers and over finite fields; and for arbitrary
precision floating point arithmetic.

NTL provides high quality implementations of state-of-the-art algorithms for:
* arbitrary length integer arithmetic and arbitrary precision floating point
  arithmetic;
* polynomial arithmetic over the integers and finite fields including basic
  arithmetic, polynomial factorization, irreducibility testing, computation
  of minimal polynomials, traces, norms, and more;
* lattice basis reduction, including very robust and fast implementations of
  Schnorr-Euchner, block Korkin-Zolotarev reduction, and the new 
  Schnorr-Horner pruning heuristic for block Korkin-Zolotarev;
* basic linear algebra over the integers, finite fields, and arbitrary
  precision floating point numbers. 

%package -n %{libname}
Summary:	Main library for NTL (Number Theory Library)
Group:		System/Libraries
Provides:	%{name} = %{EVRD}

%description -n %{libname}
This package contains the libraries needed to run programs dynamically linked
with NTL (Number Theory Library).

%package -n %{develname}
Group:		Development/C++
Summary:	Shared libraries and header files for NTL (Number Theory Library)
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	gf2x-devel

%description -n %{develname}
This package contains the shared libraries and header files needed for
developing NTL (Number Theory Library) applications.

%prep
%setup -q

%build
export CC=gcc
export CXX=g++
pushd src
./configure \
  CXX="${CXX-g++}" \
  CXXFLAGS="`echo %optflags | sed 's/-O[0-9]/-O1/'` -fPIC" \
  PREFIX=%{_prefix} \
  DOCDIR=%{_docdir} \
  INCLUDEDIR=%{_includedir} \
  LIBDIR=%{_libdir} \
  NATIVE=off \
  NTL_GF2X_LIB=on \
  SHARED=on
popd

# not smp-safe
make -C src V=1

%install
make -C src install \
  PREFIX=%{buildroot}%{_prefix} \
  DOCDIR=%{buildroot}%{_docdir} \
  INCLUDEDIR=%{buildroot}%{_includedir} \
  LIBDIR=%{buildroot}%{_libdir} 

# Unpackaged files
rm -rfv %{buildroot}%{_docdir}/NTL
rm -fv  %{buildroot}%{_libdir}/libntl.la
rm -fv  %{buildroot}%{_libdir}/libntl.a

%ifarch %{multilib_arches}
# hack to allow parallel installation of multilib factory-devel
for header in NTL/config NTL/gmp_aux NTL/mach_desc  ; do
mv  %{buildroot}%{_includedir}/${header}.h \
    %{buildroot}%{_includedir}/${header}-%{__isa_bits}.h
install -p -m644 %{SOURCE1} %{buildroot}%{_includedir}/${header}.h
sed -i \
  -e "s|@@INCLUDE@@|${header}|" \
  -e "s|@@INCLUDE_MACRO@@|$(echo ${header} | tr '/.' '_')|" \
  %{buildroot}%{_includedir}/${header}.h
done
%endif

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc doc/*
%{_includedir}/*
%{_libdir}/*.so

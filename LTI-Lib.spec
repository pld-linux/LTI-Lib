#
# Conditional build:
%bcond_with	mmx
%bcond_with	sse
%bcond_with	3dnow
%bcond_without	gtk

Summary:	LTI-Lib - computer vision library.
Summary(pl):	LTI-Lib - biblioteka do komputerowego przetwarzania obrazów.
Name:		LTI-Lib
Version:	1.9.8
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/sourceforge/ltilib/031124_ltilib-%{version}.tar.bz2
# Source0-md5:	dfa6616f3dc5dae04e84311764181b96
Patch0:		%{name}-Makefile.patch
URL:		http://ltilib.sourceforge.net/doc/homepage/index.shtml
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	gcc-g77
BuildRequires:	graphviz
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	tetex-latex-bibtex
%if %{with gtk}
BuildRequires:	gtk+-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The LTI-Lib is an object oriented library with algorithms and data
structures frequently used in image processing and computer vision.

%description -l pl
LTI-Lib jest zorientowan± obiektowo bibliotek± zawieraj±c± najczê¶ciej
u¿ywane algorytmy i struktury danych w procesach przetwarzania
i analizy obrazów.

%package doc
Summary:	LTI-Lib - documentation
Summary(pl):	LTI-Lib - dokumentacja
Group:		Development/Libraries

%description doc
LTI-Lib documentation.

%description doc -l pl
Dokumentacja biblioteki LTI-Lib.

%prep
%setup -q -n ltilib
%patch0 -p1

%build
cd doc/styleguide/en
%{__make} pdf

cd ../../../linux
%{__aclocal}
%{__autoconf}
%{__autoheader}

%ifarch i386
    _ac_cpu="Generic i386"	; export _ac_cpu
    _ac_mmx="no"		; export _ac_mmx
    _ac_sse="no"		; export _ac_sse
    _ac_3dnow="no"		; export _ac_3dnow
%endif

%ifarch i486
    _ac_cpu="Generic i486"	; export _ac_cpu
    _ac_mmx="no"		; export _ac_mmx
    _ac_sse="no"		; export _ac_sse
    _ac_3dnow="no"		; export _ac_3dnow
%endif

%ifarch i586
    _ac_cpu="Generic Pentium"	; export _ac_cpu
    _ac_mmx="no"		; export _ac_mmx
    _ac_sse="no"		; export _ac_sse
    _ac_3dnow="no"		; export _ac_3dnow
%endif

%ifarch i686
    _ac_cpu="Generic i686"	; export _ac_cpu
    _ac_mmx="yes"		; export _ac_mmx
    _ac_sse="no"		; export _ac_sse
    _ac_3dnow="no"		; export _ac_3dnow
%endif

%ifarch athlon
    _ac_cpu="Generic Athlon"	; export _ac_cpu
    _ac_mmx="yes"		; export _ac_mmx
    _ac_sse="no"		; export _ac_sse
    _ac_3dnow="yes"		; export _ac_3dnow
%endif

%if %{with mmx}
    _ac_mmx="yes"		; export _ac_mmx
%endif

%if %{with sse}
    _ac_sse="yes"		; export _ac_sse
%endif

%if %{with 3dnow}
    _ac_3dnow="yes"		; export _ac_3dnow
%endif

%configure \
%if %{without gtk}
	--without-gtk \
%endif
	--disable-debug

%{__make} doxydoc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}-doc

cp doc/html/*.html	$RPM_BUILD_ROOT/%{_docdir}/%{name}-doc
cp doc/html/*.png	$RPM_BUILD_ROOT/%{_docdir}/%{name}-doc
cp doc/html/*.gif	$RPM_BUILD_ROOT/%{_docdir}/%{name}-doc

cd linux
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_prefix}/lib/ltilib
rm -f $RPM_BUILD_ROOT%{_includedir}/ltilib

cd $RPM_BUILD_ROOT%{_prefix}/lib
ln -s ltilib-%{version} ltilib
cd $RPM_BUILD_ROOT%{_includedir}
ln -s ltilib-%{version} ltilib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README doc/styleguide/en/*.pdf
%attr(755,root,root) %{_bindir}/*
%{_includedir}/ltilib
%{_includedir}/ltilib-%{version}/*
%{_libdir}/ltilib
%{_libdir}/ltilib-%{version}/*

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc

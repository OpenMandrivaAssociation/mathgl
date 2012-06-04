%define		mainlibmajor 5
%define		mainlibname %mklibname mgl %{mainlibmajor}
%define		fltklibmajor 5
%define		fltklibname %mklibname mgl-fltk %{fltklibmajor}
%define		glutlibmajor 5
%define		glutlibname %mklibname mgl-glut %{glutlibmajor}
%define		qtlibmajor 5
%define		qtlibname %mklibname mgl-qt %{qtlibmajor}
%define		wxlibmajor 5
%define		wxlibname %mklibname mgl-wx %{wxlibmajor}
%define		develname %mklibname mgl -d
%define		staticdevelname %mklibname mgl -d -s

%define		octave_api api-v37

# we need x.y.z format here
%define		pkgversion 1.11.1

Name:		mathgl
# 1.11.2 seems to be broken
Version:	1.11.1.1
Release:	%mkrel 2
Summary:	Library for scientific graphics
License:	GPLv2+
Group:		System/Libraries
Url:		http://mathgl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/mathgl/%{name}-%{version}.tar.gz
Patch0:		mathgl-1.10-mdv-fix-fltk-include-path.patch
Patch1:		mathgl-1.11.2-zlib.patch
Patch2:		mathgl-1.11.1.1-lz.patch
Patch3:		mathgl-1.11.1.1-oct.patch
Patch4:		mathgl-1.11.1.1-gz.patch
BuildRequires:	qt4-devel
BuildRequires:	gsl-devel
BuildRequires:	GL-devel
%if %{mdvver} <= 201100
BuildRequires:	mesaglut-devel
%else
BuildRequires:	freeglut-devel
%endif
BuildRequires:	fltk-devel
BuildRequires:	hdf5-devel
BuildRequires:	wxgtku-devel
BuildRequires:	octave-devel
BuildRequires:	swig >= 1:2.0
BuildRequires:	libjpeg-devel
BuildRequires:	giflib-devel
BuildRequires:	texinfo
BuildRequires:	texi2html

%description
MathGL is a library for making high-quality scientific graphics. It
provides fast data plotting and handling of large data arrays.
MathGL has Qt, FLTK, OpenGL interfaces and can be used even from
console programs.

%package tools
Summary:	Tools for MathGL
Group:		Sciences/Mathematics

%description tools
This package contains the MathGL tools.

%package examples
Summary:	Examples for MathGL
Group:		Sciences/Mathematics

%description examples
This package contains the MathGL examples.

%package data
Summary:	Data files for MathGL
Group:		Sciences/Mathematics

%description data
This package contains the MathGL data files.

%package octave
Summary:	MathGL bindings for octave
Group:		Sciences/Mathematics
Requires(post):	octave(api) = %{octave_api}
Requires(postun): octave(api) = %{octave_api}
Requires:	octave(api) = %{octave_api}

%description octave
This package contains the MathGL bindings for octave.

%package doc
Summary:	Documentation for MathGL
Group:		Sciences/Mathematics
%if %{mdvver} <= 201100
Requires(post):	info-install
Requires(preun): info-install
%endif

%description doc
This package contains the MathGL documentation.

%package -n %{mainlibname}
Summary:	Main runtime library for MathGL
Group:		System/Libraries
Requires:	%{name}-data = %{version}

%description -n %{mainlibname}
MathGL is a library for making high-quality scientific graphics. It
provides fast data plotting and handling of large data arrays.
MathGL has Qt, FLTK, OpenGL interfaces and can be used even from
console programs.

This package contains the MathGL main runtime library.

%package -n %{fltklibname}
Summary:	Fltk runtime library for MathGL
Group:		System/Libraries

%description -n %{fltklibname}
This package contains the MathGL fltk runtime library.

%package -n %{glutlibname}
Summary:	Glut runtime library for MathGL
Group:		System/Libraries

%description -n %{glutlibname}
This package contains the MathGL glut runtime library.

%package -n %{qtlibname}
Summary:	Qt runtime library for MathGL
Group:		System/Libraries

%description -n %{qtlibname}
This package contains the MathGL Qt runtime library.

%package -n %{wxlibname}
Summary:	WxWidgets runtime library for MathGL
Group:		System/Libraries

%description -n %{wxlibname}
This package contains the MathGL wxWidgets runtime library.

%package -n %{develname}
Summary:	Development files for MathGL
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{mainlibname} = %{version}
Requires:	%{fltklibname} = %{version}
Requires:	%{glutlibname} = %{version}
Requires:	%{qtlibname} = %{version}
Requires:	%{wxlibname} = %{version}

%description -n %{develname}
This package contains the MathGL development files.

%package -n %{staticdevelname}
Summary:	Static development files for MathGL
Group:		Development/Other
Requires:	%{develname} = %{version}

%description -n %{staticdevelname}
This package contains the MathGL static development files.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

# fix EOL
for i in AUTHORS COPYRIGHT README
do
  sed -i 's/\r//' $i
done

%build
autoreconf
%configure2_5x \
	--enable-double \
	--enable-pthread \
	--enable-gsl \
	--enable-glut \
	--enable-hdf5 \
	--enable-hdf5_18 \
	--enable-gif \
	--enable-jpeg \
	--enable-fltk \
	--enable-wx \
	--enable-qt \
	--enable-octave \
	--enable-testio \
	--enable-docs
%make

%install
%__rm -rf %{buildroot}
%makeinstall

######################################################################
# octave .oct file fix and install                                   #
# from Fedora specfile                                               #
######################################################################
%__mkdir_p temp-octave

pushd .
cd temp-octave
#Decompress tarballed "oct" file and remove tarball
tar -zxf %{buildroot}/%{_datadir}/%{name}/octave/%{name}.tar.gz
%__rm %{buildroot}/%{_datadir}/%{name}/octave/%{name}.tar.gz

#Copy the .oct file and supporting files to octave packages dir
%__mkdir_p %{buildroot}/%{_libexecdir}/octave/packages/%{name}-%{pkgversion}/
#Remove empty INDEX file
%__rm %{name}/INDEX

#Fix PKG_ADD
echo "pkg load mathgl" > %{name}/PKG_ADD
echo "mathgl;" >> %{name}/PKG_ADD

#fix wrong version number in description
%__sed -i 's/1.9/1.11/' %{name}/DESCRIPTION

# We cannot use version macro with octave package search,
# as pkg.m assumes a x.y.z format for packages. Failing
# to do this renders the plugin inoperable. So we use pkgversion
cp -pR %{name}/inst/* %{buildroot}/%{_libexecdir}/octave/packages/%{name}-%{pkgversion}/

#packinfo dir is required, or octave will not find the dir in recursive search
%__mkdir_p %{buildroot}/%{_datadir}/octave/packages/%{name}-%{pkgversion}/packinfo
cp -p %{name}/COPYING %{buildroot}/%{_datadir}/octave/packages/%{name}-%{pkgversion}/packinfo/
cp -p %{name}/DESCRIPTION %{buildroot}/%{_datadir}/octave/packages/%{name}-%{pkgversion}/packinfo/
cp -p %{name}/PKG_ADD %{buildroot}/%{_datadir}/octave/packages/%{name}-%{pkgversion}/packinfo/

popd
######################################################################

%clean
%__rm -rf %{buildroot}

%post octave
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%postun octave
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%if %{mdvver} <= 201100
%post doc
%_install_info %{name}_en.info
%_install_info %{name}_ru.info

%preun doc
%_remove_install_info %{name}_en.info
%_remove_install_info %{name}_ru.info
%endif

%files tools
%{_bindir}/mgl2*
%{_bindir}/mglview

%files examples
%{_bindir}/mgl*_example

%files data
%{_datadir}/%{name}

%files octave
%{_datadir}/octave/packages/*
%{_libexecdir}/octave/packages/*

%files doc
%{_docdir}/%{name}
%{_infodir}/*

%files -n %{mainlibname}
%doc AUTHORS COPYING COPYRIGHT ChangeLog.txt NEWS README
%{_libdir}/libmgl.so.*

%files -n %{fltklibname}
%{_libdir}/libmgl-fltk.so.*

%files -n %{glutlibname}
%{_libdir}/libmgl-glut.so.*

%files -n %{qtlibname}
%{_libdir}/libmgl-qt.so.*

%files -n %{wxlibname}
%{_libdir}/libmgl-wx.so.*

%files -n %{develname}
%{_libdir}/libmgl*.so
%if %{mdvver} <= 201100
%{_libdir}/*.la
%endif
%{_includedir}/mgl

%files -n %{staticdevelname}
%{_libdir}/*.a

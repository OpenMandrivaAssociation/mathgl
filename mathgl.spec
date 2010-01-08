%define mainlibmajor 5
%define mainlibname %mklibname mgl %{mainlibmajor}
%define fltklibmajor 5
%define fltklibname %mklibname mgl-fltk %{fltklibmajor}
%define glutlibmajor 5
%define glutlibname %mklibname mgl-glut %{glutlibmajor}
%define qtlibmajor 5
%define qtlibname %mklibname mgl-qt %{qtlibmajor}
%define wxlibmajor 5
%define wxlibname %mklibname mgl-wx %{wxlibmajor}
%define develname %mklibname mgl -d
%define staticdevelname %mklibname mgl -d -s

%define octave_api api-v37

Name:		mathgl
Version:	1.10
Release:	%mkrel 1
Summary:	Library for scientific graphics
License:	GPLv2+
Group:		System/Libraries
Url:		http://mathgl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/mathgl/%{name}-%{version}.tgz
Patch0:		mathgl-1.10-mdv-fix-fltk-include-path.patch
Patch1:		mathgl-1.10-mdv-fix-mgl_qt_example-linkage.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	qt4-devel
BuildRequires:	gsl-devel
BuildRequires:	GL-devel
BuildRequires:	mesaglut-devel
BuildRequires:	fltk-devel
BuildRequires:	hdf5-devel
BuildRequires:	libwxgtk2.8-devel
BuildRequires:	octave-devel
BuildRequires:	swig
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
Requires(post): info-install
Requires(preun): info-install

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
%patch1 -p1 -b .linkage

# fix EOL
for i in AUTHORS COPYRIGHT README
do
  sed -i 's/\r//' $i
done

%build
autoreconf
%configure --enable-all --enable-octave
%make

%install
rm -rf %{buildroot}
%makeinstall

# octave .oct file fix and install 
# from Fedora specfile

mkdir -p temp-octave

pushd .
cd temp-octave
#Decompress tarballed "oct" file and remove tarball
tar -zxf %{buildroot}/%{_datadir}/%{name}/octave/%{name}.tar.gz
rm %{buildroot}/%{_datadir}/%{name}/octave/%{name}.tar.gz

#Copy the .oct file and supporting files to octave packages dir
mkdir -p %{buildroot}/%{_libexecdir}/octave/packages/%{name}-1.10.0/
#Remove empty INDEX file
rm %{name}/INDEX

#Fix PKG_ADD
echo "pkg load mathgl" > %{name}/PKG_ADD
echo "mathgl;" >> %{name}/PKG_ADD

#fix wrong version number in description
sed -i 's/1.9/1.10/' %{name}/DESCRIPTION

#We cannot use version macro with octave package search,
# as pkg.m assumes a x.y.z format for packages. Failing
# to do this renders the plugin inoperable
cp -pR %{name}/inst/* %{buildroot}/%{_libexecdir}/octave/packages/%{name}-1.10.0/

#packinfo dir is required, or octave will not find the dir in recursive search
mkdir -p %{buildroot}/%{_datadir}/octave/packages/%{name}-1.10.0/packinfo
cp -p %{name}/[A-Z]* %{buildroot}/%{_datadir}/octave/packages/%{name}-1.10.0/packinfo

popd 

%clean
rm -rf %{buildroot}

%post octave
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%postun octave
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%post doc
%_install_info %{name}_en.info
%_install_info %{name}_ru.info

%preun doc
%_remove_install_info %{name}_en.info
%_remove_install_info %{name}_ru.info

%files tools
%defattr(-,root,root,-)
%{_bindir}/mgl2*
%{_bindir}/mglview

%files examples
%defattr(-,root,root,-)
%{_bindir}/mgl*_example

%files data
%defattr(-,root,root,-)
%{_datadir}/%{name}

%files octave
%defattr(-,root,root,-)
%{_datadir}/octave/packages/*
%{_libexecdir}/octave/packages/*

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}
%{_infodir}/*

%files -n %{mainlibname}
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog.txt NEWS README
%{_libdir}/libmgl.so.*

%files -n %{fltklibname}
%defattr(-,root,root,-)
%{_libdir}/libmgl-fltk.so.*

%files -n %{glutlibname}
%defattr(-,root,root,-)
%{_libdir}/libmgl-glut.so.*

%files -n %{qtlibname}
%defattr(-,root,root,-)
%{_libdir}/libmgl-qt.so.*

%files -n %{wxlibname}
%defattr(-,root,root,-)
%{_libdir}/libmgl-wx.so.*

%files -n %{develname}
%defattr(-,root,root,-)
%{_libdir}/libmgl*.so
%{_libdir}/*.la
%{_includedir}/mgl

%files -n %{staticdevelname}
%defattr(-,root,root,-)
%{_libdir}/*.a

%define		mod_name	video
%define 	apxs		/usr/sbin/apxs
Summary:	Shows images grabbed from a v4l device
Summary(pl):	Wy�wietla obrazy zrzucone z urz�dzenia v4l
Name:		apache-mod_%{mod_name}
Version:	0.1.0
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://borud.no/mod_video/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	c1def4425d597596a1c4c5bb0f607085
Patch0:		%{name}-webcam.patch
URL:		http://modvideo.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This package contains an Apache module for serving snapshots from the
video4linux API.

%description -l pl
Pakiet ten zawiera modu� do Apache umo�liwiaj�cy serwowanie zdj��
bezpo�rednio generowanych z kamer obs�ugiwanych poprzez video4linux
API.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lpng -ljpeg

%install
rm -rf $RPM_BUILD_ROOT

install -D mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_pkglibdir}/*

%define		mod_name	video
Summary:	Shows images grabbed from a v4l device
Summary(pl):	Wy�wietla obrazy zrzucone z urz�dzenia v4l
Name:		apache-mod_%{mod_name}
Version:	0.1.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://borud.no/mod_video/download/mod_%{mod_name}-%{version}.tar.gz
Patch0:		%{name}-webcam.patch
URL:		http://modvideo.sourceforge.net/
BuildRequires:	apache(EAPI)-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
Prereq:		/usr/sbin/apxs
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This package contains an Apache module for serving snapshots from the
video4linux API.

%description -l pl
Pakiet ten zawiera modu� do Apache umo�liwiajacey serwowanie zdj��
bezpo�rednio generowanych z kamer obs�ugiwanych poprzez video4linux
API.

%prep 
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lz -lpng -ljpeg

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_pkglibdir}/*

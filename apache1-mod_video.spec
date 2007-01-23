%define		mod_name	video
%define 	apxs		/usr/sbin/apxs1
Summary:	Shows images grabbed from a v4l device
Summary(pl):	Wy¶wietla obrazy zrzucone z urz±dzenia v4l
Name:		apache1-mod_%{mod_name}
Version:	0.1.0
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://borud.no/mod_video/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	c1def4425d597596a1c4c5bb0f607085
Patch0:		%{name}-webcam.patch
URL:		http://modvideo.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_video <= 0.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This package contains an Apache module for serving snapshots from the
video4linux API.

%description -l pl
Pakiet ten zawiera modu³ do Apache umo¿liwiaj±cy serwowanie zdjêæ
bezpo¶rednio generowanych z kamer obs³ugiwanych poprzez video4linux
API.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lpng -ljpeg

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 0.1.0-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*

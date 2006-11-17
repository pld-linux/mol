#
# TODO:
#  - scripts should search for modules in /lib/moduiles
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools
%bcond_with	minimal		# no X, no sound
%bcond_without	debugger	# no debugger

%{?debug:%define with_debugger 1}

%define	_basever 0.9.71
%define	_minor	.1
%define _rel	1
Summary:	Runs MacOS natively on Linux/ppc
Summary(ja):	Mac On Linux - Linux/ppc ¾å¤Î MacOS ¥Í¥¤¥Æ¥£¥Ö¼Â¹Ô´Ä¶­
Summary(pl):	Natywne uruchamianie MacOS na Linux/ppc
Name:		mol
Version:	%{_basever}%{_minor}
Release:	%{_rel}
License:	GPL
Group:		Applications/Emulators
#Source0:	http://www.maconlinux.org/downloads/%{name}-%{version}.tgz
Source0:	http://www.mirrorservice.org/sites/www.ibiblio.org/gentoo/distfiles/%{name}-%{version}.tar.bz2
# Source0-md5:	3eaa51927191b03b06828609a1122307
Source1:	%{name}.desktop
Source2:	%{name}-terminal.desktop
Source3:	%{name}.png
Patch0:		%{name}-iquote.patch
Patch1:		%{name}-scripts.patch
Patch2:		%{name}-molrc.patch
URL:		http://www.maconlinux.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with userspace}
BuildRequires:	gcc >= 4.0
%if !%{with minimal}
BuildRequires:	alsa-lib-devel
BuildRequires:	libpng-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
%endif
%{?with_debugger:BuildRequires:	ncurses-devel}
%endif
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
Requires:	dev >= 2.8.0-24
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _mol_libdir 		%{_libdir}/mol/%{_basever}
%define _mol_datadir 		%{_datadir}/mol/%{_basever}
%define _mol_localstatedir	/var/lib/mol

%description
With MOL you can run MacOS under Linux - in full speed! All PowerPC
versions of MacOS are supported (including MacOSX 10.2).

%description -l ja
MOL ¤Ï MacOS ¤ò Linux ¾å¤ÇÆ°ºî¤µ¤»¤ë¤³¤È¤¬½ÐÍè¤Þ¤¹¡¥Æ°ºî¤â¹âÂ®¤Ç¤¹¡¥
¥Ð¡¼¥¸¥ç¥ó 9.2 ¤ò´Þ¤á¡¤PowerPC ÍÑ MacOS ¤ÎÁ´¥Ð¡¼¥¸¥ç¥ó¤¬Æ°ºî¤·¤Þ¤¹¡¥

%description -l pl
Przy u¿yciu MOL mo¿na uruchamiaæ MacOS pod Linuksem - z pe³n±
szybko¶ci±! Obs³ugiwane s± wszystkie wersje PowerPC MacOS-a (w³±cznie
z MacOSX 10.2).

%package -n kernel%{_alt_kernel}-misc-mol
Summary:	Mac-on-Linux kernel modules
Summary(pl):	Modu³y j±dra Mac-on-Linux
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-misc-mol
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking).

%description -n kernel%{_alt_kernel}-misc-mol -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci).

%package -n kernel%{_alt_kernel}-smp-misc-mol
Summary:	Mac-on-Linux kernel modules SMP
Summary(pl):	Modu³y j±dra Mac-on-Linux SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-misc-mol
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking). SMP
version.

%description -n kernel%{_alt_kernel}-smp-misc-mol -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci). Wersja dla j±der SMP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
echo 'obj-m := sheep.o' > src/netdriver/Makefile.26
sed -i 's@ \./configure @ true @' config/Makefile.master

cat << EOF | sed 's/^ *//' > config/defconfig-ppc
    CONFIG_PPC=y
    CONFIG_OLDWORLD=y
    CONFIG_FBDEV=y
%if %{with minimal}
    # CONFIG_X11 is not set
    # CONFIG_VNC is not set
    # CONFIG_ALSA is not set
    # CONFIG_OSS is not set
%else
    CONFIG_X11=y
    CONFIG_VNC=y
    CONFIG_ALSA=y
    CONFIG_OSS=y
%endif
    # CONFIG_XDGA is not set
    CONFIG_USBDEV=y
    # CONFIG_PCIPROXY is not set

    ### Debugging
    CONFIG_TTYDRIVER=y
%if %{with debugger}
    CONFIG_DEBUGGER=y
    CONFIG_DHCP_DEBUG=y
%else
    # CONFIG_DEBUGGER is not set
    # CONFIG_DHCP_DEBUG is not set
%endif

%if 0%{?debug:1}
    CONFIG_SCSIDEBUG=y
    CONFIG_DUMP_PACKETS=y
%else
    # CONFIG_SCSIDEBUG is not set
    # CONFIG_DUMP_PACKETS is not set
%endif
    # CONFIG_HOSTED is not set

    ### Network drivers
    CONFIG_TUN=y
    CONFIG_TAP=y
    CONFIG_SHEEP=y
EOF

%build
rm config/configure/configure
%{__make} configure
cd obj-ppc/config
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
%configure \
	AS="%{__cc} -c" \
%if %{with minimal}
	--disable-alsa \
	--disable-png \
%endif
	--disable-xdga
cd ../..

export TERM=dumb
%{__make} defconfig

%if %{with userspace}
%{__make} \
	NCURSES_INCLUDES="-I/usr/include/ncurses" \
	prefix=%{_prefix} \
	BUILD_MODS=n
%endif

%if %{with kernel}
%{__make} obj-ppc/include/molversion.h local-includes

%{__make} -C src/kmod/Linux setup-common
%build_kernel_modules T=$TMPDIR -m mol -C obj-ppc/build/src/kmod

%{__make} -C src/netdriver setup-tree-26
%build_kernel_modules -m sheep -C obj-ppc/build/src/netdriver
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}	\
	docdir=/moldoc

install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}/mol.png
%endif

%if %{with kernel}
%install_kernel_modules -m obj-ppc/build/src/{kmod/mol,netdriver/sheep} -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%post	-n kernel%{_alt_kernel}-misc-mol
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-misc-mol
%depmod %{_kernel_ver}

%if %{with smp} && %{with dist_kernel}
%post	-n kernel%{_alt_kernel}-smp-misc-mol
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-misc-mol
%depmod %{_kernel_ver}smp
%endif
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc $RPM_BUILD_ROOT/moldoc/*
%dir %{_sysconfdir}/mol
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mol/[!t]*
%attr(755,root,root) %{_sysconfdir}/mol/tunconfig
%attr(755,root,root) %{_bindir}/*
%dir %{_mol_libdir}
%dir %{_mol_libdir}/bin
%attr(755,root,root) %{_mol_libdir}/bin/keyremap
%attr(755,root,root) %{_mol_libdir}/bin/kver_approx
%attr(755,root,root) %{_mol_libdir}/bin/modload
%attr(755,root,root) %{_mol_libdir}/bin/mol_uname
%attr(755,root,root) %{_mol_libdir}/bin/molrcget
%attr(755,root,root) %{_mol_libdir}/bin/selftest
%attr(755,root,root) %{_mol_libdir}/bin/startmol
%attr(4755,root,root) %{_mol_libdir}/bin/mol
%if %{with debugger}
%attr(755,root,root) %{_mol_libdir}/bin/moldeb
%endif
%{_mol_libdir}/mol.symbols
%dir %{_mol_datadir}
%{_mol_datadir}/images
%{_mol_datadir}/oftrees
%{_mol_datadir}/syms
%{_mol_datadir}/vmodes
%{_mol_datadir}/nvram
%{_mol_datadir}/graphics
%{_mol_datadir}/config
%{_mol_datadir}/drivers
%{_mol_datadir}/startboing
%{_desktopdir}/mol*.desktop
%{_pixmapsdir}/mol.png
%dir %{_mol_localstatedir}
%{_mol_localstatedir}/nvram.nw
%{_mol_localstatedir}/nvram.x
%{_mandir}/man1/*
%{_mandir}/man5/*
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-mol
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/mol.ko*
/lib/modules/%{_kernel_ver}/misc/sheep.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-misc-mol
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/mol.ko*
/lib/modules/%{_kernel_ver}smp/misc/sheep.ko*
%endif
%endif

#
# TODO:
#  - building without userspace (make in userspace is preparing files
#    for module building)
#  - scripts should search for modules in /lib/moduiles
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#%%bcond_without	userspace	# don't build userspace tools
%bcond_with	minimal		# no X, no sound
%bcond_without	debugger	# no debugger

%define _rel	0.1
Summary:	Runs MacOS natively on Linux/ppc
Summary(ja):	Mac On Linux - Linux/ppc ¾å¤Î MacOS ¥Í¥¤¥Æ¥£¥Ö¼Â¹Ô´Ä¶­
Summary(pl):	Natywne uruchamianie MacOS na Linux/ppc
Name:		mol
Version:	0.9.70
Release:	%{_rel}
License:	GPL
Group:		Applications/Emulators
Source0:	http://www.maconlinux.org/downloads/%{name}-%{version}.tgz
# Source0-md5:	bfdd0bd6ae01018b5c46f87d4ad879f1
#Source1:	mol.init
Patch0:		%{name}-modules-update.patch
Patch1:		%{name}-modules26.patch
#Patch0:	%{name}-curses.patch
#Patch1:	%{name}-configure.patch
#Patch2:	%{name}-kernel.patch
#Patch3:	%{name}-sheepnet.patch
#Patch4:	%{name}-netdriver.patch
#Patch5:	%{name}-libimport.patch
#Patch6:	%{name}-usbdev.patch
#Patch7:	%{name}-gkh.patch
#Patch8:	%{name}-gkh-compiler_h.patch
#Patch9:	%{name}-gkh-includes.patch
Patch10:	%{name}-warnings.patch
URL:		http://www.maconlinux.org/
#BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	bison
#BuildRequires:	flex
#%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,preun):	/sbin/chkconfig
Requires:	dev >= 2.8.0-24
Requires:	kernel(mol)
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _mol_libdir 		%{_libdir}/mol/%{version}
%define _mol_datadir 		%{_datadir}/mol/%{version}
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

%package -n kernel%{_alt_kernel}-%{name}
Summary:	Mac-on-Linux kernel modules
Summary(pl):	Modu³y j±dra Mac-on-Linux
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Requires(post,postun):	/sbin/depmod
Provides:	kernel(mol)
#Obsoletes:	kernel-mol

%description -n kernel%{_alt_kernel}-%{name}
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking).

%description -n kernel%{_alt_kernel}-%{name} -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci).

%package -n kernel%{_alt_kernel}-smp-%{name}
Summary:	Mac-on-Linux kernel modules SMP
Summary(pl):	Modu³y j±dra Mac-on-Linux SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/Emulators
Requires(post,postun):	/sbin/depmod
Provides:	kernel(mol)
#Obsoletes:	kernel-mol

%description -n kernel%{_alt_kernel}-smp-%{name}
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking). SMP
version.

%description -n kernel%{_alt_kernel}-smp-%{name} -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci). Wersja dla j±der SMP.

%prep
%setup -q
chmod +w -R .
%patch0 -p1
%patch1 -p1
%patch10 -p1
sed -i 's|@KERNEL_SRC@|%{_kernelsrcdir}|g' src/kmod/Linux/Makefile.26
sed -i '/struct menu \*current_menu/s/static//' config/kconfig/mconf.c
sed -i '/KERNEL_SOURCE=/s|=.*|="%{_kernelsrcdir}"|' scripts/kernelsrc

cat << EOF | sed 's/^ *//' > config/defconfig-ppc
    CONFIG_PPC=y
    CONFIG_FBDEV=y
%if !%{with minimal}
    CONFIG_OLDWORLD=y
    CONFIG_X11=y
    CONFIG_VNC=y
    CONFIG_XDGA=y
    CONFIG_ALSA=y
    CONFIG_OSS=y
    CONFIG_USBDEV=y
    CONFIG_TTYDRIVER=y
%else
    # CONFIG_OLDWORLD is not set
    # CONFIG_X11 is not set
    # CONFIG_VNC is not set
    # CONFIG_XDGA is not set
    # CONFIG_ALSA is not set
    # CONFIG_OSS is not set
    # CONFIG_USBDEV is not set
    # CONFIG_TTYDRIVER is not set
%endif
%if %{with debugger}
    CONFIG_DEBUGGER=y
%else
    # CONFIG_DEBUGGER is not set
%endif

    ### Network drivers
    CONFIG_TUN=y
    CONFIG_TAP=y
    CONFIG_SHEEP=y

EOF

%build
%{__autoheader}
%{__autoconf}

CFLAGS="%{rpmcflags} -I/usr/include/ncurses -DNETLINK_TAPBASE=16"; export CFLAGS

%configure \
%if !%{with minimal}
	--with-x	\
	--enable-alsa	\
	--enable-xdga	\
	--enable-png
%endif

%{__make} clean
%{__make} defconfig
%{__make} \
	prefix=%{_prefix}

cd src/kmod/build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h

	%if %{with dist_kernel}
		%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
	%else
		install -d o/include/config
		touch o/include/config/MARKER
		ln -sf %{_kernelsrcdir}/scripts o/scripts
	%endif

	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv mol.ko mol-$cfg.ko
done

cd ../../netdriver/build
echo 'obj-m := sheep.o' > Makefile
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h

	%if %{with dist_kernel}
		%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
	%else
		install -d o/include/config
		touch o/include/config/MARKER
		ln -sf %{_kernelsrcdir}/scripts o/scripts
	%endif

	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv sheep.ko sheep-$cfg.ko
done
cd ../../..

%install
rm -rf $RPM_BUILD_ROOT

#install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}	\
	docdir=moldoc

#install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%if %{with kernel}
cd src
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install kmod/build/mol-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/mol.ko
install netdriver/build/sheep-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/sheep.ko
%if %{with smp} && %{with dist_kernel}
install kmod/build/mol-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/mol.ko
install netdriver/build/sheep-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/sheep.ko
%endif
cd ..
%endif

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#/sbin/chkconfig --add mol
#if [ -f /var/lock/subsys/mol ]; then
#	/etc/rc.d/init.d/mol stop 1>&2
#	/etc/rc.d/init.d/mol start 1>&2
#else
#	echo "Run \"/etc/rc.d/init.d/mol start\" to load modules"
#fi

#%preun
#if [ "$1" = "0" ]; then
#	if [ -f /var/lock/subsys/mol ]; then
#		/etc/rc.d/init.d/mol stop 1>&2
#	fi
#	/sbin/chkconfig --del mol
#fi

%if %{with kernel}
%post	-n kernel%{_alt_kernel}-%{name}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-%{name}
%depmod %{_kernel_ver}

%if %{with smp} && %{with dist_kernel}
%post	-n kernel%{_alt_kernel}-smp-%{name}
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-%{name}
%depmod %{_kernel_ver}smp
%endif
%endif

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
#%attr(754,root,root) /etc/rc.d/init.d/mol
%attr(755,root,root) %{_mol_libdir}/mol.symbols
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
%dir %{_mol_localstatedir}
%{_mol_localstatedir}/nvram.nw
%{_mandir}/man1/*
%{_mandir}/man5/*

%if %{with kernel}
%files -n kernel%{_alt_kernel}-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
%endif

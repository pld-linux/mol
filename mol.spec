#
# TODO:
# 2.6 kernel support
# 
# Conditional build:
%bcond_without dist_kernel 	# without distribution kernel packages
%bcond_without dist_gkh		# without distribution glibc-kernel-headers

%define _snap 040105
%define _rel 0.2

%if "%{_snap}" != "0"
%define snapshot snap%{_snap}.rel
%else
%define snapshot %{nil}
%endif

Summary:	Runs MacOS natively on Linux/ppc
Summary(pl):	Natywne uruchamianie MacOS na Linux/ppc
Name:		mol
Version:	0.9.69
Release:	%{snapshot}%{_rel}
License:	GPL
Group:		Applications/Emulators
Source0:	mol-%{_snap}.tar.bz2
# Source0-md5:	d371cf7f3b5b40d243cd62f0f62aad8b
Source1:	mol.init
Source2:	libimport-%{_snap}.tar.bz2
# Source2-md5:	7b897b5948e068f472f2fbe70037d2bd
Patch0:		%{name}-curses.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-kernel.patch
Patch3:		%{name}-sheepnet.patch
Patch4:		%{name}-netdriver.patch
Patch5:		%{name}-libimport.patch
Patch6:		%{name}-usbdev.patch
Patch7:		%{name}-gkh.patch
URL:		http://www.maconlinux.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ncurses-devel
BuildRequires:	bzip2
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:BuildRequires:	kernel-headers}
%{?with_dist_kernel:BuildRequires:	kernel-source}
Requires(post,preun):	/sbin/chkconfig
Requires:	kernel(mol)
Requires:	dev >= 2.8.0-24
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _bdir %{name}-%{version}
%define _kver %(echo %{_kernel_ver} | cut -d- -f1)
%define _mol_libdir 		%{_libdir}/mol/%{version}
%define _mol_datadir 		%{_datadir}/mol/%{version}
%define _mol_localstatedir	/var/lib/mol

%description
With MOL you can run MacOS under Linux - in full speed! All PowerPC
versions of MacOS are supported (including MacOSX 10.2).

%description -l pl
Przy u¿uciu MOL mo¿na uruchamiaæ MacOS pod Linuksem - z pe³n±
szybko¶ci±! Obs³ugiwane s± wszystkie wersje PowerPC MacOS-a (w³±cznie
z MacOSX 10.2).

%package -n kernel-%{name}
Summary:	Mac-on-Linux kernel modules
Summary(pl):	Modu³y j±dra Mac-on-Linux
Group:		Applications/Emulators
Release:	%{snapshot}%{_rel}@%{_kernel_ver_str}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-mol
Provides:	kernel(mol)

%description -n kernel-%{name}
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking).

%description -n kernel-%{name} -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci).

%package -n kernel-smp-%{name}
Summary:	Mac-on-Linux kernel modules SMP
Summary(pl):	Modu³y j±dra Mac-on-Linux SMP
Group:		Applications/Emulators
Release:	%{snapshot}%{_rel}@%{_kernel_ver_str}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-mol
Provides:	kernel(mol)

%description -n kernel-smp-%{name}
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking). SMP
version.

%description -n kernel-smp-%{name} -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci). Wersja dla jader SMP.

%prep
%setup -q -n mol
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 
%patch4 -p1
%patch5 -p1

%if %{with dist_gkh}
%patch6 -p1 
%patch7 -p1
%endif

bzip2 -dc %{SOURCE2} | tar -xf - 

%build
rm -f missing
rm -f acinclude.m4
mkdir scripts/buildtools
%{__aclocal} -I . 2>/dev/null
echo "AC_DEFUN([AM_PROG_AS],[])" > acinclude.m4
%{__autoheader}
%{__automake} -a -c 
%{__autoconf}

export KERNEL_SOURCE=`pwd`/linux/
cp -rdp %{_kernelsrcdir}/ .

%configure --enable-fhs --enable-debugger --disable-tap --disable-tun
%{__make} clean

rm linux/.config 
cp -f linux/config-smp linux/.config
(cd linux; make oldconfig)

%{__make} -C scripts 
%{__make} -C src/kmod CC="%{__cc} -D__KERNEL_SMP" 
%{__make} -C src/netdriver CC="%{__cc} -D__KERNEL_SMP" 
mkdir smp
cp -f src/kmod/build/mol.o smp
cp -f src/netdriver/build/sheep.o smp

rm linux/.config
cp -f linux/config-up linux/.config
(cd linux; make oldconfig)

%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install -d $RPM_BUILD_ROOT/modules/{up,smp}

for x in graphics drivers images nvram ; do
    test -d mollib/$x || mkdir mollib/$x
done
		
scripts/libimport copy 

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

mv -f $RPM_BUILD_ROOT%{_datadir}/doc/mol-%{version} $RPM_BUILD_ROOT/moldoc
mv -f $RPM_BUILD_ROOT%{_libdir}/mol/%{version}/modules/%{_kver} $RPM_BUILD_ROOT/modules/up
cp -r smp/ $RPM_BUILD_ROOT/modules/
mv -f $RPM_BUILD_ROOT/modules/smp/{mol.o,sheep.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/
mv -f $RPM_BUILD_ROOT/modules/up/%{_kver}/{mol.o,sheep.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mol
if [ -f /var/lock/subsys/mol ]; then
	/etc/rc.d/init.d/mol stop 1>&2
	/etc/rc.d/init.d/mol start 1>&2
else
	echo "Run \"/etc/rc.d/init.d/mol start\" to load modules"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mol ]; then
		/etc/rc.d/init.d/mol stop 1>&2
	fi
	/sbin/chkconfig --del mol
fi

%post	-n kernel-%{name}
%depmod %{_kernel_ver}

%postun -n kernel-%{name}
%depmod %{_kernel_ver}

%post	-n kernel-smp-%{name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-%{name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc $RPM_BUILD_ROOT/moldoc/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mol/*
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
%attr(754,root,root) /etc/rc.d/init.d/mol
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

%files -n kernel-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*

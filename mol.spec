#
# Conditional build:
# _without_dist_kernel	- without distribution kernel packages
#
Summary:	Runs MacOS natively on Linux/ppc
Summary(pl):	Natywne uruchamianie MacOS na Linux/ppc
Name:		mol
Version:	0.9.68
Release:	0.3
License:	GPL
Group:		Applications/Emulators
Source0:	mol-rsync.tgz
Patch0:		%{name}-curses.patch
Patch1:		%{name}-configure.patch
URL:		http://www.maconlinux.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ncurses-devel
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
Requires:	kernel(mol)
Requires:	dev >= 2.8.0-24
ExclusiveArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _kver %(echo %{_kernel_ver} | cut -d- -f1)
%define _mol_libdir 		%{_libdir}/mol/%{version}
%define _mol_datadir 		%{_datadir}/mol/%{version}
%define _mol_localstatedir	/var/lib/mol

%description
With MOL you can run MacOS under Linux - in full speed! All PowerPC
versions of MacOS are supported (including MacOS 9.2).

%description -l pl
Przy u¿uciu MOL mo¿na uruchamiaæ MacOS pod Linuksem - z pe³n±
szybko¶ci±! Obs³ugiwane s± wszystkie wersje PowerPC MacOS-a (w³±cznie
z MacOS 9.2).

%package -n kernel-%{name}
Summary:	Mac-on-Linux kernel modules
Summary(pl):	Modu³y j±dra Mac-on-Linux
Group:		Applications/Emulators
Requires(post,postun):  /sbin/depmod
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
Requires(post,postun):  /sbin/depmod
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
%setup -q -n mol-rsync
%patch0 -p1
%patch1 -p1 

%build
rm -f missing
%{__aclocal} -I .
%{__autoheader}
%{__automake}
%{__autoconf}
%configure --enable-fhs --enable-debugger
%{__make} clean
%{__make} -C scripts all
%{__make} CC="gcc -D__SMP__" SMP=1 modules_
mkdir smp
%{__make} DESTDIR=$RPM_BUILD_DIR/mol-rsync/smp install_modules
%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install -d $RPM_BUILD_ROOT/modules/{up,smp}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc/mol-%{version} $RPM_BUILD_ROOT/moldoc
mv -f $RPM_BUILD_ROOT%{_libdir}/mol/%{version}/modules/%{_kver} $RPM_BUILD_ROOT/modules/up
cp -r smp/%{_libdir}/mol/%{version}/modules/%{_kver} $RPM_BUILD_ROOT/modules/smp
mv -f $RPM_BUILD_ROOT/modules/smp/%{_kver}/{mol.o,molsymglue.o,sheep.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/
mv -f $RPM_BUILD_ROOT/modules/up/%{_kver}/{mol.o,molsymglue.o,sheep.o} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/

%clean
rm -rf $RPM_BUILD_ROOT


%post -n kernel-%{name}
/sbin/depmod -a

%postun -n kernel-%{name}
/sbin/depmod -a

%post -n kernel-smp-%{name}
/sbin/depmod -a

%postun -n kernel-smp-%{name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc $RPM_BUILD_ROOT/moldoc
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mol/*
%attr(755,root,root) %{_bindir}/*
%dir %{_mol_libdir}
%dir %{_mol_libdir}/bin
%attr(755,root,root) %{_mol_libdir}/bin/*
#%dir %{_mol_libdir}/modules
%attr(755,root,root) %{_mol_libdir}/mol.symbols
%dir %{_mol_datadir}
%{_mol_datadir}/images
%{_mol_datadir}/oftrees
%{_mol_datadir}/pci_roms
%{_mol_datadir}/syms
%{_mol_datadir}/vmodes
%{_mol_datadir}/nvram
%{_mol_datadir}/graphics
%{_mol_datadir}/config
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

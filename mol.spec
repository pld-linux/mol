Summary:	Runs MacOS natively on Linux/ppc
Summary(pl):	Natywne uruchamianie MacOS na Linux/ppc
Name:		mol
Version:	0.9.63
Release:	0.3
License:	GPL
Group:		Applications/Emulators
Source0:	ftp://ftp.nada.kth.se/pub/home/f95-sry/Public/mac-on-linux/%{name}-%{version}.tgz
Patch0:		%{name}-curses.patch
Patch1:		%{name}-mknod.patch
URL:		http://www.maconlinux.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
Requires:	kernel-mol
Requires:	dev >= 2.8.0-24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
With MOL you can run MacOS under Linux - in full speed! All PowerPC
versions of MacOS are supported (including MacOS 9.2).

%description -l pl
Przy u¿uciu MOL mo¿na uruchamiaæ MacOS pod Linuksem - z pe³n±
szybko¶ci±! Obs³ugiwane s± wszystkie wersje PowerPC MacOS-a (w³±cznie
z MacOS 9.2).

%package -n kernel-mol
Summary:	Mac-on-Linux kernel modules
Summary(pl):	Modu³y j±dra Mac-on-Linux
Group:		Applications/Emulators
ExclusiveArch:	ppc

%description -n kernel-mol
This package contains the Mac-on-Linux kernel module needed by MOL. It
also contains the sheep_net kernel module (for networking).

%description -n kernel-mol -l pl
Ten pakiet zawiera modu³ j±dra Mac-on-Linux potrzebny dla MOL. Zawiera
tak¿e modu³ j±dra sheep_net (dla sieci).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
aclocal
%{__autoconf}
%{__automake}
%configure --enable-fhs
%{__make} clean
%{__make} KERNEL_TREES=%kernel_trees

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
mv -f $RPM_BUILD_ROOT%{_datadir}/doc/mol-%{version} $RPM_BUILD_ROOT/moldoc

%clean
rm -rf $RPM_BUILD_ROOT

%define _mol_libdir 		%{_libdir}/mol/%{version}
%define _mol_datadir 		%{_datadir}/mol/%{version}
%define _mol_localstatedir	/var/lib/mol

%files
%defattr(644,root,root,755)
%doc $RPM_BUILD_ROOT/moldoc
%config %{_sysconfdir}/molrc
%_mol_localstatedir/nvram.nw
%{_mandir}/man1/*
%{_mandir}/man5/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %_mol_libdir/bin/*
%dir %_mol_libdir/modules
%_mol_datadir/images/*
%_mol_datadir/oftrees/*
%_mol_datadir/pci_roms/*
%_mol_datadir/syms/*
%_mol_datadir/vmodes/*
%_mol_datadir/nvram/*
%_mol_datadir/startboing
%_mol_datadir/config/molrc.sys

%files -n kernel-mol
%defattr(644,root,root,755)
%{_mol_libdir}/modules/

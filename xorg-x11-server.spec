# This package is an experiment in active integration of upstream SCM with
# Fedora packaging.  It works something like this:
#
# The "pristine" source is actually a git repo (with no working checkout).
# The first step of %%prep is to check it out and switch to a "fedora" branch.
# If you need to add a patch to the server, just do it like a normal git
# operation, dump it with git-format-patch to a file in the standard naming
# format, and add a PatchN: line.  If you want to push something upstream,
# check out the master branch, pull, cherry-pick, and push.

# X.org requires lazy relocations to work.
%undefine _hardened_build

#global gitdate 20161026
%global stable_abi 1

%if !0%{?gitdate} || %{stable_abi}
# Released ABI versions.  Have to keep these manually in sync with the
# source because rpm is a terrible language.
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 23
%global videodrv_minor 0
%global xinput_major 24
%global xinput_minor 1
%global extension_major 10
%global extension_minor 0
%endif

%if 0%{?gitdate}
# For git snapshots, use date for major and a serial number for minor
%global minor_serial 0
%global git_ansic_major %{gitdate}
%global git_ansic_minor %{minor_serial}
%global git_videodrv_major %{gitdate}
%global git_videodrv_minor %{minor_serial}
%global git_xinput_major %{gitdate}
%global git_xinput_minor %{minor_serial}
%global git_extension_major %{gitdate}
%global git_extension_minor %{minor_serial}
%endif

%global pkgname xorg-server

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   1.19.1
Release:   3%{?gitdate:.%{gitdate}}%{dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X

#VCS:      git:git://git.freedesktop.org/git/xorg/xserver
%if 0%{?gitdate}
# git snapshot.  to recreate, run:
# ./make-git-snapshot.sh `cat commitid`
Source0:   xorg-server-%{gitdate}.tar.xz
#Source0:   http://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
Source1:   make-git-snapshot.sh
Source2:   commitid
%else
Source0:   http://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
Source1:   gitignore
%endif

Source4:   10-quirks.conf

Source10:   xserver.pamd

# "useful" xvfb-run script
Source20:  http://svn.exactcode.de/t2/trunk/package/xorg/xorg-server/xvfb-run.sh

# for requires generation in drivers
Source30: xserver-sdk-abi-requires.release
Source31: xserver-sdk-abi-requires.git

# maintainer convenience script
Source40: driver-abi-rebuild.sh

# Various fixes pending upstream
Patch2: 0005-xfree86-Remove-redundant-ServerIsNotSeat0-check-from.patch
Patch3: 0006-xfree86-Make-adding-unclaimed-devices-as-GPU-devices.patch
Patch4: 0007-xfree86-Try-harder-to-find-atleast-1-non-GPU-Screen.patch

# Patches for better integration with the nvidia driver, pending upstream
Patch11: 0001-xfree86-Free-devlist-returned-by-xf86MatchDevice.patch
Patch12: 0002-xfree86-Make-OutputClassMatches-take-a-xf86_platform.patch
Patch13: 0003-xfree86-Add-options-support-for-OutputClass-Options.patch
Patch14: 0004-xfree86-xf86platformProbe-split-finding-pci-info-and.patch
Patch15: 0005-xfree86-Allow-overriding-primary-GPU-detection-from-.patch
Patch16: 0006-xfree86-Add-ModulePath-support-for-OutputClass-confi.patch

# From Debian use intel ddx driver only for gen4 and older chipsets
%if 0%{?fedora} > 25
Patch20: 06_use-intel-only-on-pre-gen4.diff
%endif

#Patch6044: xserver-1.6.99-hush-prerelease-warning.patch

Patch7025: 0001-Always-install-vbe-and-int10-sdk-headers.patch

# Submitted upstream, but not going anywhere
Patch7027: xserver-autobind-hotplug.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1384486
Patch8000: 0001-xfree86-Take-input-lock-for-xf86TransparentCursor.patch
Patch8001: 0001-xfree86-Take-the-input-lock-for-xf86RecolorCursor.patch
Patch8002: 0001-xfree86-Take-input_lock-for-xf86ScreenCheckHWCursor.patch

# because the display-managers are not ready yet, do not upstream
Patch10000: 0001-Fedora-hack-Make-the-suid-root-wrapper-always-start-.patch

%global moduledir	%{_libdir}/xorg/modules
%global drimoduledir	%{_libdir}/dri
%global sdkdir		%{_includedir}/xorg

%ifarch s390 s390x
%global with_hw_servers 0
%else
%global with_hw_servers 1
%endif

%if %{with_hw_servers}
%global enable_xorg --enable-xorg
%else
%global enable_xorg --disable-xorg
%endif

%ifnarch %{ix86} x86_64
%global no_int10 --disable-vbe --disable-int10-module
%endif

%global kdrive --enable-kdrive --enable-xephyr --disable-xfake --disable-xfbdev
%global xservers --enable-xvfb --enable-xnest %{kdrive} %{enable_xorg}

BuildRequires: systemtap-sdt-devel
BuildRequires: git
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.17

BuildRequires: xorg-x11-proto-devel >= 7.7-10
BuildRequires: xorg-x11-font-utils >= 7.2-11

BuildRequires: dbus-devel libepoxy-devel systemd-devel
BuildRequires: xorg-x11-xtrans-devel >= 1.3.2
BuildRequires: libXfont2-devel libXau-devel libxkbfile-devel libXres-devel
BuildRequires: libfontenc-devel libXtst-devel libXdmcp-devel
BuildRequires: libX11-devel libXext-devel
BuildRequires: libXinerama-devel libXi-devel

# DMX config utils buildreqs.
BuildRequires: libXt-devel libdmx-devel libXmu-devel libXrender-devel
BuildRequires: libXi-devel libXpm-devel libXaw-devel libXfixes-devel

BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel
BuildRequires: pkgconfig(wayland-client) >= 1.3.0
BuildRequires: pkgconfig(epoxy)
%if !0%{?rhel}
BuildRequires: pkgconfig(xshmfence) >= 1.1
%endif
BuildRequires: libXv-devel
BuildRequires: pixman-devel >= 0.30.0
BuildRequires: libpciaccess-devel >= 0.13.1 openssl-devel bison flex flex-devel
BuildRequires: mesa-libGL-devel >= 9.2
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libgbm-devel
# XXX silly...
BuildRequires: libdrm-devel >= 2.4.0 kernel-headers

BuildRequires: audit-libs-devel libselinux-devel >= 2.0.86-1
BuildRequires: libudev-devel
%if !0%{?rhel}
# libunwind is Exclusive for the following arches
%ifarch aarch64 %{arm} hppa ia64 mips ppc ppc64 %{ix86} x86_64
BuildRequires: libunwind-devel
%endif
%endif

BuildRequires: pkgconfig(xcb-aux) pkgconfig(xcb-image) pkgconfig(xcb-icccm)
BuildRequires: pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)

# All server subpackages have a virtual provide for the name of the server
# they deliver.  The Xorg one is versioned, the others are intentionally
# unversioned.

%description
X.Org X11 X server


%package common
Summary: Xorg server common files
Group: User Interface/X
Requires: pixman >= 0.30.0
Requires: xkeyboard-config xkbcomp

%description common
Common files shared among all X servers.


%if %{with_hw_servers}
%package Xorg
Summary: Xorg X server
Group: User Interface/X
Provides: Xorg = %{version}-%{release}
Provides: Xserver
# HdG: This should be moved to the wrapper package once the wrapper gets
# its own sub-package:
Provides: xorg-x11-server-wrapper = %{version}-%{release}
%if !0%{?gitdate} || %{stable_abi}
Provides: xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides: xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides: xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides: xserver-abi(extension-%{extension_major}) = %{extension_minor}
%endif
%if 0%{?gitdate}
Provides: xserver-abi(ansic-%{git_ansic_major}) = %{git_ansic_minor}
Provides: xserver-abi(videodrv-%{git_videodrv_major}) = %{git_videodrv_minor}
Provides: xserver-abi(xinput-%{git_xinput_major}) = %{git_xinput_minor}
Provides: xserver-abi(extension-%{git_extension_major}) = %{git_extension_minor}
%endif
Obsoletes: xorg-x11-glamor < %{version}-%{release}
Provides: xorg-x11-glamor = %{version}-%{release}
Obsoletes: xorg-x11-drv-modesetting < %{version}-%{release}
Provides: xorg-x11-drv-modesetting = %{version}-%{release}
%if 0%{?fedora} > 24
# Dropped from F25
Obsoletes: xorg-x11-drv-vmmouse < 13.1.0-4
%endif

Requires: xorg-x11-server-common >= %{version}-%{release}
Requires: system-setup-keyboard

%description Xorg
X.org X11 is an open source implementation of the X Window System.  It
provides the basic low level functionality which full fledged
graphical user interfaces (GUIs) such as GNOME and KDE are designed
upon.
%endif


%package Xnest
Summary: A nested server
Group: User Interface/X
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xnest

%description Xnest
Xnest is an X server which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.


%package Xdmx
Summary: Distributed Multihead X Server and utilities
Group: User Interface/X
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xdmx

%description Xdmx
Xdmx is proxy X server that provides multi-head support for multiple displays
attached to different machines (each of which is running a typical X server).
When Xinerama is used with Xdmx, the multiple displays on multiple machines
are presented to the user as a single unified screen.  A simple application
for Xdmx would be to provide multi-head support using two desktop machines,
each of which has a single display device attached to it.  A complex
application for Xdmx would be to unify a 4 by 4 grid of 1280x1024 displays
(each attached to one of 16 computers) into a unified 5120x4096 display.


%package Xvfb
Summary: A X Windows System virtual framebuffer X server
Group: User Interface/X
# xvfb-run is GPLv2, rest is MIT
License: MIT and GPLv2
Requires: xorg-x11-server-common >= %{version}-%{release}
# required for xvfb-run
Requires: xorg-x11-xauth
Provides: Xvfb

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on
machines with no display hardware and no physical input devices.
Xvfb simulates a dumb framebuffer using virtual memory.  Xvfb does
not open any devices, but behaves otherwise as an X display.  Xvfb
is normally used for testing servers.


%package Xephyr
Summary: A nested server
Group: User Interface/X
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xephyr

%description Xephyr
Xephyr is an X server which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.  Unlike
Xnest, Xephyr renders to an X image rather than relaying the
X protocol, and therefore supports the newer X extensions like
Render and Composite.


%package Xwayland
Summary: Wayland X Server
Group: User Interface/X
Requires: xorg-x11-server-common >= %{version}-%{release}

%description Xwayland
Xwayland is an X server for running X clients under Wayland.


%if %{with_hw_servers}
%package devel
Summary: SDK for X server driver module development
Group: User Interface/X
Requires: xorg-x11-util-macros
Requires: xorg-x11-proto-devel
Requires: libXfont2-devel
Requires: pkgconfig pixman-devel libpciaccess-devel
Provides: xorg-x11-server-static
Obsoletes: xorg-x11-glamor-devel < %{version}-%{release}
Provides: xorg-x11-glamor-devel = %{version}-%{release}

%description devel
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.
%endif


%package source
Summary: Xserver source code required to build VNC server (Xvnc)
Group: Development/Libraries
BuildArch: noarch

%description source
Xserver source code needed to build VNC server (Xvnc)


%prep
%autosetup -N -n %{pkgname}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
rm -rf .git
cp %{SOURCE1} .gitignore
# ick
%global __scm git
%{expand:%__scm_setup_git -q}
%autopatch

%if %{with_hw_servers} && 0%{?stable_abi}
# check the ABI in the source against what we expect.
getmajor() {
    grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $4 }'
}

getminor() {
    grep -i ^#define.ABI.$1_VERSION hw/xfree86/common/xf86Module.h |
    tr '(),' '   ' | awk '{ print $5 }'
}

test `getmajor ansic` == %{ansic_major}
test `getminor ansic` == %{ansic_minor}
test `getmajor videodrv` == %{videodrv_major}
test `getminor videodrv` == %{videodrv_minor}
test `getmajor xinput` == %{xinput_major}
test `getminor xinput` == %{xinput_minor}
test `getmajor extension` == %{extension_major}
test `getminor extension` == %{extension_minor}

%endif

%build

%global default_font_path "catalogue:/etc/X11/fontpath.d,built-ins"

%if %{with_hw_servers}
%global dri_flags --enable-dri --enable-dri2 %{?!rhel:--enable-dri3} --enable-suid-wrapper --enable-glamor
%else
%global dri_flags --disable-dri --disable-dri2
%endif

%if 0%{?fedora}
%global bodhi_flags --with-vendor-name="Fedora Project"
%global wayland --enable-xwayland
%endif

# ick
%if 0%{?rhel}
sed -i 's/WAYLAND_SCANNER_RULES.*//g' configure.ac
%endif

# --with-pie ?
autoreconf -f -v --install || exit 1
# export CFLAGS="${RPM_OPT_FLAGS}"
# XXX without dtrace

%configure %{xservers} \
	--enable-dependency-tracking \
	--disable-static \
	--with-pic \
	%{?no_int10} --with-int10=x86emu \
	--with-default-font-path=%{default_font_path} \
	--with-module-dir=%{moduledir} \
	--with-builderstring="Build ID: %{name} %{version}-%{release}" \
	--with-os-name="$(hostname -s) $(uname -r)" \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
        --without-dtrace \
	--disable-linux-acpi --disable-linux-apm \
	--enable-xselinux --enable-record --enable-present \
	--enable-config-udev \
	--disable-unit-tests \
	--enable-dmx \
	%{?wayland} \
	%{dri_flags} %{?bodhi_flags} \
	${CONFIGURE}
        
make V=1 %{?_smp_mflags}


%install
%make_install moduledir=%{moduledir}

%if %{with_hw_servers}
rm -rf $RPM_BUILD_ROOT%{_libdir}/xorg/modules/multimedia/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/xserver

mkdir -p $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d

# make sure the (empty) /etc/X11/xorg.conf.d is there, system-setup-keyboard
# relies on it more or less.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d

mkdir -p $RPM_BUILD_ROOT%{_bindir}

%if %{stable_abi}
install -m 755 %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%else
sed -e s/@MAJOR@/%{gitdate}/g -e s/@MINOR@/%{minor_serial}/g %{SOURCE31} > \
    $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
chmod 755 $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%endif

%endif

# Make the source package
%global xserver_source_dir %{_datadir}/xorg-x11-server-source
%global inst_srcdir %{buildroot}/%{xserver_source_dir}
mkdir -p %{inst_srcdir}/{Xext,xkb,GL,hw/{xquartz/bundle,xfree86/common}}
mkdir -p %{inst_srcdir}/{hw/dmx/doc,man,doc,hw/dmx/doxygen}
cp {,%{inst_srcdir}/}hw/xquartz/bundle/cpprules.in
cp {,%{inst_srcdir}/}man/Xserver.man
cp {,%{inst_srcdir}/}doc/smartsched
cp {,%{inst_srcdir}/}hw/dmx/doxygen/doxygen.conf.in
cp {,%{inst_srcdir}/}xserver.ent.in
cp {,%{inst_srcdir}/}hw/xfree86/Xorg.sh.in
cp xkb/README.compiled %{inst_srcdir}/xkb
cp hw/xfree86/xorgconf.cpp %{inst_srcdir}/hw/xfree86

install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT%{_bindir}/xvfb-run

find . -type f | egrep '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' |
xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
# SLEDGEHAMMER
find %{inst_srcdir}/hw/xfree86 -name \*.c -delete

# Remove unwanted files/dirs
{
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/Options
    rm -f $RPM_BUILD_ROOT%{_bindir}/in?
    rm -f $RPM_BUILD_ROOT%{_bindir}/ioport
    rm -f $RPM_BUILD_ROOT%{_bindir}/out?
    rm -f $RPM_BUILD_ROOT%{_bindir}/pcitweak
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcitweak.1*
    find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
%if !%{with_hw_servers}
    rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/xorg-server.pc
    rm -f $RPM_BUILD_ROOT%{_datadir}/aclocal/xorg-server.m4
    rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/xorg-server
%endif
# wtf
%ifnarch %{ix86} x86_64
    rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/lib{int10,vbe}.so
%endif
}


%files common
%doc COPYING
%{_mandir}/man1/Xserver.1*
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

%if 1
%global Xorgperms %attr(4755, root, root)
%else
# disable until module loading is audited
%global Xorgperms %attr(0711,root,root) %caps(cap_sys_admin,cap_sys_rawio,cap_dac_override=pe)
%endif

%if %{with_hw_servers}
%files Xorg
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/X
%{_bindir}/Xorg
%{_libexecdir}/Xorg
%{Xorgperms} %{_libexecdir}/Xorg.wrap
%{_bindir}/cvt
%{_bindir}/gtf
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%{_libdir}/xorg/modules/drivers/modesetting_drv.so
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libglx.so
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libglamoregl.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libwfb.so
%ifarch %{ix86} x86_64
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libvbe.so
%endif
%{_mandir}/man1/gtf.1*
%{_mandir}/man1/Xorg.1*
%{_mandir}/man1/Xorg.wrap.1*
%{_mandir}/man1/cvt.1*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man4/exa.4*
%{_mandir}/man4/modesetting.4*
%{_mandir}/man5/Xwrapper.config.5*
%{_mandir}/man5/xorg.conf.5*
%{_mandir}/man5/xorg.conf.d.5*
%dir %{_sysconfdir}/X11/xorg.conf.d
%dir %{_datadir}/X11/xorg.conf.d
%{_datadir}/X11/xorg.conf.d/10-quirks.conf
%endif


%files Xnest
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.1*

%files Xdmx
%{_bindir}/Xdmx
%{_bindir}/dmxaddinput
%{_bindir}/dmxaddscreen
%{_bindir}/dmxreconfig
%{_bindir}/dmxresize
%{_bindir}/dmxrminput
%{_bindir}/dmxrmscreen
%{_bindir}/dmxtodmx
%{_bindir}/dmxwininfo
%{_bindir}/vdltodmx
%{_bindir}/dmxinfo
%{_bindir}/xdmxconfig
%{_mandir}/man1/Xdmx.1*
%{_mandir}/man1/dmxtodmx.1*
%{_mandir}/man1/vdltodmx.1*
%{_mandir}/man1/xdmxconfig.1*

%files Xvfb
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.1*

%files Xephyr
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1*

%files Xwayland
%{_bindir}/Xwayland

%if %{with_hw_servers}
%files devel
%doc COPYING
#{_docdir}/xorg-server
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{sdkdir}/*.h
%{_datadir}/aclocal/xorg-server.m4
%endif

%files source
%{xserver_source_dir}


%changelog
* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.19.1-3
- Fix a few input thread lock issues causing intel crashes (#1384486)

* Mon Jan 16 2017 Adam Jackson <ajax@redhat.com> - 1.19.1-2
- Limit the intel driver only on F26 and up

* Wed Jan 11 2017 Adam Jackson <ajax@redhat.com> - 1.19.1-1
- xserver 1.19.1

* Tue Jan 10 2017 Hans de Goede <hdegoede@redhat.com> - 1.19.0-4
- Follow Debian and only default to the intel ddx on gen4 or older intel GPUs

* Tue Dec 20 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-3
- Add one more patch for better integration with the nvidia binary driver

* Thu Dec 15 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-2
- Add some patches for better integration with the nvidia binary driver
- Add a patch from upstream fixing a crash (rhbz#1389886)

* Wed Nov 23 2016 Olivier Fourdan <ofourdan@redhat.com> 1.19.0-1
- xserver 1.19.0
- Fix use after free of cursors in Xwayland (rhbz#1385258)
- Fix an issue where some monitors would show only black, or
  partially black when secondary GPU outputs are used

* Tue Nov 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.19.0-0.8.rc2
- Update device barriers for new master devices (#1384432)

* Thu Nov  3 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.7.rc2
- Update to 1.19.0-rc2
- Fix (hopefully) various crashes in FlushAllOutput() (rhbz#1382444)
- Fix Xwayland crashing in glamor on non glamor capable hw (rhbz#1390018)

* Tue Nov  1 2016 Ben Crocker <bcrocker@redhat.com> - 1.19.0-0.6.20161028
- Fix Config record allocation during startup: if xorg.conf.d directory
- was absent, a segfault resulted.

* Mon Oct 31 2016 Adam Jackson <ajax@redhat.com> - 1.19.0-0.5.20161026
- Use %%autopatch instead of doing our own custom git-am trick

* Fri Oct 28 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.4.20161026
- Add missing Requires: libXfont2-devel to -devel sub-package (rhbz#1389711)

* Wed Oct 26 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.3.20161026
- Sync with upstream git, bringing in a bunch if bug-fixes
- Add some extra fixes which are pending upstream
- This also adds PointerWarping emulation to Xwayland, which should improve
  compatiblity with many games

* Wed Oct  5 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.2.20160929
- Add a fix from upstream to fix xterm crash under Xwayland (fdo#97974)
- Add a fix from upstream to fix glamor / xwayland not working with glvnd
- Add a fix from upstream to fix input devices no longer working
  after a vt-switch

* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> - 1.19.0-0.1.20160929
- Rebase to current git master (1.19-rc1+)
- Drop Obsoletes for the driver packages removed from F21 (its been 2
  years since they have been removed now)

* Thu Sep 08 2016 Adam Jackson <ajax@redhat.com> 1.18.4-6
- Backport GLX_EXT_libglvnd support from 1.19

* Thu Sep 01 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.18.4-5
- Fall back to libinput if the module is missing

* Thu Aug 25 2016 Hans de Goede <hdegoede@redhat.com> - 1.18.4-4
- Fix (undo) server ABI breakage from 1.18.4-3

* Thu Aug 25 2016 Hans de Goede <hdegoede@redhat.com> - 1.18.4-3
- Various switchable-graphics / prime fixes from upstream, mostly
  related to using the modesetting driver in prime setups
- Fix Xorg -configure not working (rhbz#1368502)

* Fri Aug 19 2016 Kalev Lember <klember@redhat.com> - 1.18.4-2
- Backport a number of XWayland fixes from master

* Tue Jul 19 2016 Adam Jackson <ajax@redhat.com> - 1.18.4-1
- xserver 1.18.4

* Mon Jul 04 2016 Olivier Fourdan <ofourdan@redhat.com> 1.18.3-8
- Fix segfault in Xwayland due to cursor update after unrealize (#1338979)

* Tue Jun 28 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.18.3-7
- Fix segfault caused by forced indicator update (#1335439)

* Fri Jun 17 2016 Hans de Goede <hdegoede@redhat.com> - 1.18.3-6
- Add switchable-graphics / prime fixes from f24 branch
- Add some more switchable-graphics / prime fixes from upstream

* Mon Jun 13 2016 Adam Jackson <ajax@redhat.com> - 1.18.3-5
- Restore DRI1 for now

* Mon May 09 2016 Adam Jackson <ajax@redhat.com> - 1.18.3-4
- Move a symbol from DRI1 to DRI2 code to fix ati/openchrome

* Thu May 05 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.18.3-3
- Fix NumLock indicator light turning off after layout change (#1047151)

* Thu Apr 14 2016 Adam Jackson <ajax@redhat.com> - 1.18.3-2
- Stop building DRI1 support
- Don't build DRI2 on s390{,x}

* Mon Apr 04 2016 Adam Jackson <ajax@redhat.com> 1.18.3-1
- xserver 1.18.3

* Thu Mar 17 2016 Adam Jackson <ajax@redhat.com> 1.18.2-2
- Fix red tint artifacts in glamor
- Fix a performance cliff in present triggered by plasma
- Silence some xf86vidmode log spam

* Fri Mar 11 2016 Adam Jackson <ajax@redhat.com> 1.18.2-1
- xserver 1.18.2

* Wed Mar 09 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.18.1-3
- Stop bug warnings on three-finger pinch gestures (#1282252)

* Mon Feb 15 2016 Dave Airlie <airlied@redhat.com> 1.18.1-2
- fix issues with reverse prime and present.

* Mon Feb 08 2016 Adam Jackson <ajax@redhat.com> 1.18.1-1
- xserver 1.18.1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Hans de Goede <hdegoede@redhat.com> - 1.18.0-2
- Fix Xorg.wrap kms detection to so that the server does not always run
  as root

* Mon Nov 09 2015 Adam Jackson <ajax@redhat.com> 1.18.0-1
- xserver 1.18.0

* Tue Oct 27 2015 Dave Airlie <airlied@redhat.com> 1.18.0-0.6
- update to git snapshot of 1.7.99.902 (1.18.0 rc2)

* Wed Oct 14 2015 Hans de Goede <hdegoede@redhat.com> - 1.18.0-0.5
- Fix xorg sometimes crashing on machine poweroff/shutdown (#1269210)

* Thu Sep 24 2015 Rex Dieter <rdieter@fedoraproject.org> 1.18.0-0.4
- pull in candidate fix for clients getting stuck waiting indefinitely
  for an idle event when a CRTC is turned off (#1256082,#1258084)

* Tue Sep 22 2015 Dave Airlie <airlied@redhat.com> 1.18.0-0.3
- hack to fix GLX_MESA_copy_sub_buffer regression (#1265395)

* Mon Sep 07 2015 Dave Airlie <airlied@redhat.com> 1.18.0-0.2
- update to git snapshot of 1.7.99 (1.18.0 rc1)

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> 1.18.0-0.1
- git snapshot of what will be 1.18.0 (should be ABI stable)

* Wed Jul 15 2015 Dave Airlie <airlied@redhat.com> 1.17.2-2
- fix bug with glamor and PRIME where server would crash

* Tue Jun 16 2015 Adam Jackson <ajax@redhat.com> 1.17.2-1
- xserver 1.17.2

* Tue Jun 16 2015 Dave Airlie <airlied@redhat.com> 1.17.1-16
- fix bug with glamor and overlapping copies

* Wed Jun 10 2015 Ray Strode <rstrode@redhat.com> 1.17.1-15
- CVE-2015-3164

* Tue May 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.17.1-14
- Add the unaccelerated valuator masks, fixes nonmoving mouse in SDL
  (#1208992)

* Wed May 20 2015 Kalev Lember <kalevlember@gmail.com> - 1.17.1-13
- Obsolete xorg-x11-drv-void

* Tue May 19 2015 Hans de Goede <hdegoede@redhat.com> - 1.17.1-12
- Fix "start -- vt7" not working fix breaking headless setups (#1203780)

* Sat May 02 2015 Adel Gadllah <adel.gadllah@gmail.com> - 1.17.1-11
- modesetting: Fix software cursor fallback (#1205725)

* Thu Apr 30 2015 Hans de Goede <hdegoede@redhat.com> - 1.17.1-10
- Fix "start -- vt7" not working (#1203780)

* Sat Apr 11 2015 Ray Strode <rstrode@redhat.com> 1.17.1-9
- Handle logind timeouts more gracefuly.
- Bump timeouts so they don't happen in practice
  Fixes X on some old optimus and other hybrid hardware
  Related: #1209347

* Thu Apr 09 2015 Adam Jackson <ajax@redhat.com> 1.17.1-8
- Fix endian detection code (#1206060)

* Wed Mar 18 2015 Hans de Goede <hdegoede@redhat.com> - 1.17.1-7
- Modify the server wrapper to not always start the server as root.
  Callers of the server which start it in a way which is compatible with the
  server running without root rights can now set a XORG_RUN_AS_USER_OK env
  variable and then the wrapper will behave as if needs_root_rights = auto
  is specified, unless overriden from Xwrapper.config

* Wed Mar 04 2015 Adam Jackson <ajax@redhat.com> 1.17.1-6
- Fix int10 interrupt vector setup

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 1.17.1-5
- omg, define something to 0 makes it work, security.

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 1.17.1-4
- require lazy relocations to work, remove cement

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.17.1-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Dave Airlie <airlied@redhat.com> 1.17.1-2
- fix regression in SI:localuser handling

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 1.17.1-1
- New upstream release 1.17.1 (rhbz#1144404)
- xorg-x11-drv-modesetting is now included in xorg-x11-server-Xorg,
  obsolete it
- Fix xorg-x11-drv-r128 obsoletes (rhbz#1176791)

* Fri Feb 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.16.2.901-3
- CVE-2015-0255: unchecked XKB string lengths

* Thu Feb 05 2015 Ray Strode <rstrode@redhat.com> 1.16.2.901-2
- Add patch from ickle to fix flicker on login / durin vt switch
  see https://bugzilla.gnome.org/show_bug.cgi?id=737226

* Wed Dec 10 2014 Dave Airlie <airlied@redhat.com> 1.16.2.901-1
- upstream security release. 1.16.2.901

* Fri Nov 21 2014 Dave Airlie <airlied@redhat.com> 1.16.2-1
- New upstream bugfix release 1.16.2

* Fri Nov 21 2014 Dave Airlie <airlied@redhat.com> 1.16.1-2
- backport glamor DRI3 sync integration from upstream

* Fri Oct  3 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.1-1
- New upstream bugfix release 1.16.1 (rhbz#1144404)

* Thu Sep 11 2014 Adam Jackson <ajax@redhat.com> 1.16.0-10
- Only send GLX_BufferSwapComplete for PresentCompleteKindPixmap

* Wed Sep 10 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-9
- Fixup Xwayland summary, remove . at end of summaries (rhbz#1140225)

* Tue Sep 09 2014 Kalev Lember <kalevlember@gmail.com> - 1.16.0-8
- Update the versions of obsoletes for dropped drivers

* Tue Sep  2 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-7
- Drop Fedora specific xorg-non-pci.patch, replace with solution from
  upstream

* Thu Aug 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-6
- drop no longer valid configure arguments (rhbz#1133350)

* Mon Aug 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.16.0-5
- re-add support for non pci platform devices

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  8 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-3
- Really fix conditionals to allow building on F-20 (rhbz#1127351)

* Thu Aug  7 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-2
- Fix xwayland conditionals to allow building on F-20 (rhbz#1127351)

* Mon Jul 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Thu Jul 17 2014 Adam Jackson <ajax@redhat.com> 1.15.99.904-4
- Add Obsoletes for video drivers dropped in F21+

* Fri Jul 11 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.904-3
- Fix startx crash introduced by 1.15.99.904 (rhbz#1118540)

* Fri Jul 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.15.99.904-2
- Don't force the screensaver off on DPMS unblank

* Tue Jul  8 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.904-1
- Update to 1.15.99.904

* Wed Jul  2 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.903-5
- Fix code including glamor.h not compiling due to strndup re-definition

* Wed Jul 02 2014 Adam Jackson <ajax@redhat.com> 1.15.99.903-4
- Snap xwayland damage reports to the bounding box

* Wed Jul  2 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.903-3
- Fix xvfb crash on client disconnect (rhbz#1113128)

* Thu Jun 19 2014 Dennis Gilmore <dennis@ausil.us> - 1.15.99.903-2
- add support for non pci platform devices

* Wed Jun 11 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.903-1
- Update to 1.15.99.903
- This bumps the videodrv ABI once more, so all drivers must be rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.99.902-8.20140428
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Adam Jackson <ajax@redhat.com> 1.15.99.902-7
- Don't try to build Xwayland in F20
- Fix shadowfb initialization to, er, work

* Wed May 14 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.15.99.902-6.20140428
- Revert button mapping for Evoluent Vertical mouse, the default mapping
  matches the manufacturer's documentation (#612140)

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.902-5.20140428
- Add hw/xfree86/Xorg.sh.in to xorg-x11-server-source

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.902-4.20140428
- Git snapshot 20140428
- This fixes the silent hardware cursor API break in 1.15.99.902 (#1090897)

* Fri Apr 25 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.902-3
- Add missing BuildRequires for dbus-devel, libepoxy-devel, mesa-libEGL-devel,
  mesa-libgbm-devel and systemd-devel
- Fix compilation of int10 module on arm

* Wed Apr 23 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.902-2
- Add --enable-glamor to configure flags

* Thu Apr 17 2014 Hans de Goede <hdegoede@redhat.com> - 1.15.99.902-1
- Update to 1.15.99.902
- Drop the Xwayland as extension patch-set
- Add a new xorg-x11-server-Xwayland package with the new standalone Xwayland
  server

* Fri Feb 28 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.15.0-5
- Search all parent devices for a PnPID.

* Mon Feb 17 2014 Adam Williamson <awilliam@redhat.com> - 1.15.0-4
- fix xwayland crash under mutter (RH #1065109 , BGO #724443)

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.15.0-3
- Prevent out-of-bounds access in check_butmap_change (#1061466)

* Tue Jan 14 2014 Adam Jackson <ajax@redhat.com> 1.15.0-2
- exa-only-draw-valid-trapezoids.patch: Fix crash in exa.

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> 1.15.0-1
- xserver 1.15.0

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> 1.14.99.904-1
- 1.15RC4
- Re-disable int10 on arm

* Mon Dec  2 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.99.902-2
- Add aarch64 to platforms that have libunwind

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> 1.14.99.902-1
- 1.15RC2

* Mon Nov 18 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-6
- Prefer fbdev to vesa, fixes fallback path on UEFI

* Fri Nov 08 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-5
- Restore XkbCopyDeviceKeymap for (older) tigervnc

* Fri Nov 08 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-4
- Explicitly enable DRI2

* Thu Nov 07 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-3
- Merge Xinerama+{Damage,Render,Composite} fix series

* Thu Nov 07 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-2
- Fix build with --disable-present

* Thu Nov 07 2013 Adam Jackson <ajax@redhat.com
- Don't bother trying to build the unit tests for now

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> 1.14.99.901-1
- 1.15RC1

* Mon Oct 28 2013 Adam Jackson <ajax@redhat.com> 1.14.99.3-2
- Don't build xwayland in RHEL

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> 1.14.99.3-1
- xserver 1.14.99.3
- xwayland branch refresh
- Drop some F17-era Obsoletes
- Update BuildReqs to match reality

* Wed Oct 23 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.3-6
- Fix Xdmx cursor jumps (#1019821)

* Tue Oct 08 2013 Adam Jackson <ajax@redhat.com> 1.14.3-5
- Snap wayland damage reports to the bounding box

* Thu Oct 03 2013 Adam Jackson <ajax@redhat.com> 1.14.3-4
- Fix up fixing up the driver list after filtering out non-wayland

* Wed Oct 02 2013 Adam Jackson <ajax@redhat.com> 1.14.3-3
- Only look at wayland-capable drivers when run with -wayland

* Mon Sep 23 2013 Adam Jackson <ajax@redhat.com> 1.14.3-2
- xwayland support

* Mon Sep 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.3-1
- xserver 1.14.3

* Tue Jul 30 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-9
- Fix active touch grabs, second touchpoint didn't get sent to client
- Fix version mismatch for XI 2.2+ clients (where a library supports > 2.2
  but another version than the originally requested one).

* Tue Jul 30 2013 Dave Airlie <airlied@redhat.com> 1.14.2-8
- fixes for multi-monitor reverse optimus

* Mon Jul 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-7
- Fix erroneous valuator 1 coordinate when an absolute device in relative
  mode doesn't send y coordinates.

* Fri Jul 19 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-6
- Add new version of the resolution-based scaling patch - scale y down
  instead of x up. That gives almost the same behaviour as current
  synaptics. Drop the synaptics quirk, this needs to be now removed from the
  driver.

* Mon Jul 15 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-5
- Fix logspam when trying to free a non-existant grab.
- Update touch patch to upstream version (from fdo #66720)
- re-add xephyr resizable patch, got lost in rebase (#976995)

* Fri Jul 12 2013 Dave Airlie <airlied@redhat.com> 1.14.2-4
- reapply dropped patch to fix regression (#981953)

* Tue Jul 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-3
- Fix crash on 32-bit with virtual box guest additions (#972095)

* Tue Jul 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-2
- Fix crash in gnome-shell when tapping a menu twice (fdo #66720)

* Thu Jul 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.2-1
- xorg-server 1.4.2
- drop merged patches
- Add a quirk to set the synaptics resolution to 0 by default. The pre-scale
  patch in the server clashes with synaptics inaccurate resolution numbers,
  causing the touchpad movement to be stunted.

* Thu Jun 06 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.1.901-2
- Backport the touch grab race condition patches from fdo #56578

* Thu Jun 06 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.1.901-1
- xserver 1.14.2RC1

* Tue Jun 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.14.1-4
- Update quirks for trackballs and the La-VIEW Technology Naos 5000 mouse

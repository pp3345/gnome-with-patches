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
%undefine _strict_symbol_defs_build

#global gitdate 20161026
%global stable_abi 1

%if !0%{?gitdate} || %{stable_abi}
# Released ABI versions.  Have to keep these manually in sync with the
# source because rpm is a terrible language.
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 24
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
Version:   1.20.5
Release:   7%{?gitdate:.%{gitdate}}%{?dist}
URL:       http://www.x.org
License:   MIT

#VCS:      git:git://git.freedesktop.org/git/xorg/xserver
%if 0%{?gitdate}
# git snapshot.  to recreate, run:
# ./make-git-snapshot.sh `cat commitid`
Source0:   xorg-server-%{gitdate}.tar.xz
#Source0:   http://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
Source1:   make-git-snapshot.sh
Source2:   commitid
%else
Source0:   https://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
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

# From Debian use intel ddx driver only for gen4 and older chipsets
Patch1: 06_use-intel-only-on-pre-gen4.diff
# Default to xf86-video-modesetting on GeForce 8 and newer
Patch2: 0001-xfree86-use-modesetting-driver-by-default-on-GeForce.patch

# Default to va_gl on intel i965 as we use the modesetting drv there
# va_gl should probably just be the default everywhere ?
Patch3: 0001-xf86-dri2-Use-va_gl-as-vdpau_driver-for-Intel-i965-G.patch

# Submitted upstream, but not going anywhere
Patch5: 0001-autobind-GPUs-to-the-screen.patch

# because the display-managers are not ready yet, do not upstream
Patch6: 0001-Fedora-hack-Make-the-suid-root-wrapper-always-start-.patch

# test for https://bugzilla.redhat.com/show_bug.cgi?id=1697591
# see also https://gitlab.freedesktop.org/xorg/xserver/merge_requests/36
# ofourdan> Disabling those for now, causing regressions (#1714981, #1723715)
#Patch21: 0001-modesetting-Weaksauce-atomic-property-debugging.patch
#Patch22: 0002-modesetting-Propagate-more-failure-in-drmmode_set_mo.patch
#Patch23: 0003-modesetting-Factor-out-drmmode_target_output.patch
#Patch24: 0004-modesetting-Use-atomic-instead-of-per-crtc-walks-whe.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1697804
Patch25: 0001-Xi-return-AlreadyGrabbed-for-key-grabs-255.patch

# From current server-1.20-branch:
# https://bugzilla.redhat.com/1708119
Patch26: 0001-xwayland-Avoid-a-crash-on-pointer-enter-with-a-grab.patch
# https://bugzilla.redhat.com/1691745
Patch27: 0001-xwayland-Check-status-in-GBM-pixmap-creation.patch
# https://bugzilla.redhat.com/1645553
Patch28: 0001-glamor-Make-pixmap-exportable-from-gbm_bo_from_pixma.patch
Patch29: 0001-xwayland-Reset-scheduled-frames-after-hiding-tablet-.patch

# https://gitlab.freedesktop.org/xorg/xserver/issues/839
# https://bugzilla.redhat.com/1726419
Patch30: 0001-Revert-present-scmd-Check-that-the-flip-and-screen-p.patch

# Build failure with recent glibc
# https://gitlab.freedesktop.org/xorg/xserver/issues/840
Patch31: 0001-compiler.h-Do-not-include-sys-io.h-on-ARM-with-glibc.patch

Patch32: 0001-Xi-Use-current-device-active-grab-to-deliver-touch-e.patch
Patch33: 0002-dri2-Sync-i965_pci_ids.h-from-mesa.patch
Patch34: 0003-xwayland-Update-screen-pixmap-on-output-resize.patch
Patch35: 0004-xwayland-Expand-the-RANDR-screen-size-limits.patch
# https://bugzilla.redhat.com/1729925
Patch36: 0005-xwayland-Do-not-free-a-NULL-GBM-bo.patch
Patch37: 0006-xsync-Add-resource-inside-of-SyncCreate-export-SyncC.patch
Patch38: 0007-GLX-Add-a-per-client-vendor-mapping.patch
Patch39: 0008-GLX-Use-the-sending-client-for-looking-up-XID-s.patch
Patch40: 0009-GLX-Add-a-function-to-change-a-clients-vendor-list.patch
Patch41: 0010-GLX-Set-GlxServerExports-major-minor-Version.patch
Patch42: 0011-miext-sync-Fix-needless-ABI-change.patch
Patch43: 0012-glx-Fix-previous-context-validation-in-xorgGlxMakeCu.patch
Patch44: 0013-xwayland-Separate-DamagePtr-into-separate-window-dat.patch
Patch45: 0014-xwayland-Refactor-surface-creation-into-a-separate-f.patch
Patch46: 0015-xwayland-Handle-the-case-of-windows-being-realized-b.patch

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
BuildRequires: pkgconfig(wayland-eglstream-protocols)
BuildRequires: pkgconfig(wayland-client) >= 1.3.0
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(xshmfence) >= 1.1
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
# libunwind is Exclusive for the following arches
%ifarch aarch64 %{arm} hppa ia64 mips ppc ppc64 %{ix86} x86_64
%if !0%{?rhel}
BuildRequires: libunwind-devel
%endif
%endif

BuildRequires: pkgconfig(xcb-aux) pkgconfig(xcb-image) pkgconfig(xcb-icccm)
BuildRequires: pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)

%description
X.Org X11 X server


%package common
Summary: Xorg server common files
Requires: pixman >= 0.30.0
Requires: xkeyboard-config xkbcomp

%description common
Common files shared among all X servers.


%package Xorg
Summary: Xorg X server
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
# Dropped from F25
Obsoletes: xorg-x11-drv-vmmouse < 13.1.0-4

Requires: xorg-x11-server-common >= %{version}-%{release}
Requires: system-setup-keyboard
Requires: xorg-x11-drv-libinput
Requires: libEGL

%description Xorg
X.org X11 is an open source implementation of the X Window System.  It
provides the basic low level functionality which full fledged
graphical user interfaces (GUIs) such as GNOME and KDE are designed
upon.


%package Xnest
Summary: A nested server
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
Requires: xorg-x11-server-common >= %{version}-%{release}
Requires: libEGL

%description Xwayland
Xwayland is an X server for running X clients under Wayland.


%package devel
Summary: SDK for X server driver module development
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


%package source
Summary: Xserver source code required to build VNC server (Xvnc)
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

%if 0%{?stable_abi}
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

export CFLAGS="$RPM_OPT_FLAGS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1"
export CXXFLAGS="$RPM_OPT_FLAGS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1"
export LDFLAGS="$RPM_LD_FLAGS -specs=/usr/lib/rpm/redhat/redhat-hardened-ld"

%ifnarch %{ix86} x86_64
%global no_int10 --disable-vbe --disable-int10-module
%endif

%global kdrive --enable-kdrive --enable-xephyr --disable-xfake --disable-xfbdev
%global xservers --enable-xvfb --enable-xnest %{kdrive} --enable-xorg
%global default_font_path "catalogue:/etc/X11/fontpath.d,built-ins"
%global dri_flags --enable-dri --enable-dri2 %{?!rhel:--enable-dri3} --enable-suid-wrapper --enable-glamor
%global bodhi_flags --with-vendor-name="Fedora Project"

autoreconf -f -v --install || exit 1

%configure %{xservers} \
	--enable-dependency-tracking \
        --enable-xwayland-eglstream \
	--disable-static \
	--with-pic \
	%{?no_int10} --with-int10=x86emu \
	--with-default-font-path=%{default_font_path} \
	--with-module-dir=%{_libdir}/xorg/modules \
	--with-builderstring="Build ID: %{name} %{version}-%{release}" \
	--with-os-name="$(hostname -s) $(uname -r)" \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
        --without-dtrace \
	--disable-linux-acpi --disable-linux-apm \
	--enable-xselinux --enable-record --enable-present \
	--enable-config-udev \
	--disable-unit-tests \
	--enable-dmx \
	--enable-xwayland \
	%{dri_flags} %{?bodhi_flags} \
	${CONFIGURE}
        
make V=1 %{?_smp_mflags}


%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/xserver

mkdir -p $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/X11/xorg.conf.d

# make sure the (empty) /etc/X11/xorg.conf.d is there, system-setup-keyboard
# relies on it more or less.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d

%if %{stable_abi}
install -m 755 %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%else
sed -e s/@MAJOR@/%{gitdate}/g -e s/@MINOR@/%{minor_serial}/g %{SOURCE31} > \
    $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
chmod 755 $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%endif

install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT%{_bindir}/xvfb-run

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

find . -type f | egrep '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' |
xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
find %{inst_srcdir}/hw/xfree86 -name \*.c -delete

# Remove unwanted files/dirs
{
    find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
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

%files devel
%doc COPYING
#{_docdir}/xorg-server
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/*.h
%{_datadir}/aclocal/xorg-server.m4

%files source
%{xserver_source_dir}


%changelog
* Thu Aug 29 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-7
- Pick latest fixes from xserver stable branch upstream (rhbz#1729925)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  8 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-5
- Do not include <sys/io.h> on ARM with glibc to avoid compilation failure.
- Do not force vbe and int10 sdk headers as this enables int10 which does
  not build on ARM without <sys/io.h>

* Mon Jul  8 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-4
- Fix regression causing screen tearing with upstream xserver 1.20.5
  (rhbz#1726419)

* Fri Jun 28 2019 Olivier Fourdan <ofourdan@redhat.com> 1.20.5-3
- Remove atomic downstream patches causing regressions (#1714981, #1723715)
- Xwayland crashes (#1708119, #1691745)
- Cursor issue with tablet on Xwayland
- Xorg/modesetting issue with flipping pixmaps with Present (#1645553)

* Thu Jun 06 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.20.5-2
- Return AlreadyGrabbed for keycodes > 255 (#1697804)

* Thu May 30 2019 Adam Jackson <ajax@redhat.com> - 1.20.5-1
- xserver 1.20.5

* Tue Apr 23 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-4
- Fix some non-atomic modesetting calls to be atomic

* Wed Mar 27 2019 Peter Hutterer <peter.hutterer@redhat.com> 1.20.4-3
- Fix a Qt scrolling bug, don't reset the valuator on slave switch

* Thu Mar 21 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-2
- Backport an Xwayland crash fix in the Present code

* Tue Feb 26 2019 Adam Jackson <ajax@redhat.com> - 1.20.4-1
- xserver 1.20.4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Olivier Fourdan <ofourdan@redhat.com> - 1.20.3-3
- More Xwayland/Present fixes from upstream (rhbz#1609181, rhbz#1661748)

* Thu Dec 06 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.20.3-2
- Xwayland/Present fixes from master upstream

* Thu Nov 01 2018 Adam Jackson <ajax@redhat.com> - 1.20.3-1
- xserver 1.20.3

* Mon Oct 15 2018 Adam Jackson <ajax@redhat.com> - 1.20.2-1
- xserver 1.20.2

* Thu Oct  4 2018 Hans de Goede <hdegoede@redhat.com> - 1.20.1-4
- Rebase patch to use va_gl as vdpau driver on i965 GPUs, re-fix rhbz#1413733

* Thu Sep 13 2018 Dave Airlie <airlied@redhat.com> - 1.20.1-3
- Build with PIE enabled (this doesn't enable bind now)

* Mon Sep 10 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.20.1-2
- Include patches from upstream to fix Xwayland crashes

* Thu Aug 09 2018 Adam Jackson <ajax@redhat.com> - 1.20.1-1
- xserver 1.20.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-4
- Xorg and Xwayland Requires: libEGL

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 1.20.0-3
- Backport fixes for RHBZ#1579067

* Wed May 16 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-2
- Xorg Requires: xorg-x11-drv-libinput

* Thu May 10 2018 Adam Jackson <ajax@redhat.com> - 1.20.0-1
- xserver 1.20

* Wed Apr 25 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.905-2
- Fix xvfb-run's default depth to be 24

* Tue Apr 24 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.905-1
- xserver 1.20 RC5

* Thu Apr 12 2018 Olivier Fourdan <ofourdan@redhat.com> - 1.19.99.904-2
- Re-fix "use type instead of which in xvfb-run (rhbz#1443357)" which
  was overridden inadvertently

* Tue Apr 10 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.904-1
- xserver 1.20 RC4

* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 1.19.99.903-1
- xserver 1.20 RC3

* Tue Feb 13 2018 Olivier Fourdan <ofourdan@redhat.com> 1.19.6-5
- xwayland: avoid race condition on new keymap
- xwayland: Keep separate variables for pointer and tablet foci (rhbz#1519961)
- xvfb-run now support command line option “--auto-display”

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Olivier Fourdan <ofourdan@redhat.com> 1.19.6-3
- Avoid generating a core file when the Wayland compositor is gone.

* Thu Jan 11 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.19.6-2
- Fix handling of devices with ID_INPUT=null

* Wed Dec 20 2017 Adam Jackson <ajax@redhat.com> - 1.19.6-1
- xserver 1.19.6

* Thu Oct 12 2017 Adam Jackson <ajax@redhat.com> - 1.19.5-1
- xserver 1.19.5

* Thu Oct 05 2017 Olivier Fourdan <ofourdan@redhat.com> - 1.19.4-1
- xserver-1.19.4
- Backport tablet support for Xwayland

* Fri Sep 08 2017 Troy Dawson <tdawson@redhat.com> - 1.19.3-9
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul  2 2017 Ville Skyttä <ville.skytta@iki.fi> - 1.19.3-6
- Use type instead of which in xvfb-run (rhbz#1443357)

* Thu May 04 2017 Orion Poplawski <orion@cora.nwra.com> - 1.19.3-5
- Enable full build for s390/x

* Mon Apr 24 2017 Ben Skeggs <bskeggs@redhat.com> - 1.19.3-4
- Default to xf86-video-modesetting on GeForce 8 and newer

* Fri Apr 07 2017 Adam Jackson <ajax@redhat.com> - 1.19.3-3
- Inoculate against a versioning bug with libdrm 2.4.78

* Thu Mar 23 2017 Hans de Goede <hdegoede@redhat.com> - 1.19.3-2
- Use va_gl as vdpau driver on i965 GPUs (rhbz#1413733)

* Wed Mar 15 2017 Adam Jackson <ajax@redhat.com> - 1.19.3-1
- xserver 1.19.3

* Thu Mar 02 2017 Adam Jackson <ajax@redhat.com> - 1.19.2-1
- xserver 1.19.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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

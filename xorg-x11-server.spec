# This package is an experiment in active integration of upstream SCM with
# Fedora packaging.  It works something like this:
#
# The "pristine" source is actually a git repo (with no working checkout).
# The first step of %%prep is to check it out and switch to a "fedora" branch.
# If you need to add a patch to the server, just do it like a normal git
# operation, dump it with git-format-patch to a file in the standard naming
# format, and add a PatchN: line.  If you want to push something upstream,
# check out the master branch, pull, cherry-pick, and push.  FIXME describe
# rebasing, add convenience 'make' targets maybe.

#define gitdate 20120215
%define stable_abi 1

%if !0%{?gitdate} || %{stable_abi}

# Released ABI versions.  Have to keep these manually in sync with the
# source because rpm is a terrible language.

%define ansic_major 0
%define ansic_minor 4
%define videodrv_major 12
%define videodrv_minor 0
%define xinput_major 16
%define xinput_minor 0
%define extension_major 6
%define extension_minor 0

%else

# For git snapshots, use date for major and a serial number for minor

%define minor_serial 0

%define ansic_major %{gitdate}
%define ansic_minor %{minor_serial}
%define videodrv_major %{gitdate}
%define videodrv_minor %{minor_serial}
%define xinput_major %{gitdate}
%define xinput_minor %{minor_serial}
%define extension_major %{gitdate}
%define extension_minor %{minor_serial}

%endif

%define pkgname xorg-server

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   1.12.2
Release:   1%{?gitdate:.%{gitdate}}%{dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X

#VCS:      git:git://git.freedesktop.org/git/xorg/xserver
%if 0%{?gitdate}
# git snapshot.  to recreate, run:
# ./make-git-snapshot.sh `cat commitid`
Source0:   xorg-server-%{gitdate}.tar.xz
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

# OpenGL compositing manager feature/optimization patches.
# FIXME: who calls this?
#Patch103:  xserver-1.5.0-bg-none-root.patch

# Trivial things to never merge upstream ever:
# This really could be done prettier.
Patch5002: xserver-1.4.99-ssh-isnt-local.patch

# don't build the (broken) acpi code
Patch6011: xserver-1.6.0-less-acpi-brokenness.patch

# ajax needs to upstream this
Patch6027: xserver-1.6.0-displayfd.patch
Patch6030: xserver-1.6.99-right-of.patch
#Patch6044: xserver-1.6.99-hush-prerelease-warning.patch

# Fix libselinux-triggered build error
# RedHat/Fedora-specific patch
Patch7013: xserver-1.12-Xext-fix-selinux-build-failure.patch

# backport pci slot claiming fix for kms drivers
Patch7015: xserver-fix-pci-slot-claims.patch
# backport modesetting fallback driver
Patch7016: xserver-1.12-modesetting-fallback.patch

%define moduledir	%{_libdir}/xorg/modules
%define drimoduledir	%{_libdir}/dri
%define sdkdir		%{_includedir}/xorg

%ifarch s390 s390x %{?rhel:ppc ppc64}
%define with_hw_servers 0
%else
%define with_hw_servers 1
%endif

%if %{with_hw_servers}
%define enable_xorg --enable-xorg
%else
%define enable_xorg --disable-xorg
%endif

%ifnarch %{ix86} x86_64 %{arm}
%define no_int10 --disable-vbe --disable-int10-module
%endif

%define kdrive --enable-kdrive --enable-xephyr --disable-xfake --disable-xfbdev
%define xservers --enable-xvfb --enable-xnest %{kdrive} %{enable_xorg}

BuildRequires: systemtap-sdt-devel
BuildRequires: git-core
BuildRequires: automake autoconf libtool pkgconfig
BuildRequires: xorg-x11-util-macros >= 1.1.5

BuildRequires: xorg-x11-proto-devel >= 7.6-20
BuildRequires: xorg-x11-font-utils >= 7.2-11

BuildRequires: xorg-x11-xtrans-devel >= 1.2.2-1
BuildRequires: libXfont-devel libXau-devel libxkbfile-devel libXres-devel
BuildRequires: libfontenc-devel libXtst-devel libXdmcp-devel
BuildRequires: libX11-devel libXext-devel
BuildRequires: libXinerama-devel libXi-devel

# DMX config utils buildreqs.
BuildRequires: libXt-devel libdmx-devel libXmu-devel libXrender-devel
BuildRequires: libXi-devel libXpm-devel libXaw-devel libXfixes-devel

# Broken, this is global, should be Xephyr-only
BuildRequires: libXv-devel

BuildRequires: pixman-devel >= 0.21.8
BuildRequires: libpciaccess-devel >= 0.12.901-1 openssl-devel byacc flex
BuildRequires: mesa-libGL-devel >= 7.6-0.6
# XXX silly...
BuildRequires: libdrm-devel >= 2.4.0 kernel-headers

BuildRequires: audit-libs-devel libselinux-devel >= 2.0.86-1
BuildRequires: libudev-devel

# All server subpackages have a virtual provide for the name of the server
# they deliver.  The Xorg one is versioned, the others are intentionally
# unversioned.

%description
X.Org X11 X server

%package common
Summary: Xorg server common files
Group: User Interface/X
Requires: pixman >= 0.21.8
Requires: xkeyboard-config xkbcomp

%description common
Common files shared among all X servers.

%if %{with_hw_servers}
%package Xorg
Summary: Xorg X server
Group: User Interface/X
Provides: Xorg = %{version}-%{release}
Provides: Xserver
Provides: xserver-abi(ansic-%{ansic_major}) = %{ansic_minor}
Provides: xserver-abi(videodrv-%{videodrv_major}) = %{videodrv_minor}
Provides: xserver-abi(xinput-%{xinput_major}) = %{xinput_minor}
Provides: xserver-abi(extension-%{extension_major}) = %{extension_minor}
# Dropped from F17, use evdev
Obsoletes: xorg-x11-drv-acecad <= 1.5.0-2.fc16
Obsoletes: xorg-x11-drv-aiptek <= 1.4.1-2.fc16
Obsoletes: xorg-x11-drv-elographics <= 1.3.0-2.fc16
Obsoletes: xorg-x11-drv-fpit <= 1.4.0-2.fc16
Obsoletes: xorg-x11-drv-hyperpen <= 1.4.1-2.fc16
Obsoletes: xorg-x11-drv-mutouch <= 1.3.0-2.fc16
Obsoletes: xorg-x11-drv-penmount <= 1.5.0-3.fc16
%if 0%{?fedora} > 17
# Dropped from F18, use a video card instead
Obsoletes: xorg-x11-drv-ark <= 0.7.3-15.fc17
Obsoletes: xorg-x11-drv-chips <= 1.2.4-8.fc18
Obsoletes: xorg-x11-drv-s3 <= 0.6.3-14.fc17
Obsoletes: xorg-x11-drv-tseng <= 1.2.4-12.fc17
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
Summary: A nested server.
Group: User Interface/X
Obsoletes: xorg-x11-Xnest
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xnest

%description Xnest
Xnest is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.

%package Xdmx
Summary: Distributed Multihead X Server and utilities
Group: User Interface/X
Obsoletes: xorg-x11-Xdmx
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
Summary: A X Windows System virtual framebuffer X server.
Group: User Interface/X
# xvfb-run is GPLv2, rest is MIT
License: MIT and GPLv2
Obsoletes: xorg-x11-Xvfb
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
Summary: A nested server.
Group: User Interface/X
Requires: xorg-x11-server-common >= %{version}-%{release}
Provides: Xephyr

%description Xephyr
Xephyr is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.  Unlike
Xnest, Xephyr renders to an X image rather than relaying the
X protocol, and therefore supports the newer X extensions like
Render and Composite.


%if %{with_hw_servers}
%package devel
Summary: SDK for X server driver module development
Group: User Interface/X
Obsoletes: xorg-x11-sdk xorg-x11-server-sdk
Requires: xorg-x11-util-macros
Requires: xorg-x11-proto-devel
Requires: pkgconfig pixman-devel libpciaccess-devel
# Virtual provide for transition.  Delete me someday.
Provides: xorg-x11-server-sdk = %{version}-%{release}
Provides: xorg-x11-server-static


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
%setup -q -n %{pkgname}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%if 0%{?gitdate}
git checkout -b fedora
sed -i 's/git/&+ssh/' .git/config
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
%else
git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
cp %{SOURCE1} .gitignore
git add .
git commit -a -q -m "%{version} baseline."
%endif

# Apply all the patches.
git am -p1 %{patches} < /dev/null

%if %{with_hw_servers} && !0%{?gitdate}
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

%define default_font_path "catalogue:/etc/X11/fontpath.d,built-ins"

%if %{with_hw_servers}
%define dri_flags --with-dri-driver-path=%{drimoduledir}
%else
%define dri_flags --disable-dri
%endif

%if 0%{?fedora}
%define bodhi_flags --with-vendor-name="Fedora Project"
%endif

# --with-pie ?
autoreconf -f -v --install || exit 1
# export CFLAGS="${RPM_OPT_FLAGS}"
%configure --enable-maintainer-mode %{xservers} \
	--disable-static \
	--with-pic \
	%{?no_int10} --with-int10=x86emu \
	--with-default-font-path=%{default_font_path} \
	--with-module-dir=%{moduledir} \
	--with-builderstring="Build ID: %{name} %{version}-%{release}" \
	--with-os-name="$(hostname -s) $(uname -r)" \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
        --with-dtrace \
	--disable-xaa \
	--enable-xselinux --enable-record \
	--enable-config-udev \
	%{dri_flags} %{?bodhi_flags} \
	${CONFIGURE}
        
make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT moduledir=%{moduledir}

%if %{with_hw_servers}
rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/libxf8_16bpp.so
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

%if !0%{?gitdate} || %{stable_abi}
install -m 755 %{SOURCE30} $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%else
sed -e s/@MAJOR@/%{gitdate}/g -e s/@MINOR@/%{minor_serial}/g %{SOURCE31} > \
    $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
chmod 755 $RPM_BUILD_ROOT%{_bindir}/xserver-sdk-abi-requires
%endif

%endif

# Make the source package
%define xserver_source_dir %{_datadir}/xorg-x11-server-source
%define inst_srcdir %{buildroot}/%{xserver_source_dir}
mkdir -p %{inst_srcdir}/{Xext,xkb,GL,hw/{xquartz/bundle,xfree86/common}}
mkdir -p %{inst_srcdir}/{hw/dmx/doc,man,doc,hw/dmx/doxygen}
cp {,%{inst_srcdir}/}hw/xquartz/bundle/cpprules.in
cp {,%{inst_srcdir}/}man/Xserver.man
cp {,%{inst_srcdir}/}doc/smartsched
cp {,%{inst_srcdir}/}hw/dmx/doxygen/doxygen.conf.in
cp {,%{inst_srcdir}/}xserver.ent.in
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
}

%clean
rm -rf $RPM_BUILD_ROOT


%files common
%defattr(-,root,root,-)
%doc COPYING
%{_mandir}/man1/Xserver.1*
%{_libdir}/xorg/protocol.txt
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

%if 1
%define Xorgperms %attr(4755, root, root)
%else
# disable until module loading is audited
%define Xorgperms %attr(0711,root,root) %caps(cap_sys_admin,cap_sys_rawio,cap_dac_override=pe)
%endif

%if %{with_hw_servers}
%files Xorg
%defattr(-,root,root,-)
%config %attr(0644,root,root) %{_sysconfdir}/pam.d/xserver
%{_bindir}/X
%{Xorgperms} %{_bindir}/Xorg
%{_bindir}/cvt
%{_bindir}/gtf
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libglx.so
%{_libdir}/xorg/modules/extensions/libdri.so
%{_libdir}/xorg/modules/extensions/libdri2.so
%{_libdir}/xorg/modules/extensions/libdbe.so
%{_libdir}/xorg/modules/extensions/libextmod.so
%{_libdir}/xorg/modules/extensions/librecord.so
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libwfb.so
%ifarch %{ix86} x86_64 %{arm}
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libvbe.so
%endif
%{_mandir}/man1/gtf.1*
%{_mandir}/man1/Xorg.1*
%{_mandir}/man1/cvt.1*
%{_mandir}/man4/fbdevhw.4*
%{_mandir}/man4/exa.4*
%{_mandir}/man5/xorg.conf.5*
%{_mandir}/man5/xorg.conf.d.5*
%dir %{_sysconfdir}/X11/xorg.conf.d
%dir %{_datadir}/X11/xorg.conf.d
%{_datadir}/X11/xorg.conf.d/10-evdev.conf
%{_datadir}/X11/xorg.conf.d/10-quirks.conf
%endif


%files Xnest
%defattr(-,root,root,-)
%{_bindir}/Xnest
%{_mandir}/man1/Xnest.1*

%files Xdmx
%defattr(-,root,root,-)
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
%defattr(-,root,root,-)
%{_bindir}/Xvfb
%{_bindir}/xvfb-run
%{_mandir}/man1/Xvfb.1*


%files Xephyr
%defattr(-,root,root,-)
%{_bindir}/Xephyr
%{_mandir}/man1/Xephyr.1*


%if %{with_hw_servers}
%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_docdir}/xorg-server
%{_bindir}/xserver-sdk-abi-requires
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
%{sdkdir}/*.h
%{_datadir}/aclocal/xorg-server.m4
%endif


%files source
%defattr(-, root, root, -)
%{xserver_source_dir}

%changelog
* Wed May 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.2-1
- xserver 1.12.2

* Fri May 25 2012 Dave Airlie <airlied@redhat.com> 1.12.1-2
- xserver-fix-pci-slot-claims.patch: backport slot claiming fix from master
- xserver-1.12-modesetting-fallback.patch: add modesetting to fallback list

* Mon May 14 2012 Peter Hutterer <peter.hutterer@redhat.com>
- Drop xserver-1.10.99.1-test.patch:
  cd89482088f71ed517c2e88ed437e4752070c3f4 fixed it

* Mon May 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.1-1
- server 1.12.1
- force autoreconf to avoid libtool errors
- update patches for new indentation style.

* Mon May 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.0-6
- Make timers signal-safe (#814869)

* Sun May 13 2012 Dennis Gilmore <dennis@ausil.us> 1.12.0-5
- enable vbe on arm arches

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 1.12.0-4
- Obsolete some old video drivers in F18+

* Wed Mar 21 2012 Adam Jackson <ajax@redhat.com> 1.12.0-3
- Tweak arches for RHEL

* Wed Mar 14 2012 Adam Jackson <ajax@redhat.com> 1.12.0-2
- Install Xorg mode 4755, there's no security benefit to 4711. (#712432)

* Mon Mar 05 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.0-1
- xserver 1.12
- xserver-1.12-dix-reset-last.scroll-when-resetting-the-valuator-45.patch:
  drop, 6f2838818

* Thu Feb 16 2012 Adam Jackson <ajax@redhat.com> 1.11.99.903-2.20120215
- Don't pretend int10 is a thing on non-PC arches

* Thu Feb 16 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.903-1.20120215
- Server version is 1.11.99.903 now, use that.

* Wed Feb 15 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-7.20120215
- Today's git snapshot

* Sun Feb 12 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-6.20120124
- Fix installation of xserver-sdk-abi-requires script, if stable_abi is set
  always install the relese one, not the git one

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-5.20120124
- ABI is considered stable now:
  video 12.0, input 16.0, extension 6.0, font 0.6, ansic 0.4

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-4.20120124
- xserver-1.12-dix-reset-last.scroll-when-resetting-the-valuator-45.patch:
  reset last.scroll on the device whenever the slave device switched to
  avoid jumps during scrolling (#788632).

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-3.20120124
- Today's git snapshot
- xserver-1.12-xaa-sdk-headers.patch: drop, a55214d11916b

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-2.20120103
- xserver-1.12-Xext-fix-selinux-build-failure.patch: fix build error
  triggered by Red Hat-specific patch to libselinux

* Tue Jan 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.11.99.901-1.20120103
- Git snapshot 98cde254acb9b98337ddecf64c138d38c14ec2bf
- xserver-1.11.99-optionstr.patch: drop
- 0001-Xext-don-t-swap-CARD8-in-SProcSELinuxQueryVersion.patch: drop

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-11
- Always install XAA SDK headers so drivers still build

* Thu Dec 15 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-10
- --disable-xaa

* Thu Dec 01 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-9
- xserver-1.8-disable-vboxvideo.patch: Drop, should be fixed now
- Drop vesamodes and extramodes, rhpxl is no more
- Stop building libxf86config, pyxf86config will be gone soon

* Tue Nov 29 2011 Dave Airlie <airlied@redhat.com> 1.11.99.1-8
- put optionstr.h into devel package

* Mon Nov 21 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-7
- Restore DRI1 until drivers are properly prepared for it

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-6
- Disable DRI1

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-5
- Obsolete some dead input drivers.

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 1.11.99.1-3
- Fix permissions on abi script when doing git snapshots

* Wed Nov 09 2011 Peter Hutterer <peter.hutterer@redhat.com>  1.11.99.1-1.20111109
- Update to today's git snapshot
- xserver-1.6.1-nouveau.patch: drop, upstream
- xserver-1.10.99-config-add-udev-systemd-multi-seat-support.patch: drop,
  upstream
- 0001-dix-block-signals-when-closing-all-devices.patch: drop, upstream

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com>
- Change the ABI magic for snapshots

* Mon Oct 24 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.11.1-2
- Block signals when removing all input devices #737031

* Thu Oct 13 2011 Adam Jackson <ajax@redhat.com>
- Drop some Requires >= on things where we had newer versions in F14.

* Mon Sep 26 2011 Adam Jackson <ajax@redhat.com> 1.11.1-1
- xserver 1.11.1

* Mon Sep 12 2011 Adam Tkac <atkac redhat com> 1.11.0-2
- ship more files in the -source subpkg

* Tue Sep 06 2011 Adam Jackson <ajax@redhat.com> 1.11.0-1
- xserver 1.11.0

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> 1.10.99.902-1.20110818
- xserver 1.11rc2

* Fri Jul 29 2011 Dave Airlie <airlied@redhat.com> 1.10.99.1-10.2011051
- xvfb-run requires xauth installed, fix requires (from jlaska on irc)

* Wed Jul 27 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.10.99.1-9.20110511
- Add support for multi-seat support from the config/udev backend.

* Wed Jun 29 2011 Dan Horák <dan[at]danny.cz> 1.10.99.1-8.20110511
- don't build tests when --disable-xorg is used like on s390(x)

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.10.99.1-7.20110511
- BuildRequires: systemtap-sdt-devel, configure --with-dtrace

* Wed May 11 2011 Adam Tkac <atkac redhat com> 1.10.99.1-6.20110511
- include hw/dmx/doc/doxygen.conf.in in the -source subpkg

* Mon May 09 2011  1.10.99.1-5.20110511
- Today's server from git
- xserver-1.10-fix-trapezoids.patch: drop, c6cb70be1ed7cf7
- xserver-1.10-glx-pixmap-crash.patch: drop, 6a433b67ca15fd1
- xserver-1.10-bg-none-revert.patch: drop, dc0cf7596782087

* Thu Apr 21 2011 Hans de Goede <hdegoede@redhat.com> 1.10.99.1-4.20110418
- Drop xserver-1.9.0-qxl-fallback.patch, since the latest qxl driver
  supports both revision 1 and 2 qxl devices (#642153)

* Wed Apr 20 2011 Soren Sandmann <ssp@redhat.com> 1.10.99.1-3.20110418
- xserver-1.10-fix-trapezoids.patch: this patch is necessary to prevent
  trap corruption with pixman 0.21.8.

* Tue Apr 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.10.99.1-2.20110418
- rebase all patches
- xserver-1.10-vbe-malloc.patch: drop, d8caa782009abf4d
- "git rm" all unused patches

* Mon Apr 18 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.10.99.1-1.20110418
- Today's server from git

* Wed Mar 30 2011 Adam Jackson <ajax@redhat.com> 1.10.0-7
- xserver-1.10-glx-pixmap-crash.patch, xserver-1.10-bg-none-revert.patch:
  bugfixes from xserver-next

* Tue Mar 22 2011 Adam Jackson <ajax@redhat.com> 1.10.0-6
- Fix thinko in pointer barrier patch

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.10.0-5
- add more files into -source subpkg

* Thu Mar 17 2011 Adam Jackson <ajax@redhat.com> 1.10.0-4
- xserver-1.10-pointer-barriers.patch: Backport CRTC confinement from master
  and pointer barriers from the development tree for same.
- xserver-1.10-vbe-malloc.patch: Fix a buffer overrun in the VBE code.

* Fri Mar 11 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-3
- Add Xen virtual pointer quirk to 10-quirks.conf (#523914, #679699)

* Wed Mar 09 2011 Adam Jackson <ajax@redhat.com> 1.10.0-2
- Merge from F16:

    * Wed Mar 09 2011 Adam Jackson <ajax@redhat.com> 1.10.0-2
    - Disable filesystem caps in paranoia until module loading is audited

    * Fri Feb 25 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.9.99.902-1
    - xserver 1.10.0
    - server-1.9-99.901-xkb-repeat-issues.patch: drop, merged
    - xserver-1.4.99-pic-libxf86config.patch: drop, see 60801ff8
    - xserver-1.6.99-default-modes.patch: drop, see dc498b4
    - xserver-1.7.1-multilib.patch: drop, see a16e282
    - ABI bumps: xinput to 12.2, extension to 5.0, video to 10.0

* Fri Feb 25 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.9.99.1-6.20101201
- xserver-1.9.99.1-xfree86-don-t-overwrite-option-list-32115.patch (#676827)
- xserver-1.9.99.1-xfree86-swap-the-order-to-be-merged-lists-in-xf86Col.patch
  (#676827)

* Thu Feb 24 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.9.99.1-5.20101201
- xserver-1.9.99.1-xkb-split-out-keymap-compilation.patch (#676827 prep work)
- xserver-1.9.99.1-xkb-if-the-keymap-failed-to-compile-load-the-default.patch
  (#676827 fix)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.99.1-4.20101201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.9.99.1-3
- server-1.9-99.901-xkb-repeat-issues.patch: update xkb repeat flags when
  the compat map updates (#537708)

* Mon Dec 06 2010 Adam Tkac <atkac redhat com> 1.9.99.1-2
- add more files to -source subpkg to fix TigerVNC build

* Wed Dec 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9.99.1-1
- Today's git snapshot
- Drop hal→udev migration warning. Two releases later should be enough.
- xserver-1.8.0-no-xorg.patch: drop, upstream
- xserver-1.7.0-randr-gamma-restore.patch: drop, upstream
- xserver-1.7.1-gamma-kdm-fix.patch: drop, upstream
- xserver-1.9.0-tcflush-fix.patch: drop, upstream
- xserver-1.9.1-pxtc-crash.patch: drop, upstream
- xserver-1.9.0-vbe-panelid-sanity.patch: drop, upstream
- xserver-1.9.0-classic-default-mode.patch: drop, upstream

* Tue Nov 23 2010 Adam Jackson <ajax@redhat.com> 1.9.1-6
- xserver-1.5.0-projector-fb-size.patch: Drop.

* Tue Nov 23 2010 Adam Jackson <ajax@redhat.com> 1.9.1-5
- Drop mode-debug patch

* Thu Nov 18 2010 Adam Jackson <ajax@redhat.com> 1.9.1-4
- Disable frame pointers for profiling, will revert for F15

* Tue Nov 09 2010 Adam Jackson <ajax@redhat.com> 1.9.1-3
- xserver-1.9.1-pxtc-crash.patch: Fix crash with Xinerama enabled

* Mon Oct 25 2010 Adam Jackson <ajax@redhat.com>
- Explicitly --without-dtrace so it still builds even if you have
  systemtap-sdt-devel installed. (#605588)

* Mon Oct 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-2
- This time with the source tarball.

* Mon Oct 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- xserver 1.9.1
- xserver-1.9.0-vbe-insanity.patch: drop, merged.

* Wed Oct 13 2010 Adam Jackson <ajax@redhat.com> 1.9.0-15
- xserver-1.9.0-qxl-fallback.patch: Use vesa for older qxl devices since
  the driver lost backwards-compat. (#641991)

* Mon Oct 11 2010 Adam Jackson <ajax@redhat.com> 1.9.0-14
- xserver-1.9.0-classic-default-mode.patch: Bump classic driver default
  mode size to 1024x768. (related to #641991)

* Tue Oct 05 2010 Adam Jackson <ajax@redhat.com> 1.9.0-13
- xserver-1.9.0-vbe-insanity.patch: Fix thinko.

* Mon Oct 04 2010 Adam Jackson <ajax@redhat.com> 1.9.0-12
- xserver-1.9.0-vbe-insanity.patch: Fix VBE < 3.0 support.

* Wed Sep 29 2010 jkeating - 1.9.0-11
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Adam Tkac <atkac redhat com> 1.9.0-10
- add more files to -sources subpkg to fix tigervnc builds

* Mon Sep 13 2010 Adam Jackson <ajax@redhat.com> 1.9.0-9
- xserver-1.9.0-vbe-panelid-sanity.patch: Refuse to believe tiny (or negative)
  sizes from PanelID. (#632805)

* Mon Sep 13 2010 Matěj Cepl <mcepl@redhat.com> - 1.9.0-8
- Call mktemp correctly (fixes RHBZ bug 632879)

* Thu Sep 02 2010 Adam Jackson <ajax@redhat.com> 1.9.0-7
- ... but only in F15 and later.

* Thu Sep 02 2010 Adam Jackson <ajax@redhat.com> 1.9.0-5
- Drop the SUID bit from Xorg, use fs caps instead.

* Fri Aug 27 2010 Adam Jackson <ajax@redhat.com> 1.9.0-4
- Remove link to bodhi, it's used in multiple places in ways that don't
  make sense (#627755)

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.9.0-3
- Fix static lib packaging guideline nonconformance (#609625)

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.9.0-2
- xserver-1.9.0-tcflush-fix.patch: Fix 100% CPU usage bug.

* Mon Aug 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-1
- xserver 1.9.0
- xserver-1.9-reset-root-null.patch: drop, upstream.

* Mon Aug 16 2010 Dave Airlie <airlied@redhat.com> 1.8.99.906-2
- fix use-after-free for root window - hopefully fix (#596985)

* Fri Aug 13 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.906-1
- xserver 1.8.99.906
- xserver-1.8-enter-leave-woes.patch: drop, upstream.

* Mon Aug 02 2010 Adam Jackson <ajax@redhat.com> 1.8.99.905-3
- Drop RANDR debugging patch, not useful.

* Wed Jul 21 2010 Adam Tkac <atkac redhat com> 1.8.99.905-2
- include more files in the -source subpkg to make Xvnc compilable

* Fri Jul 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.905-1
- xserver 1.8.99.905
- xserver-1.8-entervt.patch: drop, upstream.

* Thu Jul 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.904-6
- xserver-1.8-enter-leave-woes.patch: ignore grabs for enter/leave events
  (#538462)

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 1.8.99.904-5
- Add patch from master which blocks gnome-shell development

* Fri Jul 09 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.904-3
- BuildRequires updated xorg-x11-font-utils for font-utils 1.1
- Requires libXfont 1.4.2 or newer (#611753)

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 1.8.99.904-2
- Install COPYING as necessary.

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.99.904-1
- Update to current git master (1.9 snapshot 4).
- New ABIS: videodrv 8, input 11, extension 4
- Drop upstreamed patches.

* Thu Jun 24 2010 Adam Jackson <ajax@redhat.com>
- Drop a bunch of old Obsoletes from F11 and earlier.
- Drop explicit driver Requires.
- Update pixman and libdrm Requires to be more like reality.

* Tue Jun 22 2010 Dan Horák <dan@danny.cz> 1.8.0-8
- fix built with --disable-xorg like on s390/s390x

* Wed Jun 16 2010 Adam Jackson <ajax@redhat.com> 1.8.0-7
- Make -Xorg package provide its own ABI versions.  Fail %%prep if they
  don't match what the specfile claims.
- Add xserver-sdk-abi-requires to -devel to make it easy for driver packages
  to require the ABI versions they were built against.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-6
- xserver-1.8.0-xorg.conf.d-changes.patch: push in the upcoming 1.8.1
  xorg.conf.d changes. The X server uses /etc/X11/xorg.conf now for custom
  config and /usr/share/X11/xorg.conf.d for system-provided config.
- xserver-1.8-no-hardcoded-etc.patch: drop, obsolete.
- 00-evdev.conf: drop, use the upstream one.

* Thu Apr 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-5
- xserver-1.4.99-pic-libxf86config.patch: update, only merge CFLAGS for
  libxf86config.a, not AM_CFLAGS. Makes patch mangling for the next set of
  patches easier.

* Wed Apr 14 2010 Adam Tkac <atkac redhat com> 1.8.0-4
- xserver-1.7.6-export-more-dix-functions.patch: export XkbCopyDeviceKeymap
  function, needed by VNC

* Mon Apr 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-3
- xserver-1.7.6-export-dix-functions: export some functions in use by VNC.

* Mon Apr 12 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-2
- Add Xen virtual pointer quirk to 10-quirks.conf (#523914)

* Tue Apr 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- xserver 1.8.0
- Drop merged patches.
- Rename xdmx client to dmxinfo (change upstream).
- xserver-1.8-no-hardcoded-etc.patch: don't hardcode $prefix/etc for the
  server-installed 10-evdev.conf.

* Tue Apr 06 2010 Peter Hutterer <peter.hutterer@redhat.com>
- Auto-append the gitdate to the Release whenever it is set.

* Tue Mar 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.902-3.20100319
- xserver-1.8-merge-driver.patch: merge driver from input classes into
  options. Fixes wacom hotplugging issues.

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.902-2.20100319
- xserver-1.7.4-owner-events.patch: if owner-events is true for passive
  grabs, add the window mask (#543647)

* Fri Mar 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.902-1.20100319
- Update to today's git.

* Thu Mar 04 2010 Adam Jackson <ajax@redhat.com> 1.7.99.901-12.20100304
- xserver-1.6.1-nouveau.patch: Fall back to nv if nouveau won't load. (#519298)

* Thu Mar 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-11.20100304
- Update to today's git.
- BuildRequires libselinux-devel >= 2.0.86 

* Thu Feb 25 2010 Adam Jackson <ajax@redhat.com> 1.7.99.901-10.20100223
- xserver-1.8-disable-vboxvideo.patch: Disable vboxvideo. (adamw)

* Thu Feb 25 2010 Dave Airlie <airlied@redhat.com> 1.7.99.901-9.20100223
- fix right-of patch to allow driver to override right-of with clone

* Tue Feb 23 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-8.0100215
- Require udev >= 148-1 for xorg-x11-server-Xorg, otherwise we don't see any
  input devices (#566396). This requires is just needed now in the
  transition period, we still have users with an older udev but newer
  server. Also, 148-1 didn't actually exist in Fedora, but whatever next one
  will do.
- Update to today's master, re-enables RECORD.

* Mon Feb 22 2010 Ben Skeggs <bskeggs@redhat.com> 1.7.99.901-7.20100215
- exa: fix gnome-panel corruption

* Fri Feb 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-6.20100215
- Only match device paths of /dev/input/event* for the evdev classes.
  Reduces the number of error messages seen in the log when evdev can't
  ioctl /dev/input/mouse devices.

* Fri Feb 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-5.2010208
- Change 00-evdev.conf to match all devices but joysticks (#566418)

* Wed Feb 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-4.2010208
- One day I'll remember to cvs add everything.
  xserver-1.8-udev-warning.patch added.

* Wed Feb 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-3.2010208
- Add 10-quirks.conf for specific black/whitelisting of devices.
- xserver-1.8-udev-warning.patch: stick giant warning into log file that fdi
  files need to be ported.

* Tue Feb 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-2.2010208
- Add 00-evdev.conf this time.

* Tue Feb 16 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.901-1.2010208
- Update to today's git master (1.8RC1)
- xserver-1.7.4-reset-sli-pointers.patch: drop, upstream
- Enable udev config, drop hal.
- Require system-setup-keyboard (renamed fedora-setup-keyboard)

* Mon Feb 08 2010 Ben Skeggs <bskeggs@redhat.com> 1.7.99.3-3.20100208
- Update to today's git master

* Mon Feb 08 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.3-2.20100120
- xserver-1.7.4-reset-sli-pointers.patch: reset the server LED indicator
  pointers after device class copying (#540584) 

* Wed Jan 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.99.3-1.20100120
- Update to today's git master.
- Disable prelease warning patch - this is a prerelease
- Remove upstreamed patches.
- Remove shave files, shave was purged.

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.7.3-7
- Require xkeyboard-config, not xkbdata. xkbdata has been replaced by
  xkeyboard-config.

* Mon Jan 04 2010 Adam Jackson <ajax@redhat.com> 1.7.3-6
- Build with V=1 for debugging.

* Mon Dec 21 2009 Adam Tkac <atkac redhat com> 1.7.3-5
- ship shave.in and shave-libtool.in in the -source subpackage

* Mon Dec 21 2009 Dave Airlie <airlied@redhat.com> 1.7.3-4
- Backport FB changes from master.

* Wed Dec 17 2009 Dave Airlie <airlied@redhat.com> 1.7.3-3
- backport EXA fixes from master, should fix xfig crashes X server

* Mon Dec 14 2009 Adam Jackson <ajax@redhat.com> 1.7.3-2
- xserver-1.7.1-sigaction.patch: Drop, exacerbates a race that leads to weird
  behaviour like spontaneously repeating keys.

* Tue Dec 08 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.7.3-1
- xserver 1.7.3
- xserver-1.7.1-stat-sanity.patch: Drop, merged upstream.
- xserver-1.7.1-window-pictures.patch: Drop, code it bases on reverted
  upstream
- xserver-1.7.1-window-picture-performance-regression.patch: Drop, code it
  bases on reverted upstream.

* Tue Nov 24 2009 Adam Jackson <ajax@redhat.com> 1.7.1-12
- xserver-1.7.1-glx14-swrast.patch: Enable GLX 1.4 for software GLX.

* Tue Nov 24 2009 Adam Jackson <ajax@redhat.com> 1.7.1-11
- xserver-1.7.1-window-picture-performance-regression.patch: Paper over a
  performance regression caused by the window picture fixes.

* Mon Nov 23 2009 Adam Jackson <ajax@redhat.com> 1.7.1-10
- Fix crash message output. (#539401)

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-9
- xserver-1.7.1-stat-sanity.patch: stat directories that actually exist
  (possibly #537737).

* Mon Nov 16 2009 Adam Jackson <ajax@redhat.com> 1.7.1-8
- xserver-1.7.1-libcrypto.patch: Avoid linking against libssl, which is huge
  and drags in dependent libs we don't care about.
- xserver-1.7.1-sigaction.patch: Microoptimization to SIGIO handling.

* Fri Nov 06 2009 Adam Jackson <ajax@redhat.com>
- Fix the previous changelog entry to name the right patch

* Fri Nov 06 2009 Dave Airlie <airlied@redhat.com> 1.7.1-7
- xserver-1.7.1-window-pictures.patch: remove the miClearDrawable (fingers crossed) (#533236)
- xserver-1.7.1-gamma-kdm-fix.patch: fix KDM vt gamma (#533217)

* Wed Nov 04 2009 Adam Jackson <ajax@redhat.com> 1.7.1-6
- xserver-1.7.1-multilib.patch: Keep defining _XSERVER64, it's needed in
  some of the shared client/server headers.

* Wed Nov  4 2009 Soren Sandmann <ssp@redhat.com> 1.7.1-5
- Update xserver-1.7.1-window-pictures.patch. Instead of calling
  GetImage(), simply call fb* functions rather than the screen
  hooks. (#524244)

* Tue Nov  3 2009 Adam Jackson <ajax@redhat.com> 1.7.1-3
- xserver-1.7.1-window-pictures.patch: Fix Render from Pictures backed by
  Windows to not crash in the presence of KMS. (#524244)

* Thu Oct 29 2009 Adam Jackson <ajax@redhat.com> 1.7.1-2
- xserver-1.7.1-multilib.patch: Fix silly multilib issue. (#470885)

* Mon Oct 26 2009 Adam Jackson <ajax@redhat.com> 1.7.1-1
- xserver 1.7.1

* Sat Oct 24 2009 Ben Skeggs <bskegg@redhat.com> 1.7.0-5
- Fix unbalancing of Prepare/FinishAccess in EXA mixed pixmaps (rh#528005)

* Fri Oct 16 2009 Dave Airlie <airlied@redhat.com> 1.7.0-4
- update GLX for 1.4 version reporting

* Fri Oct 09 2009 Ben Skeggs <bskeggs@redhat.com> 1.7.0-3
- xserver-1.7.0-exa-looping-forever-is-evil.patch: Fix rendercheck hang

* Thu Oct 08 2009 Adam Jackson <ajax@redhat.com> 1.7.0-2
- xserver-1.7.0-randr-gamma-restore.patch: Restore CRTC gamma on EnterVT.

* Mon Oct 05 2009 Dave Airlie <airlied@redhat.com> 1.7.0-1
- rebase to 1.7.0 upstream release - were 99% this already

* Thu Oct 01 2009 Dave Airlie <airlied@redhat.com> 1.6.99.903-2
- backport EXA and rotate crash fixes

* Mon Sep 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99.903-1
- xserver 1.6.99.903 

* Tue Sep 22 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99.902-1
- xserver 1.6.99.902 
- cvs rm the now obsolete autoconf endian patch.

* Thu Sep 17 2009 Kristian Høgsberg <krh@redhat.com> - 1.6.99.901-3
- Back out pageflip patch and follow on patches.

* Thu Sep 17 2009 Peter Hutterer <peter.hutterer@redhat.com>
- xserver-1.5.99.3-dmx-xcalloc.patch: Obsolete, drop.
- cvs rm a few other patches not used anymore. 

* Tue Sep 15 2009 Adam Jackson <ajax@redhat.com> 1.6.99.901-2
- xserver-1.6.99-hush-prerelease-warning.patch: Quiet, you.
- Point to bodhi for the "check for latest version" message.

* Mon Sep 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99.901-1
- xserver 1.6.99.901 
- Re-enable Xdmx
- xserver-1.4.99-document-fontpath-correctly.patch: Drop

* Tue Sep 08 2009 Adam Jackson <ajax@redhat.com> 1.6.99.900-2
- Fix -source subtree to not include generated C files from hw/xfree86.
  Actually, just remove all C files from hw/xfree86 in -source, since we
  don't need them to build Xvnc.

* Mon Sep 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99.900-1
- xserver 1.6.99.900 

* Thu Sep 03 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-45.20090903
- Today's git snapshot.

* Tue Sep 01 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-44.20090901
- Today's git snapshot (incl. vga-arbitration).
- dri2-page-flip.patch: rebase.
- xserver-1.6.99-vga-arb.patch: Drop.

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-43.20090828
- Today's git snapshot.

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 1.6.99-42.20090825
- rebuilt with new openssl and audit

* Tue Aug 25 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-41.20090825
- Today's git snapshot.

* Mon Aug 24 2009 Ben Skeggs <bskeggs@redhat.com> 1.6.99-40.20090820
- xserver-1.6.1-nouveau.patch: remove vesa fallback for 0x08xx chips, KMS
  should work on them now, there's accel issues on some of them but we can
  fallback to shadowfb in the driver and keep KMS support.

* Fri Aug 21 2009 Adam Jackson <ajax@redhat.com> 1.6.99-39.20090820
- xserver-1.6.99-default-modes.patch: Don't add default modes to the pool if
  the driver returned real modes (and has no EDID).

* Thu Aug 20 2009 Adam Jackson <ajax@redhat.com> 1.6.99-37.20090820
- Today's git snapshot.
- xserver-1.6.99-dri2-swapbuffers-fallback.patch: Fix SwapBuffers crash.
- xserver-1.6.99-linkmap.patch: Drop, superceded upstream.
- xserver-1.6.1-proc-cmdline.patch, xserver-1.6.99-dpms.patch, 
  xserver-1.6.99-eventtime.patch: Drop, merged.

* Wed Aug 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-36.20090814
- xserver-1.6.99-eventtime.patch: don't reset the last event time when the
  screen saver activates.

* Mon Aug 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-35.20090814
- xserver-1.6.99-dpms.patch: don't reset last event time on DPMS changes.

* Fri Aug 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-34.20090814
- Today's git snapshot.

* Tue Aug 11 2009 Adam Jackson <ajax@redhat.com> 1.6.99-33.20090807
- xserver-1.6.99-show-ugly-cursor.patch: Drop, gtk bug found.

* Tue Aug 11 2009 Dave Airlie <airlied@redhat.com> 1.6.99-32.20090807
- update to latest -git for EXA fixes

* Mon Aug 10 2009 Adam Jackson <ajax@redhat.com> 1.6.99-31.20090807
- Move libxf86config.a back to -server-devel
- xserver-1.6.99-show-ugly-cursor.patch: Un-suppress the initial root cursor
  hiding until we figure out what's wrong with gtk in anaconda.

* Fri Aug 07 2009 Dave Airlie <airlied@redhat.com> 1.6.99-30.20090807
- goddamit: reapply picify libxf86config.a hopefully

* Fri Aug 07 2009 Dave Airlie <airlied@redhat.com> 1.6.99-29.20090807
- rebase upstream
- libxf86config.a revenge, brought back .a upstream, doesn't work as .so

* Thu Aug 06 2009 Adam Jackson <ajax@redhat.com> 1.6.99-28.20090804
- xserver-1.6.99-dri2-crash-fixes.patch: don't cough and die just because
  the driver had the gall not to register a SwapBuffers handler.

* Wed Aug 05 2009 Adam Jackson <ajax@redhat.com> 1.6.99-27.20090804
- xserver-1.6.99-vga-arb.patch: Fix crashes from miscompilation without
  xorg-config.h.

* Wed Aug 05 2009 Dave Airlie <airlied@redhat.com> 1.6.99-26.20090804
- fix VGA arb device lookup - noticed by mclasen in qemu

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.6.99-25.20090804
- fix VGA arb fatal error

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.6.99-24.20090804
- update server snapshot + add VGA arbitration

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 1.6.99-23.20090724
- Un-Requires xorg-x11-filesystem

* Wed Jul 29 2009 Kristian Høgsberg <krh@redhat.com> - 1.6.99-22.20090724
- Add DRI2 page flipping feature.

* Tue Jul 28 2009 Adam Jackson <ajax@redhat.com> 1.6.99-21.20090724
- xserver-1.6.99-right-of.patch: Default to right-of initial placement
  for RANDR 1.2 drivers with enough virtual space.

* Tue Jul 28 2009 Adam Jackson <ajax@redhat.com> 1.6.99-20.20090724
- xserver-1.6.99-use-pci-access-boot.patch: Some chips (thanks Intel) will
  change their PCI class at runtime if you disable their VGA decode, so
  consider both 0x0300 and 0x0380 classes when looking for the boot VGA.

* Tue Jul 28 2009 Adam Jackson <ajax@redhat.com> 1.6.99-19.20090724
- xserver-1.6.99-randr-error-debugging.patch: Dump RANDR protocol errors
  to the log.
- Un-package xf8_16bpp, no one cares.

* Mon Jul 27 2009 Dave Airlie <airlied@redhat.com> 1.6.99-18.20090724
- xserver-1.6.99-use-pci-access-boot.patch: use pciaccess boot vga
- not sure what is up with the Conflicts stuff

* Sat Jul 25 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-17.20090724
- Bump release number.

* Fri Jul 24 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-16.20090724
- Today's git snapshot.

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.6.99-16.20090721
- xserver-1.6.99-linkmap.patch: Print load offsets of all DSOs on backtrace
  so we can addr2line afterwards.

* Tue Jul 21 2009 Adam Jackson <ajax@redhat.com> 1.6.99-15.20090721
- Today's git snapshot.

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> 1.6.99-14.20090715
- Move PAM config file here from xdm.

* Wed Jul 15 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-13.20090715
- Today's git snapshot.

* Tue Jul 14 2009 Adam Jackson <ajax@redhat.com> 1.6.99-12.20090714
- Today's git snapshot.
- Drop the %%pre script for Xorg, everyone ought to be migrated by now.

* Fri Jul 10 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-11.20090710
- Today's git snapshot.
- xserver-1.6.0-no-i810.patch: Drop.

* Tue Jul 07 2009 Adam Jackson <ajax@redhat.com> 1.6.99-10.20090707
- Today's git snapshot.
- xserver-1.4.99-pic-libxf86config.patch: Drop.
- xserver-1.4.99-document-fontpath-correctly.patch: Typo fixes.
- libxf86config subpackages.

* Mon Jul 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-9.20090706
- Today's git snapshot.
- xserver-1.5.0-bad-fbdev-thats-mine.patch: Drop. Merged upstream.

* Mon Jun 29 2009 Adam Jackson <ajax@redhat.com> 1.6.99-8.20090618
- Move xkb requires to -common subpackage, Xephyr needs them too.

* Mon Jun 29 2009 Adam Jackson <ajax@redhat.com> 1.6.99-7.20090618
- xserver-1.5.99.902-selinux-debugging.patch: Drop.
- xorg-x11-server-1.1.0-no-move-damage.patch: Drop.
- xserver-1.4.99-dont-backfill-bg-none.patch: Drop.

* Tue Jun 23 2009 Adam Tkac <atkac redhat com> 1.6.99-6.20090618
- build xorg-x11-server-source as noarch

* Tue Jun 23 2009 Ben Skeggs <bskeggs@redhat.com> 1.6.99-5.20090618
- update nouveau autoconfig patch from F11

* Mon Jun 22 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-4.20090618
- move libxf86config.so to devel package, libxf86config.so.* stays in the
  Xorg package.

* Sun Jun 21 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-3.20090618
- Move libxf86config files to package xorg-x11-server-Xorg, libxf86config is
  a shared lib now and required by the Xorg binary.

* Fri Jun 19 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99-2.20090618
- add missing commitid file.

* Thu Jun 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.99.1.20090618
- Today's git snapshot.
- disable Xdmx - it's broken upstream
- Removing patches merged upstream or obsolete.
  xserver-1.4.99-endian.patch - obsolete with autoconf 2.63-1 (#449944)
  xserver-1.5.99.902-sod-off-poulsbo.patch - upstream
  xserver-1.6.0-selinux-less.patch - upstream
  xserver-1.5.99.902-vnc.patch - upstream
  xserver-1.6.0-restore-zap.patch - upstream
  xserver-1.6.0-xinerama-cursors.patch - upstream
  xserver-1.6.0-xinerama-crashes.patch - obsolete, server 1.6 only
  xserver-1.6.1-xkbsendmap.patch - upstream
  xserver-1.6.0-randr-xinerama-crash.patch - upstream
  xserver-1.6.1-avoid-malloc-for-logging.patch - upstream
  xserver-1.6.1-exa-avoid-swapped-out.patch - upstream
  xserver-1.6.1-exa-create-pixmap2.patch -  upstream
  xserver-1.6.1-fix-glx-drawable.patch - upstream
  xserver-1.6.1-randr-gamma.patch - upstream 
  xserver-1.6.1-vt-switch.patch - obsolete
  xserver-1.6.1-pea-quirk.patch - will be upstream

* Tue Apr 14 2009 Adam Jackson <ajax@redhat.com> 1.6.1-1
- xserver 1.6.1

* Mon Apr 13 2009 Adam Jackson <ajax@redhat.com> 1.6.0-20
- Obsolete a bunch of input drivers. (#493221)

* Thu Apr 09 2009 Adam Jackson <ajax@redhat.com> 1.6.0-19
- xserver-1.6.0-no-i810.patch: Don't try to load i810.

* Thu Apr 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-18
- xserver-1.6.0-restore-zap.patch: Restore default off for DontZap.

* Mon Apr 06 2009 Adam Jackson <ajax@redhat.com> 1.6.0-17
- xserver-1.6.0-displayfd.patch: Add -displayfd commandline option.

* Mon Mar 30 2009 Adam Jackson <ajax@redhat.com> 1.6.0-16
- Don't nuke ModulePath lines in xorg.conf anymore.  If you're still doing
  this it's probably because you need to. (#490294)

* Wed Mar 25 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-15
- xserver-1.6.0-xtest-pointerscreen.patch: set POINTER_SCREEN flag for core
  XTestFakeInput events (#490984)
- xserver-1.6.0-xinerama-cursors.patch: don't display SW cursors when
  switching screens.
- xserver-1.6.0-xinerama-crashes.patch: don't crash on key repeats in xinerama
  setups.

* Wed Mar 18 2009 Adam Jackson <ajax@redhat.com> 1.6.0-14
- s390 fixes (Karsten Hopp)

* Thu Mar 12 2009 Adam Jackson <ajax@redhat.com> 1.6.0-13
- xselinux-1.6.0-selinux-nlfd.patch: Acquire the netlink socket from selinux,
  check it ourselves rather than having libselinux bang on it all the time.

* Wed Mar 11 2009 Adam Jackson <ajax@redhat.com> 1.6.0-12
- Requires: pixman >= 0.14.0

* Wed Mar 11 2009 Adam Jackson <ajax@redhat.com> 1.6.0-11
- xserver-1.6.0-less-acpi-brokenness.patch: Don't build the (broken)
  ACPI code.

* Wed Mar 11 2009 Adam Jackson <ajax@redhat.com> 1.6.0-10
- xserver-1.6.0-selinux-less.patch: Don't init selinux unless the policy
  says to be an object manager.

* Fri Mar 06 2009 Dennis Gilmore <dennis@ausil.us> 1.6.0-9
- BR kernel-headers not kernel-devel

* Fri Mar 06 2009 Adam Jackson <ajax@redhat.com> 1.6.0-8
- xserver-1.6.0-primary.patch: Really, only look at VGA devices. (#488869)

* Thu Mar 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-7
- Remove 10-x11-keymap.fdi, this is provided by fedora-setup-keyboard now.

* Wed Mar 04 2009 Adam Jackson <ajax@redhat.com> 1.6.0-6
- Move fedora-setup-keyboard (and libdrm) Requires to the Xorg subpackage,
  since they won't do anything at the top level.
- Remove BR: freetype freetype-devel.
- xserver-1.6.0-primary.patch: Only consider actual VGA devices.

* Wed Mar 04 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-5
- Drop our own fedora-setup-keyboard script, Require: fedora-setup-keyboard
  package instead.

* Tue Mar 03 2009 Adam Jackson <ajax@redhat.com> 1.6.0-4
- xserver-1.6.0-selinux-raw.patch: Deal in raw contexts, to avoid paying
  the price for setrans on every object.
- xserver-1.6.0-primary.patch: Try harder to figure out what the primary
  video device is on machines with multiple GPUs.
- xserver-1.6.0-selinux-destroy.patch: Don't bother relabeling objects that
  are on the way to destruction.

* Mon Mar 02 2009 Adam Jackson <ajax@redhat.com> 1.6.0-3
- xserver-1.6.0-preferred-thinko.patch: Fix a thinko in output setup when
  only one head is attached.

* Fri Feb 27 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-2
- xserver-1.6.0-XIPropToInt.patch: add XIPropToInt helper function
  (requirement for XATOM_FLOAT patch)
- xserver-1.6.0-XATOM_FLOAT.patch: add support for float properties.

* Wed Feb 25 2009 Adam Jackson <ajax@redhat.com> 1.6.0-1
- xserver 1.6.0

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 1.5.99.903-3
- xserver-1.5.99.903-fontmod.h: Fix build against new libXfont.

* Wed Feb 18 2009 Adam Jackson <ajax@redhat.com> 1.5.99.903-2
- xserver-1.5.99.903-glx-visual-score.patch: Fix visual scoring.

* Wed Feb 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.903-1
- xserver 1.6. RC 3
- remove patches merged into upstream.

* Tue Feb 17 2009 Adam Jackson <ajax@redhat.com> 1.5.99.902-13
- xserver-1.5.99.902-randr-soft-getpanning.patch: Fail RRGetPanning softly
  when the driver doesn't support it.

* Mon Feb 16 2009 Ben Skeggs <bskeggs@redhat.com> 1.5.99.902-12
- xserver-1.5.99.902-nouveau.patch: select nouveau as default driver
  for NVIDIA GPUs

* Mon Feb 16 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-11
- xserver-1.5.99.902-xkb-colors.patch: don't confuse src and dst when copying
  color labels (#469572)

* Thu Feb 12 2009 Adam Tkac <atkac redhat com> 1.5.99.902-10
- don't call drv->UnInit if device doesn't have driver

* Wed Feb 11 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-9
- xserver-1.5.99.902-always-RAW.patch: always init the console to RAW mode.

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com> 1.5.99.902-8
- Re-enable RECORD. (#472168)

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com> 1.5.99.902-7
- xserver-1.5.99.902-sod-off-poulsbo.patch: Don't try the intel driver on
  GMA500. (#472674)

* Tue Feb 10 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-6
- xserver-1.5.99.902-listen-for-hal.patch: listen for HAL startup
  notifications if it isn't running already.

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-5
- xserver-1.5.99.902-mediakeys-crash.patch: don't crash when multimedia keys
  are pressed (#483435)

* Sun Feb 08 2009 Adam Jackson <ajax@redhat.com> 1.5.99.902-4
- xserver-1.5.99.902-selinux-debugging.patch: Try to figure out why selinux
  class map setup fails.
- Remove mtrr header hack.

* Fri Feb 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-3
- Update 10-x11-keymap.fdi: only call fedora-setup-keyboard for devices with
  input.capabilities = keyboard (#484217)

* Wed Feb 04 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-2
- xserver-1.5.99.902-xinerama.patch: don't update the sprite root window in
  Xinerama setups (#473825)

* Tue Feb 03 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.902-1
- xserver 1.6. RC 2

* Tue Jan 27 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.901-5
- replace fedora-setup-keyboard with pure python one (#478431)

* Tue Jan 27 2009 Dave Airlie <airlied@redhat.com> 1.5.99.901-4
- xserver-1.5.99.3-fix-core-fonts.patch (#478999)

* Mon Jan 26 2009 Adam Tkac <atkac redhat com> 1.5.99.901-3
- improved xserver-1.5.99.3-broken-mtrr-header.patch to unbreak mtrr.h again

* Mon Jan 26 2009 Adam Tkac <atkac redhat com> 1.5.99.901-2
- rebuild against new openssl

* Tue Jan 13 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.901-1
- xserver 1.6 RC 1
- fix "git-xyz" to "git xyz"
- revert yesterdays changes to make-git-snapshot.sh, that was a bad idea.

* Mon Jan 12 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.3-5
- rebase to today's server-1.6-enterleave branch, current 1.6 plus enterleave
  patches.
- drop xserver-1.5.99.3-offscreen-pixmaps.patch - merged upstream
- fix up git checkout in make-git-snapshot.sh to allow a remote branch to be
  specified as $1.

* Thu Jan 08 2009 Adam Jackson <ajax@redhat.com> 1.5.99.3-8
- xserver-1.5.99.3-broken-mtrr-header.patch: Unbreak broken mtrr.h.

* Wed Jan 07 2009 Adam Jackson <ajax@redhat.com> 1.5.99.3-7
- xserver-1.5.99.3-offscreen-pixmaps.patch: Turn off offscreen pixmaps in XAA.
  Again.  Sigh.

* Wed Jan 07 2009 Adam Tkac <atkac redhat com> 1.5.99.3-6
- use "git am" instead of "git-am"
- added more sources into xorg-x11-server-source to make source compilable

* Mon Dec 29 2008 Dave Airlie <airlied@redhat.com> 1.5.99.3-5
- remove unused build options - enable dri2

* Wed Dec 24 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.3-4
- xserver-1.5.99.3-ddx-rules.patch: enable the DDX to set the rules for the
  core devices (#477712)
- Require xorg-x11-drv-evdev 2.1.0-3 for ABI.

* Mon Dec 22 2008 Adam Jackson <ajax@redhat.com> 1.5.99.3-3
- xserver-1.5.0-bad-fbdev-thats-mine.patch: Do the same for sbus that we do
  for pci.

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.3-2
- Update to today's server-1.6  branch tip.

* Fri Dec 19 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.99.3-1
- xserver 1.5.99.3
- drop patches merged into master
- xserver-1.5.99.3-dmx-xcalloc.patch: avoid dmx Xcalloc build errors

* Wed Nov 05 2008 Adam Jackson <ajax@redhat.com> 1.5.3-1
- xserver 1.5.3

* Fri Oct 31 2008 Adam Jackson <ajax@redhat.com> 1.5.2-12
- xserver-1.5.2-drain-console.patch: Silently eat any input we get from the
  tty fd, lest terrible wakeup storms ensue.

* Tue Oct 28 2008 Adam Jackson <ajax@redhat.com> 1.5.2-11
- Un-require mouse and keyboard, we're an evdev shop now
- Drop some obsoletes from the F7 timeframe
- Require vesa on i386 and amd64, fbdev elsewhere

* Mon Oct 27 2008 Adam Jackson <ajax@redhat.com> 1.5.2-10
- xserver-1.5.0-bg-none-root.patch: Make it something the driver has to
  explicitly claim support for, so we don't get garbage when you do -nr
  on vesa for example.

* Mon Oct 27 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-9
- xserver-1.5.2-more-sanity-checks.patch: more sanity checks to stop vmmouse
  from segfaulting the server. #434807

* Wed Oct 22 2008 Peter Hutterer <peter.hutterer@redhat.com>
- Update xserver-1.5.2-disable-kbd-mouse.patch: add line to xorg.conf man-page
  stating that devices are disabled if AEI is on.

* Wed Oct 22 2008 Peter Hutterer <peter.hutterer@redhat.com>
- fix typo in xserver-1.5.2-no-duplicate-devices.patch

* Mon Oct 20 2008 Adam Jackson <ajax@redhat.com> 1.5.2-8
- xserver-1.5.2-exa-sync-less.patch: Avoid migrating pixmaps out on
  PutImage.

* Mon Oct 20 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-7
- xserver-1.5.2-no-duplicate-devices.patch: don't re-add devices through HAL
  if they are already added (#467462).

* Sun Oct 19 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-6
- Update xserver-1.5.2-disable-kbd-mouse.patch: if no config file is present,
  we need to force AllowEmptyInput on.

* Thu Oct 16 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-5
- xserver-1.5.2-enable-RAW-console.patch: enable RAW mode for console, no need
  for grabbing the evdev device anymore.
- xserver-1.5.2-disable-kbd-mouse.patch: if AllowEmptyInput is on, don't allow
  mouse or keyboard drivers.

* Tue Oct 14 2008 Adam Jackson <ajax@redhat.com> 1.5.2-4
- xserver-1.5.2-lies-damn-lies-and-aspect-ratios.patch: Catch even more
  cases of the monitor encoding aspect ratio for size. (#458747)

* Tue Oct 14 2008 Adam Jackson <ajax@redhat.com> 1.5.2-3
- xserver-1.5.2-backtrace-defines.patch: Get HAVE_BACKTRACE defined even at
  the DIX level.

* Fri Oct 10 2008 Adam Jackson <ajax@redhat.com> 1.5.2-2
- xserver-1.5.1-global-backtrace.patch: Make backtraces possible from
  outside the xfree86 DDX.
- xserver-1.5.2-mieq-backtrace.patch: bt when we fill the input queue.

* Fri Oct 10 2008 Adam Jackson <ajax@redhat.com> 1.5.2-1
- xserver 1.5.2
- xserver-1.5.0-comment-out-glxdri2.c: Drop, no longer relevant.
- xserver-1.5.0-xkb-core-kbd-map-fix.patch: Drop, merged.
- xserver-1.5.1-int10-leaks.patch: Drop, merged.

* Fri Oct 10 2008 Adam Jackson <ajax@redhat.com> 1.5.1-11
- xserver-1.3.0-no-prerelease-warning.patch: Drop.

* Tue Oct 07 2008 Dave Airlie <airlied@redhat.com> 1.5.1-10
- actually apply exa fix patch

* Tue Oct 07 2008 Adam Jackson <ajax@redhat.com> 1.5.1-9
- xserver-1.5.1-xgi.patch: Move XGI cards onto the sis driver. (#453812)

* Tue Oct 07 2008 Adam Jackson <ajax@redhat.com> 1.5.1-8
- xserver-1.5.1-int10-leaks.patch: Shut up some useless int10 debugging and
  plug a memory leak.

* Tue Oct 7 2008 Adam Jackson <ajax@redhat.com> 1.5.1-7
- xserver-1.5.1-mode-debug.patch: Force mode debugging on.

* Tue Oct 7 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.5.1-6
- xserver-1.5.0-xkb-core-kbd-map-fix.patch: don't invent groups when mapping
  from xkb to core and back, and squash canonical types into explicit ones on
  core reconstruction (2 patches). #460545

* Mon Oct 06 2008 Dave Airlie <airlied@redhat.com> 1.5.1-5
- xserver-1.5.1-exa-fix-glyph-segfault.patch - fix EXA rects crash (462447)

* Tue Sep 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.1-4
- fix typo. :P

* Tue Sep 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.1-3
- add xvfb-run helper script to Xvfb package

* Thu Sep 25 2008 Dave Airlie <airlied@redhat.com> 1.5.1-2
- fix crash with x11perf on r500 modesetting

* Tue Sep 23 2008 Adam Jackson <ajax@redhat.com> 1.5.1-1
- xserver 1.5.1
- Trim %%changelog.

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 1.5.0-6
- Comment out glxdri2.c since it doesn't compile. (krh says it
  won't break at runtime). 

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 1.5.0-5
- Bump BuildRequires on mesa-GL-devel. Maybe that will work.

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 1.5.0-4
- Bump BuildRequires on xorg-x11-proto-devel

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 1.5.0-3
- Change the external monitor patch to base off of amount of video ram.

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> 1.5.0-3
- Change the default screen limits to include room for a 1280 wide
  projector.

* Wed Sep 10 2008 Dave Airlie <airlied@redhat.com> 1.5.0-2
- bring master exa back

* Wed Sep 03 2008 Adam Jackson <ajax@redhat.com> 1.5.0-1
- xserver 1.5.0
- Revert to the EXA from 1.5.0, should be good enough one hopes.
- Add .gitignore from git, so working with the artificial git tree is less
  flakey.

* Mon Aug 25 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-10
- xserver-1.5.0-edid-backport.patch: Backport EDID updates from master.

* Wed Aug 20 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-9
- xserver-1.5.0-hide-cursor.patch: Suppress displaying the cursor until
  an app calls XDefineCursor().

* Thu Aug 14 2008 Kristian Høgsberg <krh@redhat.com> - 1.4.99.906-8
- Add bg-none-root patch for plymouth.

* Thu Aug 14 2008 Dave Airlie <airlied@redhat.com> 1.4.99.906-7
- EXA backport master EXA code for optimisations

* Wed Aug 13 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-6
- xserver-1.5.0-enable-selinux.patch: Enable selinux again.

* Tue Aug 05 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.4.99.906-5
- xserver-1.5.0-xkb-fix-ProcXkbSetXYZ-to-work-on-all.patch: force xkb requests
  to apply to all extension devices.
- drop call-SwitchCoreKeyboard.patch
- xserver-1.5.0-force-SwitchCoreKeyboard-for-evdev.patch: force
  SwitchCoreKeyboard for evdev devices to push device keymap into core device.

* Mon Aug 04 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-4
- 10-x11-keymap.fdi, fedora-setup-keyboard: Attempt to read keyboard settings
  from /etc/sysconfig/keyboard and stuff them into hal.

* Mon Aug 04 2008 Peter Hutterer <peter.hutterer@redhat.com> 1.4.99.906-3
- xserver-1.5.0-call-SwitchCoreKeyboard-for-first-device.patch: force a keymap
  switch to push the device keymap into the core device.

* Thu Jul 31 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-2
- Drop the evdev keyboarding patch.

* Thu Jul 24 2008 Adam Jackson <ajax@redhat.com> 1.4.99.906-1
- 1.5RC6.

* Wed Jul 02 2008 Adam Tkac <atkac redhat com> 1.4.99.905-2.20080701
- build with -rdynamic to make dri_swrast happy

* Mon Jun 30 2008 Adam Jackson <ajax@redhat.com> 1.4.99.905-1.20080701
- 1.5RC5.

* Thu Jun 19 2008 Adam Tkac <atkac redhat com>
- workaround broken AC_C_BIGENDIAN macro (#449944)

* Thu Jun 12 2008 Dave Airlie <airlied@redhat.com> 1.4.99.902-3.20080612
- xserver-1.5.0-fix-single-aspect.patch - fix 2560x1600 on my monitor.

* Thu Jun 12 2008 Dave Airlie <airlied@redhat.com> 1.4.99.902-2.20080612
- cve-2008-1377: Record and Security Extension Input validation
- cve-2008-1379: MIT-SHM extension Input Validation flaw
- cve-2008-2360: Render AllocateGlyph extension Integer overflows
- cve-2008-2361: Render CreateCursor extension Integer overflows
- cve-2008-2362: Render Gradient extension Integer overflows
- Rebase to 1.5 head for security patches for above

* Mon Jun 09 2008 Adam Jackson <ajax@redhat.com> 1.4.99.902-1.20080609
- Today's git snapshot.

* Tue May 06 2008 Bill Nottingham <notting@redhat.com> 1.4.99.901-29.20080415
- rebuild against new xorg-x11-xtrans-devel (#445303)

* Mon May 05 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-28.20080415
- xserver-1.5.0-compiz-clip-fix.patch: Make compiz stop blinking every
  so often. (#441219)

* Mon May 05 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-27.20080415
- xserver-1.5.0-hal-closedown.patch: Fix a crash in the hal code when
  closing a device.

* Mon Apr 28 2008 Soren Sandmann <sandmann@redhat.com>
- Preserve user's CFLAGS

* Thu Apr 24 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-26.20080415
- xserver-1.5.0-no-evdev-keyboards-kthnx.patch: Disable evdev for keyboards
  even on combo devices.  This means combo devices will go through the old
  mouse driver too.  Oh well.  (#440380)

* Thu Apr 24 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-25.20080415
- xserver-1.5.0-f-spot-screws-glx.patch: stop GLX crashing X server when
  f-spot exists (#443299)

* Wed Apr 23 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-24.20080415
- xserver-1.5.0-glcore-swap-no-crashy.patch: Fix issue with googleearth
  crashing GLcore.

* Tue Apr 22 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-23.20080415
- xserver-1.5.0-stenciled-visuals.patch: Prefer visuals with a stencil
  buffer for the default GLX visual.  (Hans de Goede, #442510)

* Tue Apr 15 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-22.20080415
- rebase to upstream server 1.5 branch from today - drop acr quirk

* Thu Apr 10 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-21.20080407
- xserver-1.5.0-selinux-off-by-default.patch: Re-disable selinux by default,
  again, in a way that lets you enable it if you really want to.

* Wed Apr 09 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-20.20080407
- xserver-1.5.0-quirk-acr.patch - add quirk for another monitor.

* Tue Apr 08 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-19.20080407
- Today's rebase.  Patch merge, some int10 fixes.

* Mon Apr 07 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-18.20080401
- xorg-x11-server-Red-Hat-extramodes.patch: Remove some of the more
  implausible modes.  Cargo cult programming woo.

* Fri Apr  4 2008 Kristian Høgsberg <krh@redhat.com> 1.4.99.901-17.20080401
- Add xserver-1.5.0-dont-bitch-about-record.patch (don't try to load
  librecord.so when we don't build it) and
  xserver-1.5.0-handle-failing-dri-create-screen.patch (#440491).

* Wed Apr  2 2008 Kristian Høgsberg <krh@redhat.com> 1.4.99.901-16.20080401
- Fix crash when DRI2 fails to initialize and crash when initializing
  software GL visuals (#440175).

* Tue Apr  1 2008 Kristian Høgsberg <krh@redhat.com> 1.4.99.901-15.20080401
- Rebase to new snapshot to pull in DRI2 direct rendering work.
- Stop shipping librecord.so.

* Tue Apr 01 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-14.20080314
- Remove vmmouse again, way too broken.  Let this be a lesson to you:
  never try.

* Thu Mar 27 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-13.20080314
- archify the vmmouse logic.

* Thu Mar 27 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-12.20080314
- xserver-1.5.0-fix-lsl-quirk.patch - fix the LSL quirk (#435216)

* Wed Mar 26 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-11.20080314
- xserver-1.5.0-vmmouse.patch: Use vmmouse(4) for the automagic mouse
  section.  It'll just fall back to the mouse(4) driver anyway if it's
  not a vmmouse.

* Tue Mar 18 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-10.20080314
- xserver-1.5.0-no-evdev-keyboards-kthnx.patch: Sorry, evdev keyboarding is
  just too broken.

* Fri Mar 14 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-9.20080314
- Today's snapshot.  Mostly just patch merge with rawhide.

* Thu Mar 13 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-8.20080310
- xserver-1.5.0-aspect-match.patch: Fix the RANDR 1.2 initial configuration
  heuristic for the case where the best possible mode is the first one in
  the first monitor's mode list.

* Thu Mar 13 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-7.20080310
- xserver-1.5.0-xaa-sucks: Disable XAA offscreen pixmaps by default.  They're
  almost always a performance loss anyway.  Use Option "XaaOffscreenPixmaps"
  to turn them back on.

* Thu Mar 13 2008 Dave Airlie <airlied@redhat.com> 1.4.99.901-6.20080310
- fix fbdev probing with no hardware to not load fbdev if pci slot claimed

* Wed Mar 12 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-5.20080310
- xserver-1.5.0-unselinux.patch: Disable selinux extension for now.
- xserver-1.5.0-ia64.patch: Fix ia64 PCI support. (#429878)

* Tue Mar 11 2008 Kristian Høgsberg <krh@redhat.com> 1.4.99.901-4.20080310
- Checkout the tip of the git snapshot so we get the most recent DRI2
  texture from pixmap changes in the build.  Bump mesa build requires.

* Tue Mar 11 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-3.20080310
- New 1.5 snapshot.
- xserver-1.5-x86emu.patch: Fix an x86emu quirk.

* Fri Mar 07 2008 Adam Jackson <ajax@redhat.com> 1.4.99.901-1.20080307
- Today's 1.5 snapshot.

* Tue Mar 04 2008 Adam Jackson <ajax@redhat.com> 1.4.99.900-0.28.20080304
- Today's 1.5 snapshot.
- Obsolete: xorg-x11-drv-magictouch to get it uninstalled.

* Mon Mar 03 2008 Adam Jackson <ajax@redhat.com> 1.4.99.900-0.27.20080303
- Switch to 1.5 branch and rebase.

* Thu Feb 28 2008 Jeremy Katz <katzj@redhat.com> - 1.4.99.1-0.26
- Pull in another SELinux fix from upstream

* Wed Feb 27 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.25
- Today's git snapshot.  Selinux fixes, XKB crash fix.

* Tue Feb 26 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.24
- Today's git snapshot.  PCI cleanups, AIGLX fix.

* Fri Feb 22 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.23
- Today's git snapshot.  Xinerama and XKB fixes, patch merging, etc.
- Remove some dead patches.

* Thu Feb 21 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.22
- Today's git snapshot, misc bugfixes.

* Fri Feb 15 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.21
- Today's git snapshot.  Features DRI2 and input hotplugging.  Tasty.

* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.20
- Conflict against insufficiently new libpciaccess. (#390751)

* Tue Jan 29 2008 Adam Tkac <atkac redhat com> 1.4.99.1-0.19
- added dix/protocol.txt to source subpackage

* Fri Jan 18 2008 Dave Airlie <airlied@redhat.com> 1.4.99.1-0.18
- cve-2007-6429.patch: Fix patch to not break java apps

* Fri Jan 18 2008 Dave Airlie <airlied@redhat.com> 1.4.99.1-0.17
- cve-2007-5760.patch: XFree86-Misc Extension Invalid Array Index Vulnerability
- cve-2007-6427.patch: XInput Extension Memory Corruption Vulnerability
- cve-2007-6428.patch: TOG-CUP Extension Memory Corruption Vulnerability
- cve-2007-6429.patch: EVI and MIT-SHM Extension Integer Overflow Vulnerability
- cve-2008-0006-server-fixup.patch: PCF Font Vulnerability - this patch isn't strictly required with new version of libXfont.

* Wed Jan 16 2008 Kristian Høgsberg <krh@redhat.com> 1.4.99.1-0.16
- Add xserver-1.4.99-engage-composite-crack-mode.patch to better hide
  protocol side effects such as loss of grabs and focus when
  redirecting/unredirecting windows (#350271).

* Mon Jan 07 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.15
- Today's git snapshot.  X-SELinux!
- Drop the code to migrate from /etc/X11/XF86Config*.
- s/perl -p -i -e/sed -i/g

* Mon Jan 07 2008 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.14
- Sync with F8 bugfixes:
  - xorg-x11-server-Red-Hat-extramodes.patch: Don't supply non-CVT-R timings
    for 1920x{1080,1200}.
  - xserver-1.3.0-ignore-extra-entity.patch: If a driver doesn't support
    secondary entities, don't fatal error just ignore and keep going.
  - xserver-1.3.0-randr-fix-set-rotations-xinerama.patch: Attempt to stop
    xinerama segfaulting randr12.

* Mon Dec 10 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.13
- xserver-1.4.99-alloca-poison.patch: Fatal error on {DE,}ALLOCATE_LOCAL
  so we don't build broken drivers.
- xserver-1.4.99-ssh-isnt-local.patch: Try harder to disable MIT-SHM for
  ssh-forwarded connections.

* Mon Dec 03 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.12
- xserver-1.4.99-apm-typedefs.patch: Temporary hack for broken kernels that
  don't publish the /dev/apm_bios types.

* Wed Nov 28 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.11
- Today's rebase.
- BR on git-core instead of git.
- Bump mesa-source BR to cope with extended CreatePixmap signature.
- xserver-1.4.99-openchrome.patch: Use openchrome not via when running
  without a config file.

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.10
- -devel Requires: pixman-devel and libpciaccess-devel.

* Mon Nov 12 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.8
- Fix buildrequires and other buildsystem nonsense.

* Fri Nov 02 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.6
- Merge a bunch of the more trivial patches upstream.
- New git snapshot containing the merged bits.
- Remove unused patches.
- Drop the XFree86 obsoletes.

* Fri Nov 02 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.5
- New git snapshot that fixes Xdmx build.
- Reenable Xdmx build.
- Rebase (or drop) the rest of our patches outside the PCI code.
- Add -common subpackage for shared files.
- Rename -sdk to -devel for verisimilitude.
- Simplify the %%configure line a bit.

* Thu Nov 01 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.4
- Update mesa and libdrm buildreqs.
- Reenable Xephyr build.

* Wed Oct 31 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.3
- Only invoke git-am once.
- Disable building mfb and cfb as well.

* Wed Oct 31 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.2
- BuildRequires: git.
- Manage the source directory as a git repo.
- Use git-am(1) to apply patches instead of %patch.
- Reformat a bunch of patches to conform to git-am's rules.
- Add wfb to file manifest.
- Drop afb, sorry Amiga users.
- Delete the SecurityPolicy man page from the buildroot, until we have a
  xorg-x11-server-common.
- Update to today's snapshot.

* Wed Oct 31 2007 Adam Jackson <ajax@redhat.com> 1.4.99.1-0.1
- Begin rebasing to git master.  It almost builds, assuming you disable
  glx, kdrive, and dmx, and remove like half the patches.

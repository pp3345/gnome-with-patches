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

%global gitdate 20120822
%global stable_abi 1

%if !0%{?gitdate} || %{stable_abi}
# Released ABI versions.  Have to keep these manually in sync with the
# source because rpm is a terrible language.
%global ansic_major 0
%global ansic_minor 4
%global videodrv_major 13
%global videodrv_minor 0
%global xinput_major 18
%global xinput_minor 0
%global extension_major 7
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
Version:   1.12.99.905
Release:   3%{?gitdate:.%{gitdate}}%{dist}
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

# Trivial things to never merge upstream ever:
# This really could be done prettier.
Patch5002: xserver-1.4.99-ssh-isnt-local.patch

# don't build the (broken) acpi code
Patch6011: xserver-1.6.0-less-acpi-brokenness.patch

# ajax needs to upstream this
Patch6030: xserver-1.6.99-right-of.patch
#Patch6044: xserver-1.6.99-hush-prerelease-warning.patch

# Fix libselinux-triggered build error
# RedHat/Fedora-specific patch
Patch7013: xserver-1.12-Xext-fix-selinux-build-failure.patch

# needed when building without xorg (aka s390x)
Patch7017: xserver-1.12.2-xorg-touch-test.patch

# send keycode/event type for slow keys enable (#816764)
Patch7020: xserver-1.12-xkb-fill-in-keycode-and-event-type-for-slow-keys-ena.patch

Patch7022: 0001-linux-Refactor-xf86-En-Dis-ableIO.patch
Patch7023: 0002-linux-Make-failure-to-iopl-non-fatal.patch
Patch7024: 0003-xfree86-Change-the-semantics-of-driverFunc-GET_REQUI.patch
Patch7025: 0001-Always-install-vbe-and-int10-sdk-headers.patch

# do not upstream - do not even use here yet
Patch7027: xserver-autobind-hotplug.patch

# backport fixes from list
Patch7030: 0001-xf86-crtc-don-t-free-config-name.patch
Patch7031: 0002-dix-free-default-colormap-before-screen-deletion.patch

# backport multi-seat fixes from list
Patch7040: 0001-config-udev-add-wrapper-around-check-if-server-is-no.patch
Patch7041: 0002-config-udev-respect-seat-for-hotplugged-video-device.patch
Patch7042: 0003-xf86-fix-multi-seat-video-device-support.patch

%global moduledir	%{_libdir}/xorg/modules
%global drimoduledir	%{_libdir}/dri
%global sdkdir		%{_includedir}/xorg

%ifarch s390 s390x %{?rhel:ppc ppc64}
%global with_hw_servers 0
%else
%global with_hw_servers 1
%endif

%if %{with_hw_servers}
%global enable_xorg --enable-xorg
%else
%global enable_xorg --disable-xorg
%endif

%ifnarch %{ix86} x86_64 %{arm}
%global no_int10 --disable-vbe --disable-int10-module
%endif

%global kdrive --enable-kdrive --enable-xephyr --disable-xfake --disable-xfbdev
%global xservers --enable-xvfb --enable-xnest %{kdrive} %{enable_xorg}

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
%global dri_flags --with-dri-driver-path=%{drimoduledir}
%else
%global dri_flags --disable-dri
%endif

%if 0%{?fedora}
%global bodhi_flags --with-vendor-name="Fedora Project"
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
%global Xorgperms %attr(4755, root, root)
%else
# disable until module loading is audited
%global Xorgperms %attr(0711,root,root) %caps(cap_sys_admin,cap_sys_rawio,cap_dac_override=pe)
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
* Mon Aug 27 2012 Dave Airlie <airlied@redhat.com> 1.12.99.905-3
- port multi-seat video fixes from upstream

* Fri Aug 24 2012 Dave Airlie <airlied@redhat.com> 1.12.99.905-2
- reintroduce auto config but working this time
- fix two recycle/exit crashes

* Wed Aug 22 2012 Dave Airlie <airlied@redhat.com> 1.12.99.905-1
- rebase to 1.12.99.905 snapshot

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 1.12.99.904-4
- autobind was horribly broken on unplug - drop it like its hotplug.

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 1.12.99.904-3
- add git fixes + autobind to gpu devices.

* Wed Aug 15 2012 Adam Jackson <ajax@redhat.com> 1.12.99.904-2
- Always install int10 and vbe sdk headers

* Wed Aug 08 2012 Dave Airlie <airlied@redhat.com> 1.12.99.904-1
- rebase to 1.12.99.904 snapshot

* Fri Aug 03 2012 Adam Jackson <ajax@redhat.com> 1.12.99.903-6
- Make failure to iopl non-fatal

* Mon Jul 30 2012 Adam Jackson <ajax@redhat.com> 1.12.99.903-5
- No need to --disable-xaa explicitly anymore.

* Thu Jul 26 2012 Adam Jackson <ajax@redhat.com> 1.12.99.903-4
- Install xserver-sdk-abi-requires.release based on stable_abi not gitdate,
  so drivers built against a server that Provides multiple ABI versions will
  Require the stable version.

* Thu Jul 26 2012 Adam Jackson <ajax@redhat.com> 1.12.99.903-3
- Make it possible to Provide: both stable and gitdate-style ABI versions.

* Thu Jul 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.99.903-2
- xserver-1.12-os-print-newline-after-printing-display-name.patch: drop,
  014ad46f1b353a95e2c4289443ee857cfbabb3ae

* Thu Jul 26 2012 Dave Airlie <airlied@redhat.com> 1.12.99.903-1
- rebase to 1.12.99.903 snapshot

* Wed Jul 25 2012 Dave Airlie <airlied@redhat.com> 1.12.99.902-3
- fix crash due to GLX being linked twice

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.99.902-2.20120717
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.12.99.902-1
- server 1.12.99.902

* Mon Jul 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.3-1
- server 1.12.3

* Tue Jun 26 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.2-4
- send keycode/event type down the wire when SlowKeys enable, otherwise
  GNOME won't warn about it (#816764)

* Thu Jun 21 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.12.2-3
- print newline after printing $DISPLAY to -displayfd (#824594)

* Fri Jun 15 2012 Dan Horák <dan[at]danny.cz> 1.12.2-2
- fix build without xorg (aka s390x)

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

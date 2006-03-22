%define pkgname xorg-server
%define cvsdate cvs20060321
%define mesalib MesaLib-6.5-cvs20060321.tar.bz2

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   1.0.99.1
Release:   2
URL:       http://www.x.org
License:   MIT/X11
Group:     User Interface/X
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   http://xorg.freedesktop.org/releases/X11R7.0/src/everything/%{pkgname}-%{version}.tar.bz2
Source1:   %{mesalib}
Source100: comment-header-modefiles.txt

Patch0:    xorg-x11-server-0.99.3-init-origins-fix.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=5093
Patch1:    xorg-server-0.99.3-fbmmx-fix-for-non-SSE-cpu.patch
# xorg-server-0.99.3-rgb.txt-dix-config-fix.patch is from post-RC2 CVS
Patch2:    xorg-server-0.99.3-rgb.txt-dix-config-fix.patch
Patch3:    xserver-1.0.0-parser-add-missing-headers-to-sdk.patch
Patch4:    xorg-x11-server-1.0.1-composite-fastpath-fdo4320.patch
Patch5:    xorg-server-1.0.1-backtrace.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=6010
Patch6:    xserver-1.0.1-randr-sdk.patch
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=181292.  hacky patch
Patch7:    xorg-x11-server-1.0.1-fpic-libxf86config.patch
Patch8:    xorg-server-1.0.99-composite-visibility.patch

Patch1000:  xorg-redhat-die-ugly-pattern-die-die-die.patch
Patch1001:  xorg-x11-server-1.0.1-Red-Hat-extramodes.patch

# INFO: We don't ship the X server on s390/s390x/ppc64
ExcludeArch: s390 s390x ppc64

%define moduledir	%{_libdir}/xorg/modules
%define sdkdir		%{_includedir}/xorg

%ifarch %{ix86} x86_64 ppc ia64
%define xservers --enable-xorg --enable-dmx --enable-xvfb --enable-xnest
%else
%define xservers --disable-xorg --disable-dmx --enable-xvfb --enable-xnest
%endif

# NOTE: The developer utils are intended for low level video driver hackers,
# doing low level bit twiddling, who really know what they are doing, and are
# disabled by default, as they are not generally useful to end users.
# FIXME: Reconfigure the spec file to put them in a separate subpackage, so
# I can build one build with them enabled, install them, then disable it again.
%define with_developer_utils	0

%ifarch %{ix86} x86_64 ppc ia64
%define with_dri	1
%else
%define with_dri	0
%endif

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros >= 0.99.1
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
# FIXME: The version specification can be removed from here in the future,
# as it is not really mandatory, but forces a bugfix workaround on people who
# are using pre-rawhide modular X.
BuildRequires: libXfont-devel >= 0.99.2-3
BuildRequires: libXau-devel
BuildRequires: libxkbfile-devel
# libdmx-devel needed for Xdmx
BuildRequires: libdmx-devel
# libXdmcp-devel needed for Xdmx
BuildRequires: libXdmcp-devel
# libXmu-devel needed for Xdmx
BuildRequires: libXmu-devel
# libXext-devel needed for Xdmx
BuildRequires: libXext-devel
# libX11-devel needed for Xdmx
BuildRequires: libX11-devel
# libXrender-devel needed for Xdmx
BuildRequires: libXrender-devel
# libXi-devel needed for Xdmx
BuildRequires: libXi-devel
# libXres-devel needed for something that links to libXres that I never bothered to figure out yet
BuildRequires: libXres-devel
# libfontenc-devel needed for Xorg, but not specified by
# upstream deps.  Build fails without it.
BuildRequires: libfontenc-devel
# liblbxutil-devel needed for lbx
BuildRequires: liblbxutil-devel
# Required for Xtst examples
BuildRequires: libXtst-devel
# For Xdmxconfig 
BuildRequires: libXt-devel libXpm-devel libXaw-devel
# To query fontdir from fontutil.pc
BuildRequires: xorg-x11-font-utils >= 1.0.0-1
# Needed at least for DRI enabled builds
%if %{with_dri}
BuildRequires: mesa-libGL-devel >= 6.4.1-1
# "mesa-libGL-source >= 6.4.2-2" required for the solution for bug #176976
# BuildRequires: mesa-source >= 6.4.2-2
BuildRequires: libdrm-devel >= 2.0-1
%endif
%description
X.Org X11 X server

# ----- Xorg --------------------------------------------------------

%package Xorg
Summary: Xorg X server
Group: User Interface/X
# NOTE: The X server invokes xkbcomp directly, so this is required.
Requires: xkbcomp
# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base
# NOTE: Require some basic drivers for minimal configuration. (#173060)
Requires: xorg-x11-drv-mouse xorg-x11-drv-keyboard xorg-x11-drv-vesa
# NOTE: Require the driver meta-package to ensure that all drivers are always
# installed all of the time.  Why?  To guarantee that the drivers for your
# video and input devices are always installed all of the time, and ensure
# that OS installs and upgrades "work" without ending up with "oops, my
# driver isn't installed".  Drivers have always been "all installed" in
# every previous OS release, and this one is no different.  Drivers are split
# up into individual packages to facilitate making easy individual driver
# updates, NOT for allowing people to uninstall drivers to save $0.01 of
# hard disk space.  Why?  Because there is no "good" reason not to do so,
# necause 1Gb of hard disk space costs about $0.75 right now for starters.
Requires: xorg-x11-drivers >= 0.99.2-4

# NOTE: We use implementation non-specific "xkbdata" here, to make it easy
# to switch to the freedesktop.org 'xkeyboard-config' project replacment
# in the future.
Requires: xkbdata
# FIXME: Investigate these two and see what utils are needed, and use virtuals
Requires: xorg-x11-server-utils >= 0.99.2-5
Requires: xorg-x11-utils
# FIXME: This Requires on libXfont can be removed from here in the future,
# as it is not really mandatory, but forces a bugfix workaround on people who
# are using pre-rawhide modular X.
Requires: libXfont >= 0.99.2-3

Obsoletes: XFree86 xorg-x11
# NOTE: This virtual provide should be used when one wants to depend on
# the implementation specific (and optionally version specific) Xorg X
# server, but in an OS packaging independent manner.  This futureproofs
# package dependencies against possible future Xorg package renaming.
Provides: Xorg = %{version}-%{release}
Provides: Xserver

%description Xorg
X.org X11 is an open source implementation of the X Window System.  It
provides the basic low level functionality which full fledged
graphical user interfaces (GUIs) such as GNOME and KDE are designed
upon.

# ----- Xnest -------------------------------------------------------

%package Xnest
Summary: A nested server.
Group: User Interface/X
#Requires: %{name} = %{version}-%{release}
Obsoletes: XFree86-Xnest, xorg-x11-Xnest
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xnest X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xnest

%description Xnest
Xnest is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.

# ----- Xdmx --------------------------------------------------------

%package Xdmx
Summary: Distributed Multihead X Server and utilities
Group: User Interface/X
#Requires: %{name}-Xorg = %{version}-%{release}
Obsoletes: xorg-x11-Xdmx
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xdmx X server.  It is intentionally not
# versioned, since it should be agnostic.
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

# ----- Xvfb --------------------------------------------------------

%package Xvfb
Summary: A X Windows System virtual framebuffer X server.
Group: User Interface/X
Obsoletes: XFree86-Xvfb xorg-x11-Xvfb
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xvfb X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xvfb

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on
machines with no display hardware and no physical input devices.
Xvfb simulates a dumb framebuffer using virtual memory.  Xvfb does
not open any devices, but behaves otherwise as an X display.  Xvfb
is normally used for testing servers.

# ----- sdk ---------------------------------------------------------

%package sdk
Summary: SDK for X server driver module development
Group: User Interface/X
Obsoletes: XFree86-sdk xorg-x11-sdk
Requires: xorg-x11-util-macros
Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Provides: libxf86config-devel = %{version}-%{release}

%description sdk
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.

# -------------------------------------------------------------------

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p0 -b .init-origins-fix
#%patch1 -p0 -b .fbmmx-fix-for-non-SSE-cpu
#%patch2 -p0 -b .rgb.txt-dix-config-fix
%patch3 -p0 -b .parser-add-missing-headers-to-sdk
%patch4 -p0 -b .composite-fastpath-fdo4320
%patch5 -p0 -b .backtrace
%patch6 -p1 -b .randrsdk
%patch7 -p1 -b .xf86configfpic
%patch8 -p1 -b .composite-visibility

%patch1000 -p0 -b .redhat-die-ugly-pattern-die-die-die
%patch1001 -p1 -b .Red-Hat-extramodes

tar xfj %{_sourcedir}/%{mesalib}

%build
#FONTDIR="${datadir}/X11/fonts"
#DEFAULT_FONT_PATH="${FONTDIR}/misc:unscaled,${FONTDIR}/TTF/,${FONTDIR}/OTF,${FONTDIR}/Type1/,${FONTDIR}/CID/,${FONTDIR}/100dpi:unscaled,${FONTDIR}/75dpi:unscaled"

#	--disable-dependency-tracking \

automake; autoconf
%configure %{xservers} \
	--disable-xprint \
	--disable-static \
	--enable-composite \
	--enable-xtrap \
	--enable-xcsecurity \
	--enable-xevie \
	--enable-lbx \
%if %{with_dri}
	--enable-dri \
	--with-mesa-source=%{_builddir}/%{pkgname}-%{version}/Mesa-6.5 \
%endif
	--with-module-dir=%{moduledir} \
	--with-os-name="Fedora Core 5" \
	--with-os-vendor="Red Hat, Inc." \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
	--with-rgb-path=%{_datadir}/X11/rgb \
	--disable-xorgcfg \
	--enable-install-libxf86config \
	--with-fontdir=%(pkg-config --variable=fontdir fontutil)

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT moduledir=%{moduledir}

# Remove all libtool archives (*.la)
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

# FIXME: This should be done upstream, so it's one less thing to hack.
# Make these directories now so the Xorg package can own them.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

# Install the vesamodes and extramodes files to let our install/config tools
# be able to parse the same modelist as the X server uses (rhpxl).
{
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/xorg
    for each in vesamodes extramodes ; do
        install -m 0644 %{SOURCE100} $RPM_BUILD_ROOT%{_datadir}/xorg/$each
        cat hw/xfree86/common/$each >> $RPM_BUILD_ROOT%{_datadir}/xorg/$each
        chmod 0444 $RPM_BUILD_ROOT%{_datadir}/xorg/$each
    done
}

# FIXME: Remove unwanted files/dirs
{
    rm $RPM_BUILD_ROOT%{_bindir}/xorgconfig
    rm $RPM_BUILD_ROOT%{_mandir}/man1/xorgconfig.1*
    rm $RPM_BUILD_ROOT%{_libdir}/X11/Cards
    rm $RPM_BUILD_ROOT%{_libdir}/X11/Options
    rm $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/cfg.sample
    rm $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/xorg.cfg
%if ! %{with_developer_utils}
    rm -f $RPM_BUILD_ROOT%{_bindir}/inb
    rm -f $RPM_BUILD_ROOT%{_bindir}/inl
    rm -f $RPM_BUILD_ROOT%{_bindir}/inw
    rm -f $RPM_BUILD_ROOT%{_bindir}/ioport
    rm -f $RPM_BUILD_ROOT%{_bindir}/outb
    rm -f $RPM_BUILD_ROOT%{_bindir}/outl
    rm -f $RPM_BUILD_ROOT%{_bindir}/outw
    rm -f $RPM_BUILD_ROOT%{_bindir}/pcitweak
    rm -f $RPM_BUILD_ROOT%{_bindir}/cvt
%endif
}

%clean
rm -rf $RPM_BUILD_ROOT

%pre Xorg
{
  # Install/Upgrade section
  pushd /etc/X11
  # Migrate any pre-existing XFree86 4.x config file to xorg.conf if it
  # doesn't already exist, and rename any remaining XFree86 4.x config files
  # to have .obsoleted file extensions, to help avoid end user confusion for
  # people unaware of the config file name change between server
  # implementations, and avoid bug reports.  If this turns out to confuse
  # users, I can modify it to add comments to the top of the obsoleted files
  # to point users to xorg.conf   <mharris@redhat.com>
  for configfile in XF86Config XF86Config-4 ; do
    if [ -r $configfile ]; then
      if [ -r xorg.conf ]; then
        mv -f $configfile $configfile.obsoleted
    else
        mv -f $configfile xorg.conf
      fi
    fi
  done
  # Massage pre-existing config files to work properly with X.org X11
  # - Remove xie and pex5 modules from the config files, as they are long
  #   since obsolete, and not provided since XFree86 4.2.0
  # - Remove Option "XkbRules" "xfree86" to help work around upgrade problems
  #   such as https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=120858
#  for configfile in xorg.conf ; do
    configfile="xorg.conf"
    OLD_MODULEPATH="/usr/X11R6/lib/modules"
    if [ -r $configfile -a -w $configfile ]; then
      # Remove module load lines from the config file for obsolete modules
      perl -p -i -e 's/^.*Load.*"(pex5|xie|xtt).*\n$"//gi' $configfile
      # Change the keyboard configuration from the deprecated "keyboard"
      # driver, to the newer "kbd" driver.
      perl -p -i -e 's/^\s*Driver(.*)"keyboard"/Driver\1"kbd"/gi' $configfile
      # Remove any Options "XkbRules" lines that may be present
      perl -p -i -e 's/^.*Option.*"XkbRules".*"(xfree86|xorg)".*\n$//gi' $configfile
      # Remove RgbPath specifications from the config file as they are
      # unnecessary, and break upgrades from monolithic to modular X.
      # Fixes bugs (#173036, 173435, 173453, 173428)
      perl -p -i -e 's#^\s*RgbPath.*$##gi' $configfile
      # If ModulePath is specified in the config file, check for the old
      # monolithic module path, and replace it with the new one.
      perl -p -i -e "m,^\s*ModulePath.*\"${OLD_MODULEPATH}\".*$,; s,${OLD_MODULEPATH},%{moduledir}," $configfile
    fi
#  done
  popd
} &> /dev/null || :

# ----- Xorg --------------------------------------------------------

%files Xorg
%defattr(-,root,root,-)
# FIXME: The build fails to find the Changelog for some reason.
#%doc ChangeLog
%{_bindir}/X
%attr(4711, root, root) %{_bindir}/Xorg
%{_bindir}/getconfig
%{_bindir}/getconfig.pl
%{_bindir}/gtf
%if %{with_developer_utils}
%{_bindir}/inb
%{_bindir}/inl
%{_bindir}/inw
%{_bindir}/ioport
%{_bindir}/outb
%{_bindir}/outl
%{_bindir}/outw
%{_bindir}/pcitweak
%{_bindir}/cvt
%endif
%{_bindir}/scanpci
%dir %{_datadir}/xorg
%{_datadir}/xorg/vesamodes
%{_datadir}/xorg/extramodes
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libGLcore.so
%{_libdir}/xorg/modules/extensions/libdbe.so
%{_libdir}/xorg/modules/extensions/libdri.so
%{_libdir}/xorg/modules/extensions/libextmod.so
%{_libdir}/xorg/modules/extensions/libglx.so
%{_libdir}/xorg/modules/extensions/librecord.so
%{_libdir}/xorg/modules/extensions/libxtrap.so
%dir %{_libdir}/xorg/modules/input
%dir %{_libdir}/xorg/modules/fonts
%{_libdir}/xorg/modules/fonts/libbitmap.so
%{_libdir}/xorg/modules/fonts/libfreetype.so
%{_libdir}/xorg/modules/fonts/libtype1.so
%dir %{_libdir}/xorg/modules/linux
%{_libdir}/xorg/modules/linux/libdrm.so
%{_libdir}/xorg/modules/linux/libfbdevhw.so
%dir %{_libdir}/xorg/modules/multimedia
%{_libdir}/xorg/modules/multimedia/bt829_drv.so
%{_libdir}/xorg/modules/multimedia/fi1236_drv.so
%{_libdir}/xorg/modules/multimedia/msp3430_drv.so
%{_libdir}/xorg/modules/multimedia/tda8425_drv.so
%{_libdir}/xorg/modules/multimedia/tda9850_drv.so
%{_libdir}/xorg/modules/multimedia/tda9885_drv.so
%{_libdir}/xorg/modules/multimedia/uda1380_drv.so
%{_libdir}/xorg/modules/libafb.so
%{_libdir}/xorg/modules/libcfb.so
%{_libdir}/xorg/modules/libcfb16.so
%{_libdir}/xorg/modules/libcfb32.so
%{_libdir}/xorg/modules/libddc.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libi2c.so
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/libmfb.so
%{_libdir}/xorg/modules/libpcidata.so
%{_libdir}/xorg/modules/librac.so
%{_libdir}/xorg/modules/libramdac.so
%{_libdir}/xorg/modules/libscanpci.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libvbe.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libxaa.so
%{_libdir}/xorg/modules/libxf1bpp.so
%{_libdir}/xorg/modules/libxf4bpp.so
%{_libdir}/xorg/modules/libxf8_16bpp.so
%{_libdir}/xorg/modules/libxf8_32bpp.so
%dir %{_libdir}/xserver
%{_libdir}/xserver/SecurityPolicy
#%dir %{_mandir}/man1x
%{_mandir}/man1/getconfig.1x*
%{_mandir}/man1/gtf.1x*
%{_mandir}/man1/pcitweak.1x*
%{_mandir}/man1/scanpci.1x*
%{_mandir}/man1/Xorg.1x*
%{_mandir}/man1/Xserver.1x*
%{_mandir}/man1/cvt.1*
#%dir %{_mandir}/man4x
#%{_mandir}/man4/fbdevhw.4x*
%{_mandir}/man4/fbdevhw.4*
#%dir %{_mandir}/man5x
%{_mandir}/man5/getconfig.5x*
%{_mandir}/man5/xorg.conf.5x*
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

# ----- Xnest -------------------------------------------------------

%files Xnest
%defattr(-,root,root,-)
%{_bindir}/Xnest
#%dir %{_mandir}/man1x
%{_mandir}/man1/Xnest.1x*

# ----- Xdmx --------------------------------------------------------

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
%{_bindir}/xdmx
%{_bindir}/xdmxconfig
#%dir %{_mandir}/man1x
%{_mandir}/man1/Xdmx.1x*
%{_mandir}/man1/dmxtodmx.1x*
%{_mandir}/man1/vdltodmx.1x*
%{_mandir}/man1/xdmxconfig.1x*

# ----- Xvfb --------------------------------------------------------

%files Xvfb
%defattr(-,root,root,-)
%{_bindir}/Xvfb
#%dir %{_mandir}/man1x
%{_mandir}/man1/Xvfb.1x*

# ----- sdk ---------------------------------------------------------

%files sdk
%defattr(-,root,root,-)
%{_libdir}/libxf86config.a
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
#%dir %{_includedir}/xorg/sdk
%{sdkdir}/*.h
%{_datadir}/aclocal/xorg-server.m4

# -------------------------------------------------------------------

%changelog
* Wed Mar 22 2006 Soren Sandmann <sandmann@redhat.com> 1.0.99.1-2
- Add xorg-server-1.0.99-composite-visibility.patch to get rid of flashing
  titlebars in compositing metacity.

* Tue Mar 21 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.1-1
- Update to 1.0.99.1 snapshot.

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1.0.1-8
- build libxf86config with -fPIC (#181292)
- fix sgi 1600sw extra mode (#182430)

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> 1.0.1-7
- install randrstr.h as part of sdk as required for building some drivers

* Tue Feb 21 2006 Mike A. Harris <mharris@redhat.com>
- Added xorg-server-1.0.1-backtrace.patch which enables the Xorg server's
  built in backtrace support by default, as it was inadvertently disabled in
  7.0.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-6.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-6
- Added xorg-x11-server-1.0.1-Red-Hat-extramodes.patch which is a merger of
  XFree86-4.2.99.2-redhat-custom-modelines.patch and
  xorg-x11-6.8.2-laptop-modes.patch from FC4 for (#180301)
- Install a copy of the vesamodes and extramodes files which contain the list
  of video modes that are built into the X server, so that the "rhpxl" package
  does not have to carry around an out of sync copy for itself. (#180301)

* Tue Feb  7 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-5
- Updated "BuildRequires: mesa-source >= 6.4.2-2" to get fix for (#176976)

* Mon Feb  6 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4
- Fix brown paper bag error introduced in rpm post script in 1.0.1-4.

* Mon Feb  6 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added xorg-x11-server-1.0.1-composite-fastpath-fdo4320.patch with changes
  suggested by ajax to fix (fdo#4320).
- Cosmetic cleanups to satiate the banshees.

* Sun Feb  5 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added xorg-x11-server-1.0.1-fbpict-fix-rounding.patch from CVS HEAD.
- Added xorg-x11-server-1.0.1-SEGV-on-null-interface.patch which prevents a
  SEGV on null interfaces (#174279,178986)

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xserver 1.0.1 from X11R7.0

* Thu Dec 22 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Added "Provides: libxf86config-devel = %{version}-%{release}" to sdk package.

* Wed Dec 21 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Added xserver-1.0.0-parser-add-missing-headers-to-sdk.patch to provide the
  necessary libxf86config.a headers to be able to use the library. (#173084)

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xserver 1.0.0 from X11R7 RC4
- Removed the following patches, which are now integrated upstream:
  - xorg-server-0.99.3-rgb.txt-dix-config-fix.patch,
  - xorg-server-0.99.3-fbmmx-fix-for-non-SSE-cpu.patch
- Changed manNx directories to manN to match upstream defaults.
- Added libxf86config.a to sdk subpackage.
- Updated build dependency of "mesa-libGL-devel >= 6.4.1-1"
- Added "BuildRequires: xorg-x11-font-utils >= 1.0.0-1" to be able to query
  the fontdir from fontutil.pc which is implemented currently by a custom
  patch.
- Enable xtrap, xcsecurity, xevie, and lbx on all builds, not just DRI builds.
- Fix sdk installation path, so that drivers can find the files again.
- Update file manifest, to deal with X server modules that have moved to
  a subdir, etc.

* Mon Nov 28 2005 Kristian Høgsberg <krh@redhat.com>
- Add a few missing BuildRequires.

* Fri Nov 25 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-9
- Added "Requires: xorg-x11-drivers >= 0.99.2-4" as a dependency of the Xorg
  subpackage, to ensure that anaconda installs all of the drivers during OS
  installs and upgrades, as requested by Jeremy Katz.

* Fri Nov 25 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-8
- Added xorg-server-0.99.3-rgb.txt-dix-config-fix.patch which fixes the
  --with-rgb-path option to actually *work*.
- Updated libdrm dep to 1.0.5

* Wed Nov 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-7
- Update xorg-x11-server-utils dep to 0.99.2-5 to ensure rgb.txt is installed
  in correct location - _datadir/X11/rgb
- Added --with-rgb-path configure option to specify _datadir/X11/rgb so the
  X server finds the rgb.txt database properly, for bugs (#173453, 173435,
  173428, 173483, 173734, 173737, 173594)
- Added xorg-server-0.99.3-fbmmx-fix-for-non-SSE-cpu.patch to prevent SSE/MMX
  code from being activated on non-capable VIA CPU. (#173384,fdo#5093)

* Thu Nov 17 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-6
- Add the missing rpm pre script from monolithic xorg-x11 packaging,
  clean it up a bit, reorder it for slight performance gain.
- Add some perl magic to pre script to remove RgbPath from xorg.conf,
  in order to fix bug (#173036, 173435, 173453, 173428)
- Add more perl magic to pre script to update ModulePath to the new
  location if it is specified in xorg.conf.
- Added xorg-x11-server-0.99.3-init-origins-fix.patch ported from monolithic
  xorg-x11 package to fix Xinerama bug.
- Added xorg-redhat-die-ugly-pattern-die-die-die.patch to kill the ugly grey
  stipple once again for bug (#173423).
- Added "BuildRequires: libdrm-devel" for DRI enabled builds.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-5
- Xorg server should be suid for users to be able to run startx (#173064)

* Mon Nov 14 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-4
- Added temporary "BuildRequires: libXfont-devel >= 0.99.2-3" and
  "Requires: libXfont-devel >= 0.99.2-3" to ensure early-testers of
  pre-rawhide modular X have installed the work around for (#172997).
- Added implementation specific "Requires: xkbdata" to Xorg subpackage, as
  we want to ensure the xkb data files are present, but allow us the option
  of easily switching implementations to "xkeyboard-config" at a future
  date, if we decide to go that route.
- Re-enable _smp_mflags during build.
- Added "Requires: xorg-x11-drv-vesa" to Xorg subpackage (#173060)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-3
- provide Xserver
- add another requires for basic bits

* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-2
- add some deps to the Xorg subpackage for base fonts, keyboard and mouse 
  drivers, and rgb.txt that the server really wont work without

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Update to xorg-server-0.99.3 from X11R7 RC2.
- Add xorg-server.m4 to sdk subpackage, and "X" symlink to Xorg subpackage.

* Thu Nov 10 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-4
- Added "Requires: xkbcomp" for Xorg server, as it invokes it internally.

* Wed Nov 9 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added "BuildRequires: libXtst-devel" for Xtst examples.

* Mon Nov 7 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added versioning to Xorg virtual Provide, to allow config tools and driver
  packages to have version based requires.

* Thu Oct 27 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Update to xorg-server-0.99.2 from X11R7 RC1.
- Add "BuildRequires: xorg-x11-util-macros >= 0.99.1".
- Add "BuildRequires: mesa-source >= 6.4-4" for DRI builds.
- Added dmx related utilities to Xdmx subpackage.
- Individually list each X server module in file manifest.
- Hack man1 manpages to be installed into man1x.
- Add the following ./configure options --disable-dependency-tracking,
  --enable-composite, --enable-xtrap, --enable-xcsecurity, --enable-xevie,
  --enable-lbx, --enable-dri, --with-mesa-source, --with-module-dir,
  --with-os-name, --with-os-vendor, --with-xkb-output, --disable-xorgcfg
- Added getconfig, scanpci et al to Xorg subpackage
- Added inb, inl, inw, ioport, outboutl, outw, pcitweak utils to Xorg package
  conditionally, defaulting to "off".  These utilities are potentially
  dangerous and can physically damage hardware and/or destroy data, so are
  not shipped by default.
- Added "BuildRequires: libdmx-devel" for dmx utilities
- Added "BuildRequires: libXres-devel" for Xres examples
- Added {_libdir}/xserver/SecurityPolicy to Xorg subpackage for XSECURITY

* Mon Oct  3 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2.cvs20050830.2
- Fix license tag to be "MIT/X11"
- Change Xdmx subpackage to Obsolete xorg-x11-Xdmx instead of xorg-x11-Xnest

* Sun Oct  2 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2.cvs20050830.1
- Update BuildRequires for new library package naming (libX...)
- Use Fedora Extras style BuildRoot tag
- Invoke make with _smp_mflags to take advantage of SMP systems

* Tue Aug 30 2005 Kristian Hogsberg <krh@redhat.com> 0.99.1-2.cvs20050830
- Go back to %spec -n, use new cvs snapshot that supports overriding
  moduledir during make install, use %makeinstall.
- Drop %{moduledir}/multimedia globs.

* Fri Aug 26 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2.cvs20050825.0
- Added build dependency on xorg-x11-libfontenc-devel, as the build fails
  half way through without it, even though upstream dependencies do not
  specify it as required.

* Tue Aug 23 2005 Kristian Hogsberg <krh@redhat.com> 0.99.1-1
- Initial spec file for the modular X server.

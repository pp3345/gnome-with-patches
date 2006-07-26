%define pkgname xorg-server

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   1.1.1
# NOTE: Now using the 'dist' tag as per http://fedoraproject.org/wiki/DistTag
# For rawhide builds, bump the number /before/ the dist tag.  For package
# upgrades to officially released distribution releases, if the package
# Version field above is not changing, append and/or bump a digit /after/
# the dist tag.  ie:  25%{dist}.0 -> 25%{dist}.1 ...
Release:   12%{?dist}
URL:       http://www.x.org
License:   MIT/X11
Group:     User Interface/X
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.bz2
Source100: comment-header-modefiles.txt

Patch0:    xorg-x11-server-0.99.3-init-origins-fix.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=5093
Patch1:    xorg-server-0.99.3-fbmmx-fix-for-non-SSE-cpu.patch
Patch3:    xserver-1.0.0-parser-add-missing-headers-to-sdk.patch
Patch4:    xorg-x11-server-1.0.1-composite-fastpath-fdo4320.patch
Patch5:    xorg-x11-server-libxf86config-dont-write-empty-sections.patch

# OpenGL compositing manager feature/optimization patches.
Patch100:  xorg-x11-server-1.1.0-no-move-damage.patch
Patch101:  xorg-x11-server-1.1.0-dont-backfill-bg-none.patch
Patch102:  xorg-x11-server-1.1.0-gl-include-inferiors.patch
Patch103:  xorg-x11-server-1.1.0-tfp-damage.patch
Patch104:  xorg-x11-server-1.1.0-mesa-copy-sub-buffer.patch
Patch105:  xorg-x11-server-1.1.1-enable-composite.patch
Patch106:  xorg-x11-server-1.1.1-no-composite-in-xnest.patch

# Red Hat specific tweaking, not intended for upstream
# XXX move these to the end of the list
Patch1000:  xorg-redhat-die-ugly-pattern-die-die-die.patch
Patch1001:  xorg-x11-server-Red-Hat-extramodes.patch
Patch1002:  xorg-x11-server-1.1.0-redhat-xephyr-only-hack.patch
Patch1003:  xorg-x11-server-1.0.1-fpic-libxf86config.patch
Patch1004:  xorg-x11-server-1.1.1-selinux-awareness.patch

# Backports of post-1.1 stuff.
Patch2001:  xorg-x11-server-1.1.0-pci-scan-fixes.patch
Patch2004:  xorg-x11-server-1.1.0-no-zlib.patch
Patch2005:  xorg-x11-server-1.1.1-Xdmx-render-fix-fdo7482.patch

# autoconfiguration feature patches
Patch3001:  xorg-x11-server-1.1.0-edid-mode-injection-1.patch
Patch3002:  xorg-x11-server-1.1.0-edid-mode-injection-2.patch
Patch3003:  xorg-x11-server-1.1.0-cvt-generator-in-core.patch
Patch3004:  xorg-x11-server-1.1.0-no-autoconfig-targetrefresh.patch
Patch3005:  xorg-x11-server-1.1.1-getconfig-pl-die-die-die.patch
Patch3006:  xorg-x11-server-1.1.1-dpms-on-by-default.patch
Patch3007:  xorg-x11-server-1.1.1-edid-root-window-properties.patch
Patch3008:  xorg-x11-server-1.1.1-sanedefaultmode.patch
Patch3009:  xorg-x11-server-1.1.1-module-list.patch

%define moduledir	%{_libdir}/xorg/modules
%define drimoduledir	%{_libdir}/dri
%define sdkdir		%{_includedir}/xorg

%ifarch %{ix86} x86_64 ppc ppc64 ia64 alpha sparc sparc64
%define xservers --enable-xorg --enable-dmx --enable-xvfb --enable-xnest --enable-kdrive --enable-xephyr
%define with_hw_servers 1
%define with_dmx_server 1
%endif
%ifarch s390 s390x
%define xservers --disable-xorg --disable-dmx --enable-xvfb --enable-xnest --enable-kdrive --enable-xephyr
%define with_hw_servers 0
%define with_dmx_server 0
%endif

# NOTE: The developer utils are intended for low level video driver hackers,
# doing low level bit twiddling, who really know what they are doing, and are
# disabled by default, as they are not generally useful to end users.
# FIXME: Reconfigure the spec file to put them in a separate subpackage, so
# I can build one build with them enabled, install them, then disable it again.
%define with_developer_utils	0

%ifarch %{ix86} x86_64 ppc ia64 alpha sparc sparc64
%define with_dri	1
%endif
%ifarch ppc64 s390 s390x
%define with_dri	0
%endif

# FIXME: Temporary Build deps on autotools, as needed...
#BuildRequires: automake17
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros >= 0.99.1
BuildRequires: xorg-x11-proto-devel >= 7.1-1
BuildRequires: xorg-x11-xtrans-devel
# FIXME: The version specification can be removed from here in the future,
# as it is not really mandatory, but forces a bugfix workaround on people who
# are using pre-rawhide modular X.
BuildRequires: libXfont-devel >= 0.99.2-3
BuildRequires: libXau-devel
BuildRequires: libxkbfile-devel
# libXres-devel needed for something that links to libXres that I never bothered to figure out yet
BuildRequires: libXres-devel
# libfontenc-devel needed for Xorg, but not specified by
# upstream deps.  Build fails without it.
BuildRequires: libfontenc-devel
# Required for Xtst examples
BuildRequires: libXtst-devel
# libXdmcp-devel needed for Xdmx, Xnest, Xephyr
BuildRequires: libXdmcp-devel
# libX11-devel needed for Xdmx, Xnest, Xephyr
BuildRequires: libX11-devel
# libXext-devel needed for Xdmx, Xnest, Xephyr
BuildRequires: libXext-devel
#
BuildRequires: freetype-devel >= 2.1.9-1
# FIXME: Disabling zlib-devel dep as we are applying the xorg-x11-server-1.1.0-no-zlib.patch
# patch which should remove any dependency on zlib anyway.
#BuildRequires: zlib-devel

# FIXME: libXt-devel should be wrapped in with_dmx_server - for Xdmxconfig,
# probably should only be needed for DMX builds, but the build explodes with
# a bogus configure check failure if this is missing.
BuildRequires: libXt-devel


%if %{with_dmx_server}
# libdmx-devel needed for Xdmx
BuildRequires: libdmx-devel
# libXmu-devel needed for Xdmx
BuildRequires: libXmu-devel
# libXrender-devel needed for Xdmx
BuildRequires: libXrender-devel
# libXi-devel needed for Xdmx
BuildRequires: libXi-devel
BuildRequires: libXpm-devel
BuildRequires: libXaw-devel
%endif

# To query fontdir from fontutil.pc
BuildRequires: xorg-x11-font-utils >= 1.0.0-1
# Needed at least for DRI enabled builds
%if %{with_dri}
BuildRequires: mesa-libGL-devel >= 6.5-1
BuildRequires: mesa-source >= 6.5-19
BuildRequires: libdrm-devel >= 2.0-1
%endif

BuildRequires: libselinux-devel

%description
X.Org X11 X server

# ----- Xorg --------------------------------------------------------
%if %{with_hw_servers}
%package Xorg
Summary: Xorg X server
Group: User Interface/X
# NOTE: The X server invokes xkbcomp directly, so this is required.
Requires: xkbcomp
# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base
# NOTE: Require some basic drivers for minimal configuration. (#173060)
# We _should_ install every driver, but OLPC wants different (#191781),
# which is quite lame and wants an better solution.
Requires: xorg-x11-drv-mouse xorg-x11-drv-keyboard xorg-x11-drv-vesa
Requires: xorg-x11-drv-void xorg-x11-drv-evdev
#Requires: xorg-x11-drivers >= 0.99.2-4

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
%endif

# ----- Xnest -------------------------------------------------------
%package Xnest
Summary: A nested server.
Group: User Interface/X
Obsoletes: XFree86-Xnest, xorg-x11-Xnest
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xnest X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xnest

# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base

%description Xnest
Xnest is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.

# ----- Xdmx --------------------------------------------------------
%if %{with_dmx_server}
%package Xdmx
Summary: Distributed Multihead X Server and utilities
Group: User Interface/X
Obsoletes: xorg-x11-Xdmx
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xdmx X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xdmx

# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base

%description Xdmx
Xdmx is proxy X server that provides multi-head support for multiple displays
attached to different machines (each of which is running a typical X server).
When Xinerama is used with Xdmx, the multiple displays on multiple machines
are presented to the user as a single unified screen.  A simple application
for Xdmx would be to provide multi-head support using two desktop machines,
each of which has a single display device attached to it.  A complex
application for Xdmx would be to unify a 4 by 4 grid of 1280x1024 displays
(each attached to one of 16 computers) into a unified 5120x4096 display.
%endif
# ----- Xvfb --------------------------------------------------------

%package Xvfb
Summary: A X Windows System virtual framebuffer X server.
Group: User Interface/X
Obsoletes: XFree86-Xvfb xorg-x11-Xvfb
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xvfb X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xvfb

# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base

%description Xvfb
Xvfb (X Virtual Frame Buffer) is an X server that is able to run on
machines with no display hardware and no physical input devices.
Xvfb simulates a dumb framebuffer using virtual memory.  Xvfb does
not open any devices, but behaves otherwise as an X display.  Xvfb
is normally used for testing servers.

# ----- Xephyr -------------------------------------------------------

%package Xephyr
Summary: A nested server.
Group: User Interface/X
# NOTE: This virtual provide should be used by packages which want to depend
# on an implementation nonspecific Xephyr X server.  It is intentionally not
# versioned, since it should be agnostic.
Provides: Xephyr

# NOTE: The X server requires 'fixed' and 'cursor' font, which are provided
# by xorg-x11-fonts-base
Requires: xorg-x11-fonts-base

%description Xephyr
Xephyr is an X server, which has been implemented as an ordinary
X application.  It runs in a window just like other X applications,
but it is an X server itself in which you can run other software.  It
is a very useful tool for developers who wish to test their
applications without running them on their real X server.  Unlike
Xnest, Xephyr renders to an X image rather than relaying the
X protocol, and therefore supports the newer X extensions like
Render and Composite.

# ----- sdk ---------------------------------------------------------
%if %{with_hw_servers}
%package sdk
Summary: SDK for X server driver module development
Group: User Interface/X
Obsoletes: XFree86-sdk xorg-x11-sdk
Requires: xorg-x11-util-macros
Requires: xorg-x11-proto-devel

Requires(pre): xorg-x11-filesystem >= 0.99.2-3

Provides: libxf86config-devel = %{version}-%{release}

%description sdk
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.
%endif
# -------------------------------------------------------------------

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p0 -b .init-origins-fix
%patch3 -p0 -b .parser-add-missing-headers-to-sdk
%patch5 -p0 -b .libxf86config-dont-write-empty-sections

%patch100 -p0 -b .no-move-damage
%patch101 -p0 -b .dont-backfill-bg-none
%patch102 -p0 -b .gl-include-inferiors
%patch103 -p0 -b .tfp-damage
%patch104 -p0 -b .mesa-copy-sub-buffer
%patch105 -p0 -b .enable-composite
%patch106 -p1 -b .no-xnest-composite

%patch1000 -p0 -b .redhat-die-ugly-pattern-die-die-die
%patch1001 -p0 -b .Red-Hat-extramodes
%patch1002 -p1 -b .xephyr
%patch1003 -p1 -b .fpic
%patch1004 -p1 -b .selinux-awareness

%patch2001 -p1 -b .pci-scan
%patch2004 -p1 -b .zlib
%patch2005 -p1 -b .Xdmx

%patch3001 -p1 -b .edid1
%patch3002 -p1 -b .edid2
%patch3003 -p1 -b .cvt
%patch3004 -p1 -b .targetrefresh
%patch3005 -p1 -b .getconfig-pl-die-die-die
%patch3006 -p1 -b .dpms-on-by-default
%patch3007 -p1 -b .edid-on-root-window
%patch3008 -p1 -b .sanedefaultmode
%patch3009 -p1 -b .module-list

%build
#FONTDIR="${datadir}/X11/fonts"
#DEFAULT_FONT_PATH="${FONTDIR}/misc:unscaled,${FONTDIR}/TTF/,${FONTDIR}/OTF,${FONTDIR}/Type1/,${FONTDIR}/CID/,${FONTDIR}/100dpi:unscaled,${FONTDIR}/75dpi:unscaled"

#	--disable-dependency-tracking \
# also, --enable-kdrive just for Xephyr is overkill, should fix that upstream

aclocal ; automake ; autoconf
%configure %{xservers} \
	--disable-xprint \
	--disable-static \
	--with-pic \
	--enable-composite \
	--enable-xtrap \
	--enable-xcsecurity \
	--enable-xevie \
	--with-default-font-path="unix/:7100" \
	--with-module-dir=%{moduledir} \
	--with-os-name="Fedora Core 5" \
	--with-os-vendor="Red Hat, Inc." \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
	--with-rgb-path=%{_datadir}/X11/rgb \
	--disable-xorgcfg \
	--enable-install-libxf86config \
	--with-fontdir=%(pkg-config --variable=fontdir fontutil) \
%if %{with_dri}
	--enable-dri \
	--with-mesa-source=%{_datadir}/mesa/source \
	--with-dri-driver-path=%{drimoduledir} \
%else
	--disable-dri \
%endif

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT moduledir=%{moduledir}


%if %{with_hw_servers}
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
%endif

# FIXME: Remove unwanted files/dirs
{
    rm -f $RPM_BUILD_ROOT%{_bindir}/xorgconfig
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xorgconfig.1*
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/Cards
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/Options
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/cfg.sample
    rm -f $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/xorg.cfg
    rm -f $RPM_BUILD_ROOT%{_bindir}/getconfig
    rm -f $RPM_BUILD_ROOT%{_bindir}/getconfig.pl
%if ! %{with_developer_utils}
    rm -f $RPM_BUILD_ROOT%{_bindir}/inb
    rm -f $RPM_BUILD_ROOT%{_bindir}/inl
    rm -f $RPM_BUILD_ROOT%{_bindir}/inw
    rm -f $RPM_BUILD_ROOT%{_bindir}/ioport
    rm -f $RPM_BUILD_ROOT%{_bindir}/outb
    rm -f $RPM_BUILD_ROOT%{_bindir}/outl
    rm -f $RPM_BUILD_ROOT%{_bindir}/outw
    rm -f $RPM_BUILD_ROOT%{_bindir}/pcitweak
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/pcitweak.1*
%endif
    rm -f $RPM_BUILD_ROOT%{_mandir}/man1/getconfig.1x*
    rm -f $RPM_BUILD_ROOT%{_mandir}/man5/getconfig.5x*
    # Remove all libtool archives (*.la)
    find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

%ifarch s390 s390x
    # FIXME: The following files get installed on s390/s390x and we don't
    # want some of them on s390 at all, and others should be in a -common
    # subpackage, but it's not worth doing that for 3 files right now.
#    error: Installed (but unpackaged) file(s) found:
#	   /randrstr.h
#	   /usr/lib/pkgconfig/xorg-server.pc
#	      /usr/lib/xserver/SecurityPolicy
#	      /usr/share/aclocal/xorg-server.m4
#	      /usr/share/man/man1/Xserver.1x.gz
#	      /var/lib/xkb/README.compiled
    rm -f $RPM_BUILD_ROOT/randrstr.h
    rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
    rm -rf $RPM_BUILD_ROOT%{_libdir}/xserver
    rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal
    rm -rf $RPM_BUILD_ROOT/var/lib/xkb
#    rm -f $RPM_BUILD_ROOT%{_datadir}/man/man1/Xserver.1x*
%endif
}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_hw_servers}
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
%endif

# ----- Xorg --------------------------------------------------------

%if %{with_hw_servers}
%files Xorg
%defattr(-,root,root,-)
# FIXME: The build fails to find the Changelog for some reason.
#%doc ChangeLog
%{_bindir}/X
%attr(4711, root, root) %{_bindir}/Xorg
%{_bindir}/gtf
%{_bindir}/cvt
%if %{with_developer_utils}
%{_bindir}/inb
%{_bindir}/inl
%{_bindir}/inw
%{_bindir}/ioport
%{_bindir}/outb
%{_bindir}/outl
%{_bindir}/outw
%{_bindir}/pcitweak
%endif
%{_bindir}/scanpci
%dir %{_datadir}/xorg
%{_datadir}/xorg/vesamodes
%{_datadir}/xorg/extramodes
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%if %{with_dri}
%{_libdir}/xorg/modules/extensions/libGLcore.so
%{_libdir}/xorg/modules/extensions/libdri.so
%{_libdir}/xorg/modules/extensions/libglx.so
%endif
%{_libdir}/xorg/modules/extensions/libdbe.so
%{_libdir}/xorg/modules/extensions/libextmod.so
%{_libdir}/xorg/modules/extensions/librecord.so
%{_libdir}/xorg/modules/extensions/libxtrap.so
%dir %{_libdir}/xorg/modules/input
%dir %{_libdir}/xorg/modules/fonts
%{_libdir}/xorg/modules/fonts/libbitmap.so
%{_libdir}/xorg/modules/fonts/libfreetype.so
%{_libdir}/xorg/modules/fonts/libtype1.so
%dir %{_libdir}/xorg/modules/linux
%if %{with_dri}
%{_libdir}/xorg/modules/linux/libdrm.so
%endif
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
%if %{with_developer_utils}
%{_mandir}/man1/pcitweak.1x*
%endif
%{_mandir}/man1/gtf.1x*
%{_mandir}/man1/scanpci.1x*
%{_mandir}/man1/Xorg.1x*
%{_mandir}/man1/Xserver.1x*
%{_mandir}/man1/cvt.1*
#%dir %{_mandir}/man4x
#%{_mandir}/man4/fbdevhw.4x*
%{_mandir}/man4/fbdevhw.4*
#%dir %{_mandir}/man5x
%{_mandir}/man5/xorg.conf.5x*
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled
%endif

# ----- Xnest -------------------------------------------------------

%files Xnest
%defattr(-,root,root,-)
%{_bindir}/Xnest
#%dir %{_mandir}/man1x
%{_mandir}/man1/Xnest.1x*
# NOTE: Xserver.1x intentionally present in multiple subpackages
%{_mandir}/man1/Xserver.1x*

# ----- Xdmx --------------------------------------------------------

%if %{with_dmx_server}
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
# NOTE: Xserver.1x intentionally present in multiple subpackages
%{_mandir}/man1/Xserver.1x*
%endif

# ----- Xvfb --------------------------------------------------------

%files Xvfb
%defattr(-,root,root,-)
%{_bindir}/Xvfb
#%dir %{_mandir}/man1x
%{_mandir}/man1/Xvfb.1x*
# NOTE: Xserver.1x intentionally present in multiple subpackages
%{_mandir}/man1/Xserver.1x*

# ----- Xephyr -------------------------------------------------------

%files Xephyr
%defattr(-,root,root,-)
%{_bindir}/Xephyr
# no manpage yet
#%dir %{_mandir}/man1x
#%{_mandir}/man1/Xephyr.1x*
# NOTE: Xserver.1x intentionally present in multiple subpackages
%{_mandir}/man1/Xserver.1x*

# ----- sdk ---------------------------------------------------------
%if %{with_hw_servers}
%files sdk
%defattr(-,root,root,-)
%{_libdir}/libxf86config.a
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}/xorg
#%dir %{_includedir}/xorg/sdk
%{sdkdir}/*.h
%{_datadir}/aclocal/xorg-server.m4
%endif
# -------------------------------------------------------------------

%changelog
* Wed Jul 26 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-12.fc6
- Added "1920x1080" CVT modes to Red-Hat-extramodes patch for (#195272)
- Sorted the extramodes file by X res, then Y res for ease of maintenance.

* Tue Jul 25 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-11.fc6
- Add selinux{,-devel} buildreqs.

* Tue Jul 25 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-10.fc6
- xorg-x11-server-1.1.1-selinux-awareness.patch: Added for new Mesa
  selinux code.
- xorg-x11-server-1.1.1-Xdmx-render-fix-fdo7482.patch: Backport a Render
  fix for Xdmx.
- xorg-x11-server-1.1.1-no-composite-in-xnest.patch: Disable Composite in
  Xnest, as it's known not to work.
- Fix default font path to match the config file we used to generate.
- Fix default module set to match the config file we used to generate.
- Disable use of TLS GLX dispatch to match Mesa selinux nonsense.

* Mon Jul 24 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-8.fc6
- Added "1440x900@60" CVT mode to Red-Hat-extramodes patch for (#179865)

* Fri Jul 21 2006 Mike A. Harris <mharris@redhat.com>
- Added "1152x864 @ 100.00" GTF mode to Red-Hat-extramodes patch (#49264)

* Fri Jul 21 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-7.fc6
- Only ship pcitweak manpage if we are building it (#199653)
- Fix dist tag usage (Was {dist}, should be {?dist})
- Added xorg-x11-server-libxf86config-dont-write-empty-sections.patch to
  prevent config file parser/writer from writing out empty sections (#198653)
- Add dependency on xorg-x11-fonts-base to all X server subpackages (#186091)

* Tue Jul 18 2006 Jeremy Katz <katzj@redhat.com> 1.1.1-6.fc6
- Saner defaults for hsync/vrefresh on monitors that can't be probed

* Thu Jul 13 2006 Kristian Høgsberg <krh@redhat.com>  1.1.1-5.fc6
- Tag as 1.1.1-5.fc6.

* Wed Jul 12 2006 Kristian Høgsberg <krh@redhat.com>  1.1.1-5.fc5.aiglx
- Enable composite by default.
- Split spiffiffity patch into one patch per change:
  xorg-x11-server-1.1.0-no-move-damage.patch and
  xorg-x11-server-1.1.0-dont-backfill-bg-none.patch.

* Wed Jul 12 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-4.fc6
- Restore placing the raw EDID block on the root window.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.1-3.1.fc6
- rebuild

* Tue Jul 11 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-3.fc6
- Enable DPMS by default.

* Tue Jul 11 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-2.fc6
- Remove nonsensical runtime perl dependency.

* Sat Jul 08 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1.fc6
- Update to 1.1.1.

* Sat Jul 08 2006 Kristian Høgsberg <krh@redhat.com>  1.1.0-27.fc6
- Enable TLS for GLX to match the mesa build config.

* Fri Jul 07 2006 Kristian Høgsberg <krh@redhat.com>  1.1.0-26
- Add xorg-x11-server-1.1.0-mesa-copy-sub-buffer.patch to hook up the
  GLX_MESA_copy_sub_buffer extension.

* Fri Jun 30 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-25.fc6
- Start using the new %%{dist} tag <http://fedoraproject.org/wiki/DistTag>
  experimentally in the package Release field to help prevent problems like
  (#197266) from occuring in the future.

* Wed Jun 28 2006 Mike A. Harris <mharris@redhat.com>
- Disable build dependency on zlib-devel now that we are not uselessly linking
  against it.

* Tue Jun 27 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-24
- Don't (uselessly) link the server against zlib.
- Fix the 1680x1050 modes to be the CVT timings instead of GTF.

* Mon Jun 26 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-23
- Fix an open-coded check for reduced-blanking modes to only apply to analog
  connectors.
- Reorder the EDID patches slightly.

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-22
- Added xorg-xserver-1.1.0-setuid.diff to fix potential security issue (#196094)
- Disable DRI on ppc64 builds.
- Conditionalize inclusion of DRI related X server modules to with_dri builds.

* Tue Jun 20 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-21
- Update xorg-x11-server-1.1.0-tfp-damage.patch to use glTexSubImage2D
  to only update the part of the texture that changed, based on damage
  regions.

* Mon Jun 19 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-20
- Remove with_xnest_server conditional, and fix more BuildRequires to pull
  in libX11-devel, libXext-devel, zlib-devel, etc. for Xnest and Xephyr.
- Remove unwanted files leftover in buildroot for s390/s390x builds.
- Add Xserver.1x manpage to multiple subpackages, as it applies equally to
  Xorg, Xnest, Xvfb, Xephyr.

* Mon Jun 19 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-19
- Add with_xnest_server conditional and disable on s390, since Xnest
  fails to build on there (Xlib doesn't get added to the link line).
- Add -f to removal of xorgconfig and others which may or may not be built.

* Mon Jun 19 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-18
- Add xorg-x11-server-1.1.0-convolution-filter-fix.patch and
  xorg-x11-server-1.1.0-tfp-damage.patch backported to make compiz go
  faster and make compiz shadows work.

* Mon Jun 19 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-17
- Disable filling in monitor gamma info from EDID momentarily, since drivers
  will use that field to set the card's gamma ramp.
- Backport some stuff from git: cw crash fix, faster pci scanning, some
  log message cleanup.

* Fri Jun 16 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-16
- Enable spec support for s390, s390x, alpha, sparc, and sparc64 architectures.
- Add with_hw_servers conditional to disable hardware servers on s390/s390x.
- Add with_dmx_server to disable DMX on s390/s390x.
- Added "release" number to "BuildRequires: freetype-devel >= 2.1.9-1" for
  dependency futureproofing.
- Force "--disable-dri" on s390/s390x, to attempt to work around ./configure
  failure to find libdrm, which should not be needed on s390 builds anyway.

* Thu Jun 15 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-15
- Add loader infrastructure for publishing PCI ID lists in the drivers, and
  autodetecting drivers based on that.  Currently unused since no drivers
  publish such a list yet.
- Fix mouse autoconfig to use /dev/input/mice instead of /dev/mouse.

* Wed Jun 14 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-14
- Change selection atom to _COMPIZ_GL_INCLUDE_INFERIORS in
  xorg-x11-server-1.1.0-gl-include-inferiors.patch.

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> 1.1.0-13
- put back my -fPIC patch, libxf86config isn't built with fPIC otherwise

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-12
- Add EDID mode autodetection.

* Mon Jun 12 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-11
- Add xorg-x11-server-1.1.0-gl-include-inferiors.patch to let GL
  rendering include child windows.

* Mon Jun 12 2006 Adam Jackson <ajax@redhat.com> 1.1.0-10
- Misc build fixes for ppc64.

* Mon Jun 12 2006 Adam Jackson <ajax@redhat.com> 1.1.0-9
- --enable-xorg on ppc64 too.
- Re-add cvt, got dropped somehow.

* Fri Jun 09 2006 Kristian Høgsberg <krh@redhat.com> 1.1.0-8
- Add our friend, libtool, to BuildRequires.

* Thu Jun 08 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-7
- Change "BuildRequires: freetype-devel >= 2.1.10" to 2.1.9, as Xorg 7.0
  contains 2.1.9 in "extras" and 7.1 does not appear to have a requirement on
  a newer freetype.
- Janitorial cleanups for spec file changelog consistency.
- Call aclocal before automake, otherwise automake >= 1.9.6 is required in
  order to rebuild the package.
- Build 1.1.0-4, 1.1.0-5, and 1.1.0-6 appear to have failed in brew but nobody
  fixed them.  It appears automake 1.9 breaks the build.

* Wed Jun 07 2006 Jeremy Katz <katzj@redhat.com> 1.1.0-6
- BR automake and autoconf

* Wed Jun 07 2006 Jeremy Katz <katzj@redhat.com> 1.1.0-5
- build on ppc64 so that we have an X server there

* Tue Jun 06 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-4
- Hack the kdrive makefile to only attempt to build Xephyr, avoids linking
  sixteen extra servers just to delete them.
- Move cvt to the default install set, same as gtf.

* Mon Jun 05 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-3
- Drop the libxf86config -fPIC patch, just build the whole thing with
  --with-pic instead.  Add void and evdev to the required driver list for
  upcoming autoconfig magic.

* Thu May 25 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-2
- Add "Requires: xorg-x11-proto-devel >= 7.1-1" to sdk for numerous (52) bug
  reports of drivers failing to build with mock.

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Xorg 7.1 final.

* Tue May 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.99.903-2
- Disable dependency on xorg-x11-drivers package, for OLPC.  (#191781)
- Add "BuildRequires: freetype-devel >= 2.1.10" for bug (#192021)

* Fri May 12 2006 Adam Jackson <ajackson@redhat.com> 1.0.99.903-1
- Update to 7.1RC3, plus experimental fix for fdo bug #6827.

* Mon May 01 2006 Adam Jackson <ajackson@redhat.com> 1.0.99.902-1
- Update to 7.1RC2 plus fix for CVE 2006-1526.  Disable the fastpathing
  patch for fdo bug #4320 since that should be covered in the generic
  Render code now.

* Mon Apr 24 2006 Adam Jackson <ajackson@redhat.com> 1.0.99.901-6
- Backport a Render crash fix from HEAD.

* Thu Apr 13 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.901-5
- Update spiffiffity patch to only suppress move damage events for
  manually redirected windows.

* Wed Apr 12 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.901-4
- Bump for rawhide build.

* Wed Apr 12 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.901-3
- Add xorg-x11-server-1.0.99.901-cow-fix.patch to fix crash when
  releasing the COW.

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.901-2
- Bump for fc5 build.

* Sat Apr 08 2006 Adam Jackson <ajackson@redhat.com> 1.0.99.901-1
- Update to 7.1 RC1.

* Thu Apr 06 2006 Adam Jackson <ajax@redhat.com> 1.0.99.2-2
- Remove LBX to match upstream policy.
- Add Xephyr server.

* Tue Apr 04 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.2-1
- Update to 1.0.99.2 snapshot and go back to using mesa-source package.
- Drop xorg-server-1.0.99-composite-visibility.patch.
- Drop xorg-server-1.0.1-backtrace.patch.
- Drop xorg-server-0.99.3-rgb.txt-dix-config-fix.patch.
- Add xorg-server-1.0.99.2-spiffiffity.patch.

* Thu Mar 23 2006 Kristian Høgsberg <krh@redhat.com>
- Pass --with-dri-driver-path so we're sure to point it to the right path.

* Wed Mar 22 2006 Soren Sandmann <sandmann@redhat.com> 1.0.99.1-2
- Add xorg-server-1.0.99-composite-visibility.patch to get rid of flashing
  titlebars in compositing metacity.

* Tue Mar 21 2006 Kristian Høgsberg <krh@redhat.com> 1.0.99.1-1
- Update to 1.0.99.1 snapshot.

* Mon Mar 06 2006 Jeremy Katz <katzj@redhat.com> 1.0.1-8
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

* Wed Feb 08 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-6
- Added xorg-x11-server-1.0.1-Red-Hat-extramodes.patch which is a merger of
  XFree86-4.2.99.2-redhat-custom-modelines.patch and
  xorg-x11-6.8.2-laptop-modes.patch from FC4 for (#180301)
- Install a copy of the vesamodes and extramodes files which contain the list
  of video modes that are built into the X server, so that the "rhpxl" package
  does not have to carry around an out of sync copy for itself. (#180301)

* Tue Feb 07 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-5
- Updated "BuildRequires: mesa-source >= 6.4.2-2" to get fix for (#176976)

* Mon Feb 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4
- Fix brown paper bag error introduced in rpm post script in 1.0.1-4.

* Mon Feb 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added xorg-x11-server-1.0.1-composite-fastpath-fdo4320.patch with changes
  suggested by ajax to fix (fdo#4320).
- Cosmetic cleanups to satiate the banshees.

* Sun Feb 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
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

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added "BuildRequires: libXtst-devel" for Xtst examples.

* Mon Nov 07 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
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

* Mon Oct 03 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2.cvs20050830.2
- Fix license tag to be "MIT/X11"
- Change Xdmx subpackage to Obsolete xorg-x11-Xdmx instead of xorg-x11-Xnest

* Sun Oct 02 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2.cvs20050830.1
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

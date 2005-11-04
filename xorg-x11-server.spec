%define tarball xorg-server
%define cvsdate xxxxxxxxxxx

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   0.99.2
Release:   1
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/X11R7.0-RC1/everything/%{tarball}-%{version}.tar.bz2
#ource0:   %{tarball}-%{version}-%{cvsdate}.tar.bz2
License:   MIT/X11
Group:     User Interface/X
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# INFO: We don't ship the X server on s390/s390x/ppc64
ExcludeArch: s390 s390x ppc64

%define moduledir %{_libdir}/xorg/modules
%define sdkdir %{_includedir}/xorg
%define xservers --enable-xorg --enable-dmx --enable-xvfb --enable-xnest

# NOTE: The developer utils are intended for low level video driver hackers,
# doing low level bit twiddling, who really know what they are doing, and are
# disabled by default, as they are not generally useful to end users.
%define with_developer_utils	0

%ifarch %{ix86} x86_64 ia64 ppc
%define with_dri	1
%else
%define with_dri	0
%endif

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros >= 0.99.1
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libXfont-devel
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
# libfontenc-devel needed for Xorg, but not specified by
# upstream deps.  Build fails without it.
BuildRequires: libfontenc-devel
# Needed at least for DRI enabled builds
%if %{with_dri}
BuildRequires: mesa-source >= 6.4-4
%endif
%description
X.Org X11 X server

# ----- Xorg --------------------------------------------------------

%package Xorg
Summary: Xorg X server
Group: User Interface/X
Obsoletes: XFree86 xorg-x11
Provides: Xorg

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
Obsoletes: XFree86-Xnest xorg-x11-Xnest
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
#Requires: %{name} = %{version}-%{release}
Obsoletes: XFree86-Xvfb xorg-x11-Xvfb
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

%description sdk
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.

# -------------------------------------------------------------------

%prep
%setup -q -n %{tarball}-%{version}

%build
# FIXME: Using ./configure directly to see if it works around a problem during
# %%insall when %%configure is used and "make install DESTDIR" is used
%configure %{xservers} \
	--disable-dependency-tracking \
	--disable-xprint \
	--disable-static \
	--enable-composite \
	--enable-xtrap \
	--enable-xcsecurity \
	--enable-xevie \
	--enable-lbx \
%if %{with_dri}
	--enable-dri \
	--with-mesa-source=%{_datadir}/mesa/source \
%endif
	--with-module-dir=%{moduledir} \
	--with-os-name="Fedora Core 5" \
	--with-os-vendor="Red Hat, Inc." \
	--with-xkb-output=%{_localstatedir}/lib/xkb \
	--disable-xorgcfg

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
#makeinstall moduledir=$RPM_BUILD_ROOT%{moduledir} sdkdir=$RPM_BUILD_ROOT%{sdkdir}
# DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT moduledir=%{moduledir} sdkdir=%{sdkdir}

# Remove all libtool archives (*.la) from modules directory, as we do not
# ship these.
#find $RPM_BUILD_ROOT%{_libdir}/xorg/modules -type f -name '*.la' | xargs rm -f -- || :
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :

# Make these directories now so the Xorg package can own them.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

# FIXME: Remove unwanted files/dirs
{
    rm $RPM_BUILD_ROOT%{_bindir}/xorgconfig
    rm $RPM_BUILD_ROOT%{_mandir}/man1/xorgconfig.1*
    rm $RPM_BUILD_ROOT%{_libdir}/X11/Cards
    rm $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/cfg.sample
    rm $RPM_BUILD_ROOT%{_libdir}/X11/getconfig/xorg.cfg
}

# FIXME: Move/rename manpages to correct location
{
    mv $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/man1x
    for each in $RPM_BUILD_ROOT%{_mandir}/man1x/* ; do
        mv $each ${each/.1/.1x}
    done
}


%clean
rm -rf $RPM_BUILD_ROOT


# ----- Xorg --------------------------------------------------------

%files Xorg
%defattr(-,root,root,-)
# FIXME: The build fails to find the Changelog for some reason.
#%doc ChangeLog
%dir %{_bindir}
%{_bindir}/Xorg
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
%endif
%{_bindir}/scanpci
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/extensions
%{_libdir}/xorg/modules/extensions/libdri.so
%dir %{_libdir}/xorg/modules/input
%dir %{_libdir}/xorg/modules/linux
%{_libdir}/xorg/modules/linux/libdrm.so
%dir %{_libdir}/xorg/modules/multimedia
%{_libdir}/xorg/modules/multimedia/bt829_drv.so
%{_libdir}/xorg/modules/multimedia/fi1236_drv.so
%{_libdir}/xorg/modules/multimedia/libi2c.so
%{_libdir}/xorg/modules/multimedia/msp3430_drv.so
%{_libdir}/xorg/modules/multimedia/tda8425_drv.so
%{_libdir}/xorg/modules/multimedia/tda9850_drv.so
%{_libdir}/xorg/modules/multimedia/tda9885_drv.so
%{_libdir}/xorg/modules/multimedia/uda1380_drv.so
%{_libdir}/xorg/modules/libGLcore.so
%{_libdir}/xorg/modules/libafb.so
%{_libdir}/xorg/modules/libbitmap.so
%{_libdir}/xorg/modules/libcfb.so
%{_libdir}/xorg/modules/libcfb16.so
%{_libdir}/xorg/modules/libcfb24.so
%{_libdir}/xorg/modules/libcfb32.so
%{_libdir}/xorg/modules/libdbe.so
%{_libdir}/xorg/modules/libddc.so
%{_libdir}/xorg/modules/libexa.so
%{_libdir}/xorg/modules/libextmod.so
%{_libdir}/xorg/modules/libfb.so
%{_libdir}/xorg/modules/libfbdevhw.so
%{_libdir}/xorg/modules/libfreetype.so
%{_libdir}/xorg/modules/libglx.so
%{_libdir}/xorg/modules/libint10.so
%{_libdir}/xorg/modules/liblayer.so
%{_libdir}/xorg/modules/libmfb.so
%{_libdir}/xorg/modules/libpcidata.so
%{_libdir}/xorg/modules/librac.so
%{_libdir}/xorg/modules/libramdac.so
%{_libdir}/xorg/modules/librecord.so
%{_libdir}/xorg/modules/libscanpci.so
%{_libdir}/xorg/modules/libshadow.so
%{_libdir}/xorg/modules/libshadowfb.so
%{_libdir}/xorg/modules/libtype1.so
%{_libdir}/xorg/modules/libvbe.so
%{_libdir}/xorg/modules/libvgahw.so
%{_libdir}/xorg/modules/libxaa.so
%{_libdir}/xorg/modules/libxf1bpp.so
%{_libdir}/xorg/modules/libxf4bpp.so
%{_libdir}/xorg/modules/libxf8_16bpp.so
%{_libdir}/xorg/modules/libxf8_32bpp.so
%{_libdir}/xorg/modules/libxf8_32wid.so
%dir %{_mandir}
%dir %{_mandir}/man1x
%{_mandir}/man1x/getconfig.1x*
%{_mandir}/man1x/gtf.1x*
%{_mandir}/man1x/pcitweak.1x*
%{_mandir}/man1x/scanpci.1x*
%{_mandir}/man1x/Xorg.1x*
%{_mandir}/man1x/Xserver.1x*
%dir %{_mandir}/man4x
%{_mandir}/man4x/fbdevhw.4x*
%dir %{_mandir}/man5x
%{_mandir}/man5x/getconfig.5x*
%{_mandir}/man5x/xorg.conf.5x*
%dir %{_localstatedir}/lib/xkb
%{_localstatedir}/lib/xkb/README.compiled

# ----- Xnest -------------------------------------------------------

%files Xnest
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/Xnest
%dir %{_mandir}
%dir %{_mandir}/man1x
%{_mandir}/man1x/Xnest.1x*

# ----- Xdmx --------------------------------------------------------

%files Xdmx
%defattr(-,root,root,-)
%dir %{_bindir}
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
%dir %{_mandir}
%dir %{_mandir}/man1x
%{_mandir}/man1x/Xdmx.1x*
%{_mandir}/man1x/dmxtodmx.1x*
%{_mandir}/man1x/vdltodmx.1x*
%{_mandir}/man1x/xdmxconfig.1x*

# ----- Xvfb --------------------------------------------------------

%files Xvfb
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/Xvfb
%dir %{_mandir}
%dir %{_mandir}/man1x
%{_mandir}/man1x/Xvfb.1x*

# ----- sdk ---------------------------------------------------------

%files sdk
%defattr(-,root,root,-)
%dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/xorg-server.pc
%dir %{_includedir}
%dir %{_includedir}/xorg
%{_includedir}/xorg/*.h

# -------------------------------------------------------------------

%changelog
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
- Added "BuildRequires: libdmx-devel" for dmx utilities et al.

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

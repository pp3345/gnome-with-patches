%define tarball xorg-server
%define moduledir %{_libdir}/xorg/modules
%define sdkdir %{_includedir}/xorg

%define cvsdate cvs20050830

Summary:   X.Org X11 X server
Name:      xorg-x11-server
Version:   0.99.1
Release:   2.%{cvsdate}.1
URL:       http://www.x.org
#Source0:   http://xorg.freedesktop.org/X11R7.0-RC0/everything/%{tarball}-%{version}.tar.bz2
Source0:   %{tarball}-%{version}-%{cvsdate}.tar.bz2
License:   MIT/MIT
Group:     User Interface/X
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# INFO: We don't ship the X server on s390/s390x/ppc64
Excludearch: s390 s390x ppc64

%define xservers --enable-xorg --enable-dmx --enable-xvfb --enable-xnest

BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel
BuildRequires: libXfont-devel
BuildRequires: libXau-devel
BuildRequires: libxkbfile-devel
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
BuildRequires: pkgconfig

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
Requires: %{name} = %{version}-%{release}
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
Requires: %{name}-Xorg = %{version}-%{release}
Obsoletes: xorg-x11-Xnest
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
Requires: %{name} = %{version}-%{release}
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
Provides: xorg-x11-server-sdk = 7.0.0

%description sdk
The SDK package provides the developmental files which are necessary for
developing X server driver modules, and for compiling driver modules
outside of the standard X11 source code tree.  Developers writing video
drivers, input drivers, or other X modules should install this package.

# -------------------------------------------------------------------

%prep
%setup -q -n %{tarball}-%{version}-%{cvsdate}

%build
%configure %{xservers} \
	--enable-composite \
	--disable-xprint \
	--disable-static \
	--with-module-dir=%{moduledir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall moduledir=$RPM_BUILD_ROOT%{moduledir} sdkdir=$RPM_BUILD_ROOT%{sdkdir}

# Remove all libtool archives (*.la) from modules directory, as we do not
# ship these.
find $RPM_BUILD_ROOT%{_libdir}/xorg/modules -name '*.la'| xargs rm

# Make these directories now so the Xorg package can own them.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,input}

%clean
rm -rf $RPM_BUILD_ROOT

# FIXME: where did the man pages go?

# ----- Xorg --------------------------------------------------------

%files Xorg
%defattr(-,root,root,-)
# FIXME: The build fails to find the Changelog for some reason.
#%doc ChangeLog
%dir %{_bindir}
%{_bindir}/Xorg
%dir %{_libdir}/xorg
%dir %{_libdir}/xorg/modules
%dir %{_libdir}/xorg/modules/drivers
%dir %{_libdir}/xorg/modules/input
%{_libdir}/xorg/modules/*.so

# ----- Xnest -------------------------------------------------------

%files Xnest
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/Xnest

# ----- Xdmx --------------------------------------------------------

# FIXME: dmx tools? (dmxtodmx, vdltodmx, xdmxconfig)

%files Xdmx
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/Xdmx

# ----- Xvfb --------------------------------------------------------

%files Xvfb
%defattr(-,root,root,-)
%dir %{_bindir}
%{_bindir}/Xvfb

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

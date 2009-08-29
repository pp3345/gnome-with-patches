Name:           mutter
Version:        2.27.3
Release:        3%{?dist}
Summary:        Window and compositing manager based on Clutter

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://git.gnome.org/cgit/mutter
Source0:        ftp://ftp.gnome.org/pub/gnome/sources/%{name}/2.27/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Workaround for glibc bug https://bugzilla.redhat.com/show_bug.cgi?id=520209
Patch0: mutter-math-workaround.patch

BuildRequires: clutter-devel
BuildRequires: pango-devel
BuildRequires: startup-notification-devel
BuildRequires: gtk2-devel
BuildRequires: pkgconfig
BuildRequires: GConf2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gir-repository-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcursor-devel
BuildRequires: libXcomposite-devel
BuildRequires: zenity
BuildRequires: intltool
BuildRequires: gnome-doc-utils
BuildRequires: desktop-file-utils

Requires: control-center-filesystem
Requires: startup-notification
Requires: GConf2
Requires: dbus-x11
Requires: zenity

%description
Mutter is a window and compositing manager that displays and manages
your desktop via OpenGL. Mutter combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Mutter can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as gnome-shell or
Moblin. For this reason, Mutter is very extensible via plugins, which
are used both to add fancy visual effects and to rework the window
management behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk-doc

%description devel
Header files and libraries for developing Mutter plugins. Also includes
utilities for testing Metacity/Mutter themes.

%prep
%setup -q
%patch0 -p1 -b .math-workaround

%build
%configure --with-clutter --disable-static

SHOULD_HAVE_DEFINED="HAVE_SM HAVE_XINERAMA HAVE_XFREE_XINERAMA HAVE_SHAPE HAVE_RANDR HAVE_STARTUP_NOTIFICATION HAVE_COMPOSITE_EXTENSION"

for I in $SHOULD_HAVE_DEFINED; do
  if ! grep -q "define $I" config.h; then
    echo "$I was not defined in config.h"
    grep "$I" config.h
    exit 1
  else
    echo "$I was defined as it should have been"
    grep "$I" config.h
  fi
done

make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#Remove libtool archives.
rm -rf %{buildroot}/%{_libdir}/*.la

%find_lang %{name}

# Mutter contains a .desktop file so we just need to validate it
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%pre 
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/mutter.schemas \
    > /dev/null || :
fi

%preun 
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
    %{_sysconfdir}/gconf/schemas/mutter.schemas \
    > /dev/null || :
fi

%post 
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
    %{_sysconfdir}/gconf/schemas/mutter.schemas \
  > /dev/null || :

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS HACKING doc/theme-format.txt
%doc %{_mandir}/man1/mutter.1.gz
%doc %{_mandir}/man1/mutter-message.1.gz
%{_bindir}/mutter
%{_bindir}/mutter-message
%{_datadir}/applications/*.desktop
%{_datadir}/gnome/wm-properties/mutter-wm.desktop
%{_sysconfdir}/gconf/schemas/mutter.schemas
%{_datadir}/mutter
%{_libdir}/lib*.so.*
%{_libdir}/mutter/

%files devel
%defattr(-,root,root,-)
%{_bindir}/mutter-theme-viewer
%{_bindir}/mutter-window-demo
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%doc %{_mandir}/man1/mutter-theme-viewer.1.gz
%doc %{_mandir}/man1/mutter-window-demo.1.gz

%changelog
* Sat Aug 29 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-3
- Fix %%preun GConf script to properly be for package removal

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-2
- Add a workaround for Red Hat bug #520209

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-1
- Update to 2.27.3, remove mutter-metawindow.patch

* Fri Aug 21 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.2-2
- Add upstream patch needed by latest mutter-moblin

* Tue Aug 11 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.2-1
- New upstream 2.27.2 release. Drop upstreamed patches.

* Wed Jul 29 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-5
- Add upstream patches for clutter 1.0

* Wed Jul 29 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-4
- Add patch to fix mutter --replace

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-2
- Updates from review request

* Fri Jul 17 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-1
- Update to official 2.27.1 and review updates

* Thu Jun 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.0-0.2
- Updates from initial reviews

* Thu Jun 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.0-0.1
- Initial packaging

Name:           gjs
Version:        1.29.16
Release:        1%{?dist}
Summary:        Javascript Bindings for GNOME

Group:          System Environment/Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:        MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:            http://live.gnome.org/Gjs/
#VCS:           git://git.gnome.org/gjs
Source0:        http://download.gnome.org/sources/%{name}/1.29/%{name}-%{version}.tar.xz

BuildRequires: js-devel
BuildRequires: cairo-devel
BuildRequires: gobject-introspection-devel >= 1.29.16
BuildRequires: readline-devel
BuildRequires: dbus-glib-devel
BuildRequires: intltool
BuildRequires: pkgconfig
# Bootstrap requirements
BuildRequires: gtk-doc gnome-common

# https://bugzilla.gnome.org/show_bug.cgi?id=655482
Patch0: install-gi-headers.patch

%description
Gjs allows using GNOME libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -q

%patch0 -p1 -b .headers
rm -f configure

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure --disable-static)

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS README
%{_bindir}/gjs
%{_bindir}/gjs-console
%{_libdir}/*.so.*
%{_libdir}/gjs-1.0
%{_libdir}/gjs/*.typelib
%{_datadir}/gjs-1.0

%files devel
%doc examples/*
%{_includedir}/gjs-1.0
%{_libdir}/gjs/*.gir
%{_libdir}/pkgconfig/gjs-1.0.pc
%{_libdir}/pkgconfig/gjs-dbus-1.0.pc
%{_libdir}/pkgconfig/gjs-internals-1.0.pc
%{_libdir}/*.so

%changelog
* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 1.29.16-1
- Update to 1.29.16

* Thu Aug 04 2011 Bastien Nocera <bnocera@redhat.com> 1.29.15-3
- Install missing headers

* Thu Jul 28 2011 Colin Walters <walters@verbum.org> - 1.29.15-2
- BR latest g-i to fix build issue

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 1.29.15-1
- Update to 1.29.15

* Mon Jun 27 2011 Adam Williamson <awilliam@redhat.com> - 1.29.0-2
- build against js, not gecko (from f15 branch, but patch not needed)
- BR cairo-devel (also from f15)

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.29.0-1
- Update to 1.29.0

* Thu Apr 28 2011 Christopher Aillon <caillon@redhat.com> - 0.7.14-3
- Rebuild against newer gecko

* Thu Apr 14 2011 Colin Walters <walters@verbum.org> - 0.7.14-2
- BR readline; closes #696254

* Mon Apr  4 2011 Colin Walters <walters@verbum.org> - 0.7.14-1
- Update to 0.7.14; fixes notification race condition on login

* Tue Mar 22 2011 Christopher Aillon <caillon@redhat.com> - 0.7.13-3
- Rebuild against newer gecko

* Fri Mar 18 2011 Christopher Aillon <caillon@redhat.com> - 0.7.13-2
- Rebuild against newer gecko

* Thu Mar 10 2011 Colin Walters <walters@verbum.org> - 0.7.13-1
- Update to 0.7.13

* Wed Mar  9 2011 Christopher Aillon <caillon@redhat.com> - 0.7.11-3
- Rebuild against newer gecko

* Fri Feb 25 2011 Christopher Aillon <caillon@redhat.com> - 0.7.11-2
- Rebuild against newer gecko

* Tue Feb 22 2011 Owen Taylor <otaylor@redhat.com> - 0.7.11-1
- Update to 0.7.11

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 0.7.10-4
- Require gecko-libs instead of xulrunner

* Wed Feb  9 2011 Colin Walters <walters@verbum.org> - 0.7.10-3
- Add a hardcoded Requires on xulrunner; see comment

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Colin Walters <walters@verbum.org> - 0.7.10-1
- New upstream release

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 0.7.9-3
- Rebuild for new xulrunner

* Fri Jan 14 2011 Christopher Aillon <caillon@redhat.com> - 0.7.9-2
- Rebuild for new xulrunner

* Fri Jan 14 2011 Colin Walters <walters@verbum.org> - 0.7.9-1
- 0.7.9

* Wed Jan 12 2011 Colin Walters <walters@verbum.org> - 0.7.8-1
- Update to 0.7.8
- Drop upstreamed patches
- BR latest g-i for GI_TYPE_TAG_UNICHAR

* Wed Dec 29 2010 Dan Williams <dcbw@redhat.com> - 0.7.7-3
- Work around Mozilla JS API changes

* Wed Dec 22 2010 Colin Walters <walters@verbum.org> - 0.7.7-2
- Remove rpath removal; we need an rpath on libmozjs, since
  it's in a nonstandard directory.

* Mon Nov 15 2010 Owen Taylor <otaylor@redhat.com> - 0.7.7-1
- Update to 0.7.7

* Tue Nov  9 2010 Owen Taylor <otaylor@redhat.com> - 0.7.6-1
- Update to 0.7.6

* Fri Oct 29 2010 Owen Taylor <otaylor@redhat.com> - 0.7.5-1
- Update to 0.7.5

* Mon Oct  4 2010 Owen Taylor <otaylor@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 0.7.1-3
- Rebuild for new gobject-introspection

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.7.1-2
- New upstream version
- Changes to allow builds from snapshots

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> 0.7-1
- Update to 0.7

* Wed Mar 24 2010 Peter Robinson <pbrobinson@gmail.com> 0.6-1
- New upstream 0.6 stable release

* Sat Feb 20 2010 Peter Robinson <pbrobinson@gmail.com> 0.5-1
- New upstream 0.5 release

* Thu Jan 14 2010 Peter Robinson <pbrobinson@gmail.com> 0.5-0.1
- Move to git snapshot to fix compile against xulrunner 1.9.2.1

* Thu Aug 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-1
- New upstream 0.4 release

* Fri Aug  7 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-2
- Updates from the review request

* Wed Jul  8 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-1
- New upstream release. Clarify licensing for review

* Sat Jun 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.2-1
- Initial packaging

%global glib2_version 2.58.0
%global gobject_introspection_version 1.61.2
%global gtk3_version 3.20
%global mozjs78_version 78.4.0-1

Name:          gjs
Version:       1.66.1
Release:       2%{?dist}
Summary:       Javascript Bindings for GNOME

# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           https://wiki.gnome.org/Projects/Gjs
Source0:       https://download.gnome.org/sources/%{name}/1.66/%{name}-%{version}.tar.xz

BuildRequires: cairo-gobject-devel
BuildRequires: dbus-daemon
BuildRequires: dbus-glib-devel
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: gettext
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: mozjs78-devel >= %{mozjs78_version}
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sysprof-devel

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gobject-introspection%{?_isa} >= %{gobject_introspection_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: mozjs78%{?_isa} >= %{mozjs78_version}

# Filter provides for private libraries
%global __provides_exclude_from ^%{_libdir}/gjs/

%description
Gjs allows using GNOME libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary: Tests for the gjs package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The gjs-tests package contains tests that can be used to verify
the functionality of the installed gjs package.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
#meson_test

%files
%license COPYING
%doc NEWS README.md
%{_bindir}/gjs
%{_bindir}/gjs-console
%{_libdir}/*.so.*
%{_libdir}/gjs

%files devel
%doc examples/*
%{_includedir}/gjs-1.0
%{_libdir}/pkgconfig/gjs-1.0.pc
%{_libdir}/*.so
%dir %{_datadir}/gjs-1.0
%{_datadir}/gjs-1.0/lsan/
%{_datadir}/gjs-1.0/valgrind/

%files tests
%{_libexecdir}/installed-tests/
%{_datadir}/glib-2.0/schemas/org.gnome.GjsTest.gschema.xml
%{_datadir}/installed-tests/

%changelog
* Mon Oct 19 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.66.1-2
- Rebuild against mozjs78-78.4.0-1

* Fri Oct  9 2020 Kalev Lember <klember@redhat.com> - 1.66.1-1
- Update to 1.66.1

* Tue Sep 22 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.66.0-2
- Rebuild against mozjs78-78.3.0-1

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 1.66.0-1
- Update to 1.66.0

* Sun Sep 06 2020 Kalev Lember <klember@redhat.com> - 1.65.92-1
- Update to 1.65.92

* Fri Aug 28 2020 Adam Williamson <awilliam@redhat.com> - 1.65.91-3
- Backport MR #483 to fix frequent g_variant_unref errors in journal

* Mon Aug 24 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.91-2
- Rebuild against mozjs78-78.2.0-1

* Sun Aug 23 2020 Kalev Lember <klember@redhat.com> - 1.65.91-1
- Update to 1.65.91

* Mon Aug 17 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.90-1
- Update to 1.65.90
- Switch over from mozjs68 to mozjs78

* Fri Jul 31 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.4-3
- Rebuild against mozjs68-68.11.0-1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.65.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 1.65.4-1
- Update to 1.65.4

* Tue Jun 30 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.3-2
- Rebuild against mozjs68-68.10.0-1

* Fri Jun 05 2020 Kalev Lember <klember@redhat.com> - 1.65.3-1
- Update to 1.65.3

* Tue Jun 02 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.2-3
- Rebuild against mozjs68-68.9.0-1

* Tue May 12 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.2-2
- Rebuild against mozjs68-68.8.0-1

* Tue May 05 2020 Kalev Lember <klember@redhat.com> - 1.65.2-1
- Update to 1.65.2

* Tue Apr 07 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.65.1-2
- Rebuild against mozjs68-68.7.0-1

* Sat Mar 28 2020 Kalev Lember <klember@redhat.com> - 1.65.1-1
- Update to 1.65.1

* Sat Mar 28 2020 Kalev Lember <klember@redhat.com> - 1.64.1-1
- Update to 1.64.1

* Tue Mar 17 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.64.0-2
- Rebuild against mozjs68-68.6.0-2 (built with gcc 10)

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 1.64.0-1
- Update to 1.64.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 1.63.92-1
- Update to 1.63.92

* Tue Feb 18 2020 Kalev Lember <klember@redhat.com> - 1.63.91-1
- Update to 1.63.91

* Mon Feb 03 2020 Kalev Lember <klember@redhat.com> - 1.63.90-1
- Update to 1.63.90
- Switch to building with mozjs68

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.63.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Kalev Lember <klember@redhat.com> - 1.63.3-1
- Update to 1.63.3

* Wed Dec 11 2019 Florian Müllner <fmuellner@redhat.com> - 1.63.2-1
- Update to 1.63.2

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 1.58.3-1
- Update to 1.58.3

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 1.58.1-1
- Update to 1.58.1

* Sun Sep 08 2019 Kalev Lember <klember@redhat.com> - 1.58.0-1
- Update to 1.58.0

* Wed Sep 04 2019 Kalev Lember <klember@redhat.com> - 1.57.92-2
- Rebuild against mozjs60 60.9.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 1.57.92-1
- Update to 1.57.92

* Mon Aug 19 2019 Kalev Lember <klember@redhat.com> - 1.57.91-1
- Update to 1.57.91

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 1.57.90-1
- Update to 1.57.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.57.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Kalev Lember <klember@redhat.com> - 1.57.4-1
- Update to 1.57.4
- Enable sysprof capture support

* Tue Jul 09 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.57.3-3
- Rebuild against mozjs60 60.8.0

* Sat Jun 22 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.57.3-2
- Rebuild against mozjs60 60.7.2

* Thu Jun 20 2019 Kalev Lember <klember@redhat.com> - 1.57.3-1
- Update to 1.57.3

* Wed Jun 19 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.57.2-3
- Rebuild against mozjs60 60.7.1

* Tue May 21 2019 Kalev Lember <klember@redhat.com> - 1.57.2-2
- Rebuild against mozjs60 60.7.0

* Tue May 21 2019 Kalev Lember <klember@redhat.com> - 1.57.2-1
- Update to 1.57.2

* Thu May 09 2019 Kalev Lember <klember@redhat.com> - 1.57.1-1
- Update to 1.57.1

* Wed May 08 2019 Kalev Lember <klember@redhat.com> - 1.56.2-1
- Update to 1.56.2

* Mon Apr 15 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.56.1-2
- Rebuild against mozjs60-60.6.1

* Mon Apr 08 2019 Kalev Lember <klember@redhat.com> - 1.56.1-1
- Update to 1.56.1

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 1.56.0-1
- Update to 1.56.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 1.55.92-1
- Update to 1.55.92

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 1.55.91-1
- Update to 1.55.91

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.55.90-3
- Rebuild for readline 8.0

* Thu Feb 14 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.55.90-2
- Rebuild against mozjs60 built by GCC9: ABI change detected by Taskotron/abicheck

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 1.55.90-1
- Update to 1.55.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.55.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Kalev Lember <klember@redhat.com> - 1.55.4-1
- Update to 1.55.4

* Wed Jan 02 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.55.1-3
- Add BR dbus-daemon to fix running tests on F30

* Wed Jan 02 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.55.1-2
- Rebuilt against mozjs60 60.4.0

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 1.55.1-1
- Update to 1.55.1

* Fri Oct 05 2018 Kalev Lember <klember@redhat.com> - 1.54.1-2
- Rebuilt against mozjs60 60.2.2

* Mon Sep 24 2018 Kalev Lember <klember@redhat.com> - 1.54.1-1
- Update to 1.54.1

* Thu Sep 13 2018 Kalev Lember <klember@redhat.com> - 1.54.0-3
- Rebuilt against mozjs60 60.2.0 that broke ABI (#1628438)

* Mon Sep 10 2018 Kalev Lember <klember@redhat.com> - 1.54.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 1.54.0-1
- Update to 1.54.0
- Switch to building with mozjs60

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.52.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 08 2018 Kalev Lember <klember@redhat.com> - 1.52.3-1
- Update to 1.52.3

* Wed Apr 18 2018 Kalev Lember <klember@redhat.com> - 1.52.2-1
- Update to 1.52.2

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 1.52.1-1
- Update to 1.52.1

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 1.52.0-1
- Update to 1.52.0

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 1.51.92-1
- Update to 1.51.92

* Wed Feb 21 2018 Kalev Lember <klember@redhat.com> - 1.51.91-1
- Update to 1.51.91

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 1.51.90-1
- Update to 1.51.90
- Drop ldconfig scriptlets
- Filter provides for private libraries

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.50.4-2
- Switch to %%ldconfig_scriptlets

* Sun Jan 28 2018 Kalev Lember <klember@redhat.com> - 1.50.4-1
- Update to 1.50.4

* Thu Jan 18 2018 Kalev Lember <klember@redhat.com> - 1.50.3-1
- Update to 1.50.3

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 1.50.2-1
- Update to 1.50.2

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 1.50.1-1
- Update to 1.50.1

* Wed Sep 20 2017 Kalev Lember <klember@redhat.com> - 1.50.0-1
- Update to 1.50.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com> - 1.49.3-1
- Update to 1.49.3

* Tue Jun 13 2017 Bastien Nocera <bnocera@redhat.com> - 1.49.2-2
+ gjs-1.49.2-2
- Add fix for possible use-after-free crasher (bgo #781799)

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 1.49.2-1
- Update to 1.49.2

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 1.48.3-1
- Update to 1.48.3

* Fri Apr 21 2017 Kalev Lember <klember@redhat.com> - 1.48.2-1
- Update to 1.48.2

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 1.48.1-1
- Update to 1.48.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 1.48.0-1
- Update to 1.48.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 1.47.92-1
- Update to 1.47.92

* Wed Mar 01 2017 Kalev Lember <klember@redhat.com> - 1.47.91-1
- Update to 1.47.91

* Wed Feb 15 2017 Kalev Lember <klember@redhat.com> - 1.47.90-1
- Update to 1.47.90
- Switch to building with mozjs38
- Set minimum required glib2 and gtk3 versions

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Kalev Lember <klember@redhat.com> - 1.47.4-1
- Update to 1.47.4
- Remove lib64 rpaths

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.47.0-2
- Rebuild for readline 7.x

* Thu Nov 10 2016 Florian Müllner <fmuellner@redhat.com> - 3.47.0-1
- Update to 1.47.0

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 1.46.0-1
- Update to 1.46.0
- Don't set group tags
- Use make_install macro

* Tue Jul 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.1.45.4-1
- Update to 1.45.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.45.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Kalev Lember <klember@redhat.com> - 1.45.3-1
- Update to 1.45.3
- Update project URL

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 1.44.0-1
- Update to 1.44.0
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.43.3-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Dec 29 2014 Richard Hughes <rhughes@redhat.com> - 1.43.3-1
- Update to 1.43.3

* Mon Sep 29 2014 Kalev Lember <kalevlember@gmail.com> - 1.42.0-1
- Update to 1.42.0

* Fri Sep  5 2014 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.41.91-2
- Build installed tests

* Mon Sep 01 2014 Kalev Lember <kalevlember@gmail.com> - 1.41.91-1
- Update to 1.41.91

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.41.4-1
- Update to 1.41.4

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 1.41.3-1
- Update to 1.41.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Kalev Lember <kalevlember@gmail.com> - 1.40.1-1
- Update to 1.40.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 1.40.0-2
- Tighten -devel deps
- Set minimum gobject-introspection version

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 1.40.0-1
- Update to 1.40.0

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 1.39.91-1
- Update to 1.39.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1.39.90-1
- Update to 1.39.90

* Wed Feb 05 2014 Adam Williamson <awilliam@redhat.com> - 1.39.3-2
- build against mozjs24

* Wed Jan 29 2014 Richard Hughes <rhughes@redhat.com> - 1.39.3-1
- Update to 1.39.3

*  Wed Nov 20 2013 Jasper St. Pierre <jstpierre@mecheye.net> - 1.39.0-1
- Update to 1.39.0

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 1.38.1-1
- Update to 1.38.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 1.38.0-1
- Update to 1.38.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 1.37.6-1
- Update to 1.37.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 1.37.4-1
- Update to 1.37.4

* Tue May 28 2013 Colin Walters <walters@verbum.org> - 1.37.1-1
- Update to 1.37.1, and switch to mozjs17

* Mon Apr 29 2013 Kalev Lember <kalevlember@gmail.com> - 1.36.1-1
- Update to 1.36.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1.36.0-1
- Update to 1.36.0

* Thu Mar 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.35.9-1
- Update to 1.35.9

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 1.35.8-1
- Update to 1.35.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 1.35.4-1
- Update to 1.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.35.3-1
- Update to 1.35.3

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 1.35.2-1
- Update to 1.35.2

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.34.0-1
- Update to 1.34.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 1.33.14-1
- Update to 1.33.14

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 1.33.10-1
- Update to 1.33.10

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.33.9-1
- Update to 1.33.9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 1.33.4-1
- Update to 1.33.4

* Thu Jul  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.33.3-2
- Enable verbose build

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 1.33.3-1
- Update to 1.33.3

* Sat Jun  9 2012 Matthias Clasen <mclasen@redhat.com> - 1.33.2-2
- Fix the build

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 1.33.2-1
- Update to 1.33.2

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 1.32.0-1
- Update to 1.32.0

* Wed Mar 21 2012 Matthias Clasen <mclasen@redhat.com> - 1.31.22-1
- Update to 1.31.22

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 1.31.20-1
- Update to 1.31.20

* Tue Feb  7 2012 Colin Walters <walters@verbum.org> - 1.31.10-2
- Drop custom .gir/.typelib directories; see upstream commit
  ea4d639eab307737870479b6573d5dab9fb2915a

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 1.31.10-1
- 1.31.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> 1.31.6-1
- 1.31.6

* Fri Dec 02 2011 Karsten Hopp <karsten@redhat.com> 1.31.0-2
- fix crash on PPC, bugzilla 749604

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 1.31.0-1
- Update to 1.31.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.30.0-1
- Update to 1.30.0

* Wed Sep 21 2011 Matthias Clasen <mclasen@redhat.com> 1.29.18-1
- Update to 1.29.18

* Mon Sep 05 2011 Luis Bazan <bazanluis20@gmail.com> 1.29.17-2
- mass rebuild

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> 1.29.17-1
- Update to 1.29.17

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 1.29.16-1
- Update to 1.29.16

* Thu Jul 28 2011 Colin Walters <walters@verbum.org> - 1.29.0-3
- BR latest g-i to fix build issue

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

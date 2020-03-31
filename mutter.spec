%global gtk3_version 3.19.8
%global glib_version 2.53.2
%global gsettings_desktop_schemas_version 3.33.0
%global json_glib_version 0.12.0
%global libinput_version 1.4
%global pipewire_version 0.2.2
%global mutter_api_version 5

Name:          mutter
Version:       3.34.5
Release:       1%{?dist}
Summary:       Window and compositing manager based on Clutter

License:       GPLv2+
#VCS:          git:git://git.gnome.org/mutter
URL:           http://www.gnome.org
Source0:       http://download.gnome.org/sources/%{name}/3.34/%{name}-%{version}.tar.xz

# Work-around for OpenJDK's compliance test
Patch0:        0001-window-actor-Special-case-shaped-Java-windows.patch

# https://gitlab.gnome.org/GNOME/mutter/merge_requests/739
# Complements the backported Xwayland randr resolution change emulation support
# necessary for SDL2 apps to work correctly
Patch1:        0001-window-Add-adjust_fullscreen_monitor_rect-virtual-me.patch
Patch2:        0002-window-xwayland-Add-Xwayland-fullscreen-games-workar.patch

# Mitigate crash on tear down. (rhbz#1770089, rhbz#1770089)
Patch3:        0001-compositor-Guard-against-untimely-calls.patch

BuildRequires: chrpath
BuildRequires: pango-devel
BuildRequires: startup-notification-devel
BuildRequires: gnome-desktop3-devel
BuildRequires: glib2-devel >= %{glib_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: pkgconfig
BuildRequires: gobject-introspection-devel >= 1.41.0
BuildRequires: libSM-devel
BuildRequires: libwacom-devel
BuildRequires: libX11-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcursor-devel
BuildRequires: libXcomposite-devel
BuildRequires: libxcb-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: libxkbfile-devel
BuildRequires: libXtst-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: pkgconfig(glesv2)
BuildRequires: pam-devel
BuildRequires: pipewire-devel >= %{pipewire_version}
BuildRequires: pkgconfig(sysprof-capture-3)
BuildRequires: systemd-devel
BuildRequires: upower-devel
BuildRequires: xorg-x11-server-Xorg
BuildRequires: xkeyboard-config-devel
BuildRequires: zenity
BuildRequires: desktop-file-utils
# Bootstrap requirements
BuildRequires: gtk-doc gnome-common gettext-devel git
BuildRequires: libcanberra-devel
BuildRequires: gsettings-desktop-schemas-devel >= %{gsettings_desktop_schemas_version}
BuildRequires: gnome-settings-daemon-devel
BuildRequires: meson
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-eglstream)

BuildRequires: json-glib-devel >= %{json_glib_version}
BuildRequires: libgudev1-devel
BuildRequires: libinput-devel >= %{libinput_version}
BuildRequires: xorg-x11-server-Xwayland

Obsoletes: mutter-wayland < 3.13.0
Obsoletes: mutter-wayland-devel < 3.13.0

# Make sure yum updates gnome-shell as well; otherwise we might end up with
# broken gnome-shell installations due to mutter ABI changes.
Conflicts: gnome-shell < 3.21.1

Requires: control-center-filesystem
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: pipewire%{_isa} >= %{pipewire_version}
Requires: startup-notification
Requires: dbus
Requires: zenity

Requires:      json-glib%{?_isa} >= %{json_glib_version}
Requires:      libinput%{?_isa} >= %{libinput_version}

Patch100: 575.patch
Patch110: 724.patch
Patch120: rt-default.patch
Patch130: 798.patch
Patch150: 526.patch
Patch180: 692.patch
Patch190: 888.patch
Patch200: 889.patch
Patch210: 898.patch
Patch220: 867.patch
Patch230: 906.patch
Patch250: 918.patch
Patch260: 850.patch
Patch270: 969.patch
Patch280: 983.patch
Patch290: 985.patch
Patch300: 984.patch
Patch310: 1000.patch
Patch320: 991.patch
Patch330: 1001.patch
Patch340: 1017.patch
Patch350: 1004.patch
Patch360: 1033.patch
Patch380: 1036.patch
Patch390: 1049.patch
Patch400: 1052.patch
Patch410: 1058.patch
Patch411: ebc07871eb5043a856f2698bb6320a5ef7dd521d.patch
Patch420: 1082.patch
Patch430: 1074.patch
Patch440: 1071.patch
Patch450: 1099.patch
Patch460: 1083.patch
Patch470: 1008.patch

%description
Mutter is a window and compositing manager that displays and manages
your desktop via OpenGL. Mutter combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Mutter can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as GNOME Shell. For
this reason, Mutter is very extensible via plugins, which are used both
to add fancy visual effects and to rework the window management
behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for developing Mutter plugins. Also includes
utilities for testing Metacity/Mutter themes.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -S git

%build
%meson -Degl_device=true -Dwayland_eglstream=true
%meson_build

%install
%meson_install

%find_lang %{name}

# Mutter contains a .desktop file so we just need to validate it
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc NEWS
%{_bindir}/mutter
%{_datadir}/applications/*.desktop
%{_libdir}/lib*.so.*
%{_libdir}/mutter-%{mutter_api_version}/
%{_libexecdir}/mutter-restart-helper
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-*.xml
%{_mandir}/man1/mutter.1*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tests
%{_libexecdir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/mutter-%{mutter_api_version}/tests

%changelog
* Tue Mar 31 2020 Florian Müllner <fmuellner@redhat.com> - 3.34.5-1
- Update to 3.34.5

* Wed Mar 11 2020 Jonas Ådahl <jadahl@redhat.com> - 3.34.4-2
- Avoid crash when KMS node starts returning NULL resources
  Resolves: #1812423
- Fixes landed after 3.34.4
  Resolves: #1808450
  Resolves: #1808107
  Resolves: #1807576
  Resolves: #1806600
- Don't crash when fullscreen on inert wl_output
  Resolves: #1791357

* Mon Mar 02 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.4-101
- Add ebc07871 "shaped-texture: Add `get_width()`/`get_height()` API"
- Add !1082 "Culling fixes" @39a8c047 (partial)
- Add !1074 "clutter/stage: Cache get_update_time results" @08880261 (manually rebased)
- Add !1071 "cogl: reduce temporary allocations calculating redraw regions" @c1b189ed (manually rebased)
- Remove !1035 "window: Ignore requests to be placed on non-existent workspaces" (merged)
- Add !1099 "cursor-renderer-native: Fix hw cursor for non-square sprites" @390fd7dd
- Add !1083 "clutter: do less when removing actors" @a3fc6518
- Add !1008 "wayland/keyboard: Use write() instead of mmapped address to write file" @cb683ae4
- Rebase to gnome-3-34@2709a4ff

* Mon Feb 17 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.4-100
- Add !1058 "window-actor/x11: Make culling of opaque windows X11 only" @c89f8f19
- Add !1052 "cullable: Check if effects are disabled" @aceadfe3
- Add !1049 "wayland/actor-surface: Do not set opaque region for XWayland clients" @19814497
- Add !1036 "cullable: Support culling of integer scaled actors" @264f6885 (manually rebased)
- Rebase !798 "Wayland surface fullscreen unredirect"
- Rebase to 3.34.4-1.fc31

* Sun Feb 16 2020 Florian Müllner <fmuellner@redhat.com> - 3.34.4-1
- Update to 3.34.4

* Tue Feb 04 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.3-201
- Add !1035 "window: Ignore requests to be placed on non-existent workspaces" @aa0aa89a
- Rebase to gnome-3-34@2235629d

* Sat Feb 01 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.3-200
- Update !983 "clutter/text: Check if attributes are equal before applying" @9b7fe584
- Update !1001 "More selection leak fixes" @98040e67
- Add !1033 "clutter/actor: Fix GValue leak when overwriting transition values" @55b1f914
- Add !1004 "background: Scale monitor_area after texture creation" @cf6493d3
- Add !1017 "backend-eglnative: Search for the xsettings schema recursively" @d28a6409
- Remove !1002 "Region leak fixes" (upstreamed)
- Rebase to gnome-3-34@666bd250

* Tue Jan 14 2020 Jonas Ådahl <jadahl@redhat.com> - 3.34.3-2
- Backport KMS race condition crash fix
- Backport Wayland subsurface crash fix
  Resolves: #1779865
  Resolves: #1770591

* Mon Jan 13 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.3-101
- Add !1002 "Region leak fixes" @8499c7da
- Add !1001 "More selection leak fixes" @9584dd8d
- Add !991 "Miscellaneous leak fixes" @802309ca
- Add !1000 "clutter-actor: Add detail to captured-event" @177dbd65

* Mon Jan 06 2020 Yussuf Khalil <dev@pp3345.net> - 3.34.3-100
- Rebase to 3.34.3-1.fc31

* Sun Jan 05 2020 Florian Müllner <fmuellner@redhat.com> - 3.34.3-1
- Update to 3.34.3

* Fri Dec 27 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.2-101
- Add !984 "Ignore monitor connector ID when possible" @9958f6a5
- Add !985 "window-actor: Also cull out clip_region" @99db3cc9
- Add !983 "clutter/text: Check if attributes are equal before applying" @59f4e36f
- Add !969 "Batch clip rectangles into a single upload" @4aab814c (manually rebased)
- Update !724 "Sync timelines to hardware vsync" @f7d81f8a (manually rebased)
- Rebase to gnome-3-34@57243108

* Sun Dec 15 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.2-100
- Rebase to 3.34.2-1.fc31

* Wed Dec 11 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.2-1
- Update to 3.34.2
- Drop relevant downstream patches

* Mon Dec 09 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-1200
- Rebase to gnome-3-34@868a6179

* Mon Dec 02 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 3.34.1-12
- Backport patch to fix clipboard manager crashes

* Wed Nov 27 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-1101
- Rebase to gnome-3-34@1b75d78c

* Mon Nov 18 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-1100
- Remove !875 "window-actor: Destroy the actor despite stuck animations" (obsoleted)
- Remove !873 "fix The Memory Leak (2019-10-21T19:00:24+02:00 edition)" (merged)
- Add !850 "Make default focus window on each workspace appear focused" @f5252158 (manually rebased)
- Rebase to gnome-3-34@d78585d6

* Tue Nov 12 2019 Jonas Ådahl <jadahl@redhat.com> - 3.34.1-11
- Backport two memory leak fixes

* Tue Nov 12 2019 Jonas Ådahl <jadahl@redhat.com> - 3.34.1-10
- Backport yet another patch from the stable branch

* Mon Nov 11 2019 Jonas Ådahl <jadahl@redhat.com> - 3.34.1-9
- Backport current patches from the stable branch
- Add patchs to mitigate crash on tear down
  Resolves: #1759876
  Resolves: #1764311
  Resolves: #1770535
  Resolves: #1770539
  Resolves: #1770540

* Thu Nov 07 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-800
- Add !867 "Use regions for Cogl clipping and culling" @e746d880 (manually rebased)
- Add !918 "surface-actor-wayland: Do not send frame callbacks if the actor is obscured" @5e87d67e (manually rebased)
- Add !875 "window-actor: Destroy the actor despite stuck animations" @a295538e
- Add !906 "Fix buffer age checks on multiple monitors" @d47324e8
- Add !898 "clutter/cogl: Fix invalidation on non-primary monitors with no buffer age" @6bfa61a3
- Add !889 "clutter/cogl: Fix clipped redraw off scaled views" @9678fd53 (manually rebased)
- Add !888 "Handle empty invalidations" @2e9faaf6
- Add !692 "clutter-stage-cogl: Use regions" @30783949 (manually rebased)
- Rebase to gnome-3-34@cf785989

* Wed Nov 06 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-8
- Backport MR #843 (and related MR #860) to fix log spam (#1761327)

* Wed Nov 06 2019 LuK1337 <priv.luk@gmail.com> - 3.34.1-7
- Backport MR #884

* Mon Nov  4 2019 Hans de Goede <hdegoede@redhat.com> - 3.34.1-6
- Backport 2 patches which complement the backported Xwayland randr
  resolution change emulation support (necessary for SDL2 apps)

* Tue Oct 29 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.1-5
- Enable sysprof support
  The required dependency was missing from rawhide when the feature
  landed, but there's no reason for keeping it disabled nowadays

* Mon Oct 21 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-403
- Add !873 "fix The Memory Leak (2019-10-21T19:00:24+02:00 edition)" @40e6aa7d

* Mon Oct 21 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-402
- Remove !860 "clutter/stage: Actually set key focus to an actor on key focus" (merged)
- Rebase to gnome-3-34@85f5db7e

* Tue Oct 15 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-401
- Add !860 "clutter/stage: Actually set key focus to an actor on key focus" @553211dd
- Unrevert !843 "clutter/actor: Save key-focus state and unset it before destruction"

* Tue Oct 15 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-400
- Revert !843 "clutter/actor: Save key-focus state and unset it before destruction" (regression)
- Remove !849 "x11: Map mimetypes back to selection atoms" (merged)
- Rebase to gnome-3-34@a22731e2

* Mon Oct 14 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-4
- Update MR #832 backport to fully fix cursor zoom bug (#1749433)

* Sun Oct 13 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-3
- Backport MR #849 to fix bug introduced by MR #842

* Sat Oct 12 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-2
- Backport multiple fixes for F31 FE/blocker bugs:
  MR #832 for #1749433 (also needs change in gnome-shell)
  MR #840 for #1760254
  MR #848 for #1751646 and #1759644
  MR #842 for #1758873

* Sat Oct 12 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-102
- Unrevert !842 "x11: Translate well known selection atoms to mimetypes"
- Add !849 "x11: Map mimetypes back to selection atoms" @5c1be223

* Sat Oct 12 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-101
- Revert !842 "x11: Translate well known selection atoms to mimetypes" (regression)

* Sat Oct 12 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.1-100
- Remove !828 "clutter/actor: Mark implicit transitions as remove-on-complete" (merged)
- Rebase to master@e1751ad9

* Wed Oct 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Fri Oct 04 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.0-500
- Add !526 "Implement scaled/transformed hardware cursors" @b99f08c6
- Add !828 "clutter/actor: Mark implicit transitions as remove-on-complete" @f74812d3
- Rebase to master@ca318c15

* Sat Sep 28 2019 Kenneth Topp <toppk@bllue.org> - 3.34.0-5
- Backport fix for dual special modifier keys bug (#1754867)
- Backport fix that enables core dumps (#1748145)

* Sat Sep 28 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.0-400
- Add !798 "Wayland surface fullscreen unredirect" @7377cf85 (manually rebased)
- Rebase to master@437f6b3d

* Fri Sep 27 2019 Kenneth Topp <toppk@bllue.org> - 3.34.0-4
- Backport a patch to prevent crash during animations
- See upstream issue https://gitlab.gnome.org/GNOME/mutter/issues/815

* Sat Sep 21 2019 Yussuf Khalil <dev@pp3345.net> - 3.34.0-300
- Enable real-time scheduling by default
- Add !724 "Sync timelines to hardware vsync" @e335d349
- Add !575 "Honour `CLUTTER_ACTOR_NO_LAYOUT` more efficiently" @1e3acd0e
- Rebase to master@b5775e3d

* Thu Sep 12 2019 Kalev Lember <klember@redhat.com> - 3.34.0-3
- Update previous patch to final upstream version

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Backport a patch to fix xsettings/ibus-x11 initialization (#1750512)

* Mon Sep 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Wed Sep 04 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Tue Sep 03 2019 Ray Strode <rstrode@redhat.com> - 3.33.91-2
- Fix crash dealing with powersaving
  Resolves: #1747845

* Wed Aug 21 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.91-1
- Update to 3.33.91

* Sat Aug 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Kalev Lember <klember@redhat.com> - 3.33.4-2
- Rebuilt for libgnome-desktop soname bump

* Sat Jul 20 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Mon Jun 24 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Wed May 22 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.2-1
- Update to 3.33.2

* Tue May 14 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Wed Apr 17 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Wed Apr 17 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-4
- Backport MR #498 for spinner bug, plus two crasher fixes
  Resolves: #1692135

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-3
- Rebuild with Meson fix for #1699099

* Mon Mar 25 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-2
- Backport work-around for hangul text input bug (rhbz#1632981)

* Tue Mar 12 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Fri Mar 08 2019 Kalev Lember <klember@redhat.com> - 3.31.92-3
- Backport more inverted colour fixes (#1686649)

* Wed Mar 06 2019 Kalev Lember <klember@redhat.com> - 3.31.92-2
- Backport a patch to fix inverted colours

* Tue Mar 05 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 21 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Thu Feb 07 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Sat Nov 17 2018 Kalev Lember <klember@redhat.com> - 3.31.2-2
- Remove libtool .la files from private libs (#1622944)

* Wed Nov 14 2018 Florian Müllner <fmuellner@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Mon Oct 22 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-5
- Backport work-around for hangul text input bug (rhbz#1632981)

* Sat Oct 20 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-4
- Backport a couple of memory leak fixes (rhbz#1641254)

* Thu Oct 11 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-3
- Fix disabled monitor when laptop lid is closed (rhbz#1638444)

* Thu Oct 11 2018 David Herrmann <dh.herrmann@gmail.com> - 3.30.1-2
- Reduce 'dbus-x11' dependency to 'dbus'. The xinit script are no longer the
  canonical way to start dbus, but the 'dbus' package is nowadays required to
  provide a user and system bus to its dependents.

* Mon Oct 08 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Wed Oct 03 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-3
- Backport fix for #1630943 from upstream master

* Thu Sep 06 2018 Mateusz Mikuła <mati865@gmail.com> - 3.30.0-2
- Enable EGLDevice support

* Tue Sep 04 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Wed Aug 29 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Mon Aug 20 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.91-1
- Update to 3.29.91

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 3.29.90-2
- Update libpipewire requirements

* Wed Aug 01 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 3.29.4-2
- Backport MR#175 to fix 90/270 degree screen rotation

* Wed Jul 18 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.4-1
- Update to 3.29.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 3.29.2-2
- Backport crasher fix from upstream master (#1585360)

* Thu May 24 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.2-1
- Update to 3.29.2

* Wed Apr 25 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Fri Apr 13 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Wed Feb 28 2018 Adam Williamson <awilliam@redhat.com> - 3.27.91-2
- Backport MR#36 to fix RHBZ #1547691 (GGO #2), mouse issues

* Wed Feb 21 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.1-4
- Rebuild against newer gnome-desktop3 package
- Add patch for adjustments to pipewire 0.1.8 API

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.1-2
- Remove obsolete scriptlets

* Mon Oct 30 2017 Florian Müllner <fmuellner@redhat.com> - 3.27.1-1
- Include 32-bit build fixes

* Tue Oct 17 2017 Florian Müllner <fmuellner@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Fri Oct 06 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.1-2
- Fix screencasts

* Wed Oct 04 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Thu Sep 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-5
- Adjust to pipewire API break

* Wed Sep 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-5
- Enable tablet support

* Tue Sep 12 2017 Adam Williamson <awilliam@redhat.com> - 3.26.0-4
- Also backport BGO #787570 fix from upstream

* Tue Sep 12 2017 Adam Williamson <awilliam@redhat.com> - 3.26.0-3
- Backport upstream fixes for crasher bug BGO #787568

* Tue Sep 12 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-2
- Enable remote desktop support

* Tue Sep 12 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Sep 07 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Thu Aug 24 2017 Bastien Nocera <bnocera@redhat.com> - 3.25.91-2
+ mutter-3.25.91-2
- Fix inverted red and blue channels with newer Mesa

* Tue Aug 22 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Thu Aug 10 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Florian Müllner <fmuellner@redhat.con> - 3.25.4-1
- Update to 3.25.4

* Wed Jun 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Wed May 24 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Thu May 18 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.1-2
- Fix copy+paste of UTF8 strings between X11 and wayland

* Thu Apr 27 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.1-1
- Update to 3.25.1

* Tue Apr 11 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Tue Mar 14 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Fri Mar 10 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.91-4
- Apply startup-notification hack again

* Tue Mar 07 2017 Adam Williamson <awilliam@redhat.com> - 3.23.91-3
- Backport more color fixes, should really fix BGO #779234, RHBZ #1428559

* Thu Mar 02 2017 Adam Williamson <awilliam@redhat.com> - 3.23.91-2
- Backport fix for a color issue in 3.23.91 (BGO #779234, RHBZ #1428559)

* Wed Mar 01 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Thu Feb 16 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Fri Dec 02 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.2-2
- Fix build error on 32-bit platforms

* Thu Nov 24 2016 Kevin Fenzi <kevin@scrye.com> - 3.23.2-2
- Some fixes to get building. Still needs patch1 rebased.

* Wed Nov 23 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Tue Nov  8 2016 Matthias Clasen <mclasen@redhat.com> - 3.23.1-2
- Fix 1376471

* Sun Oct 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Tue Oct 18 2016 Kalev Lember <klember@redhat.com> - 3.22.1-3
- Backport a fix to make gnome-screenshot --area work

* Tue Oct 11 2016 Adam Jackson <ajax@redhat.com> - 3.22.1-2
- Prefer eglGetPlatformDisplay() to eglGetDisplay()

* Tue Oct 11 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 28 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.0-2
- Include fix for crash on VT switch

* Mon Sep 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Tue Sep 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 3.21.91-2
- wayland/cursor-role: Increase buffer use count on construction (#1373372)

* Tue Aug 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 3.21.90-3
- clutter/evdev: Fix absolute pointer motion events (#1369492)

* Sat Aug 20 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Update minimum dep versions

* Fri Aug 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Wed Jul 20 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.4-1
- Update to 3.21.4
- Drop downstream patch
- Fix build error on 32-bit

* Tue Jun 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Fri May 27 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Fri Apr 29 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Wed Apr 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.91-2
- Include fix for invalid cursor wl_buffer access

* Thu Mar 03 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Fri Feb 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Thu Dec 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Wed Nov 25 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Tue Nov 10 2015 Ray Strode <rstrode@redhat.com> 3.19.1-5.20151110git049f1556d
- Update to git snapshot

* Thu Oct 29 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Wed Oct 21 2015 Ray Strode <rstrode@redhat.com> 3.18.1-4
- Force the cursor visible on vt switches after setting
  the crtc to workaround that qxl bug from before in a
  different situation
  Related: #1273247

* Wed Oct 21 2015 Kalev Lember <klember@redhat.com> - 3.18.1-3
- Backport a fix for a common Wayland crash (#1266486)

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.1-2
- Bump gnome-shell conflicts version

* Thu Oct 15 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Sep 16 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 03 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Thu Sep 03 2015 Ray Strode <rstrode@redhat.com> 3.17.90-2
- Add workaround for qxl cursor visibility wonkiness that we
  did for f22
  Related: #1200901

* Thu Aug 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Thu Jul 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.3-2
- Bump for new gnome-desktop3

* Thu Jul 02 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Thu Apr 30 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Thu Apr 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1.1-2
- Bump gnome-shell conflicts version

* Wed Apr 15 2015 Rui Matos <rmatos@redhat.com> - 3.16.1.1-1
- Update to 3.16.1.1

* Tue Apr 14 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-2
- Update minimum dep versions
- Use license macro for the COPYING file

* Tue Mar 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> - 3.15.91-2
- Rebuild for libinput soname bump

* Wed Mar 04 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.91-1
- Update to 3.15.91

* Fri Feb 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Mon Feb 02 2015 Adam Williamson <awilliam@redhat.com> - 3.15.4-2
- backport ad90b7dd to fix BGO #743412 / RHBZ #1185811

* Wed Jan 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 3.15.3-3
- Rebuild for libinput soname bump

* Mon Jan 12 2015 Ray Strode <rstrode@redhat.com> 3.15.3-2
- Add specific BuildRequires for wayland bits, so we don't
  get wayland support by happenstance.
- Add BuildRequires for autogoo since ./autogen.sh is run as part of
  the build process

* Fri Dec 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.3-1
- Revert unsatisfiable wayland requirement

* Fri Dec 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Thu Nov 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.2-1
- Update to 3.15.2

* Wed Nov 12 2014 Vadim Rutkovsky <vrutkovs@redhat.com> - 3.15.1-2
- Build installed tests

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Tue Oct 21 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.1-2
- Fix regression in handling raise-on-click option (rhbz#1151918)

* Tue Oct 14 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.1-1
- Update to 3.14.1

* Fri Oct 03 2014 Adam Williamson <awilliam@redhat.com> - 3.14.0-3
- backport fix for BGO #737233 / RHBZ #1145952 (desktop right click broken)

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Bump gnome-shell conflicts version

* Mon Sep 22 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.92-1
- Update to 3.13.92

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.13.91-2
- Rebuild for libinput soname bump

* Wed Sep 03 2014 Florian Müllner <fmuellner@redhat.com> - 3.31.91-1
- Update to 3.13.91, drop downstream patches

* Tue Aug 26 2014 Adel Gadllah <adel.gadllah@gmail.com> - 3.13.90-4
- Apply fix for RH #1133166

* Mon Aug 25 2014 Hans de Goede <hdegoede@redhat.com> - 3.13.90-3
- Add a patch from upstream fixing gnome-shell crashing non stop on
  multi monitor setups (rhbz#1103221)

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 3.13.90-2
- Rebuild for new wayland

* Wed Aug 20 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-3
- Rebuilt for upower 0.99.1 soname bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- New gobject-introspection has been built, drop the last patch again

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Revert annotation updates until we get a new gobject-introspection build

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Update to 3.13.1

* Wed Jun 11 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.2-2
- Backport fix for legacy fullscreen check

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.2-1
- Update to 3.13.2, drop upstreamed patches

* Thu May  8 2014 Matthias Clasen <mclasen@redhat.com> - 3.13.1-5
- Fix shrinking terminals

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-4
- Backport an upstream fix for a Wayland session crash

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-3
- Install mutter-launch as setuid root

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Obsolete mutter-wayland

* Wed Apr 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Tue Apr 15 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions

* Tue Mar 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Wed Mar 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Thu Mar 06 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for cogl soname bump

* Wed Feb 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-4
- Rebuilt for gnome-desktop soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.11.5-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-2
- Rebuilt for cogl soname bump

* Wed Feb 05 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Fri Dec 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Wed Nov 13 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Wed Oct 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Tue Oct 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1.1-1
- Update to 3.10.1.1

* Mon Oct 14 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.0.1-1
- Update to 3.10.0.1

* Mon Sep 23 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-2
- Update the description and URL
- Tighten -devel subpackage deps with _isa
- Use the make_install macro

* Mon Sep 16 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-2
- Rebuilt for libgnome-desktop soname bump

* Tue Sep 03 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-2
- Rebuilt for cogl 1.15.4 soname bump

* Tue Jul 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Wed Jul 10 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Tue Jun 18 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Tue May 28 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Wed May 01 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Tue Apr 23 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 04 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.4-2
- Rebuild for new cogl

* Tue Jan 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Tue Dec 18 2012 Florian Müllner <fmuellner@redhat.com> - 3.7.3-1
- Update to 3.7.3

* Mon Nov 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-2
- Rebuild against new cogl

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.90-2
- Rebuild against new cogl/clutter

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-3
- Make resize grip area larger

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-2
- Don't check for Xinerama anymore - it is now mandatory

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2
- Remove upstreamed patches

* Wed May 09 2012 Adam Jackson <ajax@redhat.com> 3.4.1-3
- mutter-never-slice-shape-mask.patch, mutter-use-cogl-texrect-api.patch:
  Fix window texturing on hardware without ARB_texture_non_power_of_two
  (#813648)

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence glib-compile-schemas scriplets

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Conflict with gnome-shell versions older than 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-2
- Rebuild against new cogl

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-2
- Rebuild against new cogl

* Thu Jan  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-2
- Rebuild against new clutter

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Owen Taylor <otaylor@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Wed Sep 14 2011 Owen Taylor <otaylor@redhat.com> - 3.1.91.1-1
- Update to 3.1.91.1

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-1
- Update to 3.1.90.1

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3.1-3
- Rebuild

* Mon Jul  4 2011 Peter Robinson <pbrobinson@gmail.com> - 3.1.3.1-2
- rebuild against new clutter/cogl

* Mon Jul 04 2011 Adam Williamson <awilliam@redhat.com> - 3.1.3.1-1
- Update to 3.1.3.1

* Thu Jun 30 2011 Owen Taylor <otaylor@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Wed May 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.2.1-1
- Update to 3.0.2.1

* Fri Apr 29 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-3
- Actually apply the patch for #700276

* Thu Apr 28 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Make session saving of gnome-shell work

* Mon Apr 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Owen Taylor <otaylor@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Owen Taylor <otaylor@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Mar  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-2
- Build against libcanberra, to enable AccessX feedback features

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-2
- Rebuild against newer gtk

* Tue Feb  1 2011 Owen Taylor <otaylor@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild against new gtk
- Drop no longer needed %%clean etc

* Mon Nov 29 2010 Owen Taylor <otaylor@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Tue Nov  9 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-2
- Rebuild against newer gtk3

* Fri Oct 29 2010 Owen Taylor <otaylor@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct  4 2010 Owen Taylor <otaylor@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-4
- Rebuild against newer gobject-introspection

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 2.31.5-3
- Rebuild for new gobject-introspection

* Tue Jul 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 2.31.5-2
- Build against gtk3

* Mon Jul 12 2010 Colin Walters <walters@pocket> - 2.31.5-1
- New upstream version

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.31.2-5
- Rebuild against new gobject-introspection

* Tue Jul  6 2010 Colin Walters <walters@verbum.org> - 2.31.2-4
- Changes to support snapshot builds

* Fri Jun 25 2010 Colin Walters <walters@megatron> - 2.31.2-3
- drop gir-repository-devel dep

* Wed May 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-2
- removed "--with-clutter" as configure is claiming it to be an unknown option

* Wed May 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-1
- New upstream 2.31.2 release

* Thu Mar 25 2010 Peter Robinson <pbrobinson@gmail.com> 2.29.1-1
- New upstream 2.29.1 release

* Wed Mar 17 2010 Peter Robinson <pbrobinson@gmail.com> 2.29.0-1
- New upstream 2.29.0 release

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 2.28.1-0.2
- mutter-2.28.1-add-needed.patch: Fix FTBFS from --no-add-needed

* Thu Feb  4 2010 Peter Robinson <pbrobinson@gmail.com> 2.28.1-0.1
- Move to git snapshot

* Wed Oct  7 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Sep 15 2009 Owen Taylor <otaylor@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.4-1
- Remove workaround for #520209
- Update to 2.27.4

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

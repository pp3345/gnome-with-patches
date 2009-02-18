From 24a1f522d52d9cf5720dad28107bea33e623fd7b Mon Sep 17 00:00:00 2001
From: Adam Jackson <ajax@redhat.com>
Date: Wed, 18 Feb 2009 15:33:14 -0500
Subject: [PATCH] uninclude fontmod.h

---
 hw/xfree86/loader/loaderProcs.h |    1 -
 1 files changed, 0 insertions(+), 1 deletions(-)

diff --git a/hw/xfree86/loader/loaderProcs.h b/hw/xfree86/loader/loaderProcs.h
index 827f3a9..a10f0b3 100644
--- a/hw/xfree86/loader/loaderProcs.h
+++ b/hw/xfree86/loader/loaderProcs.h
@@ -56,7 +56,6 @@
 #undef IN_LOADER
 #define IN_LOADER
 #include "xf86Module.h"
-#include <X11/fonts/fontmod.h>
 
 typedef struct module_desc {
     struct module_desc *child;
-- 
1.6.1.3


From 70cd71bc194060b58c0973ba931f69b4de0f698d Mon Sep 17 00:00:00 2001
From: =?utf-8?q?S=C3=B8ren=20Sandmann=20Pedersen?= <sandmann@redhat.com>
Date: Thu, 11 Sep 2008 14:28:25 -0400
Subject: [PATCH] Comment out glxdri2.c

---
 glx/glxdri2.c |    2 ++
 1 files changed, 2 insertions(+), 0 deletions(-)

diff --git a/glx/glxdri2.c b/glx/glxdri2.c
index 9a3bc1f..4862124 100644
--- a/glx/glxdri2.c
+++ b/glx/glxdri2.c
@@ -1,3 +1,4 @@
+#if 0
 /*
  * Copyright © 2007 Red Hat, Inc
  *
@@ -582,3 +583,4 @@ __GLXprovider __glXDRI2Provider = {
     "DRI2",
     NULL
 };
+#endif
-- 
1.6.0.1


// 251 Charts: keeps the app usable offline.
const CACHE = "chart251-d06aac58c1";
const SHELL = ["./", "index.html", "manifest.webmanifest", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png", "favicon.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// serve from the cache right away, and refresh it in the background (pages, fonts and the PDF library alike)
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.open(CACHE).then(async cache => {
    const hit = await cache.match(e.request, { ignoreSearch: e.request.mode === "navigate" });
    const net = fetch(e.request).then(res => { if (res && (res.ok || res.type === "opaque")) cache.put(e.request, res.clone()); return res; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    const res = await net;
    return res || (e.request.mode === "navigate" ? cache.match("index.html") : Response.error());
  }));
});

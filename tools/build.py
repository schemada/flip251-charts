"""Build every published version of Flip 251 Charts from the one editable source, src/chart251.html.

    python3 tools/build.py

Writes:
  index.html, manifest.webmanifest, sw.js   the installable web app (GitHub Pages serves these)
  dist/flip251-charts.html                  the same tool as one plain web page, for any host
  dist/squarespace-code-block.html          paste into a Squarespace Code Block (self-sizing frame)
"""
import os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
import re, html
src=open(os.path.join(ROOT, 'src', 'chart251.html')).read()
title=re.search(r'<title>(.*?)</title>',src).group(1)
style=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
body=src[src.index('</style>')+len('</style>'):]
head_tags=''.join(re.findall(r'<link[^>]+>\n?|<script src=[^>]+></script>\n?',src[:src.index('<style>')]))
standalone=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  f'<title>{title}</title>\n{head_tags}<style>\nhtml{{-webkit-text-size-adjust:100%}}body{{margin:0}}\n[hidden]{{display:none!important}}\n{style}</style>\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n')
open(os.path.join(ROOT, 'dist', 'flip251-charts.html'),'w').write(standalone)
emb_style=re.sub(r'@media \(prefers-color-scheme: dark\) \{.*?\n\}\n','',style,flags=re.S)
emb_style=re.sub(r':root\[data-theme="dark"\] \{[^}]*\}\n','',emb_style)
emb_style=emb_style.replace("background: var(--bg); color: var(--bg-ink);","background: transparent; color: var(--bg-ink);").replace("padding-block: 28px;","padding-block: 8px 24px;")
emb_body=body.strip().replace('<a class="btn primary" id="open" href="#">','<a class="btn primary" id="open" href="#" target="_top">')
resize="""<script>
(function () {
  function send() { try { parent.postMessage({ flip251Height: Math.ceil(document.body.getBoundingClientRect().height) }, "*"); } catch (e) {} }
  window.addEventListener("load", send); window.addEventListener("resize", send);
  if (window.ResizeObserver) new ResizeObserver(send).observe(document.body);
  document.addEventListener("click", function () { setTimeout(send, 50); });
  send();
})();
</script>"""
inner=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  f'<title>{title}</title>{head_tags.replace(chr(10),"")}<style>html{{-webkit-text-size-adjust:100%}}body{{margin:0}}[hidden]{{display:none!important}}{emb_style}</style></head><body>'+emb_body+resize+'</body></html>')
inner=inner.encode('ascii','xmlcharrefreplace').decode()
block=('<!-- Flip 251 Charts: paste this whole block into a Squarespace Code Block -->\n'
  '<iframe id="flip251-charts" title="ii-V-I chart builder for iReal Pro" style="display:block;width:100%;max-width:1200px;margin:0 auto;border:0;height:2100px;" '
  'allow="clipboard-write; web-share" srcdoc="'+html.escape(inner,quote=True)+'"></iframe>\n<script>\n  window.addEventListener("message", function (e) {\n'
  '    var f = document.getElementById("flip251-charts");\n    if (f && e.source === f.contentWindow && e.data && e.data.flip251Height) f.style.height = e.data.flip251Height + "px";\n  });\n</script>\n')
assert all(ord(c)<128 for c in block)
open(os.path.join(ROOT, 'dist', 'squarespace-code-block.html'),'w').write(block)

# ---------------- installable app folder ----------------
import json, os
app_head = """<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="251 Charts">
<meta name="application-name" content="251 Charts">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#e7e2d8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1a1916" media="(prefers-color-scheme: dark)">
<meta name="description" content="Design a custom ii-V-I exercise with basic chord progressions, then send it to iReal Pro or save it as a PDF.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="favicon.png">
"""
app_css = """
/* as an installed app: clear the notch and home bar, no rubber-band scrolling past the ends */
html { overscroll-behavior: none; }
body { padding-top: max(28px, calc(env(safe-area-inset-top, 0px) + 14px)); padding-bottom: max(28px, calc(env(safe-area-inset-bottom, 0px) + 14px)); }
@media (display-mode: standalone) { body { -webkit-touch-callout: none; } .sheetimg { -webkit-touch-callout: default; } }
"""
app_sw = """<script>
  // works offline after the first visit
  if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
</script>
"""
page = standalone.replace("<title>", app_head + "<title>", 1).replace("</style>\n</head>", app_css + "</style>\n</head>", 1).replace("</body>", app_sw + "</body>", 1)
open(os.path.join(ROOT, 'index.html'), 'w').write(page)
manifest = {
  "name": "Flip 251 Charts", "short_name": "251 Charts",
  "description": "Design a custom ii-V-I exercise with basic chord progressions, then send it to iReal Pro or save it as a PDF.",
  "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
  "background_color": "#e7e2d8", "theme_color": "#e7e2d8",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
open(os.path.join(ROOT, 'manifest.webmanifest'), 'w').write(json.dumps(manifest, indent=2))
_ver = hashlib.sha1(page.encode()).hexdigest()[:10]
open(os.path.join(ROOT, 'sw.js'), 'w').write(("""// Flip 251 Charts: keeps the app usable offline.
const CACHE = "chart251-__VERSION__";
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
""").replace("__VERSION__", _ver))
print("built: index.html, manifest.webmanifest, sw.js, dist/flip251-charts.html, dist/squarespace-code-block.html (cache " + _ver + ")")


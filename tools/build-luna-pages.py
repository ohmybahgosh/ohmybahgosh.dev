#!/usr/bin/env python3
"""Builds the Luna Atlas category pages (/luna-atlas/categories/...), the examples page and sitemap.xml
from luna-atlas/catalog.json.  Runs on every deploy after the catalog is refreshed, so counts stay current.
    python3 tools/build-luna-pages.py"""
import os, sys, json, re, glob, datetime
sys.path.insert(0, os.path.dirname(__file__))
from site_template import page, write, article_ld, esc, SITE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = ("Home", "/"); ATLAS = ("Luna Atlas", "/luna-atlas/"); CATS = ("Categories", "/luna-atlas/categories/")
ACC = "#33e1ff"

NAMES = {
    "tv-broadcast": "TV Broadcast / DVR", "misc": "Misc", "input": "Input & Keys", "audio": "Audio", "media": "Media Playback",
    "power": "Power", "apps": "Applications", "bluetooth": "Bluetooth", "network": "Network / Wi-Fi", "settings": "Settings",
    "system-info": "System Info", "security": "Security / Keys", "db": "Database (db8)", "display": "Display / Panel",
    "storage": "Storage & USB", "connection": "Connection Manager", "update": "Software Update", "notifications": "Notifications & Alerts",
    "camera": "Camera", "activity": "Activity Manager", "devmode": "Developer Mode & Testing", "power-mgmt": "Power Management",
    "ui": "UI / Compositor", "picture": "Picture", "location": "Location", "keys": "Key Management", "sound": "Sound",
}
BLURB = {
    "tv-broadcast": "Tuning, channels, the programme guide, recording and everything else the TV's broadcast side does: antenna and cable, CI modules and the DVR.",
    "misc": "Services that don't fit one category: helpers, vendor plugins and smaller system pieces.",
    "input": "The remote, keyboards, mice, gamepads and the TV's HDMI and other external inputs: sending keys, reading input status and switching sources.",
    "audio": "Volume, mute, sound output, audio routing and the TV's audio policy, including sound bars and Bluetooth audio.",
    "media": "The media pipeline: playback sessions, the TV's players, DLNA and casting, AirPlay and media metadata.",
    "power": "Power state, screen off and on, standby and reboot.  Many of these are flagged dangerous for good reason.",
    "apps": "The application manager: launching and closing apps, listing what's installed, the foreground app and app lifecycle.",
    "bluetooth": "Bluetooth pairing, devices, profiles and the remote's Bluetooth link.",
    "network": "Wi-Fi, wired Ethernet, IP settings and network status.",
    "settings": "The settings service: reading and changing the TV's system, picture, sound and other settings.",
    "system-info": "Model, firmware, hardware, device IDs and other system properties.",
    "security": "Certificates, keys, DRM and the TV's security services.",
    "db": "db8, webOS's built-in JSON database that apps and services store data in.",
    "display": "The panel and display output: picture output, panel controls and screen settings at the hardware level.",
    "storage": "USB drives, internal storage, mounting and file system services.",
    "connection": "The connection manager: network connection state and switching between connections.",
    "update": "Firmware and software update checks, downloads and installs.  Block updates on a rooted TV before experimenting here.",
    "notifications": "Toasts, alerts and pop-ups on screen.  The friendliest place to start with luna-send.",
    "camera": "USB and built-in camera services.",
    "activity": "The activity manager: scheduled and triggered background jobs.",
    "devmode": "Developer Mode and LG's testing services.",
    "power-mgmt": "Sleep, wake and power-management timers.",
    "ui": "The compositor and system UI: surfaces, overlays and the launcher layer.",
}
MIN_METHODS = 40     # smaller categories stay in the catalog but get no page of their own

EXAMPLES = [  # task, uri, payload
    ("Show a toast message", "luna://com.webos.notification/createToast", '{"message":"Hello from luna-send"}'),
    ("Show an alert with a button", "luna://com.webos.notification/createAlert", '{"message":"Dinner is ready","buttons":[{"label":"OK"}]}'),
    ("See which app is on screen", "luna://com.webos.applicationManager/getForegroundAppInfo", "{}"),
    ("Close an app", "luna://com.webos.applicationManager/close", '{"id":"com.webos.app.browser"}'),
    ("Mute the sound", "luna://com.webos.audio/setMuted", '{"muted":true}'),
    ("Turn the volume up a step", "luna://com.webos.audio/volumeUp", "{}"),
    ("Set the volume", "luna://com.webos.audio/setVolume", '{"volume":15}'),
    ("Turn the picture off (sound keeps playing)", "luna://com.webos.service.tvpower/power/turnOffScreen", "{}"),
    ("Turn the picture back on", "luna://com.webos.service.tvpower/power/turnOnScreen", "{}"),
    ("Read the power state", "luna://com.webos.service.tvpower/power/getPowerState", "{}"),
    ("Get the model and firmware", "luna://com.webos.service.tv.systemproperty/getSystemInfo", '{"keys":["modelName","firmwareVersion","sdkVersion"]}'),
    ("Get the software version", "luna://com.webos.service.update/getCurrentSWInformation", "{}"),
    ("Check the network connection", "luna://com.webos.service.connectionmanager/getStatus", "{}"),
    ("Read the picture mode", "luna://com.webos.settingsservice/getSystemSettings", '{"category":"picture","keys":["pictureMode"]}'),
    ("List the inputs and what's connected", "luna://com.webos.service.eim/getAllInputStatus", "{}"),
    ("Read the system time", "luna://com.palm.systemservice/time/getSystemTime", "{}"),
]

def atlas_link(svc=None, m=None, cat=None):
    if cat: return f"/luna-atlas/#/?cat={cat}"
    return "/luna-atlas/#/" + svc + (("/" + m) if m else "")

def cmd(uri, payload="{}"): return f"luna-send -n 1 -f {uri} '{payload}'"

def code(c):
    return f'<div class="code"><pre><span class="pr">$ </span>{esc(c)}</pre><button class="copy" type="button" data-copy="{esc(c)}">copy</button></div>'

def head(eyebrow, h1, lead):
    return (f'<section class="doc-hero" style="--accent:{ACC}"><div class="eyebrow">{eyebrow}</div>'
            f'<h1 class="h2" style="margin-top:12px">{h1}</h1><p class="lead">{lead}</p></section>')

def badge(a, d=False):
    col = {"public": "#3ddc97", "private": "#ffb547", "ssap": "#33e1ff", "root": "#ff3ea5"}.get(a, "#7783a8")
    out = f'<span class="pill" style="--ca:{col}">{esc(a)}</span>'
    if d: out += ' <span class="pill" style="--ca:#ff3ea5">⚠ dangerous</span>'
    return out

def trunc(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"

def build():
    cat = json.load(open(os.path.join(ROOT, "luna-atlas/catalog.json")))
    total_m, total_s = cat["counts"]["methods"], cat["counts"]["services"]
    by = {}
    for s in cat["services"]:
        for m in s["methods"]:
            by.setdefault(m["c"], []).append((s, m))
    cats = sorted([c for c in by if len(by[c]) >= MIN_METHODS], key=lambda c: -len(by[c]))
    written = []

    # ---- category pages
    for c in cats:
        rows = by[c]; name = NAMES.get(c, c.title())
        svcs = {}
        for s, m in rows: svcs.setdefault(s["service"], [s, 0])[1] += 1
        svc_list = sorted(svcs.values(), key=lambda x: -x[1])
        n_doc = sum(1 for _, m in rows if m["dc"] == "documented")
        n_pub = sum(1 for _, m in rows if m["a"] == "public")
        n_dz = sum(1 for _, m in rows if m["d"])
        path = f"/luna-atlas/categories/{c}/"
        top = ", ".join(s["service"] for s, _ in svc_list[:2])
        title = f"{name} luna-send commands for LG webOS"
        desc = trunc(f"{len(rows):,} LG webOS luna-send methods for {name.lower()}, across {len(svc_list)} services like {top}, with access levels and commands to run.", 160)
        examples = [(s, m) for s, m in rows if m["dc"] == "documented" and not m["d"] and m["a"] in ("public", "ssap")][:30]
        svc_rows = "".join(
            f'<tr><td><a href="{atlas_link(s["service"])}"><code>{esc(s["service"])}</code></a></td><td>{n}</td><td>{esc(trunc(s.get("sd", ""), 140))}</td></tr>'
            for s, n in svc_list)
        ex_html = "".join(
            f'<div class="lm"><div class="lmh"><a href="{atlas_link(s["service"], m["m"])}"><b>{esc(m["m"])}</b></a> {badge(m["a"])}'
            f'<span class="dim mono" style="font-size:12px">{esc(s["service"])}</span></div>'
            f'<p>{esc(trunc(m["desc"], 220))}</p>'
            + (f'<p class="dim" style="font-size:13px">params: {", ".join("<code>" + esc(k) + "</code>" for k in list(m["p"])[:8])}</p>' if m["p"] else "")
            + code(cmd(m["u"])) + "</div>" for s, m in examples)
        body = head(f"$ luna-atlas --cat {c}", f"{esc(name)} luna-send commands.", esc(BLURB.get(c, "")) + f"  {len(rows):,} methods in {len(svc_list)} services.") + f"""
<article class="doc" style="--accent:{ACC}">
<div class="stats lstats"><div><b>{len(rows):,}</b><span>methods</span></div><div><b>{len(svc_list)}</b><span>services</span></div><div><b>{n_doc:,}</b><span>documented</span></div><div><b>{n_pub:,}</b><span>public</span></div><div><b>{n_dz}</b><span>flagged dangerous</span></div></div>
<p><a class="btn" href="{atlas_link(cat=c)}">open {esc(name)} in the catalog ↗</a></p>
<h2>Services</h2>
<div class="tblw"><table class="tbl"><thead><tr><th>service</th><th>methods</th><th>what it does</th></tr></thead><tbody>{svc_rows}</tbody></table></div>
<h2>Documented methods to start with</h2>
<p>Public and SSAP methods from LG's documentation, none flagged dangerous.  Each opens in the catalog with its full parameter table.  Run them on a rooted TV or in Developer Mode.</p>
{ex_html or '<p>No documented public methods in this category yet: see the full list in the catalog.</p>'}
<div class="callout" style="--accent:#ff3ea5;margin-top:28px"><b>Before you run anything.</b>  Methods marked dangerous can change, reset or break things on the TV.  Running one from here is exactly as safe as typing the same <code>luna-send</code> yourself.  See <a href="https://github.com/ohmybahgosh/WEBOS-LUNA-SEND-ATLAS/blob/main/docs/dangerous.md" target="_blank" rel="noopener">dangerous.md</a>.</div>
<h2>Other categories</h2>
<div class="chips lchips">{"".join(f'<a href="/luna-atlas/categories/{o}/">{esc(NAMES.get(o, o))} <span>{len(by[o]):,}</span></a>' for o in cats if o != c)}</div>
</article>"""
        ld = [article_ld(path, title, desc, {"@type": "Thing", "name": "luna-send"}),
              {"@type": "ItemList", "name": f"{name} luna-send services", "numberOfItems": len(svc_list),
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["service"]} for i, (s, _) in enumerate(svc_list[:50])]}]
        written.append(write(ROOT, path, page(path, title, desc, body, [HOME, ATLAS, CATS, (name, path)], ld=ld,
                                              og_image="/assets/og/luna-atlas.png", og_alt="Luna Atlas: every LG webOS luna-send command", menu_current="/luna-atlas/")))

    # ---- categories index
    path = "/luna-atlas/categories/"
    small = [c for c in by if c not in cats]
    cards = "".join(f'<a class="card gcard" href="/luna-atlas/categories/{c}/"><b>{esc(NAMES.get(c, c))}</b><span>{len(by[c]):,} methods · {esc(trunc(BLURB.get(c, ""), 90))}</span></a>' for c in cats)
    body = head("$ luna-atlas categories", "luna-send commands by category.",
                f"All {total_m:,} LG webOS luna-send methods across {total_s} services, grouped by what they do.  Pick one to see its services and documented commands.") + f"""
<article class="doc" style="--accent:{ACC}">
<div class="gcards">{cards}</div>
<p class="dim" style="font-size:14px">Smaller groups ({", ".join(esc(NAMES.get(c, c)) for c in small)}) are in the <a href="/luna-atlas/">full catalog</a>.  New to luna-send?  Start with the <a href="/luna-atlas/examples/">common examples</a>.</p>
</article>"""
    written.append(write(ROOT, path, page(path, "LG webOS luna-send commands by category · Luna Atlas",
        trunc(f"Browse {total_m:,} LG webOS luna-send methods by category: apps, audio, input, network, power, settings, Bluetooth, notifications and more.", 160),
        body, [HOME, ATLAS, CATS], ld=[{"@type": "CollectionPage", "name": "luna-send commands by category", "url": SITE + path}],
        og_image="/assets/og/luna-atlas.png", menu_current="/luna-atlas/")))

    # ---- examples
    idx = {m["u"]: (s, m) for s in cat["services"] for m in s["methods"]}
    rows = []
    for task, uri, payload in EXAMPLES:
        if uri not in idx: continue
        s, m = idx[uri]
        rows.append(f'<div class="lm"><div class="lmh"><b>{esc(task)}</b> {badge(m["a"], m["d"])}</div>'
                    f'<p><a href="{atlas_link(s["service"], m["m"])}"><code>{esc(uri)}</code></a>  {esc(trunc(m["desc"], 160))}</p>{code(cmd(uri, payload))}</div>')
    path = "/luna-atlas/examples/"
    body = head("$ luna-send --examples", "Common luna-send examples.",
                "Copy-and-paste luna-send commands for everyday things on an LG webOS TV: toasts, apps, volume, the screen, system info and settings.") + f"""
<article class="doc" style="--accent:{ACC}">
<h2>Before you start</h2>
<p>You need a shell on the TV: a rooted TV with SSH from the Homebrew Channel (see <a href="/guides/ssh-into-lg-tv/">SSH into a rooted LG TV</a>), or Developer Mode.  Every command below uses <code>-n 1</code> to wait for one reply and <code>-f</code> to print it formatted.  Methods marked <b>private</b> need root.</p>
{"".join(rows)}
<h2>Find more</h2>
<p>These are a handful of {total_m:,}.  <a href="/luna-atlas/">Search the full catalog</a>, or <a href="/luna-atlas/categories/">browse by category</a>.  Methods that support subscriptions keep reporting changes if you add <code>"subscribe": true</code> and drop <code>-n 1</code>.</p>
</article>"""
    written.append(write(ROOT, path, page(path, "luna-send examples for LG webOS TVs · Luna Atlas",
        "Copy-and-paste luna-send commands for LG webOS TVs: show a toast, close apps, mute, set the volume, turn the picture off, read model, firmware and settings.",
        body, [HOME, ATLAS, ("Examples", path)], ld=[article_ld(path, "Common luna-send examples for LG webOS TVs",
        "Copy-and-paste luna-send commands for everyday tasks on LG webOS TVs.")],
        og_image="/assets/og/luna-atlas.png", menu_current="/luna-atlas/")))
    return written

def sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith((".git", "node_modules")): continue
        s = open(f, encoding="utf-8").read()
        if re.search(r'name="robots" content="[^"]*noindex', s): continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not m or not m.group(1).startswith(SITE): continue
        loc = m.group(1)
        depth = loc[len(SITE):].strip("/").count("/") + (0 if loc == SITE + "/" else 1)
        pr = "1.0" if loc == SITE + "/" else "0.9" if depth == 1 else "0.7" if depth == 2 else "0.5"
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    urls.sort(key=lambda u: (u.count("/"), u))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)
    return len(urls)

if __name__ == "__main__":
    for w in build(): print("wrote", w)
    print("sitemap urls:", sitemap())

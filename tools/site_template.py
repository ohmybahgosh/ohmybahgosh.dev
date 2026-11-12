"""Shared page shell for the generated pages (guides, FAQs, install hub, Luna Atlas categories).
Matches the hand-written pages: same head, header, menu and footer."""
import html, json

SITE = "https://ohmybahgosh.dev"
CSS_V = "r2611b"
JS_V = "r2611d"

def esc(s): return html.escape(s, quote=True)

def menu(current=""):
    def a(href, icon, name, small):
        cur = ' aria-current="page"' if href == current else ""
        return (f'<a href="{href}"{cur}><img src="/assets/img/{icon}" alt="" width="40" height="40" loading="lazy">'
                f'<b>{name}</b><small>{small}</small></a>')
    return f"""<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="ohmybahgosh.dev home"><span class="px">&gt;_</span><span>ohmybahgosh<em>.dev</em></span></a>
    <nav class="nav" aria-label="Main">
      <div class="menu" data-menu>
        <button class="mbtn" type="button" aria-expanded="false" aria-controls="pmenu">projects <span class="chev" aria-hidden="true">▾</span></button>
        <div class="mpanel" id="pmenu">
        <div class="mgrp"><span>TV apps</span>
          {a("/tivibro/", "tivibro-icon.webp", "TiviBro", "IPTV player with a real guide")}
          {a("/lg-usb-2-eth0/", "eth0-icon.webp", "LG-USB-2-ETH0", "USB Ethernet as the TV's eth0")}
          {a("/webos-entware-installer/", "entware-icon.webp", "Entware", "Linux packages and add-ons")}
          {a("/ssh-doctor/", "ssh-doctor-icon.webp", "SSH Doctor", "Check and fix SSH from the TV")}
        </div>
        <div class="mgrp"><span>reference and tools</span>
          {a("/luna-atlas/", "luna-atlas-icon.webp", "Luna Atlas", "Every luna-send command")}
          {a("/pipseek/", "pipseek-icon.webp", "pipseek", "Search PyPI from your terminal")}
        </div>
        <a class="mall" href="/install/">$ install guide: root, Homebrew Channel, repo</a>
        </div>
      </div>
      <a href="/install/" class="hide-s">install</a>
      <a href="/guides/" class="hide-s">guides</a>
      <a href="/about/" class="hide-s">about</a>
      <a href="/contact/" class="hide-s">contact</a>
      <a href="https://github.com/ohmybahgosh" class="hide-s" target="_blank" rel="noopener">github ↗</a>
      <button class="kbtn theme" type="button" data-theme-toggle aria-label="Toggle light and dark theme" title="Light / dark"><span class="moon">☾</span><span class="sun">☀</span></button>
      <button class="kbtn" type="button" data-pal-open aria-label="search: open the command palette"><span class="ic-s" aria-hidden="true">⌕</span><span>search</span><kbd>⌘K</kbd></button>
    </nav>
  </div>
</header>"""

FOOTER = f"""<footer>
  <div class="wrap">
    <div>
      <div><span class="c-gr">root@ohmybahgosh</span>:<span class="c-cy">~</span># echo "made by OhMyBahGosh"</div>
      <div style="margin-top:6px">© <span data-year>2026</span> OhMyBahGosh · open-source projects · not affiliated with LG Electronics</div>
      <div style="margin-top:6px"><a data-mail="text" href="/contact/">hello at ohmybahgosh dot dev</a></div>
    </div>
    <nav aria-label="Footer">
      <a href="/">~/</a>
      <a href="/tivibro/">tivibro</a>
      <a href="/lg-usb-2-eth0/">lg-usb-2-eth0</a>
      <a href="/webos-entware-installer/">entware</a>
      <a href="/ssh-doctor/">ssh-doctor</a>
      <a href="/luna-atlas/">luna-atlas</a>
      <a href="/pipseek/">pipseek</a>
      <a href="/install/">install</a>
      <a href="/guides/">guides</a>
      <a href="/about/">about</a>
      <a href="/contact/">contact</a>
      <a href="https://github.com/ohmybahgosh" target="_blank" rel="noopener">github ↗</a>
    </nav>
  </div>
</footer>
<script src="/assets/js/site.js?v={JS_V}" defer></script>
<script data-goatcounter="https://ohmybahgosh.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""

def breadcrumbs(trail):
    """trail: [(name, path), ...] from Home to this page."""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

def crumb_html(trail):
    parts = ['<a href="/">~</a>']
    for i, (n, p) in enumerate(trail[1:]):
        last = i == len(trail) - 2
        slug = p.strip("/").split("/")[-1] or n
        parts.append("<span>/</span>")
        parts.append(f'<span class="c-gr">{esc(slug)}</span>' if last else f'<a href="{p}">{esc(slug)}</a>')
    return '<div class="crumb">' + "".join(parts) + "</div>"

def page(path, title, desc, body, trail, ld=None, body_class="p-doc", og_image="/assets/og/home.png",
         og_alt="ohmybahgosh.dev: open-source apps for rooted LG webOS TVs", robots="index,follow,max-image-preview:large",
         menu_current=""):
    assert len(desc) <= 160, (path, len(desc))
    url = SITE + path
    mod = today()
    graph = [{"@type": "WebSite", "@id": SITE + "/#website", "name": "ohmybahgosh.dev", "url": SITE + "/"}, breadcrumbs(trail)] + (ld or [])
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f"""<!doctype html>
<html lang="en" data-root="/">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#05070d">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<script>try{{var t=localStorage.getItem("omb-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preload" href="/assets/fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jetbrains-mono.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ohmybahgosh.dev">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<meta name="author" content="OhMyBahGosh">
<meta property="article:modified_time" content="{mod}">
<meta name="robots" content="{robots}">
<script type="application/ld+json">
{ldjson}
</script>
<!-- Google Analytics (GA4); ads features stay off -->
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});gtag('js',new Date());gtag('config','G-7J8VQ3FKKM');</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7J8VQ3FKKM"></script>
</head>
<body class="{body_class}">
<div class="bgfx" aria-hidden="true"></div>
{menu(menu_current)}
<main>
<div class="wrap">
{crumb_html(trail)}
{body}
</div>
</main>

{FOOTER}"""

PUBLISHED = "2026-11-09"
def today():
    import datetime; return datetime.date.today().isoformat()

def author():
    return {"@type": "Person", "@id": SITE + "/#person", "name": "OhMyBahGosh", "url": SITE + "/about/",
            "sameAs": ["https://github.com/ohmybahgosh"]}

def article_ld(path, headline, desc, about=None, image="/assets/og/home.png", published=PUBLISHED, modified=None, keywords=None):
    d = {"@type": "TechArticle", "@id": SITE + path + "#article", "headline": headline[:110], "description": desc, "url": SITE + path,
         "mainEntityOfPage": SITE + path, "image": SITE + image, "author": author(), "publisher": {"@id": SITE + "/#person"},
         "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en-US",
         "datePublished": published, "dateModified": modified or today()}
    if about: d["about"] = about
    if keywords: d["keywords"] = keywords
    return d

def faq_ld(qas):
    import re
    def plain(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qas]}

def faq_html(qas):
    return "\n".join(f'<details class="faq"><summary>{q}</summary><div>{a}</div></details>' for q, a in qas)

def write(root, path, content):
    import os
    out = os.path.join(root, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f: f.write(content)
    return out

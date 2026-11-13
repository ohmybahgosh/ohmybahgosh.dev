#!/usr/bin/env python3
"""Builds the hand-written SEO pages: /install/, /guides/ and its guides, and each app's /faq/.
Edit the content here and run:  python3 tools/build-pages.py
The Luna Atlas category pages and sitemap come from tools/build-luna-pages.py (run on every deploy)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_template import page, write, article_ld, faq_ld, faq_html, esc, SITE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = ("Home", "/")
REPO = "https://ohmybahgosh.dev/repo"

def head(eyebrow, h1, lead, accent="#33e1ff"):
    return f"""<section class="doc-hero" style="--accent:{accent}">
  <div class="eyebrow">{eyebrow}</div>
  <h1 class="h2" style="margin-top:12px">{h1}</h1>
  <p class="lead">{lead}</p>
</section>"""

def doc(inner, accent="#33e1ff"):
    return f'<article class="doc" style="--accent:{accent}">\n{inner}\n</article>'

def code(s):
    lines = "\n".join(f'<span class="pr">$ </span>{esc(l)}' if not l.startswith("#") else f'<span class="c-mu">{esc(l)}</span>' for l in s.strip().split("\n"))
    return f'<div class="code"><pre>{lines}</pre></div>'

def steps(items):
    return '<div class="steps">' + "".join(f'<div class="step"><div><h3>{t}</h3><p>{p}</p></div></div>' for t, p in items) + "</div>"

def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tb = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tblw"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'

def related(links):
    cards = "".join(f'<a class="card gcard" href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in links)
    return f'<h2>Related</h2><div class="gcards">{cards}</div>'

def callout(html, accent=None):
    st = f' style="--accent:{accent}"' if accent else ""
    return f'<div class="callout"{st}>{html}</div>'

PAGES = []
def add(path, **kw): PAGES.append((path, kw))

# =====================================================================================  install hub
INSTALL_FAQ = [
    ("Do I need a rooted TV?",
     "For LG-USB-2-ETH0, Entware and SSH Doctor, yes: they change things only root can.  TiviBro also runs in LG's Developer Mode without root, and Luna Atlas's catalog is a web page anyone can browse.  Running <code>luna-send</code> commands needs root or Developer Mode."),
    ("Can my TV still be rooted?",
     "It depends on the exact firmware, not just the model.  Check it at <a href=\"https://cani.rootmy.tv/\" target=\"_blank\" rel=\"noopener\">cani.rootmy.tv</a>.  As of November 2026, webOS 26 firmware released after October 10, 2026 can't be rooted, and a TV on patched firmware can't be rooted again, so keep firmware updates off on a rooted TV."),
    ("What is the Homebrew Channel?",
     "The open-source app store for rooted LG TVs, from the webosbrew project.  The rooting tools install it, it runs apps as root, and it can add repositories like <code>ohmybahgosh.dev/repo</code> so apps show up and update from the TV."),
    ("Will these apps void anything or change system files?",
     "None of them writes to the TV's system partitions.  They keep their files in the Homebrew Channel's folders or on app storage, and each one has a clean uninstall.  Rooting itself is your choice and your risk, as with any homebrew."),
    ("How do updates work?",
     "Once the repository is added, new versions show up in the Homebrew Channel as an update for each app.  The site rebuilds the repository from each project's GitHub releases, so an update is usually listed within minutes of a release."),
]
add("/install/",
    title="Install guide: root, Homebrew Channel and app compatibility",
    desc="How to get the ohmybahgosh.dev apps on an LG TV: check if it can be rooted, set up the Homebrew Channel, add the repo, and see which app works on which TV.",
    trail=[HOME, ("Install", "/install/")],
    og_image="/assets/og/home.png",
    ld=[article_ld("/install/", "Install guide: root, Homebrew Channel and app compatibility",
                   "Rooting status, the Homebrew Channel, adding the ohmybahgosh.dev repository and app compatibility for LG webOS TVs.",
                   keywords=["root LG TV", "webOS Homebrew Channel", "Homebrew Channel repository", "LG webOS compatibility"]),
        faq_ld(INSTALL_FAQ)],
    body=head("$ ./install --help", "Install guide.", "Everything you need to get the apps onto an LG TV: whether yours can be rooted, the Homebrew Channel, the repository, and which app works on which TV.") + doc(f"""
<nav class="toc" aria-label="On this page"><a href="#root">1. Root</a><a href="#hbc">2. Homebrew Channel</a><a href="#repo">3. Add the repo</a><a href="#compat">4. Compatibility</a><a href="#no-root">No root?</a><a href="#faq">FAQ</a></nav>

<h2 id="root">1. Check whether your TV can be rooted</h2>
<p>Three of the four TV apps need root, because they change things a normal app can't: which network port the TV uses, Linux packages on its storage, and its SSH server.  Whether a TV can be rooted depends on its exact firmware version, so look it up first at <a href="https://cani.rootmy.tv/" target="_blank" rel="noopener">cani.rootmy.tv</a>.</p>
{callout("<b>webOS 26 and current firmware.</b>  LG has been patching the holes rooting tools use.  Per the <a href=\"https://tv.slada.sk/guides/rooting-guide\" target=\"_blank\" rel=\"noopener\">EPK archive's rooting guide</a>, webOS 26 firmware released after October 10, 2026 can't be rooted, and once a TV is on patched firmware it can't be rooted again.  On a rooted TV, keep updates off: the Homebrew Channel's <b>Block system updates</b>, and LG-USB-2-ETH0's <a href=\"/lg-usb-2-eth0/#updates\">Block updates harder</a> for what that misses.", "#ff3ea5")}
<p>The common rooting tools are <a href="https://rootmy.tv" target="_blank" rel="noopener">RootMyTV</a>, <a href="https://github.com/throwaway96/faultmanager-autoroot" target="_blank" rel="noopener">faultmanager-autoroot</a> (webOS 4.0 to 4.5 and others), crashd and DejaVuln.  The <a href="https://www.webosbrew.org/pages/rooting/" target="_blank" rel="noopener">webosbrew rooting page</a> lists which one fits which firmware.</p>

<h2 id="hbc">2. The Homebrew Channel</h2>
<p>Every rooting tool above installs the <a href="https://github.com/webosbrew/webos-homebrew-channel" target="_blank" rel="noopener">webOS Homebrew Channel</a>, the open-source app store for rooted LG TVs.  It runs apps as root, turns SSH and telnet on, blocks system updates, and installs apps from repositories.  If it's on your home screen, you're ready for step 3.</p>

<h2 id="repo">3. Add the ohmybahgosh.dev repository</h2>
<p>One repository gives you all four TV apps, and each new release shows up as an update.</p>
<div class="code"><pre>{REPO}</pre></div>
{steps([("Open the Homebrew Channel's settings", "Open the Homebrew Channel and select the gear icon at the top right."),
        ("Add the repository", "Scroll to <b class=\"c-wh\">Repositories</b>, choose <b class=\"c-wh\">Add repository</b>, enter <code>https://ohmybahgosh.dev/repo</code> and confirm."),
        ("Install the apps", "Go back to the app list.  TiviBro, LG-USB-2-ETH0, Entware and SSH Doctor are there: install the ones you want.")])}
<p>More detail, and how to remove a repository, in <a href="/guides/homebrew-channel-repository/">How to add a repository to the Homebrew Channel</a>.</p>

<h2 id="compat">4. Which app works on which TV</h2>
{table(["app", "needs", "webOS", "notes"], [
    ['<a href="/tivibro/">TiviBro</a>', "Developer Mode or root", "4 and newer", "Tested from a 2019 webOS 4 OLED to webOS 25.  Also in its own repo, <code>tivibro.app/repo</code>."],
    ['<a href="/lg-usb-2-eth0/">LG-USB-2-ETH0</a>', "root + Homebrew Channel", "every rooted webOS", "Reports from webOS 3.5 to 26.  Whether an adapter works depends on its chip and your kernel's drivers."],
    ['<a href="/webos-entware-installer/">Entware</a>', "root + Homebrew Channel", "23 to 25 tested, 4 and up", "64-bit (aarch64) and 32-bit (armv7) kernels.  About 50 MB free."],
    ['<a href="/ssh-doctor/">SSH Doctor</a>', "root + Homebrew Channel", "every rooted webOS", "Runs through the Homebrew Channel, so it works when SSH doesn't."],
    ['<a href="/luna-atlas/">Luna Atlas</a>', "nothing to browse", "any", "The catalog is a web page.  Running commands needs root or Developer Mode."],
])}

<h2 id="no-root">No root?</h2>
<p>LG's own <a href="https://webostv.developer.lge.com/develop/getting-started/developer-mode-app" target="_blank" rel="noopener">Developer Mode</a> can install apps on any webOS TV, without root.  TiviBro works that way: its <a href="https://tivibro.app" target="_blank" rel="noopener">install guide on tivibro.app</a> covers it.  Developer Mode sessions expire and need renewing, and the three tools that change the system still need root.</p>

<h2 id="faq">FAQ</h2>
{faq_html(INSTALL_FAQ)}

{related([("/guides/", "All guides", "How-tos for rooted LG TVs"),
          ("/guides/ssh-into-lg-tv/", "SSH into a rooted LG TV", "Log in, add a key, fix common errors"),
          ("/guides/lg-tv-ethernet-100mbps/", "LG TV Ethernet stuck at 100 Mbps", "Why, and how to go faster")])}
"""))

# =====================================================================================  guides
GUIDES = []
def guide(slug, title, desc, card, h1, lead, body, faq=None, accent="#33e1ff", about=None, og="/assets/og/home.png", keywords=None):
    path = f"/guides/{slug}/"
    GUIDES.append((path, card[0], card[1]))
    ld = [article_ld(path, title, desc, about, image=og, keywords=keywords)]
    if faq: ld.append(faq_ld(faq))
    full = head("$ cat guides/" + slug + ".md", h1, lead, accent) + doc(body + (f'<h2 id="faq">FAQ</h2>\n{faq_html(faq)}' if faq else ""), accent)
    add(path, title=title, desc=desc, trail=[HOME, ("Guides", "/guides/"), (card[0], path)], ld=ld, body=full, og_image=og)

# --- 1. 100 Mbps
ETH_FAQ = [
    ("Is the LG TV Ethernet port really only 100 Mbit/s?",
     "On LG's TVs, yes: the built-in port is Fast Ethernet, 100 Mbit/s, which works out to about 95 Mbit/s of real traffic.  A faster router, switch or cable won't change that.  The TV's settings may still say the link is connected at 100."),
    ("Will a gigabit or 2.5G USB adapter give me gigabit?",
     "No.  Most LG TVs only have USB 2.0 ports, which top out around 300 Mbit/s in practice.  That's still about three times the built-in port.  On a TV with a USB 3.0 port (usually the blue one), use that for more."),
    ("Can I just plug in a USB Ethernet adapter without root?",
     "The TV may see it, but webOS calls it <code>eth1</code>.  The settings then show no wired connection, and some streaming apps, like Paramount+, refuse to play over it.  Making the adapter the TV's <code>eth0</code> needs root, which is what LG-USB-2-ETH0 does."),
    ("Is Wi-Fi faster than the wired port?",
     "Often, on a good Wi-Fi 5 or Wi-Fi 6 connection close to the router.  It's less steady than a cable, though, and that's what causes buffering on high-bitrate streams.  Test both with the same file or speed test."),
    ("Why does Plex or Jellyfin buffer on my LG TV over Ethernet?",
     "Often it's the 100 Mbit/s port: a 4K remux can peak above what it carries, even when the file plays fine elsewhere.  Check the file's bitrate against 95 Mbit/s.  Wi-Fi with a strong signal, or a USB adapter as <code>eth0</code> on a rooted TV, gives it room."),
    ("What needs more than 100 Mbit/s?",
     "4K Blu-ray remuxes from Plex, Jellyfin or a local server, which can peak well above 100 Mbit/s, and game streaming like Moonlight at high bitrates.  Regular streaming apps use far less."),
]
guide("lg-tv-ethernet-100mbps",
      title="LG TV Ethernet port speed: why it's 100 Mbps, how to go faster",
      keywords=["lg tv ethernet port speed", "lg tv only 100mbps", "lg tv ethernet speed slow", "lg tv ethernet vs wifi", "lg tv gigabit ethernet usb"],
      desc="LG TVs' built-in Ethernet port tops out at 100 Mbit/s.  Why it happens, what Wi-Fi and USB adapters can do, and how rooted TVs get about 300 Mbit/s wired.",
      card=("LG TV Ethernet stuck at 100 Mbps", "Why the wired port is slow, and how to get about three times faster"),
      h1="LG TV Ethernet stuck at 100 Mbps?",
      lead="It isn't your cable or your router.  LG builds its TVs' wired port as 100 Mbit/s Ethernet.  Here's what that means, and the ways around it.",
      accent="#3ddc97", og="/assets/og/lg-usb-2-eth0.png",
      about={"@type": "Thing", "name": "LG webOS TV Ethernet speed"},
      faq=ETH_FAQ, body=f"""
{callout("<b>Short answer.</b>  The built-in port is 100 Mbit/s, about 95 in practice.  On a rooted TV, a USB Ethernet adapter made into the TV's <code>eth0</code> with <a href=\"/lg-usb-2-eth0/\">LG-USB-2-ETH0</a> gets about 250 to 330 Mbit/s over USB 2.0, and settings and streaming apps treat it as the real wired connection.", "#3ddc97")}

<h2>Why it's 100 Mbit/s</h2>
<p>LG's TVs use a Fast Ethernet controller for the wired port: 100 Mbit/s, with real throughput around 95.  It's a hardware limit, so a gigabit switch, a new Cat6 cable or a faster internet plan won't move it.  For most streaming apps that's plenty.  It isn't for high-bitrate local files: 4K Blu-ray remuxes over Plex or Jellyfin, and game streaming with Moonlight, can stutter or buffer.</p>

<h2>Every model, the C2, C4 and G4 included</h2>
<p>This isn't one model's quirk.  Measured on TVs from a 2020 UN7300 to a 2024 G4 and a 2026 G6, the built-in port lands at about 95 Mbit/s.  Look up your model's Ethernet port speed and you'll find the same answer: 100 Mbit/s.</p>

<h2>Your options</h2>
<h3>1. Wi-Fi</h3>
<p><b class="c-wh">Ethernet vs Wi-Fi on an LG TV:</b> on a strong Wi-Fi 5 or Wi-Fi 6 signal, the TV's Wi-Fi can beat the wired port on paper.  It's also less steady, and steadiness is what high-bitrate playback needs.  Worth a test, especially with the router in the same room.</p>
<h3>2. A USB Ethernet adapter, on a stock TV</h3>
<p>Plug one in and the TV may detect it, but webOS names it <code>eth1</code>.  The TV's settings then show "Not Connected", and some apps, like Paramount+, refuse to play over it.  Without root there's no way to change that.</p>
<h3>3. A USB Ethernet adapter as eth0, on a rooted TV</h3>
<p><a href="/lg-usb-2-eth0/">LG-USB-2-ETH0</a> makes the adapter the TV's <code>eth0</code>, the name webOS and its apps expect, and parks the built-in port as <code>eth2</code>.  Settings show the wired connection and apps play over the faster link.  It runs at every boot, follows the adapter being plugged and unplugged, can keep Wi-Fi as a backup, and undoes cleanly.  Where your kernel's driver for the adapter is missing or slow, it can find, check and load one built for your exact kernel.</p>

<h2>Real speeds</h2>
<p>Measured on real TVs, mostly over USB 2.0 ports:</p>
{table(["setup", "speed"], [
    ["Built-in port, any model", "about 95 Mbit/s"],
    ["RTL8153 adapter, generic <code>cdc_ncm</code> driver (2024 C4)", "200 to 255 Mbit/s, with drops"],
    ["Same adapter with a Realtek <code>r8152</code> driver", "290 to 330 Mbit/s"],
    ["RTL8156 on a 2022 C2, webOS 25", "272 down, 287 up"],
    ["RTL8153 on a 2024 G4, webOS 24", "293 down, 285 up"],
    ["ASIX AX88179 on a 2020 UN7300, webOS 5", "228 down, 325 up"],
    ["RTL8153 on a 2026 G6, webOS 26", "247 down, 312 up"],
])}
<p>USB 2.0 is the ceiling, at around 300 Mbit/s.  Still about three times the built-in port, and plenty for 4K remuxes.  Sources and more results are on the <a href="/lg-usb-2-eth0/">LG-USB-2-ETH0 page</a>.</p>

<h2>What you need</h2>
<ul>
<li>A rooted LG TV with the Homebrew Channel: see the <a href="/install/">install guide</a>.</li>
<li>A USB Ethernet adapter with a chip your TV has a driver for: see <a href="/guides/usb-ethernet-adapter-lg-tv/">which adapter to buy</a>.</li>
<li>Wi-Fi connected while you set it up, as a way back in while the ports switch over.</li>
</ul>
<p>Then add <code>{REPO}</code> to the Homebrew Channel, install LG-USB-2-ETH0 and choose <b class="c-wh">Run at every boot</b>.</p>

<h2>Check the link isn't 100 Mbit/s too</h2>
<p>If the adapter also shows 100 Mbit/s, it's usually the cable: flat and older cables often carry only two of their four wire pairs.  Try a Cat5e or better cable, or another port on the router or switch.  LG-USB-2-ETH0's status screen flags a 100 Mbit/s link.</p>
{related([("/guides/usb-ethernet-adapter-lg-tv/", "Best USB Ethernet adapters for LG TVs", "Chips that work, and ones to skip"),
          ("/lg-usb-2-eth0/", "LG-USB-2-ETH0", "The app and script"),
          ("/lg-usb-2-eth0/faq/", "LG-USB-2-ETH0 FAQ", "Updates, Wi-Fi, wake-on-LAN and more")])}
""")

# --- 2. adapters
ADP_FAQ = [
    ("Does the brand matter?",
     "Less than the chip.  The TV needs a driver for the adapter's chip, and that depends on its kernel.  Realtek RTL8153 or RTL8156 and ASIX AX88179 are the safe picks."),
    ("Should I buy a 2.5G adapter?",
     "Only if your TV has a USB 3.0 port.  On a USB 2.0 port, which many LG TVs have, a gigabit adapter does about as well for less.  Both land around 300 Mbit/s."),
    ("How do I know which chip an adapter has?",
     "Check the maker's datasheet or reviews, since many listings don't say.  On the TV, <code>lsusb</code> shows the ID: <code>0bda:8153</code> is Realtek RTL8153, <code>0bda:8156</code> is RTL8156, and <code>0b95:1790</code> is ASIX AX88179."),
    ("Which adapter for an LG C2, C4 or G4?",
     "All three have a Realtek or ASIX driver to use.  Tested: an RTL8156 2.5G adapter on a C2, a TP-Link UE306 (AX88179) on a C4, and RTL8153 and AX88179 adapters on G4s.  Their ports run at USB 2.0 speed, so a gigabit adapter does as well as a 2.5G one."),
    ("My adapter isn't detected.  Now what?",
     "The kernel probably has no driver for its chip.  LG-USB-2-ETH0's <code>status</code> lists adapters the kernel sees without a driver, <code>get-driver</code> offers a driver built for your kernel when one is known, and <code>test-driver</code> one waiting for testers."),
]
guide("usb-ethernet-adapter-lg-tv",
      title="USB Ethernet adapter for LG TV: what works (C2, C4, G4 and more)",
      keywords=["usb ethernet adapter lg tv", "lg tv usb ethernet adapter not working", "lg c2 usb ethernet adapter", "lg c4 usb ethernet adapter", "lg g4 usb ethernet adapter"],
      desc="Which USB Ethernet adapters work on LG webOS TVs: the chips with drivers (Realtek RTL8153, RTL8156, ASIX AX88179), ones to skip, and tested models.",
      card=("Best USB Ethernet adapters for LG TVs", "The chips with drivers, the ones to skip, and tested models"),
      h1="Which USB Ethernet adapter for an LG TV?",
      lead="Buy by chip, not by brand.  An adapter only works if the TV's kernel has a driver for its chip, and LG's kernels vary by model and firmware.",
      accent="#3ddc97", og="/assets/og/lg-usb-2-eth0.png", faq=ADP_FAQ, body=f"""
{callout("<b>Safe picks.</b>  A gigabit adapter with a <b>Realtek RTL8153</b> or <b>ASIX AX88179</b> chip.  A <b>Realtek RTL8156</b> 2.5G adapter is fine too, but on a USB 2.0 port it's no faster.", "#3ddc97")}

<h2>The chips</h2>
{table(["chip", "on LG TVs"], [
    ["<b>Realtek RTL8153</b> (gigabit), <code>0bda:8153</code>", "The most common.  Many kernels have Realtek's <code>r8152</code> built in.  Newer ones may only have the slower generic <code>cdc_ncm</code> driver, and a few none at all, where a driver built for that kernel can be loaded."],
    ["<b>Realtek RTL8156</b> (2.5G), <code>0bda:8156</code>", "Works on <code>cdc_ncm</code> out of the box, and faster with Realtek's newer <code>r8152_oot</code> driver where one is built for your kernel."],
    ["<b>ASIX AX88179</b> (gigabit), <code>0b95:1790</code>", "Works out of the box on many TVs with the kernel's own <code>ax88179_178a</code> driver.  Where it's missing, there's often one to get or test."],
    ["ASIX AX88179A, AX88772D", "Skip for now: newer chips older TV kernels may not handle, and untested on a TV."],
    ["Aquantia AQC111/112, Davicom DM9601, Microchip LAN78xx", "No LG kernel includes these drivers.  Builds are waiting for testers, but a Realtek or ASIX adapter is the safer buy."],
])}

<h2>Tested on real TVs</h2>
{table(["adapter", "chip", "TV", "result"], [
    ["UGREEN USB-C to 2.5G", "RTL8156BG", "2022 C2, webOS 25", "272 down, 287 up with <code>r8152_oot</code>"],
    ["TP-Link UE306", "AX88179", "2020 UN7300, webOS 5", "228 down, 325 up with a driver from <code>get-driver</code>"],
    ["TP-Link UE306", "AX88179", "2024 C4", "about 300, out of the box"],
    ["RTL8153 adapter", "RTL8153", "2024 G4, webOS 24", "293 down, 285 up"],
    ["Cable Matters USB Ethernet", "RTL8153", "2020 UN7300, webOS 5", "184 down, 229 up with a driver from <code>get-driver</code>"],
    ["ASIX AX88179 adapter", "AX88179", "2024 G4, webOS 25", "292 down, 51 up"],
    ["RTL8153 adapter", "RTL8153", "2026 G6, webOS 26", "247 down, 312 up"],
])}
<p>More models that use the same chips, with plain links and no affiliate codes, are in the <a href="https://github.com/ohmybahgosh/LG-USB-2-ETH0#choosing-an-adapter" target="_blank" rel="noopener">LG-USB-2-ETH0 README</a>.  Sellers sometimes change parts without changing the listing, so check the chip before you buy.</p>

<h2 id="not-working">USB Ethernet adapter not working on an LG TV?</h2>
<p>Three causes cover almost every case:</p>
<ul>
<li><b class="c-wh">It's working, but as eth1.</b>  The adapter has a link and an address, yet settings say "Not Connected" and some apps won't play.  webOS only treats <code>eth0</code> as the wired connection.  On a rooted TV, <a href="/lg-usb-2-eth0/">LG-USB-2-ETH0</a> fixes the name.</li>
<li><b class="c-wh">No driver for its chip.</b>  The adapter isn't detected at all, because the kernel on your model and firmware has no driver for that chip.  LG-USB-2-ETH0's <code>status</code> shows adapters the kernel sees without a driver, and <code>get-driver</code> offers one built for your kernel when one exists.</li>
<li><b class="c-wh">The slow generic driver.</b>  A Realtek adapter on <code>cdc_ncm</code> works but drops and tops out lower.  Realtek mode moves it to the TV's own <code>r8152</code> where the kernel has one.</li>
</ul>

<h2>USB 2.0 vs USB 3.0</h2>
<p>Many LG TVs, the C2 included, only have USB 2.0 ports.  There every adapter tops out around 300 Mbit/s, about three times the built-in port.  If your TV has a USB 3.0 port (usually the blue one), plug into that.  A USB-C adapter needs a USB-C to USB-A converter on most LG TVs, and those are usually USB 2.0.</p>

<h2>Check before you buy</h2>
<p>On a rooted TV, LG-USB-2-ETH0's <code>status</code> lists which USB network drivers your kernel has.  Its <a href="https://github.com/ohmybahgosh/LG-USB-2-ETH0/blob/main/docs/firmware-audit.md" target="_blank" rel="noopener">firmware audit</a> lists them model by model, read straight from LG's firmware.</p>
{related([("/guides/lg-tv-ethernet-100mbps/", "LG TV Ethernet stuck at 100 Mbps", "Why, and how to go faster"),
          ("/lg-usb-2-eth0/", "LG-USB-2-ETH0", "Make the adapter the TV's eth0"),
          ("/install/", "Install guide", "Root, Homebrew Channel, repo")])}
""")

# --- 3. SSH
SSH_FAQ = [
    ("What's the default SSH login for a rooted LG TV?",
     "User <code>root</code>, port 22, password <code>alpine</code>, once SSH is turned on in the Homebrew Channel.  Adding your first key turns the <code>alpine</code> password off at the next boot."),
    ("Why does SSH say Connection refused?",
     "The SSH server isn't running or listening on that port.  Turn on SSH in the Homebrew Channel's settings and restart the TV, or use SSH Doctor's <b>Turn SSH on now</b>, which starts it without a restart."),
    ("I added a key and now the password doesn't work.",
     "That's by design: the first key in <code>authorized_keys</code> turns <code>alpine</code> off at the next boot.  If the key itself doesn't work, often because of Windows line endings or a key pasted on several lines, SSH Doctor's <b>Fix my keys file</b> or <b>Go back to password login</b> gets you back in."),
    ("Is Developer Mode SSH the same thing?",
     "No.  Developer Mode runs its own SSH on port 9922, for LG's developer tools, with a key and passphrase from the Developer Mode app.  The Homebrew Channel's SSH is root on port 22."),
    ("How do I copy files to the TV?",
     "Over SFTP.  WinSCP, FileZilla and Cyberduck work with the Homebrew Channel's <code>sftp-server</code>, using the same login as SSH."),
]
guide("ssh-into-lg-tv",
      title="LG TV SSH: default password, setup and common errors",
      keywords=["lg tv ssh password", "webos ssh default password", "webos ssh connection refused", "lg tv developer mode ssh", "ssh into lg webos tv"],
      desc="Turn on SSH on a rooted LG TV, log in as root, add a key, copy files over SFTP, and fix Connection refused, Permission denied and host key errors.",
      card=("SSH into a rooted LG TV", "Log in, add a key, copy files, and fix the common errors"),
      h1="SSH into a rooted LG TV.",
      lead="How to turn SSH on, log in as root, switch to a key, copy files, and get back in when it breaks.",
      accent="#3ddc97", og="/assets/og/ssh-doctor.png", faq=SSH_FAQ, body=f"""
<h2>1. Turn SSH on</h2>
<p>You need a rooted TV with the <a href="/install/">Homebrew Channel</a>.  Open it, select the gear icon, turn on <b class="c-wh">SSH Server</b>, and restart the TV.  While you're there, keeping <b class="c-wh">Telnet</b> on too gives you a way back in if SSH ever breaks.</p>

<h2>2. Log in</h2>
<p>Find the TV's IP address in its network settings, then from a computer on the same network:</p>
{code("ssh root@192.168.1.50")}
<p><b class="c-wh">The webOS SSH default password:</b> user <code>root</code>, port 22, password <code>alpine</code>.  On Windows, the built-in <code>ssh</code> in PowerShell or Windows Terminal works the same, or use PuTTY.</p>

<h2>3. Switch to a key</h2>
<p>Keys go in <code>/home/root/.ssh/authorized_keys</code>, one per line.  The first key you add turns password login off at the next boot, so check the key works before you restart.  The common ways this goes wrong: Windows line endings in the file, a key wrapped across lines, a private key pasted instead of the <code>.pub</code> half, or the wrong owner or permissions.</p>
<p><a href="/ssh-doctor/">SSH Doctor</a> skips all of that: on the TV, choose <b class="c-wh">Set up a key</b>, scan the QR code or open the address on your computer or phone, enter the short pairing code, and upload a key or let the browser make one.  It also gives you a ready-made <code>~/.ssh/config</code> entry, so <code>ssh lgtv</code> just works.</p>

<h2 id="devmode">Developer Mode SSH is different</h2>
<p>LG's Developer Mode runs its own SSH server on port 9922, as user <code>prisoner</code>, with a key and passphrase the Developer Mode app gives you.  It's meant for LG's developer tools (<code>ares</code> and webOS Dev Manager), it isn't root, and it can't change the system.  Everything else on this page is the Homebrew Channel's root SSH on a rooted TV.</p>

<h2>4. Copy files</h2>
<p>SFTP uses the same login.  WinSCP, FileZilla and Cyberduck work with the Homebrew Channel's <code>sftp-server</code>, or from a terminal:</p>
{code("scp movie.mkv root@192.168.1.50:/media/internal/")}

<h2>When it breaks</h2>
{table(["error", "what it usually means"], [
    ["<code>Connection refused</code>", "SSH is off, didn't start, or something else took port 22."],
    ["<code>Permission denied (publickey)</code>", "A key was added, so <code>alpine</code> is off, and the key doesn't match or the keys file is broken."],
    ["<code>No supported authentication methods available</code> (PuTTY)", "The same, seen from PuTTY."],
    ["<code>REMOTE HOST IDENTIFICATION HAS CHANGED</code>", "The TV's host key changed, usually after a reset.  Check its fingerprint, then remove the old line from <code>known_hosts</code>."],
    ["<code>no matching host key type found</code>", "A newer SSH client refusing the TV's older key type."],
])}
<p>None of these needs a factory reset.  <a href="/ssh-doctor/">SSH Doctor</a> runs through the Homebrew Channel rather than over SSH, so it works even when SSH is completely broken: it shows which of these it is, in plain words, and fixes it with one button, with a backup and an undo.</p>
{related([("/ssh-doctor/", "SSH Doctor", "Check and fix SSH from the TV"),
          ("/ssh-doctor/faq/", "SSH Doctor FAQ", "Passwords, ports, keys only"),
          ("/webos-entware-installer/", "Entware", "A bash shell and Linux packages")])}
""")

# --- 4. repo
REPO_FAQ = [
    ("What is a Homebrew Channel repository?",
     "A web address that serves a list of apps with their versions and download links.  The Homebrew Channel reads it, shows those apps in its list, and offers updates when the list changes."),
    ("Is it safe to add a repository?",
     "Apps from it run as root, so only add ones you trust.  Every app in <code>ohmybahgosh.dev/repo</code> is open source, built from its GitHub releases, and checked by SHA-256 when it downloads."),
    ("Which apps does ohmybahgosh.dev/repo add?",
     "TiviBro, LG-USB-2-ETH0, Entware and SSH Doctor."),
    ("How do I remove a repository?",
     "In the Homebrew Channel's settings, under Repositories, select it and remove it.  Apps you already installed stay installed."),
]
guide("homebrew-channel-repository",
      title="Homebrew Channel on LG TV: install it and add a repository",
      keywords=["homebrew channel lg tv", "install homebrew channel lg tv", "homebrew channel lg repository", "webos homebrew ipk"],
      desc="Add a repository to the webOS Homebrew Channel on a rooted LG TV, step by step, plus what a repository is, how updates work and how to remove one.",
      card=("Add a Homebrew Channel repository", "Step by step, with updates and removal"),
      h1="Add a repository to the Homebrew Channel.",
      lead="Repositories are how apps that aren't in the default list get onto a rooted LG TV, and how they update from the TV.",
      faq=REPO_FAQ, body=f"""
<h2 id="install-hbc">Installing the Homebrew Channel</h2>
<p>The Homebrew Channel isn't in LG's store.  The rooting tool installs it: <a href="https://rootmy.tv" target="_blank" rel="noopener">RootMyTV</a>, faultmanager-autoroot, crashd or DejaVuln, depending on your firmware.  Check yours at <a href="https://cani.rootmy.tv/" target="_blank" rel="noopener">cani.rootmy.tv</a>, and see <a href="/guides/root-lg-tv-2026/">rooting an LG TV in 2026</a>.</p>

<h2>Add a repository: steps</h2>
{steps([("Open the settings", "Open the Homebrew Channel on the TV and select the gear icon at the top right."),
        ("Add the repository", "Scroll to <b class=\"c-wh\">Repositories</b> and choose <b class=\"c-wh\">Add repository</b>.  Type the address, for example <code>https://ohmybahgosh.dev/repo</code>, and confirm."),
        ("Find the apps", "Go back to the app list.  The repository's apps are listed with the rest: open one and choose <b class=\"c-wh\">Install</b>."),
        ("Updates", "New versions show up as an update on the app's page in the Homebrew Channel.")])}

<h2>Repositories worth adding</h2>
{table(["address", "what's in it"], [
    ["<code>https://ohmybahgosh.dev/repo</code>", "TiviBro, LG-USB-2-ETH0, Entware and SSH Doctor"],
    ["<code>https://tivibro.app/repo</code>", "TiviBro on its own"],
    ["<code>https://tivibro.app/testing</code>", "Every TiviBro test build as soon as it's out"],
])}

<h2>Typing it with the remote</h2>
<p>The on-screen keyboard is slow, so type carefully: <code>https://</code> included, no trailing spaces.  If the app list doesn't change, check the TV is online and the address has no typos, then reopen the Homebrew Channel.</p>

<h2>Prefer the command line?</h2>
<p>Every app here can also be installed over SSH: see each app's page.  TiviBro, for example, installs with one line on a rooted TV:</p>
{code("curl -fsSL https://tivibro.app/install | sh")}
{related([("/install/", "Install guide", "Root, Homebrew Channel and compatibility"),
          ("/guides/ssh-into-lg-tv/", "SSH into a rooted LG TV", "For installs from the command line"),
          ("/#homebrew", "The repository", "What's in ohmybahgosh.dev/repo")])}
""")

# --- 5. IPTV
IPTV_FAQ = [
    ("Is TiviMate available on LG TVs?",
     "No.  TiviMate is an Android app, for Android TV and Fire TV.  LG TVs run webOS, so it doesn't install there."),
    ("What is TiviBro?",
     "A free, open-source IPTV player for LG webOS TVs, built in the style of TiviMate: the guide is the home screen.  It plays your own Xtream Codes, M3U or Stalker portal subscription.  It doesn't come with channels."),
    ("Do I need a rooted TV for TiviBro?",
     "No.  It installs in LG's Developer Mode too.  On a rooted TV, the Homebrew Channel installs and updates it from the TV."),
    ("Is TiviBro free?",
     "Yes, every feature, MIT licensed, with no account, ads or tracking.  It counts installs by version once a day, anonymously, and that can be switched off."),
    ("Which LG TVs does TiviBro run on?",
     "webOS 4 and newer.  It's tested every day on real TVs from a 2019 webOS 4 OLED to webOS 25.  It's in alpha testing, so expect some rough edges."),
]
guide("iptv-player-lg-tv",
      title="TiviMate for LG TV? The free webOS alternative with a real guide",
      keywords=["tivimate for lg tv", "tivimate alternative for lg webos", "best iptv player lg tv", "lg webos iptv player free", "xtream iptv lg tv", "m3u player lg tv"],
      desc="TiviMate doesn't run on LG webOS TVs.  TiviBro is a free, open-source IPTV player for webOS 4 and newer with a TiviMate-style guide, catch-up and a web editor.",
      card=("An IPTV player for LG TVs", "Looking for TiviMate on webOS? Here's the alternative"),
      h1="Looking for TiviMate on an LG TV?",
      lead="TiviMate is Android-only, so it won't install on webOS.  TiviBro is a free, open-source IPTV player built for LG TVs, with the same guide-first layout.",
      accent="#5b8cff", og="/assets/og/tivibro.png", faq=IPTV_FAQ,
      about={"@type": "SoftwareApplication", "name": "TiviBro", "url": "https://tivibro.app", "operatingSystem": "LG webOS"}, body=f"""
{callout("<b>TiviBro's home is <a href=\"https://tivibro.app\" target=\"_blank\" rel=\"noopener\">tivibro.app</a>.</b>  Install steps, the full feature list, the Android phone app and the user guide are all there.  This page is the short version.", "#5b8cff")}

<h2>What it does</h2>
<ul>
<li><b class="c-wh">Guide first.</b>  Live preview top left, details top right, groups one press away.  OK previews, OK again goes fullscreen.</li>
<li><b class="c-wh">Your own subscription.</b>  An Xtream Codes IPTV login, or an M3U playlist with an XMLTV guide.  Paste your provider's whole link and it fills in the rest.</li>
<li><b class="c-wh">Set up from your phone.</b>  Scan the QR code on the first screen and type your login with a real keyboard.</li>
<li><b class="c-wh">Catch-up, movies and shows, search.</b>  Rewind the guide, your provider's VOD with posters and resume, and one search across everything.</li>
<li><b class="c-wh">Sports and PPV, readable.</b>  Events crammed into channel names show with the game in the guide at its real time.  <b class="c-wh">My teams</b> gathers your teams' games from every channel.</li>
<li><b class="c-wh">A web editor and an Android app.</b>  Clean up thousands of channels from any browser, with drafts and undo.  The phone app is a remote that can also play channels on the TV and turn it on.</li>
</ul>

<h2>TiviBro and TiviMate</h2>
{table(["", "TiviBro", "TiviMate"], [
    ["Runs on LG webOS TVs", "Yes", "No, Android TV and Fire TV"],
    ["Price", "Free, every feature", "Free version, Premium paid"],
    ["Open source", "Yes, MIT", "No"],
    ["Edit your playlist from a computer", "Yes, with autosaved drafts", "On the TV only"],
    ["Set up by scanning a QR code", "Yes", "Type it with the remote"],
    ["Recording", "Not yet", "Premium"],
])}
<p class="dim" style="font-size:14px">TiviMate column from its own site and public guides, October 2026.  TiviMate is a great app; this is what TiviBro adds on an LG TV.</p>

<h2>Install</h2>
<p>On a rooted TV, add <code>https://tivibro.app/repo</code> (or <code>{REPO}</code>) to the Homebrew Channel and install it from the app list.  Without root, use LG's Developer Mode.  Both are covered on <a href="https://tivibro.app" target="_blank" rel="noopener">tivibro.app</a>.</p>
{related([("https://tivibro.app", "tivibro.app", "TiviBro's own site and install guide"),
          ("/tivibro/", "TiviBro project page", "Source, builds and releases"),
          ("/tivibro/faq/", "TiviBro FAQ", "Root, providers, backups, privacy")])}
""")

# --- 6. root in 2026
ROOT_FAQ = [
    ("Can you still root an LG TV in 2026?",
     "Some, yes.  It depends on the exact firmware, not just the model or year.  Check yours at <a href=\"https://cani.rootmy.tv/\" target=\"_blank\" rel=\"noopener\">cani.rootmy.tv</a>.  webOS 26 firmware released after October 10, 2026 is patched, and so is most current firmware on older models."),
    ("Can webOS 26 be rooted?",
     "Only on webOS 26 firmware released before October 10, 2026, per the EPK archive's rooting guide.  The table on this page lists which builds for which models."),
    ("If my TV updates to patched firmware, can I root it again?",
     "No.  Once it's on patched firmware there's no known way back in, so on a rooted TV, keep updates blocked."),
    ("Does rooting void the warranty?",
     "That's between you and LG, and it can vary by country.  Rooting changes the TV's software, it's done at your own risk, and nothing on this site can undo LG's terms."),
    ("What do I get from rooting?",
     "The Homebrew Channel, SSH as root, and apps that need it: a faster wired connection with LG-USB-2-ETH0, Linux packages and add-ons with Entware, and SSH Doctor.  TiviBro runs without root."),
]
guide("root-lg-tv-2026",
      title="Can you root an LG TV in 2026? webOS 26 status by model",
      desc="Which LG TVs can still be rooted in 2026: the webOS 26 cutoff, rootable firmware by model, the tools, and how to keep a rooted TV from updating.",
      card=("Rooting an LG TV in 2026", "The webOS 26 cutoff and which firmware still works"),
      h1="Rooting an LG TV in 2026.",
      lead="Whether an LG TV can be rooted comes down to its exact firmware build.  Here's where things stand, model by model, as of November 2026.",
      accent="#ff3ea5", keywords=["root lg tv 2026", "webos 26 root", "lg tv root check", "root lg tv webos 25", "can i root my tv lg"],
      faq=ROOT_FAQ, body=f"""
{callout("<b>Check your exact firmware first</b> at <a href=\"https://cani.rootmy.tv/\" target=\"_blank\" rel=\"noopener\">cani.rootmy.tv</a> (Settings, then Support, then Software Update shows the version).  And if your TV is rootable today, turn off automatic updates now: one update can close the door for good.", "#ff3ea5")}

<h2>The short version</h2>
<ul>
<li>webOS 26 firmware released <b class="c-wh">before October 10, 2026</b> can still be rooted.  Later builds can't, per the <a href="https://tv.slada.sk/guides/rooting-guide" target="_blank" rel="noopener">EPK archive's rooting guide</a>.</li>
<li>Older TVs on older firmware are often rootable with RootMyTV, faultmanager-autoroot (webOS 4.0 to 4.5), crashd or DejaVuln.  The <a href="https://www.webosbrew.org/pages/rooting/" target="_blank" rel="noopener">webosbrew rooting page</a> matches tool to firmware.</li>
<li>Once a TV is on patched firmware, it can't be rooted again.</li>
</ul>

<h2>webOS 26, model by model</h2>
{table(["TVs", "webOS 26 firmware that can still be rooted"], [
    ["2022 to 2025 OLEDs with LG's own chips (C2, C3, C4, C5, G4, G5 and more)", "43.21.71, 43.21.73, 43.21.74 and 43.21.77 (August and September 2026).  43.21.84, 43.21.94 and 43.21.96 are patched."],
    ["2026 OLEDs (C6, G6)", "Launch firmware 43.02 to 43.11, and 43.21.60 to 43.21.69"],
    ["2026 B6", "43.21.45 to 43.21.59 (August and September 2026).  43.21.88 is patched."],
    ["2026 QNED7S", "None known"],
    ["2024 B4 and 2025 B5", "None yet"],
    ["2024 LCDs with the K8LpN2 chip (UT81, QNED80T)", "43.22.13 (September 2026)"],
])}
<p class="dim" style="font-size:14px">From LG-USB-2-ETH0's <a href="https://github.com/ohmybahgosh/LG-USB-2-ETH0#webos-compatibility" target="_blank" rel="noopener">webOS compatibility notes</a>, which track the EPK archive.  Firmware moves fast: confirm at cani.rootmy.tv before you start.</p>

<h2>After rooting</h2>
<ol>
<li><b class="c-wh">Block updates.</b>  Turn on the Homebrew Channel's <b>Block system updates</b>, and see <a href="/guides/block-lg-tv-updates/">how to block LG TV updates</a> for what it misses.</li>
<li><b class="c-wh">Add the repository</b> <code>{REPO}</code>: see the <a href="/install/">install guide</a>.</li>
<li><b class="c-wh">Turn on SSH</b> if you want a shell: <a href="/guides/ssh-into-lg-tv/">LG TV SSH</a>.</li>
</ol>
{related([("/install/", "Install guide", "Homebrew Channel, the repo and compatibility"),
          ("/guides/block-lg-tv-updates/", "Block LG TV updates", "Keep root once you have it"),
          ("/guides/homebrew-channel-repository/", "Homebrew Channel repositories", "Add apps that aren't in the default list")])}
""")

# --- 7. block updates
UPD_FAQ = [
    ("Is turning off automatic updates in the TV's settings enough?",
     "Not on its own.  It stops automatic installs, but the TV still checks and can prompt, and people have found updates getting through.  On a rooted TV, block the servers as well."),
    ("Which LG update servers should I block?",
     "<code>snu.lge.com</code>, <code>su.lge.com</code>, <code>su-ssl.lge.com</code> and <code>su-dev.lge.com</code> (what the Homebrew Channel blocks), plus <code>nsu.lge.com</code>, <code>snu-dev.lge.com</code> and <code>ngfts.lge.com</code>, which it misses."),
    ("Can I block LG TV updates with Pi-hole or my router's DNS?",
     "Yes, add those hostnames to your blocklist.  It covers the TV before it has even started.  It can't block the update server the TV reaches by IP address, <code>156.147.69.32</code>: that needs a firewall rule, on the router or on the TV."),
    ("Will blocking updates break apps?",
     "It doesn't touch app updates from LG's store or the Homebrew Channel.  It blocks firmware updates only."),
]
guide("block-lg-tv-updates",
      title="How to block LG TV firmware updates (Pi-hole, DNS, rooted TVs)",
      desc="Block LG webOS firmware updates: the servers to block on Pi-hole or your router, what the Homebrew Channel misses, and a fuller block for rooted TVs.",
      card=("Block LG TV firmware updates", "Pi-hole, router DNS, and what the Homebrew Channel misses"),
      h1="Block LG TV firmware updates.",
      lead="A firmware update can remove root, and patched firmware can't be rooted again.  Here's every layer of blocking, from your router to the TV itself.",
      accent="#ff3ea5", keywords=["lg tv block updates", "lg tv block updates dns", "pihole block lg tv updates", "lg tv disable updates", "lg tv stop updates"],
      faq=UPD_FAQ, body=f"""
<h2>1. On any TV: turn off automatic updates</h2>
<p>In the TV's settings, under Support and Software Update, turn off automatic updates.  It's the first layer, but not enough on its own.</p>

<h2>2. On your network: block the servers</h2>
<p>Add these to Pi-hole, AdGuard Home or your router's DNS blocklist.  This works whether or not the TV is rooted, and it's in place before the TV has even started.</p>
<div class="code"><pre>snu.lge.com
su.lge.com
su-ssl.lge.com
su-dev.lge.com
nsu.lge.com
snu-dev.lge.com
ngfts.lge.com</pre></div>
<p>DNS can't block one thing: the updater also reaches a server by IP address, <code>156.147.69.32</code>.  Block that with a firewall rule on the router if it supports one.</p>

<h2>3. On a rooted TV: the Homebrew Channel's block</h2>
<p>The Homebrew Channel's <b class="c-wh">Block system updates</b> points the first four servers above at nothing in the TV's hosts file.  People in <a href="https://github.com/webosbrew/webos-homebrew-channel/issues/96" target="_blank" rel="noopener">Homebrew Channel issue #96</a> found what it misses: <code>nsu.lge.com</code>, LG's current update server, which a TV still reached with the block on, plus the IP address above and an update check that runs early in boot.</p>

<h2>4. On a rooted TV: Block updates harder</h2>
<p><a href="/lg-usb-2-eth0/">LG-USB-2-ETH0</a>'s <b class="c-wh">Block updates harder</b> covers the gaps, at once and again at every boot:</p>
<ul>
<li>Turns off webOS's own update check (the hidden <code>softwareUpdateEnable</code> setting), including the early one at boot.</li>
<li>Adds <code>nsu.lge.com</code>, <code>snu-dev.lge.com</code> and <code>ngfts.lge.com</code> to the hosts file, without touching the Homebrew Channel's lines.</li>
<li>Blocks <code>156.147.69.32</code> with one firewall rule.</li>
<li>Deletes update details already found or downloaded, so a waiting prompt goes away.</li>
</ul>
<p>Turning it off undoes all of it.  It's a toggle in the LG-USB-2-ETH0 TV app, or <code>--block-updates</code> over SSH, and it works whether or not you use a USB adapter.</p>
{related([("/guides/root-lg-tv-2026/", "Rooting an LG TV in 2026", "Which firmware is still rootable"),
          ("/lg-usb-2-eth0/", "LG-USB-2-ETH0", "Includes Block updates harder"),
          ("/install/", "Install guide", "Root, Homebrew Channel, the repo")])}
""")

# --- Wake on LAN with a USB adapter
WAKE_FAQ = [
    ("Can an LG TV wake up through a USB Ethernet adapter?",
     "No.  Standby resets the TV's USB ports, so the adapter is gone by the time the wake-up arrives.  LG's network wake listens on Wi-Fi, and on the built-in port when it has a cable."),
    ("Which MAC address do I send the wake-up to?",
     "The Wi-Fi MAC address, not the adapter's.  On a rooted TV, LG-USB-2-ETH0's <code>status</code> prints the right one.  If the built-in port has a cable in it, its MAC works too."),
    ("Why does the internet stop working when I turn Wi-Fi back on?",
     "webOS's connection manager ranks a connection it has checked as online ahead of one that's only ready, so Wi-Fi can take over the TV's traffic.  <b>Wi-Fi wake in standby</b> keeps the adapter first, and checks every 10 seconds."),
    ("Does Wi-Fi need its own IP address?",
     "Yes, if you set fixed IPs.  Wi-Fi and the adapter with the same IP break the TV's connection.  Letting the router hand out addresses, with a reservation for each MAC, is easiest."),
    ("Why did the TV boot instead of just turning on?",
     "After a longer time off, the TV can be in deeper standby, and waking it boots it fresh.  That's normal, and the adapter is connected again either way."),
]
WAKE_GH = "https://github.com/ohmybahgosh/LG-USB-2-ETH0"
def wout(s): return f'<div class="code"><pre>{esc(s.strip())}</pre></div>'
guide("lg-tv-wake-on-lan",
      title="Turn on an LG TV over the network with a USB Ethernet adapter (Wake on LAN)",
      desc="Why Wake on LAN and Turn on via Wi-Fi stop working when a USB Ethernet adapter is an LG TV's main connection, and how to keep them working on a rooted TV.",
      card=("Wake on LAN with a USB adapter", "Keep Turn on via Wi-Fi and Home Assistant working"),
      h1="Turn on an LG TV over the network, with a USB adapter.",
      lead="A USB Ethernet adapter makes an LG TV two to three times faster on the wire.  But Wake on LAN, <b class=\"c-wh\">Turn on via Wi-Fi</b>, the ThinQ app and Home Assistant can't wake the TV through it.  Here's why, and how to keep all of them working on a rooted TV.",
      accent="#33e1ff", og="/assets/og/lg-usb-2-eth0.png", keywords=["lg tv wake on lan", "lg tv turn on via wifi", "lg tv wake on lan usb ethernet", "home assistant turn on lg tv", "lg tv wol not working"],
      faq=WAKE_FAQ, body=f"""
<h2>Why the adapter can't wake the TV</h2>
<p>Standby resets the TV's USB ports, so the adapter is gone by the time a wake-up packet arrives.  LG's network wake listens on Wi-Fi instead, and on the built-in port when it has a cable.  So with an adapter, Wi-Fi is how the TV gets woken.</p>
<p>Two things get in the way of that:</p>
<ul>
<li><b class="c-wh">Some TVs drop off Wi-Fi in standby</b> while the adapter is the main connection.  A G6 on webOS 26 did (<a href="{WAKE_GH}/discussions/19" target="_blank" rel="noopener">discussion #19</a>): connected while on, unreachable once off.</li>
<li><b class="c-wh">Some TVs turn Wi-Fi off when a cable is connected.</b>  A 2022 C2 on webOS 25 turned it off at boot with the adapter in, and didn't join Wi-Fi again on its own.</li>
</ul>
<p>And once Wi-Fi is kept on next to the adapter, webOS's connection manager can move the TV's traffic to Wi-Fi.  It ranks a connection it has checked as online ahead of one that's only ready, so when Wi-Fi reconnects, the internet goes through Wi-Fi.  On the C2 that meant apps slowed down or stopped loading until Wi-Fi was turned off again.</p>

<h2>The fix: Wi-Fi wake in standby</h2>
<p><a href="/lg-usb-2-eth0/">LG-USB-2-ETH0</a>, which makes the adapter the TV's <code>eth0</code>, has a <b class="c-wh">Wi-Fi wake in standby</b> switch (<code>--wifi-wake</code> over SSH) that handles all three:</p>
<ul>
<li><b class="c-wh">While the TV is on</b>, it keeps Wi-Fi on and joined to your saved network, and keeps the adapter ahead of Wi-Fi so traffic goes over the cable.  Every 10 seconds it checks the internet hasn't moved to Wi-Fi, and moves it back if it has.</li>
<li><b class="c-wh">Just before standby</b>, if Wi-Fi is connected and Turn on via Wi-Fi is on, it disconnects only the adapter's network session.  The adapter stays plugged in and stays <code>eth0</code>, and Wi-Fi stays ready for the wake-up.</li>
<li><b class="c-wh">When the TV is on again</b>, or at the next boot if it lost power in standby, it connects the adapter again (up to 10 tries, as the adapter can take a few seconds to come back) and puts it ahead of Wi-Fi.</li>
</ul>
<p>Tested on a 2022 C2, woken from standby over Wi-Fi with the adapter back as the main connection afterwards, and on a G6 on webOS 26.</p>

<h2>Set it up</h2>
<ol>
<li>Root the TV and install the Homebrew Channel (see the <a href="/install/">install guide</a>), then LG-USB-2-ETH0, and turn on <b class="c-wh">Run at every boot</b>.</li>
<li>Turn on <b class="c-wh">Turn on via Wi-Fi</b> in the TV's settings, usually under General, Devices, External Devices, TV On With Mobile.</li>
<li>Join your Wi-Fi network once in the TV's network settings.  If you use fixed IPs, give Wi-Fi its own, not the adapter's: two connections with the same IP break the TV's connection.</li>
<li>Turn on <b class="c-wh">Wi-Fi wake in standby</b> in the app.  It starts right away, no restart needed.</li>
</ol>
<p>Or over SSH:</p>
{code("sh LG-USB-2-ETH0.sh install --wifi-wake")}

<h2>Wake the TV</h2>
<p>Send the wake-up to the TV's <b class="c-wh">Wi-Fi MAC address</b>, not the adapter's.  <code>status</code> prints the one to use:</p>
{wout("Turning the TV on over the network (Turn on via Wi-Fi, apps, Home Assistant)\ngoes through Wi-Fi, not the adapter: standby resets the USB ports.\nWake it by wlan0's MAC, aa:bb:cc:dd:ee:ff.")}
<p>Send it to your network's broadcast address (like <code>192.168.1.255</code>) on port 9:</p>
<ul>
<li><b class="c-wh">A phone app:</b> any Wake on LAN app, with the Wi-Fi MAC, the broadcast address and port 9.</li>
<li><b class="c-wh">Linux or a Pi:</b> <code>wakeonlan -i 192.168.1.255 aa:bb:cc:dd:ee:ff</code></li>
<li><b class="c-wh">Home Assistant:</b> <code>wake_on_lan.send_magic_packet</code> with the Wi-Fi MAC and broadcast address, for example in the LG webOS integration's Turn on automation.</li>
<li><b class="c-wh">The LG ThinQ app</b> uses Turn on via Wi-Fi on its own.</li>
</ul>
<p>If Home Assistant or an app learned the TV's "wired" MAC after the adapter became <code>eth0</code>, that's the adapter's.  Point it at the Wi-Fi MAC.</p>

<h2>Check it's working</h2>
<p>Everything it does goes in <code>/var/lib/webosbrew/lg-usb-2-eth0.log</code>, with why it did or didn't hand over.  A full standby and wake on a C2:</p>
{wout("=== power: Active Standby ===\n=== standby: disconnected the adapter's network session, so Wi-Fi stays ready for wake ===\n=== power: Active Standby (Prepare Power Off) ===\n=== power: Power Off ===\n=== boot hook (wait 120s, module .../r8152_oot.ko) ===\nDone: the USB adapter is eth0, the built-in port is eth2.\n=== awake: try 1 of 10: the adapter has no cable link yet ===\n=== awake: the adapter is connected again (try 2) ===\nFollowing standby for Wi-Fi wake.\n=== power: Active ===")}
<p>With the TV on, the internet should go through the adapter, with Wi-Fi ready behind it:</p>
{wout("$ ip route | head -1\ndefault via 192.168.1.1 dev eth0\n$ connmanctl services | head -2\n*AO Wired              ethernet_..._cable\n*AR YourNetwork        wifi_..._managed_psk")}
<p>The <a href="{WAKE_GH}/wiki/Wi-Fi-wake" target="_blank" rel="noopener">full guide on GitHub</a> lists every log line and what it means, plus troubleshooting.</p>
{related([("/lg-usb-2-eth0/", "LG-USB-2-ETH0", "Includes Wi-Fi wake in standby"),
          ("/guides/lg-tv-ethernet-100mbps/", "LG TV Ethernet stuck at 100 Mbps", "Why, and how to go faster"),
          ("/guides/usb-ethernet-adapter-lg-tv/", "Which USB Ethernet adapter", "The chip matters more than the brand")])}
""")

# --- 8. tailscale
TS_FAQ = [
    ("Is there a Tailscale app for LG TVs?",
     "Not in LG's store.  On a rooted TV, Entware's Tailscale add-on runs Tailscale on the TV itself."),
    ("What does Tailscale on the TV let me do?",
     "Reach the TV from anywhere on your tailnet with no ports opened: SSH, and the Entware services on it like File Browser, Syncthing, Transmission and the phone dashboard."),
    ("Does it reconnect after a restart?",
     "Yes.  It starts with the TV and signs back in by itself."),
    ("Does it change the TV's DNS or firewall?",
     "No.  DNS and the firewall stay webOS's."),
]
guide("tailscale-lg-tv",
      title="Tailscale on an LG TV: set it up on a rooted webOS TV",
      desc="Run Tailscale on a rooted LG webOS TV with Entware's one-press add-on: sign in with a QR code, then reach the TV and its services from anywhere on your tailnet.",
      card=("Tailscale on an LG TV", "One-press setup on a rooted TV, sign in with a QR code"),
      h1="Tailscale on an LG TV.",
      lead="On a rooted LG TV, Tailscale runs on the TV itself: one press in the Entware app, a QR code to sign in, and the TV is on your tailnet.",
      accent="#ffb547", og="/assets/og/webos-entware-installer.png", keywords=["tailscale lg tv", "tailscale lg tv webos", "install tailscale lg tv", "use tailscale on lg tv"],
      faq=TS_FAQ, body=f"""
<h2>What you need</h2>
<ul>
<li>A rooted LG TV with the Homebrew Channel (<a href="/install/">install guide</a>).</li>
<li><a href="/webos-entware-installer/">Entware</a> from <code>{REPO}</code>, installed from its TV app.</li>
<li>A Tailscale account.</li>
</ul>

<h2>Set it up</h2>
{steps([("Open Add-ons", "In the Entware TV app, open <b class=\"c-wh\">Add-ons</b> and go to the network services."),
        ("Add Tailscale", "Select <b class=\"c-wh\">Tailscale</b> and add it.  The app installs it and starts it with the TV."),
        ("Sign in", "The app shows a QR code of the sign-in link.  Scan it with your phone and approve the TV in your tailnet."),
        ("Connect", "From any device on your tailnet: <code>ssh root@&lt;the TV's tailnet IP&gt;</code>.")])}
<p>Over SSH instead:</p>
<div class="code"><pre><span class="pr">$ </span>webos-entware add tailscale
<span class="pr">$ </span>webos-entware info tailscale</pre></div>

<h2>What it's good for</h2>
<ul>
<li><b class="c-wh">SSH from anywhere</b>, with no ports opened on your router.</li>
<li><b class="c-wh">The TV's services over your tailnet:</b> File Browser, Syncthing and Transmission, and Entware's phone dashboard, which only answers your home network and your tailnet.</li>
</ul>
<p>It reconnects by itself after a restart, and DNS and the firewall stay webOS's.  Removing the add-on signs the TV out of your tailnet.</p>
{related([("/webos-entware-installer/", "Entware", "25 one-press add-ons"),
          ("/guides/lg-tv-file-sharing-samba/", "File sharing on an LG TV", "Samba, File Browser and DLNA"),
          ("/guides/ssh-into-lg-tv/", "LG TV SSH", "Logins, keys and common errors")])}
""")

# --- 9. samba / file sharing
SMB_FAQ = [
    ("Can an LG TV share files over Samba (SMB)?",
     "Not out of the box.  On a rooted TV, Entware's Samba add-on shares a folder with Windows and Mac over SMB2 and up, with a password, and it shows up in Windows' Network."),
    ("Where do the shared files live?",
     "In <code>/opt/files</code> on the TV's app storage, with <code>Downloads</code>, <code>Media</code> and <code>Sync</code> folders, and USB drives under <code>USB</code>."),
    ("Is guest access on?",
     "No.  Each service gets a random 16-character password made on the TV, and nothing starts with its stock settings."),
    ("Can other devices play the TV's files?",
     "Yes, with the DLNA media server add-on: other TVs, consoles and VLC see it as \"LG TV (Entware)\" and can play videos, music and photos from it."),
]
guide("lg-tv-file-sharing-samba",
      title="LG TV file sharing: Samba, File Browser and DLNA on webOS",
      desc="Share files with a rooted LG webOS TV: a Samba share for Windows and Mac, File Browser for your phone, and a DLNA server, each one press in Entware.",
      card=("File sharing on an LG TV", "Samba, File Browser and DLNA on a rooted TV"),
      h1="File sharing on an LG TV.",
      lead="Copy files to the TV from Windows or Mac, manage them from your phone's browser, and play them on other devices.  On a rooted TV, each is one press.",
      accent="#ffb547", og="/assets/og/webos-entware-installer.png", keywords=["samba lg tv", "lg tv samba share", "smb lg tv", "lg tv file browser", "lg tv dlna server"],
      faq=SMB_FAQ, body=f"""
<h2>The three add-ons</h2>
{table(["add-on", "what you get", "where"], [
    ["<b>Samba</b>", "Share <code>/opt/files</code> with Windows and Mac, SMB2 and up.  It shows up in Windows' Network.", "<code>\\\\&lt;TV IP&gt;\\TV</code>, user <code>tv</code>"],
    ["<b>File Browser</b>", "Upload, download and manage files from a browser on your phone or computer.", "<code>http://&lt;TV IP&gt;:8090</code>, user <code>admin</code>"],
    ["<b>DLNA media server</b>", "Play videos, music and photos from the TV and its USB drives on other TVs, consoles and VLC.", "\"LG TV (Entware)\""],
])}
<p>All three come with <a href="/webos-entware-installer/">Entware</a>, from <code>{REPO}</code> on a rooted TV.  Add them in the TV app's <b class="c-wh">Add-ons</b>, or from your phone with <b class="c-wh">Manage from your phone</b>.</p>

<h2>Safe by default</h2>
<ul>
<li>A random 16-character password, made on the TV, for anything with a login.  No guest access.</li>
<li>One shared folder, <code>/opt/files</code>, with <code>Downloads</code>, <code>Media</code> and <code>Sync</code>, and USB drives in <code>USB</code>.  Removing a service never deletes your files.</li>
<li>A service won't start if something else on the TV has its port.  File Browser uses 8090, because webOS takes 8080.</li>
</ul>

<h2>See the password</h2>
<p>Open the service in the TV app's Add-ons for its address, password and a QR code, or over SSH:</p>
<div class="code"><pre><span class="pr">$ </span>webos-entware info samba
<span class="pr">$ </span>webos-entware password samba --ask</pre></div>
<p>Away from home?  Add <a href="/guides/tailscale-lg-tv/">Tailscale</a> and reach File Browser over your tailnet.</p>
{related([("/guides/tailscale-lg-tv/", "Tailscale on an LG TV", "Reach the TV from anywhere"),
          ("/webos-entware-installer/", "Entware", "Linux packages and add-ons"),
          ("/install/", "Install guide", "Root, Homebrew Channel, the repo")])}
""")

# --- guides index
add("/guides/",
    title="Guides for rooted LG webOS TVs · ohmybahgosh.dev",
    desc="How-tos for rooted LG webOS TVs: faster wired Ethernet, which USB adapter to buy, SSH, Homebrew Channel repositories and an IPTV player with a real guide.",
    trail=[HOME, ("Guides", "/guides/")],
    ld=[{"@type": "CollectionPage", "name": "Guides for rooted LG webOS TVs", "url": SITE + "/guides/",
         "hasPart": [{"@type": "TechArticle", "name": t, "url": SITE + p} for p, t, _ in GUIDES]}],
    body=head("$ ls guides/", "Guides.", "How-tos for rooted LG TVs, from the questions that come up most around these apps.") +
         doc('<div class="gcards">' + "".join(f'<a class="card gcard" href="{p}"><b>{t}</b><span>{d}</span></a>' for p, t, d in GUIDES) +
             '<a class="card gcard" href="/install/"><b>Install guide</b><span>Root, the Homebrew Channel, the repo, and which app works on which TV</span></a></div>'))

# =====================================================================================  app FAQs
def app_faq(slug, name, title, desc, intro, qas, accent, og):
    path = f"/{slug}/faq/"
    body = head(f"$ man {slug.split('-')[0] if slug != 'lg-usb-2-eth0' else slug}", f"{name} FAQ.", intro, accent) + doc(
        faq_html(qas) + related([(f"/{slug}/", name, "The project page"), ("/install/", "Install guide", "Root, Homebrew Channel, repo"), ("/guides/", "Guides", "How-tos for rooted LG TVs")]), accent)
    add(path, title=title, desc=desc, trail=[HOME, (name, f"/{slug}/"), ("FAQ", path)], ld=[faq_ld(qas)], body=body, og_image=og)

app_faq("tivibro", "TiviBro", "TiviBro FAQ: install, providers, backups and privacy",
        "Answers about TiviBro, the free IPTV player for LG webOS TVs: root or not, providers, the phone app, backups, updates and privacy.",
        "Quick answers.  The full user guide lives on <a href=\"https://tivibro.app\" target=\"_blank\" rel=\"noopener\">tivibro.app</a>.", IPTV_FAQ[1:] + [
    ("Does TiviBro come with channels?", "No.  It plays the Xtream Codes, M3U or Stalker portal subscription you already have, with its XMLTV guide."),
    ("How do I install it?", "On a rooted TV, add <code>https://tivibro.app/repo</code> or <code>https://ohmybahgosh.dev/repo</code> to the Homebrew Channel, or run <code>curl -fsSL https://tivibro.app/install | sh</code> over SSH.  Without root, use LG's Developer Mode."),
    ("Is there a phone app?", "Yes, for Android.  It's a remote, plays your channels and media on the TV, opens the web editor, and turns the TV on over the network and Bluetooth.  Download the APK from <a href=\"https://tivibro.app/apk/\" target=\"_blank\" rel=\"noopener\">tivibro.app/apk</a>."),
    ("Can I edit my channels from a computer?", "Yes.  Open <b>Edit on phone</b> on the TV for a QR code, an address and a password.  The web editor hides, sorts, renames and copies channels, and changes are drafts until you press <b>Send to TV</b>."),
    ("How do backups work?", "Everything goes into one file locked with a passphrase you choose (AES-256-GCM), from the TV, the phone app or the web editor.  A brand-new TV can restore it from its first screen."),
    ("Do my provider logins leave the TV?", "No.  The web editor only sees server names, logs mask usernames and passwords, and problem reports replace server names before anything is sent."),
    ("My TV can't play DTS or Dolby TrueHD.", "LG TVs from 2020 to 2022 can't play DTS, and none plays TrueHD.  TiviBro picks another track in your language, or converts the sound to Dolby Digital while you watch."),
], "#5b8cff", "/assets/og/tivibro.png")

app_faq("lg-usb-2-eth0", "LG-USB-2-ETH0", "LG-USB-2-ETH0 FAQ: USB Ethernet as eth0 on LG TVs",
        "Answers about LG-USB-2-ETH0: firmware updates, Wi-Fi, waking the TV over the network, drivers, two adapters and how to undo it.",
        "Making a USB Ethernet adapter the TV's <code>eth0</code>, answered.", [
    ("What does it do?", "It makes a USB Ethernet adapter the TV's <code>eth0</code>, the interface webOS and its apps expect, and parks the 100 Mbit/s built-in port as <code>eth2</code>.  Settings show the wired connection and apps use the faster link."),
    ("How much faster is it?", "About 250 to 330 Mbit/s over the USB 2.0 ports most LG TVs have, against about 95 for the built-in port.  See <a href=\"/guides/lg-tv-ethernet-100mbps/\">LG TV Ethernet stuck at 100 Mbps</a>."),
    ("Does it survive a firmware update?", "The hook lives in the Homebrew Channel's folder, so it stays as long as root does.  If an update removes root, the TV just goes back to the built-in port.  Current firmware can't be rooted again, so keep updates off."),
    ("Does it change my network settings?", "No.  webOS still sets up the wired connection.  Only the interface names change, unless you turn on the Wi-Fi backup or Block updates harder."),
    ("Can I still turn the TV on over the network?", "Not through the adapter: standby resets the TV's USB ports.  Leave Wi-Fi connected and send the wake-up to the Wi-Fi MAC address, which <code>status</code> prints.  If your TV drops off Wi-Fi in standby, turns Wi-Fi off with the adapter in, or moves traffic to Wi-Fi, turn on <b>Wi-Fi wake in standby</b>: see <a href=\"/guides/lg-tv-wake-on-lan/\">Wake on LAN with a USB adapter</a>."),
    ("My adapter isn't detected.", "The kernel likely has no driver for its chip.  <code>get-driver</code> offers one built for your exact kernel when one is known, and <code>test-driver</code> one waiting for testers.  More than 350 are built, for over 50 LG kernels from webOS 3.5 to webOS 25."),
    ("Can I use two adapters?", "Yes.  Pin the one you want with <code>--mac</code>.  Otherwise the first adapter with a cable in wins."),
    ("How do I undo it?", "Press <b>Turn everything off</b> in the TV app before removing it, or run <code>sh LG-USB-2-ETH0.sh uninstall --now</code>.  No system files are touched."),
], "#3ddc97", "/assets/og/lg-usb-2-eth0.png")

app_faq("webos-entware-installer", "Entware", "Entware on LG webOS FAQ: install, packages and add-ons",
        "Answers about Entware on rooted LG webOS TVs: requirements, 32-bit or 64-bit, add-ons, the phone dashboard, reboots and uninstalling.",
        "Linux packages and a real shell on a rooted LG TV, answered.", [
    ("What is Entware?", "A package manager for embedded Linux devices, with over a thousand packages.  On a rooted LG TV it gives you <code>opkg</code>, a bash shell and tools like htop, tmux, git and Python."),
    ("What do I need?", "A rooted LG TV with the Homebrew Channel, an internet connection on the TV and about 50 MB free.  SSH is only needed for the shell: the TV app doesn't need it."),
    ("Which TVs does it support?", "webOS 23, 24 and 25 are the main targets, and webOS 4 and up should work.  Both 64-bit and 32-bit kernels are supported."),
    ("Why 32-bit or 64-bit?", "Every LG TV runs a 32-bit system, but Entware brings its own libraries, so only the kernel matters.  A 64-bit kernel gets the faster <code>aarch64</code> build, a 32-bit one <code>armv7</code>."),
    ("What are add-ons?", "25 one-press setups, each with what it needs on webOS: tools like git and Python, and network services like Tailscale, Samba, File Browser, a DLNA media server, Transmission and Syncthing."),
    ("Can I manage it from my phone?", "Yes.  <b>Add-ons > Manage from your phone</b> shows a QR code that opens a dashboard on your phone, signed in, for add-ons and passwords."),
    ("Does it survive a reboot?", "Yes.  A boot script from the Homebrew Channel mounts it at every start."),
    ("Does the app phone home?", "No.  It only talks to GitHub, to check for and download its own updates."),
], "#ff3ea5", "/assets/og/webos-entware-installer.png")

app_faq("ssh-doctor", "SSH Doctor", "SSH Doctor FAQ: fix SSH on rooted LG webOS TVs",
        "Answers about SSH Doctor: how it works when SSH is broken, the alpine password, pairing a key, changing the port, keys only and SFTP.",
        "Fixing SSH on a rooted LG TV from the TV itself, answered.", SSH_FAQ[:3] + [
    ("How can it fix SSH if SSH is broken?", "It's a TV app that runs as root through the Homebrew Channel, not over SSH, so it works with just the remote."),
    ("How does pairing a key work?", "Choose <b>Set up a key</b> on the TV, scan the QR code or open the address on your computer or phone, enter the short code, and upload a public key or let the browser make one.  The private key never leaves your device."),
    ("Can I set my own root password?", "Yes, on the TV or from your phone.  It's turned into a SHA-512 crypt hash first, so the password itself is never sent over the network or saved on the TV."),
    ("Can I move SSH off port 22?", "Yes.  The old port stays open alongside the new one until you've logged in on the new one, so a typo can't lock you out."),
    ("Does it change system files?", "No.  Settings live in the Homebrew Channel's folders, a backup is kept before every change, and <b>Reset to Homebrew Channel defaults</b> removes all of it."),
], "#3ddc97", "/assets/og/ssh-doctor.png")

app_faq("luna-atlas", "Luna Atlas", "Luna Atlas FAQ: luna-send on LG webOS TVs",
        "Answers about luna-send and Luna Atlas: what the Luna Service Bus is, running commands, access levels, dangerous methods and where the data comes from.",
        "luna-send and the catalog, answered.", [
    ("What is luna-send?", "The command-line tool every LG webOS TV ships to talk to the Luna Service Bus, the internal message bus every system service listens on: power, apps, inputs, picture and sound, Wi-Fi, notifications and hundreds more."),
    ("What do I need to run a command?", "A rooted TV, or LG's Developer Mode, and a shell on the TV.  Browsing the catalog needs nothing."),
    ("What do public, private and the other access levels mean?", "Public methods are open to normal apps.  Private ones are for LG's own apps and services, and need root or a privileged caller.  Some are only reachable as root, and SSAP methods are the ones LG's remote-control API exposes."),
    ("Why does luna-send say permission denied?",
     "Usually the method is private: it's for LG's own apps and services, and a normal caller isn't allowed.  Each method in the catalog shows its access level.  Private methods need root, and Developer Mode's shell isn't root."),
    ("Is it safe to run these?", "Many calls change settings, inputs or power, and a few can reset the TV, wipe data or brick it.  Those are flagged dangerous.  Running one from the catalog is exactly as safe as typing the same <code>luna-send</code> yourself."),
    ("Where does the data come from?", "LG's webOS TV and webOS OSE docs, the homebrew and remote-control community, and the service list introspected from a rooted TV.  Each method says whether it's documented or inferred."),
    ("Is there a command-line version?", "Yes, <code>luna-atlas.sh</code> in the GitHub repo can search, show and run methods over SSH, with tab completion.  It's an early preview."),
    ("Can I browse by what a command does?", "Yes: <a href=\"/luna-atlas/categories/\">browse by category</a>, or start from <a href=\"/luna-atlas/examples/\">common luna-send examples</a>."),
], "#33e1ff", "/assets/og/luna-atlas.png")

# =====================================================================================  tour video page
CHAPTERS = [  # start, end, key, name, what it covers
    (4, 44, "tivibro", "TiviBro", [
        ("The guide is the home screen", "Preview in the window, OK again for fullscreen."),
        ("Xtream Codes or M3U", "Runs on the TV itself, webOS 4 and newer."),
        ("Edit on your computer or phone", "Hide, sort and rename hundreds of channels, then Send to TV.  The TV picks it up in seconds."),
        ("Set up from your phone", "Scan the code on the first screen and type your login with a real keyboard."),
        ("A remote in your pocket", "The Android app: Play on TV, volume, My media, and Turn on over the network."),
        ("Catch-up, My teams, My media and search", "Rewind the guide, your teams' games from every channel, DLNA, WebDAV and Dropbox, and one search across everything.")]),
    (44, 67, "eth0", "LG-USB-2-ETH0", [
        ("eth0, not eth1", "Apps and settings see a wired link.  Streaming apps like Paramount+ refuse to play over eth1."),
        ("Set and forget", "Runs at every boot, follows plug and unplug, with Wi-Fi as a backup."),
        ("Speed", "About 95 Mbit/s built in, 280 over USB, measured with the app's own speed test."),
        ("Drivers", "Hundreds of drivers built for LG's kernels.  It finds, checks and loads the one for your TV.")]),
    (67, 88, "entware-installer", "Entware", [
        ("Packages", "1,100+ packages in plain categories, each with its own page."),
        ("Shell", "A real bash shell over SSH, plus ent and tv commands."),
        ("Add-ons", "25 one-press add-ons: Tailscale, Samba, File Browser, Syncthing and more."),
        ("Phone dashboard", "Manage add-ons and passwords from your phone.")]),
    (88, 109, "ssh-doctor", "SSH Doctor", [
        ("Check", "Finds out why SSH stopped working.  Runs through the Homebrew Channel, so it works when SSH doesn't."),
        ("Repair", "One button per fix, each with a backup and an undo."),
        ("Pairing code", "Add your computer's key with a short code."),
        ("Your password", "Set root's password from your phone, hashed first.")]),
    (109, 126, "luna-atlas", "Luna Atlas", [
        ("The catalog", "Every luna-send method, across 501 services."),
        ("Every method", "Parameters, access level and a ready-to-run command.  Search it, filter it, link to it.")]),
]
ICON = {"tivibro": "tivibro", "eth0": "eth0", "entware-installer": "entware", "ssh-doctor": "ssh-doctor", "luna-atlas": "luna-atlas"}
PAGEURL = {"tivibro": "/tivibro/", "eth0": "/lg-usb-2-eth0/", "entware-installer": "/webos-entware-installer/", "ssh-doctor": "/ssh-doctor/", "luna-atlas": "/luna-atlas/"}
def mmss(t): return f"{t // 60}:{t % 60:02d}"
transcript = "  ".join(f"{name}. " + "  ".join(f"{h}.  {d}" for h, d in items) for _, _, _, name, items in CHAPTERS)
video_ld = {
    "@type": "VideoObject", "@id": SITE + "/tour/#video",
    "name": "LG webOS homebrew apps: a two-minute tour",
    "description": "A tour of five open-source apps for LG webOS TVs: TiviBro (an IPTV player), LG-USB-2-ETH0 (USB Ethernet as eth0), Entware (Linux packages), SSH Doctor and Luna Atlas, with what each does and its standout features.",
    "thumbnailUrl": [SITE + "/assets/img/webos-promo-poster.webp", SITE + "/assets/og/home.png"],
    "uploadDate": "2026-11-09T14:53:55-05:00", "duration": "PT2M16S",
    "contentUrl": SITE + "/assets/media/webos-promo.mp4",
    "creator": {"@type": "Person", "@id": SITE + "/#person", "name": "OhMyBahGosh", "url": SITE + "/about/"},
    "inLanguage": "en-US", "isFamilyFriendly": True, "transcript": transcript,
    "hasPart": [{"@type": "Clip", "name": name, "startOffset": a, "endOffset": b, "url": f"{SITE}/tour/?t={a}"} for a, b, _, name, _ in CHAPTERS],
}
chap_btns = "\n".join(f'        <button type="button" data-t="{a}"><img src="/assets/img/{ICON[k]}-icon.webp" alt="" width="160" height="160" loading="lazy"><span>{n}</span><i>{mmss(a)}</i></button>' for a, _, k, n, _ in CHAPTERS)
sections = "\n".join(
    f'<h2 id="{k}">{n} <span class="dim mono" style="font-size:15px;font-weight:500">{mmss(a)}</span></h2>\n<ul>' +
    "".join(f"<li><b class=\"c-wh\">{h}.</b>  {d}</li>" for h, d in items) +
    f'</ul>\n<p><a href="{PAGEURL[k]}">More about {n}</a></p>' for a, _, k, n, items in CHAPTERS)
add("/tour/",
    title="LG webOS homebrew apps: a two-minute video tour",
    desc="Watch a two-minute tour of five open-source LG webOS apps: TiviBro, LG-USB-2-ETH0, Entware, SSH Doctor and Luna Atlas, with chapters for each app.",
    trail=[HOME, ("Tour", "/tour/")], og_image="/assets/og/home.png",
    ld=[video_ld, {"@type": "WebPage", "@id": SITE + "/tour/", "url": SITE + "/tour/", "name": "LG webOS homebrew apps: a two-minute video tour",
                   "primaryImageOfPage": SITE + "/assets/img/webos-promo-poster.webp", "mainEntity": {"@id": SITE + "/tour/#video"}, "isPartOf": {"@id": SITE + "/#website"}}],
    body=head("$ ./tour.mp4", "The webOS apps in two minutes.", "What each app does and the features that set it apart.  Sound on.") + f"""
<section id="tour" style="padding-top:18px">
    <style>
      #tour .tv{{margin-bottom:34px}}
      #tour .tour-ch{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}}
      #tour .tour-ch button{{display:flex;align-items:center;gap:10px;min-width:0;padding:10px 12px;border-radius:12px;border:1px solid var(--line2);background:rgba(255,255,255,.03);color:var(--fg);font:600 14px var(--sans);cursor:pointer;transition:.2s;text-align:left}}
      #tour .tour-ch button:hover,#tour .tour-ch button[aria-current=true]{{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 10%,transparent)}}
      #tour .tour-ch img{{width:28px;height:28px;border-radius:7px;flex:none}}
      #tour .tour-ch span{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;min-width:0}}
      #tour .tour-ch i{{font:500 12px var(--mono);font-style:normal;color:var(--fg3)}}
      @media (max-width:860px){{#tour .tour-ch{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
      @media (max-width:520px){{#tour .tour-ch{{grid-template-columns:1fr}}}}
    </style>
    <div class="tv"><video id="tour-video" src="/assets/media/webos-promo.mp4" poster="/assets/img/webos-promo-poster.webp" controls playsinline preload="metadata" width="1920" height="1080" aria-label="A two-minute tour of the webOS apps: TiviBro, LG-USB-2-ETH0, Entware, SSH Doctor and Luna Atlas"></video></div>
    <nav class="tour-ch" aria-label="Chapters">
{chap_btns}
    </nav>
    <script>
    (function(){{var v=document.getElementById("tour-video"),bs=[].slice.call(document.querySelectorAll("#tour .tour-ch button"));if(!v)return;
    function play(){{var p=v.play();if(p&&p.catch)p.catch(function(){{}});}}
    function seek(t){{if(v.readyState>=1){{v.currentTime=t;}}else{{v.addEventListener("loadedmetadata",function h(){{v.removeEventListener("loadedmetadata",h);v.currentTime=t;}});}}}}
    function go(t){{v.addEventListener("seeked",function r(){{v.removeEventListener("seeked",r);if(v.paused)play();}});seek(t);play();}}
    bs.forEach(function(b){{b.addEventListener("click",function(){{go(+b.dataset.t);history.replaceState(null,"","?t="+b.dataset.t);}});}});
    v.addEventListener("timeupdate",function(){{var c=-1;bs.forEach(function(b,i){{if(v.currentTime>=+b.dataset.t-.2)c=i;}});bs.forEach(function(b,i){{b.setAttribute("aria-current",i===c?"true":"false");}});}});
    var t=+(new URLSearchParams(location.search).get("t")||0);if(t>0&&t<136)seek(t);}})();
    </script>
</section>
""" + doc(f"""
<h2>What's in it</h2>
<p>Five open-source projects for LG webOS TVs, each with a title card and its standout features.  The four TV apps install from one Homebrew Channel repository, <code>{REPO}</code>.  Here's everything the video shows, chapter by chapter.</p>
{sections}
{related([("/install/", "Install guide", "Root, Homebrew Channel, the repo"), ("/guides/", "Guides", "How-tos for rooted LG TVs"), ("/", "ohmybahgosh.dev", "All the projects")])}
"""))

# =====================================================================================  write
if __name__ == "__main__":
    for path, kw in PAGES:
        print("wrote", write(ROOT, path, page(path, **kw)))

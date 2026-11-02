<div align="center">

<a href="https://ohmybahgosh.dev"><img src="docs/banner.svg" width="100%" alt="ohmybahgosh.dev: software LG forgot to ship"></a>

<br>

**The home of my favorite open-source projects, starting with LG webOS homebrew.**

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fohmybahgosh.dev&up_message=online&down_message=offline&label=ohmybahgosh.dev&style=flat-square&color=33e1ff&labelColor=0a0e1a)](https://ohmybahgosh.dev)
[![GitHub Pages](https://img.shields.io/github/deployments/ohmybahgosh/ohmybahgosh.dev/github-pages?label=pages&style=flat-square&labelColor=0a0e1a)](https://github.com/ohmybahgosh/ohmybahgosh.dev/deployments)
[![Last commit](https://img.shields.io/github/last-commit/ohmybahgosh/ohmybahgosh.dev?style=flat-square&color=8b5cff&labelColor=0a0e1a)](https://github.com/ohmybahgosh/ohmybahgosh.dev/commits/main)
[![No build step](https://img.shields.io/badge/build-none-3ddc97?style=flat-square&labelColor=0a0e1a)](#how-its-built)
[![License: MIT](https://img.shields.io/badge/license-MIT-8f9bbf?style=flat-square&labelColor=0a0e1a)](LICENSE)

[**Visit the site**](https://ohmybahgosh.dev) · [Projects](#projects) · [How it's built](#how-its-built) · [Add a project](#add-a-project)

<br>

<a href="https://ohmybahgosh.dev"><img src="docs/preview.png" width="100%" alt="ohmybahgosh.dev on a desktop browser and a phone: a terminal hero typing install commands beside the headline Software LG forgot to ship"></a>

</div>

<br>

## Projects

Every project gets its own page with a live terminal demo, install steps, screenshots and an FAQ.

<table>
<tr>
<td width="33%" valign="top">

### [📺 TiviBro](https://ohmybahgosh.dev/tivibro/)

The IPTV player LG TVs never got.  A free, TiviMate-style player for webOS 4+ with a guide-first layout, catch-up, movies and shows, sports and PPV events, a phone editor and an Android remote.

[![Stars](https://img.shields.io/github/stars/ohmybahgosh/TiviBro?style=flat-square&color=33e1ff&labelColor=0a0e1a)](https://github.com/ohmybahgosh/TiviBro)
[![Release](https://img.shields.io/github/v/release/ohmybahgosh/TiviBro?include_prereleases&style=flat-square&color=5b8cff&labelColor=0a0e1a&label=release)](https://github.com/ohmybahgosh/TiviBro/releases)

[Page](https://ohmybahgosh.dev/tivibro/) · [Repo](https://github.com/ohmybahgosh/TiviBro)

</td>
<td width="33%" valign="top">

### [🔌 LG-USB-2-ETH0](https://ohmybahgosh.dev/lg-usb-2-eth0/)

Make a USB Ethernet adapter the TV's `eth0` on rooted LG webOS TVs, so settings and streaming apps use the faster wired link.  Two to three times the built-in port.

[![Stars](https://img.shields.io/github/stars/ohmybahgosh/LG-USB-2-ETH0?style=flat-square&color=3ddc97&labelColor=0a0e1a)](https://github.com/ohmybahgosh/LG-USB-2-ETH0)
[![Release](https://img.shields.io/github/v/release/ohmybahgosh/LG-USB-2-ETH0?style=flat-square&color=3ddc97&labelColor=0a0e1a&label=release)](https://github.com/ohmybahgosh/LG-USB-2-ETH0/releases)

[Page](https://ohmybahgosh.dev/lg-usb-2-eth0/) · [Repo](https://github.com/ohmybahgosh/LG-USB-2-ETH0)

</td>
<td width="33%" valign="top">

### [📦 Entware Installer](https://ohmybahgosh.dev/webos-entware-installer/)

One-line Entware for rooted webOS.  Picks the right 64-bit or 32-bit build, test-runs it, survives reboots and uninstalls cleanly.  Comes with `ent`, bash, nano and webOS helpers.

[![Stars](https://img.shields.io/github/stars/ohmybahgosh/WEBOS-ENTWARE-INSTALLER?style=flat-square&color=ff3ea5&labelColor=0a0e1a)](https://github.com/ohmybahgosh/WEBOS-ENTWARE-INSTALLER)
[![Shell](https://img.shields.io/badge/POSIX-sh-ffb547?style=flat-square&labelColor=0a0e1a)](https://github.com/ohmybahgosh/WEBOS-ENTWARE-INSTALLER)

[Page](https://ohmybahgosh.dev/webos-entware-installer/) · [Repo](https://github.com/ohmybahgosh/WEBOS-ENTWARE-INSTALLER)

</td>
</tr>
</table>

## Features

| | |
|---|---|
| ⌨️ **Typed terminal demos** | Every page plays a real session from the project: installs, `status` output, build checks.  They render instantly for visitors who prefer reduced motion. |
| 📈 **Live GitHub stats** | Stars, forks, latest release and last push come straight from the GitHub API, cached in the browser for 30 minutes. |
| 🔎 **Command palette** | Press <kbd>/</kbd> or <kbd>Ctrl</kbd>+<kbd>K</kbd> (<kbd>⌘</kbd>+<kbd>K</kbd> on a Mac) to jump to any project, section or repo. |
| 📋 **One-tap copy** | Every install command has a copy button that strips comments and prompts. |
| 📱 **Phone first** | Works at 320px wide with no horizontal scroll.  Wide tables scroll on their own. |
| 🔍 **SEO and social cards** | Canonical URLs, Open Graph and Twitter cards with a custom image per page, `schema.org` JSON-LD for each project, a sitemap and robots.txt. |
| 🚫 **No tracking** | No analytics, no cookies, no third-party scripts.  Fonts and screenshots load from jsDelivr. |

## How it's built

Plain HTML, CSS and JavaScript.  No framework, no bundler, no build step: GitHub Pages serves the files as they are.

```
.
├── index.html                          home page
├── tivibro/index.html                  one folder per project page
├── lg-usb-2-eth0/index.html
├── webos-entware-installer/index.html
├── 404.html                            "command not found"
├── assets/
│   ├── css/site.css                    every style, design tokens at the top
│   ├── js/site.js                      terminals, live stats, palette, copy, tabs
│   ├── og/*.png                        1200×630 social cards
│   └── favicon.svg
├── docs/                               README banner, screenshot, repo social preview
├── CNAME · robots.txt · sitemap.xml · site.webmanifest
└── LICENSE
```

**Design:** dark grid background, neon glows, glass cards with a cursor spotlight.  Type is [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) and [JetBrains Mono](https://www.jetbrains.com/lp/mono/).  Each project page sets its own accent color with a body class (`p-tivibro`, `p-eth0`, `p-entware`).

## Add a project

1. **Copy a project folder**, for example `lg-usb-2-eth0/`, to a new folder named after the repo in lowercase.
2. **Update the page:** the `<title>`, meta description, canonical, `og:` and `twitter:` tags, the JSON-LD block, the hero, and the `data-gh="REPO:stars"` attributes so live stats point at the new repo.
3. **Add a social card** at `assets/og/<folder>.png` (1200×630).
4. **Link it everywhere:** a card in the `#repos` grid on `index.html`, the header and footer in every page, the `REPOS` list at the top of `assets/js/site.js` (for the palette and live stats), and `sitemap.xml`.
5. **Pick an accent:** add a `body.p-<name>{--accent:…;--accent2:…}` line near the top of `site.css`.

### Terminal demos

Each demo is a JSON array inside `<script type="text/x-term">` within a `.term[data-typed]` block:

```json
[
  ["$", "sh LG-USB-2-ETH0.sh apply"],
  ["o", "  Built-in eth0 <span class=c-pk>→</span> eth2"],
  ["o!", "  <span class=c-gr>Done.</span>"],
  ["p", 800]
]
```

| Entry | Does |
|---|---|
| `["$", "text"]` | Types a command after the prompt |
| `["o", "html"]` | Prints a line of output (HTML allowed) |
| `["o!", "html"]` | Prints a line, then pauses a little longer |
| `["p", ms]` | Waits |

Colors: `c-gr` green, `c-cy` cyan, `c-pk` pink, `c-am` amber, `c-vi` violet, `c-bl` blue, `c-mu` muted, `c-wh` white.  Set `data-prompt` on the `.term` to change the prompt, or `data-loop="false"` to play once.

## Hosting

GitHub Pages from `main` at the repository root, with the custom domain in `CNAME` and HTTPS enforced.  DNS is four `A` records for the bare domain pointing at GitHub Pages, plus a `www` CNAME to `ohmybahgosh.github.io`.

## License

[MIT](LICENSE).  The projects shown here have their own licenses in their own repos.

<div align="center">
<br>
<sub>Made in Michigan by <a href="https://github.com/ohmybahgosh">OhMyBahGosh</a>.  Not affiliated with LG Electronics.</sub>
</div>

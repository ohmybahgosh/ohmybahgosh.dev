# ohmybahgosh.dev

Source for **[ohmybahgosh.dev](https://ohmybahgosh.dev)**, a showcase of my LG webOS homebrew:

- **[TiviBro](https://ohmybahgosh.dev/tivibro/)**: the IPTV player LG TVs never got
- **[LG-USB-2-ETH0](https://ohmybahgosh.dev/lg-usb-2-eth0/)**: make a USB Ethernet adapter the TV's `eth0`
- **[WEBOS-ENTWARE-INSTALLER](https://ohmybahgosh.dev/webos-entware-installer/)**: one-line Entware for rooted webOS

Plain HTML, CSS and JS.  No framework, no bundler, no trackers.  Served by GitHub Pages.

## Features

- Typed terminal demos on every page (they render instantly with reduced motion)
- Live stars, forks, latest release and last push from the GitHub API, cached for 30 minutes
- Command palette: press `/` or `Ctrl K` / `⌘K`
- Copy buttons on every install command
- Fonts (JetBrains Mono, Space Grotesk) and TiviBro screenshots load through jsDelivr, so they stay in sync

## Layout

```
index.html                           home
tivibro/index.html                   repo pages
lg-usb-2-eth0/index.html
webos-entware-installer/index.html
404.html
assets/css/site.css                  all styles
assets/js/site.js                    terminals, GitHub stats, palette, copy, tabs
```

## Editing

Each page is plain HTML: edit it and push.  The header and footer are repeated in every page, so change all five when you change one.  Preview locally with:

```sh
python3 -m http.server 8000   # http://localhost:8000
```

Terminal demos are the JSON inside each `<script type="text/x-term">`: `["$", "command"]` types a command, `["o", "html"]` prints a line, `["o!", ...]` prints with a longer pause, and `["p", 800]` waits.

## Hosting

GitHub Pages from `main` at the repository root, with the custom domain in `CNAME`.

## License

MIT.  Made by [OhMyBahGosh](https://github.com/ohmybahgosh).

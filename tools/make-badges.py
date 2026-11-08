#!/usr/bin/env python3
"""Release and star badges for the GitHub profile README, served from ohmybahgosh.dev/badges/.

shields.io's GitHub badges depend on its own GitHub token pool and sometimes time out, so
these are drawn here from data/repos.json, which the deploy fetches with the repo's own token.
Same look as shields' flat-square style.

  python3 tools/make-badges.py data/repos.json badges
"""
import html, json, os, sys

# repo name -> (file prefix, release colour, stars colour)
BADGES = {
    'TiviBro': ('tivibro', '5b8cff', '33e1ff'),
    'LG-USB-2-ETH0': ('lg-usb-2-eth0', '3ddc97', '3ddc97'),
    'WEBOS-ENTWARE-INSTALLER': ('entware', 'ff3ea5', 'ff3ea5'),
    'LG-WEBOS-SSH-DOCTOR': ('ssh-doctor', '3ddc97', '3ddc97'),
    'WEBOS-LUNA-SEND-ATLAS': ('luna-atlas', '3ddc97', '33e1ff'),
    'pipseek': ('pipseek', '4c9eff', '4c9eff'),
}
LABEL_BG = '0a0e1a'

# Verdana 11px advance widths, close enough for badge sizing (textLength makes it exact)
W = {**{c: 7.0 for c in '0123456789'}, 'a': 6.8, 'b': 6.9, 'c': 5.9, 'd': 6.9, 'e': 6.7, 'f': 3.9, 'g': 6.9,
     'h': 7.0, 'i': 3.0, 'j': 3.8, 'k': 6.5, 'l': 3.0, 'm': 10.7, 'n': 7.0, 'o': 6.7, 'p': 6.9, 'q': 6.9,
     'r': 4.7, 's': 5.7, 't': 4.3, 'u': 7.0, 'v': 6.5, 'w': 9.0, 'x': 6.5, 'y': 6.5, 'z': 5.8,
     '.': 3.6, '-': 4.3, ' ': 3.5, ',': 3.6}

def width(t):
    return sum(W.get(c, 7.5) for c in t)

def badge(label, value, colour):
    lw, vw = round(width(label)) + 12, round(width(value)) + 12
    tw = lw + vw
    l, v = html.escape(label), html.escape(value)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="20" role="img" aria-label="{l}: {v}">'
            f'<title>{l}: {v}</title><g shape-rendering="crispEdges">'
            f'<rect width="{lw}" height="20" fill="#{LABEL_BG}"/><rect x="{lw}" width="{vw}" height="20" fill="#{colour}"/></g>'
            f'<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11" text-rendering="geometricPrecision">'
            f'<text x="{lw / 2:.1f}" y="14" textLength="{lw - 12}" lengthAdjust="spacingAndGlyphs">{l}</text>'
            f'<text x="{lw + vw / 2:.1f}" y="14" textLength="{vw - 12}" lengthAdjust="spacingAndGlyphs">{v}</text></g></svg>\n')

def main(src, out):
    repos = json.load(open(src)).get('repos', {})
    os.makedirs(out, exist_ok=True)
    for name, (slug, rel_c, star_c) in BADGES.items():
        r = repos.get(name)
        if not r:
            print(f'{name}: no data, keeping the badges already there')
            continue
        tag = r.get('tag') or 'none yet'
        stars = r.get('stars')
        open(os.path.join(out, f'{slug}-release.svg'), 'w').write(badge('release', tag, rel_c))
        if stars is not None:
            open(os.path.join(out, f'{slug}-stars.svg'), 'w').write(badge('stars', f'{stars:,}', star_c))
        print(f'{name}: {tag} · ★{stars}')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'data/repos.json', sys.argv[2] if len(sys.argv) > 2 else 'badges')

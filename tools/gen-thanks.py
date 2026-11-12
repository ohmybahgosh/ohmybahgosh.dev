#!/usr/bin/env python3
"""Special thanks on project pages: everyone who has helped build a project, from the
assets/thanks.json its own repo keeps up to date (its Thanks workflow).  Written into
the page between <!-- thanks:REPO:start --> and <!-- thanks:REPO:end -->.

    python3 tools/gen-thanks.py

Runs in the deploy workflow, so the list follows the repo without a commit here.
Standard library only.
"""
import html, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {"LG-USB-2-ETH0": "lg-usb-2-eth0/index.html"}
EMPTY = '<p class="thanks-empty">Nobody yet.  Test a driver, send a compatibility report, or open a pull request, and your name goes here.</p>'


def render(people):
    if not people:
        return EMPTY
    e = lambda s: html.escape(str(s), quote=True)
    rows = "\n".join('        <a class="thank" href="%s" target="_blank" rel="noopener"><img loading="lazy" src="%s" width="56" height="56" alt=""><span><b>%s</b><small>%s</small></span></a>'
                     % (e(p["url"]), e(p["avatar"] + ("&" if "?" in p["avatar"] else "?") + "s=112"), e(p["login"]), e(p["what"])) for p in people)
    return '<div class="thanks">\n%s\n      </div>' % rows


def main():
    bad = 0
    for repo, page in PAGES.items():
        url = "https://raw.githubusercontent.com/ohmybahgosh/%s/main/assets/thanks.json" % repo
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ohmybahgosh.dev-thanks"}), timeout=30) as r:
                people = json.load(r)["people"]
        except Exception as ex:
            print("%s: %s, keeping the page's list" % (repo, ex), file=sys.stderr)
            bad += 1
            continue
        f = os.path.join(ROOT, page)
        s = open(f, encoding="utf-8").read()
        start, end = "<!-- thanks:%s:start -->" % repo, "<!-- thanks:%s:end -->" % repo
        a, b = s.find(start), s.find(end)
        if a < 0 or b < a:
            print("%s has no %s block" % (page, start), file=sys.stderr)
            bad += 1
            continue
        new = s[:a + len(start)] + "\n      " + render(people) + "\n      " + s[b:]
        if new != s:
            open(f, "w", encoding="utf-8").write(new)
        print("%s: %d people" % (page, len(people)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

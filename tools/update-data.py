#!/usr/bin/env python3
"""Fetch live info about the showcased repos and write data/repos.json.

Runs in the deploy workflow (every few hours and on every push), so the site
always shows the latest versions, releases, commits and stats without anyone
editing a page.  Uses only the standard library.  Set GITHUB_TOKEN for a higher
API rate limit; it works without one for occasional local runs.
"""
import json, os, re, sys, urllib.request, urllib.error, datetime, pathlib

OWNER = "ohmybahgosh"
# repo name -> file holding a VERSION="x.y.z" line (used when there's no release yet)
REPOS = {
    "TiviBro": None,
    "LG-USB-2-ETH0": "LG-USB-2-ETH0.sh",
    "WEBOS-ENTWARE-INSTALLER": "webos-entware-installer.sh",
    "pipseek": None,
}
TOKEN = os.environ.get("GITHUB_TOKEN")


def get(path, raw=False):
    url = path if path.startswith("http") else f"https://api.github.com/{path}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
        "User-Agent": "ohmybahgosh.dev-data",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return body.decode("utf-8", "replace") if raw else json.loads(body)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def notes(md, limit=900):
    """Release notes as short plain text."""
    md = md or ""
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"^#+\s*", "", md, flags=re.M)
    md = re.sub(r"^\s*[-*+]\s+", "• ", md, flags=re.M)
    md = re.sub(r"[*_`>|]", "", md)
    md = re.sub(r"\s+", " ", md).strip()
    return md[:limit].rsplit(" ", 1)[0] + "…" if len(md) > limit else md


def repo_data(name, version_file):
    base = f"repos/{OWNER}/{name}"
    info = get(base)
    rels = get(f"{base}/releases?per_page=10") or []
    commits = get(f"{base}/commits?per_page=6") or []
    rels = [r for r in rels if not r.get("draft")]

    script_version = None
    if version_file:
        src = get(f"{base}/contents/{version_file}", raw=True)
        m = re.search(r'^\s*VERSION="?([0-9][^"\s]*)"?', src or "", re.M)
        script_version = m.group(1) if m else None

    latest = rels[0] if rels else None
    stable = next((r for r in rels if not r.get("prerelease")), None)
    tag = latest["tag_name"] if latest else (f"v{script_version}" if script_version else None)
    version = tag[1:] if tag and tag.startswith("v") else tag
    downloads = sum(a.get("download_count", 0) for r in rels for a in r.get("assets", []))

    return {
        "name": name,
        "description": info.get("description"),
        "url": info.get("html_url"),
        "homepage": info.get("homepage"),
        "topics": info.get("topics", []),
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "issues": info.get("open_issues_count", 0),
        "pushed": info.get("pushed_at"),
        "tag": tag,                                   # e.g. v0.6.0-alpha.57 or v2.6.0
        "version": version,                           # tag without the leading v
        "version_name": latest["name"] if latest and latest.get("name") else tag,
        "prerelease": bool(latest and latest.get("prerelease")),
        "released": latest.get("published_at") if latest else None,
        "stable": stable["tag_name"] if stable else None,
        "main_version": script_version,               # VERSION= on the main branch (may be ahead of the release)
        "downloads": downloads,
        "releases": [{
            "tag": r["tag_name"], "name": r.get("name") or r["tag_name"], "pre": r.get("prerelease", False),
            "at": r.get("published_at") or r.get("created_at"), "url": r["html_url"], "notes": notes(r.get("body")),
        } for r in rels[:8]],
        "commits": [{
            "msg": c["commit"]["message"].split("\n")[0][:140], "at": c["commit"]["author"]["date"],
            "url": c["html_url"], "sha": c["sha"][:7],
        } for c in commits],
    }


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "data/repos.json")
    data = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "repos": {}}
    for name, vf in REPOS.items():
        data["repos"][name] = repo_data(name, vf)
        r = data["repos"][name]
        print(f"{name}: {r['tag']} · ★{r['stars']} · {len(r['releases'])} releases · {r['downloads']} downloads")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()

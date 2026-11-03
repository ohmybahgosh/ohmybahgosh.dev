#!/usr/bin/env python3
"""Build the Homebrew Channel repository file served at https://ohmybahgosh.dev/repo.

Reads homebrew/sources.json, finds each repo's latest GitHub release, downloads the
manifest attached to it, and writes `repo` (an extensionless JSON file, the same way
tivibro.app serves its repository, so GitHub Pages serves it at /repo with no redirect).

Output is deterministic, so the workflow only commits when a release actually changed.
Usage: python3 tools/build-hb-repo.py [output-path]   (GITHUB_TOKEN optional)
"""
import json, os, sys, urllib.request, urllib.error, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = os.environ.get("GITHUB_TOKEN")


def get_json(url, api=True):
    headers = {"User-Agent": "ohmybahgosh.dev-hb-repo"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def latest_release(repo, allow_pre):
    rels = get_json(f"https://api.github.com/repos/{repo}/releases?per_page=20")
    for r in rels:
        if r.get("draft"):
            continue
        if r.get("prerelease") and not allow_pre:
            continue
        return r
    return None


def build():
    cfg = json.loads((ROOT / "homebrew" / "sources.json").read_text())
    packages = []
    for src in cfg["packages"]:
        rel = latest_release(src["repo"], src.get("prerelease", False))
        if not rel:
            print(f"skip {src['repo']}: no release", file=sys.stderr)
            continue
        asset = next((a for a in rel.get("assets", []) if a["name"] == src["manifest"]), None)
        if not asset:
            print(f"skip {src['repo']} {rel['tag_name']}: no {src['manifest']}", file=sys.stderr)
            continue
        manifest_url = f"https://github.com/{src['repo']}/releases/download/{rel['tag_name']}/{src['manifest']}"
        manifest = get_json(manifest_url, api=False)
        pkg = {
            "id": manifest["id"],
            "title": manifest.get("title", manifest["id"]),
            "iconUri": manifest.get("iconUri", ""),
            "manifestUrl": manifest_url,
            "manifest": manifest,
            "shortDescription": src.get("shortDescription") or manifest.get("appDescription", ""),
        }
        if src.get("fullDescriptionUrl"):
            pkg["fullDescriptionUrl"] = src["fullDescriptionUrl"]
        if src.get("requirements"):
            pkg["requirements"] = src["requirements"]
        pkg["release"] = {"tag": rel["tag_name"], "published": rel.get("published_at"), "url": rel["html_url"]}
        packages.append(pkg)
        print(f"{manifest['id']} {manifest.get('version')} ({rel['tag_name']})")
    n = len(packages)
    return {"paging": {"page": 1, "count": n, "maxPage": 1, "itemsTotal": n}, "packages": packages}


def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "repo"
    data = build()
    if not data["packages"]:
        sys.exit("no packages built; leaving the existing file alone")
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    out.write_text(text)
    # repo.json: the same file with an extension, so browsers show it instead of downloading it
    out.with_name(out.name + ".json").write_text(text)
    print("wrote", out, "and", out.name + ".json")


if __name__ == "__main__":
    main()

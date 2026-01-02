# download_assets.py
# 외부 리소스(src/href)를 내려받아 로컬 assets/로 옮기고 HTML을 치환합니다.
# - 로컬에서 실행 (인터넷 필요)
# - 예시:
#     python tools/download_assets.py index.html --out assets

import argparse
import re
from urllib.parse import urlparse, urlsplit
import pathlib
import requests

ASSET_RE = re.compile(r'''(?P<prefix>(?:src|href)=["'])(?P<url>https?://[^"']+)(?P<suffix>["'])''', re.IGNORECASE)

def safe_relpath(url: str) -> str:
    u = urlsplit(url)
    path = u.path or "/index"
    if path.endswith("/"):
        path += "index"
    return path.lstrip("/")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="input html (e.g. index.html)")
    ap.add_argument("--out", default="assets", help="asset output dir")
    ap.add_argument(
        "--domains",
        default="cdn.imweb.me,static.imweb.me,vendor-cdn.imweb.me,static-cdn.crm.imweb.me",
        help="comma separated allowlist"
    )
    args = ap.parse_args()

    allow = {d.strip() for d in args.domains.split(",") if d.strip()}

    html_path = pathlib.Path(args.html)
    html = html_path.read_text(encoding="utf-8", errors="ignore")

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    repls = {}

    for m in ASSET_RE.finditer(html):
        url = m.group("url")
        dom = urlparse(url).netloc
        if dom not in allow:
            continue

        rel = safe_relpath(url)
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)

        if url in repls:
            continue

        print("GET", url)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        target.write_bytes(r.content)

        repls[url] = f"{out_dir.name}/{rel}"

    for url, local in repls.items():
        html = html.replace(url, local)

    out_html = html_path.with_name("index.localized.html")
    out_html.write_text(html, encoding="utf-8")
    print("Wrote:", out_html)
    print("Downloaded assets:", len(repls))

if __name__ == "__main__":
    main()

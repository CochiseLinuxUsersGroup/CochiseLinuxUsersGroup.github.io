#!/usr/bin/env python3
"""
Incremental mirror of the cochiselinux FreeLists archive into /archive/.

Fetches the FreeLists archive (index -> month threads pages -> individual
posts) and writes ONE page per thread under /archive/: the main message shown
first, then replies nested/indented beneath it (based on FreeLists'
"By Threads" view).  Months before MIN_YEAR are ignored and removed, and
progress is recorded in tools/archive_state.json so re-runs only fetch what is
missing and an interrupted sync (e.g. the PC was powered off) resumes.

Run:  python3 tools/fetch_archive.py            (full/next sync)
      python3 tools/fetch_archive.py --all      (force refetch of every post)

Designed to be triggered weekly by .github/workflows/archive.yml.
"""

import email.utils
import html
import json
import os
import re
import shutil
import sys
import time
import urllib.request
from datetime import datetime
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "archive")
STATE_FILE = os.path.join(ROOT, "tools", "archive_state.json")

BASE = "https://www.freelists.org"
ARCHIVE_URL = BASE + "/archive/cochiselinux"
HEADERS = {"User-Agent": "Mozilla/5.0 (Cochise Linux Users Group archive mirror)"}
SLEEP = 0.5
MIN_YEAR = 2015  # do not mirror anything posted before this year

ALLOWED_TAGS = {
    "p", "br", "a", "img", "div", "span", "ul", "ol", "li", "b", "strong",
    "i", "em", "u", "blockquote", "pre", "code", "hr", "h1", "h2", "h3",
    "h4", "h5", "h6", "small", "table", "thead", "tbody", "tr", "th", "td",
}
VOID_TAGS = {"br", "hr", "img"}


class Sanitizer(HTMLParser):
    """Strips scripts/styles/ads, keeps a small whitelist, fixes URLs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe", "form", "noscript"):
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag not in ALLOWED_TAGS:
            return
        if re.fullmatch(r"h[1-6]", tag):
            tag = "h3"
        allowed = {}
        for k, v in attr_safe_attrs(tag, attrs):
            if v is None:
                continue
            allowed[k] = html.escape(v, quote=True)
        attrs_str = "".join(
            f' {k}="{v}"' for k, v in sorted(allowed.items())
        )
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe", "form", "noscript"):
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth or tag not in ALLOWED_TAGS:
            return
        if tag in VOID_TAGS:
            return
        if re.fullmatch(r"h[1-6]", tag):
            tag = "h3"
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(html.escape(data))

    def output(self):
        return "".join(self.parts)


def attr_safe_attrs(tag, attrs):
    for k, v in attrs:
        if k in ("href", "src"):
            yield k, absolutize(v)
        elif k in ("alt", "title", "width", "height", "colspan", "rowspan"):
            yield k, v


def absolutize(url):
    """Make href/src absolute; only allow http(s) links. Reject javascript:."""
    url = (url or "").strip()
    if url.lower().startswith(("javascript:", "data:", "vbscript:")):
        return ""
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return BASE + url
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return url


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read().decode("utf-8", "replace")


def safe_slug(raw):
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", raw).strip("-.")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "message"


def clean_subject(raw):
    s = html.unescape(raw).strip()
    s = re.sub(r"^\[cochiselinux\]\s*", "", s)
    return s


def month_key(mm_yyyy):
    mm, yyyy = mm_yyyy.split("-")
    return int(yyyy), int(mm)


def month_title(mm_yyyy):
    yyyy, mm = month_key(mm_yyyy)
    return datetime(yyyy, mm, 1).strftime("%B %Y")


def parse_date(date_str):
    try:
        return email.utils.parsedate_to_datetime(date_str.strip())
    except Exception:
        for fmt in ("%b %d, %Y", "%B %d, %Y", "%a, %d %b %Y %H:%M:%S %z"):
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except Exception:
                continue
    return None


def get_months():
    index = fetch(ARCHIVE_URL)
    months = set(re.findall(r'"/archive/cochiselinux/(\d{2}-\d{4})"', index))
    months = {m for m in months if month_key(m)[0] >= MIN_YEAR}
    return sorted(months, key=month_key)


class ThreadParser(HTMLParser):
    """Parses the ?threads=1 month page into a tree of message nodes."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.roots = []
        self.stack = []
        self.cur = None
        self.in_anchor = False
        self.buf = ""

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            if self.cur is not None:
                self.stack.append(self.cur)
            self.cur = {"title": "", "slug": "", "author": "", "children": []}
            self.in_anchor = False
            self.buf = ""
        elif tag == "a" and self.cur is not None:
            href = dict(attrs).get("href", "")
            m = re.match(r"/post/cochiselinux/(.+)$", href)
            if m:
                self.cur["slug"] = m.group(1)
                self.in_anchor = True
                self.buf = ""

    def handle_data(self, data):
        if self.cur is None:
            return
        if self.in_anchor:
            self.buf += data
        elif self.cur["slug"]:
            self.cur["author"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.in_anchor and self.cur is not None:
            self.cur["title"] = self.buf.strip()
            self.in_anchor = False
        elif tag == "li" and self.cur is not None:
            node = self.cur
            node["author"] = re.sub(r"^\s*-\s*", "", node["author"]).strip()
            self.cur = self.stack.pop() if self.stack else None
            if self.cur is not None:
                self.cur["children"].append(node)
            else:
                self.roots.append(node)


def flush_empties(nodes):
    """Drop slug-less nodes, splicing their children in their place."""
    out = []
    for n in nodes:
        n["children"] = flush_empties(n["children"])
        if not n["slug"]:
            out.extend(n["children"])
        else:
            out.append(n)
    return out


def get_thread_tree(mm_yyyy):
    page = fetch(f"{ARCHIVE_URL}/{mm_yyyy}?threads=1")
    p = ThreadParser()
    p.feed(page)
    return flush_empties(p.roots)


def flatten_thread(nodes):
    slugs = []
    for n in nodes:
        slugs.append(n["slug"])
        slugs.extend(flatten_thread(n["children"]))
    return slugs


def get_post(slug):
    page = fetch(f"{BASE}/post/cochiselinux/{slug}")
    m = re.search(r'<h1 class="h3">([^<]+)</h1>', page)
    subject = clean_subject(m.group(1)) if m else slug
    m = re.search(
        r'<p class="text-muted"><small>From:\s*(.*?)<br>\s*'
        r'Date:\s*(.*?)</small></p>',
        page,
        re.S,
    )
    author, date_str = ("", "")
    if m:
        author = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip())
        author = re.sub(r"\s*&lt;.*&gt;\s*$", "", author)
        author = re.sub(r"\s*<.*>\s*$", "", author).strip()
        date_str = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)).strip())
    dt = parse_date(date_str) if date_str else None

    start = page.find("</small></p>")
    end = page.find('<a name="footer">')
    if end == -1:
        end = page.find("<h3>Other related posts:")
    if start == -1:
        body = ""
    else:
        body = page[start + len("</small></p>") : end if end > start else len(page)]

    body = re.sub(
        r'<div[^>]*id="ezoic-pub-ad-placeholder-\d+"[^>]*>.*?</div>',
        "",
        body,
        flags=re.S,
    )

    san = Sanitizer()
    san.feed(body)

    return {
        "title": subject,
        "author": author,
        "date_str": date_str,
        "date_iso": dt.strftime("%Y-%m-%dT%H:%M:%S%z") if dt else "",
        "date_display": dt.strftime("%b %d, %Y") if dt else "",
        "url": f"{BASE}/post/cochiselinux/{slug}",
        "body": san.output(),
    }


def load_state():
    state = {"posts": {}}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state.update(json.load(f))
    migrate_state(state)
    return state


def migrate_state(state):
    """Old state versions keyed posts by month/local-slug; normalize to raw slug.
    Their pages are also outdated (single-message pages replaced by threads)."""
    posts = state.setdefault("posts", {})
    keys_are_old = all(k.count("/") > 0 for k in list(posts)[:200])
    if posts and keys_are_old:
        migrated = {}
        for key, post in posts.items():
            if isinstance(post, dict) and "url" in post:
                m = re.search(r"/post/cochiselinux/([^/]+)$", post["url"])
                if m:
                    migrated[m.group(1)] = post
        state["posts"] = migrated
    state["posts"] = {
        k: v for k, v in state["posts"].items()
        if isinstance(v, dict) and "url" in v
    }


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
        f.write("\n")


def render_message(node, month, depth):
    post = node.get("_post") or {
        "title": node["title"],
        "author": node["author"],
        "date_display": "",
        "url": f"{BASE}/post/cochiselinux/{node['slug']}",
        "body": "",
    }
    indent = depth * 2
    sub = ""
    for child in sorted(node["children"], key=lambda c: c["title"].lower()):
        sub += render_message(child, month, depth + 1)
    head = f'<span class="icon fa-envelope-o"></span>' if depth == 0 else ""
    meta = f"From {html.escape(post['author'] or '—')}"
    if post["date_display"]:
        meta += f" &middot; {html.escape(post['date_display'])}"
    return f"""
<div class="mail-card" style="margin-left:{indent}em;">
    <h3>{head} {html.escape(post['title'])}</h3>
    <p style="font-size:0.85em;"><em>{meta}</em></p>
    <div class="mail-body">
{post['body']}
    </div>
    <p style="font-size:0.8em; margin-bottom:0.25em;">
        <a href="{post['url']}" target="_blank" rel="noopener"><i class="fa fa-external-link"></i> View original on FreeLists</a>
    </p>
</div>
{sub}"""


def render_thread_page(roots, month):
    root = roots[0] if roots else None
    title = (root.get("_post") or {}).get("title") or (root["title"] if root else month)
    posts_joined = "".join(render_message(r, month, 0) for r in roots)
    total = len(flatten_thread(roots))
    meta = f"{total} message{'s' if total != 1 else ''}"
    if roots and roots[0].get("_post"):
        p = roots[0]["_post"]
        meta += f" &middot; started by {html.escape(p['author'] or '—')} on {html.escape(p['date_display'])}"
    page = """---
layout: default
title: __TITLE__ | CLUG Mailing List Archive
description: __DESC__ — __META__ from the cochiselinux mailing list archive.
---

<header class="special container">
    <span class="icon fa-envelope-o"></span>
    <h1>__TITLE__</h1>
    <p>__META__</p>
</header>

<section class="wrapper style1 container">
    <div class="row">
        <div class="12u">
            {% raw %}
__THREAD__
            {% endraw %}
        </div>
    </div>
    <hr />
    <p style="text-align:center; font-size:0.9em;">
        <a href="../"><i class="fa fa-archive"></i> Back to __MONTH__</a>
    </p>
</section>
"""
    return (
        page.replace("__TITLE__", html.escape(title, quote=True))
        .replace("__DESC__", html.escape(title))
        .replace("__META__", meta)
        .replace("__THREAD__", posts_joined)
        .replace("__MONTH__", html.escape(month_title(month)))
    )


def render_month_page(mm_yyyy, roots):
    lines = []
    for r in roots:
        post = r.get("_post")
        rtitle = post["title"] if post else r["title"]
        n = len(flatten_thread([r]))
        lines.append(
            f'<li><a href="{safe_slug_unique(r)}/">{html.escape(rtitle)}</a>'
            f" &mdash; <strong>{html.escape((post or {}).get('author') or r.get('author') or '')}</strong>"
            f" <em>({html.escape((post or {}).get('date_display') or '')})</em>"
            f" <small><span class=\"badge\">{n} msg{'s' if n != 1 else ''}</span></small></li>"
        )
    return f"""---
layout: default
title: {month_title(mm_yyyy)} Mailing List Archive | CLUG
description: {len(roots)} thread{'s' if len(roots) != 1 else ''} posted to the cochiselinux mailing list in {month_title(mm_yyyy)}.
---

<header class="special container">
    <span class="icon fa-envelope-o"></span>
    <h1>{month_title(mm_yyyy)}</h1>
    <p>{len(roots)} thread{'s' if len(roots) != 1 else ''}</p>
</header>

<section class="wrapper style1 container">
    <ul class="default">
{chr(10).join(lines)}
    </ul>
</section>
"""


def safe_slug_unique(node):
    return safe_slug(node["slug"])


def render_landing(years, totals):
    blocks = []
    for yyyy in sorted(years.keys(), reverse=True):
        chips = " ".join(
            f'<a href="{mm:02d}-{yyyy}/" class="button special small">{datetime(yyyy, mm, 1).strftime("%b %Y")}</a>'
            for mm in sorted(years[yyyy])
        )
        blocks.append(
            f'<h3>{yyyy}</h3>\n<div class="box" style="margin-bottom:1.5em;">{chips}</div>'
        )
    total = sum(totals.values())
    return f"""---
layout: default
title: Mailing List Archive | Cochise Linux User Group
description: Browse the full cochiselinux mailing list archive — meeting reminders, questions and community discussion, mirrored from FreeLists.
---

<header class="special container">
    <span class="icon fa-envelope-o"></span>
    <h1>Mailing List Archive</h1>
    <p>{total} messages &middot; past discussions, meeting reminders &amp; quick help &middot; mirrored from FreeLists weekly</p>
</header>

<section class="wrapper style1 container">
    <div class="row">
        <div class="12u">
            <p>Browse past discussions from the cochiselinux mailing list. Want to join the conversation?
            <a href="/mailinglist">Subscribe to the mailing list</a> — or
            <a href="https://www.freelists.org/archive/cochiselinux" target="_blank" rel="noopener">view the original archive on FreeLists</a>.</p>
            <hr />
{chr(10).join(blocks)}
        </div>
    </div>
</section>
"""


def remove_old_months(months):
    wanted = set(months)
    for name in sorted(os.listdir(OUT)):
        path = os.path.join(OUT, name)
        if os.path.isdir(path) and name not in wanted:
            print(f"  remove pre-{MIN_YEAR} month {name}")
            shutil.rmtree(path, ignore_errors=True)


def main():
    force = "--all" in sys.argv
    state = load_state()
    posts = state["posts"]
    missed = set(state.get("missed", []))
    months = get_months()
    print(f"Found {len(months)} months from {MIN_YEAR}+ in the FreeLists archive.")
    remove_old_months(months)

    years = {}
    totals = {}
    for mm_yyyy in months:
        yyyy, mm = month_key(mm_yyyy)
        try:
            roots = get_thread_tree(mm_yyyy)
        except Exception as exc:
            print(f"  skip {mm_yyyy}: {exc}")
            time.sleep(SLEEP)
            continue

        missing = [s for s in flatten_thread(roots) if s not in posts and s not in missed]
        for slug in missing:
            print(f"    fetch {slug}")
            try:
                posts[slug] = get_post(slug)
            except Exception as exc:
                print(f"      ERROR {slug}: {exc}")
                missed.add(slug)
                time.sleep(SLEEP)
                continue
            if not force:
                time.sleep(SLEEP)

        def attach(node):
            if node["slug"] in posts:
                node["_post"] = posts[node["slug"]]
            for c in node["children"]:
                attach(c)

        for r in roots:
            attach(r)

        out_dir = os.path.join(OUT, mm_yyyy)
        shutil.rmtree(out_dir, ignore_errors=True)
        os.makedirs(out_dir, exist_ok=True)

        used_slugs = set()
        for r in roots:
            local = safe_slug(r["slug"])
            n = 1
            while local in used_slugs:
                local = f"{safe_slug(r['slug'])}-{n}"
                n += 1
            used_slugs.add(local)
            d = os.path.join(out_dir, local)
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
                f.write(render_thread_page([r], mm_yyyy))

        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_month_page(mm_yyyy, roots))

        years.setdefault(yyyy, set()).add(mm)
        totals[yyyy] = totals.get(yyyy, 0) + len(flatten_thread(roots))
        print(f"  {mm_yyyy}: {len(roots)} threads / {len(flatten_thread(roots))} messages")
        save_state(state)

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_landing(years, totals))

    state["missed"] = sorted(missed)
    save_state(state)
    print(f"Done. {len(posts)} posts cached; mirrored into {OUT}/")


if __name__ == "__main__":
    main()
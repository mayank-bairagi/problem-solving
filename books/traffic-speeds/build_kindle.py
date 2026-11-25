#!/usr/bin/env python3
"""Build the Kindle ebook: build/how-fast-is-this-road.epub

Steps: SVG diagrams -> PNG (headless Chrome), cover, chapters -> EPUB (pandoc).
Run from anywhere:  python3 build_kindle.py
Needs: google-chrome, and pandoc on PATH or under build/tools/.
"""
import glob, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

BOOK = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BOOK, "build")
PNG = os.path.join(BUILD, "png")
MD = os.path.join(BUILD, "md")
OUT = os.path.join(BUILD, "how-fast-is-this-road.epub")

TITLE = "How Fast Is This Road?"
SUBTITLE = "Data engineering concepts through one simple use case at a map company"
AUTHOR = "Mayank Bairagi"
SCALE = 2          # PNG pixels per SVG unit; 2 keeps text sharp on e-ink


def find_pandoc():
    local = sorted(glob.glob(os.path.join(BUILD, "tools", "pandoc-*", "bin", "pandoc")))
    exe = local[-1] if local else shutil.which("pandoc")
    if not exe:
        sys.exit("pandoc not found: install it or unpack a release under build/tools/")
    return exe


def chrome_png(src_html, out_png, width, height, scale):
    with tempfile.TemporaryDirectory(dir=BUILD) as profile:
        subprocess.run(
            ["google-chrome", "--headless=new", "--no-sandbox", "--hide-scrollbars",
             f"--user-data-dir={profile}", f"--force-device-scale-factor={scale}",
             f"--window-size={width},{height}", f"--screenshot={out_png}",
             "file://" + src_html],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def svg_to_png(svg):
    name = os.path.splitext(os.path.basename(svg))[0]
    out = os.path.join(PNG, name + ".png")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(svg):
        return out
    head = open(svg).read(600)
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    if not m:
        sys.exit(f"no viewBox in {svg}")
    w, h = int(float(m.group(1))), int(float(m.group(2)))
    html = os.path.join(PNG, name + ".html")
    with open(html, "w") as f:
        f.write(f'<body style="margin:0;background:#fff"><img src="file://{svg}" width="{w}" height="{h}"></body>')
    chrome_png(html, out, w, h, SCALE)
    os.remove(html)
    return out


def make_cover():
    w, h = 1600, 2560
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif">
<rect width="{w}" height="{h}" fill="#fff"/>
<rect x="60" y="60" width="{w-120}" height="{h-120}" fill="none" stroke="#222" stroke-width="6"/>
<text x="800" y="620" font-size="150" font-weight="bold" text-anchor="middle" fill="#111">How Fast Is</text>
<text x="800" y="800" font-size="150" font-weight="bold" text-anchor="middle" fill="#111">This Road?</text>
<line x1="300" y1="920" x2="1300" y2="920" stroke="#222" stroke-width="5"/>
<text x="800" y="1040" font-size="56" text-anchor="middle" fill="#333">Data engineering concepts through</text>
<text x="800" y="1120" font-size="56" text-anchor="middle" fill="#333">one simple use case at a map company</text>
<g stroke="#222" stroke-width="5" fill="#e6e6e6">
<rect x="250" y="1400" width="300" height="130" rx="14"/><rect x="650" y="1400" width="300" height="130" rx="14" fill="#fff"/><rect x="1050" y="1400" width="300" height="130" rx="14"/>
<line x1="550" y1="1465" x2="650" y2="1465"/><line x1="950" y1="1465" x2="1050" y2="1465"/>
</g>
<text x="400" y="1482" font-size="48" text-anchor="middle" fill="#111">pings</text>
<text x="800" y="1482" font-size="48" text-anchor="middle" fill="#111">log</text>
<text x="1200" y="1482" font-size="48" text-anchor="middle" fill="#111">speed</text>
<text x="800" y="1700" font-size="46" font-style="italic" text-anchor="middle" fill="#444">Kafka · Flink · Spark · Iceberg · Trino · Athena</text>
<text x="800" y="1770" font-size="46" font-style="italic" text-anchor="middle" fill="#444">Postgres · DynamoDB · Airflow</text>
<text x="800" y="2300" font-size="70" text-anchor="middle" fill="#111">{AUTHOR}</text>
</svg>'''
    src = os.path.join(BUILD, "cover.svg")
    open(src, "w").write(svg)
    html = os.path.join(BUILD, "cover.html")
    open(html, "w").write(f'<body style="margin:0"><img src="file://{src}" width="{w}" height="{h}"></body>')
    out = os.path.join(BUILD, "cover.png")
    chrome_png(html, out, w, h, 1)
    os.remove(html)
    return out


CSS = """
body { line-height: 1.4; }
h1 { page-break-before: always; margin-top: 1em; }
h2 { margin-top: 1.4em; }
img { max-width: 100%; height: auto; display: block; margin: 0.8em auto; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 0.85em; }
th, td { border: 1px solid #777; padding: 0.25em 0.4em; vertical-align: top; text-align: left; }
th { background: #e6e6e6; }
pre { font-size: 0.72em; line-height: 1.25; white-space: pre-wrap; word-wrap: break-word;
      border-left: 3px solid #999; padding-left: 0.6em; margin: 0.8em 0; }
code { font-size: 0.9em; }
blockquote { margin: 0.8em 1em; font-style: italic; }
"""

PART1 = """# Part I: The Story

One use case, told concept by concept. Wayline, a fictional maps and navigation company, turns GPS pings from phones into one answer: how fast is traffic on this road right now, and how does that compare with normal?

Each chapter ends with a table mapping its ideas to *Designing Data-Intensive Applications* (Martin Kleppmann, 1st edition), questions to check yourself, and an interview conversation.
"""

PART2 = """# Part II: Technology Deep Dives

Part I explained why each tool is there. Part II goes back over each technology at interview depth: how it works inside, the topics interviewers ask about with their follow-ups, and rapid-fire questions.

Snippets are illustrative and have not been compiled or run. Defaults and version-specific behaviour should be checked against the documentation for the version you use.
"""


def main():
    os.makedirs(PNG, exist_ok=True)
    shutil.rmtree(MD, ignore_errors=True)
    os.makedirs(MD)
    pandoc = find_pandoc()

    svgs = sorted(glob.glob(os.path.join(BOOK, "diagrams", "*.svg")))
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(svg_to_png, svgs))
    print(f"diagrams: {len(svgs)} PNG in {PNG}")
    cover = make_cover()

    chapters = sorted(glob.glob(os.path.join(BOOK, "[0-9][0-9]-*.md")))
    files = []
    for path in chapters:
        num = int(os.path.basename(path)[:2])
        if num == 1:
            files.append(write(os.path.join(MD, "00-part1.md"), PART1))
        if num == 10:
            files.append(write(os.path.join(MD, "09z-part2.md"), PART2))
        text = open(path).read()
        text, n = re.subn(r"\]\(diagrams/([^)]+)\.svg\)", r"](png/\1.png)", text)
        for ref in re.findall(r"\]\(png/([^)]+\.png)\)", text):
            if not os.path.exists(os.path.join(PNG, ref)):
                sys.exit(f"{path}: missing diagram {ref}")
        # links between chapters do not survive as file links in an EPUB
        text = re.sub(r"\[([^\]]+)\]\(\d\d-[^)]+\.md\)", r"\1", text)
        files.append(write(os.path.join(MD, os.path.basename(path)), text + "\n"))

    css = write(os.path.join(BUILD, "kindle.css"), CSS)
    subprocess.run(
        [pandoc, "-f", "gfm", "-t", "epub3", "-o", OUT, "--toc", "--toc-depth=1",
         "--split-level=1", "--resource-path", BUILD, "--css", css,
         "--epub-cover-image", cover,
         "--metadata", f"title={TITLE}", "--metadata", f"subtitle={SUBTITLE}",
         "--metadata", f"author={AUTHOR}", "--metadata", "lang=en-GB"] + files,
        check=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT) / 1e6:.1f} MB, {len(chapters)} chapters)")


def write(path, text):
    with open(path, "w") as f:
        f.write(text)
    return path


if __name__ == "__main__":
    main()

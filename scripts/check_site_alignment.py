"""Fail a deployment if Book sources, Lite contents or local README links drift."""
import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, parse_qs

from build_learning_media import NOTEBOOKS, PUBLISHED, ROOT
from build_resource_index import replace_index


def same_file(source, target):
    if not target.is_file() or source.read_bytes() != target.read_bytes():
        raise ValueError(f"Missing or stale published copy: {target}")


def check(site):
    toc = (ROOT / "book/_toc.yml").read_text(encoding="utf-8")
    for page in (ROOT / "README.md", ROOT / "book/visual-library.md"):
        text = page.read_text(encoding="utf-8")
        if replace_index(text) != text:
            raise ValueError(f"Stale notebook directory: {page}")
        for url in re.findall(r'https://[^\s)<>"\]]+', text):
            if not url.startswith(PUBLISHED + "/"):
                continue
            parsed = urlsplit(url[len(PUBLISHED) + 1:])
            target = site / unquote(parsed.path or "index.html")
            if not target.is_file():
                raise ValueError(f"Broken published resource link: {url}")
            if parsed.path == "lite/lab/index.html" and "path" in parse_qs(parsed.query):
                notebook = parse_qs(parsed.query)["path"][0]
                if not (site / "lite/files" / notebook).is_file():
                    raise ValueError(f"Missing launch target: {notebook}")
    notebooks = sorted(NOTEBOOKS.glob("*.ipynb"))
    for notebook in notebooks:
        if f"file: notebooks/{notebook.stem}\n" not in toc:
            raise ValueError(f"Notebook absent from Book TOC: {notebook.name}")
        same_file(notebook, site / "_sources/notebooks" / notebook.name)
        if not (site / "notebooks" / f"{notebook.stem}.html").is_file():
            raise ValueError(f"Missing Book chapter: {notebook.stem}")
    count = 0
    for source in NOTEBOOKS.rglob("*"):
        relative = source.relative_to(NOTEBOOKS)
        if not source.is_file() or any(p in {"exports", "__pycache__", ".ipynb_checkpoints"} for p in relative.parts):
            continue
        same_file(source, site / "lite/files" / relative)
        count += 1
    print(f"Aligned {len(notebooks)} Book chapters and {count} Lite content files; README/resource links resolve")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "site")
    check(parser.parse_args().site.resolve())

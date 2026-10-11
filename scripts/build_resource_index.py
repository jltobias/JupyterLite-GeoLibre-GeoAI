"""Keep README and Book navigation aligned with the canonical notebook set."""
import argparse
from pathlib import Path
from build_learning_media import NOTEBOOKS, PUBLISHED, ROOT, PROFILES, write_or_check

START = "<!-- BEGIN NOTEBOOK RESOURCES -->"
END = "<!-- END NOTEBOOK RESOURCES -->"


def resource_table(paths=None):
    paths = sorted(NOTEBOOKS.glob("*.ipynb")) if paths is None else paths
    rows = ["| Notebook | Read / run | Visual companions |", "|---|---|---|"]
    for path in paths:
        key = path.name[:2]
        title = PROFILES[key]["title"]
        media = f"{PUBLISHED}/lite/files/assets/learning/{key}"
        rows.append(f"| {key} — {title} | [Read]({PUBLISHED}/notebooks/{path.stem}.html) · "
                    f"[Run]({PUBLISHED}/lite/lab/index.html?path={path.name}) | "
                    f"[Watch]({media}/watch.html) · [Infographic]({media}/infographic.svg) · "
                    f"[Cartoon]({media}/cartoon.svg) |")
    return "\n".join(rows)


def replace_index(text):
    if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
        raise ValueError("Expected exactly one ordered resource-index marker pair")
    before, remainder = text.split(START)
    _, after = remainder.split(END)
    return before + START + "\n\n" + resource_table() + "\n\n" + END + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path in (ROOT / "README.md", ROOT / "book/visual-library.md"):
        write_or_check(path, replace_index(path.read_text(encoding="utf-8")), args.check)
    print("Verified" if args.check else "Updated", f"README/Book links for all {len(PROFILES)} notebooks")


if __name__ == "__main__":
    main()

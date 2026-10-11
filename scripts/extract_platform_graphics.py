"""Extract selected presentation images unchanged; check published provenance offline.

Reproduce with --pptx PATH --pdf PATH. The original presentation is deliberately
not distributed with the site. CI uses --check and needs only committed assets.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "book/assets/platforms"
MANIFEST = ASSETS / "provenance.json"
PRESENTATION = {
    "title": "JupyterLite: Geospatial Data Science and Global Health",
    "author": "James L. Tobias, MS, GISP",
    "presentation_date": "2026-07-10",
    "source_basename": "Jim-Tobias-Peraton-JupyterLite-Geospatial-Data-Science-and-Global-Health-7102026",
}
# Slide numbers are one-based, verified against the supplied 47-page PDF.
FIGURES = (
    ("jupyterlite-interface.png", 11, 25, "jupyterlite",
     "JupyterLite Contributors; interface and documentation screenshot.",
     "https://jupyterlite.readthedocs.io/en/stable/"),
    ("jupyterlite-deployment.png", 17, 31, "jupyterlite",
     "JupyterLite Contributors; GitHub interface and incidental advertisement retain their respective credits. No endorsement implied.",
     "https://jupyterlite.readthedocs.io/en/stable/quickstart/deploy.html"),
    ("jupyterlite-ecosystem.png", 19, 33, "jupyterlite",
     "Graphic supplied in Tobias's presentation; separate illustrator and reuse license not specified. Project names and logos belong to their respective projects.",
     None),
    ("geolibre-workspace.png", 38, 52, "geolibre",
     "GeoLibre: Qiusheng Wu and contributors. Basemap credits visible in the source: OpenFreeMap, OpenMapTiles, OpenStreetMap contributors.",
     "https://web.geolibre.app/"),
    ("geolibre-notebook-panel.png", 39, 54, "geolibre",
     "GeoLibre documentation: Qiusheng Wu and contributors; JupyterLite and JupyterLab belong to their respective contributors.",
     "https://geolibre.app/notebook/"),
    ("geolibre-python.png", 41, 58, "geolibre",
     "GeoLibre Python documentation: Qiusheng Wu and contributors. Historical screenshot, not this site's browser adapter API.",
     "https://geolibre.app/python/"),
    ("geolibre-gallery.png", 42, 59, "geolibre",
     "GeoLibre gallery: Qiusheng Wu and contributors. Visible projects credit spatialthoughts and giswqs; each project and dataset retains its own terms.",
     "https://share.geolibre.app/"),
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def png_dimensions(raw):
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        raise ValueError("Expected an original PNG image")
    return list(struct.unpack(">II", raw[16:24]))


def extract(pptx, pdf):
    """Validate the selected source slides before writing any output."""
    for source, extension in ((pptx, "pptx"), (pdf, "pdf")):
        if source.name != PRESENTATION["source_basename"] + "." + extension:
            raise ValueError("Keep the supplied original filenames for reproducible provenance")
    raw_deck = pptx.read_bytes()
    raw_pdf = pdf.read_bytes()
    images = []
    rel_ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    doc_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    pres_ns = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
    draw_ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    with zipfile.ZipFile(io.BytesIO(raw_deck)) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        rels = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        slides = [targets[s.attrib[doc_ns + "id"]]
                  for s in presentation.find(pres_ns + "sldIdLst")]
        if len(slides) != 47:
            raise ValueError("Expected the supplied 47-slide presentation")
        for name, slide, number, chapter, credit, url in FIGURES:
            expected_slide = f"slides/slide{slide}.xml"
            if slides[slide - 1] != expected_slide:
                raise ValueError(f"Unexpected slide ordering at {slide}")
            relationships = ET.fromstring(archive.read(f"ppt/slides/_rels/slide{slide}.xml.rels"))
            image_target = f"../media/image{number}.png"
            image_ids = {r.attrib["Id"] for r in relationships.findall(rel_ns + "Relationship")
                         if r.attrib["Target"] == image_target and r.attrib["Type"].endswith("/image")}
            slide_xml = ET.fromstring(archive.read("ppt/" + expected_slide))
            used = {b.attrib.get(doc_ns + "embed") for b in slide_xml.iter(draw_ns + "blip")}
            if not image_ids.intersection(used):
                raise ValueError(f"Image {number} is not embedded on slide {slide}")
            member = f"ppt/media/image{number}.png"
            raw = archive.read(member)
            record = dict(file=name, chapter=chapter, slide=slide, pptx_member=member,
                          sha256=digest(raw), bytes=len(raw), dimensions=png_dimensions(raw),
                          attribution=credit, source_url=url, transformation="none; original PNG bytes")
            images.append((record, raw))
    manifest = dict(schema_version=1, presentation=PRESENTATION,
                    source_files={"pptx": {"name": pptx.name, "sha256": digest(raw_deck)},
                                  "pdf": {"name": pdf.name, "sha256": digest(raw_pdf)}},
                    rights_note="Supplied presentation material is not relicensed as original repository artwork. Software, documentation, logos, basemaps and gallery projects retain their respective rights; see chapter figure captions and linked upstream licenses.",
                    figures=[r for r, _ in images])
    ASSETS.mkdir(parents=True, exist_ok=True)
    for record, raw in images:
        (ASSETS / record["file"]).write_bytes(raw)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return check()


def check():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1 or manifest["presentation"] != PRESENTATION:
        raise ValueError("Unexpected presentation metadata")
    if len(manifest["figures"]) != len(FIGURES):
        raise ValueError("Expected seven selected figures")
    if {p.name for p in ASSETS.glob("*.png")} != {f[0] for f in FIGURES}:
        raise ValueError("Unexpected or missing PNG assets")
    for record, expected in zip(manifest["figures"], FIGURES):
        name, slide, number, chapter, credit, url = expected
        for key, value in dict(file=name, slide=slide, pptx_member=f"ppt/media/image{number}.png",
                               chapter=chapter, attribution=credit, source_url=url,
                               transformation="none; original PNG bytes").items():
            if record[key] != value:
                raise ValueError(f"Incorrect {key} for {name}")
        raw = (ASSETS / name).read_bytes()
        if (digest(raw), len(raw), png_dimensions(raw)) != (record["sha256"], record["bytes"], record["dimensions"]):
            raise ValueError(f"Modified or damaged presentation graphic: {name}")
    for extension in ("pdf", "pptx"):
        source = manifest["source_files"][extension]
        if source["name"] != PRESENTATION["source_basename"] + "." + extension:
            raise ValueError("Unexpected source filename")
        if len(source["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in source["sha256"]):
            raise ValueError("Invalid source checksum")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pptx", type=Path)
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()
    if args.check:
        if args.pptx or args.pdf:
            parser.error("--check uses the committed provenance manifest; omit source paths")
        check()
    else:
        if not args.pptx or not args.pdf:
            parser.error("extraction requires both --pptx and --pdf source paths")
        extract(args.pptx, args.pdf)
    print(f"{'Checked' if args.check else 'Extracted'} seven unchanged presentation graphics and provenance.")


if __name__ == "__main__":
    main()

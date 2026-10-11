"""Rebuild authored notebook guides and their local, accessible visual companions.

python scripts/build_learning_media.py             # SVG/HTML/Markdown, no extras
python scripts/build_learning_media.py --videos    # also PNG/MP4; see requirements-media.txt
python scripts/build_learning_media.py --check     # verify committed copy matches source

Existing code, execution counts and outputs are preserved. Only cells marked
learning_guide are replaced. Content anchors fail closed if code cells change.
All generated illustrations are schematic; they never claim to be model outputs.
"""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import subprocess
import tempfile
import textwrap

from learning_content import LESSONS, PROFILES

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "book/notebooks"
ASSETS = NOTEBOOKS / "assets/learning"
PUBLISHED = "https://jltobias.github.io/JupyterLite-GeoLibre-GeoAI"
INK, MUTED, BLUE, TEAL, GOLD = "#14283f", "#45576c", "#2459b8", "#087f78", "#a96112"
COLORS = [BLUE, TEAL, "#7545b3", GOLD]


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=22, color=INK, weight=400, width=None, line=1.35, mono=False):
    lines = textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False) if width else [value]
    family = "monospace" if mono else "Arial, sans-serif"
    return "".join(f'<text x="{x}" y="{y+i*size*line:.1f}" font-family="{family}" '
                   f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(s)}</text>'
                   for i, s in enumerate(lines))


def rect(x, y, w, h, fill, stroke="none", radius=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def path(d, color=MUTED, width=3, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" {extra}/>'


def circle(x, y, r=8, fill=BLUE, stroke="white"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def svg(body, title, description, w=1280, h=900):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title>'
            f'<desc id="desc">{esc(description)}</desc>{body}</svg>\n')


def schematic(kind):
    """An original 540×245 vector teaching illustration, never a data plot."""
    out = rect(0, 0, 540, 245, "#f0f5fa")
    if kind in {"map", "footprints", "risk", "triage"}:
        for x in range(30, 520, 50):
            out += path(f"M{x} 15 V210", "#d3dfeb", 1)
        for y in range(30, 220, 40):
            out += path(f"M20 {y} H520", "#d3dfeb", 1)
        out += path("M10 160 Q120 30 215 100 T530 70", "#acd2e6", 28)
        if kind == "footprints":
            for x, y, c in [(50, 35, BLUE), (160, 80, TEAL), (305, 28, "#7545b3")]:
                out += f'<rect x="{x}" y="{y}" width="160" height="112" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-width="3"/>'
            out += text(35, 232, "Boxes show coverage; pixels hold content.", 18)
        elif kind == "risk":
            for x, y, h, label in [(90, 160, 45, "A"), (245, 150, 115, "B"), (410, 160, 75, "C")]:
                out += rect(x, y-h, 35, h, BLUE, radius=3) + circle(x+17, y, 6, TEAL)
                out += text(x+10, y+27, label, 18)
            out += text(25, 230, "Illustration: column height = relative risk", 18)
        else:
            for x, y, label in [(100, 78, "A"), (280, 140, "B"), (420, 63, "C")]:
                out += circle(x, y, 14, TEAL) + text(x+20, y+6, label, 24, weight=700)
            out += text(25, 232, "Illustrative locations; longitude goes first.", 18)
    elif kind == "hex":
        for row in range(3):
            for col in range(6):
                cx, cy = 66+col*72+(row%2)*36, 50+row*62
                pts = [(cx+40*math.cos(math.radians(a)), cy+40*math.sin(math.radians(a))) for a in range(30, 390, 60)]
                out += path("M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+" Z", "white", 3, TEAL if (row,col)==(1,2) else "#c6dbee")
        out += text(25, 233, "Same point, different spatial containers", 18)
    elif kind in {"clusters", "anomaly", "retrieval", "threshold"}:
        out += path("M45 15 V205 H515", MUTED, 2)
        for j, (cx, cy) in enumerate([(125, 145), (270, 75), (420, 120)]):
            for k in range(7):
                x, y = cx+math.sin(k*2)*28, cy+math.cos(k*3)*22
                out += circle(round(x, 1), round(y, 1), 7, COLORS[j])
        if kind == "threshold":
            out += path("M48 104 H500", GOLD, 3, extra='stroke-dasharray="7 5"')
            out += text(340, 39, "cutoff", 20, GOLD)
        elif kind == "anomaly":
            out += circle(460, 30, 13, GOLD) + text(323, 23, "inspect this", 19, GOLD)
        out += text(25, 235, "Schematic feature space; axes are not geography.", 18)
    elif kind in {"pixels", "change"}:
        for side in range(2):
            for row in range(6):
                for col in range(6):
                    fill = TEAL if col < 3 else BLUE
                    if side and row in (2,3) and col in (3,4):
                        fill = GOLD
                    out += rect(20+side*290+col*32, 22+row*28, 29, 25, fill, radius=2)
        out += text(232, 113, "→", 34, BLUE)
        out += text(28, 222, "pixels", 20) + text(315, 222, "groups / changes", 20)
    elif kind == "rain":
        vals = [8, 5, 30, 65, 110, 45, 12, 2, 30, 55, 10, 5]
        out += path("M30 15 V200 H510", MUTED, 2)
        for i,v in enumerate(vals):
            out += rect(45+i*38, 198-v, 23, v, BLUE, radius=2)
        out += path("M45 178 Q110 160 170 93 T300 90 T470 115", TEAL, 5)
        out += text(25, 232, "Daily bars + an accumulating window (schematic)", 18)
    elif kind in {"network", "bridge"}:
        positions = [(65,50),(170,50),(290,50),(440,50),(65,155),(170,155),(290,155),(440,155)]
        if kind == "bridge":
            out += rect(220, 5, 25, 195, "#acd2e6", radius=2)
        for a,b in [(0,1),(1,2),(2,3),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7)]:
            xa,ya=positions[a]; xb,yb=positions[b]
            out += path(f"M{xa} {ya} L{xb} {yb}", GOLD if kind=="bridge" and (a,b)==(1,2) else "#90a8bf", 4,
                        extra='stroke-dasharray="7 5"' if kind=="bridge" and (a,b)==(1,2) else "")
        for i,(x,y) in enumerate(positions):
            out += circle(x,y,14,TEAL if i==0 else BLUE) + text(x-5,y+5,str(i),14,"white",700)
        out += text(25, 232, "Connections constrain paths (illustrative graph).", 18)
    elif kind == "terrain":
        for i in range(5):
            out += f'<ellipse cx="168" cy="106" rx="{115-i*20}" ry="{80-i*13}" fill="none" stroke="{TEAL}" stroke-width="3"/>'
        out += path("M320 180 L345 140 L378 48 L410 105 L435 134 L460 100 L505 180", TEAL, 4, "#b9e4dc")
        out += path("M38 106 H297", GOLD, 3, extra='stroke-dasharray="7 5"')
        out += text(72, 225, "contours", 20) + text(350, 225, "profile / shape", 20)
    elif kind == "hats":
        for i,c in enumerate(["#e2e8f0","#cc4343",INK,"#eabf39","#2e9670",BLUE,"#7545b3"]):
            x=40+i*69
            out += rect(x,52,42,63,c,INK,6)+rect(x-10,111,62,12,c,INK,6)
            out += text(x+10,158,str(i+1),22,INK,700)
        out += text(38, 204, "Questions → discussion → accountable action", 20)
    else:
        labels = ["Catalog", "Item", "Asset"] if kind == "catalog" else ["Browser", "Export", "Runtime"]
        for i,label in enumerate(labels):
            x=20+i*178
            out += rect(x,66,145,90,"white",COLORS[i]) + text(x+15,117,label,23,COLORS[i],700)
            if i<2: out += text(x+151,118,"→",26)
        out += text(25,215,"Follow the links and the computation boundary.",18)
    return out


def infographic(key, p):
    body = rect(0,0,1280,900,"#f5f7fa",radius=0)+rect(0,0,1280,172,INK,radius=0)
    body += text(36,39,f"BROWSER GEOAI / LAB {key} / VISUAL FIELD GUIDE",17,"#a6dce1",700)
    body += text(36,90,p["title"],40,"white",700)
    body += text(36,134,p["question"],23,"#e1ebf5")
    for i,(label,code,explanation) in enumerate(p["stages"]):
        x=28+i*313
        body += rect(x,201,294,245,"white","#d6e1ec")
        body += circle(x+30,232,17,COLORS[i]) + text(x+24,238,str(i+1),18,"white",700)
        body += text(x+57,239,label,24,COLORS[i],700)
        body += text(x+18,278,explanation,20,width=27,line=1.38)
        if i<3: body += text(x+292,330,"→",24,MUTED)
    body += text(34,492,"MAKE THE IDEA VISIBLE",18,TEAL,700)
    body += f'<g transform="translate(34 515)">{schematic(p["visual"])}</g>'
    body += text(615,492,"WHAT THE BROWSER MAKES POSSIBLE",18,TEAL,700)
    body += text(615,532,p["value"],23,width=46)
    body += text(615,679,"READ THE CODE, THEN CHECK THE CLAIM",17,GOLD,700)
    body += text(615,713,p["challenge"],21,width=48)
    body += rect(28,794,1224,80,"#e7eef5")
    body += text(46,821,p["role"],19,INK,600,width=116)
    body += text(46,889,"Original teaching illustration • schematic marks, not measured data or a model output",16,MUTED)
    return svg(body,p["title"]," ".join(s[2] for s in p["stages"])+" "+p["role"])


def comic(key, p):
    body=rect(0,0,1280,480,"#f5f7fa",radius=0)
    body+=text(28,40,f"LAB {key} / A QUESTION WORTH ASKING",23,TEAL,700)
    for i,speech in enumerate(p["dialogue"]):
        x=26+i*420
        body+=rect(x,65,398,372,"white","#ccd9e7")
        body+=rect(x+18,84,362,155,"#eaf1fa",radius=20)
        body+=text(x+36,117,speech,24,width=27,line=1.32)
        body+=path(f"M{x+72} 238 l-10 25 l35 -25", "#eaf1fa", 1, "#eaf1fa")
        cx=x+94
        if i==1:
            body+=rect(cx-33,277,66,56,"#b4e3df",TEAL,12)
            body+=path(f"M{cx} 277 v-14",TEAL,3)+circle(cx,259,5,GOLD)
            body+=circle(cx-13,299,5,INK)+circle(cx+13,299,5,INK)
            body+=path(f"M{cx-13} 319 h26",TEAL,3)
        else:
            body+=circle(cx,302,30,"#f2ceb1",INK)
            body+=path(f"M{cx-28} 296 Q{cx-12} 254 {cx+29} 286",INK,8)
            body+=circle(cx-10,300,3,INK)+circle(cx+12,300,3,INK)
            body+=path(f"M{cx-9} 314 q10 9 20 0",INK,2)
        body+=path(f"M{cx} 335 v42 M{cx} 346 l-30 14 M{cx} 346 l34 -13",INK,5)
        body+=text(x+157,314,"Code guide" if i==1 else "Learner",22,INK,700)
        body+=text(x+157,344,["Ask", "Clarify", "Investigate"][i],20,MUTED)
    body+=text(28,469,"Fictional dialogue for learning. The cartoon does not depict a live AI response.",18,MUTED)
    return svg(body,p["title"]+" — teaching cartoon"," ".join(p["dialogue"]),1280,480)


def slide(key,p,i):
    label,code,explanation=p["stages"][i]
    body=rect(0,0,960,540,"#f5f7fa",radius=0)+rect(0,0,960,90,INK,radius=0)
    body+=text(25,29,f"BROWSER GEOAI / LAB {key} / {i+1} OF 4",15,"#a6dce1",700)
    body+=text(25,68,p["title"],29,"white",700)
    body+=text(25,141,f"{i+1}. {label}",32,COLORS[i],700)
    body+=f'<g transform="translate(16 160) scale(.81)">{schematic(p["visual"])}</g>'
    body+=text(490,183,explanation,27,width=29,line=1.35)
    # Leave the lower frame clear for captions and native player controls.
    body+=rect(22,371,916,61,INK,radius=8)
    body+=text(38,409,code,23,"#a6dce1",mono=True)
    for j in range(4):
        body+=rect(22+j*234,490,214,6,COLORS[j] if j<=i else "#cedae7",radius=2)
    body+=text(24,522,"Silent storyboard • schematic illustration • pause or replay any step",17,MUTED)
    return svg(body,p["title"]+f" — step {i+1}",explanation,960,540)


CSS = """
:root{color-scheme:light;font-family:system-ui,sans-serif;color:#14283f;background:#f2f6fa}
*{box-sizing:border-box}body{margin:0}main{max-width:1050px;margin:auto;padding:clamp(18px,4vw,45px)}
h1{font-size:clamp(28px,5vw,45px);line-height:1.15}h2{margin-top:2rem}p,li{line-height:1.7}
a{color:#164fa5}a:focus-visible,summary:focus-visible{outline:3px solid #a96112;outline-offset:4px}
video,img{display:block;width:100%;height:auto;border-radius:12px}video{background:#14283f}
.kicker{color:#087f78;font-weight:700;letter-spacing:.07em}.note{background:#e3edf6;padding:16px;border-radius:10px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:18px}
article{padding:20px;background:white;border:1px solid #cddbe9;border-radius:14px}
code{overflow-wrap:anywhere;background:#e6edf5;padding:2px 5px}summary{cursor:pointer;font-weight:600}
nav{display:flex;gap:20px;flex-wrap:wrap}ol{padding-left:25px}li{padding:8px 0}
"""


def page(title,body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style>'
            f'</head><body><main>{body}</main></body></html>\n')


def watch_page(key,p,filename):
    transcript="".join(f'<li><strong>{i*8:02d}–{(i+1)*8:02d}s · {esc(label)}</strong><p>{esc(explanation)}</p>'
                       f'<code>{esc(code)}</code></li>' for i,(label,code,explanation) in enumerate(p["stages"]))
    body=(f'<nav><a href="../index.html">All visual lessons</a><a href="{PUBLISHED}/notebooks/{Path(filename).stem}.html">Read this chapter</a><a href="../../../../lab/index.html?path={filename}">Run this notebook</a></nav>'
          f'<p class="kicker">LAB {key} · 32-SECOND VISUAL WALKTHROUGH</p><h1>{esc(p["title"])}</h1>'
          f'<p>{esc(p["question"])}</p><video controls playsinline preload="none" poster="poster.png" '
          f'aria-label="Captioned walkthrough: {esc(p["title"])}"><source src="walkthrough.mp4" type="video/mp4">'
          f'<track src="captions.vtt" kind="captions" srclang="en" label="English" default>'
          f'<a href="walkthrough.mp4">Download the walkthrough</a></video>'
          '<p>Silent, captioned storyboard. Use the player to pause, seek or change playback speed. '
          'On a small screen, use fullscreen or read the transcript below. '
          'The diagrams explain the method; they are not recordings of a live model run.</p>'
          '<p><a href="walkthrough.mp4" download>Download MP4</a> · <a href="captions.vtt">Captions</a> · '
          '<a href="infographic.svg">Open infographic at full size</a></p>'
          f'<h2>What runs here?</h2><p>{esc(p["browser"])}</p><p class="note">{esc(p["role"])}</p>'
          f'<h2>Transcript and code landmarks</h2><ol>{transcript}</ol>'
          f'<h2>The common misconception</h2><img src="cartoon.svg" alt="{esc(" ".join(p["dialogue"]))}">'
          '<details><summary>Read the cartoon dialogue</summary><ol>'
          + ''.join(f'<li>{esc(line)}</li>' for line in p['dialogue']) + '</ol></details>'
          f'<h2>Try explaining it</h2><p>{esc(p["challenge"])}</p><details><summary>Check your reasoning</summary>'
          f'<p>{esc(p["answer"])}</p></details>'
          '<p>Original educational illustrations and captions authored for this repository. See the notebook for data and software citations.</p>')
    return page(p["title"],body)


def vtt(p):
    return "WEBVTT\n\n"+"\n\n".join(
        f"{i+1}\n00:00:{i*8:02d}.000 --> 00:00:{(i+1)*8:02d}.000\n{label}. {description}"
        for i,(label,code,description) in enumerate(p["stages"]))+"\n"


def md_cell(source,identifier,**metadata):
    return {"cell_type":"markdown","id":identifier,"metadata":{"learning_guide":True,**metadata},
            "source":source.splitlines(keepends=True)}


def intro(key,p,filename):
    base=f"assets/learning/{key}"
    movie=f"{PUBLISHED}/lite/files/assets/learning/{key}/watch.html"
    stages=" → ".join(s[0].lower() for s in p["stages"])
    return (f"## Start here: the question behind the code\n\n**{p['question']}**\n\n"
            f"**What you will learn:** {stages}. The numbered reading guides below follow the actual code cells. "
            "Read a guide, predict the output, then run its cell with **Shift+Enter**. Run from top to bottom; "
            "changing an upstream value requires rerunning the cells that use it.\n\n"
            f"**GeoAI connection:** {p['role']}\n\n**Why this is useful:** {p['value']}\n\n"
            f"**Where the work happens:** {p['browser']}\n\n"
            f"![{p['title']}. {' '.join(s[2] for s in p['stages'])}]({base}/infographic.svg)\n\n"
            f"### Watch the idea unfold\n\n[![Preview: {p['title']} — 32-second captioned walkthrough]({base}/poster.png)]({movie})\n\n"
            f"[▶ Watch the captioned mini-video and read its transcript]({movie}) · "
            f"[Launch this notebook]({PUBLISHED}/lite/lab/index.html?path={filename}) · "
            f"[Read this Book chapter]({PUBLISHED}/notebooks/{Path(filename).stem}.html) · "
            f"[Python and browser learning guide]({PUBLISHED}/learning-guide.html)\n\n"
            "The video is a silent four-step teaching storyboard with player controls and captions. "
            "Open the companion page to play, pause, seek or download it. "
            "The local copy is bundled under `assets/learning/"+key+"/`; downloaded media can be played offline. "
            "The infographic and the text below cover the same ideas without a video player.\n\n"
            "**Video transcript:**\n\n"+"\n\n".join(f"{i+1}. **{label} ({i*8}–{(i+1)*8} s):** {desc} Code landmark: `{code}`."
                for i,(label,code,desc) in enumerate(p["stages"]))+"\n")


def lesson_cell(key,number,lesson,code):
    return md_cell(
        f"### Code guide {number} — {lesson['title']}\n\n"
        f"**Read the Python:** {lesson['explanation']}\n\n"
        f"**Look for:** {lesson['result']}\n\n"
        f"**Pause and try:** {lesson['experiment']}\n",
        f"learn-{key}-code-{number:02d}",code_sha256=hashlib.sha256(code.encode()).hexdigest())


def transform(nb,key,filename):
    cells=[c for c in nb["cells"] if not c.get("metadata",{}).get("learning_guide")]
    code_cells=[c for c in cells if c["cell_type"]=="code"]
    if len(code_cells)!=len(LESSONS[key]):
        raise ValueError(f"{filename}: {len(code_cells)} code cells but {len(LESSONS[key])} guides")
    # Check all anchors before any edits so a shifted cell cannot acquire a wrong explanation.
    for i,(cell,lesson) in enumerate(zip(code_cells,LESSONS[key])):
        if lesson["anchor"] not in "".join(cell["source"]):
            raise ValueError(f"{filename}: guide {i+1} anchor absent: {lesson['anchor']}")
    result=[]; number=0
    for i,cell in enumerate(cells):
        if "id" not in cell:
            cell={**cell,"id":f"original-{key}-{i:02d}"}
        if cell["cell_type"]=="code":
            result.append(lesson_cell(key,number+1,LESSONS[key][number],"".join(cell["source"])))
            number+=1
        result.append(cell)
        if i==0:
            result.append(md_cell(intro(key,PROFILES[key],filename),f"learn-{key}-intro"))
    p=PROFILES[key]
    result.append(md_cell(
        f"## Make sense of the result\n\n![{' '.join(p['dialogue'])}](assets/learning/{key}/cartoon.svg)\n\n"
        "**Cartoon transcript:** "+" → ".join(p["dialogue"])+"\n\n"
        f"**Explain it to a colleague:** {p['challenge']}\n\n"
        f"<details><summary>Check your reasoning</summary>\n\n{p['answer']}\n\n</details>\n\n"
        "Write three sentences: **I used…** (source and units), **the code computed…** (method), "
        "and **I can conclude…** (plus a remaining question). Point to the map, chart or table that supports each claim.\n\n"
        "All new teaching illustrations are original schematics. Their marks and fictional dialogue are explanatory, "
        "not observations, fitted predictions or captured AI conversations. The existing citation cells identify the analytical data.\n",
        f"learn-{key}-reflection"))
    result.append(md_cell(
        "## GeoLibre creator and software attribution\n\n"
        "GeoLibre is developed by **Qiusheng Wu and contributors**. Recommended citation: "
        "Wu, Q. (2026). *GeoLibre: A lightweight, cloud-native GIS platform for visualizing, exploring, "
        "and analyzing geospatial data.* Zenodo. [doi:10.5281/zenodo.20785400](https://doi.org/10.5281/zenodo.20785400). "
        "See [the official citation guidance](https://geolibre.app/citation/) and "
        "[source and MIT license](https://github.com/opengeos/GeoLibre). These browser lessons pin "
        "the Python builders to `geolibre==3.0.0`; the independently hosted viewer may change. "
        "This repository supplies the JupyterLite adapter and teaching materials, not the upstream GIS. "
        "Keep the original dataset, demo-author and basemap credits when sharing a result.\n",
        f"learn-{key}-geolibre-credit"))
    nb={**nb,"cells":result}
    nb["metadata"]={**nb.get("metadata",{}),"learning_edition":{"version":1,"guide_count":number,
        "media":f"assets/learning/{key}/watch.html"}}
    return nb


def write_or_check(path,content,check):
    if check:
        if not path.exists() or path.read_text(encoding="utf-8")!=content:
            raise ValueError(f"Generated teaching content is stale: {path.relative_to(ROOT)}")
    else:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8",newline="\n")


def render_videos(profiles):
    import imageio_ffmpeg
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory(prefix="geoai-storyboards-") as temp, sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        tab=browser.new_page(viewport={"width":960,"height":540},device_scale_factor=1)
        for key,p in profiles.items():
            frames=Path(temp)/key; frames.mkdir()
            for i in range(4):
                tab.set_content('<html><body style="margin:0">'+slide(key,p,i)+"</body></html>")
                tab.locator("svg").screenshot(path=str(frames/f"slide-{i}.png"))
            (ASSETS/key/"poster.png").write_bytes((frames/"slide-0.png").read_bytes())
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),"-y","-v","error","-framerate","1/8",
                "-i",str(frames/"slide-%d.png"),"-t","32","-r","12","-c:v","libx264","-crf","25",
                "-pix_fmt","yuv420p","-movflags","+faststart",str(ASSETS/key/"walkthrough.mp4")],check=True)
            (ASSETS/key/"media-source.sha256").write_text(media_digest(key,p)+"\n",encoding="utf-8")
            print(f"Rendered {key}: 32-second captioned MP4",flush=True)
        browser.close()


def media_digest(key,p):
    return hashlib.sha256("".join(slide(key,p,i) for i in range(4)).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--videos",action="store_true")
    parser.add_argument("--video-keys", nargs="*", help="Render only these lab IDs when --videos is supplied")
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.check and args.videos:
        parser.error("--check does not regenerate videos")
    if args.video_keys and (not args.videos or set(args.video_keys)-set(PROFILES)):
        parser.error("--video-keys requires --videos and known lab IDs")
    paths=sorted(NOTEBOOKS.glob("*.ipynb"))
    if {p.name[:2] for p in paths}!=set(PROFILES) or set(PROFILES)!=set(LESSONS):
        raise ValueError("Every notebook must have an authored profile and cell guides")
    # Validate the entire set before mutation.
    updated=[(p,transform(json.loads(p.read_text(encoding="utf-8")),p.name[:2],p.name)) for p in paths]
    cards=[]
    for p,nb in updated:
        key=p.name[:2]; profile=PROFILES[key]; directory=ASSETS/key
        write_or_check(p,json.dumps(nb,ensure_ascii=False,indent=1)+"\n",args.check)
        for name,content in [("infographic.svg",infographic(key,profile)),("cartoon.svg",comic(key,profile)),
                             ("watch.html",watch_page(key,profile,p.name)),("captions.vtt",vtt(profile))]:
            write_or_check(directory/name,content,args.check)
        if args.check:
            for name in ("poster.png","walkthrough.mp4"):
                if not (directory/name).is_file():
                    raise ValueError(f"Missing media: {directory/name}")
            write_or_check(directory/"media-source.sha256",media_digest(key,profile)+"\n",True)
        cards.append(f'<article><p class="kicker">LAB {key}</p><h2><a href="{key}/watch.html">{esc(profile["title"])}</a></h2>'
                     f'<p>{esc(profile["question"])}</p><p>{esc(profile["role"])}</p></article>')
    gallery=page("Browser GeoAI visual learning library",f'<nav><a href="{PUBLISHED}/visual-library.html">Maps, scenes and notebook directory</a><a href="{PUBLISHED}/intro.html">Book home</a></nav><p class="kicker">{len(paths)} NOTEBOOKS · ONE QUESTION AT A TIME</p>'
                 '<h1>See what the code means</h1><p>Each lesson pairs an infographic and a teaching cartoon with a short, silent '
                 'captioned video, a transcript and a question to test your understanding. No Python kernel or third-party video service is needed.</p>'
                 '<div class="cards">'+"".join(cards)+'</div>')
    write_or_check(ASSETS/"index.html",gallery,args.check)
    if args.videos:
        render_videos({k:p for k,p in PROFILES.items() if not args.video_keys or k in args.video_keys})
    print(f"{'Verified' if args.check else 'Updated'} {len(paths)} notebooks and {sum(map(len,LESSONS.values()))} code guides.")


if __name__=="__main__":
    main()

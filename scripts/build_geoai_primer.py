"""Build original, accessible SVG teaching diagrams (no network or extra packages).

Edit this source, not the generated SVGs. Run with --check in CI.
These are conceptual illustrations, not maps, model outputs or health estimates.
"""
import argparse
import html
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "book/assets/geoai"
INK, MUTED = "#162b42", "#41576d"
BLUE, TEAL, PURPLE, GOLD = "#225caa", "#08776f", "#7447a5", "#995b0c"
COLORS = [BLUE, TEAL, PURPLE, GOLD]
PALE = ["#eaf2fd", "#e5f5f0", "#f1eafa", "#fff3d9"]


def txt(x, y, value, size=22, color=INK, bold=False, width=None):
    lines = textwrap.wrap(value, width, break_long_words=False, break_on_hyphens=False) if width else [value]
    return "".join(f'<text x="{x}" y="{y+i*size*1.35:.1f}" font-size="{size}" '
                   f'font-weight="{700 if bold else 400}" fill="{color}">{html.escape(s)}</text>'
                   for i, s in enumerate(lines))


def box(x, y, w, h, fill="white", stroke="none", r=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def line(x1, y1, x2, y2, color=MUTED, width=3, arrow=False, dashed=False):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" '
            f'fill="none"'+(' marker-end="url(#arrow)"' if arrow else '')+
            (' stroke-dasharray="7 5"' if dashed else '')+'/>' )


def dot(x, y, label="", color=TEAL, r=15):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'+
            (txt(x-7, y+7, label, 20, "white", True) if label else ""))


def card(x, y, w, h, title, body, n=0):
    return (box(x,y,w,h,PALE[n%4]) + box(x,y,6,h,COLORS[n%4],r=2)+
            txt(x+22,y+37,title,24,COLORS[n%4],True,width=int((w-40)/14))+
            txt(x+22,y+102,body,22,width=int((w-40)/12)))


def strip(y, text):
    return box(40,y,1120,65,"#edf2f6")+txt(60,y+39,text,22,MUTED)


def flow(title, subtitle, stages, takeaway):
    """Three linked stages plus a decision boundary, not a quantitative chart."""
    body = ""
    for i, (heading, content) in enumerate(stages):
        x=40+i*380
        body += card(x,180,350,350,heading,content,i)
        body += dot(x+30,570,str(i+1),COLORS[i])
        if i<2:
            body += line(x+351,350,x+375,350,arrow=True)
    return frame(title,subtitle,body+strip(605,takeaway))


def frame(title, subtitle, body):
    head = box(0,0,1200,720,"#fbfcfe",r=0)+box(0,0,1200,10,TEAL,r=0)
    head += txt(40,61,title,34,INK,True)+txt(40,104,subtitle,22,MUTED)
    head += txt(40,702,"GEOAI FIELD GUIDE  /  Original teaching schematic — not observed health data",17,MUTED)
    # A complete text alternative travels with the standalone SVG.
    content = head+body
    parsed = ET.fromstring('<g>'+content+'</g>')
    description = " | ".join(e.text for e in parsed.iter("text") if e.text)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" '
            'viewBox="0 0 1200 720" role="img" aria-labelledby="title desc" '
            'font-family="Arial, sans-serif"><title id="title">'+html.escape(title)+
            '</title><desc id="desc">'+html.escape(description)+'</desc>'+
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#41576d"/>'
            '</marker></defs>'+content+'</svg>\n')


def foundations():
    figures={}
    b=box(40,155,700,410,PALE[0],BLUE)+txt(65,200,"AI: methods for learning, reasoning and assistance",25,BLUE,True)
    b+=box(90,245,595,265,PALE[1],TEAL)+txt(115,285,"GeoAI: AI with geographic context",27,TEAL,True)
    b+=txt(115,335,"Location • distance • neighbors • networks",23)+txt(115,377,"Scale • time • imagery • spatial uncertainty",23)
    b+=txt(115,446,"Not just an AI answer displayed on a map.",23,TEAL,True)
    b+=card(775,155,385,190,"GIS contribution","Coordinates, spatial joins, layers and geographic reasoning.",1)
    b+=card(775,365,385,200,"Domain contribution","Health expertise, community knowledge, governance and decisions.",2)
    b+=strip(605,"GeoAI is a specialization of AI, not an unrelated replacement for it.")
    figures["what-is-geoai"]=frame("What makes AI geographic?","The same learning algorithms can answer very different questions when place matters.",b)

    b=""
    for offset,title,closed in [(40,"A • Bridge open",False),(630,"B • Bridge closed",True)]:
        b+=box(offset,160,530,370,PALE[0])+txt(offset+20,200,title,26,BLUE,True)
        b+=line(offset+245,215,offset+245,475,"#97c7e2",30)
        for x,y,label in [(90,340,"H"),(400,340,"C")]:
            b+=dot(offset+x,y,label,TEAL,24)
        b+=line(offset+114,340,offset+221,340,TEAL,5)
        b+=line(offset+269,340,offset+376,340,TEAL,5)
        if closed:
            b+=line(offset+227,322,offset+264,358,GOLD,6)+line(offset+227,358,offset+264,322,GOLD,6)
            b+=line(offset+90,364,offset+90,465,PURPLE,4)+line(offset+90,465,offset+400,465,PURPLE,4)+line(offset+400,465,offset+400,364,PURPLE,4)
        else:
            b+=line(offset+220,340,offset+270,340,TEAL,7)
        b+=txt(offset+24,505,"H = home area; C = clinic (invented)",21,MUTED)
    b+=strip(555,"Same straight-line distance. Different travel route. Different access to care.")
    figures["spatial-context"]=frame("Place changes the question","A coordinate pair cannot describe every barrier between a community and a service.",b)

    b=""
    rows=[("GIS / spatial algorithms","Where are services? Which route is shortest?","00, 01, 04, 07, 14, 15",BLUE),
          ("Machine learning","Which feature profiles are similar or unusual?","02, 03, 05, 08, 10, 11",TEAL),
          ("Text / optional model aid","Which demo matches? Can a plan be explained?","09; optional handoff in 12–15",PURPLE),
          ("Evidence / human reasoning","What do reported clusters mean for action?","16, 17",GOLD)]
    for i,(kind,question,labs,c) in enumerate(rows):
        y=155+i*109
        b+=box(40,y,1120,95,PALE[i])+txt(60,y+36,kind,24,c,True)+txt(60,y+70,question,21)
        b+=txt(785,y+55,labs,20,c,True)
    b+=strip(605,"A useful map does not need to pretend to be a trained model.")
    figures["methods"]=frame("Four ingredients, different jobs","GeoAI projects mix methods. Name the method that actually ran.",b)

    b=card(40,160,345,370,"Your browser","JupyterLite runs Python in WebAssembly. Small tables, arrays and scikit-learn models can run here. Local work is not automatically uploaded.",0)
    b+=card(425,160,345,370,"External data / maps","STAC APIs, imagery, basemaps and the GeoLibre hosted viewer use network services. CORS, permissions and availability still apply.",1)
    b+=card(810,160,350,370,"Optional server / GPU","Large training jobs and optional model requests run outside the default lesson. Review what data leaves the browser. Keep keys off the public site.",2)
    b+=strip(605,"Browser-native computation does not mean offline-only or automatically private.")
    figures["browser-boundary"]=frame("Where does the work happen?","The runtime boundary is also a privacy, cost and reproducibility boundary.",b)
    return figures


def workflow_figures():
    figures={}
    b=""
    steps=[("01 QUESTION","Choose a decision and an accountable owner."),
           ("02 DATA","Check permission, date, units and missingness."),
           ("03 FEATURES","Join geography; align time and spatial scale."),
           ("04 MODEL","Compare a simple baseline with learned patterns."),
           ("05 VALIDATE","Hold out places / time; map errors and uncertainty."),
           ("06 ACT + LEARN","Human review, measured benefit and monitoring.")]
    for i,(t,d) in enumerate(steps):
        row,col=divmod(i,3); x=40+col*380; y=155+row*205
        b+=card(x,y,350,180,t,d,i)
        if col<2: b+=line(x+352,y+90,x+375,y+90,arrow=True)
    b+=strip(605,"A model output becomes useful only when a real decision can be checked.")
    figures["workflow"]=frame("From geographic question to accountable action","The notebooks teach parts of this workflow; they are not deployed clinical systems.",b)
    b=""
    headers=["Input","Python representation","Meaning to preserve"]
    data=[("Clinic locations","GeoDataFrame / coordinates","CRS, date, service availability"),
          ("Satellite pixels","Array + georeferencing","Units, clouds, resolution"),
          ("Road connections","Nodes + weighted edges","Travel time, closures, direction"),
          ("District indicators","Rows + numeric columns","Denominator, period, uncertainty")]
    for j,h in enumerate(headers): b+=txt(55+j*375,177,h,24,BLUE,True)
    for i,row in enumerate(data):
        y=203+i*85; b+=box(40,y,1120,70,PALE[i])
        for j,v in enumerate(row): b+=txt(55+j*375,y+41,v,20)
    b+=strip(605,"Features are measurable model inputs, not neutral replacements for people or places.")
    figures["features"]=frame("How geography becomes Python data","Keep the meaning attached when turning maps into numbers.",b)

    b=""
    for j,mode in enumerate(["Random nearby points","Hold out a region"]):
        ox=55+j*560; b+=txt(ox,180,mode,26,COLORS[j],True)
        for row in range(5):
            for col in range(8):
                test=(row+col)%3==0 if j==0 else col>=6
                x,y=ox+col*52,220+row*53
                b+=box(x,y,44,44,PALE[3] if test else PALE[0],GOLD if test else BLUE,r=3)
                b+=txt(x+14,y+29,"T" if test else "L",20,GOLD if test else BLUE,True)
        b+=txt(ox,530,"Neighbors can share signal." if j==0 else "Tests transfer to a new area.",22)
    b+=strip(605,"L = learning data; T = test data. Also test future periods and boundary buffers.")
    figures["validation"]=frame("Do not let the test set peek at its neighbors","Choose held-out areas and dates that match the real deployment question.",b)

    b=""
    labels=[("A","0.35–0.55",0.35,0.55,TEAL),("B","0.25–0.80",0.25,0.80,PURPLE),("C","No estimate",None,None,GOLD)]
    b+=txt(55,182,"Invented model score",26,BLUE,True)
    for i,(name,label,lo,hi,c) in enumerate(labels):
        y=258+i*105; b+=txt(55,y+8,"Area "+name,24,c,True)
        if lo is not None:
            b+=line(260+lo*550,y,260+hi*550,y,c,8)+dot(260+(lo+hi)*275,y,color=c,r=11)
        else: b+=txt(350,y+8,"?",32,GOLD,True)
        b+=txt(875,y+8,label,24,c,True)
    b+=line(260,535,810,535)+txt(252,569,"0",20)+txt(802,569,"1",20)
    b+=strip(605,"Illustrative ranges only: not confidence intervals, observations or health probabilities.")
    figures["uncertainty"]=frame("An honest map has room for “we do not know”","Missing data and uncertain estimates need different symbols from low risk.",b)
    return figures


def atlas_figure():
    b=""
    rows=[("ORIENT","00 / 01 / 04 / 06 / 07","Maps, spatial scale, rainfall, runtime and catalogs"),
          ("LEARN PATTERNS","02 / 03 / 05 / 08 / 09 / 10 / 11","Clusters, anomalies, text similarity and graph roles"),
          ("TEST ASSUMPTIONS","12 / 13 / 14 / 15","Bounded plans, change, terrain and route scenarios"),
          ("INTERPRET + ASSIST","16 / 17 / 18 / 19 / 20","Evidence, human perspectives and local chat-assisted mapping")]
    for i,(title,ids,desc) in enumerate(rows):
        y=150+i*111; b+=box(40,y,1120,98,PALE[i])+txt(60,y+32,title,22,COLORS[i],True)
        b+=txt(385,y+32,ids,23,COLORS[i],True)+txt(60,y+72,desc,22)
    b+=strip(610,"Transfer the method to health only after adding suitable data, governance and validation.")
    return frame("21 labs, one learning journey","Find the skill you need before choosing a model.",b)


def program_figures():
    figures={}
    figures["hiv-continuity"]=flow("PEPFAR / HIV: protect continuity of care","Proposed program application — not a result from the teaching notebooks.",[
        ("1 • Combine evidence","Approved aggregate service data + clinic capacity + road access + flood or heat scenarios."),
        ("2 • Find fragile links","Spatial routes locate barriers. A validated model could flag unusual service changes for review."),
        ("3 • Support a decision","Program teams compare delivery routes or service options. Track continuity, equity and travel burden.")],
        "A priority map supports care planning; it must not infer an individual's HIV status.")
    b=""
    stages=[("Population living with HIV",10000,BLUE),("Know their status",8000,TEAL),("On treatment",6000,PURPLE),("Virally suppressed",5400,GOLD)]
    for i,(label,n,c) in enumerate(stages):
        y=170+i*100; b+=txt(50,y+29,label,22,c,True)+box(425,y,600*n/10000,42,c,r=4)+txt(1040,y+29,f"{n:,}",22,c,True)
    b+=txt(425,590,"6,000 / 8,000 = 75%       but       6,000 / 10,000 = 60%",23,INK,True)
    b+=strip(615,"Entirely invented nested cohort. Real quarterly service counts may not form a cohort.")
    figures["denominators"]=frame("The denominator changes the story","Read every indicator's eligible population, reporting period and missingness.",b)
    b=box(40,150,710,440,PALE[0])+txt(65,187,"Illustrative specimen referral network",25,BLUE,True)
    for x,y,label in [(140,285,"A"),(160,490,"B"),(370,385,"H"),(620,260,"L")]:
        b+=dot(x,y,label,TEAL,24)
    for a,c in [((164,295),(346,376)),((184,478),(346,397)),((394,375),(596,275))]: b+=line(*a,*c,BLUE,4,arrow=True)
    b+=txt(90,245,"Clinic A",21)+txt(95,540,"Clinic B",21)+txt(330,445,"Hub",21)+txt(595,220,"Lab",21)
    b+=card(795,150,365,200,"Measure the whole delay","Transport + pickup schedule + lab queue + result return.",1)
    b+=card(795,375,365,215,"Validate the service","Road speed alone cannot tell whether a test or treatment was delivered.",2)
    b+=strip(615,"Transfer from lab 15: weighted paths. Add real capacities and validated turnaround data.")
    figures["tb-network"]=frame("TB: the route matters, but so does the service","Proposed referral planning, not diagnosis or a treatment recommendation.",b)
    figures["polio"]=flow("Polio: turn coverage gaps into checked microplans","Existing GIS practice can inform a carefully validated GeoAI extension.",[
        ("Map the denominator","Settlements, eligible children estimates, team areas and difficult routes. Mark uncertain or missing places."),
        ("Verify locally","Imagery may suggest unmapped buildings. Field teams confirm habitation, names, access and eligibility."),
        ("Plan and evaluate","Allocate visits and logistics with local teams. Check missed settlements and independent coverage evidence.")],
        "Detected rooftops are not counts of children, households or vaccination status.")
    figures["malaria"]=flow("Malaria: tailor the question to the place and season","A candidate GeoAI extension to subnational planning, not an intervention prescription.",[
        ("Join diverse signals","Cases and testing + population + rain / temperature + vector observations + intervention coverage."),
        ("Test useful patterns","Compare seasonal baselines with lagged spatial models. Hold out districts and future seasons."),
        ("Support local review","Discuss surveillance and supply priorities. Evaluate warning lead time, missed events and false alarms.")],
        "Weather suitability is not infection risk; surveillance and program context remain essential.")
    figures["ebola"]=flow("Ebola: support verified response work","Geography helps organize a response; it does not identify infection from space.",[
        ("Verified evidence","Authorized surveillance, confirmed service locations and documented investigations. Protect access."),
        ("Operational geography","Route teams and samples; inspect reporting delays and facility access. Separate verified from unverified alerts."),
        ("Human investigation","Trained teams verify contacts and alerts. Review faster response against false alarms, harm and workload.")],
        "Sister-city links, roads and nearby homes are not evidence of person-to-person contact.")
    figures["emergency"]=flow("Emergency response: a map pin is not an open clinic","Combine hazard information with current service functionality.",[
        ("What happened?","Event footprint, date, reliability and exposed areas. Keep uncertainty and data gaps visible."),
        ("What still works?","Accessible roads + power / water + staffing + supplies + verified facility services and capacity."),
        ("What can change?","Compare feasible referral or supply routes. Record owner, last verification, operational checks and outcomes.")],
        "Potential benefit: clearer logistics choices. Confirmation: actual service delivery and access.")
    return figures


def climate_figures():
    figures={}
    b=""
    for i,(title,body) in enumerate([
        ("HAZARD","Heat, flood, drought or smoke: intensity, duration and timing."),
        ("EXPOSURE","People, services and livelihoods in the affected place and period."),
        ("VULNERABILITY","Sensitivity, housing, livelihood constraints and available protection.")]):
        b+=card(40+i*380,150,350,230,title,body,i)
    b+=line(215,385,215,435,arrow=True)+line(595,385,595,435,arrow=True)+line(975,385,975,435,arrow=True)
    b+=box(40,450,710,110,PALE[3])+txt(60,487,"Potential health / service consequences",25,GOLD,True)+txt(60,527,"Observed outcomes require health data and causal caution.",22)
    b+=box(775,450,385,110,PALE[1])+txt(795,487,"Capacity can change risk",24,TEAL,True)+txt(795,527,"Adaptation • access • continuity",21)
    b+=strip(605,"A pathway diagram explains relationships; it is not a risk equation or calibrated model.")
    figures["climate-pathways"]=frame("Climate and health: connect the missing middle","A hazard layer alone does not measure who becomes ill or loses access to care.",b)
    figures["heat"]=flow("Heat stress: a hot pixel is a starting point","Potential application: identify places needing better exposure data and protective services.",[
        ("Satellite surface","Land surface temperature describes the ground or canopy observed at a particular time."),
        ("Human exposure","Air temperature, humidity, sun, wind, housing and activity shape experienced heat. Add ground observations."),
        ("Program question","Where might cooling access or worker protection be insufficient? Validate with exposure and health evidence.")],
        "Lab 12 uses invented temperature values and a rule; it is not a heat-health forecast.")
    b=box(40,155,560,380,PALE[0])+txt(60,196,"Coastal cross-section (invented)",25,BLUE,True)
    b+='<path d="M55 480 L55 435 L190 435 L265 300 L330 405 L420 395 L555 270 L580 480 Z" fill="#c9dac0" stroke="#507a41" stroke-width="3"/>'
    b+='<path d="M55 350 L237.22 350 L190 435 L55 435 Z" fill="#9bcae8"/>'
    b+=line(55,350,575,350,BLUE,3,dashed=True)
    b+=txt(65,330,"Water level",22,BLUE,True)+txt(287,466,"Low but separated",21,GOLD,True)
    b+=card(640,155,520,180,"More than elevation","Vertical datum + tides + connectivity + defenses + drainage + scenario date.",1)
    b+=card(640,355,520,180,"Read lab 16 correctly","Its 3D height is reported relative risk. Its scenario animation is not simulated water depth.",2)
    b+=strip(605,"A DEM threshold can screen low land; a credible inundation study needs more evidence.")
    figures["coastal"]=frame("Sea-level rise: low land is not automatically flooded","Keep statistical cluster evidence separate from physical flood modeling.",b)
    figures["food-water"]=flow("Food and water insecurity: follow the whole chain","Combine environmental signals with access, affordability and service evidence.",[
        ("Environmental stress","Rainfall anomalies, water availability, crop conditions and seasonal context. Distinguish dry weather from long-term change."),
        ("People and systems","Markets, food prices, livelihoods, storage, safe water access and functioning supply systems."),
        ("Health / action evidence","Nutrition and service indicators plus local assessments. Evaluate whether assistance reaches those needing it.")],
        "Greenness is not food security. Visible water is not available or safe drinking water.")
    b=""
    for i,(title,left,right,check) in enumerate([
        ("AIR QUALITY","Satellite aerosol signal","Ground-level exposure","Add monitors, atmospheric modeling and time alignment."),
        ("WATER QUALITY","Visible color / turbidity","Microbial or chemical safety","Add samples, validated retrievals and supply-system context.")]):
        y=155+i*205
        b+=box(40,y,1120,185,PALE[i])+txt(60,y+35,title,25,COLORS[i],True)
        b+=txt(60,y+85,left,24)+txt(565,y+85,"≠",32,GOLD,True)+txt(645,y+85,right,24)
        b+=txt(60,y+145,check,22,MUTED)
    b+=strip(605,"Remote sensing provides evidence about a proxy; validate the health-relevant quantity.")
    figures["air-water"]=frame("Do not confuse a proxy with the target","A proxy is a related measurement, not the thing we ultimately want to know.",b)
    figures["vectors"]=flow("Vector shifts: suitability is one part of transmission","Explore changes in where surveillance may be useful, not who will be infected.",[
        ("Environmental suitability","Temperature, rain, seasonality, habitat and species-specific limits; extreme conditions can reduce suitability too."),
        ("Transmission conditions","Vector presence + pathogen introduction + human exposure + immunity + prevention and care."),
        ("Verified response","Use entomology and surveillance to evaluate changes. Test transfer across regions, seasons and species.")],
        "A future suitability map is conditional on its scenario and assumptions, not a case forecast.")
    b=""
    for i,(t,d) in enumerate([
        ("Climate pressure","Flood, drought, heat, livelihood disruption."),
        ("Other major drivers","Institutions, income, safety, social ties and policy."),
        ("Community choices","Adapt, stay, move temporarily or relocate; some cannot move.")]):
        b+=card(40+380*i,150,350,240,t,d,i)
    b+=line(200,400,440,465,arrow=True)+line(600,400,600,465,arrow=True)+line(990,400,760,465,arrow=True)
    b+=box(190,475,820,95,PALE[3])+txt(215,510,"Plan inclusive service continuity under several scenarios",24,GOLD,True)+txt(215,547,"Do not profile migrants or portray movement as a security threat.",22)
    b+=strip(605,"Climate, migration and conflict are context-dependent; no single map establishes causation.")
    figures["migration"]=frame("Climate, mobility and conflict: resist a single-cause story","The useful health question is how services can remain accessible and trusted.",b)
    b=""
    hats=[("WHITE","Evidence + gaps",BLUE),("RED","Concerns + trust","#ae2846"),("BLACK","Failure + harm",INK),
          ("YELLOW","Potential benefit",GOLD),("GREEN","Alternatives",TEAL),("BLUE","Owner + next step",BLUE)]
    for i,(hat,label,c) in enumerate(hats):
        x=40+(i%3)*380; y=155+(i//3)*135
        b+=box(x,y,350,110,"#edf2f6")+txt(x+20,y+38,hat,23,c,True)+txt(x+20,y+79,label,22)
    b+=box(40,455,1120,110,PALE[2])+txt(65,494,"PURPLE SYNTHESIS — the supplied graphic's extension",25,PURPLE,True)
    b+=txt(65,535,"Combine evidence, dissent and trade-offs; choose an accountable, testable next step.",22)
    b+=strip(605,"A human review framework, not seven autonomous AI agents or a validation substitute.")
    figures["decision-hats"]=frame("Rewiring global health: improve the decision loop","Use the user's Six Thinking Hats graphic as a prompt for multiple perspectives.",b)
    return figures


def render_all():
    return {**foundations(),**workflow_figures(),"notebook-atlas":atlas_figure(),
            **program_figures(),**climate_figures()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    figures=render_all()
    if not args.check: ASSETS.mkdir(parents=True,exist_ok=True)
    failures=[]
    for name,svg in figures.items():
        path=ASSETS/(name+".svg")
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8")!=svg: failures.append(str(path))
        else: path.write_text(svg,encoding="utf-8",newline="\n")
    if failures: raise SystemExit("Stale/missing diagrams:\n"+"\n".join(failures))
    print(f"{'Checked' if args.check else 'Built'} {len(figures)} original GeoAI primer diagrams.")


if __name__=="__main__":
    main()

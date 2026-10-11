"""Generate four original vector teaching visuals for the two future directions."""
import argparse
from build_learning_media import ROOT, rect, text, path, svg, comic, write_or_check

ASSETS = ROOT / 'book/assets/futures'


def cards(title, subtitle, entries, footer, *, loop=False):
    body = rect(0,0,1280,630,'#f5f7fa',radius=0)
    body += text(30,46,title,34,'#14283f',700)
    body += text(30,89,subtitle,22,'#45576c')
    colors = ['#2459b8','#087f78','#7545b3','#a96112']
    count = len(entries); width = (1220 - (count-1)*28)/count
    for i,(heading,explanation) in enumerate(entries):
        x = 30+i*(width+28)
        body += rect(x,140,width,300,'white','#cddbe9')
        body += rect(x,140,width,8,colors[i],radius=0)
        body += text(x+18,196,heading,26,colors[i],700,width=19)
        body += text(x+18,269,explanation,23,width=21 if count==4 else 29,line=1.4)
        if loop and i<count-1:
            body += text(x+width+4,306,'→',23,'#45576c',700)
    if loop:
        body += path('M1100 454 V482 H174 V458','#087f78',3)
        body += path('M167 466 L174 455 L181 466','#087f78',3)
    body += text(30,533,footer,24,'#14283f',700,width=90)
    body += text(30,602,'Original teaching schematic. Proposed concepts, not an implemented service or measured result.',18,'#45576c')
    desc = title+'. '+subtitle+' '+'. '.join(h+': '+t for h,t in entries)+' '+footer
    return svg(body,title,desc,1280,630)


def chapter_comic(title,dialogue):
    return comic('CONCEPT',{'title':title,'dialogue':dialogue}).replace('LAB CONCEPT /','CONCEPT /').replace('Code guide','Guide')


def render_all():
    return {
        'twin-loop':cards('A digital twin needs a checked feedback loop',
            'A map is one view. A twin also needs mechanisms, evidence and an update process.',[
                ('1. Observe','Governed geography, services and dated observations. Record what is missing.'),
                ('2. Model','Explicit agents, networks and assumptions. Calibrate; validate separately.'),
                ('3. Compare','Repeat baseline and scenario runs. Show uncertainty and failures.'),
                ('4. Review','People inspect results. Document changes before updating the model.')],
                'Feedback means reviewed updates, not automatic operational decisions.',loop=True),
        'twin-cartoon':chapter_comic('A rendered city is not yet a validated twin',[
            'I made a 3D city. Is it a digital twin?',
            'Show the update cycle and the tested model.',
            'We will test failures as well as successes.']),
        'protection-layers':cards('Three controls, three different questions',
            'Combine them deliberately. None alone guarantees anonymity after release.',[
                ('Encryption','Who can read the payload? A cryptographic key protects access to plaintext.'),
                ('Masking','How precise is the display? Change or generalize positions; assess residual risk.'),
                ('Aggregation','What group detail is needed? Combine records; inspect small and rare groups.')],
                'Access control and human release review surround all three.'),
        'encryption-cartoon':chapter_comic('Encrypted storage does not make a released map private',[
            'The file is encrypted. Is this map private?',
            'Decryption exposes the locations again.',
            'Review the output and recipients before sharing.']),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    for name,content in render_all().items():
        write_or_check(ASSETS/(name+'.svg'),content,args.check)
    print('Verified' if args.check else 'Generated','four original future-direction visuals')

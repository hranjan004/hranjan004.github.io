"""Geometric editorial motion studies. Illustrative geometry, never measured traces.

The featured scenes are deliberately text-free. Their sequence tells the story;
the surrounding page supplies names, evidence and technical context.
"""
from math import sin, cos, pi
import re
import xml.etree.ElementTree as ET


def attrs(values):
    return ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in values.items())


def shape(tag, child='', **kw):
    kw.setdefault('stroke', 'var(--scene-a)')
    kw.setdefault('stroke_width', 1.35)
    kw.setdefault('fill', 'none')
    kw['data_polished']='true'
    return f'<{tag} {attrs(kw)}>{child}</{tag}>'


def path(d, child='', **kw):
    return shape('path', child, d=d, **kw)


def circle(x,y,r,child='',**kw):
    return shape('circle',child,cx=x,cy=y,r=r,**kw)


def rect(x,y,w,h,child='',**kw):
    kw.setdefault('rx',3)
    return shape('rect',child,x=x,y=y,width=w,height=h,**kw)


def ellipse(x,y,rx,ry,child='',**kw):
    return shape('ellipse',child,cx=x,cy=y,rx=rx,ry=ry,**kw)


def group(content, child='', **kw):
    return f'<g {attrs(kw)}>{content}{child}</g>'


def anim(attr,values,duration=12,**kw):
    kw.setdefault('calcMode','spline')
    if kw['calcMode']=='spline':
        count=len(values.split(';'))
        kw.setdefault('keyTimes',';'.join(str(round(i/(count-1),6)) for i in range(count)))
        kw.setdefault('keySplines',';'.join(['.42 0 .28 1']*(count-1)))
    if attr=='transform':
        return f'<animateTransform attributeName="transform" type="translate" values="{values}" dur="{duration}s" repeatCount="indefinite" {attrs(kw)}/>'
    return f'<animate attributeName="{attr}" values="{values}" dur="{duration}s" repeatCount="indefinite" {attrs(kw)}/>'


def rotate(cx,cy,duration=36,reverse=False,offset=0):
    return f'<animateTransform attributeName="transform" type="rotate" from="{offset} {cx} {cy}" to="{offset+(-360 if reverse else 360)} {cx} {cy}" dur="{duration}s" repeatCount="indefinite"/>'


def travel(d,duration=12,delay=0,r=2.4,color='c'):
    return circle(0,0,r,
        f'<animateMotion path="{d}" dur="{duration}s" begin="{delay}s" repeatCount="indefinite"/>'
        +anim('opacity','0;.95;.95;0',duration,keyTimes='0;.08;.86;1',begin=f'{delay}s'),
        fill=f'var(--scene-{color})',stroke='none',opacity='0')


def trace(d,duration=12,delay=0,color='a',width=2):
    return path(d,anim('stroke-dashoffset','1;0;0',duration,keyTimes='0;.7;1',begin=f'{delay}s'),
        stroke=f'var(--scene-{color})',stroke_width=width,pathLength='1',stroke_dasharray='1',stroke_opacity='.8')


def grid(x,y,cols,rows,step=18,opacity=.12):
    return ''.join(circle(x+c*step,y+r*step,.6,fill='var(--scene-b)',stroke='none',opacity=opacity)
                   for c in range(cols) for r in range(rows))


def wave(x,y,width,height,cycles=3,points=72):
    xy=[(x+i*width/points,y+sin(i/points*2*pi*cycles)*height) for i in range(points+1)]
    return 'M'+' L'.join(f'{a:.2f} {b:.2f}' for a,b in xy)


def chip(x,y,w=100,h=100):
    return (rect(x,y,w,h,rx=8,fill='var(--scene-depth)',fill_opacity='.7')
      +rect(x+9,y+9,w-18,h-18,rx=3,stroke_opacity='.25')
      +''.join(path(f'M{x+15+i*(w-30)/6:.2f} {y-10} V{y} M{x+15+i*(w-30)/6:.2f} {y+h} V{y+h+10}',stroke_opacity='.45') for i in range(7))
      +''.join(path(f'M{x-10} {y+15+i*(h-30)/6:.2f} H{x} M{x+w} {y+15+i*(h-30)/6:.2f} H{x+w+10}',stroke_opacity='.45') for i in range(7)))


def home(x,y,scale=1):
    return group(path('M-27 0 L0 -23 L27 0 M-21 -4 V29 H21 V-4 M-5 29 V10 H7 V29',stroke_opacity='.7')
       +rect(-12,1,6,6,rx=1,stroke_opacity='.4'),transform=f'translate({x} {y}) scale({scale})')


def microgrid():
    # One aggregate stream fans into three individually resolved load channels.
    s=grid(58,39,28,10,18,.14)
    incoming=wave(55,120,165,18,2.4)
    s+=path(incoming,stroke='var(--scene-b)',stroke_opacity='.25')+trace(incoming,11.8,width=1.8)
    s+=path('M220 120 H260',stroke_opacity='.3')+travel('M55 120 H260',11.8,-6)
    s+=circle(300,120,39,fill='var(--scene-depth)',fill_opacity='.9')
    s+=circle(300,120,48,stroke_opacity='.15')
    s+=group(path('M300 74 A46 46 0 0 1 346 120 M300 166 A46 46 0 0 1 254 120',stroke='var(--scene-c)',stroke_width=2),rotate(300,120,32))
    # Bidirectional recurrent passes and three appliance heads.
    s+=path('M280 107 C290 94 310 94 320 107 M320 107 C329 118 312 125 300 120 C287 115 272 124 280 135 C290 148 310 148 320 135',stroke_width=2)
    for i,y in enumerate([58,120,182]):
        d=f'M339 120 C375 120 373 {y} 408 {y} H494'
        s+=path(d,stroke='var(--scene-b)',stroke_opacity='.25')+travel(d,11.8,-i*3.7,color='a')
        s+=circle(510,y,15,fill='var(--scene-depth)',stroke_opacity='.75')
        s+=circle(510,y,5,anim('fill-opacity','.15;.8;.15',11.8,begin=f'{-i*3.7}s'),fill='var(--scene-a)',stroke='none')
        s+=path(wave(408,y,80,7+i*2,1+i*.5),stroke='var(--scene-a)',stroke_width=1.5,stroke_opacity='.65')
    s+=home(113,177,.55)
    return s


def gx10():
    # A unified-memory accelerator; data rings feed a parallel model lattice.
    s=grid(55,34,28,10,18,.1)
    for i in range(3):
        s+=ellipse(160,85+i*24,58,19,stroke='var(--scene-b)',stroke_opacity=.2+i*.12)
        s+=path(f'M102 {85+i*24} V{99+i*24} M218 {85+i*24} V{99+i*24}',stroke_opacity='.25')
    s+=path('M218 109 C250 109 238 120 260 120',stroke_opacity='.35')
    s+=chip(267,73,94,94)
    for y in range(4):
      for x in range(4):
        s+=rect(286+x*15,92+y*15,9,9,
          anim('fill-opacity','.12;.7;.12',13.4,begin=f'{-(x+y)*.7}s'),
          rx=2,fill='var(--scene-a)',fill_opacity='.12',stroke='none')
    s+=travel('M105 110 C190 110 210 120 267 120',13.4,-2)
    # Three prediction trajectories with separate uncertainty envelopes.
    for i in range(3):
      y=74+i*47;d=f'M374 120 C404 120 397 {y} 424 {y} C454 {y} 474 {y-17+i*8} 526 {y-6}'
      s+=path(d,stroke='var(--scene-b)',stroke_opacity='.25',stroke_width=10,stroke_linecap='round')
      s+=path(d,stroke='var(--scene-a)',stroke_width=1.5,stroke_opacity='.7')+travel(d,13.4,-4-i*3,color='c')
    s+=path('M120 184 C180 208 300 201 352 184',stroke='var(--scene-b)',stroke_dasharray='2 6',stroke_opacity='.4')
    s+=travel('M352 184 C300 201 180 208 120 184',18,-9,r=2,color='b')
    return s


def silicon():
    # Eight physical execution lanes converge into a wireframe raster triangle.
    s=grid(56,38,28,10,18,.13)
    s+=chip(88,55,150,130)
    for i in range(8):
        y=75+i*12
        s+=rect(109,y,106,5,rx=1,fill='var(--scene-b)',fill_opacity='.13',stroke='none')
        d=f'M110 {y+2.5} H215'
        s+=path(d,anim('stroke-dashoffset','120;0',9.7,begin=f'{-i*.34}s',calcMode='linear'),stroke='var(--scene-a)',stroke_width=2.5,stroke_dasharray='14 106')
        s+=path(f'M238 {y+2.5} C268 {y+2.5} 270 120 305 120',stroke_opacity='.2')
    # Framebuffer lattice and a triangle filled one scan line at a time.
    s+=rect(342,45,182,151,rx=5,stroke='var(--scene-b)',stroke_opacity='.35')
    for i in range(8):s+=path(f'M352 {62+i*17} H514',stroke_opacity='.08')
    for i in range(10):s+=path(f'M{352+i*17} 55 V186',stroke_opacity='.08')
    s+=path('M374 166 L430 68 L492 166 Z',fill='var(--scene-a)',fill_opacity='.09',stroke='var(--scene-a)',stroke_width=1.8)
    for i in range(10):
        y=78+i*8.5;left=430-(y-68)*56/98;right=430+(y-68)*62/98
        s+=path(f'M{left:.2f} {y:.2f} H{right:.2f}',anim('stroke-opacity','.05;.7;.05',9.7,begin=f'{-i*.22}s'),stroke_width=3,stroke='var(--scene-b)',stroke_opacity='.15')
    s+=path('M354 55 H514',anim('transform','0 0;0 131;0 0',19.4),stroke='var(--scene-c)',stroke_width=1,stroke_opacity='.5')
    s+=path('M305 120 H342',stroke_opacity='.3')+travel('M305 120 H342',9.7,-3)
    return s


def gpupm():
    # Four power states form a stair; voltage leads frequency at each transition.
    s=grid(57,38,28,10,18,.1)
    s+=path('M70 197 H533',stroke_opacity='.15')
    for i in range(4):
        x=105+i*115;y=158-i*31
        s+=path(f'M{x-28} 195 V{y} H{x+29}',stroke_opacity='.14')
        s+=rect(x-23,y-18,46,36,rx=6,fill='var(--scene-depth)',stroke='var(--scene-b)',stroke_opacity='.45')
        for j in range(i+1):
            s+=rect(x-12+j*7,y-7,4,14,rx=1,fill='var(--scene-a)',fill_opacity='.65',stroke='none')
    voltage='M70 158 H149 V127 H264 V96 H379 V65 H502'
    clock='M70 177 H170 V146 H285 V115 H400 V84 H502'
    s+=path(voltage,stroke='var(--scene-c)',stroke_width=1.8,stroke_opacity='.65')
    s+=path(clock,stroke='var(--scene-a)',stroke_width=1.8,stroke_opacity='.65')
    s+=travel(voltage,15.3,-1,r=3,color='c')+travel(clock,15.3,-.2,r=3,color='a')
    # Recovery follows a separate return loop rather than reversing the ramp.
    recovery='M502 84 C548 84 548 214 292 214 C148 214 67 209 70 177'
    s+=path(recovery,stroke='var(--scene-b)',stroke_opacity='.18',stroke_dasharray='2 6')
    s+=travel(recovery,22.6,-13,r=2,color='b')
    return s


def tpm():
    # Evidence crosses a challenge ring; the seal resolves into a verification tick.
    s=grid(58,38,28,10,18,.1)
    s+=path('M285 40 L344 61 V112 C344 155 314 178 285 192 C256 178 226 155 226 112 V61 Z',
      stroke='var(--scene-a)',stroke_width=1.6,fill='var(--scene-a)',fill_opacity='.035')
    s+=path('M285 54 L331 70 V111 C331 146 307 165 285 176 C263 165 239 146 239 111 V70 Z',stroke_opacity='.15')
    s+=group(circle(285,112,31,stroke='var(--scene-b)',stroke_dasharray='1 7',stroke_width=2),rotate(285,112,42))
    s+=path('M270 113 L281 124 L302 100',anim('stroke-opacity','.3;1;.3',14.7),stroke_width=3,stroke='var(--scene-c)')
    for i in range(4):
        y=63+i*35
        s+=rect(80,y,45,24,rx=4,stroke='var(--scene-b)',stroke_opacity='.4')
        for j in range(4):s+=path(f'M{89+j*8} {y+7} V{y+17}',stroke_width=2,stroke_opacity='.2')
        d=f'M125 {y+12} C177 {y+12} 183 112 226 112'
        s+=path(d,stroke_opacity='.15')+travel(d,14.7,-i*2.9,r=2)
    s+=path('M344 112 H435',stroke_opacity='.25')+travel('M344 112 H435',14.7,-8)
    s+=circle(470,112,29,stroke='var(--scene-b)',stroke_opacity='.5')
    s+=circle(470,112,20,anim('r','20;24;20',14.7),stroke='var(--scene-a)',stroke_opacity='.25')
    s+=path('M458 112 L467 121 L483 102',stroke_width=2,stroke='var(--scene-a)')
    return s


def gemma():
    # Three distinct signal fingerprints are reconciled into one review object.
    s=grid(58,38,28,10,18,.1)
    for i,y in enumerate([58,120,182]):
        s+=circle(112,y,22,stroke='var(--scene-b)',stroke_opacity='.4')
        s+=path(wave(93,y,38,7,1+i),stroke='var(--scene-a)',stroke_width=1.2)
        d=f'M134 {y} C200 {y} 203 120 265 120'
        s+=path(d,stroke_opacity='.2')+travel(d,16.1,-i*4.1,r=2.6)
    # The shared adapter is a compact, rotating interference lattice.
    for i in range(3):
        s+=group(ellipse(300,120,36,14,stroke='var(--scene-b)',stroke_opacity='.45'),
          rotate(300,120,36+i*6,reverse=i%2==1,offset=i*60),transform=f'rotate({i*60} 300 120)')
    s+=circle(300,120,7,anim('r','5;8;5',16.1),fill='var(--scene-a)',fill_opacity='.55',stroke='none')
    s+=path('M338 120 H427',stroke_opacity='.25')+travel('M338 120 H427',16.1,-10)
    s+=rect(435,68,80,104,rx=7,stroke='var(--scene-b)',stroke_opacity='.5',fill='var(--scene-depth)',fill_opacity='.8')
    s+=path('M451 91 H494 M451 105 H486 M451 119 H495 M451 133 H477',stroke_opacity='.2',stroke_width=2)
    s+=path('M456 151 L465 159 L484 141',anim('stroke-opacity','.2;.9;.2',16.1),stroke='var(--scene-c)',stroke_width=2)
    return s


def gpt2():
    # A moving cache tile feeds eight SIMD lanes, accumulating a matrix result.
    s=grid(50,36,29,10,18,.08)
    for row in range(6):
      for col in range(7):
        s+=rect(70+col*15,58+row*18,10,12,rx=1,fill='var(--scene-b)',fill_opacity='.12',stroke='none')
    s+=rect(66,54,48,58,anim('x','66;111;111;66;66',16.6)+anim('y','54;54;108;108;54',16.6),rx=3,stroke='var(--scene-c)',stroke_width=1.6)
    for i in range(8):
        y=65+i*15
        s+=path(f'M220 {y} H394',stroke='var(--scene-b)',stroke_width=4,stroke_opacity='.12')
        s+=path(f'M220 {y} H394',anim('stroke-dashoffset','190;0',8.3,begin=f'{-i*.13}s',calcMode='linear'),stroke='var(--scene-a)',stroke_width=3,stroke_dasharray='20 170')
    s+=path('M180 112 C198 112 201 65 220 65 M180 122 C198 122 201 170 220 170',stroke_opacity='.25')
    for row in range(4):
      for col in range(4):
        s+=rect(446+col*17,82+row*19,12,14,
           anim('fill-opacity','.1;.8;.1',16.6,begin=f'{-(row+col)*.4}s'),
           rx=2,fill='var(--scene-a)',fill_opacity='.25',stroke='none')
    s+=path('M394 65 C425 65 413 112 446 112 M394 170 C425 170 413 122 446 122',stroke_opacity='.25')
    return s


def esp32():
    # A continuous analog signal becomes paired samples and a circular DMA buffer.
    s=grid(53,35,28,10,18,.12)
    d=wave(65,117,170,35,1.5)
    s+=path(d,stroke='var(--scene-b)',stroke_opacity='.65',stroke_width=1.6)
    for i in range(12):
        x=69+i*14;y=117+sin((x-65)/170*3*pi)*35
        s+=path(f'M{x} 167 V{y:.2f}',stroke_opacity='.13')
        s+=circle(x,round(y,2),2.5,anim('fill-opacity','.15;1;.15',12.9,begin=f'{-i*.32}s'),fill='var(--scene-c)',fill_opacity='.4',stroke='none')
    s+=path('M250 117 H300',stroke_opacity='.3')+travel('M250 117 H300',12.9,-4)
    s+=chip(311,70,95,95)
    for i in range(8):
      angle=i*pi/4;x=358.5+25*cos(angle);y=117.5+25*sin(angle)
      s+=rect(round(x-4,2),round(y-4,2),8,8,anim('fill-opacity','.12;.9;.12',12.9,begin=f'{-i*.55}s'),rx=2,fill='var(--scene-a)',fill_opacity='.2',stroke='none')
    s+=circle(358.5,117.5,13,stroke_opacity='.15')
    for i in range(2):
      d=f'M416 {108+i*20} H519'
      s+=path(d,stroke='var(--scene-b)',stroke_opacity='.3',stroke_dasharray='3 6')
      s+=travel(d,12.9,-8-i*2,r=2,color='a')
    s+=rect(524,93,15,49,rx=2,stroke_opacity='.3')
    return s


def nilm():
    # Aggregate energy separates into appliance signatures beneath a moving lens.
    s=grid(55,35,28,10,18,.12)
    points=[(63,120),(100,120),(100,83),(150,83),(150,120),(185,120),(185,66),(224,66),(224,120),(268,120),(268,94),(303,94),(303,120),(349,120),(349,78),(391,78),(391,120),(447,120),(447,99),(491,99),(491,120),(534,120)]
    s+=path('M'+' L'.join(f'{x} {y}' for x,y in points),stroke='var(--scene-a)',stroke_width=2,stroke_opacity='.65')
    for i in range(3):
      y=155+i*17
      s+=path(f'M63 {y} H534',stroke_opacity='.08')
      xs=[(100,150),(185,224),(349,391)][i]
      s+=path(f'M63 {y} H{xs[0]} V{y-11} H{xs[1]} V{y} H534',stroke='var(--scene-b)',stroke_opacity='.45')
    lens=circle(0,112,43,stroke='var(--scene-c)',stroke_opacity='.7')+path('M29 143 L44 161',stroke='var(--scene-c)',stroke_width=3)+circle(0,112,34,stroke_opacity='.12')
    s+=group(lens,'<animateTransform attributeName="transform" type="translate" values="120 0;370 0;120 0" dur="20.8s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".42 0 .28 1;.42 0 .28 1"/>',transform='translate(120 0)')
    return s


def anylog():
    # Three physical partitions reveal one aligned path through a distributed query.
    s=grid(55,36,28,10,18,.08)
    for i in range(3):
      x=105+i*155;y=70+i*13
      s+=group(rect(x,y,92,115,rx=5,fill='var(--scene-depth)',fill_opacity='.7',stroke='var(--scene-b)',stroke_opacity='.4')
          +''.join(path(f'M{x+14} {y+21+j*17} H{x+76}',stroke_opacity='.15',stroke_width=2) for j in range(5)))
    route='M65 116 H151 V142 H306 V168 H461 V116 H541'
    s+=path(route,stroke='var(--scene-c)',stroke_opacity='.45',stroke_width=1.7)
    s+=travel(route,18.2,-5,r=3,color='a')
    for x,y in [(151,116),(306,142),(461,168)]:
      s+=circle(x,y,6,anim('r','4;8;4',18.2,begin=f'{-x/40:.2f}s'),stroke='var(--scene-a)',stroke_opacity='.65',fill='var(--scene-depth)')
    return s


def fire():
    # A hand-drawn flame and a split nucleus, held in visual balance.
    s=path('M297 46 V194',stroke_opacity='.1')
    outer='M154 184 C114 167 122 132 150 110 C176 89 180 66 176 42 C224 86 203 113 220 126 C226 112 232 102 232 89 C268 141 248 185 205 195 C187 198 169 193 154 184 Z'
    s+=path(outer,anim('fill-opacity','.04;.16;.04',17.3),fill='var(--scene-c)',stroke='var(--scene-c)',stroke_width=1.6)
    inner='M174 180 C155 159 176 144 183 119 C207 145 191 153 205 164 C211 151 215 145 216 137 C236 172 210 192 190 188 Z'
    s+=path(inner,anim('opacity','.45;.9;.45',17.3),fill='var(--scene-a)',fill_opacity='.1',stroke_width=1)
    nucleus=''
    for x,y in [(404,109),(417,99),(430,109),(404,125),(417,134),(430,125)]:
      nucleus+=circle(x,y,8,fill='var(--scene-b)',fill_opacity='.15',stroke='var(--scene-b)',stroke_opacity='.7')
    s+=nucleus
    for angle in [0,60,120]:
      s+=group(ellipse(417,117,77,24,stroke='var(--scene-a)',stroke_opacity='.22'),rotate(417,117,48,offset=angle),transform=f'rotate({angle} 417 117)')
    s+=travel('M323 117 H403',17.3,-2,r=2.4,color='c')
    s+=travel('M431 110 C472 87 481 64 507 48',17.3,-9,r=2.2,color='a')
    s+=travel('M431 124 C472 150 483 176 513 188',17.3,-9,r=2.2,color='a')
    return s


FEATURED={
 'microgrid-manager':microgrid,'gx10-microgrid':gx10,
 'silicon-performance-lab':silicon,'gpupm-lab':gpupm,
 'tpm-integrity-monitor':tpm,'gemma-anomaly':gemma,
 'gpt2-performance':gpt2,'esp32-microgrid-meter':esp32,
 'nilm-labels':nilm,'anylog-field-notes':anylog,'fire-and-fission':fire,
}


def refine(scenes):
    """Preserve each subject; remove prose captions and rebuild featured motion."""
    result={}
    for identity,source in scenes.items():
        if identity in FEATURED:
            result[identity]=FEATURED[identity]()
            continue
        tree=ET.fromstring('<g>'+source+'</g>')
        # Keep mathematical labels and short component names. Narrative belongs
        # in the page copy, not tiny all-caps text over an animated illustration.
        for parent in tree.iter():
            for child in list(parent):
                if child.tag=='text':
                    text=''.join(child.itertext()).strip()
                    y=float(child.get('y','0'))
                    if y>=205 or len(text)>14 or '→' in text or '·' in text:
                        parent.remove(child)
        result[identity]=''.join(ET.tostring(child,encoding='unicode') for child in tree)
    return result


def tesphase():
    # Customer observations enter a mobile product; energy becomes a usable view.
    s=grid(60,38,27,10,18,.08)
    s+=rect(243,25,114,190,rx=16,fill='var(--scene-depth)',fill_opacity='.9',stroke='var(--scene-a)',stroke_width=1.5)
    s+=path('M284 35 H316',stroke_width=3,stroke_opacity='.4')
    s+=circle(300,95,29,stroke_opacity='.15',stroke_width=5)
    s+=circle(300,95,29,anim('stroke-dashoffset','170;40;170',18.7),stroke='var(--scene-c)',stroke_width=5,stroke_dasharray='150 40',transform='rotate(-90 300 95)')
    for i in range(3):
      s+=rect(263,143+i*17,74,7,rx=2,fill='var(--scene-b)',fill_opacity='.1',stroke='none')
      s+=rect(263,143+i*17,37+i*12,7,anim('width',f'{25+i*7};{60-i*7};{25+i*7}',18.7,begin=f'{-i*2.1}s'),rx=2,fill='var(--scene-a)',fill_opacity='.35',stroke='none')
    for i,(x,y) in enumerate([(123,65),(99,119),(155,177)]):
      s+=circle(x,y,8,stroke='var(--scene-b)',stroke_opacity='.45')
      s+=path(f'M{x-15} {y+24} C{x-15} {y+5} {x+15} {y+5} {x+15} {y+24}',stroke='var(--scene-b)',stroke_opacity='.45')
      d=f'M{x+20} {y+4} C205 {y+4} 208 117 243 117'
      s+=path(d,stroke_opacity='.12')+travel(d,18.7,-i*4,r=2)
    s+=home(464,121,1.05)
    s+=circle(470,60,12,stroke='var(--scene-c)',stroke_opacity='.7')
    for i in range(8):
      a=i*pi/4
      s+=path(f'M{470+18*cos(a):.2f} {60+18*sin(a):.2f} L{470+23*cos(a):.2f} {60+23*sin(a):.2f}',stroke='var(--scene-c)',stroke_opacity='.3')
    d='M357 117 C392 117 400 117 432 117'
    s+=path(d,stroke_opacity='.2')+travel(d,18.7,-10,color='a')
    return s


def slugboard():
    # A live calendar connects people around a shared event.
    s=grid(60,39,27,10,18,.1)
    s+=rect(198,46,204,147,rx=8,stroke='var(--scene-b)',stroke_opacity='.45',fill='var(--scene-depth)',fill_opacity='.8')
    s+=path('M198 78 H402 M230 34 V57 M370 34 V57',stroke_opacity='.5',stroke_width=2)
    for r in range(3):
      for c in range(5):
        s+=rect(217+c*35,94+r*28,25,18,rx=3,fill='var(--scene-a)',fill_opacity='.08',stroke_opacity='.1')
    s+=rect(287,122,25,18,anim('fill-opacity','.18;.7;.18',16.9),rx=3,fill='var(--scene-c)',fill_opacity='.3',stroke='var(--scene-c)',stroke_opacity='.8')
    for i,(x,y) in enumerate([(92,95),(125,177),(499,74),(474,171)]):
      s+=circle(x,y,18,stroke='var(--scene-b)',stroke_opacity='.4')+circle(x,y-3,5,stroke_opacity='.6')
      s+=path(f'M{x-9} {y+9} Q{x} {y-3} {x+9} {y+9}',stroke_opacity='.6')
      tx=198 if x<300 else 402
      d=f'M{x+(18 if x<300 else -18)} {y} C{(x+tx)/2} {y} {(x+tx)/2} 131 {tx} 131'
      s+=path(d,stroke_opacity='.13')+travel(d,16.9,-i*3.4,r=2,color='a')
    return s


def cache():
    # The long origin path fills a cache; subsequent requests take the local loop.
    s=grid(60,39,27,10,18,.11)
    s+=rect(70,78,65,84,rx=7,stroke='var(--scene-b)',stroke_opacity='.5')
    s+=path('M84 97 H120 M84 111 H112 M84 125 H119 M84 139 H105',stroke_opacity='.2')
    s+=rect(253,66,94,108,rx=7,stroke='var(--scene-a)',stroke_opacity='.6',fill='var(--scene-depth)',fill_opacity='.8')
    for i in range(4):
      s+=rect(268,82+i*20,64,11,anim('fill-opacity','.08;.45;.45;.08',19.6,begin=f'{-i*.8}s'),rx=2,fill='var(--scene-a)',fill_opacity='.2',stroke='none')
    for i in range(3):
      s+=ellipse(478,79+i*28,37,11,stroke='var(--scene-b)',stroke_opacity='.5')
      s+=path(f'M441 {79+i*28} V{99+i*28} C441 {114+i*28} 515 {114+i*28} 515 {99+i*28} V{79+i*28}',stroke='var(--scene-b)',stroke_opacity='.35')
    long='M135 97 C160 33 410 27 478 68'
    returning='M478 166 C430 211 340 207 300 174'
    fast='M135 114 H253 M253 145 H135'
    s+=path(long,stroke_opacity='.17')+path(returning,stroke_opacity='.17')
    s+=travel(long,19.6,-1,r=2,color='b')+travel(returning,19.6,-8,r=2,color='b')
    s+=path(fast,stroke='var(--scene-c)',stroke_opacity='.5',stroke_width=1.7)
    s+=travel('M135 114 H253',6.1,-1,r=2.8,color='c')+travel('M253 145 H135',6.1,-4,r=2.8,color='c')
    return s


def weather():
    # An environmental signal is acquired locally and collected on the Pi.
    s=grid(60,39,27,10,18,.08)
    s+=circle(118,83,24,stroke='var(--scene-c)',stroke_opacity='.6')
    rays=''
    for i in range(12):
      a=i*pi/6
      rays+=path(f'M{118+32*cos(a):.2f} {83+32*sin(a):.2f} L{118+40*cos(a):.2f} {83+40*sin(a):.2f}',stroke='var(--scene-c)',stroke_opacity='.35')
    s+=group(rays,rotate(118,83,70))
    s+=path('M75 170 H152 C178 170 179 139 156 137 C153 107 112 109 107 133 C83 124 63 148 75 170 Z',stroke='var(--scene-b)',fill='var(--scene-depth)',fill_opacity='.85',stroke_opacity='.5')
    s+=chip(260,79,83,83)
    s+=path(wave(276,120,51,12,1.5),stroke='var(--scene-a)',stroke_width=1.5)
    d='M171 146 C211 146 219 120 250 120'
    s+=path(d,stroke_opacity='.2')+travel(d,17.8,-1)
    for i in range(3):
      s+=path(f'M{355+i*12} {104-i*8} Q{371+i*15} 120 {355+i*12} {136+i*8}',anim('stroke-opacity','.1;.6;.1',17.8,begin=f'{-i*.5}s'),stroke='var(--scene-a)')
    s+=rect(436,74,89,96,rx=7,stroke='var(--scene-b)',stroke_opacity='.45')
    for i in range(3):
      s+=path(f'M450 {94+i*27} H510',stroke_opacity='.2')+circle(508,94+i*27,2.5,anim('fill-opacity','.2;.9;.2',17.8,begin=f'{-i*2}s'),fill='var(--scene-c)',stroke='none')
    s+=travel('M395 120 H436',17.8,-9,r=2,color='a')
    return s


FEATURED.update({'tesphase':tesphase,'slug-board':slugboard,'caching-proxy':cache,'weather-station':weather})

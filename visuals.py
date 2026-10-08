"""One topic-specific SVG composition per project and essay.

Motion uses native SVG animation, with no timers or external image dependencies.
The same subject keeps its illustration when opened from a card to a detail page.
"""
from html import escape


def animate(attr, values, duration=6, **extra):
    attrs=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in extra.items())
    if attr == 'transform':
        values=values.replace('translate(', '').replace(')', '')
        return f'<animateTransform attributeName="transform" type="translate" values="{values}" dur="{duration}s" repeatCount="indefinite" {attrs}/>'
    return f'<animate attributeName="{attr}" values="{values}" dur="{duration}s" repeatCount="indefinite" {attrs}/>'


def line(d, child='', **attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<path d="{d}" {extra}>{child}</path>'


def circle(x,y,r,child='',**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<circle cx="{x}" cy="{y}" r="{r}" {extra}>{child}</circle>'


def rect(x,y,w,h,child='',**attrs):
    attrs.setdefault('fill', 'var(--visual-bg)')
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" {extra}>{child}</rect>'


def text(x,y,label,size=12):
    return f'<text x="{x}" y="{y}" text-anchor="middle" stroke="none" fill="currentColor" font-size="{size}" font-family="Arial,sans-serif" letter-spacing="1">{escape(label)}</text>'


def travel(path,duration=6):
    return circle(0,0,4,f'<animateMotion path="{path}" dur="{duration}s" repeatCount="indefinite"/>',fill='currentColor')


def spin(cx,cy,duration):
    return f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{duration}s" repeatCount="indefinite"/>'


SCENES={}
# PROJECTS: thirteen distinct systems, rather than shared generic cover art.
SCENES['microgrid-manager']=(
    line('M110 65 H300 V170 H485 M110 65 V170 H300 M300 65 H485 V170')+
    ''.join(rect(x-42,y-23,84,46)+text(x,y+4,label,10) for x,y,label in [(110,65,'LOAD'),(300,65,'SOLAR'),(485,65,'STORAGE'),(300,170,'DECISIONS')])+
    travel('M152 65 H257',3)+travel('M300 90 V145',4)+travel('M443 65 H355 V170 H343',5))
SCENES['gpt2-performance']=(
    ''.join(rect(130+c*25,35+r*25,19,19,animate('fill-opacity','0.1;0.9;0.1',3+r*.3,begin=f'{c*.12}s'),fill='currentColor',fill_opacity='.1') for r in range(5) for c in range(6))+
    line('M320 65 H410 M320 95 H410 M320 125 H410')+rect(410,42,65,111)+text(441,104,'AVX2',13)+text(213,195,'TILE → REUSE → VECTORIZE',12))
SCENES['osmosis']=(rect(125,25,350,172)+line('M300 25 V84 M300 136 V197')+
    ''.join(circle(x,y,7,animate('cx',f'{x};{end};{x}',4+i*.5)+animate('cy',f'{y};{y+20};{y}',3+i*.4),fill='currentColor') for i,(x,y,end) in enumerate([(165,60,245),(210,130,274),(350,65,430),(410,150,330)]))+text(300,226,'PIXELS · COLLISIONS · FRAME CLOCK',11))
SCENES['caching-proxy']=(rect(70,65,95,70)+text(117,105,'CLIENT')+rect(235,45,130,110)+text(300,75,'CACHE')+
    ''.join(line(f'M257 {96+i*14} H343') for i in range(3))+rect(435,65,95,70)+text(482,105,'ORIGIN')+line('M165 100 H235 M365 100 H435')+travel('M170 95 H225 V130 H170',3.5)+text(300,205,'REUSE A COMPLETE RESPONSE',12))
SCENES['gemma-anomaly']=(
    ''.join(circle(125,y,21)+text(125,y+4,f'P{i+1}',11)+line(f'M146 {y} L275 110') for i,y in enumerate([45,110,175]))+
    rect(275,75,95,70)+text(322,104,'GEMMA')+text(322,123,'ADAPTER',9)+line('M370 110 H440')+rect(440,75,100,70)+text(490,115,'REVIEW')+
    travel('M146 45 L275 110 H440',5)+travel('M146 175 L275 110 H440',7)+text(300,222,'THREE PANELS · ONE INCIDENT',11))
SCENES['tesphase']=(rect(210,12,130,208)+rect(221,34,108,158)+line('M257 23 H293')+circle(275,204,4)+text(275,61,'TESPHASE',11)+
    ''.join(rect(235,88+i*34,80,22,animate('width',f'25;80;25',5+i),fill='currentColor',fill_opacity='.12') for i in range(3))+
    line('M150 84 L120 105 L150 125 M390 84 L420 105 L390 125')+text(455,174,'NEED',10)+text(105,174,'LISTEN',10))
SCENES['slug-board']=(
    ''.join(rect(95+i*142,40,125,147)+text(157+i*142,64,label,10) for i,label in enumerate(['DISCOVER','RSVP','DISCUSS']))+
    rect(109,85,96,30)+rect(109,130,96,30)+rect(251,85,96,30,animate('y','85;130;85',7))+
    line('M393 94 H475 M393 108 H455 M393 137 H470')+text(300,220,'EVENTS ACROSS CAMPUS',12))
SCENES['fpga-http']=(rect(242,40,120,120)+text(302,92,'FPGA')+text(302,114,'HTTP?',13)+
    ''.join(line(f'M{254+i*16} 25 V40 M{254+i*16} 160 V175') for i in range(7))+
    line('M80 100 H242 M362 100 H520')+travel('M80 100 H225',4.5)+line('M385 87 L398 100 L385 113',animate('opacity','0.15;1;0.15',4))+text(300,216,'SOFTWARE REFERENCE → HARDWARE',11))
SCENES['quick-add']=(circle(155,100,38)+text(155,107,'A',23)+circle(445,100,38)+text(445,107,'B',23)+
    line('M193 100 H407')+text(300,73,'7 + 5 = ?',23)+rect(222,128,156,12)+rect(222,128,156,12,animate('width','156;0;156',8),fill='currentColor')+text(300,201,'ONE ROUND · TWO PLAYERS',12))
SCENES['quick-decode']=(
    ''.join(rect(115+i*48,60,35,58)+text(132+i*48,97,str(i%2),24) for i in range(8))+
    rect(115,134,35,5,animate('x','115;163;211;259;307;355;403;451;115',8,calcMode='discrete'),fill='currentColor')+
    text(300,195,'COUNT · LOAD · DECODE',12))
SCENES['spiking-networks']=(
    ''.join(line(f'M85 {55+i*52} H{150+i*65} l8 -28 l8 56 l8 -28 H515',animate('stroke-dashoffset','180;0',3+i),stroke_dasharray='170 10') for i in range(3))+
    text(300,222,'ENCODING → MEMBRANE → SPIKES',11))
SCENES['weather-station']=(circle(163,82,25)+line('M163 43 V34 M125 82 H115 M192 55 L202 46')+
    line('M115 126 Q120 96 150 112 Q175 78 197 110 Q233 98 237 128 Z')+
    ''.join(line(f'M{142+i*29} 141 v15',animate('transform','translate(0 0);translate(0 16)',2+i*.3)) for i in range(3))+
    rect(340,65,100,85)+text(390,100,'ESP32')+text(390,125,'RUST',11)+line('M250 110 H330')+text(300,215,'SENSE · ACQUIRE · REPORT',12))
SCENES['battle-boats']=(
    ''.join(line(f'M{175+i*35} 30 V170 M175 {30+i*35} H315') for i in range(5))+
    rect(212,67,66,30,fill='currentColor',fill_opacity='.18')+
    circle(282,137,12,animate('r','3;18;3',4),opacity='.7')+
    line('M380 70 H415 L420 40 L430 120 L438 70 H475',animate('stroke-dashoffset','160;0',5),stroke_dasharray='140 20')+text(300,214,'INTERRUPTS → GAME STATE',12))
# WRITING: each essay gets a composition reflecting its own central question.
SCENES['fire-and-fission']=(line('M240 177 C185 120 260 100 244 35 C310 88 260 112 287 143 C302 113 316 116 321 87 C369 160 304 199 240 177 Z',animate('d','M240 177 C185 120 260 100 244 35 C310 88 260 112 287 143 C302 113 316 116 321 87 C369 160 304 199 240 177 Z;M240 177 C205 130 235 90 258 35 C285 90 283 114 287 143 C310 104 330 122 321 87 C350 157 304 199 240 177 Z;M240 177 C185 120 260 100 244 35 C310 88 260 112 287 143 C302 113 316 116 321 87 C369 160 304 199 240 177 Z',7))+circle(360,87,36)+circle(360,87,6,animate('r','3;9;3',5),fill='currentColor'))
SCENES['famine-as-foundation']=(line('M300 190 V65 M300 90 Q255 85 261 56 Q291 53 300 90 M300 124 Q348 112 345 84 Q308 88 300 124 M300 157 Q250 151 253 120 Q288 120 300 157')+circle(300,119,84,animate('stroke-dashoffset','0;528',26),stroke_dasharray='90 42'))
SCENES['participation-and-power']=(rect(235,30,130,78)+line('M246 96 L280 65 L306 90 L348 44')+''.join(circle(170+i*52,158,10)+line(f'M{170+i*52} 169 v28') for i in range(6))+line('M300 110 V148',animate('stroke-width','1;5;1',6))+line('M165 210 H435'))
SCENES['what-is-art-for']=(line('M180 117 Q300 13 420 117 Q300 218 180 117 Z')+circle(300,117,34)+circle(300,117,10,animate('cx','284;316;284',8),fill='currentColor')+line('M450 82 V152',animate('opacity','.15;1;.15',4)))
SCENES['reconstructing-memory']=( ''.join(rect(x,y,w,h,animate('opacity',f'{o};1;{o}',5+i)) for i,(x,y,w,h,o) in enumerate([(210,40,64,55,.3),(284,36,83,46,.6),(200,107,70,67,.5),(288,95,55,62,.2),(354,94,51,93,.4)]))+line('M200 202 H406',stroke_dasharray='3 8'))
SCENES['capstone-reflection']=(line('M180 103 L300 32 L420 103 V199 H180 Z')+line('M180 137 H231 L245 113 L260 157 L275 137 H420',animate('stroke-dashoffset','120;0',6),stroke_dasharray='110 10')+rect(281,162,40,37))
SCENES['electoral-systems']=(rect(183,62,92,115)+rect(325,62,92,115)+line('M204 83 H255 M345 83 H397')+rect(212,20,35,40,animate('y','20;96;20',7))+rect(354,20,35,40,animate('y','96;20;96',7))+text(229,207,'REPRESENTATION',9)+text(371,207,'ACCOUNTABILITY',9))
SCENES['ovid-aftermath']=(line('M165 153 C202 42 267 53 300 108 S387 172 438 77',animate('d','M165 153 C202 42 267 53 300 108 S387 172 438 77;M165 153 C202 172 267 160 300 108 S387 43 438 77;M165 153 C202 42 267 53 300 108 S387 172 438 77',12))+line('M170 187 H430')+''.join(circle(210+i*35,190,3,fill='currentColor') for i in range(6)))
SCENES['sources-of-law']=(line('M300 37 V190 M253 190 H347 M205 75 H395 M205 75 V128 M395 75 V128')+line('M170 128 Q205 177 240 128 Z M360 128 Q395 177 430 128 Z',animate('transform','translate(0 -4);translate(0 4);translate(0 -4)',8))+circle(300,75,7,fill='currentColor'))
SCENES['royce']=(line('M170 50 H265 V100 H355 V150 H440')+line('M440 150 V195 H135 V50 H170',animate('stroke-dashoffset','0;-200',12),stroke_dasharray='8 9')+''.join(rect(x,y,48,27) for x,y in [(170,37),(267,87),(357,137)]))
SCENES['piece-by-piece']=( ''.join(rect(170+c*46,40+r*44,40,38,animate('fill-opacity','.03;.45;.03',5+c+r,begin=f'{c*.3+r*.4}s'),fill='currentColor',fill_opacity='.03') for c in range(6) for r in range(4)))
SCENES['liberty']=(line('M208 190 V63 Q300 0 392 63 V190 M208 63 H392')+line('M208 63 L278 88 V214 L208 190 Z',animate('d','M208 63 L278 88 V214 L208 190 Z;M208 63 L226 68 V196 L208 190 Z;M208 63 L278 88 V214 L208 190 Z',10))+line('M300 158 H440 L426 147 M440 158 L426 169'))
SCENES['unfinished-revolution']=(circle(300,97,52)+line('M300 149 V210 M273 185 H327')+circle(300,97,72,animate('stroke-dashoffset','0;-452',22),stroke_dasharray='320 132'))
SCENES['johnson-reagan']=(line('M300 195 V127 L195 55 M300 127 L405 55')+travel('M300 195 V127 L195 55',6)+travel('M300 195 V127 L405 55',9)+text(182,30,'PUBLIC ACTION',10)+text(420,30,'LIMITED STATE',10))
SCENES['under-the-thumb']=(circle(300,120,82)+line('M300 38 V51 M382 120 H369 M300 202 V189 M218 120 H231')+'<g>'+line('M300 120 V62 M300 120 L338 144')+spin(300,120,30)+'</g>'+circle(300,120,5,fill='currentColor'))
SCENES['flood-myths']=( ''.join(line(f'M110 {100+i*25} Q160 {70+i*25} 210 {100+i*25} T310 {100+i*25} T410 {100+i*25} T510 {100+i*25}',animate('transform','translate(0 0);translate(-20 8);translate(0 0)',5+i)) for i in range(4))+line('M242 59 H357 L338 88 H258 Z M300 59 V22 L329 53 H300'))
SCENES['fire-fission-reflection']=(circle(300,120,12,fill='currentColor')+''.join('<g>'+f'<ellipse cx="300" cy="120" rx="110" ry="38" transform="rotate({angle} 300 120)"/>'+spin(300,120,19+idx*7)+'</g>' for idx,angle in enumerate([0,60,120])))
SCENES['connection-installation']=(line('M145 32 H455')+''.join(line(f'M{160+i*25} 32 Q{230+i*14} 128 {160+i*25} 208',animate('d',f'M{160+i*25} 32 Q{230+i*14} 128 {160+i*25} 208;M{160+i*25} 32 Q{180+i*14} 128 {180+i*25} 208;M{160+i*25} 32 Q{230+i*14} 128 {160+i*25} 208',6+i*.4)) for i in range(12)))
SCENES['slug-board-reflection']=(rect(140,55,115,110)+rect(345,55,115,110)+line('M255 110 H283 M317 110 H345',stroke_dasharray='4 5')+line('M290 91 L310 130 M310 91 L290 130',animate('opacity','.25;1;.25',4))+text(197,194,'LOCAL SUCCESS',10)+text(403,194,'INTEGRATION GAP',10))
SCENES['nilm-labels']=(line('M120 135 H193 L193 68 H233 V135 H300 L308 112 L316 135 H350 V91 H402 V135 H480')+line('M120 181 H480',stroke_dasharray='5 7')+rect(171,44,84,112,animate('x','150;350;150',10),fill='currentColor',fill_opacity='.07')+text(300,217,'CHECK THE SIGNAL AGAINST THE LABEL',10))
SCENES['anylog-field-notes']=( ''.join(rect(150+i*100,45,80,130)+line(f'M{160+i*100} 79 H{220+i*100} M{160+i*100} 101 H{220+i*100} M{160+i*100} 123 H{220+i*100}') for i in range(3))+
    circle(410,168,22,animate('cx','175;410;175',11))+line('M426 184 L445 205',animate('transform','translate(-235 0);translate(0 0);translate(-235 0)',11)))


def illustration(identity, static=False):
    """Stable identity is shared by the preview and detail, never by unrelated work."""
    import re
    shapes=SCENES[identity]
    if static:
        shapes=re.sub(r'<animate(?:Motion|Transform)?\b[^>]*/>','',shapes)
    return f'<svg class="topic-visual" data-visual="{identity}" viewBox="0 0 600 240" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shapes}</svg>'

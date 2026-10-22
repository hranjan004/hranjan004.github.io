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


# Each subject has its own palette: background, depth, and three accents.
PALETTES={
 'microgrid-manager':('#0b2825','#16443c','#6ee7a6','#f4ce62','#6edbe8'),
 'gpt2-performance':('#17172f','#30264c','#c4a5ff','#ffb77c','#6ee5ed'),
 'osmosis':('#092a3b','#174653','#55dff0','#ff87aa','#ffe38a'),
 'caching-proxy':('#12263b','#253c55','#79caff','#7de7c4','#ffd07a'),
 'gemma-anomaly':('#251633','#42264b','#d9a0ff','#ffadcf','#8bdcec'),
 'tesphase':('#282010','#463c20','#ffd76b','#9ce5c0','#ff9e7c'),
 'slug-board':('#182339','#34415b','#87c7ff','#ffb887','#a5e0c5'),
 'fpga-http':('#202528','#3c4448','#7ee8cf','#f3c16c','#9bc6ff'),
 'quick-add':('#271c2b','#4b3148','#ff9cb9','#8cdfed','#ffdc8e'),
 'quick-decode':('#152c2a','#2c4740','#7bd7b2','#d3b0ff','#ffe09c'),
 'spiking-networks':('#23152a','#442641','#ff9db1','#bfa7ff','#7ee8d5'),
 'weather-station':('#102938','#27444f','#78d6ed','#ffd379','#bcebab'),
 'battle-boats':('#101f36','#263b54','#82bfff','#fba59a','#7fe2d9'),
 'fire-and-fission':('#2f171b','#542626','#ff9960','#ffd978','#c5a6ff'),
 'famine-as-foundation':('#1b2a1c','#354d2c','#b7df8b','#f3cd72','#f39e84'),
 'participation-and-power':('#251c36','#443357','#b9a4ff','#ffb6a0','#79e1d1'),
 'what-is-art-for':('#162d32','#2b4b4e','#76e0d1','#f8c793','#c5b1f6'),
 'reconstructing-memory':('#252039','#453957','#d4b5ff','#ffa993','#8bd6e5'),
 'capstone-reflection':('#172b26','#2d4a40','#87e0bb','#efcc7e','#a4c9ff'),
 'electoral-systems':('#1b2440','#354365','#9cbbff','#ffc29a','#9de6d5'),
 'ovid-aftermath':('#302329','#59424b','#f5b1c8','#b7c5ff','#f7db99'),
 'sources-of-law':('#282618','#494932','#e7d490','#9edbc1','#afbdff'),
 'royce':('#18293b','#2e465b','#86d0ff','#eac480','#ffaab5'),
 'piece-by-piece':('#302126','#554039','#ffbd88','#a6ddc6','#c6b1ff'),
 'liberty':('#162f32','#305253','#96e4d0','#f8d489','#ffb4ad'),
 'unfinished-revolution':('#311e34','#563a55','#f7b0df','#d3bbff','#ffc18b'),
 'johnson-reagan':('#242438','#43445d','#b7c9ff','#ffbd9b','#a9dec2'),
 'under-the-thumb':('#2e241a','#514432','#efd08d','#c3b4f5','#8eddd1'),
 'flood-myths':('#102e3c','#235061','#7bdbf4','#a2baff','#ffe2a3'),
 'fire-fission-reflection':('#251b38','#443057','#c6a3ff','#ffb167','#91e2e6'),
 'connection-installation':('#1d2c31','#35494d','#a5dcd9','#f2b895','#d2b5ff'),
 'slug-board-reflection':('#2b2025','#4d373f','#f4a8b8','#89d4e9','#f8d599'),
 'nilm-labels':('#182d28','#314e3e','#a9e3a0','#ffc27d','#87d3eb'),
 'anylog-field-notes':('#212338','#3c4156','#b1c2fa','#7be0c6','#f2cb87'),
}


# Archive additions: each diagram represents its own project, not measured output.
PROJECT_IDS=set(list(PALETTES)[:13])
SCENES['concurrent-http']=(rect(75,80,85,70)+text(117,119,'HTTP')+rect(220,35,65,160)+text(252,58,'QUEUE',9)+line('M160 115 H220')+''.join(rect(375,35+i*60,130,40)+text(440,60+i*60,'WORKER '+str(i+1),10)+line(f'M285 115 H325 V{55+i*60} H375') for i in range(3))+travel('M160 115 H325 V55 H375',4.1))
SCENES['concurrency-primitives']=(rect(130,85,300,65)+''.join(rect(142+i*47,97,33,40,animate('opacity','.15;1;.15',3.2+i*.37)) for i in range(6))+line('M80 118 H130 M430 118 H515 M270 70 V45 H345')+circle(345,45,12,animate('r','8;14;8',4.8))+text(300,201,'WAIT · LOCK · SIGNAL',12))
SCENES['file-io']=(rect(100,40,155,145)+text(177,72,'STDIN',13)+line('M123 97 H220 M123 119 H195 M123 142 H210')+line('M255 112 H350')+travel('M260 112 H347',3.7)+line('M350 55 H453 L490 92 V183 H350 Z M453 55 V92 H490')+text(420,140,'FILE',17))
SCENES['pacman-search']=(line('M300 38 L185 100 M300 38 L415 100 M185 100 L125 174 M185 100 L245 174 M415 100 L355 174 M415 100 L475 174')+''.join(circle(x,y,15,animate('opacity','.3;1;.3',4+i*.31)) for i,(x,y) in enumerate([(300,38),(185,100),(415,100),(125,174),(245,174),(355,174),(475,174)]))+text(300,220,'EXPAND · EVALUATE · CHOOSE',11))
SCENES['pacman-learning']=( ''.join(rect(165+c*50,25+r*46,42,38,animate('fill-opacity','.05;.5;.05',4+r*.51+c*.23),fill='currentColor') for r in range(4) for c in range(5))+travel('M185 182 V90 H285 V44 H385',8.3)+text(300,228,'REWARD → VALUE → POLICY',11))
SCENES['pacman-capture']=(rect(105,28,390,170)+line('M300 28 V198',stroke_dasharray='5 8')+line('M160 60 V112 M160 62 H196 L185 78 H160 M440 120 V173 M440 122 H406 L417 138 H440')+circle(210,155,10,animate('cx','210;345;210',6.7),fill='currentColor')+circle(390,73,10,animate('cy','73;163;73',5.3),fill='currentColor')+text(300,225,'COORDINATE · COLLECT · DEFEND',11))
SCENES['avl-wordrange']=(line('M300 45 L205 105 M300 45 L395 105 M205 105 L150 167 M205 105 L255 167 M395 105 L350 167 M395 105 L450 167')+''.join(circle(x,y,20)+text(x,y+4,label,11) for x,y,label in [(300,45,'7'),(205,105,'3'),(395,105,'3'),(150,167,'1'),(255,167,'1'),(350,167,'1'),(450,167,'1')])+line('M125 198 H475',animate('stroke-dashoffset','0;-350',7.1),stroke_dasharray='30 15')+text(300,230,'BALANCE + SUBTREE SIZE',11))
SCENES['six-degrees']=(line('M95 125 L225 60 L370 160 L505 80 M225 60 L315 30 M370 160 L260 200')+''.join(circle(x,y,18)+text(x,y+4,l,10) for x,y,l in [(95,125,'A'),(225,60,'B'),(370,160,'C'),(505,80,'D')])+travel('M95 125 L225 60 L370 160 L505 80',6.2)+text(300,229,'EVERY EDGE HAS A FILM',11))
SCENES['algorithms-lab']=( ''.join(rect(95+i*75,42,55,42)+text(122+i*75,68,str(i+1),12) for i in range(5))+line('M150 63 H170 M225 63 H245 M300 63 H320 M375 63 H395')+''.join(rect(230,110+i*26,140,19,animate('opacity','.2;1;.2',2.5+i*.43)) for i in range(4))+text(300,231,'LINK · TRAVERSE · BACKTRACK',11))
SCENES['mininet-network']=(rect(205,82,75,60)+rect(340,82,75,60)+line('M280 112 H340 M140 48 L205 97 M140 181 L205 128 M415 97 L480 48 M415 128 L480 181')+''.join(rect(x-28,y-18,56,36) for x,y in [(120,42),(120,187),(500,42),(500,187)])+travel('M140 48 L240 112 H380 L480 181',5.6)+text(300,224,'VIRTUAL LINKS · REAL COMMANDS',10))
SCENES['saaf']=(rect(125,28,135,178)+text(192,59,'CHORE',12)+''.join(rect(142,79+i*36,15,15)+line(f'M170 {87+i*36} H240') for i in range(3))+circle(394,106,49)+line('M394 106 V72 M394 106 L421 120')+circle(394,106,5,animate('r','3;8;3',3.9),fill='currentColor')+text(394,185,'REMIND',11))
SCENES['stanchat']=(rect(110,22,145,190)+rect(345,22,145,190)+rect(125,52,95,35,animate('y','52;65;52',5.4))+rect(145,114,95,35)+rect(360,90,95,35,animate('y','90;104;90',4.6))+line('M255 106 H345')+travel('M260 106 H340',2.9)+text(300,233,'WRITE · SYNC · READ',10))
SCENES['voice-recorder']=(rect(90,25,420,178)+''.join(line(f'M{120+i*18} 112 v{(-1 if i%2 else 1)*(15+(i*17)%55)}',animate('transform','translate(0 -8);translate(0 8);translate(0 -8)',1.1+i*.07)) for i in range(21))+circle(300,178,12,animate('fill-opacity','.2;1;.2',3.1),fill='currentColor')+text(300,227,'AUDIO · PLAYBACK · PERSISTENCE',10))
SCENES['ttl-computer']=(rect(105,44,90,55)+text(150,77,'ALU')+rect(255,44,90,55)+text(300,77,'REG')+rect(405,44,90,55)+text(450,77,'RAM')+line('M150 99 V140 H450 V99 M300 99 V140 M300 140 V175')+rect(225,175,150,32)+text(300,196,'CONTROL',10)+travel('M150 140 H450',6.4)+text(300,233,'A DATAPATH YOU CAN SEE',10))
SCENES['spotify-analyzer']=( ''.join(rect(110+i*33,150-(i*19)%80,21,30+(i*19)%80,animate('height',f'{30+(i*19)%80};20;{30+(i*19)%80}',3+i*.29),fill='currentColor',fill_opacity='.2') for i in range(6))+line('M350 180 V40 M350 180 H510 M370 155 L490 65')+''.join(circle(x,y,4,fill='currentColor') for x,y in [(375,143),(405,130),(420,93),(450,110),(475,69)])+text(300,225,'PLAYLIST → FEATURES → QUESTION',10))
SCENES['market-forecasting']=(line('M90 180 H515 M90 180 V40 M100 130 L140 148 L175 80 L215 110 L260 70 L300 122 L345 60 L380 105 L425 50 L470 90 L510 65',animate('stroke-dashoffset','580;0;580',12.7),stroke_dasharray='580')+line('M345 30 V190',stroke_dasharray='5 6')+text(220,218,'TRAIN',11)+text(430,218,'FUTURE',11))
SCENES['circuit-labs']=(line('M90 120 H165 L175 100 L190 140 L205 100 L220 140 L230 120 H290 M290 85 V155 M305 85 V155 M305 120 H370')+line('M390 130 C410 38 450 215 470 120 S510 40 530 120',animate('stroke-dashoffset','210;0',4.4),stroke_dasharray='190 20')+text(185,192,'R',17)+text(298,192,'C',17)+text(460,204,'RESPONSE',10))
SCENES['expression-art']=(text(300,42,'×',24)+text(190,112,'AVG',16)+text(410,112,'SIN',16)+line('M290 53 L195 90 M310 53 L405 90 M180 123 L135 174 M200 123 L245 174 M410 123 L440 174')+text(135,192,'x',20)+text(245,192,'y',20)+text(440,192,'x · y',18)+circle(300,35,25,animate('r','22;29;22',5.9))+text(300,231,'EXPRESSIONS BECOME STRUCTURE',10))
SCENES['ml-foundations']=( ''.join(rect(80,44+i*42,75,28) for i in range(4))+line('M155 120 H235 M360 120 H440')+''.join(circle(x,y,9)+line(f'M{x+9} {y} L{330 if x==255 else 440} 120') for x in [255,330] for y in [55,120,185])+rect(440,83,85,74)+text(482,123,'LOSS',14)+travel('M155 120 H440',4.9)+text(300,231,'DATA SHAPES → MODEL → VALIDATION',10))
NEW_COLORS={
 'concurrent-http':('#172333','#2b4960','#7ce5de','#ffc484','#d9b5ff'),
 'concurrency-primitives':('#271d35','#493052','#d4a3ff','#9ce7be','#ffd58d'),
 'file-io':('#222d28','#3a5043','#c8e691','#89d7ec','#ffc2aa'),
 'pacman-search':('#2a2318','#4c402b','#ffe18a','#d0b0ff','#85dfe4'),
 'pacman-learning':('#142d34','#29505b','#8ce7d9','#edb4ff','#ffcc88'),
 'pacman-capture':('#292036','#4d355b','#d5adff','#7ddfe6','#ffb79a'),
 'avl-wordrange':('#182d22','#30513d','#a3e9a7','#ffd39e','#9ecaff'),
 'six-degrees':('#302226','#51333c','#ffb7ad','#91dae7','#e1bcff'),
 'algorithms-lab':('#20243a','#3c4364','#a9c4ff','#f5bb94','#9bdfcb'),
 'mininet-network':('#142c2c','#2b494d','#7de2cf','#e4c4ff','#f1d18e'),
 'saaf':('#2e2131','#53384d','#ecb5dc','#9edfd1','#ffd59e'),
 'stanchat':('#172938','#2e4c65','#9bdcff','#ffa7ca','#c4e99a'),
 'voice-recorder':('#2c1929','#503047','#ff9cc8','#c5b5ff','#7fe0d7'),
 'ttl-computer':('#2a281a','#4c492e','#ebd894','#a5e5ba','#a4c6ff'),
 'spotify-analyzer':('#152d25','#2d4d3d','#a0efae','#dcb4ff','#ffc397'),
 'market-forecasting':('#182a31','#304958','#86d7e8','#ffc98e','#c6b9ff'),
 'circuit-labs':('#2c201d','#513c32','#ffc08c','#88e0d6','#c3b7ff'),
 'expression-art':('#261f36','#483754','#d9b2ff','#ffca9a','#99e4cc'),
 'ml-foundations':('#282039','#47345d','#c4b2ff','#8ee8cf','#ffb79b'),
}
PALETTES.update(NEW_COLORS)
PROJECT_IDS.update(NEW_COLORS)


from motion_refinements import refine
SCENES = refine(SCENES)
PALETTES["tpm-integrity-monitor"]=("#102b31","#183a42","#71d8d0","#a9b8ff","#ffd58a")
PROJECT_IDS.add("tpm-integrity-monitor")

def illustration(identity, static=False):
    """Color, lighting and eased motion reinforce each subject's composition."""
    import re, hashlib, xml.etree.ElementTree as ET
    bg,depth,a,b,c=PALETTES[identity]
    token='visual-'+identity
    root=ET.fromstring('<g>'+SCENES[identity]+'</g>')
    # Color communicates roles: structures, connectors, moving events.
    for element in root.iter():
        tag=element.tag
        if tag in ['path','rect','circle','ellipse']:
            role=element.attrib.pop('data-role', '')
            fill=element.get('fill')
            structural=tag=='rect' or fill=='var(--visual-bg)'
            event=tag=='circle' and fill=='currentColor'
            color=(b if role=='particle-1' else a) if role else (a if structural else c if event else b)
            element.set('stroke',color)
            element.set('stroke-width',element.get('stroke-width','1.5' if structural else '1.7'))
            if structural:
                element.set('fill',f'url(#{token}-surface)')
                element.set('rx',element.get('rx','7'))
                element.set('stroke-opacity',element.get('stroke-opacity','.65'))
            elif fill=='currentColor':
                element.set('fill',color)
                if event:element.set('filter',f'url(#{token}-glow)')
            elif tag=='path' and element.get('d','').rstrip().endswith('Z'):
                element.set('fill',a);element.set('fill-opacity','.12')
            if element.get('marker-end')=='url(#ARROW)':element.set('marker-end',f'url(#{token}-arrow)')
        elif tag=='text':
            element.set('fill','#edf3f7');element.set('letter-spacing','.5')
            element.set('font-family','ui-monospace, SFMono-Regular, Consolas, monospace')
            element.set('font-weight','500')
        elif tag in ['animate','animateTransform'] and element.get('values') and not element.get('calcMode'):
            values=element.get('values').split(';');count=len(values)
            element.set('calcMode','spline')
            element.set('keyTimes',';'.join(str(round(i/(count-1),5)) for i in range(count)))
            element.set('keySplines',';'.join(['.4 0 .2 1']*(count-1)))
    seed=int(hashlib.sha256(identity.encode()).hexdigest()[:8],16)
    x1=80+seed%120;x2=410+seed%90;y1=35+seed%60;y2=115+seed%70
    defs=f'''<defs>
      <marker id="{token}-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L5 3 L0 6" fill="none" stroke="{b}" stroke-width="1"/></marker>
      <linearGradient id="{token}-backdrop" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{depth}"/><stop offset="1" stop-color="{bg}"/></linearGradient>
      <linearGradient id="{token}-surface" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{depth}"/><stop offset="1" stop-color="{bg}"/></linearGradient>
      <filter id="{token}-ambient" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="28"/></filter>
      <filter id="{token}-glow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur in="SourceGraphic" stdDeviation="1.3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>'''
    # Quiet, static atmosphere keeps attention on the subject's motion.
    ambience=f'<g filter="url(#{token}-ambient)" stroke="none" opacity=".08"><ellipse cx="130" cy="65" rx="130" ry="75" fill="{a}"/><ellipse cx="470" cy="170" rx="120" ry="65" fill="{b}"/></g>'
    frame=f'<path d="M30 45 V25 H50 M550 25 H570 V45 M570 195 V215 H550 M50 215 H30 V195" fill="none" stroke="{a}" stroke-opacity=".1" stroke-width="1"/>'
    content=ET.tostring(root,encoding='unicode')
    backdrop='' if identity in PROJECT_IDS else f'<rect width="600" height="240" fill="url(#{token}-backdrop)" stroke="none"/>'
    shapes=defs+backdrop+ambience+frame+content
    if static:
        shapes=re.sub(r'<animate(?:Motion|Transform)?\b[^>]*/>','',shapes)
    return f'<svg class="topic-visual" data-visual="{identity}" viewBox="0 0 600 240" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shapes}</svg>'

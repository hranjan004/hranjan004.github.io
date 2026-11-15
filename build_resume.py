"""Generate the one-page combined resume. Requires reportlab."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--font-dir',type=Path,required=True,help='Directory containing Carlito TTF files')
args=parser.parse_args()
for name in ['Regular','Bold','Italic','BoldItalic']:
    pdfmetrics.registerFont(TTFont('Carlito-'+name,str(args.font_dir/('Carlito-'+name+'.ttf'))))
pdfmetrics.registerFontFamily('Carlito',normal='Carlito-Regular',bold='Carlito-Bold',italic='Carlito-Italic',boldItalic='Carlito-BoldItalic')
pdfmetrics.registerFontFamily('Carlito-Regular',normal='Carlito-Regular',bold='Carlito-Bold',italic='Carlito-Italic',boldItalic='Carlito-BoldItalic')
R=Path(__file__).resolve().parent
styles={
 'body':ParagraphStyle('body',fontName='Carlito-Regular',fontSize=10.5,leading=12),
 'small':ParagraphStyle('small',fontName='Carlito-Regular',fontSize=10,leading=11.5),
 'title':ParagraphStyle('title',fontName='Carlito-Bold',fontSize=21,leading=24,alignment=TA_CENTER),
 'contact':ParagraphStyle('contact',fontName='Carlito-Regular',fontSize=9.4,leading=12,alignment=TA_CENTER),
 'skill':ParagraphStyle('skill',fontName='Carlito-Regular',fontSize=10.5,leading=13.5),
 'section':ParagraphStyle('section',fontName='Carlito-Bold',fontSize=10,leading=12,spaceBefore=6),
 'bullet':ParagraphStyle('bullet',fontName='Carlito-Regular',fontSize=10.5,leading=12,leftIndent=9,firstLineIndent=-7,spaceAfter=1.2),
}
story=[]
def p(s,k='body'):return Paragraph(s,styles[k])
def add(s,k='body'):story.append(p(s,k))
def sec(s):
 add(s.upper(),'section');story.append(HRFlowable(width='100%',thickness=.45,color='#777777',spaceAfter=4))
def row(left,right,italic=False):
 t=Table([[p(left),p(right)]],colWidths=[397,139]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1),('ALIGN',(1,0),(1,0),'RIGHT')]))
 # Paragraph alignment is separate from cell alignment.
 t._cellvalues[0][1]=Paragraph(right,ParagraphStyle('right',parent=styles['body'],alignment=2));story.append(t)
def bullet(s):add('• '+s,'bullet')
def role(org,date,title,lines):
 if org in ['Tesphase', 'Balat Enterprises', 'Vyavshay Technologies']:
  row('<b>'+org+'</b> | <i>'+title+'</i>',date)
 else:
  row('<b>'+org+'</b>',date);add('<i>'+title+'</i>')
 for s in lines:bullet(s)
 story.append(Spacer(1,1))
def proj(title,tools,lines):
 add('<b>'+title+'</b>');add(tools,'small')
 for s in lines:bullet(s)
 story.append(Spacer(1,1))
add('Harsh Ranjan','title')
add('Bay Area, CA | (408) 806-5200 | <link href="mailto:ranjan.harsh22@hotmail.com">ranjan.harsh22@hotmail.com</link> | <link href="https://www.linkedin.com/in/harsh-ranjan">LinkedIn</link> | <link href="https://hranjan004.github.io/">hranjan004.github.io</link>','contact')
sec('Education')
row('<b>University of California, Santa Cruz</b>','Sep 2022 - Dec 2026')
add('<i>B.S. Computer Engineering, Computer Systems Track</i>')
row('<b>UC San Diego - Summer Session</b> | Computer Architecture with Lab','Summer 2025')
sec('Experience')
role('Renewable Resilient Energy Systems Lab, UCSC','Sep 2026 - Present','Research Intern - Electrical Anomaly Detection System (EADS) | <link href="https://hranjan004.github.io/writing/anylog-field-notes.html" color="#24486b">Technical notes</link>',[
'Built <b>AnyLog / EdgeLake</b> Pi infrastructure; helped optimize anomaly detection for a <b>512 MB RAM budget</b> on Pi 3.'])
role('UC Santa Cruz - Economics &amp; Applied Mathematics','Fall 2025 - Present','Tutor and Reader',[
'Led <b>AM 11A groups of 10</b>; graded AM 10, AM 20 and STATS 5, explaining quantitative methods and feedback.'])
role('Tesphase','Apr 2025 - Sep 2025','Chief Technology Officer | <link href="https://hranjan004.github.io/projects/tesphase.html" color="#24486b">Project</link>',[
'<b>SC Launchpad 2025 winner.</b> Owned the <b>React Native / Node.js / Supabase</b> roadmap and architecture.',
'Ran <b>30+ NSF I-Corps interviews</b> to shape a solar product; shipped authentication, real-time sync and notifications.'])
role('Balat Enterprises','Jun 2024 - Sep 2024','Product Management Intern',[
'Turned customer feedback into <b>React / Firebase</b> specs: <b>40% fewer post-release bugs</b>; built <b>Python / JavaScript</b> lead tooling and redesigned a service tool, contributing to <b>30% higher retention</b>.'])
role('Vyavshay Technologies','Jul 2022 - Aug 2022','Marketing Intern',[
'Integrated a <b>phone API in JavaScript</b> for an internal customer-service tool; market research and campaign analysis for a rural mobility app contributed to <b>15% higher retention</b>.'])
sec('Projects')
proj('<link href="https://hranjan004.github.io/projects/silicon-performance-lab.html" color="#24486b">Silicon Performance Lab</link> - FPGA Graphics &amp; Hardware Validation | <link href="https://github.com/hranjan004/silicon-performance-lab" color="#24486b">GitHub</link>',
'Verilog, C++17, Python, iCEBreaker UP5K, Yosys, nextpnr, Icarus Verilog',[
'Increased throughput <b>11.2x to 702 jobs/s</b> with an asynchronous C++ runtime; validated <b>12,000 hardware jobs</b>.',
'Scaled compute to <b>8 lanes at 30 MHz</b>; cut dot-product execution from <b>259 to 35 cycles</b>. Validated DVI rasterizer output across <b>2,113 hardware transactions</b> and <b>420,000 simulated pixel periods</b>.'])
proj('<link href="https://hranjan004.github.io/projects/microgrid-manager.html" color="#24486b">Microgrid Manager</link> - Distributed Systems &amp; Edge ML | <link href="https://github.com/hranjan004/iems-pi-edge" color="#24486b">GitHub</link> | <link href="https://lfedge.org/how-uc-santa-cruz-students-are-using-edgelake-and-ai-to-build-a-smarter-self-sufficient-home/" color="#24486b">LF Edge blog</link>',
'Python, PyTorch, BiLSTM, ONNX, Kafka, MQTT, AnyLog / EdgeLake, PostgreSQL, Docker',[
'As lead engineer, designed and trained <b>3 two-layer BiLSTMs</b> with per-appliance heads and weighted loss; achieved <b>0.932 heat-pump F1</b> on held-out physics-labeled data.',
'Engineered the ONNX deployment and telemetry pipeline: <b>~960 messages/min across 3 nodes</b> and <b>single-digit-ms inference per panel</b>.',
'<b>GX10 - hack.dev UCSC AI hackathon</b> (<link href="https://github.com/hranjan004/iems-pi-edge" color="#24486b">GitHub</link>): built local Nemotron inference and forecasting on <b>NVIDIA GB10</b>; <b>91.91% held-out teacher agreement</b>.'])
proj('<link href="https://hranjan004.github.io/projects/esp32-microgrid-meter.html" color="#24486b">ESP32 Microgrid Meter</link> - Embedded Firmware &amp; Sampling Performance',
'ESP-IDF C, ESP32-C3, ADC / DMA, Raspberry Pi; MQTT / Home Assistant integration design',[
'Sustained <b>3,846 samples/s per channel</b> with zero drops in a <b>2-second ADC benchmark</b>; fixed-point processing ran <b>17.5x faster</b> than software float.'])
proj('<link href="https://hranjan004.github.io/projects/gpt2-performance.html" color="#24486b">GPT-2 CPU Performance Optimization</link>',
'C, Linux perf, AVX2 SIMD, Cache Tiling, POSIX Threads',[
'Reduced hot-kernel <b>L1 data-cache misses from 9.17% to 2-3%</b> through cache tiling and AVX2 vectorization; processed <b>8 floats per SIMD instruction</b> to improve matrix-multiplication efficiency.'])
sec('Technical Skills')
add('<b>Languages:</b> C, C++, Python, Rust, JavaScript, SQL, Verilog, SystemVerilog, Bash','skill')
add('<b>Devices &amp; Interfaces:</b> ESP32, Raspberry Pi, ESP-IDF, ADC / DMA, UART, SPI, I2C','skill')
add('<b>Design &amp; Validation:</b> FPGA, RTL, Yosys, Vivado, Timing Analysis, Fault Injection, Oscilloscope','skill')
add('<b>Systems &amp; Applications:</b> Linux, Docker, Git, pthreads, Kafka, MQTT, PostgreSQL, AnyLog, React, Node.js, FastAPI','skill')
add('<b>ML &amp; Performance:</b> PyTorch, BiLSTM, ONNX, CUDA, LoRA, AVX2 SIMD, Linux perf, Cache Tiling','skill')
add('<b>Product &amp; Communication:</b> Customer Discovery, Market Research, Campaign Analysis, Product Specs, Technical Writing','skill')
SimpleDocTemplate(str(R/'Harsh_Ranjan_Resume.pdf'),pagesize=(612,792),leftMargin=38,rightMargin=38,topMargin=27,bottomMargin=27,title='Harsh Ranjan - Computer Engineering',author='Harsh Ranjan').build(story)

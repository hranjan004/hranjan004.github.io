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
sec('Projects')
proj('<link href="https://hranjan004.github.io/projects/silicon-performance-lab.html" color="#24486b">Silicon Performance Lab</link> - FPGA Graphics &amp; Hardware Validation | <link href="https://github.com/hranjan004/silicon-performance-lab" color="#24486b">GitHub</link>',
'Verilog, C++17, Python, iCEBreaker UP5K, Yosys, nextpnr, Icarus Verilog',[
'Increased throughput <b>11.2x to 702 jobs/s</b> by building an asynchronous C++ runtime; validated <b>12,000 FPGA jobs</b>.',
'Engineered an <b>8-lane, 30 MHz</b> datapath, cutting dot-product execution from <b>259 to 35 cycles</b>; built a DVI rasterizer and verified <b>420,000 simulated pixel periods</b>.'])
proj('<link href="https://hranjan004.github.io/projects/microgrid-manager.html" color="#24486b">Microgrid Manager</link> - Distributed Systems &amp; Edge ML | <link href="https://github.com/hranjan004/iems-pi-edge" color="#24486b">GitHub</link> | <link href="https://lfedge.org/how-uc-santa-cruz-students-are-using-edgelake-and-ai-to-build-a-smarter-self-sufficient-home/" color="#24486b">LF Edge blog</link>',
'Python, PyTorch, BiLSTM, ONNX, Kafka, MQTT, AnyLog / EdgeLake, PostgreSQL, Docker',[
'Designed and trained <b>3 two-layer BiLSTMs</b> as lead engineer, using appliance-specific heads and weighted loss; achieved <b>0.932 heat-pump F1</b> on held-out physics-labeled data.',
'Delivered <b>single-digit-ms ONNX inference per panel</b> on a distributed telemetry pipeline handling <b>~960 messages/min across 3 nodes</b>.',
'<b>GX10 - hack.dev UCSC AI hackathon</b> (<link href="https://github.com/hranjan004/iems-pi-edge" color="#24486b">GitHub</link>): deployed local Nemotron inference and forecasting on <b>NVIDIA GB10</b>, reaching <b>91.91% held-out teacher agreement</b>.'])
proj('<link href="https://hranjan004.github.io/projects/gpt2-performance.html" color="#24486b">GPT-2 CPU Performance Optimization</link>',
'C, Linux perf, AVX2 SIMD, Cache Tiling, POSIX Threads',[
'Cut the <b>L1 data-cache miss rate from 9.17% to 2-3%</b> in GPT-2 matrix-multiplication kernels using <b>Linux perf</b> profiling, cache tiling and <b>AVX2 SIMD</b>.'])
proj('<link href="https://hranjan004.github.io/projects/esp32-microgrid-meter.html" color="#24486b">ESP32 Microgrid Meter</link> - Embedded Firmware &amp; Sampling Performance',
'ESP-IDF C, ESP32-C3, ADC / DMA, Raspberry Pi; MQTT / Home Assistant integration design',[
'Accelerated processing <b>17.5x</b> with fixed-point arithmetic versus software float; sustained <b>3,846 samples/s per channel</b> with <b>zero drops</b> in a <b>2-second ADC benchmark</b>.'])
sec('Experience')
role('Renewable Resilient Energy Systems Lab, UCSC','Sep 2026 - Present','Research Intern - Electrical Anomaly Detection System (EADS) | <link href="https://hranjan004.github.io/writing/anylog-field-notes.html" color="#24486b">Technical notes</link>',[
'Connected Pi nodes with <b>AnyLog / EdgeLake</b>; co-optimized anomaly detection for a <b>512 MB memory budget</b>.'])
role('UC Santa Cruz - Economics &amp; Applied Mathematics','Fall 2025 - Present','Tutor and Reader',[
'Taught quantitative methods in <b>10-student AM 11A sessions</b>; assessed AM 10, AM 20 and STATS 5 coursework.'])
role('Tesphase','Apr 2025 - Sep 2025','Chief Technology Officer | <link href="https://hranjan004.github.io/projects/tesphase.html" color="#24486b">Project</link>',[
'Led architecture and delivery of a <b>React Native / Node.js / Supabase</b> solar app; <b>SC Launchpad 2025 winner</b>.',
'Turned <b>30+ customer interviews (NSF I-Corps)</b> into shipped authentication, real-time sync and push notifications.'])
role('Balat Enterprises','Jun 2024 - Sep 2024','Product Management Intern',[
'Cut post-release bugs <b>40%</b> by translating customer feedback into <b>React / Firebase</b> product specifications.',
'Built <b>Python / JavaScript</b> lead tools and redesigned a customer-service tool, contributing to <b>30% higher retention</b>.'])
role('Vyavshay Technologies','Jul 2022 - Aug 2022','Marketing Intern',[
'Integrated a phone API into a <b>JavaScript</b> customer-service tool; market research and campaign analysis for a rural mobility app supported <b>15% higher retention</b>.'])
sec('Technical Skills')
add('<b>Languages:</b> C, C++, Python, Rust, JavaScript, SQL, Verilog, SystemVerilog, Bash','skill')
add('<b>Devices &amp; Interfaces:</b> ESP32, Raspberry Pi, ESP-IDF, ADC / DMA, UART, SPI, I2C','skill')
add('<b>Design &amp; Validation:</b> FPGA, RTL Design, Yosys, Vivado, Timing Analysis, Fault Injection, Oscilloscope','skill')
add('<b>Systems &amp; Applications:</b> Linux, Docker, Git, pthreads, Kafka, MQTT, PostgreSQL, AnyLog, React, Node.js, FastAPI','skill')
add('<b>ML &amp; Performance:</b> PyTorch, BiLSTM, ONNX, CUDA, LoRA, AVX2 SIMD, Linux perf, Cache Tiling','skill')
add('<b>Product &amp; Communication:</b> Customer Discovery, Market Research, Campaign Analysis, Product Specs, Technical Writing','skill')
SimpleDocTemplate(str(R/'Harsh_Ranjan_Resume.pdf'),pagesize=(612,792),leftMargin=38,rightMargin=38,topMargin=27,bottomMargin=27,title='Harsh Ranjan - Computer Engineering',author='Harsh Ranjan').build(story)

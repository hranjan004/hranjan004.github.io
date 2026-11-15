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
 row('<b>'+org+'</b>',date);add('<i>'+title+'</i>')
 for s in lines:bullet(s)
 story.append(Spacer(1,2))
def proj(title,tools,lines):
 add('<b>'+title+'</b>');add(tools,'small')
 for s in lines:bullet(s)
 story.append(Spacer(1,2))
add('Harsh Ranjan','title')
add('Bay Area, CA | (408) 806-5200 | <link href="mailto:ranjan.harsh22@hotmail.com">ranjan.harsh22@hotmail.com</link> | <link href="https://www.linkedin.com/in/harsh-ranjan">LinkedIn</link> | <link href="https://hranjan004.github.io/">hranjan004.github.io</link>','contact')
sec('Education')
row('<b>University of California, Santa Cruz</b>','Sep 2022 - Dec 2026')
add('<i>B.S. Computer Engineering, Computer Systems Track</i>')
add('<b>Coursework:</b> Computer Architecture, Embedded Systems, Operating Systems, Logic Design, Machine Learning','small')
row('<b>UC San Diego - Summer Session</b> | Computer Architecture with Lab','Summer 2025')
sec('Experience')
role('Renewable Resilient Energy Systems Lab, UCSC','Sep 2026 - Present','Research Intern - Electrical Anomaly Detection System (EADS) | <link href="https://hranjan004.github.io/writing/anylog-field-notes.html" color="#24486b">Technical notes</link>',[
'Built <b>AnyLog / EdgeLake</b> infrastructure for distributed Raspberry Pi nodes; helped optimize anomaly detection for a <b>Pi 3 deployment with a 512 MB RAM budget</b>.',
'Debugged deployments with software and infrastructure teams under Dr. Pat Mantey; wrote technical field notes.'])
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
proj('<link href="https://hranjan004.github.io/projects/silicon-performance-lab.html" color="#24486b">Silicon Performance Lab</link> - FPGA Graphics &amp; Hardware Validation | <link href="https://github.com/hranjan004/silicon-performance-lab" color="#24486b">GitHub (private)</link>',
'Verilog, C++17, Python, iCEBreaker UP5K, Yosys, nextpnr, Icarus Verilog',[
'Performed hardware validation of <b>12,000 jobs at 702 jobs/s</b>; asynchronous execution improved throughput <b>11.2x</b>.',
'Designed RTL for a fixed-function rasterizer with DVI output; passed <b>2,113 hardware transactions</b> and simulated <b>420,000 pixel periods</b>. Selected <b>8 compute lanes at 30 MHz</b> after timing analysis.'])
proj('<link href="https://hranjan004.github.io/projects/microgrid-manager.html" color="#24486b">Microgrid Manager</link> - Distributed Systems | <link href="https://github.com/hranjan004/iems-pi-edge" color="#24486b">GitHub</link> | <link href="https://lfedge.org/how-uc-santa-cruz-students-are-using-edgelake-and-ai-to-build-a-smarter-self-sufficient-home/" color="#24486b">LF Edge blog</link>',
'Python, Kafka, MQTT, AnyLog / EdgeLake, PostgreSQL, PyTorch, ONNX, Docker',[
'As capstone lead engineer, led models, labeling and dashboard work with weekly sponsor reviews; streamed <b>~960 messages/min</b> across <b>3 nodes</b> and served ONNX inference in <b>single-digit ms per panel</b>.',
'<b>GX10 - hack.dev UCSC AI hackathon</b> (<link href="https://github.com/hranjan004/microgrid-iems-gx10" color="#24486b">private GitHub</link>): built local Nemotron inference and forecasting on <b>NVIDIA GB10</b>; <b>91.91% held-out teacher agreement</b>.'])
proj('<link href="https://hranjan004.github.io/projects/esp32-microgrid-meter.html" color="#24486b">ESP32 Microgrid Meter</link> - Firmware Benchmarks; Sensing Planned',
'ESP-IDF C, ESP32-C3, ADC, Direct Memory Access (DMA), LEDC, Raspberry Pi',[
'Benchmarked embedded C firmware at <b>3,846 samples/s per channel</b> with zero drops over <b>2 seconds</b>; fixed-point math was <b>17.5x faster</b> than software float. Loopback timing standard deviation: <b>0.49 µs</b>, Wi-Fi off.',
'Designed an isolated voltage-sensing front end and <b>1 Hz Pi telemetry</b>; sensors, calibration and Home Assistant MQTT integration remain planned.'])
sec('Technical Skills')
add('<b>Languages:</b> C, C++, Python, Rust, JavaScript, SQL, Verilog, SystemVerilog, Bash','skill')
add('<b>Hardware &amp; Firmware:</b> RTL Design, FPGA, ESP-IDF, ADC / DMA, UART, SPI, I2C','skill')
add('<b>Validation &amp; Debug:</b> Timing Analysis, Fault Injection, Yosys, nextpnr, Icarus Verilog, Oscilloscope','skill')
add('<b>Distributed Systems &amp; ML:</b> Linux, Docker, Git, Kafka, MQTT, PostgreSQL, PyTorch, ONNX','skill')
add('<b>Product:</b> Customer Discovery, Market Research, Product Requirements, Technical Writing','skill')
SimpleDocTemplate(str(R/'Harsh_Ranjan_Resume.pdf'),pagesize=(612,792),leftMargin=38,rightMargin=38,topMargin=27,bottomMargin=27,title='Harsh Ranjan - Computer Engineering',author='Harsh Ranjan').build(story)

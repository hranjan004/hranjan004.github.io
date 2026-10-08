"""Reading layouts, source-aware formatting, and code-native animated motifs."""
import html,re
E=html.escape

def motif(kind,question='',compact=False):
 shapes=''
 if kind=='atom':
  shapes='<g class="orbit-group"><ellipse cx="300" cy="85" rx="105" ry="37"/><ellipse cx="300" cy="85" rx="105" ry="37" transform="rotate(60 300 85)"/><ellipse cx="300" cy="85" rx="105" ry="37" transform="rotate(120 300 85)"/><circle class="dot-fill" cx="405" cy="85" r="5"/></g><circle class="pulse-core dot-fill" cx="300" cy="85" r="11"/>'
 elif kind=='waves':
  shapes=''.join(f'<path class="wave-line" style="--delay:{i*-1}s" d="M-100 {50+i*15} Q-25 {i*15} 50 {50+i*15} T200 {50+i*15} T350 {50+i*15} T500 {50+i*15} T650 {50+i*15} T800 {50+i*15}"/>' for i in range(5))
 elif kind=='balance':
  shapes='<path d="M300 35 V140 M250 140 H350"/><g class="balance-beam"><path d="M195 55 H405 M205 55 V104 M395 55 V104 M170 104 Q205 155 240 104 Z M360 104 Q395 155 430 104 Z"/><circle class="dot-fill" cx="300" cy="55" r="6"/></g>'
 elif kind=='institutions':
  shapes='<path d="M200 48 L300 14 L400 48 Z M192 140 H408 M180 150 H420"/>'+''.join(f'<rect class="column" style="--delay:{i*-.8}s" x="{210+i*42}" y="60" width="12" height="70"/>' for i in range(5))
 elif kind=='threads':
  shapes=''.join(f'<path class="thread-line" style="--delay:{i*-.4}s" d="M{150+i*20} 12 Q{380-i*8} 85 {150+i*20} 158"/>' for i in range(15))
 elif kind=='feedback':
  shapes='<path class="flow-line" d="M145 85 H455 M455 85 V140 H145 V85"/>'+''.join(f'<rect x="{145+i*95}" y="60" width="65" height="50" rx="7"/>' for i in range(4))+'<circle class="flow-dot dot-fill" cx="150" cy="85" r="5"/>'
 else:
  shapes='<path d="M175 45 L300 85 L425 40 M175 135 L300 85 L425 135 M175 45 L175 135 M425 40 V135"/>'+''.join(f'<circle class="pulse-node" style="--delay:{i*-.7}s" cx="{x}" cy="{y}" r="{r}"/>' for i,(x,y,r) in enumerate([(175,45,10),(300,85,18),(425,40,10),(175,135,10),(425,135,10)]))
 return f'<div class="essay-motif {kind} {"compact" if compact else ""}" aria-hidden="true"><svg viewBox="0 0 600 170" fill="none" stroke="currentColor" stroke-width="1.4">{shapes}</svg></div>'+('' if not question else f'<p class="essay-question"><span>THE QUESTION</span><em>{E(question)}</em></p>')

def rich(text):
 s=E(text)
 titles=['The Society of the Spectacle','Artificial Hells','Homeric Hymn to Demeter','The Epic of Gilgamesh','Epic of Creation','Metamorphoses','Give Me Liberty!','Fire and Fission','The Entrenchment of Democracy','Theogony','Cold Dark Matter','The Distance','Triple Point']
 for title in titles:s=s.replace(E(title),'<em>'+E(title)+'</em>')
 concepts=['physics-informed','walk-forward','backpressure','mutual obligation','accountability','counter-mobilization','counter-organization','participatory art','early integration','structured adaptability','integration checkpoints','surrogate gradients','finite state machine','configuration-time','cache coherency','thread safety','negative labels','constitutional friction','Party-State Separation Principle','Purposive Autonomy Principle']
 for term in concepts:s=re.sub(r'(?i)\b'+re.escape(term)+r'\b',lambda m:'<strong>'+m[0]+'</strong>',s,count=1)
 return s

def heading(text):
 if len(text)>120:return False
 return bool(re.match(r'^(Question\s+\d|Prompt\s+\d|Part (One|Two)|\d+[.)] [A-Z])',text) or text in ['Works Cited','Notes','References','Introduction','Conclusion','The Privacy Trap','Remote Collaboration Challenges','Consensus Without Integration','Technical and Personal Limitations','Lessons in Collaborative Software Development','Recommendations and Future Applications','Educational Assessment','Process Deterioration: From Scrum to Silos','China: Constitutional Façade and Party Supremacy','The United States: Constitutional Friction and Subordination','Experience, Uncertainty, and Interpretation','Defining Installation Through Experience','Comparing the Artists','Concluding Comparison'])

def prose(blocks,kind='network'):
 out=[]
 for i,b in enumerate(blocks):
  if heading(b):out.append(f'<h2 id="section-{i}" class="essay-subhead"><span class="question-mark" aria-hidden="true">◌</span>{rich(b)}</h2>')
  elif re.match(r'^(PROMETHEUS|OPPENHEIMER):',b):
   name,body=b.split(':',1);out.append('<p class="dialogue"><strong class="speaker">'+name+'</strong>'+rich(body)+'</p>')
  else:out.append('<p>'+rich(b)+'</p>')
 return ''.join(out)

def essay_card(w,prefix='writing/'):
 return f'''<a class="essay-card" href="{prefix}{w['id']}.html">{motif(w.get('motif','network'),compact=True)}<div class="essay-card-copy"><span class="eyebrow">{E(w['kind'])} · {E(w['date'])}</span><h3>{E(w['title'])}</h3><p>{E(w['summary'])}</p><span class="read-link">Read essay <span aria-hidden="true">↗</span></span></div></a>'''

def essay_body(w):
 toc=[(i,b) for i,b in enumerate(w['body']) if heading(b)]
 contents=''
 if len(toc)>1:contents='<details class="essay-contents"><summary>In this essay</summary><ul>'+''.join(f'<li><a href="#section-{i}">{E(b)}</a></li>' for i,b in toc)+'</ul></details>'
 mins=max(1,round(sum(len(b.split()) for b in w['body'])/220))
 return f'''<main class="wrap" id="main-content"><div class="page-hero essay-hero"><a class="breadcrumb" href="index.html">← All writing</a><span class="eyebrow">{E(w['kind'])} · {E(w['date'])} · {mins} min read</span><h1>{E(w['title'])}</h1><p class="lede essay-summary">{rich(w['summary'])}</p></div><div class="reader reading-main">{motif(w.get('motif','network'),w.get('question',''))}<div class="reading-note">{E(w['note'])}</div>{contents}<article class="essay-text">{prose(w['body'],w.get('motif','network'))}</article><div class="essay-source"><strong>Text source</strong><p>{E(w.get('source','Project and Writing Archive'))}</p></div><a class="back-link" href="index.html">← Explore more writing</a></div></main>'''

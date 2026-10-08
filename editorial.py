"""Reading layouts, source-aware formatting, and code-native animated motifs."""
import html,re
E=html.escape

from visuals import illustration

def motif(identity,question='',compact=False):
 return f'<div class="essay-motif {"compact" if compact else ""}">{illustration(identity,static=compact)}</div>'+('' if not question else f'<p class="essay-question"><span>THE QUESTION</span><em>{E(question)}</em></p>')

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

def prose(blocks):
 out=[]
 for i,b in enumerate(blocks):
  if heading(b):out.append(f'<h2 id="section-{i}" class="essay-subhead"><span class="question-mark" aria-hidden="true">◌</span>{rich(b)}</h2>')
  elif re.match(r'^(PROMETHEUS|OPPENHEIMER):',b):
   name,body=b.split(':',1);out.append('<p class="dialogue"><strong class="speaker">'+name+'</strong>'+rich(body)+'</p>')
  else:out.append('<p>'+rich(b)+'</p>')
 return ''.join(out)

def essay_card(w,prefix='writing/'):
 return f'''<a class="essay-card" href="{prefix}{w['id']}.html">{motif(w['id'],compact=True)}<div class="essay-card-copy"><span class="eyebrow">{E(w['kind'])} · {E(w['date'])}</span><h3>{E(w['title'])}</h3><p>{E(w['summary'])}</p><span class="read-link">Read essay <span aria-hidden="true">↗</span></span></div></a>'''

def essay_body(w):
 toc=[(i,b) for i,b in enumerate(w['body']) if heading(b)]
 contents=''
 if len(toc)>1:contents='<details class="essay-contents"><summary>In this essay</summary><ul>'+''.join(f'<li><a href="#section-{i}">{E(b)}</a></li>' for i,b in toc)+'</ul></details>'
 mins=max(1,round(sum(len(b.split()) for b in w['body'])/220))
 return f'''<main class="wrap" id="main-content"><div class="page-hero essay-hero"><a class="breadcrumb" href="index.html">← All writing</a><span class="eyebrow">{E(w['kind'])} · {E(w['date'])} · {mins} min read</span><h1>{E(w['title'])}</h1><p class="lede essay-summary">{rich(w['summary'])}</p></div><div class="reader reading-main">{motif(w['id'],w.get('question',''))}<div class="reading-note">{E(w['note'])}</div>{contents}<article class="essay-text">{prose(w['body'])}</article><div class="essay-source"><strong>Text source</strong><p>{E(w.get('source','Project and Writing Archive'))}</p></div><a class="back-link" href="index.html">← Explore more writing</a></div></main>'''

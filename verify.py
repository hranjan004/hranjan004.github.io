"""Verify generated pages, navigation, content coverage and unique illustrations.
Run after build.py: python3 verify.py [--base-url http://127.0.0.1:4174/]
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, re, xml.etree.ElementTree as ET
from visuals import SCENES, PALETTES, illustration

ROOT=Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links=[];self.ids=[];self.h1=0;self.main=0;self.images=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        self.h1+=tag=='h1';self.main+=tag=='main'
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='img':
            assert attrs.get('alt'), 'Missing image alternative text'
            self.images.append(attrs['src'])
        for key in ['src','href']:
            if key in attrs:self.links.append(attrs[key])


def verify(base_url=None):
    pages={f:Page(f.read_text()) for f in ROOT.rglob('*.html') if '.git' not in f.parts}
    resources=set(pages);graph={f:set() for f in pages};external=set()
    for file,page in pages.items():
        assert page.h1==1 and page.main==1, f'{file}: invalid main/heading count'
        assert len(page.ids)==len(set(page.ids)), f'{file}: duplicate ids'
        source=file.read_text()
        assert not re.search(r'claude\.ai/chat|/Users/|https?://(?:10\.|192\.168\.|127\.)',source),f'{file}: private reference'
        for link in page.links:
            url=urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme in ['http','https']:external.add(link)
                continue
            target=(file.parent/unquote(url.path)).resolve() if url.path else file
            assert target.exists(), f'{file}: missing {link}'
            resources.add(target)
            if target in pages:
                graph[file].add(target)
                assert not url.fragment or unquote(url.fragment) in pages[target].ids, f'{file}: missing anchor {link}'
    seen=set();queue=[ROOT/'index.html']
    while queue:
        f=queue.pop()
        if f not in seen:seen.add(f);queue.extend(graph[f]-seen)
    assert seen==set(pages), f'Unreachable pages: {set(pages)-seen}'
    projects=json.loads((ROOT/'content.json').read_text());essays=json.loads((ROOT/'writing.json').read_text());arts=json.loads((ROOT/'art-content.json').read_text())
    identities=[p['id'] for p in projects+essays]
    assert set(identities)==set(SCENES)==set(PALETTES)
    assert len(set(PALETTES.values()))==len(identities), 'Reused palette'
    assert len(set(SCENES.values()))==len(identities), 'Reused composition'
    motion_signatures=[]
    for identity in identities:
        svg=ET.fromstring(illustration(identity))
        ids={e.get('id') for e in svg.iter() if e.get('id')}
        for e in svg.iter():
            for value in e.attrib.values():
                for ref in re.findall(r'url\(#([^)]*)\)',value):assert ref in ids, f'{identity}: missing SVG definition {ref}'
        animations=[e for e in svg.iter() if e.tag.startswith('animate')]
        assert animations, f'{identity}: no motion'
        assert all(e.get('repeatCount')=='indefinite' for e in animations)
        motion_signatures.append(tuple(ET.tostring(e) for e in animations))
        assert not any(e.tag.startswith('animate') for e in ET.fromstring(illustration(identity,static=True)).iter())
    assert len(set(motion_signatures))==len(identities),'Reused animation sequence'
    archive=[]
    for identity,art in arts.items():
        page=pages[ROOT/'art'/f'{identity}.html']
        for im in art['images']:
            assert '../assets/'+im['src'] in page.images
            archive.append(ROOT/'assets'/im['src'])
    assert len(archive)==28
    assert len(set(hashlib.sha256(f.read_bytes()).hexdigest() for f in archive))==28
    assert all(p['status'] in ['Completed','Ongoing'] for p in projects)
    assert not any('intelligent energy management' in p['title'].lower() or 'application' in p['title'].lower() for p in essays)
    assert 'I build systems that work in the <em>real world.</em><br>And write about the world they work in.' in (ROOT/'index.html').read_text()
    if base_url:
        def get(file):
            url=urljoin(base_url,file.relative_to(ROOT).as_posix())
            with urlopen(url,timeout=15) as response:
                assert response.status==200,(url,response.status)
                assert response.read(),url
        with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,resources))
    result={'pages':len(pages),'linked_resources':len(resources),'projects':len(projects),'essays':len(essays),'unique_animated_illustrations':len(identities),'archive_images':len(archive),'external_links':sorted(external),'http_checked':bool(base_url)}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base-url');args=parser.parse_args();verify(args.base_url)

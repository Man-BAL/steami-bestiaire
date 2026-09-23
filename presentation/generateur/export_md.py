# Régénère l'export Markdown (Notion) à partir de la page produite par site.py
import re, html, os
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','bestiaire-steami-presentation.html')
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','bestiaire-steami-texte-notion.md')
src=open(F).read(); body=src[src.index('<body>'):]
body=re.sub(r'<svg.*?</svg>','',body,flags=re.S)
body=re.sub(r'<script.*?</script>','',body,flags=re.S)
body=re.sub(r'<nav>.*?</nav>','',body,flags=re.S)
body=re.sub(r'<a class="totop".*?</a>','',body,flags=re.S)
body=re.sub(r'<footer>.*?</footer>','',body,flags=re.S)
def T(x):
    x=re.sub(r'<br\s*/?>',' ',x)
    return html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',x))).strip()
def find(pat,s,flags=re.S):
    m=re.search(pat,s,flags); return T(m.group(1)) if m else ''
L=[]
for tag,attrs,sec in re.findall(r'<(header|section)([^>]*)>(.*?)</\1>',body,flags=re.S):
    kick=find(r'<p class="kicker[^"]*">(.*?)</p>',sec)
    if tag=='header':
        facts=re.search(r'<div class="facts">(.*?)</div>',sec,re.S)
        rep=' · '.join(T(x) for x in re.findall(r'<span>(.*?)</span>',facts.group(1))) if facts else ''
        L+=['# '+find(r'<h1>(.*?)</h1>',sec),'','*'+kick+'*','','**'+find(r'<p class="lede">(.*?)</p>',sec)+'**','',find(r'<p class="txt">(.*?)</p>',sec),'','Repères : '+rep,'']
        continue
    h2=find(r'<h2>(.*?)</h2>',sec)
    L+=['---','','## '+h2,'*'+kick+'*','']
    special=set()
    for blockpat in (r'<div class="gap"[^>]*>(.*?)</div>', r'<div class="ctile">(.*?)</div>', r'<div class="regard"[^>]*>(.*?)</div>',
                     r'<article class="crea">(.*?)</article>', r'<div class="ex3">(.*?)</div>\s*<div class="ex3"|<div class="ex3">(.*?)</div>\s*</div>'):
        for blk in re.findall(blockpat,sec,flags=re.S):
            blk=blk if isinstance(blk,str) else ' '.join(x for x in blk if x)
            special.update(T(x) for x in re.findall(r'<p[^>]*>(.*?)</p>',blk,flags=re.S))
    ex3s=re.search(r'<div class="ex3s">(.*?)</div>\s*<p class="teach2"',sec,flags=re.S)
    if ex3s: special.update(T(x) for x in re.findall(r'<p[^>]*>(.*?)</p>',ex3s.group(1),flags=re.S))
    intro=sec
    for cls in ('x-cards','cards','grid8','example','prog2','assembly','wpills','frise'):
        intro=re.sub(r'<(div|ol|figure)[^>]*class="[^"]*'+cls+r'[^"]*".*?</\1>','',intro,flags=re.S)
    for p in re.findall(r'<p(?: class="(?:lead-p|ctx-lead|trans|x-concl|teach2)")?>(.*?)</p>',intro,flags=re.S):
        txt=T(p)
        if txt and txt not in special and not txt.startswith('Repères'): L+=[txt,'']
    # sous-titres et contenus particuliers
    for sub in re.findall(r'<h3 class="sub c">(.*?)</h3>',sec,flags=re.S): L+=['### '+T(sub),'']
    # trois regards
    for h4,p in re.findall(r'<h4[^>]*>(.*?)</h4><p>(.*?)</p>',sec,flags=re.S):
        if 'regard' in h4.lower(): L+=['- **'+T(h4)+'** · '+T(p)]
    if any('regard' in x.lower() for x in L[-4:]): L+=['']
    # questions (cartes gap)
    gaps=[T(x) for x in re.findall(r'<div class="gap"[^>]*>.*?<p>(.*?)</p>',sec,flags=re.S)]
    if gaps: L+=['- '+g for g in gaps]+['']
    # contexte
    ctx=[T(x) for x in re.findall(r'<div class="ctile">.*?<p>(.*?)</p>',sec,flags=re.S)]
    if ctx: L+=['Contexte à noter : '+', '.join(ctx)+'.','']
    # étapes numérotées
    st=re.findall(r'<li><span class="sn8">(\d+)</span><p class="ph8">(.*?)</p><b>(.*?)</b><span class="sd8">(.*?)</span></li>',sec,flags=re.S)
    if st: L+=[f'{int(n)}. **{T(b)}** ({T(ph)}) — {T(d)}' for n,ph,b,d in st]+['']
    # exemples d'investigation
    for card in re.findall(r'<article class="xcard">(.*?)</article>',sec,flags=re.S):
        L+=['### '+find(r'<h[34] class="xq">(.*?)</h[34]>',card),'*'+find(r'<p class="xsub">(.*?)</p>',card)+'*','']
        for lab,b in re.findall(r'<li style="[^"]*"><b>(.*?)</b>(.*?)</li>',card,flags=re.S):
            chips=' · '.join(T(x) for x in re.findall(r'<span class="mchip"[^>]*>(.*?)</span>',b))
            txt=T(re.sub(r'<div class="chips">.*?</div>','',b,flags=re.S))
            L+=['- **'+T(lab)+'**'+(f' ({chips})' if chips else '')+' : '+txt]
        q=find(r'<p class="xquest"[^>]*><b>(?:.*?)</b>(.*?)</p>',card)
        if q: L+=['- **Question possible** : '+q]
        L+=['']
    # fiches animaux
    for card in re.findall(r'<article class="card"[^>]*>(.*?)</article>',sec,flags=re.S):
        L+=['### '+find(r'<h3>(.*?)</h3>',card)+' ('+find(r'<span class="per[^"]*">(.*?)</span>',card).lower()+')','',find(r'<p class="trait">(.*?)</p>',card),'']
        L+=['- **'+T(dt)+'** : '+T(dd) for dt,dd in re.findall(r'<dt>(.*?)</dt><dd[^>]*>(.*?)</dd>',card,flags=re.S)]+['']
    # exemple rainette
    ex=re.search(r'<div class="example">(.*?)</figure>|<div class="example">(.*)',sec,flags=re.S)
    if ex and 'class="example"' in sec:
        e=ex.group(1) or ex.group(2)
        L+=['**'+find(r'<h3 class="exq">(.*?)</h3>',e)+'**','']
        L+=['- **'+T(dt)+'** : '+T(dd) for dt,dd in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>',e,flags=re.S)]
        cap=find(r'<div class="hypo">.*?<p>(.*?)</p>',e)
        if cap: L+=['','*'+cap+'*']
        L+=['']
    # ExAO : trois temps
    for col in re.findall(r'<div class="ex3">(.*?)</div>',sec,flags=re.S):
        L+=['**'+find(r'<h4[^>]*>(.*?)</h4>',col)+'** : '+', '.join(T(x) for x in re.findall(r'<p>(.*?)</p>',col))]
    if '<div class="ex3s">' in sec: L+=['',find(r'<p class="teach2">(.*?)</p>',sec),'']
    # programme
    for pc in re.findall(r'<div class="pcard"[^>]*>(.*?)</div>',sec,flags=re.S):
        L+=['### '+find(r'<span>(.*?)</span>',pc),'']
        L+=['- '+T(x) for x in re.findall(r'<li>(.*?)</li>',pc,flags=re.S)]+['']
    # créativité
    for a2 in re.findall(r'<article class="crea">(.*?)</article>',sec,flags=re.S):
        L+=['- **'+find(r'<h3>(.*?)</h3>',a2)+'** : '+find(r'<p>(.*?)</p>',a2)]
    if '<article class="crea">' in sec: L+=['']
    # fabrication
    for t2,p2 in re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',sec,flags=re.S):
        L+=['### '+T(t2),'',T(p2),'']
    asm=[ (T(b),T(d)) for b,d in re.findall(r'<li><b>(.*?)</b>(.*?)</li>',sec,flags=re.S) if 'asm-side' in sec]
    if asm and 'asm-side' in sec:
        L+=['**Schéma d’assemblage**','']+[f'{i}. **{b}** {d}' for i,(b,d) in enumerate(asm,1)]+['',find(r'<figcaption>(.*?)</figcaption>',sec),'']
    # pilules (disciplines)
    wp=re.search(r'<div class="wpills">(.*?)</ul>',sec,flags=re.S)
    if wp: L+=['- '+T(x) for x in re.findall(r'<li>(.*?)</li>',wp.group(1),flags=re.S)]+['']
md=re.sub(r'\n{3,}','\n\n','\n'.join(L)).strip()+'\n'
open(OUT,'w').write(md)
print(OUT, len(md.split()),'mots')

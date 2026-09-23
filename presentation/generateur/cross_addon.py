import math
HUB=[('chouette','lum','Nuits éclairées'),('fennec','mic','Bruit'),('crocodile','hts','Chaleur'),('rainette','hts','Air sec ou humide'),
     ('abeille','lum','Fleurs et pollinisation'),('martinet','pres','Météo'),('tortue','mag','Pollution lumineuse'),('chauvesouris','dist','Tranquillité la nuit')]
def nested(k,x,y,s):
    return I[k].replace('<svg viewBox="0 0 200 200" role="img">',f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 200 200">',1)
def hub_svg():
    W=H=780; cx=cy=390; n=len(HUB); rin,rout,rmed,rlab=150,236,193,300; gap=2.2
    def pt(r,a): return (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    o=f'<circle cx="{cx}" cy="{cy}" r="{rout+14}" fill="#F6F7F9"/>'
    for i,(k,sk,lab) in enumerate(HUB):
        a0=-90-180/n+i*360/n+gap; a1=a0+360/n-2*gap
        p1,p2,p3,p4=pt(rout,a0),pt(rout,a1),pt(rin,a1),pt(rin,a0)
        o+=(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{rout} {rout} 0 0 1 {p2[0]:.1f} {p2[1]:.1f} L{p3[0]:.1f} {p3[1]:.1f} A{rin} {rin} 0 0 0 {p4[0]:.1f} {p4[1]:.1f} Z" '
            f'fill="{SENS[sk][1]}" stroke="{SENS[sk][0]}" stroke-width="2.5"/>')
    o+=f'<circle cx="{cx}" cy="{cy}" r="{rin-10}" fill="#1F2455"/><circle cx="{cx}" cy="{cy}" r="{rin-22}" fill="none" stroke="#F7D117" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>'
    lines=('Ce que le vivant','nous apprend','sur nos','conditions de vie')
    for i,l in enumerate(lines):
        o+=f'<text x="{cx}" y="{cy-40+i*29}" text-anchor="middle" font-family="League Spartan,sans-serif" font-weight="700" font-size="23" fill="#fff">{l}</text>'
    for i,(k,sk,lab) in enumerate(HUB):
        a=-90+i*360/n; x,y=pt(rmed,a); c=SENS[sk][0]
        o+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="46" fill="#fff" stroke="{c}" stroke-width="5"/>'+nested(k,x-41,y-41,82)
        lx,ly=pt(rlab,a); tw=len(lab)*8.4+28
        o+=(f'<rect x="{lx-tw/2:.0f}" y="{ly-15:.0f}" width="{tw:.0f}" height="30" rx="15" fill="{c}"/>'
            f'<text x="{lx:.0f}" y="{ly+5:.0f}" text-anchor="middle" font-family="Roboto,sans-serif" font-weight="700" font-size="14.5" fill="#fff">{lab}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Roue : ce que le vivant nous apprend sur nos conditions de vie. Huit animaux et la condition que chacun signale">{o}</svg>'
CROSS=[(['rainette','chouette','fennec'],'La rainette chante-t-elle quand l’air devient humide, ou quand la lumière baisse ?','Humidité, lumière et bruit, enregistrés ensemble : on cherche quel facteur précède le chant.'),
       (['crocodile','chouette'],'Le bitume rend-il la chaleur du soleil après la tombée de la nuit ?','Température de deux sols et lumière : on compare les courbes avant et après le coucher du soleil.'),
       (['tortue','chauvesouris'],'L’éclairage public change-t-il ce qui se passe la nuit ?','Direction de la lumière artificielle et passages nocturnes, près et loin d’un lampadaire.')]
MODES=[('Un capteur par animal','Chaque sentinelle met en avant la grandeur liée au sens de son animal.'),
       ('Toutes les mesures à la fois','Une même carte peut enregistrer en parallèle la lumière, la température, l’humidité, la pression et le son.'),
       ('Des capteurs en plus','Les connecteurs de la carte accueillent d’autres capteurs : humidité du sol, CO₂…')]
DISC=[('Sciences et technologie','relations entre le vivant et son milieu, capteurs et protocoles'),('Mathématiques','mesures, tableaux, graphiques et durées'),
      ('Géographie','espace proche, cartographie et rythmes du jour et de la nuit'),('Enseignement moral et civique','débattre et argumenter des choix d’aménagement'),
      ('Français','recherche documentaire, compte rendu et argumentation'),('Arts plastiques','conception visuelle et fabrication des sentinelles')]

ENQ=[(['chouette','kid_sleep'],[('Lumière','lum')],'Nos nuits sont-elles vraiment noires ?',
       ('La chouette chasse dans de faibles niveaux de lumière et certaines espèces nocturnes évitent les zones fortement éclairées.','Les sentinelles enregistrent la lumière dans la cour et près des bâtiments, du soir au matin.','Comparer nos perceptions aux mesures et réfléchir aux effets de l’éclairage nocturne sur le vivant et le sommeil.'),'La chouette · Lumière nocturne'),
     (['fennec','kid_noise'],[('Niveau sonore','mic')],'Où et quand l’école est-elle trop bruyante ?',
       ('Les grands pavillons du fennec favorisent la perception de sons faibles.','Les sentinelles relèvent le bruit dans la classe, les couloirs, la cantine et la cour.','Comparer le bruit ressenti aux mesures et discuter de ses effets sur la fatigue, la concentration et le bien-être.'),'Le fennec · Paysage sonore'),
     (['crocodile','kid_heat'],[('Température','hts')],'Où fait-il bon dans la cour quand il fait chaud ?',
       ('Le crocodile alterne exposition au soleil et recherche d’ombre pour réguler sa température.','Les sentinelles comparent le bitume, l’herbe, l’ombre et la proximité des murs.','Comparer la chaleur ressentie aux mesures et imaginer des aménagements pour améliorer le confort d’été.'),'Le crocodile · Microclimats')]
def tree_html():
    cards=''
    for i,(ks,ms,q,(obs,mes,nous),*_) in enumerate(ENQ,1):
        chips=''.join(f'<span class="mchip" style="--c:{SENS[sk][0]}">{m}</span>' for m,sk in ms)
        cards+=(f'<article class="enq"><div class="ehead"><span class="pm">'+''.join(med(k) for k in ks)+
                f'</span><h4>{q}</h4></div><ol class="steps3"><li><b>Observer le vivant</b><span>{obs}</span></li><li><b>Mesurer</b><div class="chips">{chips}</div><span>{mes}</span></li><li><b>Pour nous</b><span>{nous}</span></li></ol></article>')
    return (f'<div class="tree"><p class="etag pex">Par exemple</p>'
            f'<div class="t-branches">{cards}</div><div class="t-join"></div>'
            f'<div class="t-bottom"><p class="etag">Conclusion</p><p>Du vivant à nous : la classe relie ce que les animaux supportent mal à ce qui dégrade aussi ses propres conditions de vie, puis propose des améliorations pour l’école.</p></div></div>')

QUESTIONS={'chouette':'À quelle heure la nuit commence-t-elle réellement ?','rainette':'L’air est-il plus humide la nuit que le jour ?',
 'fennec':'Le chant des oiseaux à l’aube est-il visible dans les mesures ?','chauvesouris':'Y a-t-il plus de passages la nuit ou le jour ?',
 'tortue':'La nuit, vers où la lumière artificielle attirerait-elle une jeune tortue ?','martinet':'La pression baisse-t-elle avant un orage ?',
 'crocodile':'Quels sols de la cour gardent la chaleur du soleil la nuit ?','abeille':'La couleur de la lumière change-t-elle du matin au soir ?'}
def qgrid_html():
    o=''
    for k,sk,lab in HUB:
        c=SENS[sk][0]
        o+=(f'<article class="qcard" style="--c:{c}"><span class="med">{I[k]}</span><div><span class="mchip">Capteur : {IDX[k][3].lower()}</span>'
            f'<p>{QUESTIONS[k]}</p></div></article>')
    return f'<div class="qgrid">{o}</div>'

def orbit_svg():
    W=H=600; c=300; R=205; n=len(HUB); o=''
    o+=f'<circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="#C9CED6" stroke-width="2" stroke-dasharray="1 8" stroke-linecap="round"/>'
    o+=f'<circle cx="{c}" cy="{c}" r="104" fill="#1F2455"/>'
    for i,l in enumerate(('Ce que le vivant','nous apprend sur','nos conditions','de vie')):
        o+=f'<text x="{c}" y="{c-34+i*25}" text-anchor="middle" font-family="League Spartan,sans-serif" font-weight="700" font-size="20" fill="#fff">{l}</text>'
    for i,(k,sk,lab) in enumerate(HUB):
        a=math.radians(-90+i*360/n); x=c+R*math.cos(a); y=c+R*math.sin(a); col=SENS[sk][0]
        o+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="41" fill="#fff" stroke="{col}" stroke-width="3"/>'+nested(k,x-37,y-37,74)
        o+=f'<text x="{x:.0f}" y="{y+62:.0f}" text-anchor="middle" font-family="Roboto,sans-serif" font-weight="700" font-size="14" fill="{col}">{lab}</text>'
    return f'<svg viewBox="-40 -10 {W+80} {H+60}" role="img" aria-label="Ce que le vivant nous apprend sur nos conditions de vie : huit animaux et la condition que chacun signale">{o}</svg>'

def ex_cards():
    o=''
    for ks,ms,q,(obs,mes,nous),sub in ENQ:
        chips=''.join(f'<span class="mchip" style="--c:{SENS[sk][0]}">{m}</span>' for m,sk in ms)
        link={'chouette':'Lumière la nuit','fennec':'Bruit','crocodile':'Chaleur'}[ks[0]]
        col={'chouette':SENS['lum'][0],'fennec':SENS['mic'][0],'crocodile':SENS['hts'][0]}[ks[0]]
        o+=(f'<article class="xcard"><div class="xpair"><span class="med big">'+I[ks[0]]+f'</span><span class="xlink" style="--c:{col}">{link}</span><span class="med big">'+I[ks[1]]+'</span></div>'
            f'<h4 class="xq">{q}</h4><p class="xsub">{sub}</p>'
            f'<ol class="xline"><li style="--d:#7B55D6"><b>Observer le vivant</b><span>{obs}</span></li>'
            f'<li style="--d:#2F8FE0"><b>Mesurer</b><div class="chips">{chips}</div><span>{mes}</span></li>'
            f'<li style="--d:#E8703A"><b>Pour nous</b><span>{nous}</span></li></ol></article>')
    return o

def board_mini():
    return (f'<svg viewBox="-6 -4 73 100" role="img" aria-label="La carte STeaMi"><path d="{OUTLINE}" fill="#141414"/>'
            '<circle cx="30.55" cy="27.75" r="21" fill="#DADDE0"/><circle cx="30.55" cy="27.75" r="18.6" fill="#0B0B0B"/>'
            '<path d="M15 34 L21 30 L27 33 L33 22 L39 26 L46 18" fill="none" stroke="#F7D117" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="7" y="81.8" width="47" height="9.9" fill="#E0B43A"/></svg>')
REGARDS=[('chouette','Le regard du vivant','Ce que l’animal perçoit, ce à quoi il réagit et le comportement qu’il adopte.','#7B55D6'),
         ('kid_look','Le regard humain','Ce que les élèves observent, ressentent et pensent pouvoir expliquer.','#E8703A'),
         ('board','Le regard du capteur','Ce que la STeaMi mesure et transforme en données comparables.','#2F8FE0')]
def regards_html():
    o=''
    for k,t,d,c in REGARDS:
        m=f'<span class="med board">{board_mini()}</span>' if k=='board' else f'<span class="med">{I[k]}</span>'
        o+=f'<article class="regard" style="--rc:{c}">{m}<h4>{t}</h4><p>{d}</p></article>'
    return f'<div class="regards">{o}</div>'
STEPS8=[('Observer et se documenter','sur un animal, son milieu et son comportement.'),('Décrire ses perceptions','et repérer ce qui semble varier dans l’environnement.'),
 ('Formuler une question et une hypothèse','reliant le comportement à une grandeur mesurable.'),('Choisir et programmer un capteur','en précisant ce qu’il mesure réellement.'),
 ('Concevoir un protocole','lieux, durée, fréquence, témoin et répétitions.'),('Mesurer et représenter les données','sous forme de tableaux et de graphiques.'),
 ('Comparer','le comportement documenté, les perceptions des élèves et les résultats.'),('Conclure et proposer une action','pour l’école ou son environnement proche.')]
CHAIN5=['Observer','questionner','mesurer','comparer','interpréter']

PHASES=[('Observer','#7B55D6','#ECE4FF',[1,2]),('Questionner','#E8703A','#FFE6D9',[3]),('Mesurer','#2F8FE0','#DDEEFF',[4,5,6]),('Comparer','#B98A1E','#FFF4C7',[7]),('Interpréter','#7B55D6','#ECE4FF',[8])]
def phases_html():
    o=''
    for name,c,pale,nums in PHASES:
        items=''.join(f'<li><span class="pn" style="--pl:{pale}">{n}</span><div><b>{STEPS8[n-1][0]}</b><span>{STEPS8[n-1][1]}</span></div></li>' for n in nums)
        o+=f'<div class="phase" style="--pc:{c}"><p class="ph-name"><i></i>{name}</p><ul>{items}</ul></div>'
    return f'<div class="phases">{o}</div>'

PHASE_OF={1:'Observer',2:'Observer',3:'Questionner',4:'Mesurer',5:'Mesurer',6:'Mesurer',7:'Comparer',8:'Interpréter'}
STEP_COL=['#FFF1B8','#FFD9C4','#CFE6FF','#E2D8FF','#CFE6FF','#E2D8FF','#FFF1B8','#FFD9C4']
def steps_grid():
    o=''
    for n,(t,d) in enumerate(STEPS8,1):
        o+=f'<li><span class="sn8">{n:02d}</span><p class="ph8">{PHASE_OF[n]}</p><b>{t}</b><span class="sd8">{d}</span></li>'
    return f'<ol class="grid8">{o}</ol>'

CORE=('chouette','rainette','crocodile','fennec','abeille','chauvesouris')
LATER={'martinet':'Il faut attendre un changement de temps, donc un suivi sur plusieurs jours.',
       'chat':'Très parlant pour découvrir un capteur, mais il ne renseigne pas sur l’environnement.',
       'tortue':'Le sujet est fort, mais le protocole suppose de tourner la sentinelle, de nuit et dehors.'}
def later_card(a):
    k,n,t,cap,ref,gr,q,per,sk=a; c=SENS[sk][0]
    return (f'<article class="later" style="--c:{c}"><span class="med">{I[k]}</span>'
            f'<div><span class="lc">{cap}</span><b>{n}</b><span class="ld">{LATER[k]}</span></div></article>')

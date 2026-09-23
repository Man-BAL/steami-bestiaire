import math
OUTLINE=open('steami_outline.txt').read().strip()
WOOD='#E6C593'; WOOD_D='#C99B5E'; ENG='#9A6A36'; LINE='#1A1A1A'
def owl_path(): return 'M30 40 L22 6 L56 28 Q80 20 104 28 L138 6 L130 40 Q156 80 150 130 Q142 196 80 204 Q18 196 10 130 Q4 80 30 40 Z'
def rrect(x,y,w,h,r): return f'M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z'
def circ(cx,cy,r): return f'M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z'
K=1.25; BX,BY=80-30.55*K,40      # carte dans le repère de la chouette
SCR=(80,BY+27.75*K); SR=21.2*K
LUM=(BX+43.85*K,BY+12.04*K)
BAT=(80-21,BY+47.1*K-28.5,42,57)
DOW=[(26,72),(134,72),(30,168),(130,168)]
OY=70; LX={'dos':20,'carte':215,'fac':410}
def P(k,x,y): return (round(LX[k]+x,1), round(OY+y,1))
def plate(ox,d,holes=''):
    return (f'<path d="{d}" transform="translate({ox+6} {OY+6})" fill="{WOOD_D}" stroke="{LINE}" stroke-width="1.4"/>'
            f'<path d="{d} {holes}" transform="translate({ox} {OY})" fill="{WOOD}" fill-rule="evenodd" stroke="{LINE}" stroke-width="1.6"/>')
dowh=' '.join(circ(x,y,3.2) for x,y in DOW)
dos=plate(LX['dos'],owl_path(),rrect(*BAT,6)+' '+dowh)
dos+=f'<g transform="translate({LX["dos"]+10} {OY+214})"><path d="M6 6 H146 V20 H6 Z" fill="{WOOD_D}" stroke="{LINE}" stroke-width="1.2"/><path d="M0 0 H140 V14 H0 Z M66 0 V7 H74 V0" fill="{WOOD}" stroke="{LINE}" stroke-width="1.4"/></g>'
fac=plate(LX['fac'],owl_path(),circ(SCR[0],SCR[1],SR+1)+' '+circ(LUM[0],LUM[1],3.2)+' '+dowh)
fac+=f'<g transform="translate({LX["fac"]} {OY})"><g fill="none" stroke="{ENG}" stroke-width="2" stroke-linecap="round">'+''.join(f'<path d="M{x-7} {y} l7 6 l7 -6"/>' for x,y in ((64,132),(80,132),(96,132),(56,150),(72,150),(88,150),(104,150),(64,168),(80,168),(96,168),(72,184),(88,184)))+f'<path d="M36 40 L30 18 M124 40 L130 18"/><circle cx="{SCR[0]}" cy="{SCR[1]}" r="{SR+8}"/></g><path d="M74 110 L86 110 L80 120 Z" fill="{ENG}"/></g>'
bx,by,bw,bh=BAT
carte_g=(f'<g transform="translate({LX["carte"]} {OY})"><rect x="{bx-30}" y="{by+10}" width="{bw}" height="{bh}" rx="6" fill="#7B55D6" stroke="{LINE}" stroke-width="1.2"/>'
       f'<g transform="translate({BX} {BY}) scale({K})"><path d="{OUTLINE}" fill="#141414" stroke="{LINE}" stroke-width=".8"/>'
       + ''.join(f'<circle cx="{30.55+28*math.cos(math.radians(a)):.2f}" cy="{30.65-28*math.sin(math.radians(a)):.2f}" r="2.5" fill="#E0B43A"/>' for a in (20,33,45,57,123,135,147,160)) +
       f'<circle cx="30.55" cy="27.75" r="21" fill="#DADDE0"/><circle cx="30.55" cy="27.75" r="18.6" fill="#0B0B0B"/>'
       f'<circle cx="23" cy="27.75" r="5.4" fill="#F7D117"/><circle cx="38.1" cy="27.75" r="5.4" fill="#F7D117"/><circle cx="23" cy="27.75" r="2.3" fill="#0B0B0B"/><circle cx="38.1" cy="27.75" r="2.3" fill="#0B0B0B"/>'
       f'<rect x="42.6" y="10.8" width="3" height="2.2" fill="#b9a8e8"/><rect x="7" y="81.8" width="47" height="9.9" fill="#E0B43A"/></g></g>')
guides=''
for (x,y) in DOW:
    a=P('dos',x,y); c=P('fac',x,y)
    guides+=f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="#8A8F93" stroke-width="1" stroke-dasharray="4 4"/>'
b1=P('dos',bx+bw/2,by+bh/2); b2=P("carte",bx+bw/2-30,by+bh/2+10)
s1=P('carte',*SCR); s2=P('fac',*SCR)
guides+=f'<line x1="{b1[0]}" y1="{b1[1]}" x2="{b2[0]}" y2="{b2[1]}" stroke="#7B55D6" stroke-width="1.6" stroke-dasharray="6 4"/>'
guides+=f'<line x1="{s1[0]}" y1="{s1[1]}" x2="{s2[0]}" y2="{s2[1]}" stroke="#B98A1E" stroke-width="1.6" stroke-dasharray="6 4"/>'
dowels=''.join(f'<rect x="{(P("dos",x,y)[0]+P("fac",x,y)[0])/2-10}" y="{P("dos",x,y)[1]-3.5}" width="20" height="7" rx="3.5" fill="{WOOD_D}" stroke="{LINE}" stroke-width="1"/>' for x,y in DOW[:2])
def pinn(n,x,y,tx,ty): return f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{LINE}" stroke-width="1"/><circle cx="{x}" cy="{y}" r="2.5" fill="{LINE}"/><circle cx="{tx}" cy="{ty}" r="12" fill="#E0B43A" stroke="{LINE}" stroke-width="1.6"/><text x="{tx}" y="{ty+4.5}" text-anchor="middle" font-family="League Spartan,sans-serif" font-weight="700" font-size="14" fill="{LINE}">{n}</text>'
d1=P('dos',150,170); d2=P('dos',bx+bw-4,by+8); d7=P('dos',120,221)
c3=P('carte',BX+12,BY+100); c4=((P("dos",134,72)[0]+P("fac",134,72)[0])/2,P("dos",134,72)[1]-3.5)
f5=P('fac',*LUM); f6=P('fac',130,170)
pins=(pinn(2,*d2,d2[0],28)+pinn(4,*c4,c4[0],28)+pinn(5,*f5,f5[0]+12,28)
      +pinn(1,*d1,d1[0]+6,392)+pinn(7,*d7,d7[0]-40,392)+pinn(3,*c3,c3[0],392)+pinn(6,*f6,f6[0],392))
ASSEMBLY=f'''<svg viewBox="0 0 600 410" role="img" aria-label="Vue éclatée de la sentinelle chouette : dos percé pour la batterie et son pied, carte STeaMi, chevilles, façade avec fenêtre d’écran">
{dos}{guides}{carte_g}{dowels}{fac}{pins}</svg>'''
ASSEMBLY_LEGEND=[('Dos','découpé à la silhouette de l’animal.'),('Ouverture','la batterie, au dos de la carte, la traverse.'),('Carte STeaMi','posée sur le dos, écran vers l’avant.'),('Chevilles','relient le dos et la façade.'),('Fenêtre capteur','laisse passer la lumière jusqu’au capteur.'),('Façade','maintient la carte ; l’écran apparaît dans la fenêtre ronde.'),('Pied à encoche','tient la sentinelle debout.')]

PROG={
 'CM1':[('Les êtres vivants · Écosystèmes','décrit les caractéristiques […] d’un écosystème (altitude, latitude, humidité, pluviométrie, luminosité, température) […] ; met en relation la présence d’êtres vivants avec les caractéristiques physiques du milieu','La rainette, la chouette et le crocodile mesurent ces paramètres ; les élèves les relient à l’activité des animaux.'),
        ('La Terre, une planète active · Météorologie','Réaliser et exploiter des mesures météorologiques en utilisant des capteurs […] au cours du temps (journée, semaine, mois, saison)','L’observatoire enregistre jour et nuit ; le martinet suit la pression.'),
        ('Les êtres vivants · Reproduction','Mettre en relation le type de fécondation […] avec le mode de reproduction ovipare et vivipare des animaux','Classer les neuf animaux : ovipares (crocodile, tortue, rainette, oiseaux, abeille) et vivipares (chat, fennec, chauve-souris).'),
        ('Les êtres vivants · Classification','Réaliser une classification en groupes emboités à partir d’un petit nombre d’espèces','Le bestiaire fournit la collection : poils, plumes, écailles, six pattes…'),
        ('Le corps humain · Le cerveau','Comprendre quelques mécanismes perceptifs et comment notre perception du monde peut être différente de sa réalité physique','Comparer nos sens, ceux des animaux et les capteurs de la carte.'),
        ('La matière · Mesures','une première approche des concepts de reproductibilité et de variabilité des mesures','Les sentinelles posées côte à côte ne donnent pas exactement les mêmes valeurs.'),
        ('Objets techniques · Programmation','Utiliser un programme pour agir sur le comportement d’un objet technique','La sentinelle est programmée par blocs pour mesurer et réagir.')],
 'CM2':[('Objets techniques · Conception','Rechercher des idées de solutions à l’aide de croquis […] Associer une contrainte à un choix de matériau […] Organiser le travail de conception d’une maquette et la fabriquer','Concevoir l’animal et son abri, choisir le matériau, fabriquer en classe ou avec un fablab.'),
        ('Objets techniques · Programmation','Comprendre un algorithme […] L’élève repère les boucles et les conditions','Mesurer à intervalle régulier (boucle), réagir à un seuil (condition).'),
        ('La Terre · Climat local','décalage temporel du cycle de vie de certaines espèces (floraison, fructification, migration, etc.)','Le martinet, migrateur, revient chaque printemps.'),
        ('Les êtres vivants · Écosystèmes','S’impliquer dans des actions et des projets relatifs à l’éducation au développement durable […] biodiversité','L’observatoire comme projet de classe sur la biodiversité proche ; la tortue ouvre sur la pollution lumineuse.')],
 '6e':[('Mouvements · Jour et nuit','Interpréter l’alternance du jour et de la nuit […] la variation de la durée de la journée […] données issues d’une éphéméride','La courbe de lumière de la chouette donne la durée du jour, à comparer à l’éphéméride.'),
       ('Les êtres vivants · Écosystèmes','Suivre les changements de peuplement au cours des saisons […] et les relier aux changements des paramètres physiques (température, ensoleillement, précipitations…)','Relancer l’observatoire à plusieurs moments de l’année.'),
       ('Les êtres vivants · Écosystèmes','concevoir et réaliser un objet technique favorisant la biodiversité (nichoir, mangeoire, hôtel à insectes)','Associer une sentinelle à un nichoir à martinets ou à un gîte à chauves-souris.'),
       ('Reproduction · Pollinisation','démontre le rôle clé des insectes dans la pollinisation','L’abeille et sa vision des couleurs des fleurs.'),
       ('Signaux · Électricité','Réaliser un circuit électrique à une boucle avec un capteur (de température, d’éclairement, de mouvement, etc.)','Relier ces capteurs à ceux, intégrés, de la STeaMi.')],
}

PROG2={ # classe : (couleur, [(notion, ce que fait le bestiaire, animaux)])
 'CM1':('#FF8A5C',[('Écosystèmes','Relier la présence des êtres vivants à l’humidité, la lumière et la température',['rainette','chouette','crocodile']),
                   ('Météorologie','Mesurer avec des capteurs au fil de la journée',['martinet']),
                   ('Ovipares et vivipares','Classer les neuf animaux du bestiaire',['crocodile','chat']),
                   ('Perception','Comparer nos sens, ceux des animaux et les capteurs',['abeille','fennec']),
                   ('Programmation','Faire réagir la sentinelle à une mesure',['chauvesouris'])]),
 'CM2':('#6CC4FF',[('Conception d’une maquette','Dessiner, choisir le matériau, fabriquer l’animal',['chouette']),
                   ('Boucles et conditions','Mesurer à intervalle régulier, réagir à un seuil',['chat']),
                   ('Climat local','Suivre le retour des migrateurs',['martinet']),
                   ('Projet de développement durable','Enquêter sur la pollution lumineuse',['tortue'])]),
 '6e': ('#B89CFF',[('Jour et nuit','Mesurer la durée du jour et la comparer à l’éphéméride',['chouette']),
                   ('Saisons','Relancer l’observatoire au fil de l’année',['rainette','crocodile']),
                   ('Biodiversité','Associer une sentinelle à un nichoir ou un gîte',['martinet','chauvesouris']),
                   ('Pollinisation','Relier la vision de l’abeille aux couleurs des fleurs',['abeille'])]),
}

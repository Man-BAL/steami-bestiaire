exec(open('illus.py').read())
exec(open('addon.py').read())
exec(open('stations_addon.py').read())
exec(open('sensors_addon.py').read())
exec(open('cross_addon.py').read())
exec(open('crea_addon.py').read())
import math
ST={'cit':('#4452C4','#D9E1FF','Citoyenneté et données'),'env':('#1E8F4E','#CDF3D6','Environnement et Bien-être'),
    'mob':('#D24A45','#FFD9D2','Mobilité et Transport'),'ene':('#E0A92B','#FFEAA8','Énergie et confort thermique'),'ia':('#A3259B','#F8D5F3','Intelligence Artificielle')}
A=[ # six sentinelles de départ — clé, nom, trait, capteur, ref, grandeur, question, période, clé capteur
 ('abeille','L’abeille','Elle perçoit l’ultraviolet, le bleu et le vert, mais ne distingue pas le rouge.','Couleur','APDS-9960','Composantes rouge, verte et bleue','Peut-on apprendre à la carte à reconnaître les couleurs des fleurs qu’une abeille visiterait ?','Jour','lum'),
 ('martinet','Le martinet','Il vit presque toujours en vol et contourne les dépressions orageuses.','Pression atmosphérique','WSEN-PADS','Pression (hPa)','La pression baisse-t-elle avant un orage ?','Jour','pres'),
 ('crocodile','Le crocodile','Ectotherme, il se chauffe au soleil sur les pierres ; la température du nid détermine le sexe des petits.','Température','WSEN-HIDS','Température (°C)','Quels sols de la cour gardent la chaleur du soleil la nuit ?','Jour','hts'),
 ('chat','Le chat','Son oreille interne perçoit la gravité et les rotations : c’est le réflexe de redressement.','Accéléromètre et gyroscope','ISM330DL','Accélération (m/s²), rotation (°/s)','Comment mesurer une chute ou un mouvement, comme le fait l’oreille interne du chat ?','Crépuscule','imu'),
 ('chouette','La chouette','Sa vision est adaptée à la très faible lumière : elle chasse au crépuscule et la nuit.','Lumière','APDS-9960','Éclairement','À quelle heure la nuit commence-t-elle réellement ?','Nuit','lum'),
 ('rainette','La rainette','Sa peau perméable doit rester humide ; elle est active par les nuits humides.','Humidité','WSEN-HIDS','Humidité relative (%)','L’air est-il plus humide la nuit que le jour ?','Nuit','hts'),
 ('chauvesouris','La chauve-souris','Par écholocation, elle estime une distance à partir du délai de retour de l’écho.','Distance (temps de vol)','VL53L1X','Distance (mm)','Combien de passages la nuit, comparée au jour ?','Nuit','dist'),
 ('fennec','Le fennec','Ses très grands pavillons auriculaires captent et concentrent les sons faibles.','Microphone','IMP34DT05','Niveau sonore relatif','Le chant des oiseaux à l’aube est-il visible dans les mesures ?','Nuit','mic'),
 ('tortue','La tortue caouanne','À la naissance, les jeunes tortues rejoignent la mer de nuit en se dirigeant vers l’horizon le plus lumineux ; adultes, elles s’orientent grâce au champ magnétique terrestre.','Magnétomètre et lumière','LIS2MDL · APDS-9960','Direction (°) et éclairement','La nuit, vers où la lumière artificielle attirerait-elle une jeune tortue ?','Nuit','mag'),
]
IDX={a[0]:a for a in A}
def logo(s=40):
    pads=''.join(f'<circle cx="{32+26*math.cos(math.radians(a)):.1f}" cy="{32+26*math.sin(math.radians(a)):.1f}" r="3.2" fill="#E0B43A"/>' for a in (200,222,244,296,318,340))
    return f'<svg width="{s}" height="{s}" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="31" fill="#141414"/>{pads}<circle cx="32" cy="34" r="19" fill="#D9DCDF"/><circle cx="32" cy="34" r="16.5" fill="#0B0B0B"/><path d="M21 36 a5 5 0 0 1 10 0 M33 36 a5 5 0 0 1 10 0" fill="none" stroke="#F7D117" stroke-width="3"/></svg>'
def per_cls(p): return {'Jour':'jour','Nuit':'nuit','Crépuscule':'crep','Orientation':'orient'}[p]
def card(a):
    k,n,t,cap,ref,gr,q,per,sk=a; c,pale=SENS[sk][0],SENS[sk][1]
    return f'''<article class="card" style="--c:{c};--pale:{pale}">
<div class="ill">{I[k]}<span class="per {per_cls(per)}">{per}</span></div>
<div class="body"><h3>{n}</h3><p class="trait">{t}</p>
<dl><dt>Capteur</dt><dd>{cap} <span class="ref">{ref}</span></dd><dt>Grandeur</dt><dd>{gr}</dd><dt>Question</dt><dd class="q">{q}</dd></dl></div></article>'''
def med(k,cls=''): return f'<span class="med {cls}">{I[k]}</span>'

# frise 24 h : positions en % (0 = minuit, 50 = midi)
FRISE=[('chouette',5),('rainette',14),('tortue',23),('abeille',38),('crocodile',50),('martinet',62),('chat',73),('chauvesouris',84),('fennec',95)]
STEPS=[('Observer','Relever les animaux actifs de jour et de nuit dans l’environnement proche de l’établissement.'),
 ('Questionner','Formuler une question qui relie un comportement animal à une grandeur mesurable.'),
 ('Émettre une hypothèse','Proposer une explication que la mesure pourra confirmer ou réfuter.'),
 ('Concevoir le protocole','Emplacements, fréquence et durée des mesures, sentinelle témoin, vérification croisée des cartes.'),
 ('Mesurer','Les sentinelles enregistrent sur batterie ; chaque série est horodatée et documentée.'),
 ('Analyser et conclure','Superposer les courbes, valider ou réfuter l’hypothèse, discuter les limites des capteurs.')]

css='''
:root{--ink:#1A1A1A;--muted:#4D5358;--gold:#E0B43A;--gold-txt:#B98A1E;--card:#F2F2F2;--line:#E4E4E4;--night:#1F2455;
--title:'League Spartan','Trebuchet MS',sans-serif;--body:'Roboto',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:67px}
body{background:#fff;color:var(--ink);font:17px/1.55 var(--body)}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding-inline:24px}
h1,h2,h3,h4{font-family:var(--title);line-height:1.08;text-wrap:balance}
h2{font-weight:300;font-size:clamp(1.9rem,3.6vw,2.7rem)} h2 b{font-weight:700}
.kicker{font:600 .78rem var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--gold-txt)}
.lede{color:var(--gold-txt);font-weight:700;font-size:1.15rem;line-height:1.45;max-width:70ch}
section{padding-block:76px}
.sec-head{display:grid;gap:12px;margin-bottom:34px;max-width:92ch}
.sec-head p:not(.lede){color:var(--muted)}
.rule{border:0;border-top:3px solid var(--gold);width:72px;margin-top:4px}
/* nav */
nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.94);backdrop-filter:blur(6px);border-bottom:3px solid var(--gold)}
nav .wrap{display:flex;align-items:center;gap:14px;height:64px}
nav .brand{font:300 1.25rem var(--title);display:flex;align-items:center;gap:10px;text-decoration:none;white-space:nowrap} nav .brand b{font-weight:700}
nav ul{list-style:none;display:flex;gap:22px;margin-left:auto;font-size:.92rem;font-weight:500}
nav a{text-decoration:none} nav ul a:hover,nav ul a:focus-visible{color:var(--gold-txt)}
/* hero */
.hero{padding-block:64px 70px;background:linear-gradient(180deg,#FFFDF4 0%,#FFF6D8 100%);overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center}
.hero h1{font-weight:300;font-size:clamp(2.8rem,6.2vw,4.8rem);letter-spacing:-.01em;margin:10px 0 18px} .hero h1 b{font-weight:700}
.hero p.txt{margin-top:16px;color:var(--muted);max-width:60ch}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.facts span{background:#fff;border:2px solid var(--ink);border-radius:99px;padding:5px 14px;font-size:.88rem;font-weight:500}
.cluster{position:relative;aspect-ratio:1;max-width:500px;width:100%;justify-self:center}
.cluster .med{position:absolute;border-radius:50%;box-shadow:0 10px 26px rgba(20,20,40,.18)}
.cluster .med svg{display:block;width:100%;height:auto}
.m1{width:46%;left:27%;top:26%;z-index:3} .m2{width:30%;left:4%;top:6%} .m3{width:28%;right:4%;top:2%} .m4{width:30%;left:0;bottom:6%} .m5{width:27%;right:6%;bottom:2%} .m6{width:20%;left:44%;top:0;z-index:2} .m7{width:22%;right:0;top:40%}
a.inl{color:var(--gold-txt);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.sec-head.full{max-width:none}
.totop{position:fixed;right:22px;bottom:calc(22px + env(safe-area-inset-bottom,0px));z-index:20;width:52px;height:52px;border-radius:50%;background:#F7D117;border:2.5px solid #1A1A1A;box-shadow:0 4px 0 #1A1A1A;display:grid;place-items:center;opacity:0;pointer-events:none;transform:translateY(8px);transition:opacity .2s,transform .2s}
.totop.show{opacity:1;pointer-events:auto;transform:none}
.totop:hover{background:#FFE14D}
@media (prefers-reduced-motion:reduce){.totop{transition:none}}
.prog2{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:start}
.pcard{background:#fff;border-radius:18px;overflow:hidden;border:2.5px solid var(--ink);box-shadow:5px 5px 0 var(--ink)}
.phead{background:var(--pc);padding:14px 18px;border-bottom:2.5px solid var(--ink)}
.phead span{font:700 1.7rem/1 var(--title)}
.pcard ul{list-style:none;padding:8px 16px 12px}
.pcard li{display:grid;grid-template-columns:84px 1fr;gap:12px;align-items:center;padding:9px 0;border-bottom:1px dashed #D9D9D9}
.pcard li:last-child{border-bottom:0}
.pm{display:flex;justify-content:center} .pm .med{display:block;width:36px;margin-left:-10px;border-radius:50%;box-shadow:0 0 0 2px #fff} .pm .med:first-child{margin-left:0} .pm svg{display:block;width:100%;height:auto}
.pcard li b{display:block;font:700 1.02rem/1.15 var(--title)} .pcard li div span{font-size:.86rem;color:var(--muted);line-height:1.35;display:block}
.official{margin-top:26px}
.official summary{cursor:pointer;display:inline-block;font-weight:700;background:#fff;border:2px solid var(--ink);border-radius:99px;padding:7px 16px;list-style:none}
.official summary::-webkit-details-marker{display:none}
.official summary::after{content:" +";} .official[open] summary::after{content:" –"}
.official .prog{margin-top:18px}
.sens-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:32px;align-items:center}
.boards{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.bview{margin:0;text-align:center} .bview svg{width:100%;height:auto;display:block} .bview figcaption{font:600 .78rem var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:8px}
.scards{display:grid;gap:10px}
.scard2{display:grid;grid-template-columns:40px 1fr auto;gap:14px;align-items:center;background:var(--pale);border-radius:14px;padding:10px 14px}
.scard2 .sn{width:34px;height:34px;border-radius:50%;background:var(--c);color:#fff;display:grid;place-items:center;font:700 1.05rem var(--title)}
.scard2 b{display:block;font:700 1.08rem/1.1 var(--title);color:var(--ink)} .scard2 .sref{font-size:.82rem;color:var(--muted)}
.scard2 em{display:inline-block;font-style:normal;background:#1A1A1A;color:#fff;border-radius:7px;padding:1px 8px;font-size:.66rem;margin-left:8px}
.scard2 .pm .med{width:38px}
.hub{max-width:720px;width:100%;margin:0 auto;text-align:center}
.pex{margin:18px 0 0;font-size:.85rem} .hub svg{width:100%;height:auto;display:block}
.hubtag{margin-bottom:0} .hubnote{font-size:.86rem;color:var(--muted);font-style:italic;margin-top:-6px}
.enum{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#F7D117;border:2px solid var(--ink);color:var(--ink);font:700 .85rem var(--title);margin-right:8px;letter-spacing:0}
h3.sub{font:700 1.35rem var(--title);margin:36px 0 16px}
.cross{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.cross article{background:var(--card);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.cross .pm{justify-content:flex-start} .cross .pm .med{width:46px}
.cross h4{font:700 1.08rem/1.25 var(--title)} .cross p{font-size:.9rem;color:var(--muted)}
.modes-disc{display:grid;grid-template-columns:1fr 1fr;gap:32px}
.modes{list-style:none;counter-reset:m;display:grid;gap:10px}
.modes li{counter-increment:m;position:relative;padding:12px 14px 12px 58px;border-radius:14px;border:2px solid var(--ink);background:#fff}
.modes li::before{content:counter(m);position:absolute;left:14px;top:12px;width:30px;height:30px;border-radius:50%;background:#6CC4FF;border:2px solid var(--ink);display:grid;place-items:center;font:700 1rem var(--title)}
.modes li:nth-child(2)::before{background:#FF8A5C} .modes li:nth-child(3)::before{background:#B89CFF}
.modes b,.disc b{display:block;font:700 1.02rem var(--title)} .modes span,.disc span{font-size:.88rem;color:var(--muted)}
.disc{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.disc li{background:var(--card);border-radius:12px;padding:10px 14px;border-left:5px solid var(--dc,#6CC4FF)}
.disc li:nth-child(2){--dc:#FF8A5C} .disc li:nth-child(3){--dc:#5FD18A} .disc li:nth-child(4){--dc:#B89CFF} .disc li:nth-child(5){--dc:#FF9FC8} .disc li:nth-child(6){--dc:#E8702A}
.tree{display:grid;gap:0;justify-items:center}
.t-top{background:#1F2455;color:#fff;border-radius:18px;padding:18px 28px;text-align:center;max-width:620px;border:3px solid var(--ink);box-shadow:5px 5px 0 var(--ink)}
.t-top .etag{color:#F7D117}
.bigq{font:700 1.6rem/1.2 var(--title)}
.etag{font:700 .72rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--gold-txt);margin-bottom:6px}
.t-branches{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:20px;width:100%;padding-top:44px;margin-bottom:0}
.t-branches::before{content:"";position:absolute;top:0;left:50%;height:22px;border-left:3px solid var(--ink)}
.t-branches::after{content:"";position:absolute;top:22px;left:16.66%;right:16.66%;border-top:3px solid var(--ink)}
.enq{position:relative;background:var(--card);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.enq::before{content:"";position:absolute;top:-22px;left:50%;height:22px;border-left:3px solid var(--ink)}
.enq::after{content:"";position:absolute;bottom:-22px;left:50%;height:22px;border-left:3px solid var(--ink)}
.enq .pm .med{width:46px} .enq .pm{justify-content:flex-start}
.enq h4{font:700 1.08rem/1.25 var(--title)} .enq p:last-child{font-size:.9rem;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.mchip{background:var(--c);color:#fff;font:700 .76rem var(--body);padding:3px 10px;border-radius:99px}
.t-bottom{position:relative;margin-top:44px;background:#fff;border:3px solid var(--ink);border-radius:18px;padding:16px 26px;text-align:center;max-width:680px;box-shadow:5px 5px 0 var(--ink)}
.t-bottom::before{content:"";position:absolute;top:-25px;left:16.66%;right:16.66%}
.t-bottom p:last-child{font-size:.95rem}
.tree .t-bottom{margin-top:0}
.t-join{position:relative;width:100%;height:44px}
.t-join::before{content:"";position:absolute;top:22px;left:16.66%;right:16.66%;border-top:3px solid var(--ink)}
.t-join::after{content:"";position:absolute;top:22px;left:50%;height:22px;border-left:3px solid var(--ink)}
.tree-join{position:relative}
.qgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:8px}
.qcard{display:grid;grid-template-columns:52px 1fr;gap:12px;align-items:start;background:var(--card);border-radius:14px;padding:12px 14px;border-left:5px solid var(--c)}
.qcard .med{display:block;width:52px} .qcard .med svg{display:block;width:100%;height:auto}
.qcard .mchip{display:inline-block;margin-bottom:6px;font-size:.7rem}
.qcard p{font:600 .92rem/1.3 var(--body)}
.ehead{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:center}
.steps3{list-style:none;display:grid;gap:8px;margin-top:4px}
.steps3 li{background:#fff;border-radius:10px;padding:9px 12px;display:grid;gap:4px;position:relative}
.steps3 li b{font:700 .74rem var(--body);letter-spacing:.1em;text-transform:uppercase}
.steps3 li:nth-child(1) b{color:#1E8F4E} .steps3 li:nth-child(2) b{color:#2F8FE0} .steps3 li:nth-child(3) b{color:#D6453D}
.steps3 li span{font-size:.88rem;color:var(--ink);line-height:1.35}
.steps3 li:not(:last-child)::after{content:"";position:absolute;left:50%;bottom:-9px;transform:translateX(-50%);border:6px solid transparent;border-top:7px solid #B9C0C5;z-index:1}
.cross-top{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;margin-bottom:34px}
.cross-top .sec-head{margin-bottom:6px}
.cross-top h3.sub{margin-top:18px}
.cross-top .hub{max-width:none}
.disc-wrap{margin-top:10px} .disc-wrap .disc{grid-template-columns:repeat(3,1fr)}
.sec-night{background:radial-gradient(ellipse at 22% 30%,#34409E 0%,#232A72 45%,#1B1F52 100%);color:#fff}
.sec-night .kicker{color:#F2CB5B} .sec-night h2{color:#fff} .sec-night .rule{border-top-color:#F2CB5B}
.x-top{display:grid;grid-template-columns:1.05fr 1fr;gap:48px;align-items:center}
.x-orbit svg{width:100%;height:auto;display:block}
.x-text h2{margin:10px 0 14px} .x-intro{color:var(--muted);margin-top:16px}
.x-modes{list-style:none;margin-top:22px;display:grid;gap:12px;counter-reset:xm}
.x-modes li{counter-increment:xm;display:grid;grid-template-columns:36px 1fr;column-gap:12px;align-items:start}
.x-modes li::before{content:counter(xm);grid-row:span 2;width:32px;height:32px;border-radius:50%;background:#F7D117;color:#1A1A1A;border:2px solid #1A1A1A;display:grid;place-items:center;font:700 1rem var(--title)}
.x-modes b{font:700 1.05rem var(--title)} .x-modes span{color:var(--muted);font-size:.9rem}
.x-pex{margin:44px 0 18px;text-align:center}
#croisees .steps4{margin-top:6px}
.x-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.xcard{background:#F4F5F7;color:var(--ink);border-radius:20px;padding:22px 22px 20px}
.xhead{display:grid;grid-template-columns:64px 1fr;gap:14px;align-items:center;margin-bottom:16px}
.xhead .med{display:block;width:64px} .xhead .med svg{display:block;width:100%;height:auto}
.xhead h4{font:700 1.15rem/1.2 var(--title)}
.xline{list-style:none;position:relative;display:grid;gap:14px;padding-left:26px}
.xline::before{content:"";position:absolute;left:7px;top:8px;bottom:8px;border-left:2px dashed #CDD3DA}
.xline li{position:relative;display:grid;gap:4px}
.xline li::before{content:"";position:absolute;left:-26px;top:3px;width:16px;height:16px;border-radius:50%;background:var(--d);box-shadow:0 0 0 4px #F4F5F7}
.xline b{font:700 .74rem var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--d)}
.xline span{font-size:.9rem;line-height:1.4}
.x-concl{max-width:980px;margin:40px auto 0;text-align:center;font-size:1.08rem;color:var(--ink);padding:18px 0;border-top:2px dotted #E0B43A;border-bottom:2px dotted #E0B43A}
.x-concl b{color:var(--gold-txt);font-family:var(--title);font-size:1.2rem}
.x-disc{margin-top:36px;text-align:center}
.x-disc ul{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:12px}
.x-disc li{background:#F4F5F7;border-radius:99px;padding:7px 16px;font-size:.88rem;color:var(--muted)}
.x-disc li b{color:var(--ink);font-weight:700;margin-right:4px}
.xpair{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:6px}
.med.big{display:block;width:100%;max-width:120px;justify-self:center} .med.big svg{display:block;width:100%;height:auto;filter:drop-shadow(0 6px 10px rgba(20,20,40,.14))}
.xlink{position:relative;font:700 .72rem var(--body);color:#fff;background:var(--c);border-radius:99px;padding:5px 10px;white-space:nowrap}
.xlink::before,.xlink::after{content:"";position:absolute;top:50%;width:10px;border-top:2px dashed var(--c)}
.xlink::before{right:100%} .xlink::after{left:100%}
.xcap{display:grid;grid-template-columns:1fr 1fr;text-align:center;font:700 .66rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:6px 0 10px}
.xq{font:700 1.15rem/1.2 var(--title);margin-bottom:14px;text-align:center}
.x-foot{margin-top:36px}
.x-foot .x-disc{text-align:center;margin-top:0} .x-foot .x-disc ul{justify-content:center}
.x-foot .x-modes{margin-top:12px}
.owls{display:flex;justify-content:center;gap:34px;flex-wrap:wrap;margin:6px 0 34px}
.owlv{margin:0;text-align:center} .owlv .med{display:block;width:130px} .owlv svg{display:block;width:100%;height:auto;filter:drop-shadow(0 8px 14px rgba(20,20,40,.16))}
.owlv figcaption{margin-top:8px;font:700 .8rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.creas{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.crea{background:var(--card);border-radius:16px;padding:20px}
.cico{display:inline-grid;place-items:center;width:72px;height:72px;border-radius:50%;background:#fff;margin-bottom:10px}
.crea h3{font-size:1.2rem;margin-bottom:6px} .crea p{font-size:.92rem;color:var(--muted)}
.hero .hk{grid-column:1/-1;white-space:nowrap;margin-bottom:-24px}
@media (max-width:760px){.hero .hk{white-space:normal;margin-bottom:0}}
.sec-head p+p{margin-top:10px}
h3.sub.c{text-align:center;margin:38px 0 18px}
.regards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.regard{background:var(--card);border-radius:18px;padding:22px;text-align:center;border-top:6px solid var(--rc)}
.regard .med{display:block;width:120px;margin:0 auto 12px;border-radius:50%} .regard .med svg{display:block;width:100%;height:auto;filter:drop-shadow(0 6px 10px rgba(20,20,40,.14))}
.regard .med.board{background:#fff;padding:14px 22px;aspect-ratio:1;box-sizing:border-box} .regard .med.board svg{filter:none}
.regard h4{font:700 1.2rem var(--title);color:var(--rc);margin-bottom:6px} .regard p{font-size:.93rem;color:var(--muted)}
.gap-q{max-width:900px;margin:22px auto 0;text-align:center;color:var(--muted)}
.gap-q span{display:inline-block;margin:8px 4px 0;background:#fff;border:2px solid var(--ink);border-radius:18px 18px 18px 4px;padding:6px 14px;color:var(--ink);font-weight:500;font-size:.92rem}
.c-lead{text-align:center;color:var(--muted);margin:-6px 0 14px}
.steps8{list-style:none;counter-reset:s8;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.steps8 li{counter-increment:s8;background:var(--card);border-radius:14px;padding:46px 16px 16px;position:relative;font-size:.9rem;color:var(--muted)}
.steps8 li b{display:block;font:700 1.02rem/1.15 var(--title);color:var(--ink);margin-bottom:3px}
.steps8 li::before{content:counter(s8);position:absolute;left:16px;top:12px;width:28px;height:28px;border-radius:50%;background:var(--nc);color:#1A1A1A;border:2px solid var(--ink);display:grid;place-items:center;font:700 .9rem var(--title)}
.steps8 li:nth-child(1){--nc:#FDEB9C} .steps8 li:nth-child(2){--nc:#FFCDB3} .steps8 li:nth-child(3){--nc:#BFE2FF} .steps8 li:nth-child(4){--nc:#BDECCB}
.steps8 li:nth-child(5){--nc:#DCCFFF} .steps8 li:nth-child(6){--nc:#FFC7DC} .steps8 li:nth-child(7){--nc:#B6EAE2} .steps8 li:nth-child(8){--nc:#EDDFC4}
.chain5{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:8px;margin:0 0 20px}
.chain5 .ch{background:#fff;border:2px solid var(--ink);border-radius:99px;padding:7px 18px;font-weight:700;box-shadow:3px 3px 0 var(--ink)}
.chain5 .ch:first-child{background:#F7D117} .chain5 .charr{font:700 1.4rem var(--title);color:var(--gold-txt)}
.xsub{font-style:italic;color:var(--gold-txt);font-weight:500;text-align:center;margin:-8px 0 12px;font-size:.9rem}
.act{display:grid;grid-template-columns:44px 1fr;gap:16px;align-items:start;max-width:860px;margin:34px auto 0;background:#FFF7DA;border-radius:16px;padding:18px 22px}
.act-i{width:40px;height:40px;border-radius:50%;background:#F7D117;border:2px solid var(--ink);display:grid;place-items:center;font:700 1.3rem Georgia,serif;font-style:italic}
.act p{font-size:1rem}
.gap-lead{text-align:center;margin:26px 0 14px;font-weight:700}
.gaps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.gap{display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:center;background:var(--g);border-radius:16px;padding:16px 18px}
.gap p{font-size:.95rem;font-style:italic}
.disc-wrap{margin-top:30px} .dk{text-align:center;margin-bottom:14px}
.xpair{margin-bottom:14px}
.xpair .med.big{position:relative;z-index:1;border-radius:50%;overflow:hidden;background:#fff;box-shadow:0 6px 12px rgba(20,20,40,.14)}
.xpair .med.big svg{clip-path:circle(50% at 50% 50%);filter:none}
.xq{min-height:2.4em;display:flex;align-items:center;justify-content:center;text-wrap:balance}
.phases{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;position:relative;align-items:start}
.phases::before{content:"";position:absolute;left:8%;right:8%;top:12px;border-top:2px dashed #CDD3DA}
.phase{position:relative}
.ph-name{display:flex;flex-direction:column;align-items:center;gap:8px;font:700 .78rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--pc);margin-bottom:12px}
.ph-name i{width:18px;height:18px;border-radius:50%;background:var(--pc);box-shadow:0 0 0 5px #fff;margin-top:4px}
.phase ul{list-style:none;display:grid;gap:10px}
.phase li{background:var(--card);border-radius:14px;padding:12px 14px;display:grid;grid-template-columns:26px 1fr;gap:10px;align-items:start;font-size:.88rem;color:var(--muted);line-height:1.35}
.phase li b{display:block;font:700 .98rem/1.2 var(--title);color:var(--ink);margin-bottom:2px}
.pn{width:26px;height:26px;border-radius:50%;background:var(--pl);color:#1A1A1A;display:grid;place-items:center;font:700 .85rem var(--title)}
.xpair{grid-template-columns:110px 1fr 110px!important}
.xpair .med.big{width:110px;max-width:110px}
.wpills{margin-top:30px}
.wpills ul{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.wpills li{background:#fff;border:2px solid var(--ink);border-radius:99px;padding:6px 16px;font-size:.88rem;color:var(--muted)}
.wpills li b{color:var(--ink)}
.ctx{margin:4px 0 28px;background:#fff;border:2px dashed #E0B43A;border-radius:16px;padding:16px 20px}
.ctx>p{font-weight:700;margin-bottom:10px}
.ctx-chips{display:flex;flex-wrap:wrap;gap:8px}
.ctx-chips span{border-radius:99px;padding:5px 13px;font-size:.88rem;font-weight:500;color:var(--ink)}
.c-lead.gl{margin:22px 0 14px}
.wpills h3.sub.c{margin-top:0}
.xband{background:#1F2455;border-radius:28px;padding:10px 28px 30px;margin:34px -28px 0}
.xband h3.sub.c{color:#fff;margin-top:26px}
.xband .xcard{background:#fff}
.xband .xline li::before{box-shadow:0 0 0 4px #fff}
.bg-sun{background:#FFF8E2}
.ms-top{display:grid;grid-template-columns:1fr 220px;gap:40px;align-items:center}
.ms-text p{color:var(--muted);margin-bottom:12px}
.ms-board{background:#fff;border-radius:50%;aspect-ratio:1;display:grid;place-items:center;padding:28px 44px;box-shadow:0 10px 24px rgba(40,30,90,.12)}
.ms-board svg{width:100%;height:auto;display:block}
.mgs{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.mg{background:#fff;border-radius:18px;padding:20px 22px;border-top:6px solid var(--mc)}
.mg-t{font:700 .78rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--mc);margin-bottom:12px}
.mg-i{background:var(--mp);border-radius:12px;padding:9px 12px;margin-bottom:8px;font-size:.93rem;font-weight:500;color:var(--ink)}
.mg-i:last-child{margin-bottom:0}
.teach{max-width:860px;margin:30px auto 0;background:#fff;border-radius:16px;padding:16px 22px;border-left:6px solid #F7D117}
.teach b{display:block;font:700 .74rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--gold-txt);margin-bottom:4px}
.sec-dark{background:#1F2455;color:#fff}
.sec-dark .kicker{color:#F2CB5B} .sec-dark h2{color:#fff} .sec-dark .rule{border-top-color:#F2CB5B} .sec-dark .sec-head p{color:#DCE0F5}
.sec-dark .xcard{background:#fff;color:var(--ink)}
.ctx-lead{color:var(--muted);margin:6px 0 16px}
.ctiles{display:grid;grid-template-columns:repeat(7,1fr);gap:12px;margin-bottom:30px}
.ctile{text-align:center} .ctile span{display:grid;place-items:center;width:58px;height:58px;border-radius:50%;margin:0 auto 8px}
.ctile p{font-size:.84rem;font-weight:500;line-height:1.25;color:var(--ink)}
.disc-sec .wpills ul{justify-content:flex-start}
.disc-sec .wpills{margin-top:0}
.trans{max-width:92ch;color:var(--ink);font-size:1.05rem;margin:34px 0 22px}
.grid8{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:26px 28px}
.grid8 li{border-top:2px solid #E0B43A;padding-top:12px;display:flex;flex-direction:column;gap:3px}
.sn8{font:300 2.3rem/1 var(--title);color:var(--gold-txt);margin-bottom:6px}
.ph8{font:700 .68rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.grid8 b{font:700 1.05rem/1.2 var(--title)} .sd8{font-size:.92rem;color:var(--muted)}
.wrap.narrow{max-width:980px}
.ex3s{display:grid;grid-template-columns:repeat(3,1fr);gap:34px;max-width:980px;margin:0 auto}
.ex3{text-align:center}
.ex3i{display:grid;place-items:center;width:62px;height:62px;border-radius:50%;margin:0 auto 10px}
.ex3 h4{font:700 1.1rem var(--title);margin-bottom:8px}
.ex3 p{font-size:.93rem;color:var(--ink);padding:9px 0;border-top:1px solid #E6E8EC}
.teach2{max-width:760px;margin:34px auto 0;text-align:center;font-size:.95rem;color:var(--muted);padding:16px 0;border-top:2px dotted #E0B43A;border-bottom:2px dotted #E0B43A}
.teach2 b{display:block;font:700 .74rem var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--gold-txt);margin-bottom:4px}
/* passe « site » */
.sec-head.full p{max-width:92ch}
h3.sub.c{text-align:left;margin:44px 0 16px;font-size:1.3rem}
.c-lead,.c-lead.gl{text-align:left}
.gap-lead{text-align:left}
.regard{background:transparent;border-top:0;text-align:left;padding:0;display:block}
.regard .med{width:104px;margin:0 0 12px}
.regard h4{margin-bottom:4px}
.crea{background:transparent;padding:0}
.cico{background:var(--card)}
.x-concl,.teach2{text-align:left;margin-left:0;max-width:92ch;padding-left:0}
.wpills ul{justify-content:flex-start}
.example .hypo{background:#fff}
#rainette .example{padding-top:0}
section{padding-block:72px}
.laters{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.later{display:grid;grid-template-columns:70px 1fr;gap:14px;align-items:center;background:#fff;border-radius:16px;padding:12px 16px}
.later .med{display:block;width:70px} .later .med svg{display:block;width:100%;height:auto;opacity:.9}
.later b{display:block;font:700 1.05rem var(--title)}
.later .lc{font:700 .68rem var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--c)}
.later span.ld{font-size:.88rem;color:var(--muted)}
/* fonds alternés */
.bg-white{background:#fff}
.bg-cool{background:#E9F6FF}
.bg-warm{background:#FFEDE5}
.bg-warm .pitem{background:#fff}
.bg-lilac{background:#F1ECFF}
.bg-rose{background:#FFEEF4}
.bg-white .steps6 li{background:var(--card);border-color:transparent}
/* principe */
.steps4{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.steps4 div{background:var(--card);border-radius:16px;padding:24px 22px;position:relative}
.steps4 .n{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;border:2.5px solid var(--ink);font:700 1.6rem/1 var(--title);color:var(--ink);background:var(--nc)}
.steps4 div:nth-child(1){--nc:#F7D117} .steps4 div:nth-child(2){--nc:#FF8A5C} .steps4 div:nth-child(3){--nc:#6CC4FF} .steps4 div:nth-child(4){--nc:#5FD18A}
.steps4 h3{font-size:1.3rem;margin:10px 0 8px}
.steps4 p{font-size:.95rem;color:var(--muted)}
/* cartes */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:24px}
.card{border-radius:18px;background:#fff;border:1px solid var(--line);overflow:hidden;display:flex;flex-direction:column}
.ill{background:var(--pale);padding:22px 0 18px;position:relative;display:grid;place-items:center}
.ill svg{width:170px;height:170px;filter:drop-shadow(0 8px 14px rgba(20,20,40,.16))}
.per{position:absolute;top:14px;right:14px;font:700 .7rem var(--body);letter-spacing:.08em;text-transform:uppercase;padding:4px 11px;border-radius:99px;background:#F7D117;color:var(--ink);border:2px solid var(--ink)}
.per.nuit{background:#3B3FB8;color:#fff} .per.crep{background:#FF8A5C;color:var(--ink)} .per.orient{background:#5ED0E6}
.card .body{padding:20px 22px 22px;display:flex;flex-direction:column;gap:12px;flex:1}
.card h3{font-size:1.45rem}
.trait{color:var(--muted);font-size:.96rem}
dl{display:grid;grid-template-columns:88px 1fr;gap:6px 12px;font-size:.9rem;border-top:1px solid var(--line);padding-top:12px}
dt{font-weight:700;color:var(--c)} .ref{font-size:.78rem;color:var(--muted);background:var(--card);border-radius:6px;padding:1px 6px;margin-left:2px;white-space:nowrap}
.q{font-style:italic}
/* observatoire */
.obs{}
.frise{position:relative;height:190px;border-radius:18px;overflow:hidden;background:linear-gradient(90deg,#2B36A8 0%,#3F4FC8 17%,#FFB36B 26%,#FFE08A 31%,#8FD6FF 38%,#CFEFFF 50%,#8FD6FF 62%,#FFB36B 71%,#B77CE8 78%,#3F4FC8 88%,#2B36A8 100%)}
.frise .med{position:absolute;top:50%;width:92px;transform:translate(-50%,-50%);border-radius:50%;box-shadow:0 6px 16px rgba(0,0,0,.25)}
.frise .med svg{display:block;width:100%;height:auto}
.frise-axis{display:flex;justify-content:space-between;font:500 .8rem var(--body);color:var(--muted);margin-top:8px;padding-inline:4px}
.frise-note{font-size:.9rem;color:var(--muted);margin-top:12px}
.steps6{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px;counter-reset:s;list-style:none}
.steps6 li{background:#fff;border-radius:14px;padding:18px 18px 18px 70px;position:relative;counter-increment:s;border:1px solid var(--line)}
.steps6 li::before{content:counter(s);position:absolute;left:18px;top:18px;width:36px;height:36px;border-radius:50%;background:var(--sc,var(--gold));border:2px solid var(--ink);display:grid;place-items:center;font:700 1.1rem var(--title)}
.steps6 li:nth-child(1){--sc:#F7D117} .steps6 li:nth-child(2){--sc:#FF8A5C} .steps6 li:nth-child(3){--sc:#FF9FC8} .steps6 li:nth-child(4){--sc:#6CC4FF} .steps6 li:nth-child(5){--sc:#5FD18A} .steps6 li:nth-child(6){--sc:#B89CFF}
.steps6 h4{font-size:1.1rem;margin-bottom:4px} .steps6 p{font-size:.9rem;color:var(--muted)}
.example{display:grid;grid-template-columns:auto 1fr;gap:28px;background:transparent;padding-left:0!important;border-radius:20px;padding:28px 30px;align-items:start}
.example .med{width:120px;display:block} .example .med svg{display:block;width:100%;height:auto}
.example h3.exq{font-size:1.35rem;margin:6px 0 16px}
.example dl{grid-template-columns:120px 1fr;border:0;padding:0;font-size:.95rem;--c:#2F8FE0;row-gap:10px}
.example .hypo{background:#fff}
.hypo{margin-top:16px;background:var(--card);border-radius:12px;padding:12px 14px;max-width:560px}
.hypo svg{width:100%;height:auto;display:block} .hypo p{font-size:.8rem;font-style:italic;color:var(--muted);margin-top:4px}
/* fabrication */
.fab{}
.fab-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:start}
.fab-grid>div{background:#fff;border-radius:16px;padding:24px;border:1px solid var(--line)}
.fab-grid h3{font-size:1.25rem;margin-bottom:10px}
.fab-grid ul{padding-left:18px;display:grid;gap:6px;font-size:.93rem}
.fab-grid svg{width:100%;height:auto;display:block;margin:6px 0 10px}
.fab-grid p{font-size:.92rem;color:var(--muted)}
.fab-grid .todo{border:2.5px solid var(--ink)}

.prog{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;align-items:start}
.pcol h3{font-size:1.6rem;padding-bottom:8px;border-bottom:3px solid var(--gold);margin-bottom:14px}
.pitem{background:var(--card);border-radius:14px;padding:14px 16px;margin-bottom:12px}
.pitem .dom{font:700 .74rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--gold-txt)}
.pitem blockquote{font-style:italic;font-size:.88rem;color:var(--muted);margin:6px 0 8px;line-height:1.45}
.pitem .link{font-size:.92rem;font-weight:500}
.fab-two{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.fab-two>div{background:#fff;border-radius:16px;padding:22px 24px;border:1px solid var(--line)}
.fab-two h3{font-size:1.3rem;margin-bottom:6px} .fab-two p{color:var(--muted);font-size:.95rem}
.assembly{margin-top:26px;background:#fff;border-radius:18px;border:1px solid var(--line);padding:24px}
.asm-grid{display:grid;grid-template-columns:1.7fr 1fr;gap:24px;align-items:center}
.asm-svg svg{width:100%;height:auto;display:block}
.asm-side .med{display:block;width:150px;margin-bottom:10px} .asm-side .med svg{display:block;width:100%;height:auto}
.asm-side ol{padding-left:22px;display:grid;gap:5px;font-size:.92rem;margin-top:8px}
.assembly figcaption{margin-top:14px;font-size:.88rem;color:var(--muted);font-style:italic}
footer{background:var(--ink);color:#fff;padding-block:30px;font-size:.88rem}
footer .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
footer b{color:var(--gold)} footer small{color:#B9BEC2;display:block;margin-top:4px}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
@media (max-width:980px){.laters{grid-template-columns:1fr} .ex3s{grid-template-columns:1fr} .grid8{grid-template-columns:1fr 1fr} .ctiles{grid-template-columns:repeat(4,1fr)} .ms-top,.mgs{grid-template-columns:1fr} .ms-board{max-width:200px;margin:0 auto} .xband{margin-inline:0;padding-inline:16px} .phases{grid-template-columns:1fr 1fr} .phases::before{display:none} .gaps{grid-template-columns:1fr} .regards,.steps8{grid-template-columns:1fr 1fr} .creas{grid-template-columns:1fr 1fr} .x-foot{grid-template-columns:1fr} .x-top,.x-cards{grid-template-columns:1fr} .cross-top{grid-template-columns:1fr} .disc-wrap .disc{grid-template-columns:1fr 1fr} .qgrid{grid-template-columns:1fr 1fr} .t-join::before{display:none} .t-branches{grid-template-columns:1fr} .t-branches::after{display:none} .cross,.modes-disc{grid-template-columns:1fr} .sens-grid{grid-template-columns:1fr} .prog2{grid-template-columns:1fr} .prog,.asm-grid,.fab-two{grid-template-columns:1fr} nav ul{display:none} .hero .wrap{grid-template-columns:1fr} .steps4{grid-template-columns:1fr 1fr} .fab-grid,.steps6{grid-template-columns:1fr} .frise .med{width:62px}}
@media (max-width:620px){.grid8{grid-template-columns:1fr} .phases{grid-template-columns:1fr} .regards,.steps8{grid-template-columns:1fr} .creas{grid-template-columns:1fr} .qgrid{grid-template-columns:1fr} .wrap{padding-inline:16px} section{padding-block:52px} .steps4{grid-template-columns:1fr} .example{grid-template-columns:1fr} .example dl{grid-template-columns:1fr} .frise{height:130px} .frise .med{width:40px}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
hypo=f'''<svg viewBox="0 0 420 150" role="img" aria-label="Allure attendue selon l’hypothèse : humidité plus forte la nuit, plus faible le jour">
<rect x="30" y="8" width="96" height="112" fill="#1F2455" opacity=".13"/><rect x="324" y="8" width="90" height="112" fill="#1F2455" opacity=".13"/>
<line x1="30" y1="120" x2="414" y2="120" stroke="#1A1A1A" stroke-width="1.4"/><line x1="30" y1="8" x2="30" y2="120" stroke="#1A1A1A" stroke-width="1.4"/>
<path d="M30 38 C86 34 118 40 150 70 C190 104 262 106 296 74 C318 52 340 40 414 38" fill="none" stroke="#7B55D6" stroke-width="3" stroke-dasharray="7 5"/>
<g font-family="Roboto,sans-serif" font-size="11" fill="#4D5358"><text x="78" y="138" text-anchor="middle">nuit</text><text x="225" y="138" text-anchor="middle">jour</text><text x="369" y="138" text-anchor="middle">nuit</text><text x="22" y="64" text-anchor="middle" transform="rotate(-90 22 64)">humidité</text></g></svg>'''
fix='''<svg viewBox="0 0 320 150" role="img" aria-label="Coupe : la batterie traverse l’ouverture de la plaque en bois, la carte repose sur le rebord et un verrou la maintient">
<rect x="16" y="72" width="288" height="14" fill="#D9BC8E" stroke="#1A1A1A" stroke-width="1.4"/><rect x="104" y="72" width="112" height="14" fill="#fff"/>
<rect x="70" y="62" width="180" height="7" fill="#1A1A1A"/><rect x="118" y="69" width="84" height="42" rx="5" fill="#3AA5A0"/>
<rect x="244" y="54" width="40" height="7" fill="#EBD2A8" stroke="#1A1A1A" stroke-width="1.2"/><line x1="264" y1="44" x2="264" y2="96" stroke="#1A1A1A" stroke-width="2.2"/>
<g font-family="Roboto,sans-serif" font-size="11" fill="#1A1A1A"><text x="70" y="54">carte STeaMi</text><text x="160" y="130" text-anchor="middle">batterie, à travers la plaque</text><text x="16" y="104">plaque en bois</text><text x="246" y="38">verrou</text></g></svg>'''

html=f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bestiaire STeaMi</title>
<meta name="description" content="Des animaux-sentinelles qui embarquent une carte STeaMi pour observer le vivant et mesurer nos conditions de vie.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@300;400;600;700&family=Roboto:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>
<span id="top"></span>
<nav><div class="wrap"><a class="brand" href="#top">{logo(36)}Bestiaire <b>STeaMi</b></a>
<ul><li><a href="#croisees">Comprendre et mesurer</a></li><li><a href="#exemples">Exemples</a></li><li><a href="#sentinelles">Sentinelles</a></li><li><a href="#observatoire">Observatoire</a></li><li><a href="#mesurer">Mesurer</a></li><li><a href="#programme">Programme</a></li><li><a href="#creativite">Créativité</a></li><li><a href="#fabrication">Fabrication</a></li></ul></div></nav>

<header class="hero"><div class="wrap">
<p class="kicker hk">Observer le vivant, mesurer l’environnement, comparer nos perceptions</p>
<div>
<h1>Le Bestiaire <b>STeaMi</b></h1>
<p class="lede">Et si les comportements des animaux nous aidaient à mieux comprendre nos propres conditions de vie ?</p>
<p class="txt">Le Bestiaire STeaMi est un projet scientifique et créatif dédié à la découverte des cartes programmables au cycle 3. Il prend appui sur les comportements et les adaptations des animaux pour amener les élèves à observer leur environnement, puis à en mesurer certaines caractéristiques avec les capteurs de la carte STeaMi.</p>
<div class="facts"><span>Cycle 3</span><span>Projet interdisciplinaire entre les sciences, les arts et la technologie</span><span>Démarche d’investigation et approche scientifique</span></div>
</div>
<div class="cluster" aria-hidden="true">{med('chouette','m1')}{med('abeille','m2')}{med('fennec','m3')}{med('rainette','m4')}{med('tortue','m5')}{med('chat','m6')}{med('chauvesouris','m7')}</div>
</div></header>

<section id="croisees" class="bg-white"><div class="wrap">
<div class="sec-head full"><p class="kicker">Comprendre et mesurer</p><h2>Le vivant, sentinelle <b>de nos conditions de vie</b></h2><hr class="rule">
<p>Le Bestiaire s’appuie sur une idée centrale : les comportements des animaux rendent visibles certaines caractéristiques de leur milieu. Leur activité, leurs déplacements ou leurs choix d’habitat donnent des indices sur la lumière, l’humidité, la température, le bruit ou les changements météorologiques.</p>
<p>Les élèves partiront de ces indices pour observer leur propre environnement. Ils décriront ce qu’ils perçoivent, formuleront des hypothèses, puis utiliseront les capteurs de la STeaMi pour mesurer les grandeurs concernées. Il ne s’agira pas de faire croire que la carte perçoit le monde comme un animal, mais de confronter trois lectures complémentaires d’une même situation.</p></div>
<h3 class="sub c">Trois regards sur un même environnement</h3>
{regards_html()}
<p class="c-lead gl">C’est en comparant ces trois regards que naissent les questions à explorer avec les élèves.</p>
<div class="gaps">
<div class="gap" style="--g:#ECE4FF;--gi:#7B55D6"><svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><path d="M26 6 A15 15 0 1 0 34 28 A12 12 0 1 1 26 6 Z" fill="#7B55D6"/></svg><p>La chouette sort à la tombée de la nuit : à quel moment la cour devient-elle aussi sombre qu’elle le recherche ?</p></div>
<div class="gap" style="--g:#FFF4C7;--gi:#B98A1E"><svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><rect x="16" y="4" width="8" height="22" rx="4" fill="#B98A1E"/><circle cx="20" cy="30" r="7" fill="#B98A1E"/></svg><p>Le crocodile se déplace vers l’ombre quand il a trop chaud : les coins ombragés de la cour sont-ils vraiment plus frais ?</p></div>
<div class="gap" style="--g:#FFE6D9;--gi:#E8703A"><svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><circle cx="14" cy="22" r="7" fill="#E8703A"/><path d="M25 14 q5 8 0 16 M30 9 q9 13 0 26" fill="none" stroke="#E8703A" stroke-width="3" stroke-linecap="round"/></svg><p>Le fennec entend les sons les plus faibles : les moments qui nous semblent calmes le sont-ils aussi pour lui ?</p></div>
</div>




</div></section>

<section id="exemples" class="sec-dark"><div class="wrap">
<div class="sec-head full"><p class="kicker">Exemples d’investigation</p><h2>Du vivant <b>jusqu’à nous</b></h2><hr class="rule">
<p>Les mesures donneront aux élèves de quoi agir : réduire un éclairage inutile, identifier un espace trop bruyant ou proposer davantage d’ombre dans la cour. Le Bestiaire fera ainsi de la mesure un outil pour comprendre l’école, argumenter des choix et imaginer des améliorations concrètes.</p></div>
<div class="x-cards">{ex_cards()}</div>
</div></section>

<section id="disciplines" class="bg-white disc-sec"><div class="wrap"><div class="sec-head full"><p class="kicker">Interdisciplinarité</p><h2>Disciplines <b>mobilisées</b></h2><hr class="rule"></div><div class="wpills"><ul>{''.join(f'<li><b>{d}</b> · {x}</li>' for d,x in DISC)}</ul></div></div></section>





<section id="sentinelles" class="bg-cool"><div class="wrap">
<div class="sec-head full"><p class="kicker">Les sentinelles</p><h2>Six animaux <b>pour commencer</b></h2><hr class="rule">
<p>Six animaux composeront la première vague du Bestiaire. Chacun ouvrira une porte d’entrée vers une question d’étude correspondant au programme du cycle 3 : voir dans la pénombre, percevoir un son faible, distinguer des couleurs, rechercher l’humidité, réguler sa température ou estimer une distance.</p><p>Pour les enfants, les animaux donneront un visage et une histoire à des grandeurs parfois abstraites. Plutôt que de découvrir une simple liste de capteurs, ils suivront neuf manières de percevoir le monde, choisiront leur sentinelle et chercheront à comprendre ce qu’elle révèle de leur propre environnement. Cette approche favorisera la curiosité, la mémorisation et l’envie d’expérimenter.</p></div>
<div class="cards">{''.join(card(a) for a in A if a[0] in CORE)}</div>
<h3 class="sub c">D’autres animaux pourront rejoindre le bestiaire</h3>
<div class="cards">{''.join(card(a) for a in A if a[0] not in CORE)}</div>
</div></section>

<section class="obs bg-white" id="observatoire"><div class="wrap">
<div class="sec-head full"><p class="kicker">L’observatoire</p><h2>Observer <b>jour et nuit</b></h2><hr class="rule">
<p>Une fois les premières sentinelles réalisées, plusieurs dispositifs pourront être répartis dans l’établissement ou installés sous des abris adaptés. Ils formeront un petit observatoire de la lumière, de la température, de l’humidité et du bruit.</p><p>Les élèves passeront alors d’une mesure ponctuelle à une comparaison dans le temps et dans l’espace. Ils superposeront les courbes, compareront les lieux et rechercheront des régularités sur une journée, plusieurs nuits ou différentes saisons.</p></div><p class="ctx-lead">Ils découvriront qu’une donnée n’a de sens que si son contexte est connu :</p><div class="ctiles"><div class="ctile"><span style="background:#DDEEFF"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path d="M16 4a9 9 0 0 1 9 9c0 7-9 15-9 15S7 20 7 13a9 9 0 0 1 9-9z" fill="#2F8FE0"/><circle cx="16" cy="13" r="3.5" fill="#fff"/></svg></span><p>Emplacement de la carte</p></div><div class="ctile"><span style="background:#FFE6D9"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><circle cx="16" cy="16" r="11" fill="#E8703A"/><path d="M16 9v7l5 3" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg></span><p>Heure de la mesure</p></div><div class="ctile"><span style="background:#FFF4C7"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><circle cx="16" cy="16" r="6" fill="#B98A1E"/><g stroke="#B98A1E" stroke-width="2.6" stroke-linecap="round"><path d="M16 3v4M16 25v4M3 16h4M25 16h4M7 7l3 3M22 22l3 3M25 7l-3 3M10 22l-3 3"/></g></svg></span><p>Exposition au soleil</p></div><div class="ctile"><span style="background:#ECE4FF"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><g fill="#7B55D6"><rect x="4" y="8" width="11" height="6" rx="1"/><rect x="17" y="8" width="11" height="6" rx="1"/><rect x="4" y="16" width="5" height="6" rx="1"/><rect x="11" y="16" width="11" height="6" rx="1"/><rect x="24" y="16" width="4" height="6" rx="1"/><rect x="4" y="24" width="11" height="4" rx="1"/><rect x="17" y="24" width="11" height="4" rx="1"/></g></svg></span><p>Présence d’un mur</p></div><div class="ctile"><span style="background:#DDEEFF"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path d="M9 24a6 6 0 0 1 0-12 8 8 0 0 1 15 2 5 5 0 0 1 0 10z" fill="#2F8FE0"/></svg></span><p>Météo</p></div><div class="ctile"><span style="background:#FFE6D9"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><circle cx="11" cy="11" r="4" fill="#E8703A"/><circle cx="21" cy="11" r="4" fill="#E8703A"/><path d="M4 26a7 7 0 0 1 14 0zM14 26a7 7 0 0 1 14 0z" fill="#E8703A"/></svg></span><p>Activité humaine</p></div><div class="ctile"><span style="background:#ECE4FF"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path d="M16 4l3.6 7.4 8.1 1.2-5.9 5.7 1.4 8.1L16 22.6l-7.2 3.8 1.4-8.1-5.9-5.7 8.1-1.2z" fill="#7B55D6"/></svg></span><p>Événement particulier</p></div></div>
<div class="frise" role="img" aria-label="Frise de 24 heures : chouette, rainette et tortue la nuit, abeille, crocodile et martinet le jour, chat au crépuscule, chauve-souris et fennec la nuit">{''.join(f'<span class="med" style="left:{x}%">{I[k]}</span>' for k,x in FRISE)}</div>
<div class="frise-axis"><span>minuit</span><span>6 h</span><span>midi</span><span>18 h</span><span>minuit</span></div>
<p class="trans">Que les sentinelles soient utilisées seules ou en réseau, chaque investigation suivra la même progression, de l’observation du vivant jusqu’à une proposition pour l’école :</p>
{steps_grid()}
</div></section>

<section id="rainette" class="bg-cool"><div class="wrap">
<div class="sec-head full"><p class="kicker">La démarche en pratique</p><h2>L’exemple <b>de la rainette</b></h2><hr class="rule">
<p>Appliquée à la rainette, la progression commune prend cette forme :</p></div>
<div class="example"><span class="med">{I['rainette']}</span>
<div><h3 class="exq">Pourquoi la rainette est-elle active la nuit ?</h3>
<dl><dt>Hypothèse</dt><dd>L’air est plus humide la nuit, ce qui limite le dessèchement de sa peau.</dd>
<dt>Protocole</dt><dd>Une sentinelle rainette et une sentinelle chouette au même endroit, une mesure toutes les 5 minutes pendant 48 heures ; une seconde rainette placée ailleurs comme témoin.</dd>
<dt>Préalable</dt><dd>Les sentinelles posées côte à côte pendant une heure, pour comparer leurs mesures avant de les disperser.</dd>
<dt>Analyse</dt><dd>La courbe de lumière délimite le jour et la nuit sur la courbe d’humidité ; on compare avec le témoin.</dd></dl>
<div class="hypo">{hypo}<p>Allure attendue si l’hypothèse est juste, sans valeurs : ce sont les mesures qui trancheront.</p></div></div></div>
</div></section>

<section id="mesurer" class="bg-white"><div class="wrap">
<div class="sec-head"><p class="kicker">L’ExAO au cycle 3</p><h2>Mesurer, enregistrer, <b>comparer</b></h2><hr class="rule">
<p>Le Bestiaire introduit l’expérimentation avec des capteurs à partir d’actions concrètes. Les élèves ne se contentent pas d’observer : ils utilisent la STeaMi pour mesurer une grandeur, conserver les résultats et mettre leurs hypothèses à l’épreuve.</p>
<p>La carte relève automatiquement la lumière, la température, l’humidité, le niveau sonore ou le mouvement. Elle produit des séries de données que la classe organise dans des tableaux et représente sous forme de graphiques.</p></div>
<h3 class="sub c">Au fil du projet, les élèves apprennent à…</h3>
<div class="ex3s"><div class="ex3"><span class="ex3i" style="background:#DDEEFF"><svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><circle cx="20" cy="20" r="12" fill="none" stroke="#2F8FE0" stroke-width="3"/><path d="M20 12v8l6 4" stroke="#2F8FE0" stroke-width="3" fill="none" stroke-linecap="round"/></svg></span><h4 style="color:#2F8FE0">Préparer la mesure</h4><p>identifier ce qui peut réellement être mesuré</p><p>choisir une fréquence et une durée d’acquisition</p><p>programmer une boucle de mesure</p></div><div class="ex3"><span class="ex3i" style="background:#FFE6D9"><svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><rect x="9" y="8" width="22" height="24" rx="4" fill="#E8703A"/><path d="M13 24l4-5 4 3 6-8" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span><h4 style="color:#E8703A">Mesurer et enregistrer</h4><p>enregistrer des données horodatées</p><p>comparer plusieurs cartes</p><p>utiliser un témoin et répéter une expérience</p></div><div class="ex3"><span class="ex3i" style="background:#ECE4FF"><svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><circle cx="18" cy="18" r="9" fill="none" stroke="#7B55D6" stroke-width="3"/><path d="M25 25l7 7" stroke="#7B55D6" stroke-width="3.4" stroke-linecap="round"/></svg></span><h4 style="color:#7B55D6">Interpréter</h4><p>reconnaître la variabilité des mesures</p><p>lire une série temporelle</p><p>distinguer une observation, un résultat et une interprétation</p><p>expliquer les limites d’un capteur</p></div></div>
<p class="teach2"><b>Pour l’enseignant·e</b> Cette démarche relève de l’ExAO, l’expérimentation assistée par ordinateur. Le Bestiaire en propose une première approche adaptée au cycle 3, à partir d’activités proches du quotidien des élèves.</p>
</div></section>

<section id="programme" class="bg-warm"><div class="wrap">
<div class="sec-head"><p class="kicker">Programme de cycle 3</p><h2>Ancrage dans <b>le programme</b></h2><hr class="rule">
<p>Le bestiaire s’appuie sur le programme de sciences et technologie du cycle 3 (BO n° 24 du 11 juin 2026).</p></div>
<div class="prog2">{''.join(f'<div class="pcard" style="--pc:{col}"><div class="phead"><span>{cl}</span></div><ul>'+''.join(f'<li><span class="pm">'+''.join(med(k) for k in ks)+f'</span><div><b>{n}</b><span>{d}</span></div></li>' for n,d,ks in items)+'</ul></div>' for cl,(col,items) in PROG2.items())}</div>
<details class="official"><summary>Voir les objectifs officiels cités</summary>
<div class="prog">{''.join(f'<div class="pcol"><h3>{cl}</h3>'+''.join(f'<article class="pitem"><p class="dom">{d}</p><blockquote>« {q} »</blockquote></article>' for d,q,l in items)+'</div>' for cl,items in PROG.items())}</div></details>
</div></section>

<section id="creativite" class="bg-white"><div class="wrap">
<div class="sec-head full"><p class="kicker">Créativité et arts plastiques</p><h2>Donner vie <b>à sa sentinelle</b></h2><hr class="rule">
<p>Chaque sentinelle est aussi une création. Les élèves imaginent le caractère de leur animal, en dessinent la silhouette et les motifs, et lui donnent des réactions : une expression, un mouvement, un son, une couleur. Le projet mobilise les arts plastiques autant que la technologie et la programmation.</p></div>
{crea_html()}
</div></section>

<section class="fab bg-sun" id="fabrication"><div class="wrap">
<div class="sec-head full"><p class="kicker">Fabrication</p><h2>Concevoir et <b>fabriquer sa sentinelle</b></h2><hr class="rule">
<p>La sentinelle est un objet technique que les élèves conçoivent et fabriquent, en réponse directe au <a class="inl" href="#programme">programme de cycle 3</a>. En CM1, ils en identifient les sous-ensembles et en décrivent le fonctionnement par un croquis légendé. En CM2, ils mènent la démarche de conception d’une maquette : rechercher des idées de solutions à l’aide de croquis, associer une contrainte à un choix de matériau, organiser le travail et fabriquer. Deux niveaux sont possibles : un assemblage simple réalisé en classe, dans le matériau de son choix, ou une fabrication menée avec un fablab partenaire, qui ajoute une étape de conception.</p></div>
<div class="fab-two">
<div><h3>En classe</h3><p>Des pièces simples (carton, bois, matériaux de récupération…), tracées, découpées et assemblées par les élèves. La carte se loge dans le dos de l’animal, sans colle.</p></div>
<div><h3>Avec un fablab</h3><p>Les élèves dessinent la silhouette et les motifs de leur animal ; le fablab les découpe, par exemple au laser. Les élèves comparent ensuite les solutions obtenues.</p></div>
</div>
<figure class="assembly"><div class="asm-grid"><div class="asm-svg">{ASSEMBLY}</div>
<div class="asm-side"><span class="med">{I['chouette']}</span><p class="kicker">Une fois assemblée</p>
<ol>{''.join(f'<li><b>{t}</b> : {d}</li>' for t,d in ASSEMBLY_LEGEND)}</ol></div></div>
<figcaption>Vue éclatée de la sentinelle chouette. La batterie, au dos de la carte, traverse l’ouverture du dos : la carte reste à plat et la façade la maintient.</figcaption></figure>
</div></section>

<footer><div class="wrap"><div><b>STeaMi</b> · Code. Communicate. Create.<small>Positions des capteurs : fichiers de fabrication du dépôt steami-reference-design.</small></div><div>Bestiaire STeaMi · L.A.B · I-NOVMICRO</div></div></footer>
<a class="totop" href="#top" aria-label="Retour en haut de page"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 5 L5 12 M12 5 L19 12 M12 5 V20" fill="none" stroke="#1A1A1A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
<script>(function(){{var b=document.querySelector('.totop');function f(){{b.classList.toggle('show',window.scrollY>500)}}window.addEventListener('scroll',f,{{passive:true}});f();b.addEventListener('click',function(e){{e.preventDefault();var r=window.matchMedia('(prefers-reduced-motion: reduce)').matches;window.scrollTo({{top:0,behavior:r?'auto':'smooth'}});history.replaceState(null,'',location.pathname);}});}})();</script>
</body></html>'''
open('/home/manon/Documents/09_Inovmicro/01_STeaMi_Ressources_pedagogiques/Bestiaire/bestiaire-steami-presentation.html','w').write(html)
print(len(html))

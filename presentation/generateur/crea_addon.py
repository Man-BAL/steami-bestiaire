def owl_variant(kind,uid):
    base=face(100,80,26,'owl','#EFDDBF'); svg=I['chouette']
    return svg.replace(base,face(100,80,26,kind,'#EFDDBF')).replace('c-chouette',f'c-chouette-{uid}').replace('g-chouette',f'g-chouette-{uid}')
OWLS=[('owl','Aux aguets'),('arc','Contente'),('closed','Endormie'),('heart','Conquise')]
def crea_icon(kind):
    I2={'face':'<circle cx="32" cy="32" r="24" fill="#101214"/><circle cx="32" cy="32" r="27" fill="none" stroke="#E9ECEE" stroke-width="4"/><path d="M19 34 a5.5 5.5 0 0 1 11 0 M34 34 a5.5 5.5 0 0 1 11 0" fill="none" stroke="#F7D117" stroke-width="3.2"/>',
        'move':'<path d="M32 44 L12 20 Q18 36 10 46 Q22 44 26 52 Z" fill="#7B55D6"/><path d="M32 44 L52 20 Q46 36 54 46 Q42 44 38 52 Z" fill="#7B55D6"/><circle cx="32" cy="44" r="7" fill="#E8703A"/><path d="M6 14 q4 -6 10 -6 M58 14 q-4 -6 -10 -6" fill="none" stroke="#1A1A1A" stroke-width="2.5" stroke-linecap="round"/>',
        'sound':'<circle cx="24" cy="36" r="12" fill="#FF8A5C"/><path d="M40 24 q8 12 0 24 M46 18 q13 18 0 36" fill="none" stroke="#FF8A5C" stroke-width="3.5" stroke-linecap="round"/><circle cx="24" cy="36" r="5" fill="#fff"/>',
        'pattern':'<rect x="8" y="8" width="22" height="22" rx="5" fill="#E6C593"/><path d="M11 20 l4 4 l4 -4 l4 4 l4 -4" fill="none" stroke="#9A6A36" stroke-width="2"/><rect x="34" y="8" width="22" height="22" rx="5" fill="#A9D8FF"/><g fill="#2F8FE0"><circle cx="41" cy="15" r="3"/><circle cx="49" cy="22" r="3"/></g><rect x="8" y="34" width="22" height="22" rx="5" fill="#F2C38B"/><path d="M12 40 q7 6 14 0 M12 48 q7 6 14 0" fill="none" stroke="#C88B47" stroke-width="2"/><rect x="34" y="34" width="22" height="22" rx="5" fill="#B77CE8"/><g fill="#fff" opacity=".8"><circle cx="40" cy="40" r="1.8"/><circle cx="48" cy="45" r="1.8"/><circle cx="42" cy="50" r="1.8"/></g>'}
    return f'<svg viewBox="0 0 64 64" width="56" height="56" aria-hidden="true">{I2[kind]}</svg>'
CREA=[('face','Un visage expressif','L’écran rond affiche des yeux et des expressions, que les élèves dessinent pixel par pixel et font changer selon la mesure.'),
      ('move','Des mouvements','Un petit servomoteur fait battre des ailes, dresser des oreilles ou tourner une tête lorsque la sentinelle détecte quelque chose.'),
      ('sound','Des sons et des lumières','Le buzzer et la LED de la carte donnent une voix et une couleur à l’animal : un cri, un signal, une couleur qui change.'),
      ('pattern','Motifs et matières','Plumes, écailles, pelage : dessinés, peints, gravés ou collés, dans les matériaux choisis par la classe.')]
def crea_html():
    owls=''.join(f'<figure class="owlv"><span class="med">{owl_variant(k,i)}</span><figcaption>{lab}</figcaption></figure>' for i,(k,lab) in enumerate(OWLS))
    cards=''.join(f'<article class="crea"><span class="cico">{crea_icon(k)}</span><h3>{t}</h3><p>{d}</p></article>' for k,t,d in CREA)
    return f'<div class="owls">{owls}</div><div class="creas">{cards}</div>'

# capteurs intégrés de la STeaMi (positions : fichiers de fabrication, vue de face, mm, y vers le haut)
SENS={ # clé : (couleur, fond pâle, nom, référence, face, x, y) — palette jaune, pêche, violet, bleu
 'lum': ('#E8703A','#FFE6D9','Lumière et couleur','APDS-9960','avant',13.3,18.61),
 'pres':('#2F8FE0','#DDEEFF','Pression','WSEN-PADS','avant',18.96,12.31),
 'dist':('#2F8FE0','#DDEEFF','Distance','VL53L1X','avant',21.75,7.37),
 'mic': ('#B98A1E','#FFF4C7','Microphone','IMP34DT05','avant',16.02,-20.38),
 'hts': ('#7B55D6','#ECE4FF','Température et humidité','WSEN-HIDS','dos',0,-22),
 'imu': ('#B98A1E','#FFF4C7','Accéléromètre et gyroscope','ISM330DL','dos',-2.5,0),
 'mag': ('#E8703A','#FFE6D9','Magnétomètre','LIS2MDL','dos',2.5,0),
}
USES={'lum':['abeille','chouette','tortue'],'pres':['martinet'],'dist':['chauvesouris'],'mic':['fennec'],'hts':['crocodile','rainette'],'imu':['chat'],'mag':['tortue']}
def board_view(face,k=3.0):
    import math
    Fx=lambda x,y:(round((x+30.55)*k,1) if face=='avant' else round((30.55-x)*k,1), round((30.65-y)*k,1))
    W,H=61.1*k,91.73*k
    tr='' if face=='avant' else f' transform="translate({W} 0) scale(-1 1)"'
    o=f'<g{tr}><path d="{OUTLINE}" transform="scale({k})" fill="#141414"/></g>'
    pads=[(26.31,9.58),(23.61,15.04),(19.80,19.80),(15.04,23.61)]; pads+=[(-x,y) for x,y in pads]
    o+=''.join(f'<circle cx="{Fx(x,y)[0]}" cy="{Fx(x,y)[1]}" r="{2.5*k}" fill="#E0B43A"/>' for x,y in pads)
    g0=Fx(-23.3 if face=='avant' else 23.3,-51.2); o+=f'<rect x="{g0[0]}" y="{g0[1]}" width="{46.6*k}" height="{9.9*k}" fill="#E0B43A"/>'
    if face=='avant':
        c=Fx(0,2.9); o+=f'<circle cx="{c[0]}" cy="{c[1]}" r="{21*k}" fill="#DADDE0"/><circle cx="{c[0]}" cy="{c[1]}" r="{18.6*k}" fill="#0B0B0B"/>'
        for s in (-1,1): o+=f'<path d="M{c[0]+s*20-9} {c[1]+2} a9 9 0 0 1 18 0" fill="none" stroke="#F7D117" stroke-width="5"/>'
        for x,y in ((-13.5,-40.5),(0,-40.5),(10.5,-40.5),(14.5,-36.5)): p=Fx(x,y); o+=f'<circle cx="{p[0]}" cy="{p[1]}" r="{2.6*k}" fill="#9AA3A8"/>'
    else:
        for x,y in ((8.7,-23.3),(-8.7,-23.3),(14.0,9.45),(-14.0,9.45)): p=Fx(x,y); o+=f'<circle cx="{p[0]}" cy="{p[1]}" r="{2.6*k}" fill="#B9C0C5"/>'
        p=Fx(0,-10.5); o+=f'<rect x="{p[0]-4.2*k}" y="{p[1]-4.2*k}" width="{8.4*k}" height="{8.4*k}" rx="4" fill="#3A3F44"/>'
    LAB={'lum':(12,40),'pres':(40,24),'dist':(42,6),'mic':(40,-24),'hts':(0,-36),'imu':(-24,14),'mag':(24,14)}
    for key,v in SENS.items():
        if v[4]!=face: continue
        p=Fx(v[5],v[6]); q=Fx(*LAB[key]); n=list(SENS).index(key)+1
        o+=f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{v[0]}" stroke-width="2.5"/><circle cx="{p[0]}" cy="{p[1]}" r="4.5" fill="{v[0]}" stroke="#fff" stroke-width="1.5"/>'
        o+=f'<circle cx="{q[0]}" cy="{q[1]}" r="14" fill="{v[0]}" stroke="#fff" stroke-width="3"/><text x="{q[0]}" y="{q[1]+5.5}" text-anchor="middle" font-family="League Spartan,sans-serif" font-weight="700" font-size="16" fill="#fff">{n}</text>'
    lab='face avant' if face=='avant' else 'dos'
    return f'<figure class="bview"><svg viewBox="-44 -40 {W+104} {H+56}" role="img" aria-label="Carte STeaMi, {lab}, avec l’emplacement des capteurs">{o}</svg><figcaption>{lab}</figcaption></figure>'
def sensor_card(key):
    c,pale,name,ref,face,x,y=SENS[key]; n=list(SENS).index(key)+1
    meds=''.join(med(a) for a in USES[key])
    return (f'<div class="scard2" style="--c:{c};--pale:{pale}"><span class="sn">{n}</span><div class="sbody"><b>{name}</b>'
            f'<span class="sref">{ref} · {"face avant" if face=="avant" else "au dos"}</span><em>Intégré à la STeaMi</em></div><span class="pm">{meds}</span></div>')

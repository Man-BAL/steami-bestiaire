# icônes des stations (dessinées dans un carré 0..48, couleur c)
def st_icon(key,c):
    W='#fff'
    I={
 'cit':f'<circle cx="16" cy="18" r="6" fill="{c}"/><circle cx="32" cy="18" r="6" fill="{c}"/><path d="M5 38 q11 -14 22 0 Z M21 38 q11 -14 22 0 Z" fill="{c}"/><rect x="30" y="4" width="4" height="8" fill="{c}"/><rect x="36" y="1" width="4" height="11" fill="{c}"/><rect x="42" y="6" width="4" height="6" fill="{c}"/>',
 'env':f'<path d="M24 4 C10 14 8 30 18 38 C26 44 38 38 38 26 C38 16 30 8 24 4 Z" fill="{c}"/><path d="M24 12 V42 M24 22 L18 17 M24 30 L31 24" stroke="{W}" stroke-width="2.6" stroke-linecap="round" fill="none"/>',
 'mob':f'<path d="M8 30 L12 20 Q13 17 17 17 H31 Q35 17 36 20 L40 30 V38 H8 Z" fill="{c}"/><rect x="15" y="21" width="18" height="7" rx="1.5" fill="{W}"/><circle cx="15" cy="38" r="4.5" fill="{c}" stroke="{W}" stroke-width="2"/><circle cx="33" cy="38" r="4.5" fill="{c}" stroke="{W}" stroke-width="2"/>',
 'ene':f'<path d="M6 24 L24 8 L42 24 V42 H6 Z" fill="{c}"/><path d="M26 16 L18 30 H24 L21 40 L31 25 H25 Z" fill="{W}"/>',
 'ia':f'<rect x="12" y="12" width="24" height="24" rx="4" fill="{c}"/><rect x="18" y="18" width="12" height="12" rx="2" fill="{W}"/><g stroke="{c}" stroke-width="3" stroke-linecap="round"><path d="M18 6 V12 M24 6 V12 M30 6 V12 M18 36 V42 M24 36 V42 M30 36 V42 M6 18 H12 M6 24 H12 M6 30 H12 M36 18 H42 M36 24 H42 M36 30 H42"/></g>',
    }[key]
    return I
def st_pin(key,c,pale):
    return (f'<svg class="stpin" viewBox="0 0 100 100" aria-hidden="true"><path d="M50 5 A45 45 0 1 0 95 50 L95 5 Z" fill="{pale}" stroke="{c}" stroke-width="8" stroke-linejoin="round"/>'
            f'<g transform="translate(26 26)">{st_icon(key,c)}</g></svg>')
def sensors_for(key):
    seen=[]; o=''
    for a in A:
        if a[8]!=key: continue
        name,ref=a[3],a[4]
        if (name,ref) in seen: continue
        seen.append((name,ref))
        o+=f'<div class="scap"><b>{name}</b><span>{ref}</span><em>Intégré à la STeaMi</em></div>'
    return o
def station_card(key,c,p,n):
    meds=''.join(med(a[0]) for a in A if a[8]==key)
    names=', '.join(a[1] for a in A if a[8]==key)
    return (f'<div class="st" style="--c:{c};--pale:{p}">{st_pin(key,c,p)}<h3>Station <b>{n}</b></h3>'
            f'<div class="meds">{meds}</div><p>{names}</p><div class="scaps"><p class="kicker">Capteurs utilisés</p>{sensors_for(key)}</div></div>')

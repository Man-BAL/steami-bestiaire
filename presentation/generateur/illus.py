import math
Y='#F7D117'
def face(cx,cy,r,kind='arc',ring='#E9ECEE'):
    o=f'<circle cx="{cx}" cy="{cy}" r="{r*1.16:.1f}" fill="{ring}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#101214"/>'
    e=r*0.36; rr=r*0.2; w=r*0.13; ey=cy+r*0.05
    if kind=='arc':
        for s in (-1,1): x=cx+s*e; o+=f'<path d="M{x-rr:.1f} {ey:.1f} A{rr:.1f} {rr:.1f} 0 0 1 {x+rr:.1f} {ey:.1f}" fill="none" stroke="{Y}" stroke-width="{w:.1f}"/>'
    elif kind=='owl':
        for s in (-1,1): x=cx+s*r*0.4; o+=f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="{r*0.3:.1f}" fill="{Y}"/><circle cx="{x:.1f}" cy="{cy:.1f}" r="{r*0.13:.1f}" fill="#101214"/>'
    elif kind=='arrow':
        o+=f'<path d="M{cx} {cy-r*0.62:.1f} l{r*0.34:.1f} {r*0.42:.1f} h{-r*0.2:.1f} v{r*0.6:.1f} h{-r*0.28:.1f} v{-r*0.6:.1f} h{-r*0.2:.1f} Z" fill="{Y}"/>'
    elif kind=='closed':
        for sg in (-1,1): x=cx+sg*e; o+=f'<path d="M{x-rr:.1f} {ey:.1f} A{rr:.1f} {rr:.1f} 0 0 0 {x+rr:.1f} {ey:.1f}" fill="none" stroke="{Y}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
    elif kind=='surprise':
        for sg in (-1,1): x=cx+sg*r*0.38; o+=f'<circle cx="{x:.1f}" cy="{cy-r*0.05:.1f}" r="{r*0.2:.1f}" fill="{Y}"/><circle cx="{x:.1f}" cy="{cy-r*0.05:.1f}" r="{r*0.08:.1f}" fill="#101214"/>'
        o+=f'<ellipse cx="{cx}" cy="{cy+r*0.42:.1f}" rx="{r*0.1:.1f}" ry="{r*0.13:.1f}" fill="{Y}"/>'
    elif kind=='heart':
        for sg in (-1,1):
            x=cx+sg*e; h=rr*1.1
            o+=f'<path d="M{x:.1f} {ey+h*0.9:.1f} C{x-h*1.6:.1f} {ey-h*0.2:.1f} {x-h*0.6:.1f} {ey-h*1.3:.1f} {x:.1f} {ey-h*0.35:.1f} C{x+h*0.6:.1f} {ey-h*1.3:.1f} {x+h*1.6:.1f} {ey-h*0.2:.1f} {x:.1f} {ey+h*0.9:.1f} Z" fill="#FF5C8A"/>'
    elif kind=='smile':
        o+=f'<path d="M{cx-r*0.4:.1f} {cy-r*0.05:.1f} Q{cx} {cy+r*0.45:.1f} {cx+r*0.4:.1f} {cy-r*0.05:.1f}" fill="none" stroke="{Y}" stroke-width="{w:.1f}" stroke-linecap="round"/>'
    return o
def stars(n,seed,col='#FFF6D6'):
    import random; R=random.Random(seed); o=''
    for _ in range(n):
        x,y=R.uniform(15,185),R.uniform(12,110); r=R.choice((1,1.2,1.6,2.2))
        o+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="{R.uniform(.5,1):.2f}"/>'
    return o
def frame(k,bg,scene,animal):
    return f'''<svg viewBox="0 0 200 200" role="img"><defs><clipPath id="c-{k}"><circle cx="100" cy="100" r="100"/></clipPath></defs>
<g clip-path="url(#c-{k})">{bg}{scene}</g>{animal}</svg>'''
def lin(k,a,b): return f'<linearGradient id="g-{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
def bgg(k,a,b): return f'<defs>{lin(k,a,b)}</defs><rect width="200" height="200" fill="url(#g-{k})"/>'
SH='<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#000" opacity=".12"/>'
def shadow(x,y,rx,ry): return SH.format(x=x,y=y,rx=rx,ry=ry)

I={}
# ---------- ABEILLE
I['abeille']=frame('abeille',bgg('abeille','#8FD6FF','#E3F6FF'),
 '<circle cx="164" cy="42" r="16" fill="#FFE17A"/><path d="M0 170 Q60 150 120 166 T200 160 L200 200 L0 200 Z" fill="#8FDB6E"/>'
 '<path d="M42 200 Q44 172 40 150" stroke="#4E9E4A" stroke-width="4" fill="none"/><g fill="#FF8FB1"><circle cx="40" cy="138" r="9"/><circle cx="52" cy="146" r="9"/><circle cx="28" cy="146" r="9"/><circle cx="46" cy="158" r="9"/><circle cx="34" cy="158" r="9"/></g><circle cx="40" cy="150" r="7" fill="#FFD23F"/>',
 shadow(118,168,44,6)+
 '<g opacity=".9"><ellipse cx="104" cy="66" rx="26" ry="15" fill="#fff" transform="rotate(-28 104 66)"/><ellipse cx="136" cy="62" rx="26" ry="15" fill="#F2FAFF" transform="rotate(24 136 62)"/></g>'
 '<clipPath id="bb"><ellipse cx="124" cy="112" rx="46" ry="34"/></clipPath><ellipse cx="124" cy="112" rx="46" ry="34" fill="#FFC53A"/>'
 '<g clip-path="url(#bb)"><rect x="116" y="70" width="13" height="90" fill="#2B2A33"/><rect x="142" y="70" width="12" height="90" fill="#2B2A33"/><ellipse cx="124" cy="138" rx="50" ry="14" fill="#F0A21C" opacity=".6"/></g>'
 '<path d="M168 108 L182 113 L168 119 Z" fill="#2B2A33"/>'
 '<path d="M66 84 Q58 60 50 54" stroke="#2B2A33" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M84 82 Q88 58 98 50" stroke="#2B2A33" stroke-width="3.5" fill="none" stroke-linecap="round"/><circle cx="49" cy="53" r="5" fill="#2B2A33"/><circle cx="99" cy="49" r="5" fill="#2B2A33"/>'
 +face(76,110,27)+'<circle cx="54" cy="122" r="5" fill="#FF9FB6" opacity=".7"/>')
# ---------- MARTINET
I['martinet']=frame('martinet',bgg('martinet','#6CC4FF','#D4EEFF'),
 '<g fill="#fff" opacity=".9"><ellipse cx="46" cy="150" rx="30" ry="12"/><ellipse cx="66" cy="142" rx="20" ry="13"/><ellipse cx="150" cy="40" rx="22" ry="9"/><ellipse cx="164" cy="34" rx="14" ry="9"/></g>',
 '<path d="M100 96 C78 70 44 58 8 64 C40 70 70 86 90 116 Z" fill="#3A3342"/><path d="M100 96 C122 70 156 58 192 64 C160 70 130 86 110 116 Z" fill="#3A3342"/>'
 '<path d="M100 98 C82 80 56 72 30 72 C58 80 78 94 92 112 Z" fill="#524A5E"/><path d="M100 98 C118 80 144 72 170 72 C142 80 122 94 108 112 Z" fill="#524A5E"/>'
 '<path d="M90 138 L80 172 L100 152 L120 172 L110 138 Z" fill="#3A3342"/><ellipse cx="100" cy="116" rx="21" ry="30" fill="#463E52"/><ellipse cx="100" cy="126" rx="10" ry="12" fill="#EDE6F2"/>'
 +face(100,84,19))
# ---------- CROCODILE
I['crocodile']=frame('crocodile',bgg('crocodile','#FFD45C','#FFF1BF'),
 '<circle cx="158" cy="44" r="22" fill="#FFB23F"/><circle cx="158" cy="44" r="30" fill="#FFB23F" opacity=".25"/><path d="M0 150 Q50 142 100 150 T200 146 L200 200 L0 200 Z" fill="#4FC3F0"/><path d="M20 164 q10 -4 20 0 M120 172 q10 -4 20 0" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/>',
 shadow(104,150,76,7)+
 '<path d="M150 118 Q186 116 196 136 Q176 132 150 134 Z" fill="#2F8F4E"/>'
 '<rect x="46" y="100" width="116" height="42" rx="21" fill="#3DAA5C"/><path d="M58 132 Q104 146 154 132 L154 140 Q104 152 58 140 Z" fill="#B7E09B"/>'
 '<g fill="#2F8F4E"><path d="M78 101 q7 -12 14 0"/><path d="M98 100 q7 -12 14 0"/><path d="M118 100 q7 -12 14 0"/><path d="M138 102 q6 -10 12 0"/></g>'
 '<path d="M8 118 Q8 104 24 102 L64 102 L64 138 L24 138 Q8 136 8 124 Z" fill="#3DAA5C"/><path d="M8 124 L64 124" stroke="#2F8F4E" stroke-width="2.5"/><path d="M14 124 l4 5 l4 -5 l4 5 l4 -5 l4 5 l4 -5 l4 5" fill="#fff"/><circle cx="16" cy="110" r="2.2" fill="#2F8F4E"/>'
 '<g fill="#2F8F4E"><rect x="60" y="136" width="14" height="16" rx="6"/><rect x="130" y="136" width="14" height="16" rx="6"/></g>'
 +face(70,92,17))
# ---------- CHAT
I['chat']=frame('chat',bgg('chat','#FFB36B','#B77CE8'),
 '<circle cx="42" cy="54" r="18" fill="#FFE3A8" opacity=".85"/>'+stars(8,3)+'<rect x="0" y="168" width="200" height="32" fill="#8A5FD0"/>',
 shadow(100,172,46,6)+
 '<path d="M132 168 C176 166 178 118 152 108" stroke="#F08A35" stroke-width="12" fill="none" stroke-linecap="round"/>'
 '<ellipse cx="100" cy="146" rx="42" ry="30" fill="#F08A35"/><ellipse cx="100" cy="152" rx="20" ry="20" fill="#FFF1E3"/>'
 '<g fill="#F08A35"><ellipse cx="80" cy="172" rx="12" ry="6"/><ellipse cx="120" cy="172" rx="12" ry="6"/></g>'
 '<path d="M58 70 L64 28 L92 56 Z M142 70 L136 28 L108 56 Z" fill="#F08A35"/><path d="M66 58 L68 40 L84 54 Z M134 58 L132 40 L116 54 Z" fill="#FFB0C0"/>'
 '<circle cx="100" cy="84" r="44" fill="#F08A35"/><path d="M84 44 q4 8 0 14 M100 40 v14 M116 44 q-4 8 0 14" stroke="#D96C1E" stroke-width="4" fill="none" stroke-linecap="round"/>'
 '<g stroke="#5A3B22" stroke-width="2" stroke-linecap="round"><line x1="54" y1="96" x2="28" y2="90"/><line x1="54" y1="102" x2="28" y2="106"/><line x1="146" y1="96" x2="172" y2="90"/><line x1="146" y1="102" x2="172" y2="106"/></g>'
 +face(100,88,27))
# ---------- TORTUE
I['tortue']=frame('tortue',bgg('tortue','#2B36A8','#3F7FD0'),
 stars(16,21)+'<circle cx="160" cy="36" r="13" fill="#FFF3C4"/><path d="M140 150 h40 M146 158 h28 M152 166 h16" stroke="#FFF3C4" stroke-width="3" stroke-linecap="round" opacity=".7"/><path d="M0 178 Q40 168 80 178 T160 176 T200 178 V200 H0 Z" fill="#E9C97A"/>',
 '<g fill="#63C29B"><ellipse cx="54" cy="70" rx="30" ry="12" transform="rotate(-32 54 70)"/><ellipse cx="146" cy="70" rx="30" ry="12" transform="rotate(32 146 70)"/><ellipse cx="62" cy="152" rx="18" ry="9" transform="rotate(34 62 152)"/><ellipse cx="138" cy="152" rx="18" ry="9" transform="rotate(-34 138 152)"/><path d="M94 170 L100 186 L106 170 Z"/></g>'
 '<circle cx="100" cy="32" r="15" fill="#63C29B"/><circle cx="94" cy="29" r="2.6" fill="#1D4B3C"/><circle cx="106" cy="29" r="2.6" fill="#1D4B3C"/>'
 '<ellipse cx="100" cy="108" rx="54" ry="64" fill="#2F9E7E"/><ellipse cx="100" cy="108" rx="46" ry="56" fill="#3BB592"/>'
 '<g fill="none" stroke="#2F9E7E" stroke-width="4"><path d="M62 72 L80 82 M138 72 L120 82 M56 124 L74 118 M144 124 L126 118 M78 158 L88 144 M122 158 L112 144"/></g>'
 +face(100,110,28,'arrow','#C9EFE0'))
# ---------- CHOUETTE
I['chouette']=frame('chouette',bgg('chouette','#2B36A8','#5B55D6'),
 stars(22,7)+'<circle cx="160" cy="40" r="16" fill="#FFF3C4"/><circle cx="152" cy="34" r="14" fill="#22306E"/>'
 '<path d="M0 162 Q60 150 120 160 T200 152" stroke="#6B4A2E" stroke-width="12" fill="none" stroke-linecap="round"/>',
 '<path d="M66 50 L72 22 L90 42 Z M134 50 L128 22 L110 42 Z" fill="#8E5E3B"/>'
 '<ellipse cx="100" cy="104" rx="50" ry="58" fill="#9C6A44"/><path d="M52 100 Q40 136 64 158 Q74 128 70 100 Z M148 100 Q160 136 136 158 Q126 128 130 100 Z" fill="#7D5132"/>'
 '<ellipse cx="100" cy="124" rx="30" ry="32" fill="#EBCFA6"/><g fill="none" stroke="#C9A578" stroke-width="3" stroke-linecap="round"><path d="M86 118 l4 4 l4 -4 M106 118 l4 4 l4 -4 M96 132 l4 4 l4 -4 M86 144 l4 4 l4 -4 M106 144 l4 4 l4 -4"/></g>'
 '<path d="M64 80 Q100 50 136 80 Q130 108 100 112 Q70 108 64 80 Z" fill="#D8B587"/>'
 +face(100,80,26,'owl','#EFDDBF')+'<path d="M95 100 L105 100 L100 110 Z" fill="#FF9E2C"/>'
 '<g fill="#FF9E2C"><rect x="84" y="156" width="10" height="9" rx="3"/><rect x="106" y="156" width="10" height="9" rx="3"/></g>')
# ---------- RAINETTE
I['rainette']=frame('rainette',bgg('rainette','#1F5FA8','#3FA0D8'),
 '<g fill="#8FD3FF" opacity=".75">'+''.join(f'<path d="M{x} {y} q-4 7 0 10 q4 -3 0 -10 Z"/>' for x,y in ((30,30),(60,50),(150,24),(178,60),(24,90),(166,104),(110,20)))+'</g>'
 '<ellipse cx="100" cy="182" rx="90" ry="22" fill="#2E9A5A"/><ellipse cx="60" cy="176" rx="34" ry="10" fill="#45BE6E"/>',
 '<g fill="#3FB35F"><path d="M50 150 Q18 156 24 176 L66 172 Z"/><path d="M150 150 Q182 156 176 176 L134 172 Z"/></g>'
 '<ellipse cx="100" cy="128" rx="60" ry="46" fill="#4CC46C"/><ellipse cx="100" cy="146" rx="40" ry="26" fill="#DDF5C9"/>'
 '<circle cx="66" cy="84" r="20" fill="#4CC46C"/><circle cx="134" cy="84" r="20" fill="#4CC46C"/>'
 '<circle cx="66" cy="82" r="12" fill="#FFD84A"/><circle cx="134" cy="82" r="12" fill="#FFD84A"/><ellipse cx="66" cy="82" rx="8" ry="4" fill="#1A1A1A"/><ellipse cx="134" cy="82" rx="8" ry="4" fill="#1A1A1A"/>'
 '<circle cx="60" cy="122" r="7" fill="#FF8FB0" opacity=".7"/><circle cx="140" cy="122" r="7" fill="#FF8FB0" opacity=".7"/>'
 +face(100,120,21,'smile','#CFF0DA'))
# ---------- CHAUVE-SOURIS
I['chauvesouris']=frame('chauvesouris',bgg('chauvesouris','#3A2FA8','#7552D8'),
 stars(24,11)+'<circle cx="100" cy="104" r="62" fill="#FFF3C4" opacity=".95"/>',
 '<path d="M80 96 L14 64 Q26 94 12 122 Q40 114 46 136 Q62 118 82 124 Z" fill="#6A4BC4"/><path d="M120 96 L186 64 Q174 94 188 122 Q160 114 154 136 Q138 118 118 124 Z" fill="#6A4BC4"/>'
 '<path d="M76 100 L32 80 M76 108 L40 118 M118 100 L168 80 M124 108 L160 118" stroke="#8C70E4" stroke-width="3" stroke-linecap="round"/>'
 '<path d="M74 64 L76 34 L92 54 Z M126 64 L124 34 L108 54 Z" fill="#54399E"/><path d="M79 56 L80 42 L88 52 Z M121 56 L120 42 L112 52 Z" fill="#FF9FB6"/>'
 '<ellipse cx="100" cy="102" rx="30" ry="40" fill="#54399E"/><ellipse cx="100" cy="118" rx="15" ry="18" fill="#7B5ED4"/>'
 +face(100,82,21)+'<path d="M94 108 l2 6 l2 -6 Z M102 108 l2 6 l2 -6 Z" fill="#fff"/>')
# ---------- FENNEC
I['fennec']=frame('fennec',bgg('fennec','#4A38B0','#B06BD6'),
 stars(18,5)+'<path d="M0 160 Q50 136 110 156 T200 150 V200 H0 Z" fill="#F5B75E"/><path d="M0 176 Q70 160 140 176 T200 172 V200 H0 Z" fill="#E89B45"/>',
 '<path d="M132 176 C170 176 180 140 166 128 C160 150 148 158 128 160 Z" fill="#F1C185"/><path d="M166 128 C174 138 174 152 168 160 C162 150 160 140 166 128 Z" fill="#6B4A2E"/>'
 '<ellipse cx="100" cy="162" rx="36" ry="22" fill="#F1C185"/><ellipse cx="100" cy="166" rx="18" ry="14" fill="#FFF3E0"/>'
 '<path d="M80 84 L40 14 Q70 30 96 70 Z M120 84 L160 14 Q130 30 104 70 Z" fill="#F1C185"/><path d="M78 72 L52 28 Q70 40 88 66 Z M122 72 L148 28 Q130 40 112 66 Z" fill="#FFB1C1"/>'
 '<ellipse cx="100" cy="104" rx="38" ry="34" fill="#F1C185"/><path d="M76 118 Q100 146 124 118 Q100 128 76 118 Z" fill="#FFF3E0"/>'
 +face(100,100,23)+'<ellipse cx="100" cy="132" rx="5" ry="3.6" fill="#2B2B2B"/>')

# ---------- ENFANTS (même style que les animaux)
SKIN='#F0BE95'; SKIN_D='#E3A57A'; HAIR='#4A3326'
def kid_face(cx,cy,r,eyes='open'):
    o=(f'<path d="M{cx-r*1.02} {cy} Q{cx-r*1.1} {cy-r*1.25} {cx} {cy-r*1.12} Q{cx+r*1.1} {cy-r*1.25} {cx+r*1.02} {cy} Z" fill="{HAIR}"/>'
       f'<circle cx="{cx}" cy="{cy+r*0.08}" r="{r}" fill="{SKIN}"/>'
       f'<path d="M{cx-r*0.95} {cy-r*0.25} Q{cx-r*0.2} {cy-r*1.05} {cx+r*0.95} {cy-r*0.35} Q{cx+r*0.6} {cy-r*1.2} {cx} {cy-r*1.1} Q{cx-r*0.8} {cy-r*1.05} {cx-r*0.95} {cy-r*0.25} Z" fill="{HAIR}"/>'
       f'<circle cx="{cx-r*0.55}" cy="{cy+r*0.35}" r="{r*0.14}" fill="#FF8FA8" opacity=".7"/><circle cx="{cx+r*0.55}" cy="{cy+r*0.35}" r="{r*0.14}" fill="#FF8FA8" opacity=".7"/>')
    ey=cy+r*0.12
    if eyes=='closed':
        for s in (-1,1): o+=f'<path d="M{cx+s*r*0.36-r*0.14} {ey} q{r*0.14} {r*0.12} {r*0.28} 0" fill="none" stroke="#3A2A20" stroke-width="{r*0.07:.1f}" stroke-linecap="round"/>'
        o+=f'<path d="M{cx-r*0.12} {cy+r*0.5} q{r*0.12} {-r*0.08} {r*0.24} 0" fill="none" stroke="#B5654A" stroke-width="{r*0.06:.1f}" stroke-linecap="round"/>'
    elif eyes=='squeeze':
        for s in (-1,1): o+=f'<path d="M{cx+s*r*0.36-r*0.14} {ey-r*0.08} l{r*0.14} {r*0.1} l{r*0.14} {-r*0.1}" fill="none" stroke="#3A2A20" stroke-width="{r*0.07:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        o+=f'<ellipse cx="{cx}" cy="{cy+r*0.55}" rx="{r*0.14}" ry="{r*0.1}" fill="#B5654A"/>'
    elif eyes=='smile':
        for s in (-1,1): o+=f'<path d="M{cx+s*r*0.36-r*0.13} {ey+r*0.03} q{r*0.13} {-r*0.16} {r*0.26} 0" fill="none" stroke="#3A2A20" stroke-width="{r*0.07:.1f}" stroke-linecap="round"/>'
        o+=f'<path d="M{cx-r*0.28} {cy+r*0.42} q{r*0.28} {r*0.26} {r*0.56} 0" fill="#B5654A"/>'
        return o
    else:
        for s in (-1,1): o+=f'<circle cx="{cx+s*r*0.36}" cy="{ey}" r="{r*0.09}" fill="#3A2A20"/>'
        o+=f'<path d="M{cx-r*0.18} {cy+r*0.52} q{r*0.18} {-r*0.1} {r*0.36} 0" fill="none" stroke="#B5654A" stroke-width="{r*0.06:.1f}" stroke-linecap="round"/>'
    return o
I['kid_sleep']=frame('kid_sleep',bgg('kid_sleep','#2B36A8','#4A4FC8'),
 stars(10,31)+'<rect x="18" y="28" width="16" height="120" fill="#6A6FB0"/><path d="M26 30 L54 30 L50 40 L30 40 Z" fill="#3B3F80"/><path d="M36 40 L4 200 L120 200 Z" fill="#FFE9A0" opacity=".38"/><circle cx="42" cy="40" r="6" fill="#FFF3C4"/>',
 '<rect x="40" y="128" width="150" height="60" rx="14" fill="#8FA8E8"/><rect x="40" y="120" width="150" height="26" rx="12" fill="#B9C9F5"/>'
 '<ellipse cx="120" cy="116" rx="46" ry="18" fill="#fff"/>'+kid_face(120,96,30,'closed')+
 '<path d="M136 150 C150 124 190 124 196 150 Z" fill="#6D7FD0"/><text x="160" y="64" font-family="League Spartan,sans-serif" font-weight="700" font-size="22" fill="#fff" opacity=".85">z</text><text x="176" y="46" font-family="League Spartan,sans-serif" font-weight="700" font-size="16" fill="#fff" opacity=".7">z</text>')
I['kid_noise']=frame('kid_noise',bgg('kid_noise','#FFB36B','#FFD9A8'),
 '<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".85"><path d="M22 70 q-10 30 0 60"/><path d="M8 58 q-14 42 0 84"/><path d="M178 70 q10 30 0 60"/><path d="M192 58 q14 42 0 84"/></g>'
 '<path d="M0 176 H200 V200 H0 Z" fill="#E88A4A"/>',
 '<path d="M62 200 Q64 150 100 146 Q136 150 138 200 Z" fill="#3FA0D8"/>'+kid_face(100,98,38,'squeeze')+
 '<ellipse cx="58" cy="106" rx="13" ry="17" fill="'+SKIN_D+'"/><ellipse cx="142" cy="106" rx="13" ry="17" fill="'+SKIN_D+'"/>'
 '<path d="M50 124 Q46 150 62 160 L74 152 Q62 144 62 124 Z" fill="'+SKIN+'"/><path d="M150 124 Q154 150 138 160 L126 152 Q138 144 138 124 Z" fill="'+SKIN+'"/>')
I['kid_heat']=frame('kid_heat',bgg('kid_heat','#FFD45C','#FFF1BF'),
 '<circle cx="160" cy="40" r="24" fill="#FFB23F"/><circle cx="160" cy="40" r="34" fill="#FFB23F" opacity=".25"/><path d="M0 172 H200 V200 H0 Z" fill="#9A9A9A"/><path d="M20 186 h30 M90 184 h40 M150 188 h30" stroke="#B5B5B5" stroke-width="4" stroke-linecap="round"/>',
 '<path d="M62 200 Q64 150 100 146 Q136 150 138 200 Z" fill="#FF7A59"/>'+kid_face(100,100,38,'open')+
 '<path d="M140 72 q-6 10 0 14 q6 -4 0 -14 Z" fill="#8FD3FF"/><path d="M60 64 q-5 8 0 11 q5 -3 0 -11 Z" fill="#8FD3FF"/>'
 '<circle cx="78" cy="118" r="7" fill="#FF6B6B" opacity=".45"/><circle cx="122" cy="118" r="7" fill="#FF6B6B" opacity=".45"/>')

I['kid_look']=frame('kid_look',bgg('kid_look','#8FD6FF','#E3F6FF'),
 '<path d="M0 172 Q60 160 120 170 T200 166 V200 H0 Z" fill="#8FDB6E"/><g fill="#fff" opacity=".9"><ellipse cx="44" cy="44" rx="20" ry="8"/><ellipse cx="160" cy="58" rx="16" ry="6"/></g>',
 '<path d="M62 200 Q64 150 100 146 Q136 150 138 200 Z" fill="#B89CFF"/>'+kid_face(100,100,38,'smile')+'<path d="M128 70 l8 -10 M136 78 l12 -4 M136 88 l12 2" stroke="#F7D117" stroke-width="4" stroke-linecap="round"/>')

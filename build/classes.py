import json,collections,re
ALIAS={'AndreCardoso':'ALSRC','BetterCallJamie':'FlatCap Jay','jasmith85':'FlatCap Jay','aand14':'drand','mattimatti':'mattibassi','Tinman86':'TinMan86'}
raw=json.load(open('scores_raw.json'))
LV='BIAM'
def lvl(l):
    l=(l or '').lower()
    if l.startswith('god') or 'tribute' in l: return None
    if 'master' in l: return 'M'
    if l.startswith('adv'): return 'A'
    if l.startswith('int'): return 'I'
    if 'begin' in l: return 'B'
def base(n):
    n=n.strip()
    if re.match(r'^ALSRC\*trw',n): n='ALSRC*'
    b=n.rstrip('*~').strip(); return ALIAS.get(b,b)
own=collections.defaultdict(lambda:collections.defaultdict(collections.Counter))
for wk,ch in raw.items():
    w=int(wk)
    if w<440: continue
    for P,slot,l,song,d,ex,ents in ch:
        L=lvl(l)
        if not L: continue
        for e in ents:
            if '*' in e[0]: continue
            own[(base(e[0]),P)][w][L]+=1
def history(wm,minrun=3):
    seq=[(w,wm[w].most_common(1)[0][0]) for w in sorted(wm)]
    runs=[]
    for w,L in seq:
        if runs and runs[-1][1]==L: runs[-1][2]+=1
        else: runs.append([w,L,1])
    keep=[r for i,r in enumerate(runs) if r[2]>=minrun or i==len(runs)-1]
    m=[]
    for r in keep:
        if m and m[-1][1]==r[1]: m[-1][2]+=r[2]
        else: m.append(list(r))
    return m
HIST={k:history(v) for k,v in own.items()}
def class_at(name,P,w):
    h=HIST.get((name,P))
    if not h: return None
    c=None
    for start,L,_ in h:
        if start<=w: c=L
        else: break
    return c or h[0][1]   # before first observed run, assume first known class

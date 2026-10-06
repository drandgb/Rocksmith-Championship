import json,collections,openpyxl,re
ALIAS={'AndreCardoso':'ALSRC','BetterCallJamie':'FlatCap Jay','jasmith85':'FlatCap Jay','aand14':'drand','mattimatti':'mattibassi','Tinman86':'TinMan86'}
DROP={'#REF!','Player Name'}
raw=json.load(open('scores_raw.json'))
DATA_WEEK=int(open('data_week.txt').read())
FONTS=json.load(open('fonts.json'))
exec(open('classes.py').read().split("raw=json.load(open('scores_raw.json'))")[1])
STATS=collections.Counter()
names=[];idx={};aka={}
def ni(n):
    n=n.strip()
    if re.match(r'^ALSRC\*trw',n): n='ALSRC*'
    m=re.match(r'^(.*?)([*~]*)$',n); base,suf=m.group(1).strip(),m.group(2)
    new=ALIAS.get(base,base); key=(new+suf,base if new!=base else None)
    if key not in idx:
        idx[key]=len(names); names.append(new+suf)
        if new!=base: aka[idx[key]]=base
    return idx[key]
def num(v):
    if v is None: return None
    return int(v) if float(v).is_integer() else round(v,2)
# SONGFIX: use the corrected spelling from the Songs Played sheet for the same week
import difflib
SP=json.load(open('songsel_byweek.json'))
def norm(t): return re.sub(r'[^a-z0-9]+',' ',t.lower().replace(' and ',' & ')).strip()
FIXED=collections.Counter()
def fixsong(wk,song):
    if not song or song=='n/a': return song
    cands=SP.get(str(wk),[]); clean=re.sub(r'\s+',' ',song).strip()
    for c in cands:
        if norm(c)==norm(clean): 
            if c!=song: FIXED[(song,c)]+=1
            return c
    best=difflib.get_close_matches(norm(clean),[norm(c) for c in cands],1,0.88)
    if best:
        c=[c for c in cands if norm(c)==best[0]][0]; FIXED[(song,c)]+=1; return c
    return clean
weeks={}
for wk,ch in raw.items():
    if int(wk)<440: continue
    out=[]
    for p,s_,l,song,d,ex,ents in ch:
        fl=FONTS.get(wk,{}).get(str(p*9+s_),[])
        L=lvl(l); rows=[]
        for k,e in enumerate(ents):
            if e[0].strip() in DROP: continue
            d_=0
            if '*' in e[0]:
                f=fl[k] if k<len(fl) and fl[k][0]==e[0].strip() else None
                fd=None
                if f and f[3] is not None:
                    if f[3]<=8: fd=-1
                    elif f[1]=='FF666666': fd=2
                    elif f[1] in ('FF000000','00000000'): fd=1
                hd=None
                oc=class_at(base(e[0]),p,int(wk)) if L else None
                if L and oc: hd=LV.index(L)-LV.index(oc); hd=-1 if hd<0 else (2 if hd>=2 else (1 if hd==1 else 0))
                if fd is not None:
                    d_=fd; STATS['font']+=1
                    if hd is not None and (hd<0)!=(fd<0): STATS['disagree']+=1
                elif hd is not None: d_=hd; STATS['history']+=1
                else: STATS['unknown']+=1
            if '*' not in e[0]:
                f=fl[k] if k<len(fl) and fl[k][0]==e[0].strip() else None
                if f and f[1] in ('FFFF00FF','FF0000FF'): d_=9; STATS['noclass']+=1   # magenta = new player/invalid, blue = no class in this path
            rows.append([ni(e[0]),num(e[1]),num(e[2]),num(e[3]),d_])
        out.append([p,s_,l,fixsong(wk,song),num(d) if d is not None else None,ex,rows])
    weeks[wk]=out
# God / tribute challenges run for 2+ weeks in a row with the same song. Only the final week of the run decides the
# winner, so a card whose song is still the God challenge next week gets a trailing 1 ("continues") and doesn't count
# toward wins or entries.
def is_god(l): l=(l or '').lower(); return l.startswith('god') or 'tribute' in l
def gkey(c): return (c[0], re.sub(r'\s+',' ',(c[3] or '').strip().lower()))
CONT=0
for wk,out in weeks.items():
    nxt={gkey(c) for c in weeks.get(str(int(wk)+1),[]) if is_god(c[2])}
    for c in out:
        if is_god(c[2]) and c[3] and c[3]!='n/a' and gkey(c) in nxt: c.append(1); CONT+=1
print('God cards that continue into the next week:',CONT)
json.dump({"names":names,"aka":aka,"weeks":weeks},open('scores.json','w'),separators=(',',':'))
N=names
LV='BIAM'
def lvl(l):
    l=l.lower()
    if l.startswith('god') or 'tribute' in l: return None
    if 'master' in l: return 'M'
    if l.startswith('adv'): return 'A'
    if l.startswith('int'): return 'I'
    if 'begin' in l: return 'B'
own2=collections.defaultdict(lambda:collections.defaultdict(collections.Counter))
win=collections.defaultdict(lambda:[[0,0,0],[0,0,0],[0,0,0]])
for wk in weeks:
    w=int(wk)
    for card in weeks[wk]:
        P,slot,l,song,d,ex,ents=card[:7]; cont=len(card)>7 and card[7]
        L=lvl(l)
        elig=[e for e in ents if e[4]>=0] if not cont else []   # a God challenge only counts in its final week
        for i,e in enumerate(elig):
            b_=N[e[0]].rstrip('*~')
            if w<=DATA_WEEK:   # only completed weeks count toward win totals
                win[b_][P][0]+=1
                if i==0: win[b_][P][1]+=1
                if i<3: win[b_][P][2]+=1
        for e in ents:
            raw_=N[e[0]]; b_=raw_.rstrip('*~')
            if L and '*' not in raw_ and e[4]!=9: own2[(b_,P)][w][L]+=1
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
ups=[]
for (n,P),wm in own2.items():
    h=history(wm)
    for a,b in zip(h,h[1:]):
        if b[1]!=a[1]: ups.append([n,P,a[1],b[1],b[0]])
ups.sort(key=lambda x:(-x[4],x[0]))
json.dump({"wins":win,"ups":ups},open('wins.json','w'),separators=(',',':'))
print('names',len(names),'aka',len(aka),'ups',len(ups))
print(win['cacahuate51'],dict(STATS))
print('song spellings fixed',sum(FIXED.values()),[k for k in FIXED if k[0].strip().lower()!=k[1].lower()][:40])

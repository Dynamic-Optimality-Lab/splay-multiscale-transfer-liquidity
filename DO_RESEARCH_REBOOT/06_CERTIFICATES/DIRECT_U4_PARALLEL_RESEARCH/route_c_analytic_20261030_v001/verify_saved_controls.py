"""Independent full-access replay and formal polynomial identity verification."""
from pathlib import Path
from collections import Counter
import sys,json,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P

def ck(v,msg):
    if not v:raise AssertionError(msg)

def pointer(raw):
    if raw is None:return None
    n=P.mknode(raw[0],pointer(raw[1]),pointer(raw[2]))
    if n['l'] is not None:n['l']['p']=n
    if n['r'] is not None:n['r']['p']=n
    return n
def serial(n):return None if n is None else [n['k'],serial(n['l']),serial(n['r'])]
def depths(n,d=0):
    if n is None:return {}
    return {n['k']:d,**depths(n['l'],d+1),**depths(n['r'],d+1)}
def profile(a,b):
    da=depths(a);db=depths(b)
    return [[i,j,v] for (i,j),v in sorted(Counter((da[k],db[k]) for k in da).items())]

def replay(r):
    a=pointer(r['source_A']);b=pointer(r['source_B']);x=r['key']
    ck(profile(a,b)==r['source_H'],'source histogram')
    ck(P._depth_to(a,x)[0]==r['dA'],'A depth')
    a,ae=P.splay_trace(a,x)
    if r['mode']=='K':
        ck(P._depth_to(b,x)[0]==r['dB'],'B depth');b,be=P.splay_trace(b,x)
    else:be=[]
    ck(serial(a)==r['destination_A'] and serial(b)==r['destination_B'],'complete source replay')
    ck(len(ae)==r['a'] and sum(e['case']!='ZIG' for e in be)==r['q'],'source costs')
    ck(profile(a,b)==r['destination_H'],'destination histogram')

def poly(*monomials):return Counter(monomials)
def clean(p):return {k:v for k,v in p.items() if v}
def combine(a,b,sign=1):
    c=Counter(a)
    for k,v in b.items():c[k]+=sign*v
    return clean(c)
def mul(a,b):
    out=Counter()
    for k,u in a.items():
        for l,v in b.items():out[tuple(i+j for i,j in zip(k,l))]+=u*v
    return clean(out)

def main():
    output=OUT/'independent_audit.json';ck(not output.exists(),'append-only output')
    data=json.loads((OUT/'profile_transport_controls.json').read_text(encoding='utf-8'))
    for r in data['records']:replay(r)
    closes=json.loads((OUT/'six_key_closed_controls.json').read_text(encoding='utf-8'))
    for closed in closes['controls']:
        for r in closed['full_replay']:replay(r)
        rows=closed['full_replay'];ck(rows[0]['source_A']==rows[-1]['destination_A']==closed['initial_A'],'A closure')
        ck(rows[0]['source_B']==rows[-1]['destination_B']==closed['initial_B'],'B closure')
        for a,b in zip(rows,rows[1:]):ck(a['destination_A']==b['source_A'] and a['destination_B']==b['source_B'],'full joins')
        ck(sum(r['a'] for r in rows)==closed['A'] and sum(r['q'] for r in rows)==closed['Q_B'],'cycle costs')
    # Work in Z[z,w,C], with C an independent formal profile symbol.
    C=poly((0,0,1));one=poly((0,0,0));z=poly((1,0,0));w=poly((0,1,0))
    HL=poly((0,0,0),(1,1,0),(1,2,0),(2,3,0),(3,2,0),(4,1,0),(0,0,1))
    HR=poly((0,0,0),(1,1,0),(1,2,0),(2,2,0),(3,3,0),(4,1,0),(0,1,1))
    expected=mul(combine(w,one,-1),combine(C,mul(poly((2,2,0)),combine(z,one,-1))))
    ck(combine(HR,HL,-1)==expected,'formal arbitrary-profile identity')
    result={'status':'PASS','whole_access_controls_replayed':len(data['records']),
            'source_StepEv_formula_controls':data['source_StepEv_identities_checked'],
            'full_closed_walks_replayed':len(closes['controls']),
            'full_closed_walk_accesses_replayed':sum(len(c['full_replay']) for c in closes['controls']),
            'formal_polynomial_ring':'Z[z,w,C]','formal_identity':'H_R-H_L=(w-1)*(C+z^2*w^2*(z-1))',
            'identity_exact':True,'finite_fits':0,'all_size_repayment_potential_proved':False,
            'control_certificate_sha256':hashlib.sha256((OUT/'profile_transport_controls.json').read_bytes()).hexdigest()}
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

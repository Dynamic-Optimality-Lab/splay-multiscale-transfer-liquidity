"""Independent pointer-source and chord-dual readback; no producer import."""
from pathlib import Path
import hashlib,json,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P

def ck(ok,msg):
    if not ok: raise AssertionError(msg)
def inspect(t):
    if t is None:return [],[]
    lk,li=inspect(t[1]);rk,ri=inspect(t[2]);keys=lk+[t[0]]+rk
    ck(keys==sorted(set(keys)),'ordered distinct subtree keys')
    return keys,li+ri+[(keys[0],keys[-1])]
def proper(t):
    keys,intervals=inspect(t)
    if keys:intervals.remove((keys[0],keys[-1]))
    ck(len(intervals)==max(0,len(keys)-1) and len(set(intervals))==len(intervals),'all proper sets exactly once')
    return keys,sorted(intervals)
def crosses(I,J):
    a,b=I[0]-1,I[1]+1;c,d=J[0]-1,J[1]+1
    return len({a,b,c,d})==4 and ((a<c<b)!=(a<d<b))
def value(a,b):
    ka,ia=proper(a);kb,ib=proper(b)
    ck(ka==kb==list(range(1,len(ka)+1)),'same ranked keys')
    adj=[[j for j,J in enumerate(ib) if crosses(I,J)] for I in ia];degree=list(map(len,adj))
    return {'A_intervals':[list(i) for i in ia],'B_intervals':[list(j) for j in ib],
      'crossing_adjacency':adj,'crossing_degrees':degree,
      **{'H'+str(k):sum(d>=k for d in degree) for k in (1,2,3)}}
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent key')
def refl(t,n):return None if t is None else [n+1-t[0],refl(t[2],n),refl(t[1],n)]

def main():
    cp=OUT/'crossing_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));rows=0;incidences=0
    def verify(r):
        nonlocal rows,incidences
        a,b=r['source_A'],r['source_B'];x=r['key'];mode=r['mode'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        ap,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bp,eb=P.splay_trace(ptr(b),x)
        else:bp,eb=ptr(b),[]
        aa,bb=raw(ap),raw(bp);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(r['destination_A'],r['destination_B']),'actual endpoints')
        ck((da,db,ac,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'actual source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source counts from depth')
        ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
        ck(ev(ea)==r['events_A'] and ev(eb)==r['events_B'],'every oriented event')
        for sa,sb,key in [(a,b,'source_values'),(aa,b,'after_A_values'),(aa,bb,'destination_values')]:
            v=value(sa,sb);ck(v==r[key],'all subtree sets, chord edges and threshold values independently regenerated')
            incidences+=len(v['A_intervals'])*len(v['B_intervals'])
        ck(abs(r['after_A_values']['H2']-r['source_values']['H2'])<=da,'A Lipschitz bound on replay')
        delta=r['destination_values']['H2']-r['source_values']['H2'];budget=2*ac-q
        ck((delta,budget,delta<=budget)==(r['delta_H2'],r['budget'],r['H2_law_holds']),'whole inequality verdict');rows+=1
    for r in c['controls']+c['reflections']:verify(r)
    ck(len(c['controls'])==len(c['reflections'])==3,'exact frozen controls')
    p,o3,o6=c['controls']
    ck(p['source_A']==[4,[2,[1,None,None],[3,None,None]],None],'registered four-key A')
    ck((p['a'],p['q'],p['z'],p['delta_H2'],p['budget'])==(0,1,1,0,-1),'principal whole-source refutation')
    ck(p['source_values']['crossing_degrees']==[1,3,1] and p['destination_values']['crossing_degrees']==[2,0,1],'conflict migrates')
    for r,m in zip(c['controls'],c['reflections']):
        n=len(inspect(r['source_A'])[0])
        ck(m['source_A']==refl(r['source_A'],n) and m['source_B']==refl(r['source_B'],n),'actual source reflection')
        ck(m['destination_A']==refl(r['destination_A'],n) and m['destination_B']==refl(r['destination_B'],n),'source commutes with reflection')
        ck((m['a'],m['q'],m['z'],m['delta_H2'])==(r['a'],r['q'],r['z'],r['delta_H2']),'reflection costs and values')
    # Fixed integer k=1; k=2; k>=3, with no parameter fit.
    ck((o6['source_values']['H1'],o6['destination_values']['H1'],o6['budget'])==(5,4,-2),'k=1 exact failure')
    ck((p['source_values']['H2'],p['destination_values']['H2'],p['budget'])==(1,1,-1),'k=2 exact failure')
    ck(max(o3['source_values']['crossing_degrees'])==2 and max(o3['destination_values']['crossing_degrees'])==0 and o3['budget']==-1,'every k>=3 has zero change, misses q=1')
    # Endpoint matching at the principal source proves this is outside the
    # previous Ehat<=T<=F bracket, independent of geometry calculations.
    _,ia=proper(p['source_A']);_,ib=proper(p['source_B'])
    common=set(ia)&set(ib);end_edges=[(i,j) for i,I in enumerate(ia) for j,J in enumerate(ib) if I[0]==J[0] or I[1]==J[1]]
    ck(not common and end_edges==[(2,1)],'one-edge endpoint graph, no forced pairs')
    ck(len(ia)-1==2 and p['source_values']['H2']==1,'H2 below Ehat=2, outside excluded bracket')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];initial_a=a;initial_b=b;At=Qt=Zt=0;delta_sum=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==11,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'shared physical source states')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z'];delta_sum+=r['delta_H2']
    ck(a==initial_a and b==initial_b and delta_sum==0,'exact paired closure and telescoping')
    ck((At,Qt,Zt)==(12,2,8)==(w['A'],w['Q_B'],w['Z_B']),'exact totals')
    bad=w['full_replay'][w['failed_edge_index']]
    ck(bad['source_A']==p['source_A'] and bad['source_B']==p['source_B'] and bad['delta_H2']==0,'failed edge reachable')
    ck(w['word'][:3]==[['D',4],['D',2],['D',4]],'explicit connector')
    result={'status':'PASS','date':'2026-10-31','source_controls':3,'reflections':3,'complete_source_edges':rows,
      'chord_incidence_comparisons_with_multiplicity':incidences,'all_source_costs_and_orientations_verified':True,
      'candidate_H2_refuted':True,'principal':{'n':4,'a':0,'q':1,'z':1,'H2_source':1,'H2_destination':1,'budget':-1},
      'all_fixed_positive_integer_thresholds_refuted':True,'threshold_scope':'one fixed integer k independent of n; not size-dependent thresholds or weighted profiles',
      'outside_old_bracket_at_principal_source':{'F':3,'Ehat':2,'H2':1},
      'closed_word':w['word'],'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'actual_pair_closure':True,'CD_counterexample':False,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'new_pair_state_graphs':0,'finite_potential_fits':0}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

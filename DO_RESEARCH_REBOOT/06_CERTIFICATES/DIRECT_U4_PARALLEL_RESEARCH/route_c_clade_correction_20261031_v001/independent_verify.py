"""Independent interval arithmetic and exact source replay of fixed controls.

Uses rank intervals, not the producer's recursive collection of full key sets.
No fitting, corpus generation, graph construction or producer import.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S

def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def tup(t):return None if t is None else (t[0],tup(t[1]),tup(t[2]))
def depths(t,d=0):return {} if t is None else {t[0]:d,**depths(t[1],d+1),**depths(t[2],d+1)}
def intervals(t):
    def visit(t):
        if t is None:return [],set()
        lk,lc=visit(t[1]);rk,rc=visit(t[2]);keys=lk+[t[0]]+rk
        ck(keys==list(range(keys[0],keys[-1]+1)),'valid consecutive rank interval')
        return keys,lc|rc|{(keys[0],keys[-1])}
    return visit(t)[1]
def F(a,b):return len(depths(a))-len(intervals(a)&intervals(b))
def G(a,b):
    da=depths(a);db=depths(b)
    return sum(Q(db[k],8**d) for k,d in da.items())
def rotations(t,direction):
    if t is None:return
    k,l,r=t
    if direction=='R' and l is not None:yield (l[0],l[1],(k,l[2],r))
    if direction=='L' and r is not None:yield (r[0],(k,l,r[1]),r[2])
    for ll in rotations(l,direction):yield (k,ll,r)
    for rr in rotations(r,direction):yield (k,l,rr)

def main():
    ck(not (OUT/'independent_audit.json').exists(),'exclusive output')
    path=OUT/'clade_correction_countercertificate.json';c=json.loads(path.read_text(encoding='utf-8'))
    checked=primitive=0;old_delete=False;old_keep=False;mirrored_failure=False
    def verify(row):
        nonlocal checked,primitive
        a=row['source_A'];b=row['source_B'];x=row['key'];mode=row['mode']
        da=depths(a)[x];db=depths(b)[x] if mode=='K' else None
        ap,ae=S.trace(dec(a),x)
        if mode=='K':bp,be=S.trace(dec(b),x)
        else:bp,be=dec(b),[]
        aa=raw(ap);bb=raw(bp);ac=len(ae);q=sum(e[0]!='ZIG' for e in be);z=sum(e[0]=='ZIG' for e in be)
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'source costs')
        ck(ac==(da+1)//2 and (q,z)==(0 if db is None else db//2,0 if db is None else db%2),'cost definitions')
        ck(aa==row['destination_A'] and bb==row['destination_B'],'full source destinations')
        ck([list(e) for e in ae]==row['events_A'] and [list(e) for e in be]==row['events_B'],'all oriented source events')
        for t,key in [(a,'source_clades_A'),(b,'source_clades_B'),(aa,'destination_clades_A'),(bb,'destination_clades_B')]:
            sets=sorted([list(range(lo,hi+1)) for lo,hi in intervals(t)])
            ck(sets==row[key],'all exact subtree key sets verified through intervals')
        f0=F(a,b);f1=F(aa,bb);g0=G(a,b);g1=G(aa,bb)
        ck((f0,f1,f1-f0)==(row['F_source'],row['F_destination'],row['delta_F']),'structural counts')
        expected={'G_source':g0,'G_destination':g1,'delta_G':g1-g0,
           'R_source':f0-g0,'R_destination':f1-g1,'delta_R':f1-f0-g1+g0}
        for k,v in expected.items():ck(str(v)==row[k],'exact independent fraction '+k)
        ck(row['required_upper_bound']==2*ac-q and row['inequality_holds']==(f1-f0<=2*ac-q),'whole edge inequality status')
        for phase,start,end,fixed,records in [('A',a,aa,b,row['primitive_A']),('B',b,bb,aa,row['primitive_B'])]:
            t=start
            for record in records:
                ck(record['before']==t,'primitive states compose')
                tt=record['after'];ck(tup(tt) in set(rotations(tup(t),record['rotation'])),'genuine single primitive rotation')
                removed=intervals(t)-intervals(tt);added=intervals(tt)-intervals(t)
                ck(len(removed)==len(added)==1,'one replaced interval')
                lo,hi=next(iter(removed));nl,nh=next(iter(added))
                ck(record['removed']==list(range(lo,hi+1)) and record['added']==list(range(nl,nh+1)),'exact changed key sets')
                ck(lo<=x<=hi and not nl<=x<=nh,'target membership in removed and added sets')
                if phase=='A':ck(abs(F(tt,fixed)-F(t,fixed))<=1,'A primitive budget')
                else:
                    ck(fixed[0]==x and not (intervals(fixed)&intervals(t))-intervals(tt),'access-root alignment, no shared set lost')
                    ck(F(fixed,tt)<=F(fixed,t),'B primitive nonincrease')
                t=tt;primitive+=1
            ck(t==end,'complete primitive trace endpoint')
        ck(len(row['primitive_A'])==da and len(row['primitive_B'])==(db or 0),'exact primitive counts')
        checked+=1
    for row in c['controls']:
        verify(row)
        if row['label']=='old_DELETE':old_delete=row['delta_F']==0 and Q(row['delta_R'])==Q(-21,8)
        if row['label']=='old_KEEP':old_keep=row['delta_F']==-1 and row['inequality_holds']
        if row['label']=='opposite_vines_KEEP_6_mirror':mirrored_failure=row['delta_F']==-1 and row['q']==2 and not row['inequality_holds']
    ck(old_delete and old_keep and mirrored_failure,'old obstruction repaired; mirror counterexample valid')
    scale_by_n={s['n']:s for s in c['rescaling_controls']}
    for n in (6,7):
        dd=next(r for r in c['controls'] if r['label']=='diagonal_DELETE_'+str(n))
        kk=next(r for r in c['controls'] if r['label']=='opposite_vines_KEEP_'+str(n))
        upper=Q(2*dd['a'],dd['delta_F']);lower=Q(kk['q'],-kk['delta_F'])
        ck(upper<lower and str(upper)==scale_by_n[n]['necessary_c_upper_from_DELETE'] and str(lower)==scale_by_n[n]['necessary_c_lower_from_KEEP'],'exact disjoint necessary scale bounds')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];a0=a;b0=b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==17,'full diagonal closed word dimension')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((mode,x,a,b)==(r['mode'],r['key'],r['source_A'],r['source_B']),'exact shared full source state')
        verify(r);a=r['destination_A'];b=r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z']
    ck(a==a0 and b==b0 and (At,Qt,Zt)==(19,4,12)==(w['A'],w['Q_B'],w['Z_B']),'actual paired closure and totals')
    bad=w['full_replay'][w['failed_edge_index']]
    ck((bad['a'],bad['q'],bad['z'],bad['delta_F'])==(0,2,1,-1),'full repayment violation in closed source walk')
    ck(primitive==c['source_rotation_identity_checks']==75,'all primitive controls covered')
    result={'status':'PASS','fixed_source_controls':len(c['controls']),'closed_replay_accesses':17,
       'full_source_edges_checked':checked,'primitive_rotation_identities_checked':primitive,
       'exact_interval_and_fraction_arithmetic':True,'all_oriented_events_agree':True,
       'old_root_DELETE':{'delta_G':'21/8','delta_R':'-21/8','delta_Psi':0},
       'full_B_counterexample':{'n':6,'a':0,'q':2,'z':1,'delta_Psi':-1,'required_upper_bound':-2},
       'rescaling_controls':c['rescaling_controls'],'actual_diagonal_pair_closure':True,
       'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'finite_fits':0,'new_pair_graphs':0,
       'CoarseDouble_refuted':False,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

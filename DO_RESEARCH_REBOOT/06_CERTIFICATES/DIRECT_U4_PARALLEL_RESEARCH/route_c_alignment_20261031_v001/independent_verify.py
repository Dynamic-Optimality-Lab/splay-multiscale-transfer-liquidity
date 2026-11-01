"""Read-only independent arithmetic and pointer replay of the fixed n=6 control.

Uses the previous complete 132-tree metric corpus. No fit, larger corpus, new
potential labels, or source graph search. Does not import the producer.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib,json,sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PRIOR=OUT.parent/'route_c_potential_20261031_v001'
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P

def check(ok,msg):
    if not ok:raise AssertionError(msg)

def tup(t):return None if t is None else (t[0],tup(t[1]),tup(t[2]))
def depths(t,d=0):
    if t is None:return {}
    return {t[0]:d,**depths(t[1],d+1),**depths(t[2],d+1)}
def ordered(t,lo=0,hi=7):
    return t is None or (lo<t[0]<hi and ordered(t[1],lo,t[0]) and ordered(t[2],t[0],hi))
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def neighbours(t):
    if t is None:return
    k,l,r=t
    if l is not None:yield (l[0],l[1],(k,l[2],r))
    if r is not None:yield (r[0],(k,l,r[1]),r[2])
    for ll in neighbours(l):yield (k,ll,r)
    for rr in neighbours(r):yield (k,l,rr)

def main():
    dest=OUT/'independent_audit.json'
    check(not dest.exists(),'exclusive output')
    c=json.loads((OUT/'root_aligned_countercertificate.json').read_text(encoding='utf-8'))
    old=json.loads((PRIOR/'explicit_potential_countercertificate.json').read_text(encoding='utf-8'))
    m=old['metric_certificate'];ts=[tup(t) for t in m['trees']];ids={t:i for i,t in enumerate(ts)}
    n=c['n'];scale=old['scale'];A=c['initial_source_A'];B=c['initial_source_B']
    check(n==6 and scale==8**5 and len(ts)==len(ids)==comb(12,6)//7==132,'complete fixed corpus dimension')
    for t in ts:check(ordered(t) and set(depths(t))==set(range(1,7)),'every valid ordered tree')
    check(sum(map(len,m['adjacency']))==660,'fixed arc count')
    for t,row in zip(ts,m['adjacency']):
        check(set(row)=={ids[u] for u in neighbours(t)},'old primitive metric adjacency independently regenerated')
    Ad,dae=P.splay_trace(ptr(A),6);Ad=raw(Ad)
    Bk,bke=P.splay_trace(ptr(B),1);Bk=raw(Bk)
    check(len(dae)==len(bke)==1,'source two zig operations')
    rows=[m,c['new_metric_row']];anchors=[ids[tup(A)],ids[tup(Ad)]]
    for row,anchor in zip(rows,anchors):
        ds=row['distances'];parents=row['parents']
        check(len(ds)==len(parents)==132 and ds[anchor]==0 and parents[anchor] is None,'metric anchor and dimensions')
        for i,d in enumerate(ds):
            check(type(d) is int and d>=0,'exact finite metric entry')
            if i!=anchor:
                check(parents[i] in m['adjacency'][i] and ds[parents[i]]==d-1,'attained path upper bound')
            for j in m['adjacency'][i]:check(abs(d-ds[j])<=1,'all edge path lower bound')
    check(c['new_metric_row']['anchor_index']==anchors[1],'new anchor identification')
    def scores(b,ds):
        db=depths(b)
        return [sum(8**(5-d)*db[k] for k,d in depths(t).items())-scale*distance for t,distance in zip(ts,ds)]
    v0=scores(B,rows[0]['distances']);vk=scores(Bk,rows[0]['distances']);vd=scores(B,rows[1]['distances'])
    check(v0==old['all_exact_scaled_scores_source'] and vk==old['all_exact_scaled_scores_destination'],'264 inherited candidate scores independently recomputed')
    check(vd==c['all_exact_scaled_DELETE_scores'],'132 new DELETE candidate scores recomputed')
    values={}
    for tag,vs,root in [('source',v0,1),('after_KEEP',vk,1),('after_DELETE',vd,6)]:
        values['U_'+tag]=F(max(vs),scale)
        values['L_'+tag]=F(max(v for t,v in zip(ts,vs) if t[0]==root),scale)
    check({k:str(v) for k,v in values.items()}==c['values'],'all six exact maxima')
    for letter in ('L','U'):
        for op in ('KEEP','DELETE'):
            check(str(values[letter+'_after_'+op]-values[letter+'_source'])==c['increments'][letter+'_'+op],'exact operation increment')
    check(values['L_after_DELETE']-values['L_source']==F(21,8)>2,'DELETE failure')
    def replay(a,b,mode,x,row):
        check(a==row['source_A'] and b==row['source_B'],'full source shared state')
        da=depths(a)[x];db=depths(b)[x] if mode=='K' else None
        pa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':pb,eb=P.splay_trace(ptr(b),x)
        else:pb,eb=ptr(b),[]
        aa,bb=raw(pa),raw(pb)
        q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        check((mode,x,da,db,len(ea),q,z)==(row['mode'],row['key'],row['dA'],row['dB'],row['a'],row['q'],row['z']),'pointer source depths and exact event costs')
        check((len(ea),q,z)==((da+1)//2,0 if db is None else db//2,0 if db is None else db%2),'source cost identities')
        for events,saved in [(ea,row['events_A']),(eb,row['events_B'])]:
            check([[e['case'],e['lo'],e['hi'],e['orient']] for e in events]==saved,'every oriented event matches frame producer')
        check(aa==row['destination_A'] and bb==row['destination_B'],'full pointer destination trees')
        return aa,bb,len(ea),q
    for mode,x,key in [('D',6,'delete_edge'),('K',1,'keep_edge')]:replay(A,B,mode,x,c[key])
    w=c['closed_DELETE_only_witness'];a=w['initial_A'];b=w['initial_B'];total=Q=0
    check(a==b==B and len(w['word'])==len(w['full_replay'])==8,'diagonal full closed word dimension')
    for (mode,x),row in zip(w['word'],w['full_replay']):
        check(mode=='D','DELETE only')
        a,b,aa,qq=replay(a,b,mode,x,row);total+=aa;Q+=qq
    check(a==b==B and total==w['A']==12 and Q==w['Q_B']==0,'exact closure and totals')
    bad=w['full_replay'][w['failed_edge_index']]
    check(bad==c['delete_edge'],'failed edge reached on closed physical walk')
    # Necessary n6 constraints only. Their overlap must NOT be called feasible.
    lD=values['L_after_DELETE']-values['L_source'];uD=values['U_after_DELETE']-values['U_source']
    lK=values['L_after_KEEP']-values['L_source'];uK=values['U_after_KEEP']-values['U_source']
    lower=(lD-2)/(lD-uD);upper=-lK/(uK-lK)
    check(lower==F(5,13) and upper==F(3503,7168) and lower<upper,'n6 necessary interval overlaps')
    # One boundary substitution checks the written n>=13 analytic contradiction;
    # it is scalar rational arithmetic, not a larger-tree evaluation or fit.
    theta_cap=F(4,7);ell13=F(2*13-7,3)
    check((1-theta_cap)*ell13-theta_cap==F(15,7)>2,'analytic threshold arithmetic')
    summary={'status':'PASS','single_tree_states':132,'directed_primitive_arcs_checked':660,
      'exact_metric_rows_certified':2,'candidate_scores_recomputed':396,'exact_values_checked':c['values'],
      'closed_DELETE_accesses':8,'closed_totals':{'A':12,'Q_B':0},'actual_diagonal_pair_closure':True,
      'full_pointer_vs_frame_events_agree':True,'DELETE_violation':'21/8 > 2',
      'n6_necessary_blend_interval_nonempty':True,'n6_interval_sufficiency_claimed':False,
      'analytic_n13_bound':'15/7 > 2','larger_finite_fits':0,'new_pair_graphs':0,
      'CoarseDouble_refuted':False,'certificate_sha256':hashlib.sha256((OUT/'root_aligned_countercertificate.json').read_bytes()).hexdigest()}
    with dest.open('x',encoding='utf-8') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()

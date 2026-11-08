"""One fixed source control and coupled anchor-phase audit; no fit/search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
s=importlib.util.spec_from_file_location('coupled_excursion_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(s);s.loader.exec_module(tu)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(name,d):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def N(k,l=None,r=None):return [k,l,r]
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return N(t[1],jt(t[2]),jt(t[3]))
def path(t,x):
    p=[]
    while isinstance(t,list):
        p.append(t[0])
        if t[0]==x:return p
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present core key')
def subtree(t,x):
    while isinstance(t,list):
        if t[0]==x:return t
        t=t[1 if x<t[0] else 2]
    raise AssertionError('present core key')
def epsilon(t,x):
    p=path(t,x);d=len(p)-1
    if not d:return 0
    if d%2:return 1
    return 2 if (p[1]<p[0])==(p[2]<p[1]) else 1
def splay(t,x):
    v,e=tu.trace(tt(t),x);return jt(v),[list(z) for z in e]
def execute(A,B,word):
    rows=[]
    for i,(mode,x) in enumerate(word):
        da=len(path(A,x))-1;aa,ae=splay(A,x)
        if mode=='KEEP':db=len(path(B,x))-1;bb,be=splay(B,x)
        else:db=None;bb=B;be=[]
        rows.append(dict(occurrence=i,mode=mode,key=x,source_A=A,source_B=B,destination_A=aa,
            destination_B=bb,d_A=da,d_B=db,a=len(ae),q=sum(e[0]!='ZIG' for e in be),
            z=sum(e[0]=='ZIG' for e in be),delta=sum(e[0]!='ZIG' for e in be)-2*len(ae),
            A_events=ae,B_events=be))
        A,B=aa,bb
    return rows
def inflate(t):
    gap=0
    def go(t):
        nonlocal gap
        if t is None:
            v='F'+str(gap);gap+=1;return v
        return N(t[0],go(t[1]),go(t[2]))
    v=go(t);assert gap==14;return v
def mirror(t):
    return None if t is None else N(14-t[0],mirror(t[2]),mirror(t[1]))


def excursions(rows,g):
    anchors=[i for i,r in enumerate(rows) if r['key']==g];M=len(rows);out=[]
    for n,i in enumerate(anchors):
        j=anchors[(n+1)%len(anchors)]
        length=(j-i)%M or M;ids=[(i+k)%M for k in range(1,length+1)]
        internal=[rows[k]['key'] for k in ids[:-1]]
        right=bool(internal) and g<internal[0] and all(a<b for a,b in zip(internal,internal[1:]))
        left=bool(internal) and g>internal[0] and all(a>b for a,b in zip(internal,internal[1:]))
        side='R' if internal and all(x>g for x in internal) else 'L' if internal and all(x<g for x in internal) else None
        startA,startB=rows[i]['destination_A'],rows[i]['destination_B']
        endA,endB=rows[j]['destination_A'],rows[j]['destination_B']
        phase=dict(start_after_block=i,return_block=j,indices=ids,internal_keys=internal,
            ordered=right or left,one_side=side,contains_negative=any(rows[k]['delta']<0 for k in ids),
            B_anchor_child_before=[startB[1][0] if isinstance(startB[1],list) else None,startB[2][0] if isinstance(startB[2],list) else None],
            common_anchor_cut=startA[0]==startB[0]==g)
        if side:
            opp=1 if side=='R' else 2
            farA=subtree(startA,g)[opp];farB=subtree(startB,g)[opp]
            for k in ids:
                assert subtree(rows[k]['source_A'],g)[opp]==subtree(rows[k]['destination_A'],g)[opp]==farA
                assert subtree(rows[k]['source_B'],g)[opp]==subtree(rows[k]['destination_B'],g)[opp]==farB
            phase['opposite_subtree_A']=farA;phase['opposite_subtree_B']=farB
            phase['whole_opposite_subtree_preserved']=True
        if phase['ordered'] and phase['common_anchor_cut'] and all(rows[k]['mode']=='KEEP' for k in ids):
            ea=[epsilon(rows[k]['source_A'],rows[k]['key']) for k in ids[:-1]]
            eb=[epsilon(rows[k]['source_B'],rows[k]['key']) for k in ids[:-1]]
            ret=rows[j];D=sum(2*a-b for a,b in zip(ea,eb));da=sum(ea);db=sum(eb)
            reserve=(da%2)+(D+1)//2
            assert (da,db)==(ret['d_A'],ret['d_B']) and reserve==2*ret['a']-ret['q']>=0
            item=dict(epsilon_A=ea,epsilon_B=eb,D=D,return_depth_A=da,return_depth_B=db,
                source_reserve=reserve,return_delta=ret['delta'])
            if reserve==0:
                child=2 if side=='R' else 1
                before=startB[child][0];after=endB[child][0]
                first=internal[0];last_helper=rows[ids[-2]]
                p=path(last_helper['source_B'],last_helper['key'])[1]
                assert after==p
                assert (before<first<after) if side=='R' else (before>first>after)
                item.update(B_child_before=before,B_child_after=after,first_target=first,
                    source_last_B_parent=p,strict_outward_drift=True)
            phase['ordered_source_formula']=item
        out.append(phase)
    return out


def injection(rows):
    pp=[i for i,r in enumerate(rows) if r['delta']>0]
    if len(pp)!=1 or (rows[pp[0]]['a'],rows[pp[0]]['q'])!=(1,3):return None
    p=pp[0];j=next((p+k)%len(rows) for k in range(1,len(rows)) if rows[(p+k)%len(rows)]['delta']<0)
    aa=[]
    for i,r in enumerate(rows):
        units=[[i,e,b] for e in range(r['a']) for b in(0,1)]
        demands=[[i,e] for e,z in enumerate(r['B_events']) if z[0]!='ZIG']
        for u,d in zip(units,demands):aa.append(dict(A_unit=u,B_double=d,kind='own'))
    aa.append(dict(A_unit=[j,rows[j]['a']-1,1],B_double=[p,2],kind='later-real-negative-block'))
    assert len({tuple(x['A_unit']) for x in aa})==len(aa)
    assert len({tuple(x['B_double']) for x in aa})==len(aa)==sum(r['q'] for r in rows)
    return dict(positive_cut=p,donor_block=j,donor_unit=[j,rows[j]['a']-1,1],assignments=aa,
        startup_credit_used=0,future_period_credit_used=0)


def main():
    V=None
    for x in range(13,0,-1):V=N(x,None,V)
    prep=[('DELETE',x) for t in [4,6,3,7] for x in(t,1)]
    episode=[('KEEP',7),('KEEP',11),('KEEP',1)]
    reset=[('KEEP',x) for t in range(13,1,-1) for x in(t,1)]
    word=prep+episode+reset;rows=execute(V,V,word)
    positives=[i for i,r in enumerate(rows) if r['delta']>0]
    full_closed=rows[-1]['destination_A']==rows[-1]['destination_B']==V
    one_positive=len(positives)==1 and (rows[positives[0]]['a'],rows[positives[0]]['q'])==(1,3)
    phases=excursions(rows,1);all_ordered=all(p['ordered'] for p in phases)
    exact=full_closed and one_positive and all_ordered
    symbolic=execute(inflate(V),inflate(V),word)
    symbolic_closed=symbolic[-1]['destination_A']==symbolic[-1]['destination_B']==inflate(V)
    reflected=execute(mirror(V),mirror(V),[(mode,14-x) for mode,x in word])
    reflected_closed=reflected[-1]['destination_A']==reflected[-1]['destination_B']==mirror(V)
    out=dict(status='VERIFIED_FE02_ORDERED_EXCURSION_CONTROL' if exact else 'FIXED_CONTROL_TARGET_FAILED',
        gate_sha256=sha(HERE/'CE00_FOUR_RULE_GATE.md'),source_word=word,rows=rows,
        symbolic_rows=symbolic,reflected_rows=reflected,anchor=1,excursions=phases,
        reflected_excursions=excursions(reflected,13),symbolic_excursions=excursions(symbolic,1),
        full_pair_closed=full_closed,symbolic_full_pair_closed=symbolic_closed,
        reflected_full_pair_closed=reflected_closed,one_positive=one_positive,positive_blocks=positives,
        all_anchor_excursions_ordered=all_ordered,block_count=len(rows),excursion_count=len(phases),
        A=sum(r['a'] for r in rows),Q=sum(r['q'] for r in rows),
        direct_injection=injection(rows) if exact else None,no_alternative_control_selected=True,
        all14_common_ordered_gap_extension=symbolic_closed,FE02_CD='OPEN',Coarse_Double_counterexample=False)
    save('coupled_excursion_control_certificate.json',out)
    oldp=BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json'
    old=read(oldp);coverage={}
    for g in range(1,14):
        ps=excursions(old['rows'],g)
        bad=next((p for p in ps if not p['ordered']),None)
        coverage[str(g)]=dict(anchor=g,excursion_count=len(ps),qualifies=bool(ps) and bad is None,
            first_bad_excursion=bad,all_excursions=ps)
    good=[int(g) for g,p in coverage.items() if p['qualifies']]
    coverage_result=dict(status='EXACT_FIXED_FE02_ANCHOR_COVERAGE_AUDIT',
        source_certificate_sha256=sha(oldp),anchors=coverage,qualifying_anchors=good,
        original_control=dict(blocks=34,A=46,Q=16,positive_block=7,exactly_one_positive=True),
        unqualified_all_FE02_anchor_coverage='REFUTED—EXACT' if not good else 'not refuted by this fixed audit',
        all_saturated_counterexample_specific_anchor_coverage='OPEN',
        no_new_source_word_or_size_searched=True,FE02_CD='OPEN')
    save('anchor_coverage_certificate.json',coverage_result)
    print(json.dumps(dict(control_status=out['status'],full_closed=full_closed,one_positive=one_positive,
        positives=positives,blocks=len(rows),excursions=len(phases),A=out['A'],Q=out['Q'],
        all_ordered=all_ordered,old_OR_qualifying_anchors=good,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()

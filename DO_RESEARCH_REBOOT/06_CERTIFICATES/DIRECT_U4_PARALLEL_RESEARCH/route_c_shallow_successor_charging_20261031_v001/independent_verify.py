"""Independent pointer-source, block, credit and novelty verification. No producer import."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def ck(ok,msg):
    if not ok:
        raise AssertionError(msg)

def main():
    cp=HERE/'shallow_successor_certificate.json'
    cert=json.loads(cp.read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('pointer_source',ROOT/'python/liquidity/legacy_embedding.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    def ptr(t):
        if t is None:return None
        z=p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if z[side] is not None:z[side]['p']=z
        return z
    def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
    def mirror(t,n):return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]
    def depth(t,x):
        d=0
        while t is not None:
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2];d+=1
        raise AssertionError('absent request')
    def evs(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    calls=0
    def access(t,x):
        nonlocal calls
        d=depth(t,x);out,es=p.splay_trace(ptr(t),x)
        q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        ck(q==d//2 and z==d%2 and len(es)==(d+1)//2,'source event units')
        calls+=1
        return raw(out),es,d,q,z
    def replay(a,b,word,rows):
        ck(len(word)==len(rows),'complete trace')
        for (mode,x),r in zip(word,rows):
            ck((mode,x,a,b)==(r['mode'],r['key'],r['source_A'],r['source_B']),'physical source sharing')
            ap,ae,da,_,_=access(a,x)
            if mode=='K':bp,be,db,q,z=access(b,x)
            else:bp,be,db,q,z=b,[],None,0,0
            ck((ap,bp)==(r['destination_A'],r['destination_B']),'exact source endpoints')
            ck((da,db,len(ae),q,z,evs(ae),evs(be),q-2*len(ae))==
               (r['d_A'],r['d_B'],r['a'],r['q'],r['z'],r['A_events'],r['B_events'],r['delta']),
               'exact costs, patterns and signed deficit')
            a,b=ap,bp
        return a,b
    def blocks(rows):
        n=len(rows);leaders=[i for i,r in enumerate(rows) if r['a']>0]
        out=[]
        for k,i in enumerate(leaders):
            j=leaders[(k+1)%len(leaders)];ids=[i];t=(i+1)%n
            while t!=j:ids.append(t);t=(t+1)%n
            key=rows[i]['key'];ac=rows[i]['a'];q=sum(rows[t]['q'] for t in ids)
            ck(all(rows[t]['a']==0 and rows[t]['key']==key for t in ids[1:]),'maximal A-root block')
            active=[t for t in ids if rows[t]['mode']=='K' and rows[t]['d_B']>0]
            ck(len(active)<=1,'at most one nontrivial B splay per block')
            out.append(dict(leader=i,key=key,indices=ids,a=ac,q=q,delta=q-2*ac,
                            B_active_access=active[0] if active else None))
        return out
    def pairs(rows,bs):
        out=[]
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            j=(i+1)%len(bs);o=bs[j];at=b['B_active_access']
            ck(at is not None,'positive block has genuine B work')
            d=depth(rows[at]['source_B'],o['key']);dd=depth(rows[at]['destination_B'],o['key'])
            ck(d<=1 and b['delta']<=2*o['a']-1,'stated source hypotheses, not assumed universal')
            ck(dd<=3 and o['q']<=1 and o['delta']<=1-2*o['a']<0,'source-derived successor surplus')
            out.append(dict(positive=i,successor=j,successor_key=o['key'],pre_positive_B_depth=d,
                            post_positive_B_depth=dd,former_B_root=rows[at]['source_B'][0],
                            capacity_bound=2*o['a']-1,pair_delta=b['delta']+o['delta']))
        used=[v for pair in out for v in (pair['positive'],pair['successor'])]
        ck(len(used)==len(set(used)) and all(v['pair_delta']<=0 for v in out),'disjoint nonpositive charging pairs')
        ck(all(b['delta']<=0 for i,b in enumerate(bs) if i not in used),'unassigned blocks nonpositive')
        return out
    def check_assignment(rows,bs,ps,allocation):
        belongs={at:i for i,b in enumerate(bs) for at in b['indices']}
        expected_demands={(at,j) for at,r in enumerate(rows) for j,e in enumerate(r['B_events']) if e[0]!='ZIG'}
        expected_credits={(at,j,slot) for at,r in enumerate(rows) for j in range(len(r['A_events'])) for slot in (0,1)}
        got_d=[];got_c=[];allowed={(v['positive'],v['successor']) for v in ps}
        for r in allocation:
            d,cr=tuple(r['demand']),tuple(r['credit'])
            ck(d in expected_demands and cr in expected_credits,'actual B-double and A-StepEv unit')
            bd,bc=belongs[d[0]],belongs[cr[0]]
            ck(bd==bc or (bd,bc) in allowed,'only local or proved immediate-successor credit')
            got_d.append(d);got_c.append(cr)
        ck(set(got_d)==expected_demands and len(set(got_d))==len(got_d),'every demand exactly once')
        ck(len(set(got_c))==len(got_c) and set(got_c)<=expected_credits,'no credit reuse')
        return len(expected_credits)-len(got_c)
    whole=prefix_rows=cut_checks=credit_assignments=0
    novelty_checks=[]
    for wi,w in enumerate(cert['witnesses']):
        initial=w['initial_diagonal'];pr=w['prefix_replay'];rows=w['full_replay']
        ck(len(pr)==2 and len(rows)==len(w['word'])==22,'predeclared finite scope')
        a,b=replay(initial,initial,w['prefix'],pr)
        ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows)
        ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired closure')
        bs=blocks(rows);ps=pairs(rows,bs)
        ck(bs==w['blocks'] and ps==w['charging_pairs'],'all stored source block metadata')
        ck(len(bs)==22 and len(ps)==1 and ps[0]['positive']==0,'sole genuine positive')
        ck((rows[0]['a'],rows[0]['q'],rows[0]['delta'])==(1,3,1),'source positive deficit')
        ck((rows[1]['a'],rows[1]['q'],rows[1]['delta'])==(2,0,-4),'successor pays with unused A credit')
        ck(rows[1]['destination_A']==rows[1]['destination_B'] and w['synchronized_after_cycle_access']==1,'K2 or reflection synchronizes full trees')
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        ck((A,Q,Z,2*A-Q)==(31,11,16,51)==(w['A'],w['Q_B'],w['Z_B'],w['weight']),'complete totals')
        unused=check_assignment(rows,bs,ps,w['credit_assignments'])
        ck(unused==w['unused_credit_count']==51 and len(w['credit_assignments'])==11,'unit certificate totals')
        ck(len(w['all_cuts'])==22,'all cyclic cuts represented')
        for cut,r in enumerate(w['all_cuts']):
            rr=rows[cut:]+rows[:cut];bc=blocks(rr);pc=pairs(rr,bc)
            shifted=[dict(demand=[(a['demand'][0]-cut)%22,a['demand'][1]],
                          credit=[(a['credit'][0]-cut)%22,a['credit'][1],a['credit'][2]])
                     for a in w['credit_assignments']]
            ck(check_assignment(rr,bc,pc,shifted)==51,'same actual credits work at every seam')
            ck(r==dict(cut=cut,accepted=True,positive_blocks=1,charged_demands=11),'cut record')
            cut_checks+=1
        pos=ps[0];root=pos['former_B_root'];next3=[bs[i]['key'] for i in (1,2,3)]
        offset=next(i for i in range(1,len(bs)) if bs[i]['key']==root)
        support=sorted({r['key'] for r in rows if r['mode']=='K'})
        ck(pos['pre_positive_B_depth']==1 and pos['successor_key']!=root,'child case outside former-root successor')
        ck(all(x!=root for x in next3) and offset==7,'old AJ/AK/AL/AM root-return predicates fail')
        ck(support==list(range(1,8)) and w['novelty']['KEEP_support']==support,'seven genuine KEEP keys')
        ck(w['novelty']['positive_blocks']==[0] and w['novelty']['positive_run_lengths']==[1], 'single positive run')
        ck(w['novelty']['former_root']==root and w['novelty']['next_three_keys']==next3 and
           w['novelty']['first_former_root_return_offset']==offset,'stored novelty source data')
        # Necessary conditions directly from pinned old definitions; no old recognizer is run.
        novelty_checks.append(dict(AJ_rejected=True,AK_AL_rejected=True,AM_rejected=True,
          AN_AO_rejected_by_positive_count=True,AP_rejected_by_next_key=True,
          AQ_AR_AS_multi_positive_components_rejected=True,support_le_5_classes_rejected=True))
        whole+=len(rows);prefix_rows+=len(pr);credit_assignments+=len(w['credit_assignments'])
    original,ref=cert['witnesses']
    ck(ref['initial_diagonal']==mirror(original['initial_diagonal'],7) and
       ref['prefix']==[[m,8-x] for m,x in original['prefix']] and
       ref['word']==[[m,8-x] for m,x in original['word']],'exact reflected source word')
    for a,b in zip(original['full_replay'],ref['full_replay']):
        ck(all(b[k]==mirror(a[k],7) for k in ('source_A','source_B','destination_A','destination_B')),'full reflected states')
    ck(len(cert['sharp_transport_controls'])==2,'exact sharp control scope')
    for r in cert['sharp_transport_controls']:
        t,ev,_,_,_=access(r['tree'],r['target'])
        d,dd=depth(r['tree'],r['tracked']),depth(t,r['tracked'])
        ck((t,evs(ev),d,dd)==(r['tree_after'],r['events'],1,3),'sharp depth-3 child transport')
        _,_,rd,rq,_=access(t,r['tracked'])
        ck(rd==3 and rq==r['return_q']==1,'one-double allowance is sharp')
    ck(cert['fixed_witness_searches']==cert['finite_fits']==cert['larger_finite_sizes']==0 and
       cert['matching_terminal_line']=='FROZEN','no search, fitting or frozen-line reopening')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=whole,
       complete_reachability_prefix_rows=prefix_rows,pointer_source_accesses=calls,
       sharp_root_child_controls=2,cyclic_cuts_verified=cut_checks,
       exact_demand_credit_assignments=credit_assignments,no_credit_reuse=True,
       actual_diagonal_reachability=True,actual_pair_closure=True,
       closed_totals_per_orientation=dict(A=31,Q_B=11,Z_B=16,weight=51),
       positive_block_pair=dict(positive_delta=1,successor_delta=-4,pair_delta=-3),
       named_old_class_exclusions=novelty_checks,
       old_recognizers_executed=False,producer_imported=False,allocation_optimizer_used=False,
       universal_CD='OPEN',restricted_class='PROVED—RESTRICTED DOMAIN',
       all_size_proof='SC01; unbounded-support nonvacuity SC02; no finite extrapolation',
       finite_fits=0,larger_finite_sizes=0,matching_terminal_line='FROZEN',
       certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()

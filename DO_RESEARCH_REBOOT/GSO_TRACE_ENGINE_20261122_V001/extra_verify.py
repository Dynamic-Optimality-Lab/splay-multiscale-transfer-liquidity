"""Independent padding, histogram-pump and original-resource path checks."""
import sys
import json
from collections import Counter,defaultdict
from fractions import Fraction
sys.dont_write_bytecode=True
import verify as V
P=V.P;C=V.C


def deflate(t,n):
    gaps=[]
    def walk(v):
        if v is None:return None
        if v.k%5:
            raw=P.raw(v);stack=[v];keys=[]
            while stack:
                q=stack.pop();keys.append(q.k);stack.extend(w for w in (q.l,q.r) if w)
            k=(min(keys)+4)//5;assert sorted(keys)==list(range(5*k-4,5*k))
            lo=5*k-4;expected=(lo+1,(lo,None,None),(lo+2,None,(lo+3,None,None)))
            assert raw==expected;gaps.append(k);return None
        return (v.k//5,walk(v.l),walk(v.r))
    out=walk(t);assert sorted(gaps)==list(range(1,n+1));return out


def padding():
    proof=V.read(V.HERE/'run_001/PADDING_PUMP_CERTIFICATE.json');out=[]
    cert=V.read(V.HERE/'run_001/FINITE_RELAXED_CANDIDATE.json');p={s:Fraction(v) for s,v in cert['values'].items()}
    for i,j,q in ((16,9,1),(17,13,5)):
        z=V.read(V.HERE/f'run_001/trace_{i:02d}.json.gz');old=V.read(V.HERE/f'run_001/trace_{j:02d}.json.gz');n=len(old['source']['initial_A']['children']);op=n+7
        assert z['source']['operations']==[[m,5*x] for m,x in old['source']['operations']]
        assert (z['A'],z['Q_B'],z['K_B'])==(old['A'],old['Q_B'],old['K_B'])
        assert set(z['original_S'])=={5*x for x in old['original_S']}
        assert {tuple(d['id']) for d in z['original_U']}=={tuple(d['id']) for d in old['original_U']}
        assert len(z['steps'])==len(old['steps'])
        for s,t in zip(z['steps'],old['steps']):
            assert s['id']==t['id'] and s['type']==t['type'] and len(s['bits'])==len(t['bits'])
            for b,a in zip(s['bits'],t['bits']):assert b['id']==a['id'] and b['promoted']==5*a['promoted'] and b['demoted']==5*a['demoted'] and b['internal_block'] is None
        for r,t in zip(z['operations'],old['operations']):
            for which in ('full_before','full_after'):
                for a in ('A','B'):assert deflate(P.from_state(r[which][a]),n)==P.raw(P.from_state(t[which][a]))
            assert r['local_only_unchanged']
        r=z['operations'][op-1];rr=[s for s in z['steps'][r['steps'][0]:r['steps'][1]] if s['actor']=='B' and s['type']=='RR']
        assert len(rr)==q and all(Counter(s['signature_before'].values())==Counter(s['signature_after'].values()) for s in rr)
        assert [r['a'],r['q'],r['k']]==[1,q+1,1] and sum(abs(v) for v in r['delta'].values())<=20
        critical_u=[d['id'] for d in z['original_U'] if d['id'][0]==op];assert len(critical_u)==q
        a=P.from_state(r['full_before']['A']);b=P.from_state(r['full_before']['B']);aa=P.from_state(r['full_after']['A']);bb=P.from_state(r['full_after']['B'])
        cores=[P.csize(P.prune(u,v)[0]) for u,v in ((a,b),(aa,b),(aa,bb))];assert cores==[n-2]*3
        slack=Fraction(r['q'])+sum(v*p.get(s,0) for s,v in r['delta'].items())-2*r['a']-2*r['k']
        assert str(slack)==proof['cases'][i-16]['finite_candidate_zero_extension_slack']
        if q==5:assert slack==2>0
        out.append({'index':i,'q':q,'operations':len(z['operations']),'physical_keys':5*n,'unchanged_original_A':z['A'],'unchanged_original_Q_B':z['Q_B'],'critical_original_U':critical_u,'critical_core_sizes':cores,'all_original_steps_matched':True,'every_rigid_gap_and_deflated_pair_checked':True,'all_projected_trees_constant_throughout_period':True,'RR_histogram_cancellation_steps':q,'anonymous_critical_delta_l1':sum(abs(v) for v in r['delta'].values()),'finite_candidate_exact_slack':str(slack)})
    return out


def resource(i,relaxed=False):
    z=V.read(V.HERE/f'run_001/trace_{i:02d}.json.gz')
    b=V.read(V.HERE/f'bank_relax_001/source_{i:02d}_H5.json.gz' if relaxed else V.HERE/f'run_001/bank_{i:02d}.json.gz')
    r=V.read(V.HERE/f'bank_relax_001/resources_{i:02d}_H5.json.gz' if relaxed else V.HERE/f'resources_001/source_{i:02d}.json.gz')
    V.bank_check(z,b)
    steps={tuple(s['id']):s for s in z['steps']};n=len(z['operations']);genuine=[x['id'] for x in z['operations'] if x['k']];vouchers=r['voucher_original_A_units'];chosen=set()
    for j,op in enumerate(genuine):
        prev=genuine[j-1];gap=set(range(prev+1,op+1)) if prev<op else set(range(prev+1,n+1))|set(range(1,op+1))
        unit=tuple(vouchers[str(op)]);assert unit not in chosen and steps[unit]['a']==1 and unit[1] in gap;chosen.add(unit)
    ev=[];owner={x:j for j,part in enumerate(z['blocks']) for x in part}
    for op in z['operations']:
        if op['k']:ev.append({'id':['K',op['id']],'a':0,'q':0,'k':1})
        ev.extend(z['steps'][op['steps'][0]:op['steps'][1]])
    byhub={f'e{j}':e for j,e in enumerate(ev)};used=Counter();loads=Counter();seen=set();available={(u,v):w for u,v,w in b['positive_flows']}
    for a in r['assignments']:
        path=a['path_nodes'];assert path[0]=='s' and path[-1]=='t' and len(path)==len(set(path))
        supply=byhub[path[1]];consumer=byhub[path[-2]];cid=tuple(a['original_B_double']);donor=tuple(a['original_A_unit'])
        assert cid not in seen and consumer['q']==1 and consumer['id']==list(cid);seen.add(cid)
        expected=supply['id'] if supply['a'] else vouchers[str(supply['id'][1])];assert list(donor)==expected and steps[donor]['a']==1
        assert a['via_KEEP_voucher']==bool(supply.get('k',0))
        for u,v in zip(path,path[1:]):used[u,v]+=1;assert used[u,v]<=available[u,v]
        loads[donor]+=1
    assert len(seen)==b['paid']==r['paid'];assert max(loads.values(),default=0)==r['maximum_actual_A_load']<=b['c']+b['d']
    return {'source':i,'assignments':len(seen),'max_A_load':max(loads.values(),default=0),'vouchers':len(vouchers),'all_paths_original_and_capacity_checked':True}


def main():
    pump=padding();resources=[resource(i) for i in range(18)];relaxed=[resource(i,True) for i in (11,12,14,15)]
    full={r['source']:r for r in resources};full.update({r['source']:r for r in relaxed})
    out={'passed':True,'padding':pump,'resources':resources,'relaxed_resources':relaxed,'total_checked_assignments':sum(x['assignments'] for x in resources)+sum(x['assignments'] for x in relaxed),'full_distinct_demands_paid_at_c4_H5':sum(x['assignments'] for x in full.values()),'all_finite_sources_fully_paid':all(full[i]['assignments']==V.read(V.HERE/f'run_001/trace_{i:02d}.json.gz')['Q_B'] for i in range(18)),'root_status':'OPEN','trust':'Separate checker imports no producer/learner/flow-builder. The arbitrary-q source proof remains a mathematical proof, not inferred from these finite samples.'}
    if not (V.HERE/'FINAL_MANIFEST.json').exists():(V.HERE/'EXTRA_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('padding','resources','relaxed_resources')}))


if __name__=='__main__':main()

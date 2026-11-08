"""Independent terminal-profile audit using the frozen two-engine harness.

Never imports the current producer. The frozen harness imports both
unmodified original source engines; none of its output writers are called.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
OLD=BASE/'route_c_fe02_turn_reset_20261101_v001'
HARNESS=OLD/'independent_verify_turn_reset.py'
spec=importlib.util.spec_from_file_location('deep_profile_frozen_independent_harness',HARNESS)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
ck=v.ck


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def pointer_gaps(t,d=0,out=None):
    if out is None:out={}
    if t is None:return out
    if isinstance(t['k'],str):
        ck(t['k'] not in out,'independent-gap-occurrence-distinct');out[t['k']]=d
    else:pointer_gaps(t['l'],d+1,out);pointer_gaps(t['r'],d+1,out)
    return out
def check_row(r):
    actual=v.edge(r['source_A'],r['source_B'],r['mode'],r['key'])
    for k in actual:
        if k in r:ck(actual[k]==r[k],'terminal-certificate-'+k)
def check_injection(rows,d):
    aa=set();bb=set()
    for z in d['assignments']:
        i,e,b=z['A_unit'];j,f=z['B_double']
        ck(0<=i<len(rows) and 0<=e<rows[i]['a'] and b in (0,1),'actual-donor-prefix-A-unit')
        ck(0<=j<len(rows) and 0<=f<len(rows[j]['B_events']) and
            rows[j]['B_events'][f][0]!='ZIG','actual-prefix-B-double')
        ck((i,e,b) not in aa and (j,f) not in bb,'prefix-no-credit-or-demand-reuse')
        aa.add((i,e,b));bb.add((j,f))
    ck(len(bb)==sum(r['q'] for r in rows),'all-actual-prefix-demands-injected')
    ck(rows[5]['delta']<0 and d['donor_A_unit']==[5,rows[5]['a']-1,1],
       'next-nontrivial-block-real-last-unit-donor')
    ck(len(aa)<=2*sum(r['a'] for r in rows),'physical-prefix-capacity-bound')


def main():
    old=read(OLD/'inward_reset_source_certificate.json')
    d=read(HERE/'terminal_depth_profile_certificate.json')
    ck(d['status']=='PASS','predetermined-terminal-source-test-passed')
    ck(d['source_certificate_sha256']==sha(OLD/'inward_reset_source_certificate.json'),
       'exact-inherited-source-certificate')
    v.history(old['rows']);v.history(old['symbolic_rows']);v.history(old['reflected_rows'])
    ck(d['endpoint_A']==old['rows'][-1]['destination_A'] and
       d['endpoint_B']==old['rows'][-1]['destination_B'],'literal-inherited-terminal-pair')
    ck([r['key'] for r in d['core_next_rows']]==list(range(2,17)),
       'complete-next-nonroot-core-target-domain')
    inj=read(HERE/'core_repayment_injection_certificate.json')
    min_core=100
    for r in d['core_next_rows']:
        ck(r['source_A']==d['endpoint_A'] and r['source_B']==d['endpoint_B'],
           'every-next-target-starts-at-same-endpoint')
        check_row(r)
        ck(r['delta']<=-1,'source-proved-core-strict-reserve')
        min_core=min(min_core,-r['delta'])
        check_injection(old['rows']+[r],inj['injections'][str(r['key'])])
        mirror=v.edge(old['reflected_rows'][-1]['destination_A'],
            old['reflected_rows'][-1]['destination_B'],'KEEP',17-r['key'])
        ck((mirror['a'],mirror['q'],mirror['delta'])==(r['a'],r['q'],r['delta']),
           'reflected-whole-source-next-core-costs')
    ga=pointer_gaps(v.pp(d['symbolic_endpoint_A']))
    gb=pointer_gaps(v.pp(d['symbolic_endpoint_B']))
    ck(len(ga)==len(gb)==17,'all-seventeen-unentered-gap-occurrences')
    ck([t['gap'] for t in d['gap_table']]==list(range(17)), 'complete-formal-gap-domain')
    min_gap=100
    for t in d['gap_table']:
        i=t['gap'];a,b=ga['A_F'+str(i)],gb['B_F'+str(i)]
        ck((a,b)==(t['alpha'],t['beta']),'independent-pointer-gap-attachment-depths')
        # Algebraic two-parity minimum; no sampled larger u or fringe sizes.
        even=a+(a%2)-b//2
        odd=(a+1)+((a+1)%2)-(b+1)//2
        ck((even,odd)==(t['reserve_u0'],t['reserve_u1']), 'exact-gap-parity-base-expressions')
        ck(min(even,odd)==t['matched_interior_min_reserve']>=1,
           'every-formal-gap-uniform-positive-base-reserve')
        min_gap=min(min_gap,even,odd)
    esc=read(HERE/'unequal_gap_escape_certificate.json')
    ck(esc['status']=='PASS' and esc['gap']==1,'fixed-unequal-gap-template-succeeded')
    for field in ('rows','reflected_rows'):
        rs=esc[field];v.history(rs)
        ck(len(v.validate(rs[0]['source_A']))==len(v.validate(rs[0]['source_B']))==22,
           'disclosed-single-exact-twenty-two-node-substitution')
        ck([(r['a'],r['q']) for r in rs]==[(1,3),(1,2),(1,2),(1,2),(1,2),(2,4)],
           'source-exact-saturated-unequal-gap-escape')
        ck((rs[-1]['d_A'],rs[-1]['d_B'])==(3,8),'actual-escape-depths-three-and-eight')
        ck(2*sum(r['a'] for r in rs)==14 and sum(r['q'] for r in rs)==15,
           'escape-fourteen-units-fifteen-double-demands')
        ck([i for i,r in enumerate(rs) if r['delta']>0]==[0] and
           all(r['delta']>=0 for r in rs),'exactly-one-positive-otherwise-saturated-open-prefix')
        ck((rs[-1]['destination_A'],rs[-1]['destination_B'])!=
           (rs[0]['source_A'],rs[0]['source_B']),'escape-prefix-not-paired-closed')
    r=esc['rows'][-1]
    Abranch=v.path(r['source_A'],8)[-1];Bbranch=v.path(r['source_B'],8)[-1]
    ck(esc['alpha']==esc['beta']==3 and esc['u_A']==0 and esc['u_B']==5,
       'preselected-gap-depths-not-fitted')
    # Inspect actual endpoint gap bodies, not just their reported lengths.
    source=esc['rows'][0]
    def body_at(T):
        return next(n for n in v.path(T,8) if 8<=n[0]<=13)
    ga0,gb0=body_at(source['source_A']),body_at(source['source_B'])
    ck(v.validate(ga0)==v.validate(gb0)==list(range(8,14)),
       'unequal-interiors-have-identical-complete-gap-key-set')
    ck(v.depth(ga0,8)==0 and v.depth(gb0,8)==5,'independent-fringe-local-depths')
    ck(4*((r['d_A']+1)//2)-esc['beta']==esc['u_B'],
       'exact-unequal-saturation-signature-even-B-depth')
    mixed=[v.mixed(esc['rows'][0]),v.mixed(esc['rows'][-1]),v.mixed(d['core_next_rows'][0])]
    ck(not esc['reachable_closed_FE02_refutation'] and not esc['Coarse_Double_counterexample'],
       'open-prefix-not-upgraded-to-original-theorem-refutation')
    # Fixed old closed controls retain their separate original provenance.
    pg=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    ore=read(BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json')
    for rs in (pg['ordinary_rows'],pg['reflected_rows'],ore['rows']):v.history(rs,closed=True)
    ck(sum(r['a'] for r in pg['ordinary_rows'])==25 and sum(r['q'] for r in pg['ordinary_rows'])==22,
       'inherited-nineteen-block-source-regression')
    pins=read(HERE/'entry_source_pins.json')
    for path,h in pins['files'].items():ck(sha(ROOT/path)==h,'inherited-source-bytes-unchanged')
    result=dict(status='PASS',total_checks=sum(v.counts.values()),checks=dict(sorted(v.counts.items())),
        both_original_engines=True,current_producer_imported=False,frozen_harness_sha256=sha(HARNESS),
        nonroot_core_targets=15,minimum_core_reserve=min_core,formal_gap_pairs=17,minimum_matched_gap_reserve=min_gap,
        all_size_claim='literal source profile plus r(u+2)=r(u)+1, not finite extrapolation',
        fixed_unequal_gap=dict(gap=1,u_A=0,u_B=5,d_A=3,d_B=8,a=2,q=4,total_explicit_keys=22),
        core_size=16,fringe_nodes_in_single_fixed_substitution=6,mixed_physical_owners=mixed,
        actual_reachable_closed_nonvacuity_of_deep_pattern='NOT ESTABLISHED',
        unrestricted_eventual_cyclic_discharge='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        Coarse_Double_counterexample=False,larger_finite_fits=0,source_graph_or_connector_search=False,
        script_sha256=sha(Path(__file__)),certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in
            (ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py')})
    save('independent_audit.json',result)
    print(json.dumps(dict(status='PASS',checks=sum(v.counts.values()),core_targets=15,gaps=17,
        minimum_core_reserve=min_core,minimum_matched_gap_reserve=min_gap,
        fixed_unequal_gap_explicit_nodes=22,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()

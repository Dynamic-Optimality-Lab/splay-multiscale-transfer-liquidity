"""Gate review only: existing exact source rows, no new source construction."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
HARNESS=BASE/'route_c_fe02_turn_reset_20261101_v001/independent_verify_turn_reset.py'
spec=importlib.util.spec_from_file_location('cyclic_review_frozen_original_harness',HARNESS)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
ck=v.ck


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')


def review(rows,g,side,closed):
    v.history(rows,closed=closed)
    ck(rows[0]['source_A'][0]==rows[0]['source_B'][0]==g,'review-initial-common-anchor-cut')
    records=[]
    for i,r in enumerate(rows):
        ck(r['key']>=g if side=='R' else r['key']<=g,'whole-history-mandatory-one-sided-domain')
        A=v.source_lca(r['source_A'],g,r['key'],side)
        B=v.source_lca(r['source_B'],g,r['key'],side,r['mode']=='KEEP')
        dA=v.depth(r['source_A'],r['key'])
        dB=v.depth(r['source_B'],r['key']) if r['mode']=='KEEP' else 0
        nA,nB=dA-A['j'],dB-B['j']
        ck(nA>=0 and nB>=0,'source-local-depths-nonnegative')
        zA,zB=dA%2,dB%2
        delta=r['q']-2*r['a']
        D0,D1=2*A['h']-B['h'],2*A['actual_h']-B['actual_h']
        residual=nB+B['e']-2*(nA+A['e'])-2*zA-zB
        ck(2*delta==D1-D0+residual,'exact-source-cost-telescope-with-residual')
        ck((dA+1)//2==r['a'] and dB//2==r['q'],'actual-events-not-comparison-work')
        records.append(dict(block=i,mode=r['mode'],key=r['key'],source_row_sha256=hashlib.sha256(
            json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            d_A=dA,d_B_performed=dB,j_A=A['j'],j_B=B['j'],n_A=nA,n_B=nB,
            e_A=A['e'],e_B=B['e'],z_A=zA,z_B=zB,D_before=D0,D_after=D1,
            delta=delta,residual=residual))
    summed_delta=sum(r['delta'] for r in records)
    summed_residual=sum(r['residual'] for r in records)
    boundary=records[-1]['D_after']-records[0]['D_before']
    ck(2*summed_delta==boundary+summed_residual,'whole-existing-history-exact-boundary-identity')
    pair_closed=(rows[-1]['destination_A'],rows[-1]['destination_B'])==(
        rows[0]['source_A'],rows[0]['source_B'])
    ck(pair_closed==closed,'actual-full-pair-endpoint-status')
    root_return=rows[-1]['destination_A'][0]==rows[-1]['destination_B'][0]==g
    if root_return:ck(boundary==0,'root-return-already-cancels-scalar-boundary')
    for name in ('A','B'):
        j=sum(r['j_'+name] for r in records);e=sum(r['e_'+name] for r in records)
        actual_change=v.depth(rows[-1]['destination_'+name],g)-v.depth(rows[0]['source_'+name],g)
        ck(e-j==actual_change,'source-frame-depth-conservation-'+name)
    return dict(anchor=g,side=side,blocks=len(rows),records=records,
        sum_delta=summed_delta,sum_residual=summed_residual,Delta_D=boundary,
        root_return=root_return,full_pair_closed=pair_closed,
        A_events=sum(r['a'] for r in rows),B_doubles=sum(r['q'] for r in rows))


def main():
    specifications=[
        ('route_c_pf_positive_gap_closure_20261101_v001','closed_source_certificate.json',
         [('ordinary_rows',1,'R',True),('reflected_rows',13,'L',True),('formal_opaque_fringe_rows',1,'R',True)]),
        ('route_c_fe02_odd_restoration_20261101_v001','odd_restoration_source_certificate.json',
         [('rows',1,'R',True),('reflected_rows',13,'L',True),('symbolic_rows',1,'R',True)]),
        ('route_c_fe02_coupled_excursions_20261101_v001','coupled_excursion_control_certificate.json',
         [('rows',1,'R',True),('reflected_rows',13,'L',True),('symbolic_rows',1,'R',True)]),
        ('route_c_fe02_turn_reset_20261101_v001','inward_reset_source_certificate.json',
         [('rows',1,'R',False),('reflected_rows',16,'L',False),('symbolic_rows',1,'R',False)]),
        ('route_c_fe02_deep_closure_20261101_v001','unequal_gap_escape_certificate.json',
         [('rows',7,'R',False),('reflected_rows',112,'L',False)])]
    results={};sources={}
    for directory,file,fields in specifications:
        p=BASE/directory/file;d=read(p);sources[p.relative_to(ROOT).as_posix()]=sha(p)
        for field,g,side,closed in fields:
            key=directory+':'+field
            results[key]=review(d[field],g,side,closed)
    tr=results['route_c_fe02_turn_reset_20261101_v001:rows']
    ck(tr['root_return'] and not tr['full_pair_closed'] and tr['Delta_D']==0 and
        tr['sum_delta']==1 and tr['sum_residual']==2,
        'inherited-unpaid-root-return-refutes-scalar-endpoint-substitution')
    dc=results['route_c_fe02_deep_closure_20261101_v001:rows']
    ck(dc['sum_delta']==1 and dc['Delta_D']==1 and dc['sum_residual']==1,
       'inherited-unequal-gap-escape-keeps-exact-open-boundary-term')
    pg=read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    v.history(pg['startup_rows'])
    ck(pg['startup_rows'][0]['source_A']==pg['startup_rows'][0]['source_B'],
       'old-W-startup-actual-diagonal-source')
    ck((pg['startup_rows'][-1]['destination_A'],pg['startup_rows'][-1]['destination_B'])==
       (pg['ordinary_rows'][0]['source_A'],pg['ordinary_rows'][0]['source_B']),
       'old-W-source-actual-reachability-prefix')
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():ck(sha(ROOT/p)==h,'all-inherited-raw-bytes-unchanged')
    data=dict(status='PASS',review_only=True,new_proof_campaign_authorized=False,
        inherited_source_hashes=sources,corpora=results,
        source_rows_audited=sum(r['blocks'] for r in results.values()),
        algebra='2 sum(delta)=Delta_D+sum(residual); residual=n_B+e_B-2(n_A+e_A)-2z_A-z_B',
        root_return_does_not_imply_full_pair_closure=True,
        scalar_endpoint_method_obstruction='EXACT on inherited valid-source root return; not a reachable-closed FE02 refutation',
        full_paired_cyclic_residual_sign='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        new_source_states_or_words_constructed=0,new_key_counts_or_fringe_substitutions=0,
        larger_finite_fits=0,source_graph_or_connector_search=False,
        Coarse_Double_counterexample=False)
    save('existing_source_telescope_review_certificate.json',data)
    audit=dict(status='PASS',total_checks=sum(v.counts.values()),checks=dict(sorted(v.counts.items())),
        both_original_engines=True,frozen_harness_sha256=sha(HARNESS),
        source_rows_audited=data['source_rows_audited'],existing_corpora=len(results),
        script_sha256=sha(Path(__file__)),
        certificate_sha256=sha(HERE/'existing_source_telescope_review_certificate.json'),
        proof_campaign_gate='FAIL; review only',FE02_CD='OPEN',
        mathematical_advancement_of_FE02='NONE; completed proof-obligation/method review',
        new_source_states_or_words_constructed=0,new_key_counts_or_fringe_substitutions=0,
        larger_finite_fits=0,original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in
            (ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py')})
    save('independent_source_review.json',audit)
    print(json.dumps(dict(status='PASS',checks=audit['total_checks'],old_source_rows=data['source_rows_audited'],
        old_corpora=len(results),TR_sum_delta=tr['sum_delta'],TR_Delta_D=tr['Delta_D'],TR_residual=tr['sum_residual'],
        proof_campaign_gate='FAIL; review only',FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()

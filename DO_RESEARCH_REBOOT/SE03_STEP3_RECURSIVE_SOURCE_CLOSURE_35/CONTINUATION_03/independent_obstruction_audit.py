"""Separate symbolic obstruction and status audit, no source replay."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    no=read(F/'B_chart_only_source_obstruction.json');live=read(F/'live_degree_release_countercertificate.json')
    for cert in (no,live):
        for n,h in cert['input_sha256'].items():assert sha(P/n)==h
        assert cert['source_queries']==cert['source_engine_calls']==0
        assert cert['UCF35_refuted'] is False
    # Independent sum: low bound2 per genuine, full-V period cost from inherited P/reflection.
    # All-r coefficient accounting uses polynomials (constant, r coefficient).
    P_cost=(-3,3);P_access=(1,1)
    expected=(4*P_access[0]-2*P_cost[0],4*P_access[1]-2*P_cost[1])
    assert expected==(10,-2)
    assert no['forced_cycle_margin_polynomial']==[expected[1],expected[0]]
    assert no['r_min']==6 and no['same_all_H1_source_claimed'] is False
    assert no['other_packetizations_refuted'] is False and no['A_dependent_potentials_refuted'] is False
    # Audit the exact counter-law calculation, not just a negative integer.
    before=[1,5,0];after=[0,4,2]
    L=lambda ds:sum(max(d-2,0) for d in ds)
    assert (L(before),L(after))==(live['L2_source'],live['L2_target'])==(3,2)
    assert 2*live['H']-live['Q']==0 and L(after)-L(before)==-1
    assert live['whole_B_Q']==38 and live['full_numeric_replay'] is False
    reg=read(F/'proof_boxes_v4.json');nodes={b['id']:b for b in reg['boxes']}
    assert nodes['UCF35']['status']=='OPEN' and not reg['A_UCF35'] and not reg['E_UCF35']
    assert nodes['R7_EXCEPTION_REPAYMENT35']['status']=='OPEN'
    assert nodes['GAMMA_COMPLETENESS35']['status']=='OPEN'
    def walk(n,seen):
        assert n not in seen
        for c in nodes[n]['children']:walk(c,seen|{n})
    for n in nodes:walk(n,set())
    prior=read(C/'CONTINUATION_02/campaign_manifest.json')
    for n,h in prior['artifacts'].items():assert sha(C/'CONTINUATION_02'/n)==h
    typed=read(F/'independent_new_theorem_audit.json')
    for n,h in typed['input_sha256'].items():assert sha(F/n)==h
    src=(B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md').read_text()
    assert 'genuine access g immediately before' in src and 'preparation nor reset enters its H count' in src
    report={'status':'PASS_WITH_SOURCE_PROOF_SCOPE','source_queries':0,'source_engine_calls':0,
      'mechanical_checks':['source dependency pins','all-r B-cycle polynomial obstruction',
        'live AF degree-release arithmetic','distinct-witness rather than fictitious common H1 cycle',
        'alternative packetization/A-dependent architecture exclusions',
        'unchanged historical artifacts and previous interface audit','acyclic open-parent proof DAG'],
      'mathematical_review':'same-agent second review of genuine precursor KEEP, A-only preparation/reset, and B-context-preserving construction; finite real D telescoping',
      'not_formal_verification':['source transformation theorem','universal source-word inductions','all-source funding'],
      'trust':'separate static implementation, same research agent; no external or proof-assistant review',
      'UCF35':'OPEN','SI34':'REFUTED_IMMUTABLE','new_architecture_refutation_scope':'B-side-only natural-macro debt only',
      'input_sha256':{p.name:sha(p) for p in sorted(F.glob('*.md'))},
      'certificate_sha256':{n:sha(F/n) for n in ['B_chart_only_source_obstruction.json','live_degree_release_countercertificate.json','proof_boxes_v4.json']}}
    with (F/'independent_obstruction_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print('SOURCE_SYMBOLIC_ARCHITECTURE_OBSTRUCTION_AUDITED; UCF35_STILL_OPEN',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify93_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

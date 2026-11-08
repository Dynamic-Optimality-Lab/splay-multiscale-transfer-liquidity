"""Append-only exact-status research checkpoint, never a Step2 seal."""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;started=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def main():
    e=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert len(pins)==e['pins_verified']==1409
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==e['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
    extra={g:0 for g in e['inherited_group_CPU']};attempts=[]
    for f in sorted(B.glob('run_*_result.json')):
        r=read(f);c=read(B/('controller_'+r['phase']+'_exit.json'))
        assert r['status']=='PASS' and c['error'] is None and r['termination'] is None
        assert r['new_finite_tests']==r['source_engine_calls']==r['old_semantic_rows_replayed']==0
        charged=r['child_CPU']+c['whole_process_CPU_seconds'];extra[r['group']]+=charged
        attempts.append({'phase':r['phase'],'group':r['group'],'status':'PASS','child_CPU':r['child_CPU'],
            'whole_controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charged,
            'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
    assert {p['phase'] for p in attempts}=={'derivation','independent','flux','flux_independent'}
    for f in B.glob('audit_*.py'):
        tree=ast.parse(f.read_text());imports={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
        assert imports<={'json','time','pathlib'}
    ia=read(B/'independent_audit.json');fa=read(B/'flux_independent_audit.json')
    assert ia['requested_completion_achieved'] is fa['requested_completion_achieved'] is False
    assert read(B/'flux_audit.json')['tokens_are_A_bits'] is False
    total=e['prior_uniform_CPU']+sum(extra.values())
    groups={g:{'inherited_CPU':e['inherited_group_CPU'][g],'new_CPU':v,
        'combined_CPU':e['inherited_group_CPU'][g]+v,'cap':e['group_caps'][g]} for g,v in extra.items()}
    assert total<7195 and all(v['combined_CPU']<v['cap'] for v in groups.values())
    out('resources_checkpoint.json',{'prior_uniform_CPU':e['prior_uniform_CPU'],
        'new_CPU_all_children_and_whole_controllers':sum(extra.values()),'cumulative_uniform_CPU':total,
        'global_allowance':7200,'required_reserve':5,'remaining_CPU_including_reserve':7200-total,
        'original_SE03_phase_groups':groups,'attempts':attempts,'new_finite_tests':0,'source_engine_calls':0,
        'old_semantic_rows_replayed':0,'new_canonical_queries':0,'canonical_query_cap':2000000,
        'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,
        'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
        'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
    out('PROOF_DEPENDENCIES.json',{'acyclic_chains':[
        ['completed maximal all-SS theorem','completed exact marked-parent update','certified edge induction','cyclic recent heap and q<=rank-1'],
        ['completed simultaneous density/prefix bounds','threshold-flow identity','deficiency+1 alternating channels','own-channel charge0/1'],
        ['channel masses','completed processed-subtree persistence','exhaustive primitive own-channel tag cases','own-channel K preservation'],
        ['own-channel preservation','exact core10 source heights','complete foreign positive-flux grammar','cyclic creation/removal matching'],
        ['completed actual Omega family','unique physical chart at R11','chart-envelope candidate rejection']],
        'full_source_donor_proof_exists':False,'no_dependency_on_desired_CD_inequality':True})
    out('PARTIAL_CERTIFICATE.json',{'status':'NEW_SOURCE_AND_FOREIGN_FLUX_THEOREMS_NOT_STEP2_CLOSURE',
        'requested_completion_achieved':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN',
        'proved':['maximal-core cyclic recency heap and q<=recent-rank-1',
            'uniform deficiency+1 signed-channel decomposition','own-channel K nonincrease',
            'exhaustive positive total core10 flux: two mirrored source forms',
            'distinct cyclic B-flux creation/removal matching'],
        'refuted_candidate':'min/max envelopes of the old and completed normalized valid five-key chart debts',
        'not_proved':['arbitrary core11 A-dependent signed zero/+1 completion','core10 compatible A funding and channel simulation',
            'complete original B-double-demand to A-bit allocator'],
        'negative_original_cycle_certified':False,'resource_exhaustion_claimed':False,
        'B_flux_tokens_are_A_units':False,'old_allocations_changed':False,'Bank25':25,'R1_R4_preserved':True,
        'inherited_pins_verified':1409,'head':e['head'],
        'independent_audit':'same-agent separate mathematical/source/algebra/ownership derivations, not external review or full compiler formalization'})
    prose('CHECKPOINT.md',f'''# New source and channel-flux theorems; Step2 is NOT closed

The requested universal six-key Step2 proof has NOT been obtained. No
original negative CD cycle or resource-cap boundary is claimed. No
CD6/Step3/Universal-CD/Dynamic-Optimality promotion is made.

MAXIMAL_CORE_RECENCY.md proves that every marked ancestor in an actual
closed maximal core is newer than its descendant in the cyclic recent
order. Therefore q<=recent-rank-1; at core11, q5 is an LRU miss and
q4 belongs to the two oldest marks. All original A helpers remain.

CHART_ENVELOPE_OBSTRUCTION.md rejects the attempted min/max envelope
repair using the completed actual Omega source. The Hamiltonian source
has just ONE valid nine-Score chart; its normalized debt1 cannot pay
the actual -2 packet with any range-two target. This is a counterexample
to the formula, not to CD. No old source rows were replayed.

CORE_DEFICIENCY_CHANNELS.md proves a uniform delta+1 threshold-channel
representation of every actual closed core. Channel words alternate,
every subtree channel mass is0/1, and marked roots have own charge1.
Core10 has two nonempty marked supports, each<=5. This partitions
labels, NOT independently evolving splay executions or A capacity.

OWN_CHANNEL_PRESERVATION.md proves K_h never increases when a channel-h
mark is accessed, by exhaustive actual LL/RR/LR/RL/zig source frames.
CORE10_FOREIGN_FLUX.md goes further: the total K_0+K_1 can increase ONLY
at RR(M0,U0,targetM1) or its mirrored LL(M1,U1,targetM0), each by1.
All other events have nonpositive total flux; a cross-channel transfer
loses a real positive U token as another gains it. Its exact cyclic
creation/removal matching has live count<=4 and distinct actual source
removal ordinals. The independent audit checks the foreign source algebra
in a different representation.

These are B-FLUX tokens, NOT actual A bits. Calling them donors would
omit the required funding bridge. They change no fixed payment and
release no reservation. Two CD5 comparisons cannot both spend the same
actual A trajectory. Neither the channel grammar nor its token matching
establishes core10 repayment. Bank25 is unchanged.

Still missing: a core11 A-dependent completion of the negative seed
through ALL zero/+1 transitions, preserving every paid negative/H2/
paired-H3 row at raised sources; and a core10 source simulation and
disjoint actual A funding theorem. The complete full allocator g needed
by fixed-owner exchange remains absent on the universal domain.

ATTEMPTS_AND_COMPLETION_GAP.md records additional attempted mechanisms
and the primary-source literature check. INDEPENDENT_AUDIT.md gives
the combined source/dependency/ownership audit. Four bounded derivation/
audit phases PASS only their stated scoped results. This is same-agent
separate derivation, not external peer review or full formalization.

R1-R4, original semantics/weights/h0/two sorts/shared midpoint/private
scopes, the frozen graph/solver/observables, all allocations and Bank25=25
remain unchanged. All1409 inherited pins verify; HEAD {e['head']},
branch coarse-double-branch, tracked tree clean. No finite tests, source
engine calls, solver/graph runs or old semantic row replays occurred.

CPU {total:.6f}/7200; remaining {7200-total:.6f} including reserve5.
Original groups symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. All proof
children and whole controllers are charged. Caps were not reset/raised,
and no budget exhaustion is used to explain the mathematical gap.
''')
    out('final_integrity.json',{'status':'PASS_PINS_RESOURCES_AND_SCOPED_CLAIMS',
        'inherited_pins_verified':1409,'head':e['head'],'tracked_tree_clean':True,
        'new_phases':4,'new_phase_failures':0,'R1_R4_preserved':True,'Bank25':25,
        'old_allocations_changed':False,'requested_completion_achieved':False,
        'metadata_CPU_excluded':time.process_time()-started})
    files=sorted(p for p in B.iterdir() if p.is_file())
    out('checkpoint_manifest.json',{'kind':'scoped source research checkpoint; not a universal Step2 seal',
        'files':[{'file':p.name,'sha256':sha(p)} for p in files],
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print(json.dumps({'status':'NEW_SOURCE_FLUX_THEOREMS_STEP2_UNPROVED','requested_completion_achieved':False,
        'inherited_pins_verified':1409,'new_files_pinned':len(files),'cumulative_CPU':total,'Step2':'OPEN'}))
if __name__=='__main__':main()

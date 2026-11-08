"""Append-only scoped checkpoint and provenance; no proof/source execution."""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;started=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def main():
    entry=read(B/'entry.json');pinfile=read(B/'dependency_pins.json')
    for p in pinfile['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert len(pinfile['pins'])==entry['pins_verified']==1253
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==entry['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
    attempts=[];groupadd={g:0 for g in entry['inherited_group_CPU']}
    for p in sorted(B.glob('run_*_result.json')):
        r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'))
        assert r['status']=='PASS' and not c['error'] and r['termination'] is None
        assert r['new_finite_tests']==r['source_engine_calls']==r['old_semantic_rows_replayed']==0
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];groupadd[r['group']]+=charge
        attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
            'controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
            'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
    assert {r['phase'] for r in attempts}=={'source_terms','independent'}
    new=sum(groupadd.values());total=entry['prior_uniform_CPU']+new
    groups={g:{'inherited_CPU':entry['inherited_group_CPU'][g],'new_CPU':v,'combined_CPU':entry['inherited_group_CPU'][g]+v,'cap':entry['group_caps'][g]} for g,v in groupadd.items()}
    assert total<7200-5 and all(v['combined_CPU']<v['cap'] for v in groups.values())
    assert read(B/'independent_audit.json')['status']=='PASS_SCOPED_SOURCE_THEOREMS_ONLY'
    assert read(B/'source_terms.json')['status']=='PASS_FREE_TERM_IDENTITIES'
    for file in ['audit_source_terms.py','audit_independent.py']:
        tree=ast.parse((B/file).read_text())
        imports={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
        assert imports<={'json','time','pathlib'}
    resources={'prior_uniform_CPU':entry['prior_uniform_CPU'],'new_CPU_all_children_and_whole_controllers':new,
        'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
        'original_SE03_phase_groups':groups,'attempts':attempts,'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
        'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
        'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True}
    out('resources_checkpoint.json',resources)
    certificate={'status':'SCOPED_SOURCE_REPAYMENT_THEOREMS_AND_PACKET_LOCAL_OBSTRUCTION',
        'universal_Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','CD6_universal':'NOT_PROMOTED',
        'new_results':[
            {'theorem':'XI_FULL_SOURCE_REPAYMENT','scope':'all twelve arbitrary ordered Fi; stated original 58-operation six-key word; reachable full paired closure',
             'A':72,'QF':34,'QE_recurrent':26,'D3':7,'J3':1,'N':0,'unmatched_P':8,'donor_units':8,
             'source':'XI_SOURCE_FAMILY.md','receipt':'source_terms.json'},
            {'theorem':'GUARDED_NONLOCAL_PACKET_REPAYMENT','scope':'disjoint q5/q1 packets with certified preparation tail triples unclaimed by prior original receipts',
             'source':'GUARDED_NONLOCAL_REPAYMENT.md','universal_guard_proved':False},
            {'theorem':'PACKET_LOCAL_DONOR_EXTENSION_FALSE','scope':'fixed Step1 fE; source-reachable fully closed Xi family; all four packet A bits common-owned and P=1',
             'source':'PACKET_LOCAL_OBSTRUCTION.md','counterexample_to_original_CD':False}],
        'proof_companions':['SOURCE_SCOPE_AND_ABSOLUTE_IDS.md','GAMMA_OMEGA_REUSE.md','INDEPENDENT_AUDIT.md'],
        'inherited_pins_verified':1253,'head':entry['head'],'Bank25':25,'R1_R4_preserved':True,
        'old_fE_and_full_receipts_changed':False,'normalized_M3_used_as_chart_switch_potential':False,
        'native_matching_terminal_changed':False,'h0_raw_changed':False,'source_semantics_changed':False,
        'independent_check':'separate same-agent primitive-rotation derivation plus mathematical ownership/scope audit',
        'external_peer_review':False,'whole_compiler_formalization':False,
        'remaining':['unprepared cold q5/q1 packets','universal original-demand ownership','core10 H1/q4 misses','other cold singletons','zero/+1 cross-class transfers','repeated nonreturning discrepancies'],
        'resource_checkpoint':'resources_checkpoint.json'}
    out('SCOPED_CERTIFICATE.json',certificate)
    prose('CHECKPOINT.md',f'''# Scoped source repayment proved; universal Step2 remains OPEN

Continue from this checkpoint without reopening completed hit, B-return-pulse,
or auxiliary-funding theorems. All1253 inherited pins verify; original HEAD
{entry['head']}, branch coarse-double-branch, tracked tree clean.
R1-R4, Bank25=25, source semantics, existing allocations and caps remain.

The current allowed terminal outcome is a GENUINELY SMALLER SOURCE-LEVEL
REPAYMENT THEOREM, plus a source counterexample to a packet-local extension.
There is NO universal Step2 promotion and NO original negative CD cycle.
Step3 and Universal CD remain OPEN.

1. XI_SOURCE_FAMILY.md proves a new original reachable fully paired-closed
six-key arbitrary-fringe source family with A72,QF34,QE26,D3=7,J3=1,N0.
Eight EXPLICIT actual DELETE-origin tail bits pay its eight unmatched full
demands, keeping every common fE assignment. This covers every original
B-double demand on this family. Its original CD slack is110, not negative.

2. PACKET_LOCAL_OBSTRUCTION.md forces actual fixed-chart debts0->2->1
at its H2/q5,1 pair, using a legal H1/q3 continuation on the SAME chart.
FIFO assigns all FOUR packet A units to common demands, the last at the
next genuine K5. P=1,N=0 nevertheless. Thus packet-local unused/released
donors do not suffice. This does not refute the general nonlocal injection.

3. GUARDED_NONLOCAL_REPAYMENT.md gives a source-driven six-slot allocation
for disjoint packets whose preparation gaps have three actual A events
at auxiliary ordinals>=4. The source triple is reserved before new modules;
prior original owners must be excluded. Max-core q5/q1 structure, not a
global demand/reserve inequality, bounds each packet's demands by six.
The guard is sufficient and has NOT been established universally. It is
not claimed necessary; another source mechanism may fund unguarded cases.

GAMMA_OMEGA_REUSE.md checks compatibility by reusing their completed source
theorems and retaining every old receipt. Omega+'s normalized-chart
residual remains<=-1. No normalized M3 debt is reinstated as a global
chart-switching potential. Alternative fresh receipts are never added
on top of inherited or Xi full-family owners.

SOURCE_SCOPE_AND_ABSOLUTE_IDS.md is MANDATORY: every displayed word role
is mapped to its actual occurrence in the legal auxiliary maximum-debt
period; no warmup or neighboring-copy unit is borrowed. Noncausal use is
only the already stated cyclic block accounting, not a changed native
matching-terminal rule. The fixed erased comparison chart is distinct
from the recent-key cold chart; no cross-chart debt equality is assumed.

Both bounded new derivation and separate primitive-rotation phases PASS.
INDEPENDENT_AUDIT.md states the mathematical scope and ownership audit.
This is a same-agent separate derivation, not external peer review or a
whole-compiler formalization. No finite tests, source-engine calls, graph
extension, solver change or old semantic row replay occurred.

CPU {total:.6f}/7200; remaining {7200-total:.6f}, including reserve5.
Original groups: symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. All children
and whole controllers are charged; no cap was reached, raised or reset.
The 2-million-query and other inherited caps remain. No budget exhaustion
is invoked to explain the remaining mathematical gap.

NEXT OPEN BRIDGE: derive actual donors for every unprepared cold packet
and prove ownership against other cold demands. Then cover core10 H1/q4,
other cold singletons, zero/+1 interactions and repeated nonreturning
discrepancies. Do not treat the guarded theorem as universal donor
existence or replace the requested source assignment by its equivalent
global cardinality inequality. SCOPED_CERTIFICATE.json is authoritative.
''')
    out('final_integrity.json',{'status':'PASS_INHERITED_PINS_AND_SCOPED_STATUS','pins_verified':1253,
        'tracked_tree_clean':True,'head':entry['head'],'Bank25':25,'R1_R4_preserved':True,
        'existing_allocations_unchanged':True,'metadata_CPU_excluded':time.process_time()-started,
        'new_phases':len(attempts),'new_phase_failures':0,'Step2_complete':False})
    files=sorted(p for p in B.iterdir() if p.is_file())
    out('checkpoint_manifest.json',{'kind':'append-only scoped checkpoint; not a universal Step2 seal',
        'files':[{'file':p.name,'sha256':sha(p)} for p in files],
        'inherited_pin_file':'dependency_pins.json','Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print(json.dumps({'status':'SCOPED_CHECKPOINT_SEALED','new_files_pinned':len(files),'inherited_pins_verified':1253,
        'cumulative_CPU':total,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'}))
if __name__=='__main__':main()

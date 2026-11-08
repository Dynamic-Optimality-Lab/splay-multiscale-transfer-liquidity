"""Append-only research checkpoint: complete source class, NOT all Step2."""
import ast,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def main():
    entry=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert len(pins)==entry['pins_verified']==1338
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==entry['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
    attempts=[];extra={g:0 for g in entry['inherited_group_CPU']}
    for f in sorted(B.glob('run_*_result.json')):
        r=read(f);c=read(B/('controller_'+r['phase']+'_exit.json'))
        assert r['status']=='PASS' and not c['error'] and r['termination'] is None
        assert r['new_finite_tests']==r['source_engine_calls']==r['old_semantic_rows_replayed']==0
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];extra[r['group']]+=charge
        attempts.append({'phase':r['phase'],'group':r['group'],'status':r['status'],'child_CPU':r['child_CPU'],
            'controller_CPU':c['whole_process_CPU_seconds'],'charged_CPU':charge,
            'allocated_child_cap':r['allocated_child_cap'],'peak_working_set_bytes_observed':r['peak_working_set_bytes_observed']})
    assert {a['phase'] for a in attempts}=={'mass','mass_independent','negative','negative_independent','zeta','zeta_independent','sweep','sweep_independent'}
    for f in B.glob('audit_*.py'):
        tree=ast.parse(f.read_text());imports={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
        assert imports<={'json','time','pathlib'}
    assert read(B/'sweep_independent_audit.json')['entire_source_class_funded'] is True
    assert read(B/'sweep_independent_audit.json')['universal_Step2'] is False
    new=sum(extra.values());total=entry['prior_uniform_CPU']+new
    groups={g:{'inherited_CPU':entry['inherited_group_CPU'][g],'new_CPU':v,'combined_CPU':entry['inherited_group_CPU'][g]+v,'cap':entry['group_caps'][g]} for g,v in extra.items()}
    assert total<7200-5 and all(v['combined_CPU']<v['cap'] for v in groups.values())
    out('resources_checkpoint.json',{'prior_uniform_CPU':entry['prior_uniform_CPU'],'new_CPU_all_children_and_whole_controllers':new,
        'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
        'original_SE03_phase_groups':groups,'attempts':attempts,'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
        'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
        'metadata_excluded_by_inherited_convention':True,'no_cap_reset_or_raise':True})
    out('PROOF_DEPENDENCIES.json',{'acyclic_chains':[
        ['sealed closed-core density and alternation','processed-subtree persistence','monotone positive-U count','closed maximal all-SS source theorem','marked-parent path compression'],
        ['all-SS source theorem','fan ports and equality case','negative-word width2','explicit B seed psi11','explicit A-dependent Dminus'],
        ['Dminus','paired safe augmentation','new Zeta free terms and full closure','candidate refutation; no full-potential promotion'],
        ['sealed fan/source H1/target-cover facts','monotone sweep forcing','no adjacent deficient episodes','complete full FIFO class allocator','fixed-owner exchange','complete scoped donor theorem'],
        ['sealed final M3 and CD5','completed Step1 actual auxiliary allocator','actual period ID transport','fixed-owner exchange']],
        'no_dependency_on_desired_CD_sum':True,'no_unproved_seed_as_full_potential':True})
    out('PARTIAL_CERTIFICATE.json',{'status':'UNIVERSAL_STRUCTURE_AND_COMPLETE_SOURCE_CLASS_NOT_UNIVERSAL_STEP2',
        'requested_completion_achieved':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN',
        'new_proved_results':[
            {'file':'CLOSED_MAXIMAL_SAME_SIDE.md','scope':'all closed maximal cores2r-1, r>=2','claim':'every B double SS marked-G/U0-P; every unmarked core subtree mass0'},
            {'file':'MARKED_PARENT_PROJECTION.md','scope':'same maximal source class','claim':'B work is marked ancestor depth; update starifies the marked ancestor path'},
            {'file':'SOURCE_EXACT_NEGATIVE_SEED.md','scope':'full core11','claim':'explicit A-dependent one/two-operation seed pays all negative, H2, paired-zero and range rows; H1/q1,q2 still open'},
            {'file':'EXTREME_SWEEP_REPAYMENT.md','scope':'all alternating extreme-sweep six-key histories, arbitrary helpers/fringes/repetitions','claim':'complete physical full allocator and fixed-owner donor injection, no prep guard/rejoin'},
            {'file':'FIXED_OWNER_EXCHANGE.md','scope':'any independently complete full allocator and compatible paid partial injection','claim':'extends all fixed receipts via distinct terminal actual units'}],
        'candidate_rejections':['any B-only full source potential','max(psi11,L)','max(source-exact Dminus,L)'],
        'negative_original_cycle_certified':False,'width2_impossible_claimed':False,
        'open':['A-dependent zero/+1 signed completion on other core11 words, retaining paid rows','full required core10/other six-key coverage','complete universal full allocator'],
        'Bank25':25,'R1_R4_preserved':True,'old_allocations_changed':False,'inherited_pins_verified':1338,
        'head':entry['head'],'independent_audit':'same-agent separate source/algebra/ownership derivations; not external review or complete compiler formalization'})
    prose('CHECKPOINT.md',f'''# Complete extreme-sweep class; universal Step2 remains OPEN

The current request to close all Step2 is NOT achieved. No complete
universal D6 or donor map has been proved. No CD(6), Step3, Universal CD
or Dynamic Optimality promotion is made.

NEW UNIVERSAL SOURCE STRUCTURE:
CLOSED_MAXIMAL_SAME_SIDE.md proves, for ALL closed maximal cores2r-1,
that every unmarked subtree has mass0 and EVERY B double is same-side
with marked grandparent/unmarked parent. Its proof uses processed-root
mass persistence and an irreversible count of positive-mass unmarked
vertices, then full B closure. No actual/abstract row is removed from
the old frozen graph. MARKED_PARENT_PROJECTION.md gives the exact
marked ancestor path-compression consequence; the marked tree is not
an immutable reference metric.

NEW FULL-CORE11 NEGATIVE BASELINE:
NEGATIVE_SEED_CORE11.md proves that negative-only full segment words
have deficit<=2 by a fan-port source grammar. SOURCE_EXACT_NEGATIVE_SEED.md
defines A-dependent Dminus by ONE/TWO actual H1 source operations. It
pays every negative, H2-helper, pairedH3 and range row at core11. Its
remaining seed obligations are H1/q1 and H1/q2. A future raising operation
must also preserve all those paid rows; this is NOT two cases remaining
in all Step2, and the seed is NOT assumed a necessary floor everywhere.

PACKET_SAFE_AUGMENTATION.md separately handles paired-source margins;
the old single-macro augmentation was not silently applied to pairs.
Both naive maxima, with the B seed or source-exact seed, are REFUTED
by ZETA_SOURCE_OBSTRUCTION.md. Zeta is a new fully paired-closed
arbitrary-fringe55-operation family with A71,QF30 and positive slack112.
Its two actual zero H1/q2 transitions force a candidate drop2-><=1.
The family has an explicit six-bit actual tail receipt preserving fE.
This is not a negative CD cycle or a refutation of all width2 functions.

B_ONLY_SOURCE_OBSTRUCTION.md independently excludes every B-only
full-source potential on actual core11 histories, using the old W9
identity plus a new11/9 pulse and actual closed H1 realizations. Different
A contexts are never concatenated into an invented negative cycle.

NEW COMPLETE REPAYMENT CLASS:
EXTREME_SWEEP_REPAYMENT.md covers arbitrary A helpers and root repeats
when genuine targets alternate the two extreme packet/sweep episodes.
Each episode has Q15,H>=7. An H7 episode forces old-extreme A depth>=5
after its five monotone H1 sweep accesses; the next packet H>=4 and
next episode H>=9. Deficient episodes cannot be adjacent. The explicit
previous-deficiency label gives2min(H,8)-15+Delta d>=0. Selecting actual
first-eight-event bits constructs COMPLETE full g, with carried bank<=1
and working queue<=17. A17-operation recurrent witness has A32,QF30 and
a real H2/q5,1 negative packet. No realization of an H7 EPISODE is claimed.

FIXED_OWNER_EXCHANGE.md then gives a source-ID-preserving donor map for
EVERY unmatched full demand in this class, retaining fixed fE(C) and
all compatible paid receipts. All accompanying erased and signed cold
demands are funded. Any active unused reservation requires explicit
valid release or exclusion. Source units/demands are transported into
one actual aligned period; prefix supply and neighboring copies are
never spent. Payment is episode/cyclic block counting, not new native
matching-terminal eligibility. This realizes the proposed full-allocator
route on a whole class, not merely a local spare-bit rule.

STILL OPEN: other core11 target orders and signed zero/+1 completion,
plus core10 and other required six-key coverage. No proof says every
source word is an alternating extreme sweep. Do not promote that class
theorem, the negative seed or the generalized exchange into Step2.

All1338 inherited pins verify. HEAD {entry['head']}; branch coarse-double-branch;
tracked tree clean. R1-R4, Bank25=25, original source semantics, two sorts,
shared midpoint, full private scopes, signed weights, h0 and existing
allocations remain. Completed M1/M2/M3/CD5/Step1 results are reused at
literal scopes. The refuted normalized chart debt is not reinstated.

All8 new bounded derivation/audit phases PASS their STATED scopes.
INDEPENDENT_AUDIT.md includes the separate mathematical coverage/source/
ownership checks; this is same-agent independent derivation, not external
peer review or whole-compiler formalization. No finite population tests,
source-engine calls, solver/graph runs or old semantic row replays occur.

CPU {total:.6f}/7200; remaining {7200-total:.6f}, including reserve5.
Cumulative groups symbolic {groups['symbolic']['combined_CPU']:.6f}/120,
independent {groups['independent']['combined_CPU']:.6f}/300. Every proof
child and whole controller is charged. No cap was reached, raised or reset.
The2-million-query and other limits remain. Budget exhaustion is not
invoked to explain the remaining mathematical gap.
''')
    out('final_integrity.json',{'status':'PASS_PINS_RESOURCES_AND_EXACT_SCOPES','inherited_pins_verified':1338,
        'head':entry['head'],'tracked_tree_clean':True,'Bank25':25,'R1_R4_preserved':True,
        'old_allocations_changed':False,'new_phases':8,'new_phase_failures':0,'requested_completion_achieved':False,
        'metadata_CPU_excluded':time.process_time()-start})
    files=sorted(p for p in B.iterdir() if p.is_file())
    out('checkpoint_manifest.json',{'kind':'research checkpoint with a complete source class; NOT a universal Step2 seal',
        'files':[{'file':p.name,'sha256':sha(p)} for p in files],
        'inherited_pin_file':'dependency_pins.json','Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print(json.dumps({'status':'SCOPED_SOURCE_CLASS_PROVED_UNIVERSAL_STEP2_OPEN','requested_completion_achieved':False,
        'inherited_pins_verified':1338,'new_files_pinned':len(files),'cumulative_CPU':total,'Step2':'OPEN'}))
if __name__=='__main__':main()

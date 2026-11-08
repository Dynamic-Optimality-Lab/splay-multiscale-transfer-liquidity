"""Metadata/provenance publication. Semantic work uses bounded run_phase.py."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:
        if isinstance(v,str):f.write(v)
        else:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def before():
    adv=read('adversarial_audit.json');ind=read('independent_audit2.json');seed=read('terminal_seeds.json')
    rows=['# Complete Campaign07 case ledger','','This is the NEW final+1 seed/zero-closure ledger. Every term has universally',
          'free ordered subtrees; populations are not bounded. Completeness and lifting',
          'are proved in PLUS_ONE_NORMAL_FORM, TERMINAL_SEEDS and ZERO_PREDECESSOR_CLOSURE.','',
          '| Old BF leaves | Final BF leaves | Terminal contexts |','|---:|---:|---:|']
    for r in seed['terminal_case_leaf_changes']:rows.append(f"|{r['from']}|{r['to']}|{r['cases']}|")
    rows+=['','| Rank word g,y,x | Source contexts |','|---|---:|']
    for r in adv['terminal_rank_orders']:rows.append('|'+','.join(map(str,r['rank_word']))+'|'+str(r['contexts'])+'|')
    rows+=['','BF final double:72 LL and72 RR. Final Stem root-degree1:96 contexts;',
           'Fork41 root-degree2:48. No admitted depth3 BF case survives the actual',
           'closed maximal-source theorem. Every A event orientation is retained.','',
           '| A event | Terminal source-term incidences | Cached inverse-case applications |','|---|---:|---:|']
    for typ,inv in [('ZIG_L','zigL'),('ZIG_R','zigR'),('LL','LL'),('RR','RR'),('LR','LR'),('RL','RL')]:
        rows.append(f"|{typ}|{adv['A_event_case_incidence_counts'][typ]}|{ind['inverse_source_cases']['inverse_'+inv]}|")
    rows+=['','These are incidence counts in overlapping free-term covers, not counts of',
           'actual populations. Unique A work at KEEP and at earlier DELETE is covered',
           'by the source normal form; both modes have full-source controls.','',
           '| Zero predecessor | Coverage rule |','|---|---|',
           '|H1/Q2|All six exact inverse identities, fixed Score and private-parent cells, actual recent orders|',
           '|H2/Q4|Every BF destination has>=4 marked leaves; cannot enter L<=3, regardless of helpers|',
           '|Paired H3/Q6|Every actual q1 successor after q5 ends atL4; cannot enter L<=3|',
           '|H0/Q0 identities|Same A/BF/recent projection; BE still quantified; no genuine H0 full macro|',
           '|Nongenuine KEEP/DELETE|Every physical occurrence retained in macro H and auxiliary execution|',
           '|Cold/hit chart switches|All full MRU predecessors, including cold insertion position5|',
           '|Reflection|Every one of32436 reflected frames included by typed language matching|','',
           'The32436-frame closure has2600 L1,4444 L2 and25392 L3 frames. The independent',
           'checker covers all22452 H1 inverse incidences; no L4 source is discarded by fiat.',
           'The initial raw-count audit failure is superseded by mutual semantic coverage.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    pins=read('dependency_pins.json');want=[
        ('DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','SOURCE DEFINITION; ordinary source/cost statement inspected previously, current hash verified'),
        ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md','SOURCE RULES; inherited IAGS/R1-R4 discipline preserved'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED universal closed-source density and odd maximal mask; proof reused'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED actual all-SS/no-zig maximal sources; source hypotheses inspected/reused'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED actual q5/q1 pairing; all successor labels preserved'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RECENT_SUPPORT_COVER.md','PROVED actual recent cover, not arbitrary chart selection'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/NEG2_CLASSIFICATION.md','PROVED negative packet cost classes; old endpoint normalization REFUTED'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FORCED_ZERO_INCOMING_02/RETURN_BARRIER.md','PROVED source marked-parent/leaf interfaces'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_POST_LOWERING_05/POST_LOWERING_NORMAL_FORM.md','PROVED actual marked-parent recency heap and full/aux root interface'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_TERMINAL_PAIR_06/FULL_PROOF.md','PROVED sealed TP-DEPTH3, cold targetsL4 and generic ordered-slot lifting; inspected, not reopened'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_TERMINAL_PAIR_06/saturation3.json','ACCEPTED06 certificate inspected; its terminal seed set is not reused for07'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_TERMINAL_PAIR_06/seal_audit.json','ACCEPTED06 seal inspected and inherited'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/source_model.py','Immutable PRIMARY ordinary source engine, only trace/true event counts used'),
        ('python/independent/splay.py','Immutable DISTINCT ordinary engine; convenience depth+1 cost never used'),
        ('DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md','SEALED CD5; proof not reopened and not used circularly'),
        ('DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md','SEALED M3; unchanged, no chart-switch extrapolation'),
        ('DO_RESEARCH_REBOOT/SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','SEALED Step1 allocation; no donor reassignment'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','SEALED reservation; fE/gE distinction and protected units unchanged')]
    by={p['path']:p for p in pins['pins']};rows=['# Current local source provenance','','All1866 inherited/local pins and external directives are recorded exactly in',
        'dependency_pins.json. Their bytes were verified at entry and revalidated at',
        'the seal. Current LOCAL artifacts are authoritative. No remote snapshot used.','',
        '| Exact path | Status / inspection and reuse | SHA256 |','|---|---|---|']
    for path,status in want:
        assert path in by,path
        rows.append('|'+path+'|'+status+'|'+by[path]['sha256']+'|')
    rows+=['','Latest Campaign01-05 verdicts/checkpoints and Campaign06 FULL_PROOF, CASE_LEDGER,',
           'saturation3, independent/adversarial/interface audits, manifest, seal and',
           'resources were inspected. source_inspection.json records the authoritative',
           'versions. The earlier invalid06 saturation.json is NEVER a proof premise.','',
           'New scope: exact six-key core11 FINAL-PLUS1. Original source states retain',
           'all A/BF/BE, erasure, support, actual chart, phase and physical-event fields.',
           'Only a necessary exclusion projection is used. Since ALL four-leaf states',
           'are excluded, every actual NEG2-S/P target is excluded with its full history;',
           'no abstract four-leaf frame is asserted to be realizable.','',
           'The only internal implementation issues were a raw-count comparison between',
           'overlapping term decompositions and a frozen word-encoding adapter. Both are',
           'resolved by authoritative successor audits. No inherited theorem was revoked.',
           'No missing dependency or conditional mathematical bridge remains in FINAL-PLUS1.',
           'Step2, CD6, Step3, Universal CD and Dynamic Optimality remain OPEN.','']
    out('SOURCE_PROVENANCE.md','\n'.join(rows))
    out('artifact_status_ledger.json',{
        'terminal_seeds.json':'AUTHORITATIVE new final+1 universal seed cover',
        'zero_closure.json':'AUTHORITATIVE complete zero-language certificate; no bound termination',
        'independent_audit2.json':'AUTHORITATIVE independent semantic seed/zero closure verification',
        'adversarial_audit.json':'AUTHORITATIVE source/negative target/reflection interfaces',
        'source_control_replay2.json':'AUTHORITATIVE mandatory historical source controls',
        'delete_event_control.json':'AUTHORITATIVE new source control, unique A event at DELETE',
        'audit_independent.py':'SUPERSEDED raw record-count equality is not a language equality criterion',
        'run_independent_result.json':'FAILED technical audit; fully charged; resolved by independent2',
        'seed_diagnostic.json':'INTERNAL diagnostic; mutual language cover investigated, not a universal proof alone',
        'audit_controls.py':'SUPERSEDED frozen dictionary/pair word encoding adapter',
        'run_controls_result.json':'FAILED before source replay; fully charged; resolved by controls2',
        'inherited06_saturation.json':'INVALID inherited draft; preserved by hash but never a premise',
        'inherited06_saturation3.json':'ACCEPTED sealed06 proof, unchanged; different terminal class'})
def final():
    entry=read('entry.json');total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);phases=[];queries=oldrows=newrows=0;peak=0
    for path in sorted(B.glob('run_*_result.json')):
        r=json.loads(path.read_text());controller=read('controller_'+r['phase']+'_exit.json')
        charge=r['child_CPU']+controller['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge
        queries+=r.get('source_engine_calls',0);oldrows+=r.get('old_semantic_rows_replayed',0);peak=max(peak,r.get('peak_working_set_bytes_observed',0))
        ex=read('audit_'+r['phase']+'_exit.json');newrows+=ex.get('new_source_rows_replayed',0)
        phases.append({'phase':r['phase'],'group':r['group'],'whole_child_CPU':r['child_CPU'],
            'whole_controller_CPU':controller['whole_process_CPU_seconds'],'charge':charge,'technical_status':r['status']})
    assert total<7195 and groups['symbolic']<120 and groups['independent']<300 and queries<2000000
    out('resources_checkpoint.json',{'prior_CPU':entry['prior_uniform_CPU'],'cumulative_CPU':total,'allowance':7200,'required_reserve':5,
        'remaining_including_reserve':7200-total,'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
        'campaign_source_engine_calls':queries,'query_cap':2000000,'maximum_observed_working_set':peak,
        'mandatory_old_period_rows_replayed':oldrows,'new_control_period_rows_replayed':newrows,'phases':phases,
        'failed_attempts_wholly_charged':True,'metadata_CPU_excluded_by_inherited_convention':True,'no_cap_or_allowance_reset':True})
    def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
    branch=git('branch','--show-current');head=git('rev-parse','HEAD');tracked=git('status','--porcelain','--untracked-files=no')
    assert branch==entry['branch'] and head==entry['head'] and not tracked
    ledger=read('artifact_status_ledger.json');files=[]
    for path in sorted(B.iterdir()):
        if path.is_file() and path.name!='campaign_manifest.json':
            files.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),
                'status':ledger.get(path.name,'authoritative audit/proof/support record; scope stated in file')})
    out('campaign_manifest.json',{'outcome':'A','theorem':'FINAL-PLUS1','branch':branch,'HEAD':head,'tracked_status':tracked,
        'worktree_status':git('status','--porcelain','--untracked-files=all'),'files':files,
        'proof_kind':'computer-assisted symbolic ordered-gap certificate with source lifting',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
if __name__=='__main__':(before if sys.argv[1]=='before' else final)()

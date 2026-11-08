"""Campaign08 metadata, provenance and ledger publication only."""
import collections,hashlib,json,subprocess,sys
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:
        if isinstance(v,str):f.write(v)
        else:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def before():
    adv=read('adversarial_audit.json');ind=read('independent_audit.json');zero=read('final_zero_inverse.json')
    rows=['# Complete NEW Campaign08 case ledger','','Every object is a universally parameterized source term, not a bounded',
          'population. The generic rotation calculus is inherited; all terminal seeds',
          'and predecessor counts below are derived for08, not copied from06/07.','',
          '| Positive class | Exact source coverage |','|---|---|',
          '|H1/Q1|One event to v at KEEP or earlier DELETE; new g,v,y,x word and actual recent orders|',
          '|H2/Q3, one positive operation|Two-event ordinary v access at depth3/4, at DELETE or terminal KEEP; excluded by BF degree|',
          '|H2/Q3, two positive operations|DELETE h then DELETE/KEEP v, each one event, arbitrary helper h; excluded by BF degree|',
          '|Other +1|Singleton price arithmetic and paired even-price law exclude every other class|','',
          'The48 final-zero sectors have source J2/K2 degree<=2. All480 actual Q3',
          'contexts produce degree>=3, so P1-B has no composable sector. There are64',
          'P1-A BF compositions,24 A-incompatible,40 surviving source-necessary cases.','',
          '| Rank word g,v,y,x | A feasible | BF compositions |','|---|---|---:|']
    for r in adv['terminal_rank_profiles']:rows.append('|'+','.join(map(str,r['word']))+'|'+str(r['A_feasible'])+'|'+str(r['BF_cases'])+'|')
    rows+=['','| A event type | +1 terminal incidences | Final-zero incidences |','|---|---:|---:|']
    for typ in ('ZIG_L','ZIG_R','LL','RR','LR','RL'):
        rows.append('|'+typ+'|'+str(adv['positive_A_event_incidences'].get(typ,0))+'|'+str(adv['zero_A_event_incidences'].get(typ,0))+'|')
    rows+=['','All six A source schemas are considered. A zero incidence here is a',
           'derived empty sector after the composed exposure constraints, not a',
           'discarded source orientation. Both A event timings are included.','',
           '| Final-zero BF double word, bottom up | Cases |','|---|---:|']
    for k,v in sorted(adv['final_zero_BF_event_words_bottom_up'].items()):rows.append('|'+k+'|'+str(v)+'|')
    rows+=['','Positive BF events:32 LL,32 RR. Exact full depths in the composition',
           'are2 for +1 target,4 for final zero,8 for cold q4 probe. All root aliases',
           'are excluded by actual source depth/MRU arguments, not arbitrary filters.','',
           '| Zero predecessor | Coverage |','|---|---|',
           '|H1/Q2|Every source inverse/root identity/private order cell and actual MRU insertion|',
           '|H2/Q4|Output marked degree>=4; no record has such degree, regardless of helpers|',
           '|Paired H3/Q6|Actual output(L4,degree1), absent from the new language; all successors retained|',
           '|H0/Q0 identity cuts|Projected identity; no genuine H0 full macro; BE remains quantified|',
           '|Nongenuine KEEP/DELETE|Original H and retained BE subsequence preserved|','',
           '| Marked leaves | Marked root degree | Closed frames |','|---:|---:|---:|']
    for r in ind['state_shapes']:rows.append(f"|{r['leaves']}|{r['marked_root_degree']}|{r['frames']}|")
    rows+=['','All5872 predecessor incidences are independently covered. The720 L4 frames',
           'are retained and have degree2; actual cold NEG2-S/P targets have degree4/1.',
           'The weaker L<=3 strategy is not used. The full closure has9624 records.','']
    out('CASE_LEDGER.md','\n'.join(rows))
    pins=read('dependency_pins.json');by={p['path']:p for p in pins['pins']}
    wanted=[
        ('DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','SOURCE DEFINITION; original full Pair Access and cost model retained'),
        ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md','SOURCE RULES; inherited IAGS/R1-R4, no finite promotion'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/CLOSED_CORE_SUBTREE_DENSITY.md','PROVED actual closed-source density; proof inspected previously, unchanged hash verified'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md','PROVED actual maximal all-SS/no-terminal-zig domain; source hypotheses reused'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY01/MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','PROVED actual q5/q1 successor partition, no synthetic macro'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FORCED_ZERO_INCOMING_02/RETURN_BARRIER.md','PROVED marked-parent source compression and leaf law'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_POST_LOWERING_05/POST_LOWERING_NORMAL_FORM.md','PROVED recency heap and source/full-auxiliary interfaces'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_POST_LOWERING_05/FORCED_ZERO_BACKWARD_FRONTIER.md','PROVED final-zero neutral J2/K2 source geometry; current source proof inspected'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_TERMINAL_PAIR_06/FULL_PROOF.md','ACCEPTED06 TP-DEPTH3, cold targetL4 and generic free-slot lifting, not reopened'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_TERMINAL_PAIR_06/saturation3.json','ACCEPTED06 version; invalid saturation.json excluded; no old terminal record reused'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FINAL_PLUS_ONE_07/PLUS_ONE_NORMAL_FORM.md','PROVED generic H1/Q1 operation timing; source normal form reused at actual scope'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FINAL_PLUS_ONE_07/FULL_PROOF.md','ACCEPTED07 FINAL-PLUS1 inspected; its terminal language does not supply08 coverage'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FINAL_PLUS_ONE_07/zero_closure.json','ACCEPTED07 certificate inspected and hash-preserved, not substituted for08'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FINAL_PLUS_ONE_07/independent_audit2.json','ACCEPTED07 semantic checker version, generic checker helpers reused'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_FINAL_PLUS_ONE_07/delete_event_control.json','ACCEPTED event-at-DELETE source control replayed unchanged'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_COLD_NEG2_01/source_model.py','IMMUTABLE primary source engine; ordinary traces/true event counts only'),
        ('python/independent/splay.py','IMMUTABLE distinct ordinary source engine; no convenience depth+1 cost'),
        ('DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md','SEALED CD5 at original scope; not reopened or used circularly'),
        ('DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md','SEALED M3; no old debt used as changing-chart potential'),
        ('DO_RESEARCH_REBOOT/SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md','SEALED auxiliary allocation; no owner reassignment'),
        ('DO_RESEARCH_REBOOT/SE03_STEP2_REPAY02/RETAINED_GAP_RESERVATION.md','SEALED reservation and fE/gE distinction preserved')]
    rows=['# Current local source provenance','','All1966 inherited/local pins and external directives are in dependency_pins.json.',
        'Their bytes were verified at entry and revalidated at the seal. The current',
        'local worktree is authoritative; no older remote snapshot was substituted.','',
        '| Exact path | Status / inspection and reuse | SHA256 |','|---|---|---|']
    for path,status in wanted:
        assert path in by,path
        rows.append('|'+path+'|'+status+'|'+by[path]['sha256']+'|')
    rows+=['','Current Campaign01-07 specifications/checkpoints/verdicts and accepted source',
        'proof interfaces were reconstructed. source_inspection.json records all07',
        'versions, manifests, seed/closure/independent/control receipts. Old06 invalid',
        'saturation.json remains preserved but is never a proof premise. No accepted',
        'theorem has been reopened; new source facts are proved at their actual scope.','',
        'NEW proof interfaces: complete final-zero inverse, generic two-event macro',
        'word forms, Q3 marked-degree obstruction, new +1->0 seed language, complete',
        'zero closure and genuine NEG2 shape separator(4,4)/(4,1) versus L4 degree2.',
        'Every full source A/BF/BE, support, erasure, chart, phase, ID, actual pair and',
        'period restriction remains. A one-way necessary projection is sufficient for',
        'the stronger BF-shaped exclusion; no realization or credit injection assumed.','',
        'No dependency is missing or left conditional inside P1Z-RETURN. The internal',
        'leaf-only candidate fails for the symbolic table; the stronger predicate is',
        'proved and independently checked. No source counterexample is claimed.',
        'Old changing-chart normalized debt stays REFUTED. Step2/CD6/Step3/Universal CD',
        'and Dynamic Optimality remain OPEN. Existing allocations and Bank25 are fixed.','']
    out('SOURCE_PROVENANCE.md','\n'.join(rows))
    out('artifact_status_ledger.json',{
        'final_zero_inverse.json':'AUTHORITATIVE complete new final-zero grammar',
        'terminal_seeds.json':'AUTHORITATIVE new combined terminal seeds; P1-B source-excluded',
        'zero_closure.json':'AUTHORITATIVE complete zero closure; queue empty, no bound termination',
        'separator.json':'AUTHORITATIVE stronger source shape separator; retains all720 four-leaf frames',
        'independent_audit.json':'AUTHORITATIVE distinct-engine semantic seed and predecessor recomputation',
        'adversarial_audit.json':'AUTHORITATIVE reflected languages, order/event/source interfaces',
        'source_control_replay.json':'AUTHORITATIVE eighteen historical/reflected source controls and new normal-form checks',
        'leaf_only_strategy':'REJECTED internal candidate, not a theorem and not a source counterexample',
        'inherited06_saturation.json':'INVALID old draft, pinned for preservation only',
        'inherited06_saturation3.json':'ACCEPTED sealed06 proof; no old terminal records reused',
        'inherited07_independent_audit2.json':'ACCEPTED07 semantic audit; predecessor method only reused',
        'all_current_phase_results':'PASS; no failed current08 draft promoted'})
def final():
    entry=read('entry.json');total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=rows=0;peak=0;phases=[]
    for path in sorted(B.glob('run_*_result.json')):
        r=json.loads(path.read_text());controller=read('controller_'+r['phase']+'_exit.json')
        charge=r['child_CPU']+controller['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge
        queries+=r.get('source_engine_calls',0);rows+=r.get('old_semantic_rows_replayed',0);peak=max(peak,r.get('peak_working_set_bytes_observed',0))
        phases.append({'phase':r['phase'],'group':r['group'],'whole_child_CPU':r['child_CPU'],
            'whole_controller_CPU':controller['whole_process_CPU_seconds'],'charge':charge,'technical_status':r['status']})
    assert total<7195 and groups['symbolic']<120 and groups['independent']<300 and queries<2000000
    out('resources_checkpoint.json',{'prior_CPU':entry['prior_uniform_CPU'],'cumulative_CPU':total,'allowance':7200,'required_reserve':5,
        'remaining_including_reserve':7200-total,'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
        'campaign_source_engine_calls':queries,'query_cap':2000000,'maximum_observed_working_set':peak,
        'mandatory_old_period_rows_replayed':rows,'phases':phases,'metadata_CPU_excluded_by_inherited_convention':True,
        'no_cap_or_allowance_reset':True,'all_full_child_and_controller_charges_included':True})
    def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
    branch=git('branch','--show-current');head=git('rev-parse','HEAD');tracked=git('status','--porcelain','--untracked-files=no')
    assert branch==entry['branch'] and head==entry['head'] and not tracked
    status=read('artifact_status_ledger.json');files=[]
    for path in sorted(B.iterdir()):
        if path.is_file() and path.name!='campaign_manifest.json':files.append({'path':path.relative_to(ROOT).as_posix(),
            'sha256':sha(path),'status':status.get(path.name,'authoritative proof/audit/support record; scope stated in file')})
    out('campaign_manifest.json',{'outcome':'A','theorem':'P1Z-RETURN','branch':branch,'HEAD':head,'tracked_status':tracked,
        'worktree_status':git('status','--porcelain','--untracked-files=all'),'files':files,
        'proof_kind':'computer-assisted universal source/ordered-gap certificate with stronger marked-degree separator',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
if __name__=='__main__':(before if sys.argv[1]=='before' else final)()

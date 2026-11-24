"""Final static integrity, exact graph certificates, source hashes and scope checks."""
import re,subprocess,sys,platform
from collections import Counter
from fractions import Fraction
from sharp02_common import *

def main(label='final_integrity_verification_v001'):
    with Run(label,limit=60) as run:
        pin=read(BASE/'SHARP02_INPUT_HASHES.json');changed={p:{'before':h,'after':sha(REPO/p)} for p,h in pin['sha256'].items() if sha(REPO/p)!=h}
        assert not changed,changed
        for name in pin['vendored_byte_exact']:assert sha(BASE/name)==sha(OLD/name)
        assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='coarse-double-branch'
        assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==pin['source_commit']
        assert not subprocess.check_output(['git','diff','--name-only'],cwd=REPO,text=True).strip()
        assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO,text=True).strip()
        required=['SHARP02_DISCOVERY_REPORT.md','SHARP02_HALL_RESULTS.json','SHARP02_ANCESTRY_EPISODES.json','SHARP02_SOURCE_WITNESSES.json',
                  'SHARP02_COUNTEREXAMPLE_CERTIFICATES.json','SHARP02_THEOREM_LEDGER.md','SHARP02_REPRODUCTION.md']
        assert all((BASE/n).is_file() for n in required)
        report=(BASE/required[0]).read_text(encoding='utf-8');assert list(map(int,re.findall(r'^## (\d+)\.',report,re.M)))==list(range(1,17))
        assert not re.search(r'@[A-Z]+@',report)
        corpus=read(BASE/'SHARP02_SOURCE_WITNESSES.json');names=set()
        for s in corpus['sources']:
            assert s['name'] not in names;names.add(s['name'])
            body={k:s[k] for k in ('initial_A','initial_B','operations')}
            body['diagonal_initial']=s.get('diagonal_initial',s['initial_A']);body['reaching_prefix']=s.get('reaching_prefix',[])
            h=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            assert h==corpus['physical_execution_sha256'][s['name']]
        assert len(names)==148
        write(BASE/'SHARP02_ENVIRONMENT.json',{'implementation_release':'SHARP02-1.0','python_implementation':platform.python_implementation(),
              'python_version':sys.version,'OS':platform.system(),'OS_release':platform.release(),'OS_version':platform.version(),
              'source_commit':pin['source_commit'],'seeded_reproduction_note':'Match this Python runtime for exact generator replay; saved exact physical sources verify without randomized generation',
              'exported_max_population':max(len(s['initial_A']['children']) for s in corpus['sources']),
              'exported_max_period_operations':max(len(s['operations']) for s in corpus['sources'])})
        assert read(BASE/'SHARP02_STANDALONE_VERIFICATION.json')['status']=='PASS'
        hall=read(BASE/'SHARP02_HALL_RESULTS.json');rows=[json.loads(z) for z in (BASE/'SHARP02_SEARCH_LOG_v002.jsonl').read_text().splitlines()]
        assert len(rows)==423 and sum(not z['vacuous'] for z in rows)==214
        for z in rows:
            assert z['Delta']==z['Q']-2*z['A']<=0
            assert z['Q_over_A']==(str(Fraction(z['Q'],z['A'])) if z['A'] else None)
            assert z['U_over_C']==(str(Fraction(z['U'],z['C'])) if z['C'] else None)
            if z['vacuous']:
                assert z['U']==0 and z['tight_nonempty_margin'] is None;continue
            r=z['broad'];weights=z['weights'];adj=z['edges'];units=z['incident_actual_units'];paid=Counter();used=Counter()
            for i,j,n in r['assignment']:
                assert n==1 and j in adj[i] and str(j) in units;paid[i]+=n;used[j]+=n
            assert all(n==1 for n in used.values()) and all(n<=weights[i] for i,n in paid.items()) and sum(paid.values())==r['flow']
            D=r['tight_subset'];near={j for i in D for j in adj[i]}
            assert D and len(near)-sum(weights[i] for i in D)==r['tight_nonempty_margin']
            if r['unmatched']:
                ds=r['deficient_subset'];nn={j for i in ds for j in adj[i]}
                assert sum(weights[i] for i in ds)-len(nn)==r['deficiency']>0
        assert sum(z['unmatched']>0 for z in rows)==1
        assert (BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW.json').read_bytes()==(BASE/'SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW_v002.json').read_bytes()
        assert read(BASE/'SHARP02_NETWORK_TESTS.json')['exact_random_graph_cases']==480
        assert not list(BASE.rglob('__pycache__'))
        info={'status':'PASS','input_pins_unchanged':len(pin['sha256']),'required_deliverables':required,'source_execution_hashes_checked':len(names),
              'all_423_recorded_candidate_graph_cost_rows_checked':True,'nonvacuous_rows':214,'exact_network_test_cases':480,
              'recorded_search_reproduction_same_raw_source_bytes':True,'tracked_git_diff_empty':True,'branch_HEAD_unchanged':True,
              'code_sha256':{p.name:sha(p) for p in BASE.glob('*.py')},'verdict':'TARGETED REFUTATION — Type II; Universal coefficient-two CD remains open'}
        write(BASE/'SHARP02_FINAL_VERIFICATION.json',info);run.check(source_hashes_checked=len(names),search_rows_checked=len(rows))
    # The Run finally receipt is now complete; aggregate exact numerical process
    # measurements without claiming that static authoring probes were timed.
    receipts=[read(p) for p in sorted((BASE/'receipts').glob('*.json'))]
    assert all(r['status']=='PASS' for r in receipts)
    total=sum(r['cpu_seconds'] for r in receipts);peak=max(r['peak_working_set_bytes'] for r in receipts)
    assert total<900 and peak<1024**3
    write(BASE/'SHARP02_RESOURCE_SUMMARY.json',{'numerical_pipeline_cpu_seconds_sum':total,
         'sum_of_stage_wall_seconds':sum(r['wall_seconds'] for r in receipts),'wall_sum_note':'sum of durations, not end-to-end elapsed time; some independent stages ran concurrently',
         'maximum_process_peak_working_set_bytes':peak,'receipts':receipts,'cumulative_CPU_ceiling':900,'per_process_memory_ceiling_bytes':1024**3,
         'scope':'versioned numerical/verification/authoring-script receipts including repeats; static shell reading and small read-only inspection probes are outside this sum',
         'old_SHARP01_initial_CPU_and_peak_memory':'unrecorded, unchanged; no retroactive values supplied','historical_allowances':'not borrowed or reset'})
    summary=read(BASE/'SHARP02_RESOURCE_SUMMARY.json')
    summary['startup_rejections_outside_measured_stage_sum']=read(BASE/'SHARP02_STARTUP_REJECTIONS.json') if (BASE/'SHARP02_STARTUP_REJECTIONS.json').exists() else []
    write(BASE/'SHARP02_RESOURCE_SUMMARY.json',summary)
    print(json.dumps({k:v for k,v in info.items() if k not in ('code_sha256','required_deliverables')}))
    print(json.dumps({'numerical_pipeline_CPU_seconds':total,'maximum_process_peak_working_set_bytes':peak,'receipts':len(receipts)}))

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'final_integrity_verification_v001')

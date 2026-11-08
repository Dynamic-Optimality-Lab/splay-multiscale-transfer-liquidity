"""Metadata/table publication only; semantic checks use the bounded controller."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def write(n,v):
    with (B/n).open('x',encoding='utf-8') as f:
        if isinstance(v,str):f.write(v)
        else:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def before():
    data=json.loads((B/'grammar.json').read_text());ind=json.loads((B/'independent_audit.json').read_text())
    rows=['# Complete symbolic terminal root-order table','','Every row denotes arbitrary ordered gap substitutions. Rank0 is the minimum',
          'among the word keys. Both engines independently derive this table; the',
          'source/frame lifting proof is FULL_PROOF.md section4. False means the',
          'entire universally parameterized one-event word has no A frame.','',
          '| Root rank word | BF term contexts | A word feasible |','|---|---:|---|']
    for r in data['order_profiles']:rows.append('| '+','.join(map(str,r['rank_word']))+' | '+str(r['B_templates'])+' | '+('YES: requires original provenance' if r['A_compatible'] else 'NO')+' |')
    rows += ['','All144 preceding-packet contexts are covered. Only two reflected orders',
             'survive locally, in eight BF contexts; their full cheap-prefix provenance',
             'is excluded by the closed260-frame backward certificate, not by this table alone.','']
    write('CASE_LEDGER.md','\n'.join(rows))
    pins=json.loads((B/'dependency_pins.json').read_text());wanted=['CLOSED_CORE_SUBTREE_DENSITY.md','CLOSED_MAXIMAL_SAME_SIDE.md','MAXIMUM_DEPTH_SUCCESSOR_REPAYMENT.md','RECENT_SUPPORT_COVER.md','NEG2_CLASSIFICATION.md','RETURN_BARRIER.md','POST_LOWERING_NORMAL_FORM.md','FORCED_ZERO_BACKWARD_FRONTIER.md','source_model.py','python/independent/splay.py']
    rows=['# Direct source provenance','','All inherited pins are in dependency_pins.json. Direct proof sources were',
          'read from the current LOCAL worktree. No remote snapshot was substituted.',
          'Each proof source below was inspected; completed old executable checks reused.','',
          '| Exact path | SHA256 |','|---|---|']
    for p in pins['pins']:
        if any(p['path'].endswith(w) for w in wanted):rows.append('| '+p['path']+' | '+p['sha256']+' |')
    rows += ['','Status distinctions: inherited density/SS/pairing/recency and cost grammar',
             'PROVED; old changing-chart normalization REFUTED; TP now PROVED by the new',
             'symbolic certificate; full Step2/Step3/Universal CD OPEN. Old CD5/M3/Step1',
             'remain sealed at their original scopes. No circular dependence on CD6.','']
    write('SOURCE_PROVENANCE.md','\n'.join(rows))
    ledger={'counterattack':'INCONCLUSIVE finite constructive family; not a proof premise',
        'preimage':'INCONCLUSIVE bounded source search; preparation group closed only at its declared fixed-core scope',
        'backward':'local relaxed A/B guard insufficient; no cheap negative-source provenance',
        'backward2':'INCONCLUSIVE local predecessor family',
        'grammar':'USED: complete symbolic context/frame calculus with lifting',
        'sourceclosure':'SCC computation NOT NEEDED; only the eight contexts later independently regenerated are used',
        'tailrefine':'USED: full eleven-Score identity refinement of surviving A skeletons',
        'saturation':'INVALID gap vocabulary mismatch; no semantic evidence',
        'saturation2':'SUPERSEDED reachable-component restriction not needed',
        'saturation3':'USED final complete density-grammar predecessor certificate',
        'independent':'USED separate-engine universal forward frame/closure audit',
        'adversarial':'USED omitted-case, target, helper and orientation audit',
        'interfaces':'USED admission, identity and final state-kind audit'}
    write('research_status_ledger.json',ledger)
def final():
    entry=json.loads((B/'entry.json').read_text());total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);phases=[];queries=0;peak=0
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());q=json.loads((B/('controller_'+r['phase']+'_exit.json')).read_text())
        charge=r['child_CPU']+q['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge;queries+=r.get('source_engine_calls',0);peak=max(peak,r.get('peak_working_set_bytes_observed',0))
        phases.append({'phase':r['phase'],'group':r['group'],'whole_child_CPU':r['child_CPU'],'whole_controller_CPU':q['whole_process_CPU_seconds'],'charge':charge,'technical_status':r['status']})
    assert total<7195 and groups['symbolic']<120 and groups['independent']<300 and queries<2000000
    write('resources_checkpoint.json',{'prior_CPU':entry['prior_uniform_CPU'],'cumulative_CPU':total,'allowance':7200,'required_reserve':5,
        'remaining_including_reserve':7200-total,'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],
        'campaign_source_engine_calls':queries,'query_cap':2000000,'maximum_observed_working_set':peak,'phases':phases,
        'metadata_CPU_excluded_by_inherited_convention':True,'no_cap_or_allowance_reset':True})
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    status=subprocess.check_output(['git','status','--short','--untracked-files=all'],cwd=ROOT,text=True);tracked=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True)
    assert branch==entry['branch'] and head==entry['head'] and not tracked
    files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file() and p.name!='campaign_manifest.json']
    write('campaign_manifest.json',{'outcome':'A','theorem':'TP-DEPTH3','proof_kind':'complete symbolic ordered-gap certificate with explicit lifting',
        'branch':branch,'HEAD':head,'tracked_status':tracked,'worktree_status':status,'files':files,'Step2':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
if __name__=='__main__':
    (before if sys.argv[1]=='before' else final)()

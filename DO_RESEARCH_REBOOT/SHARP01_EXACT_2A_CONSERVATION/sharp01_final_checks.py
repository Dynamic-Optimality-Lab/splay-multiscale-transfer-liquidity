"""Static final data/flow/preservation checks; no source replay."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,re,subprocess,time
BASE=Path(__file__).resolve().parent;REPO=BASE.parents[1]
def read(n):return json.loads((BASE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
started=time.process_time()
idx=read('SHARP01_GAP_LEDGER.json')['ledgers'];sources=read('SHARP01_SOURCE_WITNESSES.json')['sources']
rr=read('SHARP01_RESULTS.json');uu=read('SHARP01_PHYSICAL_INCIDENCE.json');by={s['name']:s for s in rr['sources']}
for src,it,summary,inc,unit in zip(sources,idx,rr['sources'],rr['incidence'],uu['sources']):
    assert src['name']==it['name']==summary['name']==inc['source']==unit['source']
    assert sha(BASE/it['path'])==it['sha256']
    l=read(it['path']);assert l['summary']==summary and l['source']==src
    gs={g['gap_index']:g for g in l['gaps']}
    if gs:
        assert sum(g['H'] for g in gs.values())==summary['A']
        assert sum(g['q'] for g in gs.values())==summary['Q']
        assert sum(g['u']-g['c'] for g in gs.values())==summary['Delta']
    else:assert summary['Q']==0
    for numerator,label in (('Q','Q_over_A'),('U','U_over_A'),('C','C_over_A')):
        assert summary[label]==(str(Fraction(summary[numerator],summary['A'])) if summary['A'] else None)
    for name,r in inc['rules'].items():
        du=Counter();cu=Counter()
        for i,j,amt in r['assignment']:
            assert isinstance(amt,int) and amt>0 and j in r['edges'][str(i)]
            du[i]+=amt;cu[j]+=amt
        assert all(v<=gs[i]['u'] for i,v in du.items()) and all(v<=gs[j]['c'] for j,v in cu.items())
        assert sum(du.values())==r['flow']
        if r['success']:assert r['flow']==summary['U']
        else:
            ds=r['deficient_subset'];near={j for i in ds for j in r['edges'][str(i)]}
            assert sum(gs[i]['u'] for i in ds)-sum(gs[j]['c'] for j in near)==r['Hall_deficiency']>0
    for name,r in unit['rules'].items():
        used=Counter();du=Counter();reasons={(i,j) for i,j,y,eid in r['edge_reasons']}
        for i,j,amt in r['assignment']:
            assert amt==1 and j in r['edges'][str(i)] and (i,j) in reasons
            used[j]+=amt;du[i]+=amt
        assert all(v==1 for v in used.values()) and all(v<=gs[i]['u'] for i,v in du.items())
        assert sum(du.values())==r['flow']
        if r['success']:assert r['flow']==summary['U']
        else:
            ds=r['deficient_subset'];near={j for i in ds for j in r['edges'][str(i)]}
            assert sum(gs[i]['u'] for i in ds)-len(near)==r['Hall_deficiency']>0
    for suffix,mult in (('_reflected',1),('_copies3',3)):
        if summary['name'].endswith(suffix):
            original=by[summary['name'][:-len(suffix)]]
            assert all(summary[k]==mult*original[k] for k in ('A','Q','U','C','Delta','VA','ZB','KB','PA','NA','DB'))
report=(BASE/'SHARP01_DISCOVERY_REPORT.md').read_text()
assert [int(x) for x in re.findall(r'^## (\d+)\.',report,re.M)]==list(range(1,19))
assert not re.search(r'@[A-Z]+@',report)
manifest=read('SHARP01_INPUT_MANIFEST.json')
old=manifest['input_sha256']['DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/exp01_sources.py']
snapshot=(BASE/'sharp01_sources.py').read_text().replace('from sharp01_oracle import vine, Tree, Replay','from exp01_oracle import vine, Tree, Replay')
assert hashlib.sha256(snapshot.encode()).hexdigest()==old
changes={rel:{'before':h,'after':sha(REPO/rel)} for rel,h in manifest['input_sha256'].items() if sha(REPO/rel)!=h}
assert set(changes)<={'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/exp01_sources.py','DO_RESEARCH_REBOOT/IAGS12_GLOBAL_BOUNDARY_REUSE.md'},changes
assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='coarse-double-branch'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==manifest['commit']
assert subprocess.check_output(['git','diff','--name-only'],cwd=REPO,text=True).strip()==''
assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO,text=True).strip()==''
assert not list(BASE.rglob('__pycache__'))
code_pins={p.name:sha(p) for p in sorted(BASE.glob('*.py'))}
newer=REPO/'DO_RESEARCH_REBOOT/IAGS12_GLOBAL_BOUNDARY_REUSE.md'
out={'status':'PASS','source_count':len(sources),'all_ledger_hashes_match':True,'all_exact_flows_and_Hall_witnesses_checked':True,
     'reflection_and_three_copy_totals_match':True,'report_sections':18,'source_snapshot_matches_pre_change_original':True,
     'tracked_git_diff_empty':True,'branch_HEAD_unchanged':True,'concurrent_changes':changes,'final_code_sha256':code_pins,
     'newer_completed_report_sha256':sha(newer),'cpu_seconds':time.process_time()-started}
out['newer_EXP01_discovery_report_sha256']=sha(REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY/EXP01_DISCOVERY_REPORT.md')
(BASE/'SHARP01_FINAL_VERIFICATION.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k not in ('final_code_sha256','concurrent_changes')}))

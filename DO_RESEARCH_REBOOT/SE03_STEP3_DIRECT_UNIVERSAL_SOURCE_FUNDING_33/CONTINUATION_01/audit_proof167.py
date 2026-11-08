"""Construct a real six-key own receipt and its canonical frozen r7 prior
on the NEW source, then apply the unchanged original full-h exchange.
No historical owner is substituted or removed. No source primitive rerun.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_JOINT_REPAIR_03';P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mp(a):return {tuple(x['demand']):tuple(x['unit']) for x in a}
def pairs(a):return [{'demand':d,'unit':u} for d,u in sorted(a.items())]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def core(t,M):
    if t is None:return set()
    a=core(t[1],M)|core(t[2],M)
    if a or t[0] in M:a.add(t[0])
    return a
def main():
    file=F/'actual_monotone_return_source.json';z=json.loads(file.read_text());rows=z['period_rows'];E=set();fE={};checks=[];ends=[i for i,r in enumerate(rows) if r['genuine_E']]
    marks={r['key'] for r in rows if r['genuine_E']};assert len(marks)==6
    cores={tuple(sorted(core(r['BE_before'],marks))) for r in rows};assert len(cores)==1;kE=len(next(iter(cores)))
    for j,end in enumerate(ends):
        pre=ends[j-1];ii=list(range(pre+1,end+1)) if pre<end else list(range(pre+1,len(rows)))+list(range(end+1))
        rr=[rows[i] for i in ii];uu=[(r['t'],a,b) for r in rr for a in range(1,r['a']+1) for b in (0,1)];dd=[(r['t'],a) for r in rr for a in range(1,r['qE']+1)]
        assert len(uu)>=len(dd) and len(uu)//2>=1 and len(dd)<=2
        fE.update(zip(dd,uu));E.update(dd);checks.append({'end_t':rows[end]['t'],'H':len(uu)//2,'Q':len(dd),'source_license':'Q<=2 and actual retained-genuine macro H>=1; direct natural own rule','occurrences':[r['t'] for r in rr]})
    assert set(fE)==E and len(set(fE.values()))==len(E)
    h0=mp(z['funding']['h0']);h=mp(z['funding']['full_h']);D=set(h);U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
    C=D&E;l={d:fE[d] for d in C}
    xp=P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py';sp=P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py'
    X=load('original_exchange167',xp);S=load('original_source_funding167',sp)
    prior=X.exchange(D,U,l,h0);a=prior['allocation'];answer=S.extend(D,U,a,h);licensed=X.exchange(D,U,l,h)
    assert answer['allocation']==licensed['allocation'] and licensed['total']
    assert all(answer['allocation'][d]==u for d,u in a.items())
    out('actual_auxiliary_owner_extension.json',{'status':'PRODUCER_ACTUAL_SIX_KEY_SOURCE_RECEIPT_AND_ORIGINAL_FROZEN_EXTENSION',
      'input_scope':'NEW period[66,130], not a replacement for any old fE/a0; no earlier input owner supplied for this new test',
      'erased_key':3,'auxiliary_genuine_keys':sorted(marks),'auxiliary_core_size':kE,
      'auxiliary_source_license':'actual six-key source own-solvent rule, all retained-genuine Q<=2,H>=1; source period and original costs checked separately by fresh replay audit',
      'fE':pairs(fE),'auxiliary_macro_receipt':checks,'common':sorted(C),'auxiliary_only_retired':sorted(E-D),
      'old_canonical_effective_a0':pairs(a),'old_frozen_count':len(a),'actual_unpaid_before_repair':sorted(D-set(a)),
      'new_actual_pairs':pairs(answer['additions']),'full_allocation':pairs(answer['allocation']),'paths':answer['paths'],
      'all_old_values_preserved':True,'fE_unchanged':True,'original_common_exchange_agrees':True,
      'working_bank':'independent full-h trace2 from the source block theorem; auxiliary/old maps are archived proof receipts, not additional unused tokens',
      'source_queries':0,'source_engine_calls':0,'principal_C33':'OPEN',
      'input_sha256':{str(file):pin(file),str(xp):pin(xp),str(sp):pin(sp)}})
    assert time.process_time()-START<CAP-1
    print(json.dumps({'status':'ACTUAL_SOURCE_FROZEN_EXTENSION_READY','auxiliary_core':kE,'fE_count':len(E),'old_frozen_count':len(a),'newly_funded':len(answer['additions']),'all_old_fixed':True,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof167_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

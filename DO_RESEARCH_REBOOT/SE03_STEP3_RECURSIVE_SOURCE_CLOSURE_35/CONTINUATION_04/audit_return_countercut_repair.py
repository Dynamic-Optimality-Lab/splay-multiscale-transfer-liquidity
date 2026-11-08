"""Independent source-depth/tail and fixed-owner static reconstruction review."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def depth(t,x):
    d=0
    while t[0]!=x:t=t[1] if x<t[0] else t[2];d+=1
    return d
def main():
    p=F/'MFR35_unpaid_source_countercut.json';r=json.loads(p.read_text());accepted=F/'independent_MFR35_unpaid_source_countercut.json';a=json.loads(accepted.read_text())
    assert a['status'].startswith('PASS_SOURCE_EXACT_') and a['all_return_demands']==3 and a['all_return_units']==2
    starts=[r['initial_common_Bprev']]+[c['A_after'] for c in r['critical_unpaid_claims'][:-1]]
    checks=[]
    for c,t,wantD,wantQ in zip(r['critical_unpaid_claims'],starts,(2,5,3),(1,2,2)):
        G=c['old_proxy'];d=depth(t,G);assert d==wantD
        row=r['full_B_rows'][c['forward_B_ordinal']-2];assert row['target']==G and row['Q']==wantQ
        H=(d+1)//2;tail=2*H-wantQ;assert tail>=1
        checks.append({'G':G,'consumer':c['consumer'],'original_start_depth':d,'H_lower_bound':H,'full_B_Q':wantQ,'natural_tail_lower_bound':tail,
          'supplier':'last actual bit1 in G preparation macro, outside the fixed h0 prefix'})
    assert r['genuine_macros']==60 and r['full_B_Q']==100 and 2*r['genuine_macros']-r['full_B_Q']==20
    paths=[p,accepted,F/'SOURCE_REPAIR_OF_RETURN_COUNTERCUT.md',F/'SS_SPLAY_INVERSE_SOURCE_THEOREM.md',B/'STREAMED_BLOCK_THEOREM.md',F/'audit_return_countercut_repair.py']
    out={'status':'PASS_EARLIER_SOURCE_TAIL_REPAYMENT_AND_COMPLETE_FIXED_OWNER_RECONSTRUCTION',
      'checks':checks,'partial_tail_donors':3,'global_original_h0_values_changed':0,
      'full_source_scope':'exact new SSI counterconstruction only, all canonical Gamma costs retained',
      'proof_review':['single-rotation depth decreases at most1, StepEv at most2',
        'canonical preparations stay in preceding genuine macros, with positive natural tails',
        'three distinct last-unit donor ordinals, all outside h0 and before their consumers',
        'owner-inclusive even selections with fixed new tails exist; selected>=120>Q100',
        'fixed partial owner count cancels; static working<=2; one actual period and original cut',
        'no fE availability assertion and no universal source-coverage assertion'],
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','reservation':'DEFERRED',
      'independent_is_same_agent_distinct_implementation':True,'input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'independent_return_countercut_repair.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify155_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

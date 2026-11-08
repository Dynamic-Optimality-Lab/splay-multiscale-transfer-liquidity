"""A decisive peeling-law control on an independently different A geometry.
BF/BE original primitive states reused by hash; exactly16 fresh A splays.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2])
sys.path.insert(0,str(C));import retirement_pools as R
sp=importlib.util.spec_from_file_location('accepted_functional_splay',B/'audit_core39.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);S.CAP=CAP;S.QCAP=min(16,QCAP);S.START=START;S.CALLS=0
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    path=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json';assert R.pin(path)=='5e00eb81aed692ab9982b5b4e3401e89827245a52748cf770ac21fa26d00e4b4'
    old=json.loads(path.read_text());keep=[r for r in old['period_rows'] if r['kind']=='K'];assert len(keep)==16 and QCAP>=16
    def vine_marked(x):return None if x>13 else (x,None if x==1 else (x-1,None,None),vine_marked(x+2))
    initial=A=vine_marked(1);rows=[]
    for i,r in enumerate(keep):
        aa=A;A,a,_,events=S.splay(A,r['key'],True)
        rows.append(dict(t=i+1,kind='K',key=r['key'],a=a,qF=r['qF'],qE=r['qE'],A_before=aa,A_after=A,BF_before=r['BF_before'],BF_after=r['BF_after'],BE_before=r['BE_before'],BE_after=r['BE_after'],A_events=events,chart_F=r['chart_F'],chart_E=r['chart_E'],inherited_B_occurrence=r['t']))
    assert A==initial
    assert R.freeze(rows[0]['BF_before'])==R.freeze(rows[-1]['BF_after']) and R.freeze(rows[0]['BE_before'])==R.freeze(rows[-1]['BE_after'])
    obj=dict(status='NEW_COMPRESSED_A_ORIGINAL_SOURCE_PRODUCER',initial_A=initial,period_rows=rows,period=[1,16],absolute_coordinates='t=p+i, 1<=i<=16; p is length of accepted reaching prefix plus finite A-only Gamma; ONE actual period',reaching_prefix='accepted original C33 prefix; DELETE Gamma(old A boundary, initial_A). Published same-key ordinary-splay transformation theorem proves this finite word exists, all operations outside I; no numerical prefix word/cost claimed',reaching_dependency=str(B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md'),inherited_B_source=str(path),inherited_B_source_sha256=R.pin(path),full_support=[1,3,5,7,9,11,13],erased_key=3,old_source_not_modified=True,no_fixed_fE_or_a0_replaced=True,source_queries=S.CALLS,source_engine_calls=S.CALLS)
    # Preserve raw completed source BEFORE graph postprocessing.
    out('compressed_A_closed_source.json',obj)
    m=R.build(R.normalize(obj,'c33'));assert m['scope']=='MAXIMAL_CORE';mm=m['macros'];NN=[{tuple(u) for u in z['N']} for z in mm];active=set(range(len(mm)));steps=[]
    while active:
        counts=collections.Counter(u for i in active for u in NN[i]);eligible=[]
        for i in active:
            private=sorted(u for u in NN[i] if counts[u]==1)
            if len(private)>=mm[i]['Q']:eligible.append((i,private))
        if not eligible:break
        i,private=min(eligible);steps.append(dict(index=i,Q=mm[i]['Q'],private_count=len(private),selected=private[:mm[i]['Q']]));active.remove(i)
    union=set().union(*(NN[i] for i in active)) if active else set();deficit=sum(mm[i]['Q'] for i in active)-len(union)
    result=dict(status='COMPRESSED_A_POOL_AND_PEELING_CONTROL',source_sha256=R.pin(F/'compressed_A_closed_source.json'),A=sum(r['a'] for r in rows),QF=len(m['D']),U=len(m['U']),macros=mm,all_macros_own_solvent=all(z['Q']<=2*z['H'] for z in mm),pool_cover=R.cover(m),peeling_steps=steps,unpeeled_indices=sorted(active),unpeeled_deficit=deficit,unpeeled_union=sorted(union),source_queries=0,source_engine_calls=0,SI34='ACTIVE')
    out('compressed_A_pool_control.json',result)
    print(json.dumps({k:result[k] for k in ('A','QF','U','all_macros_own_solvent','unpeeled_indices','unpeeled_deficit')}|{'fresh_A_splays':S.CALLS}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core43_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=S.CALLS,source_engine_calls=S.CALLS),f)

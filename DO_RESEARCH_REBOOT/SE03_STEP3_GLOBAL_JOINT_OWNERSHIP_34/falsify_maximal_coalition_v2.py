"""One adversarial maximal-core source, reusing an accepted B trajectory.
This changes the source word; it never edits or projects the old source.
"""
import importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import retirement_pools as R
CAP=float(sys.argv[1]);QCAP=min(210,int(sys.argv[2]));START=time.process_time()
sp=importlib.util.spec_from_file_location('functional_replay',B/'audit_core39.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);S.START=START;S.CAP=CAP;S.QCAP=QCAP;S.CALLS=0
def main():
    old=P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json';assert R.pin(old)=='43a3d38a5cf157c0aa049411700351641597d8fed27babf1ebf41a3ad14b01b3'
    z=json.loads(old.read_text());erase=z['erased_key'];assert erase==11
    keep=[r['target'] for r in z['rows'] if r['genuine_F']]
    reset=[('D',x) for x in list(range(1,14))+list(range(12,0,-1))]
    word=[('K',x) for x in keep]+reset
    required=len(reset)+sum(1+(k=='K')+(k=='K' and x!=erase) for k,x in word)
    assert required<=QCAP,('whole control exceeds reserved primitive budget',required,QCAP)
    initial=tuple(R.freeze(t) for t in z['rows'][0]['before']);A,BF,BE=initial
    cf=[];ce=[]
    for r in z['prefix_rows']:
        if r.get('genuine_F'):cf=[r['target']]+[x for x in cf if x!=r['target']]
        if r.get('genuine_E'):ce=[r['target']]+[x for x in ce if x!=r['target']]
    prefix=[]
    for i,(kind,x) in enumerate(reset):
        aa=A;A,a,_,_=S.splay(A,x);prefix.append(dict(t=i+1,kind=kind,key=x,a=a,qF=0,qE=0,A_before=aa,BF_before=BF,BE_before=BE,A_after=A,BF_after=BF,BE_after=BE,chart_F=cf[:],chart_E=ce[:]))
    boundary=A,BF,BE,tuple(cf),tuple(ce);rows=[]
    for i,(kind,x) in enumerate(word):
        aa,bf,be=A,BF,BE;A,a,_,_=S.splay(A,x);q=qe=0
        if kind=='K':
            g=BF[0]!=x;BF,_,q,_=S.splay(BF,x)
            if g:cf=[x]+[v for v in cf if v!=x]
            if x!=erase:
                g=BE[0]!=x;BE,_,qe,_=S.splay(BE,x)
                if g:ce=[x]+[v for v in ce if v!=x]
        rows.append(dict(t=len(reset)+i+1,kind=kind,key=x,a=a,qF=q,qE=qe,A_before=aa,BF_before=bf,BE_before=be,A_after=A,BF_after=BF,BE_after=BE,chart_F=cf[:],chart_E=ce[:]))
    assert boundary==(A,BF,BE,tuple(cf),tuple(ce))
    out=dict(status='ORIGINAL_NEW_MAXIMAL_SOURCE_CONTROL',accepted_reaching_source=str(old),accepted_reaching_source_sha256=R.pin(old),initial_after_accepted_prefix=initial,initial_charts=[list(boundary[3]),list(boundary[4])],reset_prefix=prefix,period_rows=rows,period=[rows[0]['t'],rows[-1]['t']],period_boundary=boundary,word=word,erase=erase,source_queries=S.CALLS,source_engine_calls=S.CALLS,owner_scope='no fixed fE/a0 supplied for this NEW source; raw policy test only')
    m=R.build(R.normalize(out,'c33'));assert m['scope']=='MAXIMAL_CORE';out.update(r=m['r'],core=m['core'],D=len(m['D']),U=len(m['U']),pool_test=R.cover(m),natural_prior_test=R.cover(m,m['h0']),macros=m['macros'])
    with (F/'maximal_nonmonotone_source_control.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps(dict(source_queries=S.CALLS,r=m['r'],core=m['core'],D=len(m['D']),U=len(m['U']),pool_complete=out['pool_test']['complete'],natural_prior_complete=out['natural_prior_test']['complete'])),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core42_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=S.CALLS,source_engine_calls=S.CALLS),f)

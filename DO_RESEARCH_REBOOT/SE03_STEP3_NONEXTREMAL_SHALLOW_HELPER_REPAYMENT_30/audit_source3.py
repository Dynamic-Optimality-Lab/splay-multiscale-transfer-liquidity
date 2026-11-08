"""Direct source construction of the critical Qj2 weak-helper triple.
Original rotations generate BOTH the reaching prefix and the closed period.
Source query allowance is inherited, reserved before every primitive call.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);QCAP=min(int(sys.argv[2]),430)
sp=importlib.util.spec_from_file_location('C30_source3',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('C30 reserved source-query allowance')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t

def main():
    T=fr(json.loads((P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/comb_source_fixtures.json').read_text())['reports'][0]['original_diagonal_tree'])
    a=b=e=T;word=[];tags={};kept=[];prefix=[]
    def add(mode,k,label=None,record=True):
        nonlocal a,b,e
        if label:tags[label]=len(word)+1
        before=(a,b,e);a,pa,ea=C.tr(a,k);pb=pe='';eb=ee=[];anc=[]
        if mode=='K':
            b,pb,eb=C.tr(b,k);assert len(pb)%2==0 and all(pb[i:i+2] in ('LL','RR') for i in range(0,len(pb),2))
            assert all(ev['G'] in C.M and ev['P'] not in C.M for ev in eb)
            anc=[C.p.at(before[1],pb[:i])[0] for i in range(0,len(pb),2)]
            if k!=11:e,pe,ee=C.tr(e,k)
        word.append((mode,k));prefix.append({'occurrence':len(word),'mode':mode,'target':k,'genuine_F':mode=='K' and before[1][0]!=k,
            'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,'a':len(ea),'qF':len(eb),'qE':sum(v['kind']=='DOUBLE' for v in ee),'before':before,'after':(a,b,e)})
        if mode=='K' and record:kept.append(anc)
    # Source-exact inverse of the proposed j access is inserted BEFORE the
    # preparation macro, to create Qj2 rather than the harmless Qj1 case.
    for k in (7,11,7,13,7,13,3):add('K',k)
    prep=list(range(13,0,-1))+[11,7,12,13,7,6,7,5,7,13]
    for k in prep:add('D',k)
    add('K',13,'preparation_end');add('K',7,'j');add('K',11,'helper');add('K',5,'comb')
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):add('K',k,record=False)
    assert b==T;kept=[]
    add('K',1)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):add('K',k,record=False)
    assert b==T;kept=[]
    for k in (7,13,9):add('K',k)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):add('K',k,record=False)
    assert b==T
    for k in range(13,0,-1):add('D',k)
    add('D',3);S=(a,b,e);base=len(word);rows,end=C.replay(*S,word);assert S[:2]==end[:2]
    for r in rows:r['occurrence']+=base
    tags={k:v+base for k,v in tags.items()};mm=C.L.macros(rows);al=[]
    for m in mm:
        x=m['rows'][-1]['target'];pa,ch=C.L.marked_tree(m['rows'][0]['before'][1],C.M);_,nc=C.L.marked_tree(m['rows'][-1]['after'][1],C.M);anc=[];v=pa[x]
        while v is not None:anc.append(v);v=pa[v]
        E=lambda cc:sum(max(len(v)-2,0) for v in cc.values());beta=sum(len(ch[v])>=2 for v in anc);k3=sum(len(ch[v])>=3 for v in anc);z=int(not ch[x]);c=min(m['H'],3)
        al.append({'occurrences':m['occurrences'],'target':x,'H':m['H'],'Q':m['Q'],'beta':beta,'z':z,'k3':k3,'rho':2*c-beta-z,
            'E_before':E(ch),'E_after':E(nc),'sigma_E':2*c-m['Q']+E(nc)-E(ch),'marked_before':ch,'marked_after':nc})
    trip=[next(z for z in al if tags[label] in z['occurrences']) for label in ('j','helper','comb')]
    assert [(z['H'],z['Q'],z['beta'],z['z'],z['sigma_E']) for z in trip]==[(1,2,2,0,0),(1,2,1,1,-1),(1,3,3,1,0)],trip
    assert sum(z['sigma_E'] for z in trip)==-1
    assert {r['target'] for r in rows if r['mode']=='K'}==C.M
    out('nonextremal_source_countercertificate.json',{'status':'PRODUCER_EXACT_PAIRED_CLOSED_SOURCE_PENDING_DISTINCT_AUDIT',
        'original_diagonal_tree':T,'reaching_prefix':word,'prefix_rows':prefix,'period':word,'initial':S,'end':end,'rows':rows,'actual_interval':[base+1,2*base],
        'tags':tags,'triple':trip,'macro_ledger':al,'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
        'erased_key':11,'BE_also_closed':S[2]==end[2],'owner_map_claimed':False,'A_preparation':prep,
        'refuted_candidates':['Every weak P before a marked comb forces Hj>=2 without an extremal guard','The immediate predecessor/triple E packet always repays that helper'],
        'not_refuted':['MC29-X at its stated guard','NH30 existential source repayment','all possible packetizations','Coarse-Double','Universal CD','Dynamic Optimality']})
    print(json.dumps({'status':'NONEXTREMAL_NEGATIVE_TRIPLE_SOURCE','length':len(word),'queries':C.queries,'triple':trip,'BE_closed':S[2]==end[2]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})

"""All dirty-negative alias cases checked by production DAG constant folding."""
import sys,json,time,itertools,argparse,hashlib
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'))
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BState,BTrace,b_splay_event
OUT=Path('DO_RESEARCH_REBOOT/M2_DSK01/proof_certificate.json')
def cases():
    for h in range(9):
        for bits in itertools.product((False,True),repeat=h):
            a=list(range(8,7-h,-1));period=a+[19];word=list(bits)+[False,True]
            source={'S_broot':a[-1],'S_bkr8':0,'S_brr8':19}
            for j in range(1,h+1):
                k,r=('kr','rr') if bits[j-1] else ('kl','rl')
                source[f'S_b{k}{a[j]}']=0;source[f'S_b{r}{a[j]}']=a[j-1]
            for length in range(14,19):
                yield dict(family='RIGHT_SELF',h=h,bits=list(bits),d=length,target=8,
                           claimant=8),source,period,word
    for n in range(1,9):
        for h in range(n):
            s=n-h
            for bits in itertools.product((False,True),repeat=h):
                for mode in (('ON','OFF') if n<=7 else ('ON',)):
                    z=max((j+1 for j,v in enumerate(bits) if v),default=0) if mode=='ON' else None
                    available=iter(range(1,9))
                    a=[0 if j==z else next(available) for j in range(h+1)]
                    b=[next(available) for j in range(s)]
                    x=a[0];c=b[0];period=a+[19]+b;word=list(bits)+[False]*(s+1)+[True]
                    source={'S_broot':a[-1],f'S_bkl{c}':0,f'S_brl{c}':19,
                            f'S_bkr{x}':0,f'S_brr{x}':b[-1]}
                    for j in range(1,h+1):
                        k,r=('kr','rr') if bits[j-1] else ('kl','rl')
                        source[f'S_b{k}{a[j]}']=0;source[f'S_b{r}{a[j]}']=a[j-1]
                    for j in range(1,s):
                        source[f'S_bkl{b[j]}']=0;source[f'S_brl{b[j]}']=b[j-1]
                    for length in range(14,19):
                        yield dict(family='LEFT_SUCCESSOR',h=h,s=s,bits=list(bits),zero_mode=mode,
                                   zero_position=z,d=length,target=x,claimant=c),source,period,word
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--benchmark',type=int,default=0);args=ap.parse_args()
    if not args.benchmark:assert not OUT.exists(),'Never overwrite a certificate'
    d=DAG();b=BState(d,'S');bt=BTrace(d,'T')
    out=b_splay_event(d,b,bt,0,d.const_bool(False))
    clauses=[]
    for i in range(19):
        for k,r in (('kl','rl'),('kr','rr')):
            clauses.append(d.AND(d.EQ(getattr(out,k)[i],d.const_int(0,2)),
                                 d.EQ(getattr(out,r)[i],bt.bT[0])))
    prop=d.AND(d.EQ(out.root,bt.bT[0]),d.OR(*clauses))
    base_nodes=list(d.nodes);base_tab=dict(d.tab);start=time.process_time();rows=[];failures=[]
    for index,(meta,source,period,word) in enumerate(cases(),1):
        if args.benchmark and index>args.benchmark:break
        assert time.process_time()-start<300,'Certificate CPU cap: UNKNOWN'
        pins={**source,'T_bT0':meta['target'],'T_bd0':meta['d']}
        for k in range(meta['d']+1):pins[f'T_bp0_{k}']=period[k%len(period)]
        for k in range(meta['d']):pins[f'T_bdir0_{k}']=word[k%len(word)]
        answer=d.simplify(prop,pins)
        node=d.nodes[answer]
        passed=node[0]=='const' and node[1]==BOOL and bool(node[3])
        if not passed:failures.append({**meta,'reduced_node':repr(node)})
        rows.append({**meta,'forced_final_root_claim_verified':passed,
                     'pins_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()})
        d.nodes=list(base_nodes);d.tab=dict(base_tab)
        if index%128==0:
            print(json.dumps({'cases':index,'failures':len(failures),
                              'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    result={'status':'BENCHMARK' if args.benchmark else ('COMPLETE' if not failures else 'FAILED'),
            'cases':len(rows),'right_cases':sum(r['family']=='RIGHT_SELF' for r in rows),
            'left_cases':sum(r['family']=='LEFT_SUCCESSOR' for r in rows),
            'failures':failures,'production_DAG_nodes':len(base_nodes),
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    if not args.benchmark:
        assert len(rows)==6300,(len(rows),result['right_cases'],result['left_cases'])
        with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()


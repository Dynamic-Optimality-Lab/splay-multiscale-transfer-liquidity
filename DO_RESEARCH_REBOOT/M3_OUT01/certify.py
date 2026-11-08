"""Authoritative original-DAG root-claim certificate, declared depths10..13."""
import sys,json,time,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M2_DSK01')
from certify_dirty import cases,DAG,BOOL,BState,BTrace,b_splay_event
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01')

def main():
    assert json.loads((BASE/'diagnostic.json').read_text())['status']=='PASS_NORMAL_FORM_ROOT_CLAIMS'
    out=BASE/'proof_certificate.json';assert not out.exists();start=time.process_time()
    d=DAG();b=BState(d,'S');bt=BTrace(d,'T');dest=b_splay_event(d,b,bt,0,d.const_bool(False))
    claims=[d.AND(d.EQ(getattr(dest,k)[i],d.const_int(0,2)),
                  d.EQ(getattr(dest,r)[i],bt.bT[0]))
            for i in range(19) for k,r in (('kl','rl'),('kr','rr'))]
    prop=d.AND(d.EQ(dest.root,bt.bT[0]),d.OR(*claims))
    nodes=list(d.nodes);tab=dict(d.tab);rows=[];fail=[]
    for meta,source,period,word in cases():
        if meta['d']!=14:continue
        for depth in range(10,14):
            assert time.process_time()-start<300,'UNKNOWN source-certificate CPU cap'
            meta={**meta,'d':depth}
            pins={**source,'T_bT0':meta['target'],'T_bd0':depth}
            for k in range(depth+1):pins[f'T_bp0_{k}']=period[k%len(period)]
            for k in range(depth):pins[f'T_bdir0_{k}']=word[k%len(word)]
            ans=d.simplify(prop,pins);node=d.nodes[ans]
            passed=node[0]=='const' and node[1]==BOOL and bool(node[3])
            row={**meta,'forced_final_root_claim_verified':passed,
                 'pins_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()}
            rows.append(row)
            if not passed:fail.append({**row,'remaining_node':repr(node)})
            d.nodes=list(nodes);d.tab=dict(tab)
            if len(rows)%256==0:print(json.dumps({'cases':len(rows),'failures':len(fail),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    assert len(rows)==5040
    result={'status':'PASS_PRODUCTION_DAG' if not fail else 'FAILED_PRODUCTION_DAG',
            'cases':len(rows),'right_cases':sum(r['family']=='RIGHT_SELF' for r in rows),
            'left_cases':sum(r['family']=='LEFT_SUCCESSOR' for r in rows),
            'production_DAG_nodes':len(nodes),'off_spine_fields':'ALL_UNFIXED',
            'cpu_seconds':round(time.process_time()-start,3),'failures':fail,'rows':rows}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','failures')},indent=2))

if __name__=='__main__':main()

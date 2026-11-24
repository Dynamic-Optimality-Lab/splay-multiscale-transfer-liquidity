"""Bounded exact attack on the admitted trace/ports accounting mechanism."""
import sys
import json
import time
from collections import Counter
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T


def run():
    begin=time.perf_counter();traces=[];summary=[]
    population=[]
    for i in range(13):
        z=X.K.load(X.PREV/f'source_{i:02d}.json.gz');population.append((z['source'],z['blocks']))
    for q in (5,10,25):population.append((X.K.PARAM.H(3,q),None))
    for i,(s,parts) in enumerate(population):
        path=f'run_001/trace_{i:02d}.json.gz'
        if (X.HERE/path).exists():z=X.K.load(X.HERE/path)
        else:z=X.compile_source(s,explicit_blocks=parts);X.write(path,z)
        traces.append(z)
        bank_path=f'run_001/bank_{i:02d}.json.gz'
        if (X.HERE/bank_path).exists():b=X.K.load(X.HERE/bank_path)
        else:b=T.bank(z,c=4,d=0,capacity=4);X.write(bank_path,b)
        masks=Counter(''.join(map(str,m)) for st in z['steps'] if st['q'] for m in st['retained_bit_masks'].values())
        critical=[{'op':r['id'],'a':r['a'],'q':r['q'],'k':r['k'],'local_only_unchanged':r['local_only_unchanged'],'anonymous_delta_l1':sum(abs(v) for v in r['delta'].values()),'anonymous_delta':r['delta']} for r in z['operations'] if r['q']>r['a'] and r['local_only_unchanged']]
        row={'index':i,'name':s['name'],'keys':sum(map(len,z['blocks'])),'operations':len(z['operations']),'steps':len(z['steps']),'A':z['A'],'Q_B':z['Q_B'],'K_B':z['K_B'],'U':len(z['original_U']),'R_A':z['R_A'],'A_port_packets':z['A_port_packets'],'bank_status':b['status'],'bank_paid':b['paid'],'bank_credit_used':b['issued_credit'],'projected_B_double_masks':dict(masks),'invisible_costly_operations':critical}
        summary.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ('invisible_costly_operations','projected_B_double_masks')}),flush=True)
    rows=T.potential_rows(traces);cert=T.synthesize(rows)
    if cert['status']=='FINITE_EXACT':T.verify_potential(rows,cert)
    X.write('run_001/POTENTIAL_ROWS.json.gz',rows);X.write('run_001/JOINT_PORT_POTENTIAL.json',cert)
    X.write('run_001/SUMMARY.json',{'cases':summary,'potential':{k:v for k,v in cert.items() if k!='values'},'wall_seconds':time.perf_counter()-begin,'root_status':'OPEN','universal_claim':'NONE: finite teachers are diagnostics; physical symbolic induction is a separate required obligation.'})
    print(json.dumps({'potential':{k:v for k,v in cert.items() if k!='values'},'seconds':time.perf_counter()-begin}),flush=True)


if __name__=='__main__':run()

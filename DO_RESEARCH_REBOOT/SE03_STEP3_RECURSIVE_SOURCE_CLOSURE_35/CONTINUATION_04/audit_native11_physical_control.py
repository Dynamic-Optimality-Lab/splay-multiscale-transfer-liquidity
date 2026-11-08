"""Independent physical carry/owner construction on a closed hard source."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def mirror(t):return (12-t[0],mirror(t[2]),mirror(t[1])) if t is not None else None
def point(nodes,i,a,n):
    w=1<<(n-1).bit_length()
    while i>=0:
        l,r=nodes[i];half=w//2
        if a<half:i=l
        else:i=r;a-=half
        w=half
    return -i-1
def main():
    cert=F/'native11_full_source_certificate.json';data=json.loads(cert.read_text())
    for p,h in data['input_sha256'].items():assert sha(Path(p))==h
    srcpath=F/'projected_cluster_closed_counter_source.json';accepted=json.loads((F/'independent_projected_cluster_theorem.json').read_text())
    assert accepted['input_sha256'][str(srcpath)]==sha(srcpath)
    src=json.loads(srcpath.read_text())
    with (F/'probe11_source_actions.pkl').open('rb') as f:prim=pickle.load(f)
    index={t:i for i,t in enumerate(prim['trees'])};del prim
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m={k:v for k,v in pickle.load(f).items() if k in ('classes','local')}
    with (F/'global_probe11_H3B_DAG_01.pkl').open('rb') as f:z=pickle.load(f)
    def debt(A,BF):
        a,b=index[A],index[BF];assert A[0]==BF[0]
        g=A[0];return point(z['nodes'],z['columns'][b],int(m['local'][a]),len(m['classes'][g-1]))
    reports=[]
    for reflect in (False,True):
        rows=[]
        for r in src['period_rows']:
            a=dict(r)
            for k in ('A_before','A_after','BF_before','BF_after'):a[k]=tup(r[k]);a[k]=mirror(a[k]) if reflect else a[k]
            a['key']=12-r['key'] if reflect else r['key'];rows.append(a)
        ends=[i for i,r in enumerate(rows) if r['genuine_F']];macros=[];h0={};U=set();D=set()
        for j,e in enumerate(ends):
            a=(ends[j-1]+1)%len(rows);rr=rows[a:e+1] if a<=e else rows[a:]+rows[:e+1]
            units=[(r['t'],k,b) for r in rr for k in range(1,r['a']+1) for b in (0,1)]
            dd=[(rr[-1]['t'],k) for k in range(1,rr[-1]['qF']+1)]
            own=dict(zip(dd,units));h0.update(own);U.update(units);D.update(dd)
            ds=debt(rr[0]['A_before'],rr[0]['BF_before']);dt=debt(rr[-1]['A_after'],rr[-1]['BF_after'])
            H=len(units)//2;Q=len(dd);c=min(H,4);assert 2*c-Q+dt-ds>=0
            macros.append({'end_t':rr[-1]['t'],'H':H,'Q':Q,'c':c,'units':units,'demands':dd,'own':own,'start_D':ds,'end_D':dt})
        K=max(a['end_D'] for a in macros);cut=next(j for j,a in enumerate(macros) if a['end_D']==K)
        ordered=macros[cut+1:]+macros[:cut+1];bank=[];out={};released=set();seen=set();peak=0;trace=[]
        for a in ordered:
            assert len(bank)==K-a['start_D']
            chosen=list(a['own'].values());chosen+= [u for u in a['units'] if u not in chosen][:2*a['c']-len(chosen)]
            assert len(chosen)==2*a['c'] and not set(chosen)&seen;seen.update(chosen)
            peak=max(peak,len(bank)+len(chosen));free=[u for u in chosen if u not in a['own'].values()]
            for d,u in a['own'].items():assert d not in out;out[d]=u
            for d in a['demands']:
                if d in a['own']:continue
                u=free.pop(0) if free else bank.pop(0);assert u not in out.values();out[d]=u
            remainder=bank+free;keep=K-a['end_D'];assert len(remainder)>=keep
            bank=remainder[:keep];released.update(remainder[keep:]);released.update(set(a['units'])-set(chosen))
            assert not set(bank)&set(out.values()) and len(set(bank))==len(bank)
            trace.append({'end_t':a['end_t'],'H':a['H'],'Q':a['Q'],'D_start':a['start_D'],'D_end':a['end_D'],
              'selected_units':chosen,'outgoing_actual_bank':list(bank)})
        assert not bank and set(out)==D and len(set(out.values()))==len(D)
        assert all(out[d]==u for d,u in h0.items()) and set(out.values())|released==U
        assert not set(out.values())&released and peak<=K+8<=12
        reports.append({'reflected':reflect,'actual_period':src['period'],'K':K,'working_peak':peak,'h0_preserved':len(h0),
          'full_demand_count':len(out),'full_comparison':[{'demand':d,'unit':u} for d,u in sorted(out.items())],
          'macro_trace':trace,'historical_owners_or_fE_changed':False})
    r={'status':'PASS_RESTRICTED_NATIVE11_SOURCE_CERTIFICATE_AND_PHYSICAL_CONTROL',
      'computer_assisted_sign_scope':'complete fixed eleven-anchor source domain; arbitrary rigid off-path hangers',
      'proof_inspection':'all H regimes, explicit h0 selector, actual-max cut, original static Bank25<=12 construction',
      'controls':reports,'source_queries':0,'source_engine_calls':0,
      'external_or_formal_review':False,'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (cert,srcpath,F/'independent_projected_cluster_theorem.json')}}
    with (F/'independent_native11_physical_control.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({'status':r['status'],'controls':[{k:v for k,v in a.items() if k not in ('full_comparison','macro_trace')} for a in reports],'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify140_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

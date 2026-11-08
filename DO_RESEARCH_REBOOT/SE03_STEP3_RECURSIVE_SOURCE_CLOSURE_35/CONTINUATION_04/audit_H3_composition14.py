"""Independent composition proof using the already audited complete actions."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def val(nodes,i,pos,n):
    w=1<<(n-1).bit_length()
    while i>=0:
        a,b=nodes[i];h=w//2
        if pos<h:i=a
        else:i=b;pos-=h
        w=h
    return -i-1
def main():
    data=json.loads((F/'probe11_H3_source_resolution_14.json').read_text())
    for p,h in data['input_sha256'].items():assert sha(F/p)==h
    with (F/'probe11_source_actions.pkl').open('rb') as f:a={k:v for k,v in pickle.load(f).items() if k in ('destination','H','Q','roots')}
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m={k:v for k,v in pickle.load(f).items() if k in ('local','classes')}
    with (F/'global_probe11_H3_DAG_14.pkl').open('rb') as f:z=pickle.load(f)
    assert not z['pending'] and z['status']=='LOW_AND_ADDED_H3_SUBGRAPH_COMPLETE'
    controls=[]
    for w in data['source_constraints_to_add']:
        state=w['A_source'];bs=w['B_source'];h=0;code=1
        assert int(a['roots'][state])==int(a['roots'][bs])==w['g'] and w['g']!=w['KEEP']
        for i,op in enumerate(w['A_word']):
            k=op['key'];code=12*code+k;h+=int(a['H'][state,k-1]);state=int(a['destination'][state,k-1])
            assert op['kind']==('K' if i==len(w['A_word'])-1 else 'D')
        x=w['KEEP'];bt=int(a['destination'][bs,x-1]);q=int(a['Q'][bs,x-1])
        assert state==w['A_target'] and bt==w['B_target'] and h==3 and q==w['Q']
        assert w['A_word'][-1]['key']==x and code==w['word_code_base12']
        ds=val(z['nodes'],z['columns'][bs],int(m['local'][w['A_source']]),len(m['classes'][w['g']-1]))
        dt=val(z['nodes'],z['columns'][bt],int(m['local'][state]),len(m['classes'][x-1]))
        assert (ds,dt)==(w['D_source'],w['D_target']) and 6-q+dt-ds==w['signed_margin']<0
        controls.append({'reference':w,'H':h,'Q':q,'composition_check':'complete independently accepted native11 original primitives'})
    r={'status':'PASS_LITERAL_THREE_EVENT_SOURCE_DEFECTS','source_constraints':len(controls),'controls':controls,
      'fresh_splays':0,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','full_source_cycle_counterexample':False,
      'input_sha256':{p:sha(F/p) for p in ('probe11_H3_source_resolution_14.json','global_probe11_H3_DAG_14.pkl',
        'probe11_source_actions.pkl','independent_probe11_source_actions.json')}}
    with (F/'independent_probe11_H3_source_14.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k not in ('controls','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify133_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

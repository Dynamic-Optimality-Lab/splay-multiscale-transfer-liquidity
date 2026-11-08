"""Finite, symbolic certificate using unmodified production DAG and controller."""
import sys,json,time,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from experiment import D,V,FIELDS,pack,unpack
from PC_B_CONTROLLER import BState,BTrace,b_splay_event
from PC_TYPED_DAG import DAG,BOOL
OUT=Path('DO_RESEARCH_REBOOT/M2_SEP01/proof_certificate.json')
assert not OUT.exists(),'Never overwrite an existing certificate'
start=time.process_time()
def skeleton(h):
    spine=list(range(8,7-h,-1));period=spine+[19]
    m={'root':spine[-1],**{f:[f'S.{f}{i}' for i in range(19)] for f in FIELDS}}
    m['kr'][8]=0;m['rr'][8]=19
    for j in range(1,h+1):m['kr'][spine[j]]=0;m['rr'][spine[j]]=spine[j-1]
    return spine,period,m
def symbolic_replay(h,length):
    spine,period,m=skeleton(h)
    b=pack(m);bt=BTrace(D,'S');bt.bT[0]=V(8);bt.bd[0]=V(length)
    bt.bpath[0]=[V(period[k%len(period)]) for k in range(19)]
    bt.bdir[0]=[V(k%len(period)!=h) for k in range(18)]
    out=unpack(b_splay_event(D,b,bt,0,V(False)))
    claims=[]
    for i in range(19):
        for side,k,r in (('L','kl','rl'),('R','kr','rr')):
            if out[k][i]==0 and out[r][i]==8:claims.append([i,side])
    return spine,period,m,out,claims
def taut(d,n):
    k,t,a,e=d.nodes[n]
    if k=='const' and t==BOOL:return bool(e)
    if k=='and':return taut(d,a[0]) and taut(d,a[1])
    if k=='eq':return a[0]==a[1]
    return False
rows=[]
for h in range(9):
    for length in range(19):
        assert time.process_time()-start<120,'CPU cap: incomplete certificate, no promotion'
        spine,period,m,expected,claims=symbolic_replay(h,length)
        if length>h+1:
            assert claims,('no forced root claim',h,length)
        else:
            assert expected['kr'][8]==0 and expected['rr'][8]==19
        d=DAG();b=BState(d,'S');bt=BTrace(d,'T')
        out=b_splay_event(d,b,bt,0,d.const_bool(False))
        pins={'S_broot':m['root'],'T_bT0':8,'T_bd0':length}
        symbols={}
        for f in FIELDS:
            for i,n in enumerate(getattr(b,f)):
                symbols[f'S.{f}{i}']=n
                if isinstance(m[f][i],int):pins[d.nodes[n][3][1]]=m[f][i]
        for k in range(length+1):pins[f'T_bp0_{k}']=period[k%len(period)]
        for k in range(length):pins[f'T_bdir0_{k}']=k%len(period)!=h
        def expr(v,width):return symbols[v] if isinstance(v,str) else d.const_int(v,width)
        checks=[d.EQ(out.root,d.const_int(expected['root'],5))]
        for f in FIELDS:
            width=2 if f in ('kl','kr') else 5
            checks += [d.EQ(n,expr(v,width)) for n,v in zip(getattr(out,f),expected[f])]
        if length>h+1:
            claimant,side=claims[0];k,r=('kl','rl') if side=='L' else ('kr','rr')
            property_node=d.AND(d.EQ(out.root,d.const_int(8,5)),
                 d.EQ(getattr(out,k)[claimant],d.const_int(0,2)),
                 d.EQ(getattr(out,r)[claimant],d.const_int(8,5)))
            consequence='ROOT_CLAIM'
        else:
            property_node=d.AND(d.EQ(out.kr[8],d.const_int(0,2)),
                                d.EQ(out.rr[8],d.const_int(19,5)))
            consequence='PHANTOM_PRESERVED'
        reduced=d.simplify(d.AND(*checks,property_node),pins)
        assert taut(d,reduced),('production DAG mismatch',h,length)
        rows.append({'h':h,'d':length,'consequence':consequence,
                     'claimants':claims,'all_115_fields_checked':True,
                     'structural_normal_form':{f:expected[f] for f in ('root','kl','rl','kr','rr')}})
    print(json.dumps({'completed_h':h,'cases':len(rows),
                      'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
result={'status':'COMPLETE','scope':'9 h values x 19 declared lengths, symbolic off-spine fields; label-transfer lemma required',
        'cases':len(rows),'root_claim_cases':sum(r['consequence']=='ROOT_CLAIM' for r in rows),
        'preservation_cases':sum(r['consequence']=='PHANTOM_PRESERVED' for r in rows),
        'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)


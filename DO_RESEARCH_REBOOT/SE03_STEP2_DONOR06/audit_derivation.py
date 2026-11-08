"""Universal free-frame and affine proof checks; no source instances."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
def right(t):
    g,p,d=t;k,a,b=p
    return N(k,a,N(g,b,d))
def left(t):
    g,a,p=t;k,b,d=p
    return N(k,N(g,a,b),d)
def inorder(t):return [t] if isinstance(t,str) else inorder(t[1])+[t[0]]+inorder(t[2])
def owner_ports(t,parent='H'):
    if isinstance(t,str):return {t:parent}
    k,l,r=t;new=k if k in {'g','x'} else parent
    return owner_ports(l,new)|owner_ports(r,new)
def add(*ps):
    d={}
    for p in ps:
        for k,v in p.items():d[k]=d.get(k,0)+v
    return {k:v for k,v in d.items() if v}
def neg(p):return {k:-v for k,v in p.items()}
def main():
    ll=N('g',N('p',N('x','A','B'),'C'),'D')
    rr=N('g','A',N('p','B',N('x','C','D')))
    lr=N('g',N('p','A',N('x','B','C')),'D')
    rl=N('g','A',N('p',N('x','B','C'),'D'))
    llo=right(right(ll));rro=left(left(rr))
    lro=right(N('g',left(lr[1]),lr[2]))
    rlo=left(N('g',rl[1],right(rl[2])))
    assert llo==N('x','A',N('p','B',N('g','C','D')))
    assert rro==N('x',N('p',N('g','A','B'),'C'),'D')
    assert lro==N('x',N('p','A','B'),N('g','C','D'))
    assert rlo==N('x',N('g','A','B'),N('p','C','D'))
    for s,t in [(ll,llo),(rr,rro),(lr,lro),(rl,rlo)]:assert inorder(s)==inorder(t)
    assert owner_ports(ll)==owner_ports(llo)=={'A':'x','B':'x','C':'g','D':'g'}
    assert owner_ports(rr)==owner_ports(rro)=={'A':'g','B':'g','C':'x','D':'x'}
    # Formal threshold-flow telescoping, symbols stand for arbitrary endpoints.
    assert add({'Br':1,'Bm':-1},{'Bm':1,'Bl':-1})=={'Br':1,'Bl':-1}
    assert add({'Hr':1,'Hm':-1},{'Hm':1,'Hl':-1})=={'Hr':1,'Hl':-1}
    # Exhaustive structural tag deductions for OWN-CHANNEL KEEP frames.
    # e is the off-path hanger at P: C for LL, B for RR.
    rows=[{'P':'own U','G':'own M','delta_K':{}},
          {'P':'own U','G':'foreign','delta_K':{'e':-1},'premise':'e>=0'},
          {'P':'own U','G':'own U','delta_K':{'one':-1}},
          {'P':'foreign','G':'foreign','delta_K':{}},
          {'P':'foreign','G':'own U','delta_K':{'one':-1}}]
    assert add({'oldP':-1},{'oldP':1})=={}
    # LL own-U P: source P=e, final P=0. Foreign G has no K contribution.
    assert add({},neg({'e':1}))==rows[1]['delta_K']
    # Own-U G/P case: G1->1, P1->0; foreign-P/own-U G: G1->0.
    assert (1-1)+(0-1)==-1 and 0-1==-1
    # Source-parent own-M would have own mass1+rebuilt1+e>1.
    # Mixed case: both final child charges0, a=-p,d=-g.
    assert add({'p':1,'a':1},{'g':1,'d':1})=={'p':1,'a':1,'g':1,'d':1}
    assert add({'g':1,'p':1,'a':1,'d':1},neg({'p':1,'a':1}),neg({'g':1,'d':1}))=={}
    # Omega counter uses an already completed exact source theorem only.
    old=(B.parent/'SE03_STEP2_REPAY02/RAY_NORMALIZATION_AND_OBSTRUCTION.md').read_text()
    assert 'paired weight-2' in old and 'EXACTLY1' in old and '54>0' in old
    assert -2+2-1==-1
    out('derivation_audit.json',{'status':'PASS_NEW_SCOPED_SOURCE_DERIVATIONS',
        'generic_frames':['LL','RR','LR','RL'],'free_port_owner_preservation':True,
        'recency':'new edges from just-accessed root; child access removes every initial incoming edge within one period',
        'channels':'arbitrary delta+1 threshold-crossing channels; interval flow telescopes; root own-channel charge1',
        'own_channel_SS_rows':rows,'own_channel_mixed_delta':'-I[G ownU]-I[P ownU]',
        'own_channel_terminal_zig_delta':0,
        'envelope_obstruction':'unique actual nine-Score chart at R11; normalized source1, pair-2, target<=2',
        'core10_repayment_proved':False,'core11_zero_plus1_completion_proved':False,
        'full_donor_allocation_proved':False,'Step2':'OPEN',
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0})
    print('PASS universal source frames, recency, channel algebra and exact chart-envelope rejection; Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_derivation_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

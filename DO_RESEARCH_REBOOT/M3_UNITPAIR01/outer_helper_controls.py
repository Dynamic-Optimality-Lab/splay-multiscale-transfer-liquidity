"""Fresh original H2 controls for BOTH helpers in sigma=e0+e9."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from decoder import UnitPairCertificate
from profiles import decode,core
import outside_original as O
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def hasG(t):return t=='G' or (isinstance(t,tuple) and (hasG(t[1]) or hasG(t[2])))
def expand(t,keys,parent=None,side=None,cuts=None):
    if cuts is None:cuts=[]
    if t is None:
        if parent is not None:cuts.append((parent,side))
        return O.S.balanced(list(keys)),cuts
    assert t!='G';k,l,r=t
    ll,_=expand(l,tuple(x for x in keys if x<k),k,0,cuts);rr,_=expand(r,tuple(x for x in keys if x>k),k,1,cuts)
    return O.S.node(k,ll,rr),cuts
def main():
    out=BASE/'outer_helper_controls.json';assert not out.exists();start=time.process_time();P=UnitPairCertificate()
    c=json.loads((BASE/'p0_9/relation.json').read_text());B=P.bank;selected={};wanted={(gap,w) for gap in (0,9) for w in (0,1)}
    bank={}
    for gap in (0,9):
        for b,row in enumerate(B['kernels'][str(gap)]):
            for x,pair in enumerate(row):
                if pair is not None and pair[1] in (0,1):bank.setdefault((gap,pair[1],B['trees'][b][0],x),b)
    for a,opts in enumerate(c['options']):
        root=c['shadows'][a][0][2]
        for o in opts:
            H,x,aa,gap,family,code=o
            if H!=2:continue
            for gg,w in wanted-selected.keys():
                if gg!=gap:continue
                b=bank.get((gap,w,root,x))
                if b is None:continue
                tree=decode(code,tuple(c['keys']))
                if hasG(tree):continue
                selected[(gap,w)]=(a,o,b,tree)
        if len(selected)==4:break
    assert len(selected)==4
    d=O.DAG();L=O.build_slow(d,'MXL');records=[]
    def scaled(t):return O.S.LEAF if t is None else O.S.node(16*t[0],scaled(t[1]),scaled(t[2]))
    for (gap,w),(a,o,b,t) in sorted(selected.items()):
        AA,cuts=expand(t,tuple(c['keys']));BB=scaled(B['trees'][b]);BB=O.V.insert(O.V.insert(BB,-8),136)
        tree=t;targets=[]
        from profiles import get,move
        for path in c['families'][o[4]]['word']:targets.append(get(tree,path)[0]);tree=move(tree,path)
        marks={targets[-1]//16};marks.update(i for i in range(9) if len(marks)<5);mu=sum(1<<i for i in marks)
        _,_,r=O.low(d,L,AA,BB,cuts,[['K',x] for x in targets],f'both_outer_helper{gap}_w{w}',mu)
        assert r['H']==2 and r['w']==w and r['source']['sigma']==[1]+[0]*8+[1]
        js=P.J(r['source']);jt=P.J(r['destination']);assert w-jt+js>=0
        r.update(J_source=js,J_destination=jt,residual=w-jt+js,helper_gap=gap,actual_terminal_q=r['q']);records.append(r)
        assert time.process_time()-start<300
    result={'status':'ORIGINAL_BOTH_OUTER_HELPERS_PASS','full_original_low_roots':4,'DAG_nodes':len(d.nodes),'helper_gaps':[0,9],
      'weights':[0,1],'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()

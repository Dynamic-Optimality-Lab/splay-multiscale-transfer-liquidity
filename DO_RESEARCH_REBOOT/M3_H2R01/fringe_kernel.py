"""Complete gap-0/terminal-core ten-node kernel for the residual H=2 fringe case."""
import sys,json,time
from pathlib import Path
from collections import Counter
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as F
from terminal_potential import CappedPotential
OUT=Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json')
def erase(t):
    if t==S.LEAF:return t
    if t[1]==-1:
        assert t[2]==t[3]==S.LEAF;return S.LEAF
    return S.node(t[1],erase(t[2]),erase(t[3]))
def gap_leaf(t):
    if t==S.LEAF:return False
    if t[1]==-1:return t[2]==t[3]==S.LEAF
    return gap_leaf(t[2]) or gap_leaf(t[3])
def main():
    assert not OUT.exists();start=time.process_time();P=CappedPotential();rows=[];failures=[];counts=Counter()
    for i,t in enumerate(P.trees):
        source=F.insert(t,-1);pre=S.trace(source,-1)[0];assert pre[1]==-1
        assert pre[2]==S.LEAF
        for x in range(9):
            assert time.process_time()-start<120,'UNKNOWN: fringe kernel cap'
            h=S.lookup(pre,x)[1];q=h//2;dest=S.trace(pre,x)[0];valid=gap_leaf(dest)
            row={'entry_core':i,'target':x,'terminal_depth':h,'q':q,'w':4-q,
                 'gap0_childless_at_exit':valid}
            counts['queries']+=1
            if valid:
                core=erase(dest);j=P.ids[core];residual=(4-q)-(P.psi[i]-P.psi[j])
                row.update(exit_core=j,psi_source=P.psi[i],psi_destination=P.psi[j],residual=residual)
                counts['retained']+=1;counts[f'weight_{4-q}']+=1
                if residual<0:failures.append(row)
            rows.append(row)
    result={'status':'COMPLETE' if not failures else 'FAILED_SIGNED_EXTENSION','queries':len(rows),
            'retained_endpoints':counts['retained'],'weight_counts':{k:v for k,v in counts.items() if k.startswith('weight_')},
            'failures':failures,'all_retained_inequalities_pass':not failures,
            'cpu_seconds':round(time.process_time()-start,3),'rows':rows}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()

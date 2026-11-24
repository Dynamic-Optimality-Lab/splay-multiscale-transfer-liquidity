"""GSO exact integer synthesis of rigid gap masses on original RR traces."""
import sys
import json
import time
import z3
from pathlib import Path
sys.dont_write_bytecode=True
from sources import T
HERE=Path(__file__).resolve().parent


def branch(t,parent,side):
    child=t.ch[parent][side]
    return {'gap':parent-1 if side==0 else parent} if child is None else {'lo':t.lo[child],'hi':t.hi[child]}


def templates(q):
    s=T.B.K.PARAM.H(3,q);m=len(s['initial_B']['children']);x=m-7
    t=T.B.K.OLD.Tree(s['initial_B'],list(range(1,m+1)))
    for mode,key in s['operations'][:m+6]:
        if mode=='K':T.B.K.OLD.plain(t,key)
    rows=[];step=0
    while t.parent[x] is not None:
        step+=1;p=t.parent[x];g=t.parent[p]
        typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
        if typ=='RR':rows.append({'id':['B',m+7,step],'a':branch(t,g,0),'b':branch(t,p,0),'c':branch(t,x,0),'d':branch(t,x,1)})
        pivots=[x] if g is None else [p,x] if typ in ('LL','RR') else [x,x]
        for key in pivots:t.rotate(key)
    assert len(rows)==q
    return s,rows


def synthesize(q):
    started=time.perf_counter();s,rows=templates(q);m=len(s['initial_A']['children'])
    # One interior gap in each parent-left block, and one in target-right.
    # This is a fixed embedding basis, not a restriction on source validity.
    atoms=sorted({r['b']['lo'] for r in rows}|{rows[0]['d']['lo']})
    assert len(atoms)==q+1
    w={g:z3.Int('gap_'+str(g)) for g in atoms}
    def mass(tag):
        if 'gap' in tag:return w.get(tag['gap'],z3.IntVal(0))
        return z3.IntVal(tag['hi']-tag['lo']+1)+z3.Sum([v for g,v in w.items() if tag['lo']-1<=g<=tag['hi']])
    constraints=[v>=0 for v in w.values()]
    for row in rows:constraints.extend((mass(row['a'])==mass(row['d']),mass(row['b'])==mass(row['c'])))
    total=z3.Sum(list(w.values()));solver=z3.Optimize();solver.set(timeout=20000)
    solver.add(*constraints);solver.minimize(total)
    assert solver.check()==z3.sat
    model=solver.model();gaps=[0]*(m+1)
    for g,v in w.items():gaps[g]=model.eval(v).as_long()
    amount=sum(gaps)
    lower=z3.Solver();lower.add(*constraints,total<amount);assert lower.check()==z3.unsat
    physical=[]
    for j,row in enumerate(rows):
        values={k:model.eval(mass(row[k])).as_long() for k in ('a','b','c','d')}
        assert values['a']==values['d'] and values['b']==values['c']
        # Checked here; all-q validity comes from the actual recurrence proof.
        assert values=={'a':7,'b':16*2**j-9,'c':16*2**j-9,'d':7}
        physical.append({'original_id':row['id'],'branch_sizes':values})
    assert gaps[m-6]==4
    for j,row in enumerate(rows):assert gaps[row['b']['lo']]==16*(2**j-1)
    assert amount==4+16*(2**q-1-q)
    return s,gaps,{'q':q,'old_support':m,'physical_support':m+amount,'private_vertices':amount,
        'status':'EXACT_INTEGER_MINIMUM_IN_DECLARED_GAP_BASIS','optimality':'No smaller total satisfies the exact original-trace alias constraints: UNSAT.',
        'gap_basis':atoms,'gaps':gaps,'RR':physical,'seconds':time.perf_counter()-started}


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    out=[]
    for q in (1,3,6,9):
        _,_,result=synthesize(q);out.append(result)
        print(json.dumps({k:result[k] for k in ('q','old_support','physical_support','private_vertices','seconds')}),flush=True)
    path=HERE/'OPTIMIZATION_RESULT.json';assert not path.exists();path.write_text(json.dumps(out,indent=2),encoding='utf-8')


if __name__=='__main__':main()

"""Joint affine-invariant synthesis for the unbounded physical gap recurrence."""
import sys
import json
import z3
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def dot(coeff,values):return z3.Sum([a*b for a,b in zip(coeff,values)])


def learn():
    first=[z3.Int('first_'+str(i)) for i in range(3)]
    second=[z3.Int('second_'+str(i)) for i in range(4)]
    opt=z3.Optimize();opt.set(timeout=10000)
    opt.add(first[0]==1,second[0]==1,*[z3.And(v>=-64,v<=64) for v in first+second])
    opt.minimize(z3.Sum([z3.If(v>=0,v,-v) for v in first+second]))
    c,P,S,j=z3.Ints('leftSize power privateCount completedDoubles')
    pre1=[c,P,1];post1=[2*c+9,2*P,1]
    pre2=[S,P,j,1];post2=[S+c-7,2*P,j+1,1]
    domain=[c>=7,P>=1,S>=4,j>=0];events=[]
    for iteration in range(64):
        assert opt.check()==z3.sat
        model=opt.model();v1=[model.eval(v).as_long() for v in first];v2=[model.eval(v).as_long() for v in second]
        I1=dot(v1,pre1)==0;I2=dot(v2,pre2)==0
        cases=[('initial_first',[],dot(v1,[7,1,1])==0),('initial_second',[],dot(v2,[4,1,0,1])==0),
            ('preserve_first',domain+[I1],dot(v1,post1)==0),
            ('preserve_second_joint',domain+[I1,I2],dot(v2,post2)==0)]
        failed=None
        for name,assumptions,claim in cases:
            check=z3.Solver();check.add(*assumptions,z3.Not(claim));status=check.check()
            assert status!=z3.unknown
            if status==z3.sat:
                cm=check.model();evaluate=lambda values:[cm.eval(x,model_completion=True).as_long() if z3.is_expr(x) else x for x in values]
                failed={'name':name,'pre1':evaluate(pre1),'post1':evaluate(post1),'pre2':evaluate(pre2),'post2':evaluate(post2)}
                break
        events.append({'iteration':iteration,'candidate':[v1,v2],'counterexample':failed})
        if failed is None:return {'status':'PROVED_UNBOUNDED_JOINT_AFFINE_INVARIANTS','first':v1,'second':v2,'events':events,
            'initial':[7,1,4,0],'step':['c=2*c+9','P=2*P','S=S+c-7','j=j+1'],
            'physical_meaning':'P=2^j, c is target-left full physical size; S is total private gap count starting with4 in target-right.',
            'all_q_relation':'c=16*2^j-9, S=4+16*(2^j-1-j), full support after q doubles is16*2^q+5.',
            'scope':'Recurrence invariants. Original physical source provenance uses the H3q comb and rigid-gap identities, not finite interpolation.',
            'universal_CD':'OPEN'}
        name=failed['name']
        if name=='initial_first':opt.add(dot(first,[7,1,1])==0)
        elif name=='initial_second':opt.add(dot(second,[4,1,0,1])==0)
        elif name=='preserve_first':opt.add(z3.Or(dot(first,failed['pre1'])!=0,dot(first,failed['post1'])==0))
        else:opt.add(z3.Or(dot(first,failed['pre1'])!=0,dot(second,failed['pre2'])!=0,dot(second,failed['post2'])==0))
    raise AssertionError('No recurrence certificate within declared budget.')


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    result=learn();p=HERE/'LEARNED_INDUCTION.json';assert not p.exists();p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'status':result['status'],'iterations':len(result['events']),'first':result['first'],'second':result['second']}))


if __name__=='__main__':main()

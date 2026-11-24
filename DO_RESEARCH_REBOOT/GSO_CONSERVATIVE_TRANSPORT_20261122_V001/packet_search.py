"""Bounded exact physical-state adversary for the frozen packet obligation."""
import sys
import time
import json
import random
sys.dont_write_bytecode = True
import transport as T
import role_synthesis as S


def initial(n):
    children = [[0, 0] for _ in range(n+1)]
    for k in range(1, n): children[k][1] = k+1
    parents = [0]+[k-1 for k in range(1, n+1)]
    return ([row.copy() for row in children],parents.copy(),1,
            [row.copy() for row in children],parents.copy(),1,[5]*((n+4)//5),[])


def move(state, mode, target):
    ca,pa,ra,cb,pb,rb,stock,history=state
    ca=[row.copy() for row in ca]; cb=[row.copy() for row in cb]
    pa=pa.copy(); pb=pb.copy(); stock=stock.copy()
    owner=lambda x:(x-1)//5
    if mode=='K' and rb!=target: stock[owner(target)]=5
    peak=0; debt=0; failed=False
    for actor in ('A','B') if mode=='K' else ('A',):
        ch,par,root=(ca,pa,ra) if actor=='A' else (cb,pb,rb)
        while par[target]:
            p=par[target];g=par[p]
            typ='ZIG' if not g else ('L' if p<g else 'R')+('L' if target<p else 'R')
            pivots=[target] if not g else [p,target] if typ in ('LL','RR') else [target,target]
            bits=[];scope=set()
            for y in pivots:
                parent=par[y];grand=par[parent];side=int(y>parent);middle=ch[y][1-side]
                bits.append((y,parent,grand,middle)); scope.update(owner(k) for k in (y,parent,grand,middle) if k)
                ch[parent][side]=middle
                if middle:par[middle]=parent
                ch[y][1-side]=parent;par[parent]=y;par[y]=grand
                if grand:ch[grand][int(parent>grand)]=y
                else:root=y
            if actor=='A':
                for block in scope:stock[block]=5
            else:
                order=[owner(target)]+[i for i in sorted(scope) if i!=owner(target)]
                if typ in ('LL','RR'):
                    first,second=bits
                    roles=[target,second[3],first[2],first[1],second[1],first[3]]
                    order=[]
                    for key in roles:
                        if key and owner(key) not in order:order.append(owner(key))
                assert set(order)==scope
                mass=sum(stock[i] for i in order);q=int(len(bits)==2)
                other=mass-stock[owner(target)];debt=max(0,debt+q-other);peak=max(peak,debt)
                if mass<q:failed=True
                rest=max(0,mass-q)
                for block in order:
                    stock[block]=min(5,rest);rest-=stock[block]
            if failed:break
        if actor=='A':ra=root
        else:rb=root
        if failed:break
    return (ca,pa,ra,cb,pb,rb,stock,history+[[mode,target]]),peak,failed


def fingerprint(s):
    ca,pa,ra,cb,pb,rb,stock,_=s
    return (ra,rb,tuple(pa),tuple(pb),tuple(tuple(r) for r in ca),tuple(tuple(r) for r in cb),tuple(stock))


def main():
    start=time.perf_counter();rng=random.Random(613889);evaluations=0;best=0;report=[];hit=None
    for n in (65,129,257):
        state=initial(n);seeds=[];marked={n+1-2**j for j in range((n-1).bit_length()-1)}
        word=[['D',k] for k in range(2,n+1)]+[['K' if k in marked else 'D',k] for k in range(n,0,-1)]
        for mode,target in word:
            state,peak,failed=move(state,mode,target);assert not failed
            best=max(best,peak)
            if mode=='K':seeds.append(state)
        beam=seeds[-12:];visited={fingerprint(s) for s in beam};local_evaluations=0
        for depth in range(40):
            candidates=[]
            for state in beam:
                # All keys are legal choices. Alternate modes so DELETE
                # preparations remain available rather than being optimized away.
                actions=[(mode,k) for k in range(1,n+1) for mode in ('K','D')];rng.shuffle(actions)
                for mode,target in actions:
                    if evaluations>=120000 or time.perf_counter()-start>=180:break
                    new,peak,failed=move(state,mode,target);evaluations+=1;local_evaluations+=1
                    best=max(best,peak)
                    if failed:
                        hit=(n,new,peak);break
                    fp=fingerprint(new)
                    if fp in visited:continue
                    visited.add(fp)
                    banks=new[6];zeros=sum(v==0 for v in banks)
                    # Multiple concrete objectives keep preparation diversity.
                    score=peak*24+zeros*3-sum(banks)/8+rng.random()*2
                    candidates.append((score,zeros,-sum(banks),new))
                if hit or evaluations>=120000 or time.perf_counter()-start>=180:break
            if hit or not candidates:break
            candidates.sort(key=lambda r:r[0],reverse=True)
            chosen=candidates[:8]
            low=sorted(candidates,key=lambda r:(r[1],r[2],r[0]),reverse=True)
            present={fingerprint(r[3]) for r in chosen}
            for row in low:
                if fingerprint(row[3]) not in present:
                    chosen.append(row);present.add(fingerprint(row[3]))
                if len(chosen)==12:break
            beam=[row[3] for row in chosen]
            if evaluations>=120000 or time.perf_counter()-start>=180:break
        report.append({'n':n,'transition_evaluations':local_evaluations,'maximum_packet_deficit_so_far':best})
        print(json.dumps(report[-1]),flush=True)
        if hit or evaluations>=120000 or time.perf_counter()-start>=180:break
    result={'status':'FAILED_GUARD_PREFIX_FOUND' if hit else 'NO_COUNTEREXAMPLE_IN_BOUNDED_SEARCH',
            'transition_evaluations':evaluations,'maximum_packet_deficit':best,'cases':report,
            'seconds':time.perf_counter()-start,'H':5,'policy':'SELECTED_ROLE_POLICY.json',
            'scope':'Finite exact physical-state successor search; no-hit does not prove arbitrary-source funding.',
            'universal_CD':'OPEN'}
    if hit:
        n,state,peak=hit;initial_tree={'root':1,'children':{str(k):[None,k+1 if k<n else None] for k in range(1,n+1)}}
        full_word=state[7]+[['K',k] for k in range(1,n+1)]+[['K',k] for k in range(n-1,0,-1)]
        source={'name':f'packet_search_failure_N{n}','initial_A':initial_tree,'initial_B':initial_tree,
                'diagonal':initial_tree,'prefix':[],'operations':full_word}
        z=T.F.compile_source(source);T.write('search/counterexample_trace.json.gz',z)
        chosen=T.load(T.HERE/'SELECTED_ROLE_POLICY.json');ev,_=S.prepared(z,tuple(chosen['middle_order']))
        policy=T.B.cyclic_events(z,ev,5,True,'all_original_Q');assert policy['failures']
        T.write('search/counterexample_policy.json.gz',policy)
        free=T.solve(z,5);free['trace']=T.pin(T.HERE/'search/counterexample_trace.json.gz')
        T.write('search/counterexample_free_transport.json.gz',free)
        result['complete_source']={'trace':'search/counterexample_trace.json.gz','A':z['A'],'Q_B':z['Q_B'],
                'policy_failures':len(policy['failures']),'first_failure':policy['failures'][0],'free_paid':free['paid']}
    T.write('PACKET_SEARCH_RESULT.json',result);print(json.dumps(result),flush=True)


if __name__=='__main__':main()

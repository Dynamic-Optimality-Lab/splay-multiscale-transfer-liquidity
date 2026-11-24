"""One bounded theta_1 round; finite results never certify a universal K."""
import hashlib
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
sys.setrecursionlimit(50000)
from sources import HERE,ROOT,canonical,references,vine
from replay import Tree,plain,replay,eligible
from flow import optimize,interval_cut,footprint

START=time.process_time()
ROT=REACH=WARM=0


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def generated():
    global WARM
    rng=random.Random(202611210031)
    refs=[];attempts=[]
    for case in range(64):
        n=[7,11,17,23,31][case%5];initial=vine(n)
        active=sorted(rng.sample(range(1,n+1),min(n,4+case%8)))
        if case%4==0:
            probe=max(2,n//5);outer=list(range(max(probe+2,n//2),n+1))
            word=[['K',x] for x in reversed(outer)]+[['K',probe]]
            word=[z for pair in ((['D',1],x) for x in word) for z in pair]
        else:
            word=[]
            for j in range(12+case%17):
                if j%3==0:word.append(['K',rng.choice(active)])
                else:word.append(['D',rng.randint(1,n)])
            word += [['K',active[0]],['K',active[-1]]]
        trees={a:Tree(initial,list(range(1,n+1))) for a in ('A','B')}
        def statekey():return tuple((t.root,tuple((k,*t.ch[k]) for k in t.keys)) for t in trees.values())
        seen={statekey():0};states=[{a:t.state() for a,t in trees.items()}]
        found=None
        for lap in range(1,65):
            for mode,x in word:
                WARM+=plain(trees['A'],x)
                if mode=='K':WARM+=plain(trees['B'],x)
            key=statekey()
            if key in seen:
                begin=seen[key]
                source={'name':f'periodic_{case:02d}_n{n}','initial_A':states[begin]['A'],'initial_B':states[begin]['B'],
                        'operations':word*(lap-begin),'prefix':word*begin,'diagonal':initial,
                        'generation':{'seed':202611210031,'candidate':case,'base_word':word,'prefix_copies':begin,'period_copies':lap-begin}}
                filename=f'generated_{case:02d}.json'
                (HERE/filename).write_text(json.dumps(source,separators=(',',':')),encoding='utf-8')
                refs.append({'kind':'generated','file':filename,'name':source['name']})
                found={'candidate':case,'closed':True,'warmup_copies':begin,'period_copies':lap-begin,'n':n};break
            seen[key]=lap;states.append({a:t.state() for a,t in trees.items()})
            assert WARM<=1000000 and time.process_time()-START<=360
        attempts.append(found or {'candidate':case,'closed':False,'n':n,'copies_attempted':64})
    (HERE/'GENERATED_CYCLE_SEARCH.json').write_text(json.dumps({'attempts':attempts,'warmup_search_rotations':WARM},indent=2),encoding='utf-8')
    return refs


def main():
    global ROT,REACH
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    refs=references()+generated();assert len(refs)<=280
    paths={r['path'] for r in refs if 'path' in r}
    pins=[{'path':p,'sha256':digest(ROOT/p)} for p in sorted(paths)]
    (HERE/'PINNED_SOURCE_INPUTS.json').write_text(json.dumps(pins,indent=2),encoding='utf-8')
    (HERE/'SOURCE_REFERENCES.json').write_text(json.dumps(refs,indent=2),encoding='utf-8')
    summaries=[]
    for index,ref in enumerate(refs):
        s=canonical(ref)
        def guard(rot,reach):
            assert ROT+rot<=3000000 and REACH+reach<=1000000 and time.process_time()-START<=360
        rep=replay(s,guard);ROT+=rep['rotations'];REACH+=rep['reach_rotations']
        if rep['full_carrier']:
            # Exhaust the actual evaluated frame/unit table on small sources;
            # the symbolic pivot lemma handles arbitrary sizes.
            if rep['root_rotations_only'] and len(rep['keys'])<=35:
                for d in rep['demands']:
                    a,b=d['span']
                    for u in rep['units']:
                        actual=any(eligible(bit,a,b) for bit in u['bits'])
                        assert actual==any(a<=x<=b for x in footprint(u))
        allocation=optimize(rep);local=interval_cut(rep,1)
        case={'index':index,'ref':ref,'name':s['name'],'physical_keys':rep['keys'],'S':rep['S'],
              'full_carrier':rep['full_carrier'],'root_rotations_only':rep['root_rotations_only'],'A':rep['A'],'Q_B':rep['Q_B'],
              'original_ops':len(s['operations']),'period_rotations':rep['rotations'],'prefix_rotations':rep['reach_rotations'],
              'period_clock':rep['period_clock'],'demands':rep['demands'],'allocation':allocation,'split_pivot_interval_test':local}
        file=f'case_{index:03d}.json';(HERE/file).write_text(json.dumps(case,separators=(',',':')),encoding='utf-8')
        summary={k:case[k] for k in ('index','name','full_carrier','A','Q_B','original_ops','period_rotations','prefix_rotations')}
        summary.update(file=file,U_int=len(rep['demands']),K=allocation['K'],interval_C1=local['all_intervals_pass'] if local else None)
        summaries.append(summary)
        if index%20==0 or allocation['K']>1 or index==len(refs)-1:
            print(json.dumps({'done':index+1,'name':s['name'],'U_int':len(rep['demands']),'K':allocation['K'],'rotations_so_far':ROT,'cpu':round(time.process_time()-START,3)}),flush=True)
    out={'status':'FINITE-EXACT only; universal theta_1 conservation OPEN unless a separate symbolic proof is completed',
         'cases':summaries,'case_count':len(summaries),'period_rotations':ROT,'reaching_rotations':REACH,'warmup_search_rotations':WARM,
         'K_histogram':dict(Counter(c['K'] for c in summaries)),'cpu_seconds':time.process_time()-START}
    (HERE/'FINITE_AUDIT.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}),flush=True)


if __name__=='__main__':main()

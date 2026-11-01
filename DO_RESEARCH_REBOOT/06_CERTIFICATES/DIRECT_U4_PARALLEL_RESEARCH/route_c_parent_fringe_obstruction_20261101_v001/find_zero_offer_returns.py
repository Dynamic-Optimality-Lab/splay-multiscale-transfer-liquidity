"""One fixed source-anchor zero-FI-offer return classification.

Uses only the old complete seven-core relation. Clock saturation is derived
from maximum capacity6, never a guessed path horizon or fitted coefficient.
"""
import hashlib
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_fi_rejection_certificates_20261101_v001'
KC=HERE.parent/'route_c_seven_core_return_obstruction_20261031_v001'
EC=HERE.parent/'route_c_seven_core_excess_capacity_20261031_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def path(t,key):
    out=[];dirs=[]
    while t:
        out.append(t)
        if t[0]==key:return out,dirs
        side='L' if key<t[0] else 'R';dirs.append(side);t=t[1 if side=='L' else 2]
    raise AssertionError('present source key')
def contains(t,key):
    while t:
        if key==t[0]:return True
        t=t[1 if key<t[0] else 2]
    return False


def profile(t,x,y):
    px,dirs=path(t,x);py,_=path(t,y);h=len(py)-1;d=len(dirs)
    common=0
    while common<min(len(px),len(py)) and px[common][0]==py[common][0]:common+=1
    ops=[]
    for z in range(d//2):
        top=d-2*(z+1);ops.append(dict(case=''.join(dirs[top:top+2]),site_depth=top,
            grandparent=px[top][0],parent=px[top+1][0]))
    if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=px[0][0],parent=None))
    entry=None;mu=pf_mu=r=match=0;pf_role=False
    if d==0:role='root_noop';oldraw=newraw=h
    elif x==y:role='accessed';oldraw=newraw=0
    else:
        entry=next(z for z,op in enumerate(ops) if op['site_depth']<=common-1);op=ops[entry]
        if op['case']=='ZIG':role='zig';mu=1
        elif y==op['parent']:role='parent';mu=0
        else:role='other';mu=2
        pf_mu=mu
        if op['case'] in ['LR','RL']:
            parent=px[op['site_depth']+1]
            outer=parent[1 if op['case']=='LR' else 2]
            pf_role=contains(outer,y)
            if pf_role:pf_mu=0
        later=[op for op in ops[entry+1:] if op['case']!='ZIG'];r=len(later)
        match=sum(op['case']==('LL' if y<x else 'RR') for op in later)
        oldraw=h+mu-r-match;newraw=h+pf_mu-r-match
    old=min(h+2,max(0,oldraw));new=min(h+2,max(0,newraw))
    assert 0<=new<=old
    return dict(source_depth=h,access_depth=d,operations=ops,entry=entry,role=role,
        parent_outer_fringe=pf_role,old_mu=mu,new_mu=pf_mu,outer_doubles=r,
        matching_outer_doubles=match,old_U=old,PF_U=new)


def main():
    inherited=read(OLD/'entry_source_pins.json');pins=dict(inherited['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==inherited['stage_files'] and len(stage)==125
    assert (git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no'))==(inherited['head'],inherited['branch'],'')
    save('entry_source_pins.json',dict(date='2026-11-01',files=pins,stage_files=stage,
        head=inherited['head'],branch=inherited['branch'],tracked_status='',gate_sha256=sha(HERE/'PF00_FOUR_RULE_GATE.md')))
    for name,h in read(OLD/'delivery_manifest.json')['files'].items():assert sha(OLD/name)==h
    table=read(KC/'source_transition_table.json');graph=read(KC/'reachable_relation_certificate.json')
    basis=read(KC/'independent_audit.json');cap=read(EC/'capacity_certificate.json')
    assert basis['status']=='PASS' and basis['source_table_sha256']==sha(KC/'source_transition_table.json')
    assert basis['relation_sha256']==sha(KC/'reachable_relation_certificate.json')
    pairs,edges,labels=graph['pair_ids'],graph['outgoing_edges'],cap['component_labels']
    tt,cores,F=table['transitions'],table['cores'],table['fringe']
    C={i for i,c in enumerate(labels) if c==labels[4676]};assert len(C)==18232
    def embed(t):return None if t is None else [t[0],embed(t[1]),F if t[0]==7 else embed(t[2])]
    def tr(i,key):return tt[7*i+key-1]
    fixed=[];state=4676
    for key in [6,4,1]:
        edge=next(e for e in edges[state] if e[0]==key)
        ar,br=tr(pairs[state][0],key),tr(pairs[state][1],key)
        fixed.append(dict(source=state,key=key,target=edge[1],a=ar['a'],q=br['q'],delta=edge[2]))
        state=edge[1]
    assert [r['target'] for r in fixed]==[7994,2002,4327]
    assert [(r['a'],r['q'],r['delta']) for r in fixed]==[(1,3,1),(1,2,0),(1,1,-1)]
    T=embed(cores[pairs[7994][1]])
    profiles={str(y):profile(T,4,y) for y in range(1,8)}
    assert profiles['1']['parent_outer_fringe'] and (profiles['1']['old_U'],profiles['1']['PF_U'])==(4,2)
    assert profiles['4']['old_U']==profiles['4']['PF_U']==0
    assert profiles['1']['old_U']//2==2 and profiles['1']['PF_U']//2==1
    start=7*4327+1 # clock k=2
    targets={'anchor_return':7*4676+6,'reset_return':7*12919+6}
    parent={start:None};queue=deque([start]);allowed_edges=0
    while queue:
        node=queue.popleft();s,k=node//7,node%7+1
        for key,t,delta in edges[s]:
            if t not in C or delta>0:continue
            ar=tr(pairs[s][0],key);br=tr(pairs[s][1],key)
            assert ar['a']<=3 and br['depth']>0
            ceiling=profiles[str(key)]['old_U']//2+k-1
            if ceiling<2*ar['a']:continue
            assert br['q']<=2*ar['a']
            dest=7*t+min(7,k+1)-1;allowed_edges+=1
            if dest not in parent:parent[dest]=[node,key];queue.append(dest)
    def route(target):
        if target not in parent:return None
        reverse=[];at=target
        while at!=start:
            p,key=parent[at];s,k=p//7,p%7+1;t,kk=at//7,at%7+1
            ar,br=tr(pairs[s][0],key),tr(pairs[s][1],key)
            reverse.append(dict(source=s,k=k,key=key,target=t,next_k=kk,
                a=ar['a'],q=br['q'],delta=br['q']-2*ar['a'],
                old_ceiling_lower_bound=profiles[str(key)]['old_U']//2+k-1))
            at=p
        return reverse[::-1]
    paths={name:route(node) for name,node in targets.items()}
    status='BOTH_FIXED_RETURNS_FOUND' if all(v is not None for v in paths.values()) else 'FIXED_RETURN_CLASS_PARTIAL_OR_ABSENT'
    save('fixed_return_certificate.json',dict(status=status,date='2026-11-01',
        gate_sha256=sha(HERE/'PF00_FOUR_RULE_GATE.md'),
        source_table_sha256=sha(KC/'source_transition_table.json'),source_graph_sha256=sha(KC/'reachable_relation_certificate.json'),
        source_audit_sha256=sha(KC/'independent_audit.json'),component=labels[4676],component_size=len(C),
        anchor=4676,fixed_prefix=fixed,post_anchor_T=T,profiles=profiles,first_intervention_key=4,
        start_state=4327,start_clock=2,clock_saturation=7,maximum_A_capacity=6,
        node_encoding='7*source_state+(k-1)',reachable_nodes=sorted(parent),
        predecessor_rows=[[node,*parent[node]] for node in sorted(parent) if parent[node] is not None],
        reachable_nodes_count=len(parent),allowed_reachable_edges=allowed_edges,
        targets=targets,paths=paths,
        V_KEEP_word=[6,4,1]+[e['key'] for e in paths['anchor_return']] if paths['anchor_return'] is not None else None,
        Y_KEEP_word=[6,4,1]+[e['key'] for e in paths['reset_return']] if paths['reset_return'] is not None else None,
        new_active_core_sizes=0,larger_finite_fits=0,new_source_engine_calls=0,
        matching_terminal_line='FROZEN',universal_CD='OPEN',automatic_successor_launched=False))
    print(json.dumps(dict(status=status,reachable_nodes=len(parent),allowed_edges=allowed_edges,
        source_profile_target1=profiles['1'],
        V=[6,4,1]+[e['key'] for e in paths['anchor_return']] if paths['anchor_return'] is not None else None,
        Y=[6,4,1]+[e['key'] for e in paths['reset_return']] if paths['reset_return'] is not None else None,
        preserved_files=len(pins)),indent=2))


if __name__=='__main__':main()

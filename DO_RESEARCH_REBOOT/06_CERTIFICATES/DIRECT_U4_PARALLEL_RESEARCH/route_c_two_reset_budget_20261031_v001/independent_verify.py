"""Independent pointer-source B-budget certification; no A-policy search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def main():
    cp=HERE/'B_budget_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('pointer_source',ROOT/'python/liquidity/legacy_embedding.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    def ptr(t):
        if t is None:return None
        z=p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if z[side] is not None:z[side]['p']=z
        return z
    def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
    def mirror(t):return None if t is None else [14-t[0],mirror(t[2]),mirror(t[1])]
    def vine():
        t=None
        for k in range(13,0,-1):t=[k,None,t]
        return t
    def inorder(t):return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])
    def depth(t,x):
        d=0
        while t is not None:
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2];d+=1
        raise AssertionError('present B request')
    calls=trees=0
    def access(t,x,occ):
        nonlocal calls,trees
        ck(inorder(t)==list(range(1,14)),'source B exact key set and strict BST');trees+=1
        d=depth(t,x);out,events=p.splay_trace(ptr(t),x);after=raw(out)
        ck(inorder(after)==list(range(1,14)),'destination B exact key set and strict BST');trees+=1
        ev=[[e['case'],e['lo'],e['hi'],e['orient']] for e in events]
        q=sum(e[0]!='ZIG' for e in ev);z=sum(e[0]=='ZIG' for e in ev)
        ck((q,z,len(ev))==(d//2,d%2,(d+1)//2),'exact B grouped events')
        calls+=1
        return after,dict(occurrence=occ,key=x,source_B=t,destination_B=after,d_B=d,q=q,z=z,B_events=ev)
    def mirror_row(r):
        cm={'LL':'RR','RR':'LL','LR':'RL','RL':'LR','ZIG':'ZIG'};om={'L':'R','R':'L','-':'-'}
        return dict(r,key=14-r['key'],source_B=mirror(r['source_B']),destination_B=mirror(r['destination_B']),
          B_events=[[cm[e[0]],14-e[2],14-e[1],om[e[3]]] for e in r['B_events']])
    V=[1,9,5,13,3,11,7,2,10,6,4,12,8]
    ck(cert['KEEP_skeleton']==V and cert['initial_B']==vine() and cert['key_size']==13 and cert['lap_cap']==64,'literal gated B skeleton')
    b=vine();mb=mirror(b);rows=[];boundaries=[dict(lap=0,B=b)];seen={json.dumps(b):0};start=end=None
    for lap in range(1,65):
        for x in V:
            b,r=access(b,x,len(rows));mb,mr=access(mb,14-x,len(rows))
            ck(mr==mirror_row(r),'independent reflected source states/events')
            ck(r==cert['full_replay'][len(rows)],'complete tuple/pointer B agreement')
            rows.append(r)
        boundaries.append(dict(lap=lap,B=b));key=json.dumps(b)
        if key in seen:start=13*seen[key];end=len(rows);break
        seen[key]=lap
    ck(start==13 and end==26 and boundaries==cert['boundary_records'],'first exact B boundary recurrence')
    cyc=rows[start:end];period=(end-start)//13
    ck(cyc[-1]['destination_B']==cyc[0]['source_B'] and len({json.dumps(r['source_B']) for r in cyc})==len(cyc),'primitive actual B cycle')
    G=sum(max(r['q']-2,0) for r in cyc);capacity=4*period
    ck(G==3 and capacity==4 and [r['q'] for r in cyc]==cert['q_vector'],'exact upper excess profile')
    ck(cert['cycle_G_B']==G and cert['two_effective_reset_capacity']==capacity and
      cert['primitive_period_laps']==period and cert['transient_laps']==1,'budget dimensions')
    ck(not cert['B_budget_passed'] and cert['outcome']=='BUDGET_BLOCKED' and cert['A_policy_cases_executed']==0,'predeclared gate stops A classification')
    old=json.loads((HERE.parent/'route_c_sparse_reset_strictness_20261031_v001/sparse_reset_certificate.json').read_text(encoding='utf-8'))
    W=[13,11,12,9,10,7,8,5,6,3,4,1,2];ob=vine();omb=mirror(ob);oldrows=[]
    for lap in range(1,3):
        for x in W:
            ob,r=access(ob,x,len(oldrows));omb,mr=access(omb,14-x,len(oldrows))
            ck(mr==mirror_row(r),'old B source orientation check');oldrows.append(r)
        ck(ob==old['shared_B_boundary_states'][str(lap)],'old recurrent B state matches pinned source bank')
    oldcycle=oldrows[13:26];oldG=sum(max(r['q']-2,0) for r in oldcycle)
    ck(oldcycle[-1]['destination_B']==oldcycle[0]['source_B'] and oldG==4,'old B fixed-cycle budget exactly four')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['adaptive_skeleton_changes']==0 and
      cert['matching_terminal_line']=='FROZEN','scope and freeze')
    with (HERE/'old_B_budget_replay.json').open('x',encoding='utf-8') as f:
        json.dump(dict(skeleton=W,full_replay=oldrows,cycle_G_B=oldG,reflected_rows_independently_verified=True),f,indent=2);f.write('\n')
    result=dict(status='PASS',date='2026-10-31',new_B_orbit_rows_per_orientation=len(rows),
      old_B_orbit_rows_per_orientation=len(oldrows),source_orientations=2,pointer_source_accesses=calls,
      strict_BST_tree_occurrences_validated=trees,new_B_transient_laps=1,new_B_period_laps=1,
      new_B_cycle_Q=sum(r['q'] for r in cyc),new_B_cycle_Z=sum(r['z'] for r in cyc),new_B_cycle_G=G,
      old_B_cycle_Q=sum(r['q'] for r in oldcycle),old_B_cycle_G=oldG,two_reset_minimum_capacity=4,
      policy_cases_declared_if_budget_passed=78,A_policy_cases_executed=0,new_pair_cycles_extracted=0,
      new_FI_UD_cut_trials=0,new_cycle_credit_assignments=0,strict_new_closed_walk_coverage='NOT ESTABLISHED',
      architecture_budget_outcome='BLOCKED: E<=3p<4p<=C_D on complete recurrent periods',
      old_skeleton_multi_reset_outcome='BLOCKED: E<=4p<=C_D',
      no_prefix_or_second_lap_credit=True,no_virtual_credit_pool=True,producer_imported=False,old_recognizers_executed=False,
      finite_fits=0,size_sweeps=0,adaptive_skeleton_changes=0,matching_terminal_line='FROZEN',universal_CD='OPEN',
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()

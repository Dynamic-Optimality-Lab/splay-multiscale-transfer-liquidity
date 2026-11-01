"""Refute the fixed AT root bound, reusing its unmodified evaluator in memory.

The imported module's main/save functions are never called. All disk writes
are exclusive in this new run. There is no fit or change to the candidate.
"""
from pathlib import Path
from collections import deque
import hashlib,importlib.util,json,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PRIOR=OUT.parent/'route_c_antichain_terminal_20261031_v001'
spec=importlib.util.spec_from_file_location('fixed_AT_evaluator',(PRIOR/'audit_antichain_terminal.py'))
E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def main():
    ck((OUT/'RB00_FOUR_RULE_GATE.md').is_file(),'written gate precedes audit')
    entry=json.loads((PRIOR/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(PRIOR.relative_to(ROOT).as_posix()+'/'+p for p in ['AT00_FOUR_RULE_GATE.md','AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md',
      'AT02_ALL_SIZE_REPAIRS_AND_OPEN_ROOT_STEPS.md','AT03_STRATEGY_REVIEW.md','AT04_FINAL_REPORT.md','audit_antichain_terminal.py',
      'independent_verify.py','antichain_terminal_certificate.json','independent_audit.json','final_integrity.json'])
    pins={p:sha(ROOT/p) for p in sorted(paths)};ck(all(pins[p]==h for p,h in entry['files'].items()),'all inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'RB00_FOUR_RULE_GATE.md'),
      'unchanged_evaluator_path':(PRIOR/'audit_antichain_terminal.py').relative_to(ROOT).as_posix(),
      'unchanged_candidate_definition':(PRIOR/'AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md').relative_to(ROOT).as_posix()})
    n=7;leaf=lambda k:E.S.node(k,E.S.LEAF,E.S.LEAF)
    middle=leaf(n-1)
    for k in range(n-2,2,-2):middle=E.S.node(k,leaf(k-1),middle)
    a=E.S.node(1,E.S.LEAF,E.S.node(n,middle,E.S.LEAF));b=E.S.vine(n)
    aa,bb,bad=E.edge('fixed_antichain_root_zig_DELETE7',a,b,'D',n,True)
    ck((bad['dA'],bad['a'],bad['q'],bad['z'],bad['delta_Phi'],bad['budget'])==(1,1,0,0,3,2),'registered single-zig refutation')
    ck((bad['source_completion']['F_terminal'],bad['destination_completion']['F_terminal'],bad['source_completion']['alpha_terminal'],bad['destination_completion']['alpha_terminal'])==(5,5,1,1),'equal terminal F and alpha')
    ck((bad['source_completion']['K_terminal'],bad['destination_completion']['K_terminal'],bad['source_completion']['Phi'],bad['destination_completion']['Phi'],bad['R_source'],bad['R_destination'])==(4,4,4,7,1,1),'unchanged K and correction, completion charge increases')
    _,_,reflected=E.edge('reflected_root_zig_DELETE1',E.mirror(a,n),E.mirror(b,n),'D',1,True)
    ck((reflected['dA'],reflected['a'],reflected['delta_Phi'],reflected['budget'])==(1,1,3,2),'other zig orientation refuted')
    # Only a single-tree reachability connector. No potential evaluations.
    old_terminal_count=len(E.TERMINALS);queue=deque([b]);previous={b:None};expanded=requests=0
    while queue:
        t=queue.popleft()
        if t==a:break
        expanded+=1
        for x in range(1,n+1):
            u,_=E.S.trace(t,x);requests+=1
            if u not in previous:previous[u]=(t,x);queue.append(u)
    ck(a in previous and len(previous)<=429 and len(E.TERMINALS)==old_terminal_count,'bounded connector without potential evaluations')
    prefix=[];cur=a
    while previous[cur] is not None:
        parent,x=previous[cur];prefix.append(['D',x]);cur=parent
    prefix.reverse();failed=len(prefix)
    word=prefix+[['D',7]]+[['K',x] for x in range(1,8)]+[['K',x] for x in range(6,0,-1)]
    ca=cb=b;replay=[]
    for i,(mode,x) in enumerate(word):ca,cb,r=E.edge('closed_'+str(i),ca,cb,mode,x);replay.append(r)
    ck(ca==cb==b,'actual paired diagonal closure')
    ck(replay[failed]['source_A']==E.raw(a) and replay[failed]['source_B']==E.raw(b),'registered counteredge reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck(Qt==0 and Zt==12 and sum(r['delta_Phi'] for r in replay)==0,'actual costs and explicit telescope')
    save('root_bound_countercertificate.json',{'date':'2026-10-31','fixed_candidate':'unchanged AT antichain terminal K and root completion Phi',
      'controls':[bad,reflected],'terminal_graphs':E.TERMINALS,'raw_P_graphs':E.RAW_P,
      'all_odd_family':{'n':'odd n=2m+1>=7','source_F':'n-2','destination_F':'n-2','source_alpha':1,'destination_alpha':1,
        'source_K':'n-3','destination_K':'n-3','source_completion_Q':0,'destination_completion_Q':'m',
        'actual_A_depth':1,'actual_a':1,'actual_q':0,'root_step_increment':'m=(n-1)/2','bound':2,
        'source_P':'m','destination_P':'2m','source_R':'m-2','destination_R':'m-2'},
      'closed_witness':{'initial_A':E.raw(b),'initial_B':E.raw(b),'word':word,'failed_edge_index':failed,'full_replay':replay,
        'A':At,'Q_B':Qt,'Z_B':Zt,'other_failed_indices':[i for i,r in enumerate(replay) if not r['whole_law_holds']]},
      'connector':{'single_tree_BFS_calls':1,'n':7,'states_visited':len(previous),'states_expanded':expanded,'source_requests':requests,'potential_evaluations_during_BFS':0},
      'root_double_cases_classified':False,'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'candidate_modified':False})
    print(json.dumps({'root_zig_refuted':True,'actual_A_depth':bad['dA'],'actual_a':bad['a'],'actual_q':bad['q'],
      'K_values':[bad['source_completion']['K_terminal'],bad['destination_completion']['K_terminal']],
      'Phi_values':[bad['source_completion']['Phi'],bad['destination_completion']['Phi']],
      'R_values':[bad['R_source'],bad['R_destination']],'delta':bad['delta_Phi'],'bound':bad['budget'],
      'terminal_graphs':len(E.TERMINALS),'antichain_duals':sum(len(g['maximal_antichain_duals']) for g in E.TERMINALS),
      'raw_P_graphs':len(E.RAW_P),'closed_word':word,'registered_failure_index':failed,
      'totals':[At,Qt,Zt],'other_failed_indices':[i for i,r in enumerate(replay) if not r['whole_law_holds']],
      'connector_states':len(previous),'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()

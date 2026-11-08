"""Seal a genuinely signed closed prefix and identify the remaining original family."""
import json,sys,time,collections
import z3
from support import BASE,trees,ids,psi,depth,destination,kernel,opp,PATHS,gamma_words,build
CAP=min(120,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def canon(v):return tuple(canon(q) for q in v) if isinstance(v,list) else v
def main():
    report=json.loads((BASE/'audit_independent.json').read_text());n=report['last_signed_closed_prefix'];cs=report['clauses'][:n]
    assert n==2963
    for name in ('audit_completion_v2.json','audit_joint.json'):
        old=json.loads((BASE/name).read_text())['clauses'];assert old==cs[:len(old)]
    mirrors=[ids[opp(t)] for t in trees];helpers={}
    for q in kernel['rows']:
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        i,x,j,w=q['entry_core'],q['target'],q['exit_core'],q['w']
        for h,i,x,j in ((0,i,x,j),(9,mirrors[i],8-x,mirrors[j])):helpers.setdefault(i,set()).add((h,x,j,w))
    jobs={}
    def J(i,k):
        if (i,k) not in jobs:
            out=set()
            if psi[i]<k:
                for x in range(9):
                    j=destination[i][x];w=2-depth[i][x]//2
                    if w>=k or w+psi[j]>=k:continue
                    for p in PATHS:
                        if p[0]==int(x>trees[i][0]):out.add((i,k,None,(p,),x,j,w))
                if k==2:
                    for h,x,j,w in helpers.get(i,set()):
                        if w+psi[j]>=k:continue
                        for word in gamma_words(trees[i][0],x,h):out.add((i,k,h,word,x,j,w))
            jobs[i,k]=out
        return jobs[i,k]
    proven=set();accepted_records={}
    for file,limit in (('completion_v2_checkpoints.jsonl',743),('joint_checkpoints.jsonl',1349),('independent_checkpoints.jsonl',None)):
        count=0
        for line in (BASE/file).read_text().splitlines():
            q=json.loads(line);prefix=limit if limit is not None else q['formula_prefix_length']
            if prefix>n:continue
            assert q['proof']=='UNIVERSAL_UNSAT';key=canon(q['job'])
            for cid in q['source_clause_ids']:
                assert cid<n and cid<prefix
                c=cs[cid];assert key in J(c['core'],c['level']);proven.add((cid,key))
            count+=1
        accepted_records[file]=count
    missing=[];required=0
    for cid,c in enumerate(cs):
        for key in J(c['core'],c['level']):
            required+=1
            if (cid,key) not in proven:missing.append((cid,key))
    assert not missing,missing[:3]
    inv=json.loads((BASE/'positive_inventory.json').read_text());gamma=[]
    for q in inv['Gamma1_gap0_critical_rows']:
        i,x,j=q['entry_core'],q['target'],q['exit_core']
        for h,i,x,j in ((0,i,x,j),(9,mirrors[i],8-x,mirrors[j])):
            for word in gamma_words(trees[i][0],x,h):gamma.append((i,x,j,h,word))
    closed={}
    for file,limit in (('gamma_checkpoints.jsonl',743),('joint_gamma_checkpoints.jsonl',1349),('independent_gamma_checkpoints.jsonl',None)):
        for line in (BASE/file).read_text().splitlines():
            q=json.loads(line);prefix=limit if limit is not None else q['formula_prefix_length']
            if prefix>n:continue
            number=q['job'];assert canon([q['source_core'],q['target_key'],q['destination_core'],q['helper'],q['word']])==gamma[number]
            assert q['proof'] in ('UNIVERSAL_UNSAT','STATIC_VISIBLE_SEED_CAPACITY_CONTRADICTION');closed[number]=q
    stop=report['Gamma1_next_job'];assert set(range(stop))<=set(closed)
    remaining=gamma[stop:];roots={trees[i][0] if h==0 else 8-trees[i][0] for i,x,j,h,w in remaining}
    assert roots=={8},roots
    # NEW universal public source implication: hidden helper + extremal root
    # and tall core necessarily satisfies the already proved old ceiling H.
    tall=[];x=z3.Int('extremal_hidden_terminal')
    for h in (0,9):
        for p in ((0,0),(0,1)):
            word=(p,(1,0)) if h==0 else tuple(tuple(1-v for v in q) for q in (p,(1,0)))
            r=8 if h==0 else 0
            u=build(word,r,x,h,'tall'+str(len(tall)));a=u['source']
            if h==9:a=__import__('support').opposite_alpha(a)
            guard=z3.And(a[1]<=9,z3.Or(a[3]==9,z3.And(a[1]==9,a[4]==9)),*(a[j]!=0 for j in range(1,7)))
            sol=z3.Solver();sol.add(*u['constraints'],x>=1 if h==0 else x>=0,x<=7,z3.Not(guard))
            assert sol.check()==z3.unsat
            tall.append({'helper':h,'word':word,'old_ceiling_public_conditions_negation':'UNSAT'})
    assert time.process_time()<CAP-2
    out={'status':'UNIVERSAL_CLOSED_PREFIX_AND_EXTREMAL_REDUCTION_PASS','clauses':cs,'accepted_clause_count':n,
      'required_signed_clause_word_obligations':required,'covered_signed_clause_word_obligations':len(proven),
      'missing_signed_obligations':0,'accepted_proof_records':accepted_records,
      'Gamma1_closed_initial_jobs':stop,'Gamma1_total_jobs':len(gamma),'Gamma1_remaining_jobs':len(remaining),
      'remaining_source_roots':'minimum helper:8; actual maximum:0','all_nonextremal_helper_obligations_closed':True,
      'tall_hidden_source_exclusion':tall,'discarded_unproved_tail_clauses':len(report['clauses'])-n,
      'new_finite_tests':0,'completed_semantic_checks_replayed':0,'M3_complete':False}
    write('audit_prefix.json',out);print(json.dumps({k:v for k,v in out.items() if k not in ('clauses','tall_hidden_source_exclusion')},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_prefix_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

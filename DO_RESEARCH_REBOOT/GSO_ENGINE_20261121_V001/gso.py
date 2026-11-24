"""First bounded working GSO command line; every universal claim requires a proof contract."""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from kernel import HERE,dump,load,source_from_cycle
import teacher


def outdir(name):
    root=(HERE/name).resolve();assert root.is_relative_to(HERE) and root!=HERE
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'Sealed engine; use a fresh versioned copy for new writes.'
    root.mkdir(parents=True,exist_ok=True);return root


def build_run(args):
    out=outdir(args.output);summary=[]
    for n in range(args.min_support,args.max_support+1):
        path=out/f'graph_{n}.json.gz'
        if path.exists():
            graph=load(path)
            if 'SCC' not in graph:teacher.annotate_recurrence(graph);dump(path,graph)
        else:graph=teacher.build(n);dump(path,graph)
        trials={}
        for C in ['0','1/2','1','2']:
            trial=teacher.exact_trial(graph,C);trials[C]=trial
            if trial['status']=='VIOLATING_CYCLE':dump(out/f'cycle_n{n}_C{C.replace("/","_")}.json',{'source':source_from_cycle(graph,trial['cycle'],f'trial_n{n}_C{C}'),'certificate':trial})
        best=teacher.optimum(graph);dump(out/f'certificates_{n}.json.gz',{'trials':trials,'optimum':best})
        if best.get('attaining_cycle'):dump(out/f'optimum_cycle_n{n}.json',{'source':source_from_cycle(graph,best['attaining_cycle'],f'optimum_n{n}'),'C':best['C']})
        row={'support':n,'trees':len(graph['trees']),'reachable_pairs':len(graph['pairs']),'edges':len(graph['edges']),'exact_finite_C':best.get('C'),'status':best['status'],'build_cpu_seconds':graph['build_cpu_seconds']}
        summary.append(row);print(json.dumps(row),flush=True)
    dump(out/'GRAPH_SUMMARY.json',{'scope':'Complete exact finite original-state graphs only. Increasing support requires a separate source-uniform proof.','cases':summary})


def attack_run(args):
    from adversary import build_sources
    import learner
    out=outdir(args.output);rows=[];graphs={}
    for n in range(1,7):
        path=out/f'graph_{n}.json.gz';graph=load(path)
        if 'SCC' not in graph:teacher.annotate_recurrence(graph);dump(path,graph)
        graphs[n]=graph;rows.extend(teacher.graph_rows(graph))
    selected=out/'selected_source_rows.json.gz'
    if selected.exists():source_rows=load(selected)
    else:source_rows=build_sources(out);dump(selected,source_rows)
    rows+=source_rows;seed=learner.evaluate_seed(rows);dump(out/'SEED_E3_RESULT.json',seed)
    results=[]
    for columns,grammar in [(6,'frontier3'),(12,'frontier3_roots_guarded')]:
        result=learner.fit(rows,columns,grammar,out);dump(out/(grammar+'_synthesis.json'),result);results.append(result)
        # Every finite-graph failure can be embedded in an original closed
        # source because only recurrent edges entered the candidate teacher.
        for j,r in enumerate(result['history']):
            ident=r['worst_row']
            if ident[0]=='graph' and r['worst_exact_slack']!='0':
                n,eid=ident[1:];cycle=teacher.close_edge(graphs[n],eid)
                dump(out/f'{grammar}_counter_round{j}.json',{'source':source_from_cycle(graphs[n],cycle,f'{grammar}_round{j}'),'failing_original_operation':1,'candidate':{'theta':r['theta'],'C':r['C'],'grammar':grammar}})
    dump(out/'ATTACK_SUMMARY.json',{'source_uniform_root':'OPEN','finite_recurrent_graph_rows':len(rows)-len(source_rows),'historical_and_parametric_selected_rows':len(source_rows),'results':[{'grammar':r['grammar'],'status':r['status'],'candidate':r.get('candidate')} for r in results],
                                  'scope':'Finite exact CEGIS only until the symbolic whole-operation cost contract is universally proved. No finite result closes the root.'})


def research_run(args):
    """One real bounded end-to-end slice, with cached stages explicit."""
    start=time.process_time();out=outdir(args.output);stages=[]
    def stage(name,fn,cached=False):
        t=time.perf_counter()
        if not cached:fn()
        stages.append({'stage':name,'reused_existing_certificate':cached,'wall_seconds':time.perf_counter()-t})
    if not (out/'GRAPH_SUMMARY.json').exists():
        args.min_support=1;args.max_support=6;stage('complete_original_graphs_and_exact_teacher',lambda:build_run(args))
    else:stage('complete_original_graphs_and_exact_teacher',lambda:None,True)
    stage('bounded_CEGIS_on_frozen_nonlinear_grammars',lambda:attack_run(args),(out/'ATTACK_SUMMARY.json').exists())
    from adversary import holdouts
    from symbolic import run as symbolic_run
    from parametric import run as parametric_run
    from registry import candidate_failures,finalize
    from flow_adapter import run as flow_run
    stage('holdout_original_source_adversary',lambda:holdouts(out))
    stage('rigid_subtree_and_learned_loop_invariants',lambda:symbolic_run(out),(out/'LOOP_INDUCTION_CERTIFICATE.json').exists())
    stage('parametric_source_constraints_and_exact_dual',lambda:parametric_run(out),(out/'PARAMETRIC_DUAL_CERTIFICATE.json').exists())
    stage('literal_complete_source_counterexamples',lambda:candidate_failures(out))
    stage('frozen_flow_oracle_and_independent_original_U_checker',lambda:flow_run(out),(out/'FLOW_ADAPTER_VERIFICATION.json').exists())
    def lean():
        # Explicit installed version: no dependency installation or lake build.
        r=subprocess.run(['lean','+leanprover/lean4:v4.21.0',str(HERE/'CertificateKernel.lean')],capture_output=True,text=True,cwd=str(HERE))
        (out/'LEAN_KERNEL_CHECK.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,r.stdout+r.stderr
        dump(out/'LEAN_KERNEL_CHECK.json',{'passed':True,'returncode':r.returncode,'toolchain':'leanprover/lean4:v4.21.0','scope':'Rigid-tree inorder identities and conditional telescope only; original BST source model, parametric source proofs and global cost inequality are not fully formalized.','output':r.stdout})
    stage('installed_Lean_certificate_kernel',lean,(out/'LEAN_KERNEL_CHECK.json').exists())
    stage('independent_graph_source_feature_and_dual_verification',lambda:subprocess.run([sys.executable,'-B',str(HERE/'verify.py'),'--output',args.output],check=True,cwd=str(HERE)),(out/'INDEPENDENT_VERIFICATION.json').exists())
    stage('typed_registry_and_universal_acceptance_gate',lambda:finalize(out))
    dump(out/'PIPELINE_RUN.json',{'engine':'GSO bounded version1','stages':stages,'driver_cpu_seconds':time.process_time()-start,'reproduction':'Cached stages are rechecked by the independent verifier; a new output directory executes them afresh. A sealed artifact is read-only.'})
    print(json.dumps({'engine':'WORKING_VERSION_1','root':load(out/'ENGINE_RESULT.json')['source_uniform_root'],'stages':len(stages)}),flush=True)


def status_run(args):
    out=HERE/args.output
    print(json.dumps(load(out/'ENGINE_RESULT.json'),indent=2))


def verify_run(args):
    subprocess.run([sys.executable,'-B',str(HERE/'verify.py'),'--output',args.output,'--no-write'],check=True,cwd=str(HERE))


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    build=sub.add_parser('build');build.add_argument('--min-support',type=int,default=1);build.add_argument('--max-support',type=int,default=6);build.add_argument('--output',default='run_001');build.set_defaults(func=build_run)
    attack=sub.add_parser('attack');attack.add_argument('--output',default='run_001');attack.set_defaults(func=attack_run)
    research=sub.add_parser('research');research.add_argument('--output',default='run_001');research.set_defaults(func=research_run)
    status=sub.add_parser('status');status.add_argument('--output',default='run_001');status.set_defaults(func=status_run)
    verify=sub.add_parser('verify');verify.add_argument('--output',default='run_001');verify.set_defaults(func=verify_run)
    args=parser.parse_args()
    if args.command=='build':assert 1<=args.min_support<=args.max_support<=6
    args.func(args)


if __name__=='__main__':main()

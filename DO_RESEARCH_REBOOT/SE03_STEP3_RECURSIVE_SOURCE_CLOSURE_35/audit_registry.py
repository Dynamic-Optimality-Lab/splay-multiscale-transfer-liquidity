"""Independent dependency/scope audit. This does not prove ROOT35."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    z=read(F/'proof_boxes.json');nodes={b['id']:b for b in z['boxes']};assert len(nodes)==len(z['boxes']) and z['root']=='ROOT35'
    allowed={'PROVED','REFUTED','ACTIVE','BLOCKED','SUPERSEDED BY PROVED STRONGER LEMMA'}
    fields={'id','parent','target','source_scope','hypotheses','inherited_results','required_children','dual_falsification_objective','reduction_justification','status','verification_status','parent_bridge','artifact','edge_type'}
    edges={i:set() for i in nodes}
    for i,b in nodes.items():
        assert fields<=set(b) and b['status'] in allowed and (F/b['artifact']).is_file()
        edges[i].update(b['required_children']);edges[i].update(j for j in b['inherited_results'] if j in nodes)
        if b['status']=='PROVED':assert all(nodes[j]['status']=='PROVED' for j in b['required_children'])
    visiting=set();done=set()
    def visit(i):
        assert i not in visiting
        if i in done:return
        visiting.add(i)
        for j in edges[i]:visit(j)
        visiting.remove(i);done.add(i)
    for i in nodes:visit(i)
    for route in z['proof_routes']['ROOT35']:
        assert not all((j=='INHERITED_EXTERIOR' or nodes[j]['status']=='PROVED') for j in route)
    assert nodes['ROOT35']['status']==nodes['U35']['status']=='BLOCKED' and z['not_A_or_E'] and z['not_terminal_A_L']
    assert nodes['MODEL35']['source_scope'].startswith('abstract') and nodes['REAL35']['edge_type']=='dual-candidate-route'
    for i in (2,3,5,6,7,8):assert nodes[f'OWNER-{i}']['hypotheses'] and 'GIVEN' in nodes[f'OWNER-{i}']['source_scope']
    assert not (F/'FULL_PROOF.md').exists()
    for name in ('independent_recursive_lemma_audit.json','independent_source_and_recursion_audit.json'):
        for p,h in read(F/name)['input_sha256'].items():assert sha(Path(p) if Path(p).is_absolute() else F/p)==h
    assert sha(B/'run_phase_1440.py')==read(F/'entry.json')['controller_sha256']
    for ph in ('proof170','proof171','proof172','core43','verify84','verify85'):assert read(B/f'run_{ph}_result.json')['status']=='PASS'
    result=dict(status='PASS_DEPENDENCY_DAG_AND_SCOPE_AUDIT_NOT_ROOT_PROOF',input_sha256={n:sha(F/n) for n in ('proof_boxes.json','proof_debt.json','C35_ROOT_RECONSTRUCTION.md','C35_TERMINAL_VERDICT.md')},closed_boxes=[i for i,b in nodes.items() if b['status']=='PROVED'],unresolved_boxes=[i for i,b in nodes.items() if b['status']!='PROVED'],proof_dependency_graph_acyclic=True,no_required_active_child_hidden=True,conditional_owner_hypotheses_preserved=True,source_root_verdict='UNRESOLVED_MATHEMATICAL_BLOCKER',source_law_proved=False,source_countercut_proved=False,source_queries=0,source_engine_calls=0,trust='same-agent separate implementation audit; not external peer review or formal proof-assistant verification')
    with (F/'independent_registry_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify86_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)

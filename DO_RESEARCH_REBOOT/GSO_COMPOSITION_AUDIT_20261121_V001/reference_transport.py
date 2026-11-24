"""Exact original A rotations as a root-BST reference for genuine B requests."""
import json
from collections import defaultdict
import composition as M
K=M.K


def compile_reference(saved):
    source=saved['source'];rep=K.OLD.replay(source);genuine=[r['op'] for r in saved['rows'] if r['mode']=='K' and r['full_before']['B']['root']!=r['target']]
    if not genuine:
        assert rep['Q_B']==0
        return {'source':source['name'],'Q_B':0,'K_B':0,'reference_required':False,'trivial_no_B_rotation_case':True}
    last=genuine[-1];initial=saved['rows'][last-1]['full_after'];keys=sorted(rep['keys'])
    A=K.OLD.Tree(initial['A'],keys);B=K.OLD.Tree(initial['B'],keys);units=defaultdict(list)
    for unit in rep['units']:units[unit['id'][1]].append(unit)
    all_ids=[];bundles=[];R_A=R_B=0;previous=last;period=len(source['operations'])
    for op in genuine:
        ids=list(range(previous+1,op+1)) if previous<op else list(range(previous+1,period+1))+list(range(1,op+1))
        bits=[]
        for access in ids:
            for unit in units[access]:
                for bit,event in enumerate(unit['bits']):
                    identifier=['A',access,unit['id'][2],bit];assert A.parent[event['p']]==event['g'];A.rotate(event['p']);R_A+=1
                    bits.append({'original_id':identifier,'promoted':event['p'],'demoted':event['g']});all_ids.append(tuple(identifier))
        target=source['operations'][op-1][1];assert A.root==target and A.state()==saved['rows'][op-1]['full_after']['A']
        rb=K.OLD.plain(B,target);R_B+=rb;assert B.state()==saved['rows'][op-1]['full_after']['B']
        bundles.append({'genuine_original_KEEP':op,'target':target,'original_A_access_ids':ids,'actual_original_A_rotations':bits,'reference_request_cost':1+len(bits),'B_real_rotations':rb})
        previous=op
    assert len(all_ids)==len(set(all_ids))==sum(len(unit['bits']) for unit in rep['units'])
    assert A.state()==initial['A'] and B.state()==initial['B']
    K_B=len(genuine);reference=R_A+K_B;b_cost=R_B+K_B
    assert K_B<=rep['A'] and R_A<=2*rep['A'] and reference<=3*rep['A'] and 2*rep['Q_B']<=b_cost
    return {'source':source['name'],'source_A':rep['A'],'Q_B':rep['Q_B'],'physical_keys':keys,'K_B':K_B,'R_A':R_A,'R_B':R_B,'reference_cost':reference,'B_root_BST_cost':b_cost,'reference_initial_A':initial['A'],'B_initial':initial['B'],'bundles':bundles,'all_real_A_bits_used_exactly_once':True,'reference_and_B_full_closure':True,'startup_prefix_credit':0,'source_prefix_separately_verified':True,'root_model_note':'Each actual reference request ends at its root. Helpers are reproduced as real rotations between requests, not additional charged searches or virtual bits.'}


def main():
    out=M.HERE/'reference';out.mkdir(exist_ok=False);summary=[]
    for path in sorted(M.HERE.glob('source_*.json.gz')):
        z=compile_reference(K.load(path));M.write('reference/'+path.name,z)
        summary.append({k:z[k] for k in ('source','source_A','Q_B','K_B','R_A','R_B','reference_cost','B_root_BST_cost') if k in z})
    M.write('PERIODIC_TRANSFER_CERTIFICATE.json',{'status':'PROVED_GENERIC_PERIODIC_ROOT_BST_TRANSFER_USING_CITED_EXTERNAL_THEOREM_FOR_ITS_FACTOR','generic_hypothesis':'Splay cost <= f(n)*OPT + g(n), arbitrary initial splay tree, optimal initial reference tree, finite g(n).','root_BST_costs':'Reference uses exactly R_A+K_B per period; original B cost is R_B+K_B after omitting root repeats.','repetition':'For every integer t>=1, t*(R_B+K_B) <= f(n)*t*(R_A+K_B)+g(n). Divide by t and let t grow at fixed n.','conclusion':'Q_B <= f(n)*(R_A+K_B)/2 <= (3/2)*f(n)*A','external_primary':{'url':'https://arxiv.org/html/2607.18498v1#S5','version':'v1, submitted20July2026','input':'Theorem1, with f(n)=O(log log n * log^2 log log n) and g(n)=O(n f(n)).','status':'Primary external theorem used, not independently reproved by this audit.'},'all_source_corollary':'Q_B(W) = O(log log n * log^2 log log n)*A(W), with small n absorbed in the absolute constant.','limitation':'The factor depends on physical support n and is unbounded. This is not the requested universal finite constant; cyclic repetition does not remove a multiplicative support factor.','finite_reference_audits':summary,'unrestricted_constant_root':'OPEN'})
    print(json.dumps({'reference_sources':len(summary),'real_A_bits':sum(x.get('R_A',0) for x in summary),'reference_cost':sum(x.get('reference_cost',0) for x in summary),'root_status':'OPEN','factor':'Support-dependent; external theorem not independently reproved.'}))


if __name__=='__main__':main()

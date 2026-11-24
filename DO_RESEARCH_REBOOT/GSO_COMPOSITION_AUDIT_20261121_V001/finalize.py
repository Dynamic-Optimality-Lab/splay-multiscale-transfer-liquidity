"""Bind checked original composition evidence and its explicit open frontier."""
import hashlib
import json
from pathlib import Path
import composition as M
import gso
K=M.K;HERE=M.HERE;ROOT=HERE.parent.parent


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    proof=K.load(HERE/'NOTION_PROOF_REFERENCE.json');assert proof['readback_verified'] and all(x['verified'] for x in proof['workspace_updates'])
    pins={x['path']:x for x in K.load(M.PREVIOUS/'PINNED_SOURCE_INPUTS.json')}
    extra=['GSO_CONTEXT_LIFECYCLE_20261121_V001/FINAL_MANIFEST.json','GSO_CONTEXT_LIFECYCLE_20261121_V001/context.py','GSO_CONTEXT_LIFECYCLE_20261121_V001/source_audit.py','GSO_CONTEXT_LIFECYCLE_20261121_V001/verify.py','CD_UNIFORM01/SUPPORT_ERASURE_CLOSURE.md','CD_UNIFORM01/MARK_SUBSET_LIFT.md','RESEARCH_RULES.md']
    for name in extra:
        path='DO_RESEARCH_REBOOT/'+name;pins[path]={'path':path,'sha256':digest(ROOT/path)}
    K.dump(HERE/'PINNED_SOURCE_INPUTS.json',list(pins.values()))
    code=[p for p in HERE.iterdir() if p.suffix in ('.py','.lean')];proof['code_sha256']={p.name:digest(p) for p in sorted(code)};K.dump(HERE/'NOTION_PROOF_REFERENCE.json',proof)
    result=gso.status();result['notion']=proof['url'];result['prior_artifacts_preserved']=4926;K.dump(HERE/'ENGINE_RESULT.json',result)
    claims=[
      {'claim':'The proposed composition algebra, with explicit local potential boundary term','status':'PROVED_FROM_EXPLICIT_PREMISES','scaled_constant':'3L+2D+B_scaled for 2Q_B<=scaled_constant*A, where B_scaled bounds carry=2*sum(Phi_start-Phi_end). If the unscaled boundary sum is <=B0*A, the original coefficient is 3L/2+D+B0.'},
      {'claim':'Temporal cutting of licensed finite-potential histories','status':'PROVED_UNIVERSAL_WITHIN_THE_CERTIFICATE_DOMAIN','scope':'Retain endpoints; independent closed pieces not required.'},
      {'claim':'Raw internal original A StepEv attribution to disjoint blocks has load1','status':'PROVED_ALL_ORIGINAL_SOURCES','warning':'Not a proof that an unconstructed legal local history costs this much.'},
      {'claim':'Interval projection produces ordinary local Pair Access histories','status':'REFUTED_EXACT','source':'source_02.json.gz','stronger':'Projected B endpoint is outside its full ordinary-splay reachable set, even with unlimited A work.'},
      {'claim':'Zero attributed original A work is enough for each projected local transition','status':'REFUTED_EXACT','source':'source_01.json.gz'},
      {'claim':'Identifying rank-block vertices yields a smaller BST quotient','status':'REFUTED_EXACT','source':'source_01.json.gz','witness':'Original A path7,4,6 produces block cycle1,0,1.'},
      {'claim':'E<=Q_B<=E+2A for fixed blocks of size<=5','status':'PROVED_ALL_ORIGINAL_SOURCES','consequence':'Bounding this E is equivalent to the original target up to constants.'},
      {'claim':'E_t<=D a_t for every finite absolute D','status':'REFUTED_ALL_PARAMETER_LOCAL_LAW','source_family':'Complete H_3,q, q>=1. E_t=q+1, a_t=1.','warning':'The global aggregate E(W)<=D A(W) is not refuted.'},
      {'claim':'Original real-A root-BST reference cost R_A+K_B<=3A','status':'PROVED_ALL_ORIGINAL_SOURCES','model':'Exact cyclic genuine-B gaps, no virtual bits or prefix credit.'},
      {'claim':'Q_B=O(log log n * log^2 log log n) A','status':'PROVED_COROLLARY_USING_EXTERNAL_THEOREM','dependency':'https://arxiv.org/html/2607.18498v1#S5','warning':'External theorem not independently reproved; n factor is unbounded. Not relaxed Universal CD.'},
      {'claim':'General adaptive or overlapping paired-core composition and an absolute Universal CD constant','status':'OPEN','first_missing':'A physically valid noncommon interface, legally applicable local histories and global interaction/resource/boundary budgets.'}
    ]
    K.dump(HERE/'THEOREM_CERTIFICATE.json',{'proof':proof['url'],'claims':claims,'old_results_preserved':True,'new_unrestricted_original_constant_obligations_deleted':0,'finite_and_symbolic_scopes_distinguished':True})
    print(json.dumps({'claims':len(claims),'input_pins':len(pins),'code_bindings':len(code),'notion':proof['url'],'root_status':'OPEN'}))


if __name__=='__main__':main()

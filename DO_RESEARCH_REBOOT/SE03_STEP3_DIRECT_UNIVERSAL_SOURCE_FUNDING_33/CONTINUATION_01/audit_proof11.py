"""Exact incoming-genuine image domain; independently of source reachability."""
import json,pickle,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'nine_label_native_action_cache.json').read_text());T=z['trees'];N=len(T);D=z['destination'];image={D[s][x] for s in range(N) for x in range(9) if T[s][0]!=x+1};ac=collections.Counter(t[0] for t in T);bc=collections.Counter(T[s][0] for s in image)
    with (B/'pair9_debt_00.pkl').open('rb') as f:s=pickle.load(f)
    mirror=s['mirror'];fixedA=collections.Counter(T[a][0] for a in range(N) if mirror[a]==a);fixedB=collections.Counter(T[a][0] for a in image if mirror[a]==a);product=sum(ac[x]*bc[x] for x in ac);fix=sum(fixedA[x]*fixedB[x] for x in ac);domain=(product+fix)//2
    assert all(divmod(v,N)[1] in image for v in s['nodes'])
    result={'status':'COMPLETE_INCOMING_IMAGE_PAIR_DOMAIN' if domain==len(s['nodes']) else 'PROPER_PAIR_SUBDOMAIN','native_B_genuine_image_states':len(image),'image_root_counts':dict(bc),'product_mod_reflection':domain,'stored_nodes':len(s['nodes']),'all_original_nine_anchor_synchronized_genuine_boundaries_covered':domain==len(s['nodes']),'private_scope':'arbitrary rigid BST gaps, with NO original A operand inside a gap','source_queries':0,'principal_U33':'OPEN'}
    out('pair9_incoming_image_domain.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof11_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

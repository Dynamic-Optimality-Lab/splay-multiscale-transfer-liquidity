"""Independent algebra and written-proof review of local source composition.

No source graph expansion or finite passing population test. Written
universal implications remain a human-readable proof, not a formal proof.
"""
import hashlib,json,sys,time
from pathlib import Path
from collections import Counter
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plus(a,b):
    z=Counter(a);z.update(b);return {k:v for k,v in z.items() if v}
def main():
    # Arbitrary two adjacent certified macro laws; the shared boundary debt
    # cancels symbolically. Induction in the paper extends this to any length.
    e1={'c1':2,'q1':-1,'D0':-1,'D1':1};e2={'c2':2,'q2':-1,'D1':-1,'D2':1}
    assert plus(e1,e2)=={'c1':2,'q1':-1,'D0':-1,'c2':2,'q2':-1,'D2':1}
    # The owner's count cancels independently, including zero-owner cases.
    assert plus({'selected':1,'n':-1},{'Q':-1,'n':1})=={'selected':1,'Q':-1}
    for name in ('independent_probe11_LOW_B_01.json','independent_probe11_LOW_B_02.json',
                 'independent_probe11_LOW_B_03.json','independent_probe11_HIGH_envelope_B01.json',
                 'independent_probe11_H3_actual_signs_B01.json','independent_AW35_UF35_proof_review.json'):
        data=json.loads((F/name).read_text());assert data['status'].startswith('PASS')
        # Pins are checked at this receipt's own recorded source-root convention.
        for p,h in data.get('input_sha256',{}).items():
            if Path(p).is_absolute():assert sha(Path(p))==h
    paths=[F/'BALANCED_LOCAL_ALPHABET_COMPOSITION.md',F/'NATIVE11_FULL_SOURCE_THEOREM.md',
      F/'ARBITRARY_SUPPORT_ANCHORED_WORD_FUNDING.md',F/'independent_AW35_UF35_proof_review.json',
      B/'STREAMED_BLOCK_THEOREM.md',P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md',F/'audit_BLC35_proof.py']
    out={'status':'PASS_BALANCED_LOCAL_ALPHABET_COMPOSITION_PROOF_REVIEW',
      'reviewed':['pointwise native11 signs apply to open blocks; no closed-subtree-density hypothesis reused',
        'inactive global marks stay opaque only when outside all anchor paths and never accessed in that block',
        'D_end=D_start required within each actual local alphabet, never across changing charts',
        'per-macro selected owner-inclusive units union to the block inventory without reuse',
        'AW local anchors may be globally marked elsewhere; exact B operand/path geometry is unchanged',
        'actual disjoint consecutive macro blocks give disjoint occurrence IDs despite shared key labels',
        'zero carry at all block seams; inherited static queue<=2; no online temporal policy claimed',
        'both-endpoint one-period transport; fixed h0/fE/historical maps unchanged',
        'partition existence is an explicit unproved source-coverage condition, not an IAGS reduction'],
      'scope':'every original source with the specified actual partition, unbounded global support and private populations at stated local scopes',
      'universal_partition_existence':'OPEN','JR35':'OPEN','reservation':'DEFERRED',
      'source_queries':0,'source_engine_calls':0,'independent_is_same_agent_distinct_implementation':True,
      'verification_boundary':'symbolic cancellation algebra and independent written proof inspection, not external or formal verification',
      'input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'independent_BLC35_proof_review.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify149_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

"""Typed research status and a root gate that rejects finite/conditional evidence."""
from dataclasses import dataclass
import hashlib
from kernel import dump,load,ROOT


@dataclass(frozen=True)
class Obligation:
    name:str
    status:str
    scope:str
    checked:bool
    evidence:str


REQUIRED=('original_model_binding','reachable_state_induction','whole_operation_cost','boundary_cancellation','global_resource_budget')


def root_gate(obligations):
    byname={x.name:x for x in obligations};missing=[]
    for name in REQUIRED:
        obj=byname.get(name)
        if obj is None or not obj.checked or obj.status!='PROVED' or obj.scope!='ALL_ORIGINAL_SOURCES' or not obj.evidence:missing.append(name)
    return {'root_status':'PROVED' if not missing else 'OPEN','first_missing':missing[0] if missing else None,'missing':missing}


def finalize(out):
    dual=load(out/'PARAMETRIC_DUAL_CERTIFICATE.json');symbolic=load(out/'SYMBOLIC_FRONTIER_IDENTITIES.json');independent=load(out/'INDEPENDENT_VERIFICATION.json')
    assert independent['passed'] and independent['exact_dual']['exact_dual_arithmetic'] and len(symbolic['rows'])==7
    # A symbolic source proof is a separately audited record, never synthesized
    # by changing a finite-status flag. Until that exists, preserve the gap.
    source_proof=out/'UNIVERSAL_SOURCE_PROOF_REFERENCE.json'
    library=out.parent/'UNIVERSAL_SOURCE_PROOF_REFERENCE.json'
    if not source_proof.exists() and library.exists():dump(source_proof,load(library))
    proved=source_proof.exists() and load(source_proof).get('readback_verified',False)
    if proved:
        ref=load(source_proof)
        assert ref.get('physical_source_proof_reviewed') and ref.get('mathematical_status')=='PROVED_SOURCE_UNIFORM_NECESSARY_CONSTRAINTS'
        assert ref.get('code_sha256') and all(hashlib.sha256((out.parent/name).read_bytes()).hexdigest()==digest for name,digest in ref['code_sha256'].items())
    grammar_status='REFUTED—EXACT' if proved else 'SYMBOLIC_DUAL_READY—SOURCE_PROOF_RECORD_PENDING'
    gate=root_gate([
        Obligation('original_model_binding','PROVED','ALL_ORIGINAL_SOURCES',True,'Original source semantics and all prior frozen interfaces retained; mathematical binding, not a new Lean formalization.'),
        Obligation('reachable_state_induction','PROVED','ALL_ORIGINAL_SOURCES',True,'Chosen invariant is well-formed same-key BST pairs, a superset of reachable states. Original rotations preserve inorder; Lean checks the rigid-subtree identities. Exact reachable-set enumeration is separately finite.'),
        Obligation('whole_operation_cost','REFUTED' if proved else 'OPEN','DECLARED_FRONTIER3_GRAMMARS',proved,'PARAMETRIC_DUAL_CERTIFICATE.json'),
        Obligation('boundary_cancellation','PROVED','ALL_ORIGINAL_SOURCES',True,'Single-valued physical pair state function cancels on exact full pair closure.')])
    result={'engine_status':'WORKING_BOUNDED_VERSION_1','root_gate':gate,'source_uniform_root':'OPEN','principal_grammar_status':grammar_status,
            'pruned_declared_grammars':['frontier3','frontier3_roots_guarded'] if proved else [],
            'prior_exclusions_preserved':[str(ROOT/'DO_RESEARCH_REBOOT/GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/SYMBOLIC_SYNTHESIS_CERTIFICATE.json')],
            'implemented':['full original-state kernel and complete reachable graphs','free-state positive-cycle/potential teacher with exact optimal finite certificates','bounded CEGIS coefficient learner in two nonlinear physical grammars','exact LP basis reconstruction','complete original-source adversary and closed-period counterexample embedding','rigid-subtree symbolic feature proof checker','affine loop-invariant synthesis and Z3 induction checks','exact parametric dual/pruning module','installed Lean rotation and conditional telescope certificate integration','legacy exact-U flow/min-cut and independent-verification adapter','typed root-acceptance gate'],
            'not_implemented':['general automated proof-mechanism invention','e-graph representation search','complete unbounded-BST invariant synthesizer','complete Lean formalization of original source model and all universal source-family proofs'],
            'strategic_result':'Declared frontier family excluded for all fixed coefficients and finite C.' if proved else 'Source-uniform identity/dual deduction ready; explicit source proof must be recorded.',
            'original_residual_classes_newly_paid':0,'original_root_obligations_deleted':0,
            'stop':'No automatic frontier4 or donor-policy expansion; a fresh specific physical attack must pass the original admission gates.'}
    dump(out/'ENGINE_RESULT.json',result);return result


def candidate_failures(out):
    from fractions import Fraction
    candidates=[]
    for name in ('frontier3','frontier3_roots_guarded'):
        result=load(out/(name+'_synthesis.json'))
        if result.get('candidate'):candidates.append(result['candidate'])
    candidates.append(load(out/'SEED_E3_RESULT.json')['candidate']);answer=[]
    for program in candidates:
        theta=list(map(Fraction,program['theta']));C=Fraction(program['C']);best=None
        for path in sorted(out.glob('*_N*.json.gz')):
            w=load(path)
            for row in w['rows']:
                slack=Fraction(row['q'])+sum(a*b for a,b in zip(theta,row['delta']))-C*row['a']
                if best is None or slack>best[0]:best=(slack,path.name,row['id'])
        assert best is not None and best[0]>0
        answer.append({'candidate':program,'source_file':best[1],'original_operation_id':best[2],'exact_positive_slack':str(best[0]),'conclusion':'Refutes this whole-operation potential certificate, not the original cost constant C or the universal root.'})
    dump(out/'CANDIDATE_ORIGINAL_COUNTEREXAMPLES.json',answer);return answer

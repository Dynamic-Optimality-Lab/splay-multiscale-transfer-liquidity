"""Capped proof/dependency assembly; no source engine or search."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    # Verify historical immutable artifacts, not historical moving pointer files.
    old=read(C/'CONTINUATION_01/campaign_manifest.json')
    for n,h in old['artifacts'].items():assert sha(C/'CONTINUATION_01'/n)==h
    oldpins=read(C/'dependency_manifest.json')['inherited']
    pins=[]
    for row in oldpins:
        p=Path(row['path']);assert sha(p)==row['sha256'];pins.append(row)
    sources=[('C14_SOURCE','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/SOURCE_SPEC.md','INHERITED_SOURCE_DOMAIN'),
      ('C14_SEAL','SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json','INHERITED_ACCEPTED_CD6'),
      ('STATIC_BLOCK','SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01/SOURCE_AUGMENTATION_02/SOURCE_SOLVENT_BLOCK_AUGMENTATION.md','INHERITED_CONDITIONAL_STATIC_BLOCK'),
      ('OLD_SI34','SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_01/SI34_SOURCE_REFUTATION.md','REFUTED_SI34_IMMUTABLE'),
      ('OLD_B','SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_01/SYMBOLIC_B_CLOSURE.md','INHERITED_SYMBOLIC_SOURCE_CLOSURE'),
      ('C34_MODEL','SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34/EXACT_GLOBAL_FEASIBILITY_MODEL.md','INHERITED_ORIGINAL_WITNESS_CONTRACT'),
      ('C34_INPUT','SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34/GATE_U14_EXACT_CONTRACT.md','INHERITED_CONDITIONAL_PARENT'),
      ('C33_LIMIT','SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01/SOURCE_JOINT_REPAIR_03/RESULTS_AND_LIMITS.md','RESTRICTED_PROVED_UNIVERSAL_OPEN')]
    for id,n,status in sources:
        p=P/n;pins.append(dict(id=id,path=str(p),sha256=sha(p),status=status,inspected=True))
    put('dependency_manifest.json',{'inherited':pins,'historical_manifest_sha256':sha(C/'CONTINUATION_01/campaign_manifest.json'),
        'new_directive':{'path':'C:/Users/Saif malik/.codex/attachments/4b30b9a6-d8e3-4950-9675-7cf9cfc26fea/Pasted text.txt',
          'sha256':sha(Path('C:/Users/Saif malik/.codex/attachments/4b30b9a6-d8e3-4950-9675-7cf9cfc26fea/Pasted text.txt'))},
        'controller_sha256':sha(B/'run_phase_1440.py')})
    audit=read(F/'independent_symbolic_audit.json')
    for n,h in audit['input_sha256'].items():assert sha(F/n)==h
    def box(id,target,conditions,status,children,bridge,measure,falsification,artifact):
        return dict(id=id,target=target,conditions=conditions,status=status,required_children=children,
          inheritance=['original C14 source/bank/transport','C15 finite owner exchange','immutable SI34 refutation'],
          unresolved_ambiguities=[] if status.startswith('PROVED') or status.startswith('INHERITED') else [target],
          upward_bridge=bridge,reduction_measure=measure,exact_falsification_target=falsification,artifact=artifact)
    boxes=[
      box('UCF35','complete original source-licensed frozen-owner extension for every legitimate r>=7 tuple',
        'original (W,I,fE,a0,Gamma), no broadened owner domain','OPEN_MATHEMATICAL_BLOCKER',['SRC35','COMPAT35','OWNER35'],
        'source comparison plus compatible original E_r3 predicates permits owner exchange and transport',
        'exhaustive witness-factor split, not a length descent','genuine tuple rejecting every original license footprint','UCF35_ROOT_THEOREM.md'),
      box('SRC35','independent full h containing h0 with Type A/B source proof and Bank25 for every source',
        'original source domain, independent of fE/CD(r)','OPEN',['SC35','SIMPLE35'],
        'SC35 reduces all nonsimple closed words to smaller complete closed source comparisons',
        'strict macro-count descent at every proper repeated-state split','source rejecting all independent original licenses','ARBITRARY_SUPPORT_SOURCE_PROOF.md'),
      box('SC35','complete state-cycle decomposition and exact source comparison reconstruction',
        'full labelled A/B states at natural boundaries; leaf receipts on actual leaf, not extra copies',
        'PROVED_DERIVATION',['BASE35'],
        'leaf inventories partition original macros; lift both endpoints and coarsen licensed static block',
        'each child macro count strictly below parent at a proper split; source-simple leaves explicit',
        'cost, genuine boundary, actual ID or h0 failure in a valid complete-state excision','SIMPLE_CYCLE_SOURCE_REDUCTION.md'),
      box('BASE35','closed-source comparisons at support<=6',
        'exact inherited source/owner scopes','INHERITED_PROVED',[],
        'funds low-support leaves; no silent stronger I(5) claim','terminal existing certificate',
        'concrete invalid inherited dependency only','EXACT_GATE_U14_PARENT_CONTRACT.md'),
      box('SIMPLE35','credit license for every source-simple support>=7 closed word',
        'arbitrary actual private trees, helpers, both orientations, length','OPEN',['AF35','OTHER_SIMPLE35'],
        'AF intersection and its complement form exhaustive case split; AF alone does not prove the complement',
        'exhaustive subclass split, not an alleged strict descent','complete original source/license countercertificate','ACTIVE_PROOF_BOX.md'),
      box('AF35','complete source comparison and working2 on the anchored family for all r>=4',
        'exact AF geometry, no arbitrary-source extension','PROVED_DERIVATION',['RC35','DS35'],
        'reset own capacity and disjoint actual anchor spares cover every demand class',
        'descending source induction / disjoint block inventories','AF endpoint, cost, donor collision or source-license failure','ANCHORED_FAMILY_COMPLETE_FUNDING.md'),
      box('RC35','H>=ceil(number of missing target clusters /2)',
        'same physical key set, ordinary rotations','PROVED_DERIVATION',[],
        'r missing reset clusters finance Q=r-1 macro','first cluster births along actual rotations',
        'one rotation creating two distinct new target clusters','RESET_CLUSTER_LOWER_BOUND.md'),
      box('DS35','descending maxima with intervening minimum yield right vine',
        'all projected keys accounted for; only rigid off-path operands removed','PROVED_DERIVATION',[],
        'full A reverse endpoint is T in AF','number of unprocessed maximum ranks',
        'valid descending sweep breaking the high-vine invariant','DESCENDING_SWEEP_RETURN.md'),
      box('OTHER_SIMPLE35','source credit on source-simple support>=7 histories outside covered source families',
        'no solvency, private-capacity, return-loop or future-depth assumption','OPEN',[],
        'with covered source classes proves SIMPLE35','no valid further closed-source descent presently established',
        'source with all original license alternatives infeasible','CLUSTER_COVER_ATTEMPT.md'),
      box('COMPAT35','some complete comparison satisfies each legitimate original Gamma/owner/chart/period input',
        'C(W,I) nonempty; compatibility means original reservations and retirement, not raw injectivity','OPEN',[],
        'pointwise compatible choice plus SRC35 suffices for UCF35',
        'separate existential compatibility child; no false finite enumeration',
        'legitimate input excluding every complete compatible comparison','SOURCE_DOMAIN_AND_OWNER_INPUTS.md'),
      box('OWNER35','complete compatible h has distinct free inverse-a0 terminals preserving all old owners',
        'finite actual IDs and original path permissions','INHERITED_PROVED',[],
        'finishes physical extension; cannot supply missing source h','finite path / unique incoming edge',
        'entered cycle, merged root paths or reserved endpoint under valid compatibility','GLOBAL_FULL_H_AND_FROZEN_EXCHANGE.md'),
      box('FD35','all-original-license rejecting-state-cut dual',
        'admissible semantic license footprints; no completeness assumed for a finite guessed list','PROVED_LOGICAL_CHARACTERIZATION',[],
        'states the complete root falsification burden, does not establish infeasibility',
        'finite fixed-footprint reachability; license membership remains explicit',
        'failure of the exact original-path encoding','COMPLETE_FEASIBILITY_DUAL_THEOREM.md')]
    ids={b['id'] for b in boxes};assert len(ids)==len(boxes)
    for b in boxes:assert set(b['required_children'])<=ids
    graph={b['id']:b['required_children'] for b in boxes}
    def dfs(v,active,done):
        assert v not in active
        if v in done:return
        for c in graph[v]:dfs(c,active|{v},done)
        done.add(v)
    done=set()
    for b in boxes:dfs(b['id'],set(),done)
    put('proof_boxes_v3.json',{'version':3,'root':'UCF35','root_status':'OPEN_MATHEMATICAL_BLOCKER',
      'prior_root_SI34':'REFUTED_IMMUTABLE','boxes':boxes,'all_original_license_countercut':False,
      'A_UCF35':False,'E_UCF35':False,'global_Gate_U':'OPEN',
      'new_source_queries':0,'new_actual_source_replay':False,
      'verification_scope':'AF free-term/endpoint receipt; SC mathematical derivation with pending integration audit'})
    print('SOURCE_CYCLE_REDUCTION_AND_EXACT_UNCLOSED_PARENT_REGISTRY',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof176_exit.json').open('x',encoding='utf-8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

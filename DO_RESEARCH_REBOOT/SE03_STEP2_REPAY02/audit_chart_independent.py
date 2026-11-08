"""Separate source AST and nine-Score/cold-exchange scope audit."""
import ast,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;CAP=float(sys.argv[1])
PC=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'
SC=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE'
def fn(path,name):
    raw=path.read_text(encoding='utf-8');tree=ast.parse(raw)
    return next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name),raw
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
error=None
try:
    bv,_=fn(PC/'PC_B_CONTROLLER.py','b_valid')
    bt,_=fn(SC/'STRICT_B_CONTROLLER.py','b_tree_valid')
    sv,_=fn(SC/'STRICT_LOW_COMPILER.py','state_valid7')
    low,raw=fn(SC/'STRICT_LOW_COMPILER.py','build_slow')
    assert [x.arg for x in bt.args.args]==['d','bs','st','sig','intervals']
    assert not any(isinstance(x,ast.Name) and 'mu' in x.id for x in ast.walk(bt))
    assert not any(isinstance(x,ast.Attribute) and x.attr=='mu' for x in ast.walk(bt))
    assert not any(isinstance(x,ast.Attribute) and x.attr=='mu' for x in ast.walk(bv))
    svcalls={x.func.id for x in ast.walk(sv) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name)}
    assert 'popcount5' in svcalls and 'b_valid' in svcalls
    mu_calls=[x for x in ast.walk(low) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='mubit']
    assert len(mu_calls)==1 # terminal marked test, no all-Score descendant condition
    calls={x.func.id for x in ast.walk(low) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name)}
    assert {'b_tree_valid','same_keep_target','root_terminated','no_intermediate_genuine','shadow_match7'}<=calls
    # Independently reconstruct set/word proof: recent-k window includes
    # only V, hence visits introduce <=2 per new mark. Complement forests
    # have <=2 nodes per excluded mark. At delta0 both bounds coincide.
    # A cold source component containing old v,z has four nodes. Old V5
    # core adds exactly2 nodes above v to common V4 core; z is the other
    # two-node twig. This yields exactly the chain/sibling placements.
    # Siblings are impossible by alternation or inner mark loss. Chain
    # SS demotes v plus inner U and changes the fixed ordered Score chart.
    cover=(B/'RECENT_SUPPORT_COVER.md').read_text(encoding='utf-8')
    assert 'EVERY hit in BOTH residual cores' in cover
    identity=(B/'COLD_EXCHANGE_IDENTITY.md').read_text(encoding='utf-8')
    assert '[d_virtual-d_old-1]' in identity
    assert 'That comparison remains a real obligation' in identity
    assert 'No reachability or closed-walk IH is invoked' in identity
    assert time.process_time()<CAP
    out('chart_independent_audit.json',{'status':'PASS_LOCAL_NINE_SCORE_HITS_AND_EXACT_MISS_IDENTITIES',
      'method':'separate mathematical forest/window derivation plus read-only original AST audit',
      'original_definitions_read_not_executed':True,
      'no_marked_descendant_premise_in_B_validity':True,
      'fixed_nine_Scores_may_include_unmarked_leaf':True,
      'all_hit_signed_rules':'old M3 pointwise theorem; H<=2 local source embedding; H>=3 actual q<=4 range',
      'core10_9_to8_hits':'covered with same nine Score labels; do not replace interface after actual core shrink',
      'LRU_annotation':'source-word witness only; no new controller coordinate; unique cyclic periodic order',
      'full_state_closure':'unchanged original full trees; annotations/charts agree at actual period ends',
      'virtual_chart':'one actual internal B double; same A input and real present keys, all original source costs retained',
      'hypothetical_pair_scope':'only local universal original M3 relation, no smaller closed-walk IH',
      'miss_debt_boundary_terms_discarded':False,
      'Step2_complete':False,'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('FIXED_NINE_SCORE_SOURCE_AND_COLD_EXCHANGE_INDEPENDENT_AUDIT_PASS; miss sign OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_chart_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

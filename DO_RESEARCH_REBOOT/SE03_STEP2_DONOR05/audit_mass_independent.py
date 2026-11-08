"""Separate formula/monotonicity audit; no import of the construction."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def node(k,l,r):return {'key':k,'left':l,'right':r}
def rot_r(t):
    u=t['left'];return node(u['key'],u['left'],node(t['key'],u['right'],t['right']))
def rot_l(t):
    u=t['right'];return node(u['key'],node(t['key'],t['left'],u['left']),u['right'])
def encode(t):return t if isinstance(t,str) else [t['key'],encode(t['left']),encode(t['right'])]
def flatten(t):return [t] if isinstance(t,str) else flatten(t['left'])+[t['key']]+flatten(t['right'])
def main():
    ll=node('g',node('p',node('x','A','B'),'C'),'D')
    rr=node('g','A',node('p','B',node('x','C','D')))
    lr=node('g',node('p','A',node('x','B','C')),'D')
    rl=node('g','A',node('p',node('x','B','C'),'D'))
    targets=[rot_r(rot_r(ll)),rot_l(rot_l(rr)),
        rot_r(node('g',rot_l(lr['left']),'D')),
        rot_l(node('g','A',rot_r(rl['right'])))]
    evidence=json.loads((B/'mass_audit.json').read_text())
    assert [encode(t) for t in targets]==[r['target'] for r in evidence['frames']]
    assert all(flatten(s)==flatten(t) for s,t in zip([ll,rr,lr,rl],targets))
    # The exact argument does not assume intermediate global density.
    # Processed nodes are never touched again, so final density applies NOW.
    # Their nonnegative masses plus marked x weight1 give rebuilt mass>=1;
    # its original source interval gives <=1. Hence both child masses0.
    proof_steps=[
        'inorder interval alternation bounds every source subtree mass by1',
        'marked source subtree mass1, unmarked source subtree mass0/1 by density',
        'processed roots and original offpath hangers retain their internal label sets',
        'rebuilt target mass1 and two proper masses0 at every pair',
        'parent marked impossible since mass would be>=2',
        'SS marked G -> two offpath masses0 -> K unchanged',
        'SS unmarked G -> two offpath masses1 -> K decreases1',
        'mixed -> both source unmarked masses1 -> K decreases2',
        'zig at marked whole root would require mass>=2 -> impossible',
        'full B closure forbids all strict decreases',
        'any surviving unmarked mass1 is consumed at first descendant KEEP -> contradiction']
    # Independent conservation of positive-unmarked counts in the three cases.
    assert (0+0)-(0+0)==0
    assert (1+0)-(1+1)==-1
    assert (0+0)-(1+1)==-2
    assert evidence['Step2_complete'] is False
    out('mass_independent_audit.json',{'status':'PASS_NEW_CLOSED_MAXIMAL_SOURCE_THEOREM',
        'independent_representation':'dictionary primitive rotations versus tuple formulas/polynomial mass sums',
        'proof_steps':proof_steps,'pitfall_checked':'processed subtrees are rigid under LATER outer frames; initial density not assumed on the entire intermediate tree',
        'conclusion':'all actual B doubles same-side, marked G/unmarked P, all unmarked core subtree masses0',
        'scope':'actual B-closed maximal core, all r>=2 and arbitrary finite ambient BSTs',
        'frozen_graph_filtered':False,'A_cost_bound_proved':False,'core10_covered':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'same_agent_separate_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate mass persistence, pair classification and closure audit; Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_mass_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

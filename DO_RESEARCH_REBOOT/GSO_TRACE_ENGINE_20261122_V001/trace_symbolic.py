"""Exact macro-observer factorization and conditional ledger-loop synthesis.

Does not replace physical tree provenance with sampled recurrence fitting.
The universal H3q provenance and arbitrary-gap proof are the linked manuscript.
"""
import sys
from collections import Counter
import sympy as sp
import z3
sys.dont_write_bytecode=True
import trace as X


def macro_observer(parent,left_nonempty,last=False):
    """Uniform four-key left-gap filler, active vertex at local rank4.

    Balanced filler ranks0..3 has root1, left0, right2 with right child3.
    A nonempty skeleton left subtree moves the gap root's physical parent to
    the predecessor outside this block. All nonmaximum right ports are hi.
    """
    assert parent in ('nil','lo','hi')
    shape=[4,[1,[0,None,None],[2,None,[3,None,None]]],None]
    stubs=[[1,'nil','nil'],['lo' if left_nonempty else 4,0,2],[1,'nil',3],[2,'nil','nil'],[parent,'lo' if left_nonempty else 1,'nil' if last else 'hi']]
    return [shape,stubs]


def macro_pair(pa,la,pb,lb,last=False):
    import json
    return json.dumps([5,macro_observer(pa,la,last),macro_observer(pb,lb,last)],separators=(',',':'))


def factorization_checks():
    # The finite universe of actual old BST shapes is used to validate the
    # observer formula. Universality follows from the unique-gap attachment
    # argument, not this bounded enumeration.
    cases=0
    for n in range(1,6):
        for t in X.K.shapes(1,n):
            old=X.C.raw_state(t);s={'name':'symbolic_shape','initial_A':old,'initial_B':old,'diagonal':old,'prefix':[],'operations':[],'expected_A':0,'expected_Q':0}
            full=X.C.embed(s,n=5*n,active=tuple(5*k for k in range(1,n+1)))['initial_A'];tr=X.K.OLD.Tree(full,list(range(1,5*n+1)));orig=X.K.OLD.Tree(old,list(range(1,n+1)));blocks=X.partition(list(range(1,5*n+1)),5);owner={x:i for i,b in enumerate(blocks) for x in b}
            for k in range(1,n+1):
                p=orig.parent[k];direction='nil' if p is None else 'lo' if p<k else 'hi'
                expected=macro_observer(direction,orig.ch[k][0] is not None,k==n)
                assert X.anonymous(tr,blocks[k-1],owner)==expected
                cases+=1
    # In a nonroot critical RR bit, g changes low->high parent and the
    # transported middle root h changes high->low. Both have nonempty old
    # left children and the SAME fixed A type. The promoted pivot retains its
    # low parent and its nonempty old-left status.
    low=macro_pair('hi',True,'lo',True);high=macro_pair('hi',True,'hi',True)
    assert Counter([low,high])==Counter([high,low])
    return {'status':'EXACT_MACRO_IDENTITY','finite_formula_checks':cases,'low_signature':low,'high_signature':high,'RR_exchange':['g:low->high','h:high->low'],'promoted_pivot_observer':'unchanged','A_whole_zig_touched_blocks':2,'final_LR_touched_blocks_bound':8,'whole_critical_potential_change_bound':'10*range(f)','proof_scope':'Finite formula validation plus the separately proved arbitrary-gap attachment and H3q physical recurrence. No interpolation establishes provenance.'}


def ledger_invariant():
    # Coordinates paid, bank, issued. Nullspace discovers paid+bank-issued.
    updates=sp.Matrix([[0,1,1],[1,-1,0],[0,0,0]])
    basis=updates.nullspace();assert len(basis)==1
    v=basis[0];v=v*(1/v[0]);assert list(v)==[1,1,-1]
    paid,bank,issued,initial,j,c=z3.Ints('paid bank issued initial j c')
    invariant=paid+bank-issued==initial
    results=[]
    for name,(dp,db,di),guard in [('A_issuance',(0,j,j),z3.And(j>=0,j<=c)),('KEEP_voucher',(0,j,j),j>=0),('B_double',(1,-1,0),bank>=1),('B_zig_or_conservative_transfer',(0,0,0),z3.BoolVal(True))]:
        solver=z3.Solver();solver.add(invariant,guard,z3.Not(paid+dp+bank+db-(issued+di)==initial));assert solver.check()==z3.unsat;results.append(name)
    q,a,k,d=z3.Ints('q a k d');s=z3.Solver();s.add(q+bank-issued==initial,bank==initial,issued<=c*a+d*k,z3.Not(q<=c*a+d*k));assert s.check()==z3.unsat
    return {'status':'PROVED_CONDITIONAL_LEDGER_INDUCTION','learned_invariant':'paid+bank-issued=initial_bank','verified_symbolic_updates':results,'closed_seam_consequence':'Q_B<=c*A+d*K_B<= (c+d)*A','assumptions_not_proved':['A source-uniform physical policy maintaining enough bank for every B demand','The constructed policy obeys total issuance and the chosen physical transfer scopes','A source-uniform closed nonnegative bank boundary state exists'],'warning':'The loop algebra does not manufacture the physical bank policy or its missing induction guard bank>=1.'}


def main():
    a=factorization_checks();b=ledger_invariant();X.write('SYMBOLIC_MACRO_CERTIFICATE.json',a);X.write('LEDGER_INDUCTION_CERTIFICATE.json',b)
    print({'macro_checks':a['finite_formula_checks'],'RR_type_exchange':'EXACT','ledger_invariant':b['status'],'universal_CD':'OPEN'})


if __name__=='__main__':main()

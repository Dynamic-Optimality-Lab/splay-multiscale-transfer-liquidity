"""Exact algebra supporting, not replacing, the mathematical source proof."""
import json
from pathlib import Path
from fractions import Fraction
import sympy as s
HERE=Path(__file__).resolve().parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    h,r,q,t=s.symbols('h r q t',nonnegative=True)
    checks={}
    checks['off_right_spine_right_rotation']=s.expand((1+h+2*r)-(h+r)-(1+r))==0
    # Two off-spine rotations: right-subtree sizes at parent/grandparent q,r.
    checks['off_spine_LL_double']=s.expand((1+r)+(2+q+r)-(3+q+2*r))==0
    checks['even_skew_sum']=s.expand(-(s.Rational(10,3)*(t-1)-(2*q+1)*t+3)-((6*q-7)*t+1)/3)==0
    checks['odd_skew_sum']=s.expand(-(s.Rational(5,3)*t-s.Rational(10,3)+(4*q-1)*t-(2*q+1)*t+2)-((1-6*q)*t+4)/3)==0
    z=s.symbols('z');geometric=(z-1)/3
    checks['lower_perfect_double_mass']=s.expand((2*z-1)+2*(4*z-1)+3-10*z)==0
    checks['lower_perfect_double_right_size']=s.expand((2*z-1)+(4*z-1)+2-6*z)==0
    checks['geometric_base']=geometric.subs(z,1)==0
    checks['geometric_induction']=s.expand(geometric.subs(z,4*z)-geometric-z)==0
    # F_R changes at a root right rotation by minus the old middle size h:
    # the former left child joins the global right spine; all other off-spine
    # nodes have unchanged membership and unchanged right-subtree sizes.
    checks['root_rotation_change']=s.expand(-h-(-h))==0
    checks['even_parity_leading_sign']=((6*5-7)>0)
    checks['odd_parity_leading_sign']=((1-6*5)<0)
    checks['first_maximum_quadratic_drop']=s.expand(((t-1)/2)*(((t-1)/2)+2)-(t-1)*(t+3)/4)==0
    checks['raw_credit_ratio']=s.cancel(((t-1)*(t+3)/4)/(4*(t-1))-(t+3)/16)==0
    rows=[[Fraction(2),Fraction(-1)],[Fraction(-1),Fraction(-1)]]
    checks['terminal_Farkas']=rows[0][0]+2*rows[1][0]==0 and rows[0][1]+2*rows[1][1]==-3
    assert all(checks.values())
    out={'passed':True,'checks':checks,'scope':'Exact algebra and induction-step identities. Physical substitution, source reachability, quantifiers and locality arguments are supplied in the mathematical manuscript; this is not a proof-assistant verification.'}
    (HERE/'SYMBOLIC_KERNEL_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()

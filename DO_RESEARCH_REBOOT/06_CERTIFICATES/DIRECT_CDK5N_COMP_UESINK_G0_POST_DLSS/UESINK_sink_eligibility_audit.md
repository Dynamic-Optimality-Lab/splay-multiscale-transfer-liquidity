# Joint sink eligibility audit (H4/H5 existential)

IN (a7c6504c): H≥3 non-exception candidates enumerated; exactly one (p=0:
x=3,H=18,c=1,q=3) satisfies the joint condition (w=1≤22=R−2; sole other
positives iv4 strict-K dA=4, iv8 strict-K dA=3 + strict-P). Sinks=[0].
No H4-only shortcut (code tests joint per candidate; first-eligible is the
unique eligible here).
Control (6b242e23): unique joint sink p=8 (H=4,q=3,w=1,R=6; 1+1+1=3≤6).
OUT (593b3f3a): no exception exists (|E|=0), so no joint sink question
arises; nonmembership already decided at H2.
First-H4-only failure mode (accepting H≥3 without H5) would wrongly admit
words whose other positives lack K/P — excluded by construction (joint
check mandatory per candidate; verified on IN/control where multiple H≥3
intervals exist but only the recorded p satisfies H5).

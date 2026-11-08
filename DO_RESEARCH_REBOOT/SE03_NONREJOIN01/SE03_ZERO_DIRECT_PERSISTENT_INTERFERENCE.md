# Persistent positive interference with no direct erased doubles

Status: original source family proving a uniform obstruction to a repayment
candidate. The family itself is already a small-support CD class and is
NOT promoted as new six-key CD coverage. It handles genuine zero-double
changes and exact recurrent alignment without a finite test.

Let p<x<s<g. Let A,B,C,D,E be arbitrary BSTs in the five inorder gaps.
Define full source trees

    T=g(p(A,s(x(B,C),D)),E),
    U=x(p(A,B),s(C,g(D,E))),
    V=p(A,x(B,s(C,g(D,E)))).

Consider the original all-KEEP period

    P=(Kp,Kx,Kp,Kg),

from diagonal(T,T). Kp is a left child ZIG. The next Kx has original
path R,L,L after that ZIG: LL at g,s,x then a right ZIG at p gives U.
The next Kp is a left child ZIG and gives V. Kg in V has path R,R,R:
RR at x,s,g followed by a right ZIG at p returns exactly T. Therefore
the full labeled A and B trees close. Full pre-depths are1,3,1,3;
A(P)=1+2+1+2=6, Q_full(P)=0+1+0+1=2. All three KEEP keys are genuine.

Erase BOTH Kp occurrences. During its FIRST period, E begins at T.
Its Kx has path L,R,L, so RL at p,s,x followed by a left ZIG at g gives

    E_x=x(p(A,B),g(s(C,D),E)).

Its following Kg is a right child ZIG, giving

    E_0=g(x(p(A,B),s(C,D)),E).

Thus the first erased period has Q_E=1. From E_0, Kx and Kg are simply
left and right child ZIGs and return E_0 exactly. Its recurrent charge
is0 per period. Original A returns to T after each period even in E,
because erasure changes only B modes. Hence after one common period
the pair(T,E_0) is legally reached by the changed-mode history from the
diagonal. Use the aligned block u=1,L=m for ANY integer m>=1.

On that ACTUAL closed comparison block the exact values are

    A_I=6m, Q_F=2m, Q_E=0,
    D=0, J=2m, Delta=2m, R=10m, R_p=12m.                  (1)

Full and erased B disagree at every retained Kx and Kg destination:
at x their right roots are s and g, and at g their left roots are p
and x. Full labeled trees, not just roots, establish this distinction.
At both Kp occurrences the full q is0: a genuine zero-double B change
can therefore create all of the repeated signed marginal.

The unaligned first-period marginal is1, while the aligned per-period
marginal is2. Over the first m+1 periods the marginal is2(m+1)-1;
subtracting the first-period transient marginal1 gives2m, exactly (1).
No transient unit is credited. All gaps/hangers are restored in each
history's own full recurrent state, which need not be the same state.

Consequently NO universal inequality J<=cD holds for any finite c, even
on original reachable fully closed source walks. Adding a state boundary
term cannot repair this candidate: any explicitly defined F/E-state
function has zero boundary difference on the aligned block, while D0
and J2m persist. This does not refute repayment by actual A capacity;
the original family has ample A cost and satisfies CD.

## A six-key embedding is a regression, not a novelty claim

The inherited nine-core obstruction starts at

    S=9(6(1(F0,2(F1,5(4(3(F2,F3),F4),F5))),
            8(7(F6,F7),F8)),F9)

and has marked support {1,3,5,7,9}. The new identity P applies at its
boundary with p=6,x=7,s=8,g=9 and A equal to the displayed1-rooted
subtree. Thus P itself is an exact arbitrary-fringe B identity on S.
Inserting P into any number of completed nine-core backbone periods
gives full genuine support {1,3,5,6,7,9}, core9, with genuinely nonrejoining
erased prefixes. Erased key6 has direct cost0 in every inserted P.

However the backbone's retained accesses can change subsequent signed
interference. Formula(1) applies to repeated P alone, not to this combined
six-key word. Its full/erased total, source A funding, paired simplicity,
and novelty against ALL inherited compositions are NOT established here.
The diagonal all-KEEP lift splits into old paired-closed P/backbone pieces.
Do not promote it as the mandatory new CD class or use it to claim a
completed support extension. No old backbone proof rows are rerun.

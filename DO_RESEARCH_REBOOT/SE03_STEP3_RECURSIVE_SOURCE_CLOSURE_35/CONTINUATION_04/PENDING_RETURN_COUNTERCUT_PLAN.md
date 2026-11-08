# Active proof work after checkpoint04 — NOT YET A CERTIFICATE

Root JR35 OPEN; reservation DEFERRED. Active caps symbolic2400/audit750/
global7200/queries3050000. User authorization call_495bdf978a1940b78c567c8b07c2fc40
is installed in C33 CONTINUATION_01/run_phase_2400_audit750_q3050000.py.
Keep all cumulative costs, including core62 failure and verify149 failure.

New reviewed source results since checkpoint04: BLC35 local alphabet
composition (independent_BLC35_proof_review.json via verify150; verify149
failed on receipt-schema handling, retained); RLC35 global DIRECT/SELF
normal form (independent_RLC35_and_B_only_control.json via verify151),
MFR35 two-axis return noncollision (independent_MFR35_theorem.json via
verify152). First-return event-cap2 is REFUTED on stored CCR event(59,1):
demands(59,2),(59,3),(56,2) choose two event units. ALL-return options do
fund the stored AF/CCR controls; independent_MFR35_all_return_control.json
(verify153). Universal all-return matching is OPEN, not refuted yet.

Source-only B bound Q<=2 genuine macros is refuted by genuine closed
maxcore7 word 1,11,3,9,1,13,5,7 (Q22,M8); independent verify151 replays
all8, diagonal A=B has A22 so not CD. Do not retry that shortcut.

Actual n15 source search: search_full_source15_beam.py, all-valid SS odd
B keys and A cheap helpers. Alias search_full_source15_beam_v2.py is an
EXACT BYTE COPY with same SHA256, needed by generated provenance path.
First core62 failed before save on that missing alias (4 source calls
charged). core63 batch1 saved, core64 batch2 saved. core65 batch3 uses
search_full_source15_beam_fullA.py (ALL A targets/true H) and may be running;
check its receipt before another CPU phase. No countercycle found yet.
All beam passes are only falsification searches, not universal proofs.

## New mathematical route to finish next

SS inversion: a full actual SS splay of x has old marked ancestors
G0,...,G(q-1) with unmarked separators. Its inverse word is

    Inv([])=[],
    Inv([G0]+tail)=[G0]+concat([y,G0] for y in Inv(tail)).

Length2^q-1. It restores the ENTIRE original B including arbitrary hangers,
using only SS marked accesses. Induction: first G0 undoes the outermost
two-rotation frame; each local inverse-letter y in the remaining marked
subtree is lifted by y,G0, which performs and immediately undoes the
outside root exchange. Total inverse Q=2^(q+1)-q-2. For any finite genuine
SS walk of k steps, append its inverse blocks in reverse order; total
macros M=sum2^q_i, total Q=2M-2k. This is a new uniform symbolic proof
idea; write and independently review it before promoting.

An optional Reach(T,z) recursion shows any marked z can be reached by SS
accesses from a tight maximal grammar tree: at a marked root, its immediate
U child has its marked child on the outer side. If z is in that marked
child's subtree, recursively operate there, lifting each local letter by
y,oldroot, then finish z. If z is in U's other (unmarked) subtree, first
promote the outer marked child; z is now in the smaller marked old-root
subtree. Recurse/lift, then finish z. Mark count strictly decreases.
Together with inverses this can close any SS source walk and visit every
mark; do not conflate it with A-quotient edge concatenation or funding.

## Proposed exact countercut to ALL MFR returns (not CD)

For m=3 use physical keys1..21, odd genuine marks (r11). Set Gi=1,3,5;
y=7; X3=13,X2=17,X1=21; boosters9,11,15,19. Define B0:

    root5,
    left V-(1,4),
    right 8(left=6(empty,7), right=V+(9,21)).

Bprev=Splay3(B0), one LL double. Forward genuine B word:

    5,13,3,17,1,21,7,1,3,5.

Expected original Q list [1,3,2,3,2,3,4,1,2,2]. Every path is M-U-M SS.
Append the per-access inverse words in reverse order to restore Bprev.
Expected total60 genuine macros, Q100. All11 odd marks occur (boosters
are inverse letters). Whole source is CD-safe: every genuine macro H>=1,
so2A-Q>=20 including all real A preparation/reset costs.

Before each original Gi, use canonical shortest A-only Gamma to the full
tree

    Gi(V+(1,Gi-1), (Gi+1)(empty,
       Xi(V+(Gi+2,Xi-1),V+(Xi+1,21)))).

Then KEEP Gi has A0 and ends the preparation macro. KEEP Xi is ONE actual
RR StepEv: pivot Gi at bit0 loses ancestry of BOTH Xi and y, since
Gi<Gi+1<y<Xi. Its B Q=3, outer G=Gi, so demand(Xi,3) is h0-unpaid. No
other operations lie in that Xi macro. Subsequent Gamma costs are retained
in later Gi macros. Each selected first MD group has exactly Xi then y:
later outer G accesses are on the opposite side; later Xj are outside
the retained Gi B subtree. Contact y has Gi as its original grandparents.

Before KEEP y use A-only Gamma to

    y( (y-1)(V-(1,y-2),empty), V+(y+1,21)).

KEEP y has A0. Then original DELETE(y-1)=DELETE6 is one terminal zig
pivot y, making the whole y-subtree (root7,rightV+8..21) a rigid hanger
right of the largest low key6. The next genuine1,3,5 are all<y. Their
actual A splays never enter that hanger. Thus each selected return channel
z=y to its old Gi, from contact7 to next genuine Gi, has EXACTLY ONE loss
event: DELETE6. Relaxing to both real event units gives3 unpaid demands
and2 units, deficiency1, EVEN with all return choices and owners relaxed.

After those resets, execute the literal B inverse word in A as ordinary
KEEPs, then canonical A-only Gamma back to Bprev. All costs are real and
retained. Full A/B close. Repeat the full original word; erased B/chart
first recurrence after warmup gives the actual paired-closed source
period, symbolically as in the accepted source realization proof.
No Gamma word or numeric erased/chart period is falsely reported replayed.

General m>=3: Gi=2i-1, y=2m+1, top X1=6m+3, Xi=6m+7-4i, r=3m+2,
B0 rootGm with leftV-(1,2m-2) and right(y+1)(left=(y-1)(empty,y),
right=V+(y+2,6m+3)). Forward pairs Gi,Xi descending i, then y, then Gi
ascending. Initial Bprev=SplayG(m-1)(B0). Same proof, m residual return
claims collapse on DELETE(y-1)'s two units, deficiency m-2. This remains
an UNVERIFIED CANDIDATE until exact source construction/audit finishes.

Producer can compute all B steps through accepted native11 off-target-
leaf substitution with Lift(n21), no rank catalogue. All B target depths
are<=8 at m3, so there is a non-target leaf down to n11. No fresh producer
engine query needed. Independent Mutable replay needs60 B calls plus
7 critical A controls, within ~137 remaining query cap. Preserve actual
query ledger before execution. No complete Gamma numeric replay needed.

If validated, this refutes only the FROZEN MFR all-return donor rule,
even on true natural h0 residuals; it does not refute all joint funding.
Prior preparation/inverse source bits outside those return pools remain
available. Continue the original root, not a local patch of the rule.

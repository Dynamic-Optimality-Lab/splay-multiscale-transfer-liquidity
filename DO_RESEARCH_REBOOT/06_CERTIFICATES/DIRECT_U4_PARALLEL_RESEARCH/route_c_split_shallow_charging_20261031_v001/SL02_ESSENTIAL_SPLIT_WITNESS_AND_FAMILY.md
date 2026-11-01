# A cross-run excess split between physical payers

Status: FINITE-EXACT for the literal replay and reflection; PROVED analytically for the fringe and unbounded-support extensions below. This is a strict witness for SL beyond XR, not a finite fit for universal CD.

Start diagonally at the right vine R13. Prefix DELETE13, DELETE12 reaches A=S_12(S_13 R13), B=R13. Use the predeclared 44-request cycle, with K=KEEP and D=DELETE:

    K13 D11 K12 K2 D1 D2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D13 D12.

The prefix is provenance only and provides no cycle credits. Every cycle request is its own A-root block. Actual totals are A=68, Q_B=36, Z_B=25, and 2A-Q_B=100. The first six blocks have the following exact source costs.

| Occurrence | Request | d_A | d_B | a | q | delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0 | K13 | 1 | 12 | 1 | 6 | 4 |
| 1 | D11 | 5 | frozen | 3 | 0 | -6 |
| 2 | K12 | 2 | 6 | 1 | 3 | 1 |
| 3 | K2 | 2 | 1 | 1 | 0 | -2 |
| 4 | D1 | 1 | frozen | 1 | 0 | -2 |
| 5 | D2 | 1 | frozen | 1 | 0 | -2 |

The only positive blocks are 0 and 2, separated by the nonpositive DELETE11. Anchor 0 has C_0={1,2}; anchor 2 has C_2={13,2}. Their common key is 2. Both record post-height h(2)=1.

## Exact local source identities

Notation k(L,R) means a node, a bare integer a leaf node, and '.' empty. Put

    U = 6(4(3,5),10(8(7,9),11)),
    V = 10(6(4(3,5),8(7,9)),.).

The initial A is 12(2(1,U),13). Its first four destinations are

    after K13: 13(12(2(1,U),.),.),
    after D11: 11(2(1,V),13(12,.)),
    after K12: 12(11(2(1,V),.),13),
    after K2:   2(1,11(V,12(.,13))).

D1 then D2 are inverse A zigs and restore that last A tree. They leave B frozen. B's first two genuine destinations are

    after K13:
      13(2(1,4(3,6(5,8(7,10(9,12(11,.)))))),.),
    after K12:
      12(2(1,U),13).

K2 then gives B=2(1,12(U,13)). It is a single B zig with q=0. These identities use the exact source parent-first same-side rotations; the full event orientations, endpoints and raw trees are in split_shallow_certificate.json and are independently replayed by the pointer source.

For K3,...,K13 immediately following the split, the B-double counts are

    2,1,1,0,2,1,1,0,1,0,0.

A changes root at each of these requests, so a>=1 and none is positive. By occurrence 16, the K13 destination is the common left vine L13. The next complete ascending scan ends again at L13; the descending scan ends at R13. Final D13,D12 restore the initial A, while B stays R13. Thus the whole actual pair closes, not merely an abstract projection.

## One four-unit debt, two two-unit pools

At cut 0, positive locals discharge two B demands from each positive anchor. Four residual demands remain at anchor 0 and one at anchor 2. DELETE11 lends nothing because key 11 is in neither shallow set. Its six actual units are retired unused.

| Payer occurrence | Pool | Source ceiling / reservation | Recipient and residual interval | Loan unit interval |
| --- | ---: | --- | --- | --- |
| 3, K2 | 2 | min(1,0)=0 / 0 | anchor 0: [0,2) | [0,2) |
| 4, D1 | 2 | 0 / 0 | anchor 0: [2,4) | [0,2) |
| 5, D2 | 2 | min(0,0)=0 / 0 | anchor 2: [0,1) | [0,1) |

At K2, the late anchor has h=1,k=0 and certifies q=0. At D1 and D2, no KEEP occurs, so their own-work ceilings are exactly zero. D1 is eligible only for anchor 0. D2 pays the remaining unit of anchor 2 and retires its other unit. The physical loan credits are

    (3,0,0), (3,0,1) -> anchor 0 residuals 0,1;
    (4,0,0), (4,0,1) -> anchor 0 residuals 2,3;
    (5,0,0)          -> anchor 2 residual 0.

Occurrence 5 still records both anchors as source facts even though anchor 0 has been fully paid. No previously used credit appears in the third pool. The B-changing zero-double zig at occurrence 3 is counted in the subsequent intervention histories.

## Why every XR cut rejects

If anchor 0 is the first positive encountered, DELETE11 is the only intervening block before anchor 2 and has no eligible key. XR therefore retains both anchors, excess E=5 and common set {2}. The only possible key-2 closing blocks are:

| Payer occurrence | Actual A capacity | XR minimum ceiling | E+c | Result |
| --- | ---: | ---: | ---: | --- |
| 3 | 2 | 0 | 5 | reject |
| 5 | 2 | 0 | 5 | reject |
| 18 | 6 | 13 | 18 | reject |
| 40 | 2 | 35 | 40 | reject |

DELETE1 has key 1 and cannot close a common batch containing anchor 2. A cut may omit some of these later candidates, which cannot help it. If anchor 2 is encountered first (cuts 1 or 2), any repayment of that anchor precedes the later anchor 0; after that later anchor 0, the pass ends with at most DELETE11 remaining and no eligible payer. Therefore XR rejects all 44 cuts.

SL succeeds at cuts {0,6,7,...,43}, exactly 39. Cuts 1,...,5 retain explicit unpaid debt and are not promoted. Reflection x->14-x swaps left/right and gives the same costs, memberships and physical-pool cardinalities. Both orientations are independently verified.

## Arbitrary right fringe, without larger finite fits

Graft any BST F with all keys >13 at key 13's right child in the diagonal R13. Every requested key of the literal word is <=13. No search or rotation descends into F. In each local rotation F is carried as an unchanged fringe. Structural substitution of F for that leaf therefore commutes with every request in the prefix and cycle.

All depths, A/B events, six initial costs, split loans and exact closure for requested keys stay unchanged. The C_2 shallow set may additionally contain F's root, but that key is never requested and C_0 remains {1,2}. The common key remains only 2, so the XR rejection proof also survives. This proves an arbitrary-size/fringe strict family by substitution, without executing a larger tree or imposing a fringe weight.

## Unbounded genuine KEEP support

For every n>=13 use the diagonal R_n and prefix D13,D12. Replace only the scan ranges in the literal cycle:

    K13 D11 K12 K2 D1 D2 K3 ... Kn;
    K1 ... Kn;
    K(n-1) ... K1; D13 D12.

Its length is 3n+5. The fixed <=13 portion commutes with the right fringe R_[14,n], so the first two excesses and their three paying pools are identical. The fixed K3,...,K13 portion synchronizes A and B to L13 with that right fringe. All later requests are common KEEPs until the final DELETEs and therefore nonpositive: for a common depth d, floor(d/2)<=2ceil(d/2).

An increasing complete access scan of a BST produces the left vine: induct on the next larger accessed key, preserving the consecutive already-accessed keys as its left spine and leaving only larger keys on the right. The descending counterpart produces the right vine. Thus K14,...,Kn extends the synchronized tree to L_n; the following complete ascending scan again gives L_n, descending K(n-1),...,K1 gives R_n, and the last two DELETEs restore A's prefix state. B remains R_n. All keys 1,...,n are actually KEPT.

For strictness, the only positives remain 0 and 2. Their common shallow key is still 2. The two early eligible pools each have capacity 2 and cannot meet E=5. At the key-2 access in the complete ascending scan, exactly n genuine B changes intervene after anchor 2: the first K2, K3,...,Kn, and K1. Its conservative XR ceiling is n. Any A depth is at most n-1, hence its capacity 2ceil(d_A/2)<=n. Consequently E+n exceeds that pool. The key-2 access on the descending scan has A depth 1, capacity 2 and ceiling 3n-4. No other common-key payer exists. The same two cut-order cases prove every XR cut rejects; SL cut 0 already clears both anchors at its first three eligible pools.

This is a structural proof for every n>=13, not a numerical extrapolation. Only the fixed 13-key core and its reflection were newly evaluated. Eight earlier fixed source controls were replayed unchanged; there was no word search, size sweep, fit or allocation solver.

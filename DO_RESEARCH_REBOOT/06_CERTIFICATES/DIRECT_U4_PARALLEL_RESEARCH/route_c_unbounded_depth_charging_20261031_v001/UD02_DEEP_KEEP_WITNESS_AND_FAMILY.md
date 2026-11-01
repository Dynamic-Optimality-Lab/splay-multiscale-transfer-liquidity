# A genuine deep KEEP lender with its own B work reserved

Status: FINITE-EXACT for the fixed source replay and reflection; PROVED analytically for the arbitrary-fringe and unbounded-support families below. Only the predeclared 13-key word was newly evaluated. No fit or larger finite key size was used.

Start diagonally at R13 and apply prefix D13,D12. Here K is KEEP and D is DELETE, which leaves B frozen. The resulting A is S_12(S_13 R13), and B remains R13. Use this 44-request cycle:

    K13 K11 K12 K2 D3 D2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D13 D12.

It differs from SL's fixed word only at D11->K11 and D1->D3. The tuple and pointer sources agree on every state and event. Every request is its own A-root block. Totals are A=68, Q_B=35, Z_B=30, and 2A-Q_B=101. The pair returns exactly to its cycle initial state. Prefix costs never pay cycle demands.

## Fixed local source calculation

| Occurrence | Request | d_A | d_B | a | q | delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 0 | K13 | 1 | 12 | 1 | 6 | 4 |
| 1 | K11 | 5 | 7 | 3 | 3 | -3 |
| 2 | K12 | 2 | 2 | 1 | 1 | -1 |
| 3 | K2 | 2 | 3 | 1 | 1 | -1 |
| 4 | D3 | 5 | frozen | 3 | 0 | -6 |
| 5 | D2 | 1 | frozen | 1 | 0 | -2 |

Only occurrence 0 is positive. Its old shallow set is {1,2}. Before this anchor, key 11 had B depth 10 and key 3 had B depth 2. Both actual lenders lie outside the old root/child set.

In notation k(L,R), with '.' empty and a bare integer a leaf, B just after K13 is

    13(2(1,4(3,6(5,8(7,10(9,12(11,.)))))),.).

Thus h_0(11)=7. Source splaying 11 gives

    11(4(2(1,3),8(6(5,7),10(9,.))),13(12,.)).

The seven-edge path has three doubles and a final zig. At its A side the corresponding path has five edges, giving three actual A StepEvs, hence six units. No B change intervenes after the anchor, so its exact historical ceiling is

    c_0(1)=floor(7/2)+0=3.

Reserve the first three units of that six-unit pool for its own three B doubles, and lend the last three units to anchor 0. This uses a genuinely deep KEEP, with a binding nonzero own-work reservation; it is not only an unrestricted DELETE loan.

K12 and K2 have conservative ceilings 4 and 2 respectively, capacities 2 each and actual q=1 each. They reserve their whole pools and lend nothing. They each have an actual spare unit that UD deliberately refuses to use, confirming that the reservation rule is not an exact-surplus oracle.

DELETE3 then reserves zero and lends one of its six units, clearing the last residual. Its other five units retire unused. DELETE2's two units are not needed. The actual split is:

| Payer | Own reserved prefix | Anchor 0 residual interval | Loan unit interval |
| --- | --- | --- | --- |
| occurrence 1, K11 | [0,3) | [0,3) | [3,6) |
| occurrence 4, D3 | empty | [3,4) | [0,1) |

The loan credits are (1,1,1), (1,2,0), (1,2,1), and (4,0,0). They are distinct from each other, the payer's own prefix and the anchor's two local units. The anchor's residual cursor moves 0->3->4, so no B double is paid twice.

After the split, K3,...,K13 have B-double counts

    1,0,2,1,1,0,1,0,0,0,0.

At each request A changes root and has a>=1, so none is positive. By occurrence 16, both trees are L13. All subsequent KEEPs are common. The ascending scan again yields L13, descending K12,...,K1 yields R13, and the last D13,D12 restore the initial A while B stays R13. This proves actual paired closure, not only an abstract walk closure.

## Old shallow failure at every cut

SL has the same sole positive anchor, with excess 4 and source set {1,2}. It cannot use K11 or D3 at all. Its possible eligible pools within the full physical period are:

| Occurrence | Key | Capacity | Historical ceiling | SL certified spare |
| --- | ---: | ---: | ---: | ---: |
| 3 | 2 | 2 | 2 | 0 |
| 5 | 2 | 2 | 0 | 2 |
| 17 | 1 | 12 | 15 | 0 |
| 18 | 2 | 6 | 15 | 0 |
| 40 | 2 | 2 | 37 | 0 |
| 41 | 1 | 2 | 39 | 0 |

All other keys are ineligible, including the final DELETE13 and DELETE12. Across an entire period the anchor can receive at most two old certified units, less than its four-unit excess. Any cut can only omit some of these available later pools; none can add a second copy. Thus SL rejects all 44 cuts.

UD succeeds at cuts {0,5,6,...,43}, exactly 40. Cuts 1,...,4 retain unpaid demand and correctly reject. Reflection x->14-x gives the second 13-key witness with identical costs, capacities and cut counts, and exact mirrored source states throughout.

## Arbitrary unrequested fringe

Replace R13 by R13 with any BST F of keys >13 grafted at key 13's right child. The prefix and fixed cycle never request a key in F. Each search stays among keys <=13, and every source rotation carries F intact as an off-path fringe. Substituting F for that leaf therefore commutes with the whole prefix and cycle.

The actual depths/events of requested keys, h_0(11)=7, the two lender slices and paired closure remain unchanged. Anchor 0's pre-B root/child set stays {1,2}, so SL's rejection table also remains unchanged. UD's source fact for each requested key is preserved. This supplies arbitrary tree size and fringe shape without a new finite replay or a fringe-weight assumption.

## Family with unbounded genuine KEEP support

For every n>=13, start diagonally at R_n, apply prefix D13,D12 and use

    K13 K11 K12 K2 D3 D2 K3 ... Kn;
    K1 ... Kn;
    K(n-1) ... K1; D13 D12.

The cycle length is 3n+5 and every key 1,...,n is KEPT. The fixed <=13 part commutes with the right fringe R_[14,n]. Its first positive and split repayment 3+1 are exactly as above. The fixed K3,...,K13 scan synchronizes A and B to L13 with that right fringe; K14,...,Kn extends it to L_n. Later KEEPs are common and nonpositive. Complete increasing and decreasing scans produce L_n and R_n respectively by the usual successive-key spine induction. The final D13,D12 restore the prefix A, and B stays R_n. Thus UD cut 0 succeeds and the actual pair closes for every n.

Only anchor 0 is positive. Under SL its only eligible keys remain 1 and 2. Early K2 has ceiling/capacity 2/2 and no spare; D2 supplies exactly two units. At K1 in the full ascending scan, k=n+1 and h_0(1)=2, giving ceiling n+2. At the following K2, k=n+2 and h_0(2)=1, again ceiling n+2. Every A depth is at most n-1, so both capacities are <=n and provide no old certified spare. Descending K2 and K1 have capacity 2 and ceilings 3n-2 and 3n. There is no other eligible lender. Thus the old total remains two units <4 at every n and every cut.

This analytically proves strict coverage with unbounded genuine support. The all-size source/ledger theorem UD01 itself permits arbitrary h, not just this family's fixed h=7. No larger finite n, fit, source graph or search was used; the ten old fixed controls were replayed without changing their source words, totals or old cut certificates.

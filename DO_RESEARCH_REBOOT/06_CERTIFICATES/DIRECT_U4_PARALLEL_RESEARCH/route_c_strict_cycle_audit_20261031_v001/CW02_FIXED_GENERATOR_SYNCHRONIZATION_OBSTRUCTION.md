# The fixed KEEP-only candidate synchronizes before a closed witness forms

Status: REFUTED—EXACT as a proposed strict FI\UD witness. Its all-lap/fringe obstruction is proved below. Strict new closed-walk coverage remains NOT ESTABLISHED. This is not a refutation of strict FI coverage on other seeds or words.

The gate fixed diagonal R13, setup prefix D13,D12 and the KEEP generator

    W=K13 K11 K12 K9 K10 K7 K8 K5 K6 K3 K4 K1 K2.

The source recurrence was capped at 64 laps, with immediate stopping on diagonal synchronization. It stopped after ten requests, before the first whole lap completed. No word, seed, parameter, ceiling or key size was changed after that result. The continuation begins with the known FI-only early-repayment triple but uses descending adjacent pairs to avoid the old complete reset scans. It nevertheless synchronizes.

## Exact source replay

| Occurrence | KEEP key | d_A | d_B | a | q | z | Pair equal afterward? |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 13 | 1 | 12 | 1 | 6 | 0 | no |
| 1 | 11 | 5 | 7 | 3 | 3 | 1 | no |
| 2 | 12 | 2 | 2 | 1 | 1 | 0 | no |
| 3 | 9 | 6 | 5 | 3 | 2 | 1 | no |
| 4 | 10 | 2 | 3 | 1 | 1 | 1 | no |
| 5 | 7 | 5 | 5 | 3 | 2 | 1 | no |
| 6 | 8 | 3 | 3 | 2 | 1 | 1 | no |
| 7 | 5 | 5 | 4 | 3 | 2 | 0 | no |
| 8 | 6 | 3 | 2 | 2 | 1 | 0 | no |
| 9 | 3 | 4 | 4 | 2 | 2 | 0 | YES |

The ten KEEP requests have A=21,Q_B=21 and only the first block is positive. Both source implementations agree on all raw trees, event identities/orientations and costs. In k(L,R) notation, bare leaf keys and '.' empty, the common destination is

    3(2(1,.),5(4,6(.,7(.,8(.,9(.,10(.,11(.,12(.,13))))))))).

The canonical tree is encoded explicitly in fixed_generator_certificate.json; the displayed expression names that same source identity. It is a paired-state equality, not a projected invariant. The setup starts from a true diagonal and is replayed separately, so the non-diagonal seed is reachable without borrowing its credits.

## Why this excludes all future strict cycles for the candidate

After any common KEEP, both roots are that request key. The ten requested keys above are all distinct. Thus no two after-request pair states in this transient can coincide; the initial post-setup roots are different, so it cannot equal any after-KEEP pair either. The independent verifier also checks the complete paired states directly. All nine states preceding synchronization are non-diagonal.

Once A=B, any future KEEP applies the same source map to identical trees, so equality persists. At every such request, for common depth d,

    a=ceil(d/2), q=floor(d/2),
    q-2a<=0.

Root no-ops have a=q=0. Therefore every subsequent actual closed subwalk contains only nonpositive A-root blocks and is already accepted by UD by local payment; FI has no strict new case there. No non-diagonal transient state can reappear in this diagonal future. There was no earlier repeated pair. Hence the post-setup infinite W continuation contains no strict FI\UD closed walk, for ANY number of laps.

This conclusion does not depend on evaluating 64 laps or extrapolating finite stability. Exact synchronization after ten requests and diagonal invariance prove it for the entire future. No closed candidate was extracted, no new all-cut cycle comparison was needed, and no transient or synchronization endpoint was mislabeled a closed walk.

Reflection x->14-x gives synchronization at the tenth KEEP11, with identical costs and mirrored complete source states. It is the same fixed candidate under symmetry, not a second searched word.

## Arbitrary fringe extension without a larger finite replay

Graft any unrequested BST F with all keys >13 at key 13's right child in the diagonal R13. Every setup and first-ten request is <=13. No search descends into F; source rotations carry it unchanged. Substitution of F for that leaf commutes with the complete finite source identity above. Both destinations are the same displayed common tree with F at 13's right child.

Thus synchronization occurs at the same point for every such fringe size and shape. Any later KEEP-only continuation, including arbitrary requests to F's keys, remains diagonal and locally UD-covered. The transient still has distinct requested roots and non-diagonal states. This proves an all-size obstruction for THIS reachable seed family and its KEEP-only continuations. It is not a theorem about arbitrary initial pairs, arbitrary generators, all tight-ceiling walks or all source cycles containing other DELETEs.

The fixed source attack did not meet the strictness criterion. No newly settled original CD cycle case is claimed. The predeclared stop applies; Stage 11G and the matching-terminal freeze remain unchanged.

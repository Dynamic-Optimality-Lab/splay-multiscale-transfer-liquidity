# Exact domain and imported proof audit

All paths here are relative to DO_RESEARCH_REBOOT unless explicitly external.

## Imported leaves and their original hypotheses

| Leaf | Original domain | Supporting proof / completion record |
|---|---|---|
| RT2-A | Diagonally reachable, exactly paired-closed; <=3 KEEP keys; arbitrary present DELETEs, n and length | 06_CERTIFICATES/DIRECT_NFKS_RT2/DIRECT_NFKS_RT2_coarse_double_class_proof.md and DIRECT_NFKS_RT2_terminal_status.json; depth/roundtrip/idempotence proofs alongside |
| CDK4-A | Original exactly closed class with four KEEP keys; arbitrary n/length/DELETE pattern | 06_CERTIFICATES/DIRECT_CD_K4/DIRECT_CD_K4_original_class_proof.md; B_cycle_conservation.md; seven_node_reduction.md; pruning_commutation_proof.md; one_bit_potential_certificate.md; terminal_status.json (same DIRECT_CD_K4_ prefix) |
| CDK5L-A | Exactly closed, reachable; five KEEP keys; core<=8 at every boundary; arbitrary n/length/order/DELETEs | 06_CERTIFICATES/DIRECT_CDK5_LOW/DIRECT_CDK5_LOW_restricted_class_proof.md; source_reduction_proof.md; terminal_status.json; independent_verification.json (same prefix) |
| Restricted CD | Five genuine KEEP keys, fixed nine-core; full original W_5^9 domain | RESTRICTED_CD_STEP04/RESTRICTED_CD_CERTIFICATE.json; proof, domain/dependency audit, independent audit and final_manifest.json |

The older complete finite certificates support universal reduced-graph
statements only together with the proved all-size projections. Their existing
reports are read as completed proof components: CDK4 has68876 covered reduced
transitions and zero violations; CDK5-LOW has142385 covered edges and an existing
independent PASS. We do not execute their verifiers, regenerate edges, check the
old rows again, replay witnesses, or use new finite tests. Provenance of those
artifacts is checked against the pre-existing XFER19 entry hash baseline.

The nine-core component is reused through its final publication seal. Its full
input dependency pins, phase results and original source files are retained.
The new base adds no compiler constraints, populations, masks or graph states.

## Bridges required for this union

1. **Support names:** the older leaves use all KEEP keys M, whereas CD(5) uses
   genuinely B-changing KEEP keys G. If G is nonempty, cyclic last-genuine-root
   provenance gives M=G. If G is empty, do not apply that equality: prove Q=0.
2. **Whole-walk geometry:** the five-key leaves require core<=8 throughout or
   core9 throughout. Marked-splay core-set inclusion and B closure give one
   fixed labeled core, not merely a size bound at a selected boundary.
3. **No missing core:** the existing arbitrary-M K4-L1 bound and visited-mark
   induction give5<=c<=9 when |M|=5. Integer interval splitting exhausts the
   possibilities. This is a structural proof, not an experiment on small trees.
4. **Closure:** the domain is reachable from some diagonal and then exactly
   closed in both full labeled trees. It does not require the cycle's start to
   be diagonal. Cyclic seam arguments use complete B closure for core/root
   facts and complete A closure for C_full<=A. Root equality alone is insufficient.
5. **Reachability:** rotation of a reachable closed walk remains reachable:
   follow its reaching prefix and then the appropriate finite segment. Thus
   any cyclic seam used by a leaf keeps the original reachability hypothesis.
6. **Costs:** all leaves use root edge-depth0, original StepEv a=ceil(d_A/2),
   source q=floor(d_B/2), and DELETE B-charge0. Nongenuine KEEP may have positive
   A cost. Its B charge is0; that never discards its A cost. LT=d+1 is not used.
7. **No mixed leaf arithmetic:** choose one theorem for the entire walk. The
   lower-core q-2C_KEEP edge inequalities are not stitched to M3's 2A-q edges.
   Each leaf supplies the same terminal statement Q<=2A. Nine-core B-only
   Q<=2C_KEEP is neither used nor claimed.

## Original semantics and historical discrepancies

The source-only audit reads `python/independent/splay.py` (_descend/_rebuild/
trace), `python/liquidity/legacy_embedding.py`, and `scripts/wp6_cycle_ratio.py`
as syntax. These tracked files are pinned against the unchanged HEAD and never
imported or executed. Ordinary present-key splay ends with its target at the
root; depth0 leaves the full tree unchanged. KEEP/DELETE semantics are those
in the already pinned U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md and frozen11F domain.
The broader repository's absent-key conventions are outside this original route.

K4-L1's arbitrary-M rotation proof and growing-visited-set reduction are reused.
CD5_PROOF.md independently supplies the rigid-hanger argument for set inclusion.
The old CDK5-LOW source-reduction paragraph claiming possible core-label swaps
is superseded and not used. The later11F set-inclusion/constancy argument gives
the needed stronger fact. The old reduced graph's size/shape overapproximation
still covers all real <=8-core projections, so this correction adds no premise.

Old terminal files saying the nine-core case OPEN are historical; the sealed
Restricted-CD certificate discharges it. Old files saying general CD or DO OPEN
remain correct at those broader scopes. No historical record is overwritten.

## Coverage and claim boundary

No restriction is added on ambient key count, word length, DELETE targets,
support of DELETEs, relabeling, fringe topology/population, marked mask or
signature. Zero events, nongenuine events, E3/E4 and primitive/nonprimitive
cycles remain allowed. Empty histories and empty key sets use Q=A=0; no
nonempty-core hypothesis is imposed on that branch. Zero-A walks require no
special feasibility assumption: the selected class theorem yields Q<=0.

CD(5) is universal over its stated closed-walk class, restricted only by
|G|<=5 and the original model. It is not a universal theorem over arbitrary
support. No prefix/startup or Dynamic Optimality result is promoted. R1-R4 and
Bank25=25 are preserved. The audit reuses completed mathematical theorems and
their accepted certificates; it is not external peer review or a new formal
verification of the original tree engines.

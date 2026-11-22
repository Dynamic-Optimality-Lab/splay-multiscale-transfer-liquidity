# GSO: complete-history Omega5 cycle search

**Universal Omega5/A and Universal Coarse-Double remain OPEN.** This checkpoint
implements the explicitly requested teacher upgrade. It supplies no universal
finite constant and no replacement scoped theorem.

## What changed

The previous full-state teacher stopped at six keys, where the five-credit
target refill automatically covers every B access. The previous large-support
beam stopped at its first failed payment and optimized a prefix packet statistic.
Neither implementation optimized accumulated unpaid cost on a complete period.

This module:

- Accepts full original trees at supports beyond that regime. Every physical
  vertex, including never-accessed hanging keys, remains in the state.
- Completes all physical operations after an underpayment. A failed double
  contributes one original unpaid cost; later steps are still executed.
- Ranks candidates by the exact rational **Omega5/A** of the complete original
  period, including all preparatory and restoring A work.
- Recomputes the frozen bank's **greatest clipped cyclic balance** for each
  candidate. Reaching-prefix credit is excluded.
- Extracts recurrent periods only when the full labeled A and B trees both
  repeat exactly. A stock-blind physical cycle is then evaluated afresh at its
  canonical bank seam; search-prefix stocks are never borrowed.
- Tracks real credit tokens through transfers, ancestry recreation, and the
  cyclic seam. Every funded B double is assigned a distinct slot of a literal
  original A StepEv, with load at most45.
- Records original dry packets and their last funded target drain. It does
  **not** assume that this predecessor has bounded congestion.
- Uses a separate functional-tree checker and the pinned original independent
  splay primitive. The checker imports no producer or bank code.

This is a bounded large-support physical adversary, not exhaustive enumeration
of every large paired-tree state. General invention of an arbitrary invariant
and its induction proof is not implemented by this upgrade.

## Frozen mathematics

A splays every KEEP and DELETE. B splays only KEEP. DELETE removes no key.
Original costs are ceil(depth_A/2) and floor(depth_B/2).

Blocks contain at most five consecutive physical ranks, each with capacity5.
A events reset their actual footprint; genuine KEEP resets its target once.
LL/RR pooling priority is target, middle2, external, old grandparent, old parent,
middle1, coalescing repeated or missing owners stably. Other B steps retain
target-first/increasing-block order. Terminal B zigs remain physical events
with zero original demand.

P5 is the literal paid original B-double count and Omega5 its raw complement.
On a closed trajectory, paid equals actual issuance. A issuance is at most40A;
the disjoint genuine-KEEP voucher map costs at most5A. Thus the preserved
partial budget is P5<=45A and Q_B<=45A+Omega5.

An unpaid event sees no credit and does not decrease the bank total. These
accounting identities do not bound its recurrence. A physical all-source
argument limiting repeated empty-footprint work remains missing.

## Run

From this directory, Python 3.10+ and the standard library suffice:

~~~powershell
python -B tests.py
python -B gso_omega.py status
python -B gso_omega.py search --output fresh_run --supports 33 65 129 257 513 1025 --evaluations 8000 --seconds 300 --seed 251129
python -B gso_omega.py verify run_002/complete_00.json.gz
python -B gso_omega.py accept run_002/complete_00.json.gz
python -B preserve.py --verify-seal
~~~

Search outputs require a fresh path and an unsealed versioned checkpoint.
Verification is read-only. The historical-byte check, requiring the original
local research archive, is:

~~~powershell
python -B preserve.py
~~~

The new engine and finite certificates are self-contained in Git. Historical
research directories that were already untracked are not needed at runtime and
are not silently included in the publication.

## Exact objectives and controls

The primary score is always the exact complete-period Omega5/A fraction.
Tie-breaking prefers histories with an actual B access exceeding five doubles,
then low payment margins and complete Q_B/A. Large support alone does not
exclude automatically funded short recurrent words.

Mutation includes counted helper preparations, KEEP/DELETE changes, repeated
subwords, multiscale local restoration, reflected traffic, and crossover between
different histories. Every evaluated source either contains its full restoring
tail or has an exact full-pair recurrence with an admissible reaching prefix.

The unpaid-continuation regression uses a genuine eight-double physical B trace
with a deliberately forced low-stock entry. It verifies three consecutive
underpayments and completion of all eight steps. That forced entry is **not**
claimed reachable under the frozen policy and is not an original counterexample.
It only checks that the objective and failure continuation are nonvacuous.

Eighteen implementation tests cover all five original splay step forms,
arbitrary physical labels, complete closure, cyclic cuts/repetitions, prefix
exclusion, pure credit circulations, and rejection of missing demands, changed
seams, duplicate original-A slots, and forged universal-proof metadata.

## Evidence and limitations

Each retained certificate contains its entire original source, literal physical
events, the greatest cyclic seam, every bank transition, and A-credit provenance.
An independent replay checks those objects. Population counts are producer
diagnostics; only the retained certificates are independently replayed.

The first run predates the explicit per-access nonvacuity tie-break and crossover;
its retained sources remain independently checkable. The second run records
that refinement. Neither a zero observed residual nor a maximum observed ratio
is a universal theorem.

The acceptance command remains closed because no independent arbitrary-source
Omega5 bound and induction proof has been supplied. A caller cannot promote a
finite result by changing a status field.

## Actual nonzero residual and the proof outcome

The resumed search finds an independently verified complete257-key original
source with A=989, Q_B=519, P5=517 and Omega5=2. Its raw source and every physical
event are in run_003/complete_00.json.gz. Both full labeled trees and the bank seam
close. The independently reconstructed unpaid original IDs are B(99,14) and
B(99,15). The old frozen policy implementation agrees with the new one on this
same source, including every footprint and priority.

At B(99,13) the target's last credit is consumed. The next two RR doubles have
all-zero footprints and remain physically executed. B(99,16), an LL double,
then encounters two full banks and resumes payment. The failure is therefore
present under the greatest cyclic balance and continues through real restoration.
Repeating the whole source doubles both A and Omega5; no prefix or boundary
allowance forgives the unpaid cost.

This refutes full payment by the selected H=5 policy, which was previously open.
It preserves the45A partial budget and does **not** refute Omega5=O(A).
The source has cyclic rank-travel L=645, L/A=15/23, so it also retains the older
whole-cycle rank-travel certificate. It is not a newly established UF escape.

The run's mathematical target remains unfulfilled: no absolute universal K was
proved. The finite source count, observed ratio and implementation checks are
not a substitute theorem. In particular, the observed dry-packet length two
is not asserted to be universally bounded by two.

Resume from a verified COMPLETE source, recomputing its greatest seam:

~~~powershell
python -B gso_omega.py search --output fresh_resume --supports 257 --evaluations 12000 --seconds 180 --seed 12222026 --seed-certificate run_003/complete_00.json.gz
~~~

Later runs save compressed producer-code snapshots for reproducibility. Only
rehydrate those into a fresh unsealed checkpoint. The first exploratory run
has independently checkable retained sources but predates this snapshot feature.

The main mathematical frontier and scope ledger are maintained in
[the existing GSO Notion page](https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d).

## Preservation and publication

ADMISSION.json records the user's specific upgrade and GitHub-push authorization.
The old source, policy, proofs and seals are unchanged. The vendored functional
primitive is byte-identical to the existing tracked independent primitive;
PROVENANCE.json pins it and the policy inputs.

PRIOR_BASELINE.json pins every workspace file opened by the successful inherited
preservation/seal chain. The original tracked tree is separately compared with
the old HEAD. The new checker permits the user-authorized commit while rejecting
changes to old tracked content. The inherited check preserves its historical
5,773-artifact count; the read-path inventory uses unique paths and has a
different count.

The broad initial filesystem scan was stopped because it traversed unrelated
historical material. The final baseline was instead captured from the actual
successful preservation checks. No prior file was deleted or modified.

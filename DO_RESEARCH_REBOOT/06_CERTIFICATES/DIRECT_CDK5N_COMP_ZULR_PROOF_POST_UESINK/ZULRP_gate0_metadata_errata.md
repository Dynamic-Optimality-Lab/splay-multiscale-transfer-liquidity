# Proof-stage errata (append-only; Gate-0 files untouched)

## Erratum A — Malformed entry checkpoint (CONFIRMED, nonoperative)

`UESINK_source_hashes.json` field `checkpoint` and `UESINK_terminal_status.json`
field `entry_head` record `6bf87814bbdd4d0a47dbd024c79abdaf0cef7b91`
(64 hex chars but NOT a real commit). Genuine DLSS checkpoint verified from
Git: `6bf8781c129122b4e69cd4409316c280351f16a0`, which is the recorded parent
of the UESINK-G0 commit `f902c36` (ancestry verified). Correction: read
`6bf8781…` wherever the typo appears. No evidence depended on the typo string.

## Erratum B — Generation vs screening vs manifest counts (ADJUDICATED)

Ground truth from committed state files: `parents_L1.txt` holds 425 distinct
lines (0 internal dups); op split 16 rm + 128 rep + 281 ins; raw grammar
output 441 (16+128+297) with 16 insertion collisions beside existing
identical DELETEs. `seen.txt` holds the same 425 hashes. `census.json`:
tested 5, closed 3, distinct 425, hopeful 1. Screening stopped after idx4
(rm7/OUT); the remaining 420 registered candidates were never replayed.
R3 adjudication: the freeze/screening stop rule governs screening and
selection, which complied (first qualifying OUT frozen; no later candidate
evaluated; order preserved). Pre-generating the deterministic parent list
(identity registration) before screening did not affect selection: the OUT
is first-qualifying in global canonical order (re-verified with exact
canonical-word equality — see Erratum C). No later information exists to
have influenced the freeze.
CORRECTION to Gate-0 manifest: `ZULR_search_manifest.md` claims "442
distinct parents (459 raw − 17 collisions)" — WRONG (DLSS-turn numbers
bled into the text). Correct: 441 raw → 425 distinct (16 collisions).
Terminal/census/state files already record 425/5 correctly; only the
manifest prose is affected. Verdicts unaffected (counts are bookkeeping,
not selection criteria).

## Erratum C — Hash-only deduplication (ADJUDICATED, no error found)

The committed search used SHA-256 `seen` sets, not canonical-content sets.
Independent re-enumeration with exact canonical-string equality reproduces
the identical 425-word order, identical first five (rm0,rm1,rm2,rm5,rm7),
and identical OUT selection at idx4; the 16 collisions are true duplicate
words (same canonical content from adjacent identical-DELETE insertions),
not hash collisions. No omission, no misordering, no effect on selection.
Recorded as implementation deviation without operative consequence (the
governing protocol's exact-identity requirement is satisfied by equivalence
on the executed frontier, not by code inspection alone).

## Erratum D — Budget guards (ADJUDICATED, nonoperative)

Committed code declares CAP_SEED=60000/CAP_TOTAL=300000. Per-seed guard
exists in the generation loop (untriggered — no `truncated` flag in state).
Total-cap guard is absent from the code. Actual consumption: 425 registered
(<60k), 5 screened; no truncation occurred and no candidate was skipped for
budget reasons. The missing total guard is a latent defect with zero
operative effect on this run. Not silently certified: stated here explicitly.

## Erratum E — Bank grouping arithmetic (CONFIRMED, summary-only)

Gate-0 `ZULR_banked_inventory.md` writes "Count: 3+10+10 = 23". The listed
content is 3 core (RT2/CDK4/CDK5L) + 8 nine-core (NP/S1/S2/VR/MR/MSINK/DLSS/
UESINK) + 7 AJ–AN + 5 AO–AS = 3+8+12 = 23 mechanisms. Only the summary
grouping is wrong; the mechanism set (23) is correct and complete
(reconciled against 02_PROVED/ledger/certs; AE/AF/AG/AH/U1/CWC are
obstructions/audits, not coverage). Proof-stage inventory uses 3+8+12.

## Erratum F — Adversarial evidence classification (CONFIRMED, addressed)

Gate-0 `ZULR_adversarial_results.json`: 90 records, 90/90 PASS, with kinds
41 exec / 1 exec+proof / 48 proof. The terminal "90/90 PASS" is therefore a
mixed audit result (41 executed falsification checks + 49
mathematical/documentary arguments), not 90 independent executions.
Proof-stage audit (§19-style: 80 challenges) labels every check
EXECUTABLE / MATHEMATICAL / DOCUMENTARY / HYBRID, executes the executable
class with real assertions (±O), and adds fault injections exercising
rejection paths. No hardcoded True counts as an executed test.

## Erratum G — No cross-interval sink (CONFIRMED, Gate-0 L-doc audited)

ZULR self-pays: IN has w_0=1, R_0=34, i.e. 1≤34 — NOT a joint sink
inequality. The Gate-0 L-doc's joint-inequality framing is checked here for
imported UESINK-style expressions (1+w_p≤R_p); none affect the payment
steps (verified textually: every step uses per-interval w≤R only). No
exception packet, borrowing, or shared sink anywhere in the mechanism.

## Erratum H — Hypothesis redundancy (CONFIRMED, retained)

H3 (exactly one untyped positive) already classifies all other positives,
making H5 a restatement; an E-exception (w=1,¬K,¬P,H=1) cannot coexist with
H3-uniqueness + H4 (H≥2). Hence H2 is implied by H3+H4 under source
definitions. Redundant but RETAINED: the proof checks H2/H5 explicitly, and
no generalization (multi-payer, H3-free) is claimed. Recorded as a future
research note only.

## Erratum I — Directive §8 OUT canon transcription (proof-stage record)

The directive's §8 OUT canon string carries one extra D8 (32 tokens) while
its SHA (`8cd970c7…`), n=31, A=53, provenance (rm7), and Gate-0 record all
identify the 31-token word. Authoritative OUT = the SHA-pinned 31-token
word (re-gated this stage). The printed string is a transcription error
with no operative effect (no code path consumed it).

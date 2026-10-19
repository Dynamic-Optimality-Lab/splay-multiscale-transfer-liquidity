# CL-01 Resource Forensics (additive erratum to SR-02C ledger)

Measured SR-02C process CPU from embedded cpu_s (disjoint processes):
base-rates 426.1 + counterexample-hunt 49.1 + conjunct-bisect 26.4 +
guard01 screens ~39 + verifiers/misc ~15 = ~555.7s. The committed 340s
figure was an early estimate written before the base-rates/hunt runs;
it is SUPERSEDED (not erased) by this erratum. Allowance was 236s:
OVERRUN ~320s, DOCUMENTED as unauthorized excess (no approval sought;
cause: decisive refutation required full-state capture runs). Hard caps
respected: Step-03 total ~3.10h/3.5h; campaign ~4.9h/12h; 1.8h reserve
untouched. CL01-05 gate: substep FAIL (overrun), hard-cap PASS.
CL-01 budget: arithmetic + reads only (~60s CPU); no solver/Z3/ssertify
runs authorized in CL-01 (ledger headroom exists but allocation is
diagnostic-only by this prompt's prioritization).

import hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EVID = {
 "LIQ0-02": "Layer A math/proofs/LIQ0-02.md; Layer B lean/Liquidity/Multiplicity.lean (machine-checked); Layer C ACT-10 corpus (sum mu = depth) + rotation-shape coverage.",
 "LIQ0-03": "Layer A math/proofs/LIQ0-03.md; Layer B determinism definitional (pure functions) + ACT-07 rerun-hash; Layer C ACT-08 differential.",
 "LIQ0-04": "Layer A math/proofs/LIQ0-04.md; Layer B lean/Liquidity/Activation.lean t5rho skeleton (bounded range); Layer C ACT-04 counts + partial behavior.",
 "LIQ0-05": "Layer A math/proofs/LIQ0-05.md; Layer B Activation.lean t5one_energy + t5rho_energy (machine-checked); Layer C ACT-05 conservation + ACT-08.",
 "LIQ0-06": "Layer A math/proofs/LIQ0-06.md; Layer B Preservation.lean supports_preserved (machine-checked); Layer C ACT-06.",
 "LIQ0-07": "Layer A math/proofs/LIQ0-07.md; Layer B Preservation.lean spent_never_decreases_aux + firstEligible_mem (machine-checked); Layer C ACT-06 + M10 killed.",
 "LIQ0-08": "Layer A math/proofs/LIQ0-08.md; Layer B capacity signature audit (no forbidden inputs); Layer C ACT-03 AST audit + M03-M06 killed.",
 "LIQ0-09": "Layer A math/proofs/LIQ0-09.md (definitional accounting); Layer C ACT-09 schema + diagnostics; no formal content beyond definitions.",
 "LIQ0-10": "Layer A math/proofs/LIQ0-10.md; Layer C ACT-03 audit + frozen prereg hashes; uniformity by construction.",
}
for tid, ev in EVID.items():
    thm = (ROOT / "math" / "theorems" / ("%s.md" % tid)).read_text(encoding="utf-8")
    (ROOT / "math" / "reviews" / ("%s.PACKAGE.md" % tid)).write_text(
        "# %s Review Package - PENDING-HUMAN (no verdict inferred or generated)\n\n## Statement\n%s\n## Negation\nSee theorem file.\n\n## Evidence\n%s\n\n## Review instructions\nACCEPT only if statement bytes match the frozen theorem file and evidence artifacts verify. REJECT = package rejected (truth stays UNPROVED), never refutation. Verdict solely in %s.review.json by a human.\n\n## Verdict: PENDING-HUMAN\n" % (tid, thm, ev, tid),
        encoding="utf-8")
print("WP-2 STEP 65: 9 review packages written")

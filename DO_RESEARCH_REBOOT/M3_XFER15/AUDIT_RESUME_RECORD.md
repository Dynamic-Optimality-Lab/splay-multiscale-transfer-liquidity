# Audit interruption: Windows long-path dependency lookup

The first bounded audit stopped with AssertionError at audit.py line137,
`assert p.exists()`, inside the dependency-file loop. The ten short
dependency paths exist. The final LDR01 theorem path exceeds Windows'
legacy unprefixed path length; pathlib's unprefixed existence lookup
returned false. PowerShell and the inherited long-path metadata helpers
resolve that SAME file. This is a provenance-path implementation error,
not a mathematical counterexample or a PASS for the failed audit.

The first run's status remains FAILED_OR_UNKNOWN_STOP. Its source,
traceback, CPU exits and logs are immutable. They show execution reached
line137 AFTER all12 universal constructor checks, path/price arithmetic,
signed coefficient identities, old source hashes and source AST assertions
passed. There is no exception handler or bypass in that prefix, and the
triggered assert confirms assertions were enabled. A continuation can
reuse that completed prefix without re-executing it.

resume_audit.py therefore checks the failed-run evidence and source hash,
records the successful prefix, and resumes the UNFINISHED dependency and
profile-coverage work with the Windows extended-path prefix. It does not
import or execute audit.py, rerun its constructor/algebra/source checks,
query a psi table, or evaluate an original transition. The merged final
audit can be PASS only if this continuation also passes. It explicitly
retains the failed component and its cost; no UNKNOWN is promoted.

First child charge0.234375 plus controller-through-finally0.21875 gives
0.453125 CPU seconds. Prior761.171875 becomes761.625. The continuation
gets at most119.546875 child CPU seconds, retaining the combined120
symbolic ceiling and all other original caps/reserve. The final ledger
adds both attempts. This is a repair within the same bounded audit and
same theorem; no new proof route, observable, potential or cap is added.

# Preservation checker scope and a historical manifest mismatch

The first checker broadened validation to every historical
Route C manifest. It stopped before writing outputs on an
old mismatch in route_c_analytic_20261030_v001:
the manifest's entry_source_pins.json hash differs from that
file's frozen current hash. The current file matches the
PRIOR CG entry baseline exactly. This is not a change made
by this turn. Neither historical file is edited or repaired.

Preserve the failed checker. Use check_preservation_v002.py.
It verifies every inherited raw file against the prior entry
baseline, including all528 Stage11G files against CG's complete
inventory, and explicitly validates the frozen FE01/PG02/FE02
delivery manifests. It records the old mismatch and its
pre-existing-baseline evidence separately. It does not claim
all legacy manifests are internally consistent.

This limits the manifest-consistency claim, not preservation:
every one of1605 inherited raw file hashes is unchanged.
No historical report, certificate, source or Git file is
modified. This note supersedes only RR01's checker invocation;
the mathematical gate still failed and FE02 remains OPEN.

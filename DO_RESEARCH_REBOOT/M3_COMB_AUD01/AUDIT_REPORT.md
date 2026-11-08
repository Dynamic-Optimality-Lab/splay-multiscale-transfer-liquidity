# Combined M3 certificate — independent audit

2026-10-29, Asia/Karachi.

**Audit completed. The restricted certificate passes; a full M3 certificate
is INCOMPLETE. M3 remains OPEN.** No negative original mixed cycle is
certified. There is no promotion to Stage04, Bank25 or Dynamic Optimality.

The actual missing branch is

    support(sigma)>=2, N_H>=1, D_L>2*N_H+P_L,

inside either chi8 region. The combined potential is undefined on certified
legal states with sigma=(1,1,0,...,0). This is a coverage failure of the
submitted certificate, not a counterexample to the M3 sign theorem.

## Combined certificate and complete coverage partition

The assembled candidate is in COMBINED_CERTIFICATE.json. candidate.py is a
new independent decoder for its tables and shared-state potential. Its
declared domain is every legal five-bit mask and sigma with at most one
positive component, any gap0..9 and population through266. There are2661
such signature vectors and335286 mask/signature sectors.

The ordinary potential uses the five independently audited low tables:
gaps0/9 use GAP01;1/8 use GAPINT01;2/7 use GAPINT02;3/6 use GAPINT03;4/5
use GAPINT04. Zero support uses GAP01. Reflection applies to mathematical
low core/A profiles only. Mu and sigma are preserved on the original legs,
so this static dispatch does not require compatibility between sectors.

For J in[-2,0], the assembled original two-sort certificate is

    W(O)=J(O)-5*chi8(O.b),   W(M)=-5*chi8(M.b).

Low conservation makes Delta W=Delta J. Within either region an OM high
leg pays at least2, while Delta W=-J(source)<=2. An entering high leg has
Delta W=-5-J(source)<=-3<=w. A leaving high leg is impossible. Every MO
leg preserves chi8 and has Delta W=J(destination)<=0, matching its zero
weight. The same actual midpoint is used; independent private OM/MO
witnesses are allowed. Thus the declared domain has w>=Delta W on every
leg, W in[-7,0], global finite-walk weight>=-7 and closed-walk weight>=0.
Within the outside induced graph the J bound is the sharper -2.

For arbitrary signatures, the separately proved universal high toll gives

    weight(C)>=2*N_H+P_L-D_L

on every closed mixed walk. The exhaustive logical partition is:

| Signature / cycle condition | Audit disposition |
|---|---|
| At most one positive gap component | Restricted signed certificate passes |
| Multiple positive gaps and D_L<=2*N_H+P_L | Signed counting theorem applies |
| Multiple positive gaps and D_L>2*N_H+P_L | OPEN in both chi8 regions |

An arithmetic case N_H=1,P_L=0,D_L=3 leaves the supplied lower bound at-1.
This illustrates why that inequality alone cannot discharge the last
branch; it does not assert that an actual walk has these statistics.

Both original witnesses in GAPMULTI01 were freshly reevaluated TRUE.
Their complete source AND destination states agree, but the hidden core
bills are ([],[0,1]) versus ([0],[1]). The assembled potential rejects
their shared signature. The pair rules out the literal deterministic
port-completion extension, not every possible potential or M3. No further
proof deleting the hard-deficit multi-gap branch is present.

## Independent finite verification

The checker does not import a campaign's build/verification functions.
It enumerates full ordered BSTs independently, filters the retained
anonymous-node corpus, and uses a new mutable parent-map bottom-up splay
implementation. It regenerates all A-profile transition sets, B splays,
terminal source credits and graph rows. It also independently rebuilds
the negative core DAG:4862 core trees,43758 accesses,4224 negative edges,
acyclic, with debt maximum2 and histogram4223/556/83 at0/1/2.

| Canonical gap | A models regenerated | Stored rows independently checked |
|---|---:|---:|
| 0 | 48,450 | 4,089,363 |
| 1 | 72,214 | 4,217,313 |
| 2 | 77,570 | 3,957,645 |
| 3 | 79,726 | 3,556,717 |
| 4 | 80,570 | 3,352,967 |
| Total | 358,530 | 19,174,005 |

Every stored integer residual is nonnegative, minimum0. Every value lies
in[-2,0] and below the independently computed destination debt floor.
Every analytic range/debt omission is checked and counted, including
the weight1/debt>=1 and weight0/debt2 cases. No row thinning or hidden
graph storage is used. The full16842 retained fringe kernel is rebuilt;
the special terminal-core0 and entry-root credit maxima are2 and1.
Core debt/reflection and the Gamma0 terminal debt condition are checked
on every core access. The five graphs are processed separately.

The finite result is complete for the stated finite proof corpora. It
does not enumerate all original private witnesses. Universal lifting
still uses the written source proofs: H1 fusion, charge/change injection,
Gamma0 terminal debt, the Gamma1 two-access normal form, population-
opaque shared S completion, S-empty alias erasure and the at-most-three
protected anonymous classification. Those dependencies were reviewed;
this is not a proof-assistant formalization of those inductions. The old
fourth-node census is an inherited cross-check, not the source of the
universal bound and not a substitute for that argument.

## Original transitions and projected graph semantics

Fresh production-DAG evaluation independently regenerated all11340
dirty-source identities for d10..18. All force an incoming real claim on
the final root, excluding those invalid endpoints. All171 chi8 boundary
cases also pass:54 preserve chi8 and117 force invalid root claims. The
clean last-write property is verified for all9 real targets with arbitrary
pre-final fields. Source classification retains all selected-claimant
orientations, arbitrary lower claimants, literal-slot0 ON/OFF cases and
unfixed off-spine source fields. The complete source proof, rather than a
single-phantom diagnostic, supplies coverage. High never receives low's
root-termination or no-repeat requirements.

An independent primitive check verifies every one of115 B coordinates
for408 ordered core rotation cases, plus3570 symbolic maximum-pair
identities allowing real internal gap labels. These connect the reference
low splay to the original rotation wiring and low chi8 conservation.

The frozen weighted Product was freshly built:1603124 DAG nodes, below
the4m cap. All22 original sort/weight projections were traversed using
an independent lexical free-variable checker. No private witness escapes
its sort interface. The actual interface has147 O coordinates and127 M
coordinates. Three actual projected membership checks pass: a negative
low edge, the genuine h0,d18,weight-3 OM edge, and its zero-weight MO leg
using the same actual midpoint. The original target/fiber-root distinction
is preserved, not collapsed into one key.

Separately,240 complete original roots were freshly evaluated under total
bounded assignments:129 valid LOW,39 valid HIGH and72 rejected dirty cheap
HIGH candidates. Rejected high candidates have independently valid sources
and verified source paths; they fail at the final endpoint. All actual
q and exact weights are read from original variables and checked, including
macro H charges, last terminal B depth,6-q high weight and zero MO weight.
None of the72 rejected candidates is treated as an original edge.

The h0 anomaly retains root8 while changing child fields; it remains valid.
Sixteen accepted high examples have fiber label v different from actual
B target/root, confirming that the audit does not impose synchronization
absent from the original high relation. Large inventories, opaque ports,
whole macros, dangling A refs127/255 and multi-gap high profiles remain
in the controls.

## Full-state closure and potential decoding

The audit extracts the ordinary and midpoint interfaces directly from
the total original environments, then compares them with saved records.
Every ordinary equality includes mu, all10 signature coordinates, all7
raw alpha triples, B root, all four child arrays and every lo/hi value.
Every midpoint includes its own full B, mu, sigma and fiber label v.
Structural b_equal is not silently strengthened to full B equality;
actual midpoint sharing and actual ordinary closure are checked separately.

Eleven mixed closed walks match in all raw coordinates, with the actual
midpoint shared between the OM/MO legs. Changing either a raw lo coordinate
or an otherwise unused alpha kind is detected by the closure checker.
These are eleven source-valid closure controls, not an enumeration or
absence proof for every mixed cycle. Arbitrary lengths and repeated
coordinates in the proved domain are handled by the pointwise inequality
and telescoping on the real shared states.

The new independent potential decoder checks161 accepted original records
in its declared signature domain:127 LOW and34 HIGH. Every actual low
source/destination finds its finite image, with no fallback. High-only
boundary shapes may receive the specified zero J fallback; all OM/MO
inequalities still pass. The five multi-gap high controls validate the
universal high law separately. The two multi-gap low controls correctly
remain outside this potential's domain. All66 discrete region/range
combinations in the global glue also pass.

## Dependencies, corrections and limits

dependency_ledger.json is acyclic and contains an explicit OPEN leaf for
the multi-gap hard-deficit obligation. No M1 cycle sign or full M3 result
is assumed to prove the low source reductions. The withdrawn initial
ACL01 promotion is not a mathematical premise; its AER01 erasure repair
is. The rejected B-only cycle and old capped-potential failures are not
used as original negative-cycle certificates or as sign premises. Legacy
implementation imports are distinguished from active mathematical claims.

The interior-gap statement Gamma_pre=0 is scoped to gaps1..8, where BOTH
outer gaps are absent. It must not be generalized merely from sigma0=0:
gap9 uses the reflected Gamma1 kernel. This distinction is enforced by
the assembled dispatch. Reflection is mathematical low symmetry; neither
raw high max scans nor weak private LE inventory predicates are reflected.

Two independent audit prototypes were corrected without editing old
research: the initial recursive reference paired rotations from the root
at odd depths, and the initial projected-witness renaming also matched
private auxiliary prefixes. The active reference uses target-first
parent-map pairs; the active projection harness renames exact state
namespaces only. Their failed runs are preserved. They do not refute a
production identity. Authoritative entry points are reference_v2.py,
finite_audit_v2.py and projected_product_audit_v2.py.

All444 entry research files are checked unchanged. Recursive historical
manifest checking finds333 distinct pinned files, with no hash mismatch or
conflicting pins. Tracked source and branch/HEAD remain unchanged. Each
registered phase stays below its CPU/DAG/state/edge limits; no solver,
installation, fit, graph modification or cap increase is introduced.

BEFORE: restricted low tables and high lemmas existed, with multi-gap
coverage explicitly open. RESULT: independent finite, source, projection,
closure and dependency audits pass within their stated scopes. AFTER:
the combined restricted certificate is independently reviewable; full M3
still has an OPEN branch. NET NEW SIGN-THEOREM ADVANCEMENT:0 from this audit.
The audit removes verification uncertainty, not the missing multi-gap sign
obligation. R1–R4, original source q/weights/O-M sharing, depth2/T266,
h0 correction and Bank25=25 remain preserved.

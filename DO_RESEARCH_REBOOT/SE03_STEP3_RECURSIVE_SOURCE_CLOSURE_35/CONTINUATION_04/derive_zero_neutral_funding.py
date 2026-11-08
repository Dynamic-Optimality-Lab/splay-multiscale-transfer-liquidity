"""Source-uniform restricted derivation; no new source executions."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent
B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    text=r"""# JR35-N0 — full source funding when every B double decreases Psi

Status: uniform RESTRICTED mathematical derivation. This is not universal
JR35, UCF35, reservation compatibility, Gate U closure, or Universal CD.
The accepted CSL35/ND35 physical controls support their implementations;
they do not replace the proof below.

## Frozen IAGS Box

Target: full original comparison h extending the literal natural h0,
with an original static-block working bank at most2.
Conditions: original finite exactly paired-closed source; arbitrary
genuine support r>=7, arbitrary BF core and private A/B populations;
EVERY original BF double decreases the source-defined Psi of ND35.
Inheritance: fixed BF carrier S, exact ordinary rotation formulas,
ND35 fine-step law and actual donor construction, C14 disjoint actual
packet license, selected-bit streaming, original absolute-period transport.
Ambiguities: a neutral BF double is outside THIS restricted theorem.
Additional fE locks/reservation chi are the later separate interface.
Bridge: prove the source sign per natural macro, group at equal actual
minimum-Psi boundaries, then apply the inherited block constructor.

## 1. Uniform local source law

Let Psi=|J_S(BF)\J_S(A)| on the actual full trees. Within a natural macro e
write P_e,N_e for A +/- rotations, B1_e,B2_e for BF doubles decreasing Psi
by1/2, and Z1_e for decreasing BF terminal zigs. A double contributes
two real bits; an A zig contributes two real bits although one rotation.
Thus P_e<=2H_e. The no-neutral hypothesis gives

    DeltaPsi_e=P_e-N_e-B1_e-2B2_e-Z1_e,
    Q_e=B1_e+B2_e,
    2H_e-Q_e-DeltaPsi_e
        =(2H_e-P_e)+N_e+B2_e+Z1_e >=0.             (*)

This derives a sign on EVERY original macro from source rotations.
It does not assume the desired total inequality or a global matching.
All helpers, root-repeat/nongenuine KEEPs and terminal A-zero accesses
remain in the actual macro and in H_e. There are no discarded operations.

## 2. Source-defined grouping, rather than bounded carry

On the given actual closed period compute Psi at every genuine full
natural boundary. Select ALL boundaries attaining its minimum m.
Consecutive selected boundaries in cyclic order delimit disjoint groups
of WHOLE original macros. This rule is specified from the source states,
not from a presumed feasible matching. It may have unbounded lookback
and may yield a single group; no constant-width/lookback is asserted.

Each group has Psi_start=Psi_end=m. Sum (*) only over its actual macros:

    2H_group-Q_group >=0.

This is a proved local grouped-source budget. It is not an assumption of
CD on the source period. No individual macro's shortage is suppressed:
the exact telescoping equality retains all its original demands and bits.
Equivalently the specified grouped Type-B license has D=0 and c=H_group.
Select ALL2H_group original bits, which includes every unchanged h0 bit
because each natural h0 assignment is wholly within its own macro.
The source arithmetic and packet rule are independent of fE/CD(r).

## 3. Physical construction and Bank25

Apply STREAMED_BLOCK_THEOREM.md to each disjoint group with b_s=b_t=K=0.
Emit each fixed h0 pair at its actual donor-record visit. For each other
original double demand, in its original demand order, advance the actual
A-event record stream only when the free queue is empty; use the next
unowned unit. Release excess only after all missing demands are paid.
The proved budget above prevents exhaustion. At most two physical units
are simultaneously unassigned in this construction. Every input bit is
assigned once or released once. Every original BF double is paid once.
Different groups have disjoint physical inventories and demand IDs.
Hence h is a full injection extending the literal h0, working<=2<=25.

This uses the inherited OFFLINE STATIC WITHIN-BLOCK license: a donor may
follow its demand within its certified group. It does not assert online
physical endpoint availability or a license under an additional frozen
reservation policy. No assigned unit is stored as an uncounted free IOU.
The grouping supplies independently proved source budgets, as required
by C14; merely observing a matching or a nonnegative total would not.

An independent existence construction is ND35's explicit g_plus on all
demands (there are no neutral terminals). Alternate g_plus with h0 from
each h0-unmatched start. Injectivity makes the finite paths disjoint,
and every endpoint is an actual h0-unowned bit. Keep h0 and assign these
distinct endpoints to the starts. The block-streamed h need not equal
this alternative comparison. No historical map is rewritten by either.

## 4. Absolute period, reflection and arbitrary lifting

A selected minimum boundary is only an INTERNAL full-comparison proof
cut. It does not change the separately frozen legal Step1 maximum cut.
Use the accepted C14 both-endpoint cyclic occurrence bijection to put
every donor AND demand on the original aligned interval I. The bijection
also transports h0 and all selected groups; no bit is taken from another
copy. A group wrapping I's seam denotes those actual IDs, not a second
inventory. Full A/B and recurrent BE/chart endpoints are unchanged.

The proof uses actual S-label sets, including anonymous A unary
duplicates through SET membership, and the original full A events.
No finite population or fixed support table occurs. All B cores and
arbitrary finite helper words are included. Order reversal preserves
subtree-label membership, every fine DeltaPsi, original costs, h0
ordinals and the stream construction. Thus the reflected class follows
by the actual source isomorphism, not an analogy.

## 5. Exact consequence and remaining root obligation

JR35-N0 proves an independent full comparison and its original Bank25
trace for the declared no-neutral class, at arbitrary support. It is a
source-derived new sufficient funding rule, not the universal theorem.
The raw count Q<=2A follows by counting the constructed injection.
Reservation/frozen-fE compatibility must still use its own original
exchange license; the user requested that task only after universal JR35.

The accepted CCR and AF sources HAVE neutral doubles and are not covered.
For arbitrary sources, ND35's unmatched neutral-demand terminals still
need distinct eligible physical endpoints, global noncollision, and a
licensed Bank25 schedule. Neither (*) nor the level-crossing matching
proves that missing theorem. Universal JR35 remains OPEN.
"""
    (F/'ZERO_NEUTRAL_FULL_SOURCE_FUNDING.md').write_text(text,encoding='utf-8')
    pins=[
      F/'NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md',
      F/'ND35_CSL35_PROOF_REVIEW.md',
      F/'independent_core_sector_neutral.json',
      B/'STREAMED_BLOCK_THEOREM.md',
      F.parents[1]/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
      F.parents[1]/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md']
    result={'status':'RESTRICTED_UNIFORM_DERIVATION_JR35_N0','source_queries':0,
      'source_engine_calls':0,'input_sha256':{str(p.relative_to(F.parents[1])):sha(p) for p in pins},
      'output_sha256':sha(F/'ZERO_NEUTRAL_FULL_SOURCE_FUNDING.md'),
      'physical_working_bound':2,'neutral_doubles_allowed':False,
      'arbitrary_support_and_private_populations':True,'JR35':'OPEN',
      'reservation_compatibility':'DEFERRED','independent_review':'PENDING'}
    with (F/'zero_neutral_funding_derivation.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)

"""Publication/byte-provenance metadata only. No source engine or new test."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;C27=B.parent;P=C27.parent;ROOT=P.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def jout(n,s):write(n,json.dumps(s,indent=2))
def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
def texttree(t):return str(t) if not isinstance(t,list) else str(t[0])+'('+texttree(t[1])+','+texttree(t[2])+')'
def tokens(w):return ' '.join(m+str(k) for m,k in w)
def rows_table(head,rows):return '| '+' | '.join(head)+' |\n|'+ '|'.join('---' for _ in head)+'|\n'+''.join('| '+' | '.join(str(v) for v in row)+' |\n' for row in rows)
cert=read(B/'aligned_source_and_owners.json');audit=read(B/'independent_audit2.json');entry=read(B/'entry.json');candidate=read(B/'construction_candidate.json');tags=cert['tags']
assert audit['status']=='PASS_DISTINCT_IMPLEMENTATION_EXACT_EXISTENTIAL_WITNESS'
assert audit['input_sha256'][(B/'aligned_source_and_owners.json').relative_to(ROOT).as_posix()]==sha(B/'aligned_source_and_owners.json')
assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head'] and not git('status','--porcelain','--untracked-files=no')
pins=read(B/'dependency_pins.json')
for z in pins['pins']:assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in pins['external_pins']:assert sha(Path(z['path']))==z['sha256'],z['path']
phases=[];global_used=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=0
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);c=read(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+c['whole_process_CPU_seconds'];global_used+=charge;groups[r['group']]+=charge;queries+=r['source_queries']
    phases.append({**r,'controller_CPU':c['whole_process_CPU_seconds'],'total_charge':charge})
resources={'status':'CUMULATIVE_NO_RESET','authorization':entry['authorization'],'prior_global_CPU':entry['prior_uniform_CPU'],
    'cumulative_CPU':global_used,'global_cap':7200,'global_remaining':7200-global_used,'global_reserve':5,'controller_reserve':1,
    'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],'group_remaining':{g:entry['group_caps'][g]-v for g,v in groups.items()},
    'all_rejected_or_failed_phases_charged':True,'phases':phases,'new_source_queries':queries,'source_query_limit':2000000,
    'query_note':'Conservatively also keep the sum of all new continuation queries below2M; prior C15-C27 engine calls21881 remain recorded, not reset.',
    'inherited_C15_C27_engine_calls':21881,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,
    'memory_cap_bytes':32*1024**3,'wall_limit_hours':12,'Bank25':25,'source_search_complete':False,
    'inherited_local_pins_rechecked':len(pins['pins']),'metadata_CPU_convention':'Byte/Git/JSON publication excluded under inherited convention and separately measured; no source semantics executed here.'}
assert queries<2000000 and global_used<7200 and all(groups[g]<entry['group_caps'][g] for g in groups)
meta='''Status: exact Campaign27 existential witness; distinct implementation audit PASS.
This is a computer-assisted exact finite construction, sufficient for the stated
existence theorem. It is not a universal funding proof. The second implementation
was operated by the same research agent, not an external reviewer or proof assistant.
Historical pending universal claims retain their existing status.
'''
sourcehash=sha(B/'aligned_source_and_owners.json');audithash=sha(B/'independent_audit2.json')
by={r['occurrence']:r for r in cert['rows']}
crit=[]
for k in ('j','h','g','s','t','v','p','e'):
    r=by[tags[k]];crit.append([k,tags[k],r['target'],r['A_path'] or 'root',r['a'],r['BF_path'] or 'root',r['qF'],r['BE_path'] or 'root',r['qE']])
crit_table=rows_table(['name','absolute t','key','A path','a_t','BF path','qF','BE path','qE'],crit)
bank_table=rows_table(['packet','H/QE','D before→after','new payments','carry, newest first'],[[k,str(z['H'])+'/'+str(z['Q']),str(z['D_before'])+'→'+str(z['D_after']),z['new_pairs'],z['carry']] for k in ('v','p','e') for z in cert['h6_packet_receipts'] if tags[k] in z['occurrences']])
stage_table=rows_table(['effective stage','prior paid','new successes','paid after','blocked roots'],[[z['name'],len(z['prior']),len(z['additions']),len(z['after']),len(z['blocked'])] for z in cert['policy_stages']])
guard_rows=[
['S1','K-support={1,3,5,7,9,11,13}; every full B core is exactly all13 physical keys; original all-SS hard-unary R-frame.','PASS'],
['S2','j..e are consecutive original genuine macros; complete 199 operations retained.','PASS'],
['S3','erase11; actual retained-root return epsilon1, qE(v)=qE(p)=1.','PASS'],
['S4','u_v=(769,1,1); post-p rank2 and L_p=2.','PASS'],
['S5','e at771 has A H1, BE depth8/Q4; first raw payment of u_v is e4.','PASS'],
['S6','(662,2), key9 → (771,1); (695,2), key5 → (771,2); both selected after every creator payment.','PASS'],
['S7','Full actual A prefix/period and rotations independently replayed; signed R-flip correction included.','PASS'],
['S8','Full B processes every original KEEP, including identities, and closes.','PASS'],
['S9','BE is generated from the same source by skipping only KEEP11; physical key11 remains; core9 and closure checked.','PASS'],
['S10','Applicable canonical f6 branch and literal full common/natural, leaf, creator, T19, own-tail and later successes rebuilt. Original special Step1 core9 scope not extended to smaller five-key cores.','PASS'],
['S11','A, BF and BE end trees equal their own initial trees exactly.','PASS'],
['S12','Actual I=[573,771], cut after body141; maximum debt2; every assigned demand/bit lies in I.','PASS'],
['S13','R1–R4 and old bytes/owners unchanged; raw bank10, f6 endpoint buffer4, full endpoint buffer6≤Bank25.','PASS']]
guard_table=rows_table(['guard','witness receipt','status'],guard_rows)
write('SOURCE_SPEC.md',f'''# Frozen source and theorem

{meta}
Repository `{ROOT.as_posix()}`; branch `{entry['branch']}`;
HEAD `{entry['head']}`; tracked tree clean. Actual local inputs were used.
The immutable original C27 target is `../N26_E4_FROZEN_GUARDS.md`.
The request to continue C27 and the later explicit 240/600 cap authorization
do not alter its source or guard conjunction.

THEOREM C27-EXISTS: there exists one original reachable, exactly paired-closed
seven-genuine-KEEP-key/core13 history W* satisfying every N26.E4 guard S1–S13.
Here G=1, x=7, C=11, R=13; the displayed order is key order.
The erased comparison retains six marked KEEP keys E={{1,3,5,7,9,13}}.

All physical trees have the same ordered key universe1..13. A processes
every KEEP and DELETE using ordinary bottom-up splay. BF processes every
KEEP; BE processes exactly the KEEPs other than11. DELETE is A-only;
erasure does not remove physical keys. a_t=ceil(depthA/2), q_t=floor(depthB/2).
Actual units(t,j,b), b0/1, and demand IDs(t,k) retain absolute occurrences.
Genuine macro boundaries are nonroot KEEP endpoints; processed root-repeat
KEEPS remain in the source and contribute their actual costs.

No private-population lifting theorem is needed for existential construction:
this particular permissible13-key source is the witness. No universal claim
about adding private nodes or other supports follows.

R1 exact source/target/closure; R2 real weighted costs, shared states and
physical IDs; R3 frozen owners, historical code/graphs/controllers and all
unchanged caps except the TWO explicitly authorized increases; R4 exact
proof/status distinctions. See original C14 SOURCE_SPEC.md for inherited R1–R4.
''')
write('SOURCE_INTEGRITY.md',f'''# Source provenance and preservation

{meta}
Branch `{entry['branch']}`, HEAD `{entry['head']}`; no tracked edits,
commit, push, reset, cleanup or destructive operation. All historical
untracked work is retained. New proof work is in CONTINUATION_01; the new
parent `LATEST_CONTINUATION.md` only points to it. Initial C27's unresolved
artifacts remain intact as historical snapshots, not the latest verdict.

All {len(pins['pins'])} inherited local pins and all inherited external
directive pins match at publication. `dependency_pins.json` records their
exact paths/hashes. C27 root `dependency_ledger.json` preserves inspected
source/dependency statuses. Content pins establish provenance, not truth.

Authoritative new source/owner receipt SHA256 `{sourcehash}`.
Distinct implementation receipt SHA256 `{audithash}`.
Accepted Step1/CD6 proof artifacts, old owners, event semantics and graph
files are unchanged. Prior audit-pending universal theorems remain pending.
No remote snapshot replaced newer local source.
''')
write('C26_INHERITANCE_LEDGER.md',f'''# Exact inherited interfaces

{meta}
All paths below are relative to DO_RESEARCH_REBOOT. Full hashes are in
`dependency_pins.json`; previously inspected-proof annotations are retained
in the original C27 dependency ledger.

| Source | Exact use | Status retained |
|---|---|---|
| SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/CHECKPOINT.md | Authoritative N26.E4 conjunction | Original OPEN question; now decided by one witness |
| C26 RV_RETENTION_FIRST_CONSUMER.md; RV_EFFECTIVE_OWNER_CERTIFICATE.md | Rank/consumer/owner questions | Universal manuscript labels unchanged; this instance independently rebuilt |
| SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/BIRTH_GROUP_REDUCTION.md | T19 selected zero-to-next-birth comparison | Original audit scope unchanged; actual lifetimes independently rebuilt |
| SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/audit_marked.py | Watched-edge/source creator and LAST-tail policy specification | Reimplemented on this exact source, not a new universal audit |
| SE03_STEP3_EXTREME_OWNER_RECURSION_22/CREATOR_POLICY_COMPATIBILITY.md | Every-producer creator spending, first own-tail, protected j ordinal3 | Instantiated and checked; no arbitrary-support promotion |
| SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/FINAL_VERDICT.md | Signed shadow correction, not identity surplus | Actual omitted block/shadow rejoin independently checked |
| SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24 | Literal frozen-success contract | Every old effective value kept in all new stages |
| SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/T19_ARRIVAL_LOCALIZATION.md | Two arrivals must be e1/e2/e3 from beforej | Actual pair e1/e2 constructed |
| SE03_STEP1_FUND01/source_allocation.py | Original special five-key/core9 selector | Accepted at actual scope; no such instance in this witness |
| SE03_STEP2_CD6_FINAL_ASSEMBLY_14/cd6_allocator.py | Accepted raw/optional older-common six-key dispatcher | Accepted; core9 raw branch applicable here |
| SE03_STEP2_UNARY_A_LIFT_14/branch_funding.py; branch_core9_mask0.json | Actual high-core debt and fresh-prefix bank | Accepted inherited data; lookup and all actual bank rows independently rebuilt |
| C14 UNIFORM_R_TRANSFER.md | Exact I(r) and three E_r clauses | Conditional transfer only; E_r not discharged here |

No inherited universal theorem is newly accepted merely from this witness.
The failed old candidate's paid creator/erased-core defects remain recorded.
''')
write('N26_E4_FROZEN_GUARDS.md',f'''# Same frozen target; complete simultaneous guard receipt

The original immutable definition is `../N26_E4_FROZEN_GUARDS.md`;
its exact hash is already included among the inherited pins. Nothing in
the following table changes that definition or excludes a difficult guard.

{guard_table}

{meta}
''')
write('GUARDED_E4_DEPENDENCY_GRAPH.md',f'''# Load-bearing construction graph

Common physical vine V + exact reaching prefix R0
→ one reachable (A,BF,BE) boundary
→ explicit closed199-operation word W0
→ source-exact core13/core9, all rotations/costs, two watched-edge lifetimes
→ accepted core9 debt DATA + actual six-key projection
→ maximum-debt cut after W0[141]
→ actual I=[573,771], all physical events inside I
→ canonical f6 + common/natural full a0
→ every-producer creator / T19 / first-own-tail / j comparisons
→ literal frozen-success extension and signed R correction
→ all S1–S13 on THE SAME W*.

{guard_table}

Distinct pointer-tree replay and separately rebuilt allocation rules verify
the new instance. Existing CD6 is inherited; its entire finite certificate
is not regenerated. Original pending universal source claims do not serve
as unproved instance bridges: the actual operations/lifetimes/maps are
explicit in `aligned_source_and_owners.json` and rebuilt by the checker.
''')
word=candidate['period'];r0=candidate['original_reaching_prefix'];trees='\n'.join('- '+name+': `'+texttree(t)+'`.' for name,t in zip(('A','BF','BE'),cert['initial']))
write('GUARDED_E4_SOURCE_WITNESS.md',f'''# C27-EXISTS — exact original-source witness

{meta}
W0 is the following199-operation word. `Kk` means KEEP access tok;
`Dk` means A-only access tok. No implicit operation is present.

```
{tokens(word)}
```

Start all three physical trees at V, the increasing right vine1..13 with
its14 ordered external gaps. First execute the33-operation reaching word R0:

```
{tokens(r0)}
```

To realize the legal cut as actual source time, execute R0 W0 W0 W0[1:141].
This is572 original accesses. The certified period is then
W*=W0[142:199] W0[1:141], at actual occurrences573..771.
These are one-based inclusive slices. Every endpoint of every new payment
lies in this ONE actual interval. Earlier descriptions of W0 are preparatory
and historical; their event IDs are not reused as new-period donors.

At573 the exact three physical trees are:

{trees}

Their complete after771 trees are identical, respectively. `Fk` denotes
the unchanged external gap after sorted keyk, not a physically deleted key.
All initial and intermediate physical trees, all paths and rotations, and
all source words are in `aligned_source_and_owners.json` (SHA256
`{sourcehash}`). The independently checked source has A={cert['A']},
QF={cert['QF']}, QE={cert['QE']}. The seven KEEP targets are all odd keys1..13;
erase C=11 only from comparison B processing.

{crit_table}

The j row shows its final access cost a_t, not the H_j of its preceding
DELETE-containing genuine macro. That full macro includes its actual
preparation and has H_j≥3. All h..e macros have H1. G=1<x=7<C=11<R=13.
Every full double is an actual same-side splay with marked grandparent
and unmarked physical parent; the full marked core remains all13 nodes.
The auxiliary marked core remains9. This is an original reachable history,
not an adverse abstract graph row endowed with guessed source states.

The two selected original frontiers and their distinct next births are
(662,2), key9→(771,1), and (695,2), key5→(771,2). See the lifetime proof.
The actual bank and effective owner receipts complete S3–S5/S10–S13.
''')
write('TWO_SELECTED_ZERO_LIFETIMES.md',f'''# Exact two-arrival proof

{meta}
The following events all belong to the same actual period, beforej764.
At661, KEEP7 is an actual A RL double with G1/P11, creating edge7→11.
At662, KEEP9 destroys that watched outer edge; its genuine full macro is
H1/Q2, beta2,z1, hence its second branch demand(662,2) is a zero frontier.
At694, KEEP3 is the actual A zig from root7, creating edge3→7.
At695, KEEP5 destroys that outer edge, again giving H1/Q2,beta2,z1
and frontier(695,2).

The source preparations are real DELETE words, all retained in the
199-operation receipt. The protected policy runs in EVERY creator macro,
including LOW creators. Both identified creator macros have H1 and
beta+z≥2. Their tail after the licensed prefix is therefore empty.
Neither of these zero frontiers receives a creator-tail payment. Their
raw watched-edge seed bits may have comparison preimages; they are not
assumed to be unowned donors. Every other prescribed creator success is
retained exactly.

At each source boundary compute the actual marked-parent tree in BF.
Unary ancestors become leaves; accessing an old leaf kills exactly that
leaf. Consequently per-key leaf births and deaths alternate cyclically.
Pair a birth with its preceding same-key leaf death. Actual enumeration
of these transitions in this specific source gives next key9 birth(771,1)
and next key5 birth(771,2). Nonleaf accesses to those keys between origin
and birth are kept; absence of all such accesses is NOT assumed.

The two IDs and keys are distinct. They precedej764, both lie in I, and
their births are e ordinals1/2, not the recent C/R/G births4/5/6.
They are exactly the two selected arrivals at e. The actual creator stage
does not spend e's second physical bit, so c_e=0. The first-own-tail rule
pays the smaller selected birth in its alternative comparison; it does
not move any already frozen effective full assignment. This is the
required T19 mechanism, not two invented labels on the deep event.
''')
write('RV_EPSILON1_BANK_SOURCE_BRIDGE.md',f'''# Actual epsilon1 carry receipt

{meta}
The erased B is generated from the ORIGINAL source, skipping only KEEP11.
Its actual v769 target13 starts from root1, and p770 returns to root1.
Both accesses have one B double and one actual A event; thus the inherited
top-return selector is epsilon1. It is not an independently chosen bank bit.

Accepted core9 debt uses normalized mask[1,2,3,5,7,9], certificate
SE03_STEP2_UNARY_A_LIFT_14/branch_core9_mask0.json. Each actual A boundary
is projected by erasing unmarked unary ancestors and retaining branching
separators; the actual fixed B core is rank-normalized. The independent
checker recomputes the table lookup at every packet boundary.

The actual maximum debt is2 and the realized cut precedes packet0.
For a packet with boundary debts ds,dt, keep2-ds old bits; select all
natural owner bits and the first other actual bits up to2min(H,4);
prepend fresh spares, pay the missing B ordinals in order, retain2-dt.
All25 actual signed packet inequalities and all resulting owner IDs agree
between implementations. This invokes the accepted fixed-core certificate,
not the refuted changing-chart debt.

{bank_table}

At p the R-v bit u_v=(769,1,1) is exactly carry rank2 and L_p=2.
No intervening unlisted KEEP exists. This is source-derived carry survival.
''')
write('E4_FIRST_CONSUMPTION_SOURCE_THEOREM.md',f'''# Original-source e4 first consumption

{meta}
e771 is KEEP7 with actual A pathRL (one event) and BE path of length8,
hence Q_E=4. Its natural owners are(771,1,0)/(771,1,1) for e1/e2.
There are no fresh spares in its two-unit budget. The pre-e carry is
[(770,1,1),(769,1,1)], in that order. Therefore missing e3 consumes the
p unit and missing e4 consumes u_v. The packet changes debt0→2 and
empties the bank. Earlier packets never assign u_v to a missing demand.

Thus on this actual reachable closed source,

    h6(771,4) = f6(771,4) = (769,1,1).

The equality of f6 and h6 here is justified by the applicable branch/domain
receipt in NORMALIZED_F6_GUARDED_POLICY.md. It is not an assumption that
every raw bank consumer survives arbitrary older-common normalization.
''')
write('ORIGINAL_PAIRED_SOURCE_REALIZABILITY.md',f'''# Original reachable triple execution

{meta}
The source word, common starting vine,33-operation R0 and legal572-access
prefix are explicit in GUARDED_E4_SOURCE_WITNESS.md. The three executions
are deterministically linked: A splays every access; BF splays all KEEPs;
BE splays those same KEEPs except11. All physical keys/gaps remain present.
The tuple-tree producer and parent-pointer checker agree at EVERY actual
operation, not just final costs or marked-tree shapes.

For each splay the checker records the actual initial search path, performs
the bottom-up zig/zigzig/zigzag rotations using parent pointers, and exports
the entire physical tree including every external gap. It agrees with all
stored G/P/target labels and every double/zig count. All full B paths are
even same-side pairs; their grandparent is marked and parent unmarked.
The full13-node marked core and auxiliary9-node core are checked at every
boundary. Original processed root-repeat KEEPs are retained as identities,
and their intervening A costs remain in the appropriate macro.

The exact triple after771 equals the exact triple before573. This proves
original paired closure and ALSO auxiliary closure at the legal actual
cut. BE is never initialized from an independently invented favorable tree.
Reaching it from the common vine is part of the checked original prefix.
''')
domains=rows_table(['extra erased mark','recurrent five-key core','original special Step1 applicable?'],[[z['additional_erasure'],z['recurrent_core'],'NO: core≠9'] for z in audit['older_Step1_domains']])
write('NORMALIZED_F6_GUARDED_POLICY.md',f'''# Actual applicable f6 and older-common policy

{meta}
Use the unchanged accepted C14 dispatcher cd6_allocator.py. With no
applicable pre-existing original special Step1 map its canonical branch
is raw h6. If a certified fixed old f5 is supplied on its actual domain,
the dispatcher instead preserves that common map and performs the original
exchange. These cases must not be confused.

For THIS new source, there is no pre-existing f5 map on its actual absolute
occurrences. More strongly, every possible additional marked erasure from
the retained six keys has the following recurrent source domain:

{domains}

The original special Step1 five-key/core9 selector is applicable to NONE.
The independent implementation regenerates each double-erased comparison
from the actual common prefix and checks its recurrence/core. Scalar CD5
on other cores does not manufacture a fixed physical Step1 owner map;
the separate stronger all-core I(5) interface is explicitly still open in
C14 CHECKPOINT.md. No smaller-core five-key map is invented, substituted,
or used to displace an old owner. All historical fixed maps remain intact.
Thus this is genuinely the applicable canonical f6=h6 case, not omission
of an applicable old f5 lock. The actual f6 is explicitly materialized
and independently matched at every demand, not inferred only from e4.

Next restrict f6 to ORIGINAL full-common demand IDs(t,k). Freeze this map
first; apply the original full natural comparison h0 by its licensed
common exchange. Only after these values are fixed are leaf, protected
creator, T19, first-own-tail and j comparisons used to append successes.
All existing values are literally preserved at each stage. In particular
u_v's full effective owner is(771,4), although the full natural comparison
has h0_F(769,2)=u_v. The natural comparison itself is not silently rewritten.
''')
write('GUARDED_PERIOD_CLOSURE.md',f'''# Legal absolute source period

{meta}
W0 length199 closes A/BF/BE at its printed boundary after R0. Its earliest
maximum six-key debt boundary lies after body occurrence141, which is e.
Execute R0 W0^2 W0[1:141] as a physical reaching prefix. The next199 original
accesses, W0[142:199] W0[1:141], are exactly I=[573,771]. Its first auxiliary
packet has pre-debt2=max; its final packet e has post-debt2, so the actual
bank starts and ends empty. No illegal zero-debt recut or credit creation.

For body position t, the exact bijection is

    tau(t)=572+(t-141 if t>141 else 199+t-141).

Both donor and demand endpoints are transported. The raw f6 transport was
checked against a fresh accepted dispatcher run on the legal period.
All final full policy stages were then reconstructed for THIS actual
interval before freezing its new successes. Historical earlier receipts
are left unchanged; different cyclic copies have different absolute IDs.
Every new donor satisfies573≤t≤771. Duplicate or adjacent-copy donors
are explicitly rejected by the independent checker.

The raw h6 working peak is10≤25. The endpoint-buffer realization of f6
has peak4 and the completed full instance peak6. Open a record when the
first endpoint of a fixed payment is encountered; close it at the second.
An earlier unit is stored as that actual bit; an earlier demand is a debt
record until its actual bit arrives. Both boundaries have empty buffers.
Counting BOTH kinds of records gives a conservative upper bound for actual
stored bits. This is the inherited one-period/block accounting scope,
not a claim of online causal funding for arbitrary histories or supports.
''')
write('ACTUAL_E4_EFFECTIVE_OWNER_LEDGER.md',f'''# Physical ownership, comparisons and successes

{meta}
All maps below use actual IDs in I. Alternative comparison maps are not
simultaneously asserted as additional effective owners of the same bit.

| Role | Actual identity/value |
|---|---|
| R-v physical second bit | u_v=(769,1,1) |
| Natural full comparison preimage | (769,2) |
| Raw auxiliary first consumer | e4=(771,4) |
| Applicable canonical f6 preimage | (771,4) |
| Frozen full common/effective owner | (771,4), unchanged through every stage |
| Original natural p second bit | (770,1,1) |
| Raw missing e3 payment | (771,3)→(770,1,1) |
| Post-creator e spare branch | c_e=0 |

{stage_table}

The original full domain has58 demands. Common/natural exchange initially
covers53, and the leaf comparison appends4. Later prescribed comparisons
retain all57 successes. Their unresolved effective ROOT is(661,3), not
automatically the comparison birth ID e2. The j physical ordinal3 donor
is {cert['j_donor']}; its comparison use does not by itself create a new
effective success here. The isolated owner obstruction is not a free bit.

For this one explicit source, the gap1 macro has H={cert['gap_macro_H']}.
Its ninth physical unit is {cert['source_gap_donor']}. This is outside the
raw f6 budget selection, full h0 prefix, all later comparison images and
the57 effective values; each identity is directly checked. Source reason:
the gap's natural prefix has at most6 units, the raw six-key budget at most8;
an ordinal9 selection would require all first8 also selected, impossible.
Leaf/branch prefix uses at most4; any protected creator tail occupies at
most the last6 units and lies later in this H≥8 gap; no T19 own-birth is
assigned in this gap. The j supplier is in a different original macro.
Append ONLY (661,3)→{cert['source_gap_donor']}. This produces a concrete
58-demand injection for this witness, preserving every prior value.

That optional exact-word completion is not the missing universal source
theorem: these deliberately large preparations do not occur in every
guarded history. No global inequality is used to assume its endpoint.
The endpoint and its unused status are independently explicit. In
particular u_v remains occupied and contributes no extra donor.
''')
write('SIGNED_COMPARISON_ACCOUNTING.md',f'''# Original signed R-flip correction retained

{meta}
The actual omitted R proof-comparison interval consists of g766,s767,
t768,v769,p770. It has5 actual A events (10 physical bits) and8 full B
doubles. Starting the shadow A at the original afterh765 state, omit only
that comparison block and access x=7 at e. Its actual shadow pathRLL
requires2 A events, versus the original e pathRL requiring1. The shadow
and original whole A trees rejoin exactly aftere, including every physical
subtree/gap. The shadow extra event is represented by the two ACTUAL
omitted p bits(770,1,0)/(770,1,1), not invented shadow supply.

The correction consumes2 of the10 block units: 10-8-2=0, the inherited
corrected R balance. It is not the earlier invalid +2 identity surplus.
These correction bits are not additionally assigned as free full donors;
their actual full/auxiliary ownership maps remain explicit and unchanged.
This instance does not contain the alternate G-type block whose inherited
corrected balance is−1; that theorem/status is retained, not changed.
''')
write('SOURCE_DECISION_LEDGER.md',f'''# Construction / exclusion decision

Original target: ∃W G27(W), or universal exclusion. The original frozen
guards are unchanged. The positive branch now supplies one exact W*.

| Attempt | Exact conclusion |
|---|---|
| Initial C27 manuscript candidate | REJECTED: mandatory creator payment removes claimed selection; transient erased core is not the required closed domain. Preserved at parent. |
| construct trials | Four rejected inverse-closure candidates had auxiliary core6 and critical qE1/1/2, not the target. |
| product/product2/product3/product4/product5 | Bounded actual full/erased source searches, all failed/rejected receipts preserved. No exhaustion/universal exclusion claimed. |
| separated prehistory | Fixed C18 prefix does not reach the chosen product component; local failure only. |
| backwards skeleton | Two separated zero-tail creators and next births identified in a source-reachable closed product cycle. Discovery only. |
| realize/owners/aligned | One199-operation original source plus accepted bank, applicable canonical f6 and legal actual interval constructed. |
| independent | New checker passed original trees/bank/domains, then failed an EXTRA overstrong creator assertion(beta exactly2). Source not rejected or changed. |
| independent2 | Corrects only the checker assertion to required zero-tail condition H1,beta+z≥2. Complete distinct implementation PASS. Both attempts/charges retained. |

The complete witness refutes the proposed universal source exclusion.
Failed searches never established exclusion. This is OUTCOME A — E4
SOURCE REALIZABLE. Its existence does not settle universal donor supply.
''')
write('ADVERSARIAL_SOURCE_CONTROLS.md',f'''# Exact-source adversarial controls

{meta}
The independent parent-pointer implementation imports no producer engine,
allocator, leaf-channel, creator or exchange module. It checks all572
prefix accesses and all199 period accesses, every path/rotation/tree, actual
costs, support, core constancy, the specific debt DATA lookup, fresh-prefix
bank, selected origins, creator policy, own-tail, full frozen policy,
R correction and original absolute seam.

K1 fake/duplicate births: different keys9/5 and original e1/e2 verified.
K2 recent C/R/G births: ordinals4/5/6 not selected. K3 unchanged G2 and
K4 lost-core path: old failures not reused. K5 stitched states: common
vine and all original reaching operations supplied. K6 formal bank and
K7 survival: real debt/carry rebuilt. K8 earlier consumer: every earlier
payment checked. K9 q4: actual BE depth8. K10 raw=f6: applicable old-domain
analysis precedes equality. K11 free u_v and K12 owner-cycle free: rejected
by literal e4 owner. K13 omitted creator: ALL producers run and retain
successes. K14 closure: entire triple closes. K15 neighboring copies:
all endpoints inside573..771. K16 identity A-flip: actual extra shadow
event corrected with p bits. K17 finite search⇒exclusion: no such inference.
K18 partial⇒witness: full guard receipt now explicit. K19 witness⇒global
obstruction and K20 one case⇒universal: no such promotions.

The independent checker also constructs three corrupted owner receipts:
duplicate a donor, substitute the previous cyclic-copy bit, or move e4's
frozen owner. All are rejected. These controls test THIS certificate,
not a finite substitute for a universal mathematical theorem.

First audit failure is preserved: an unnecessary assertion that each
creator has beta EXACTLY2 was false. Empty tail needs only beta+z≥2 at H1.
The original source and allocation are byte-identical between audits.
''')
write('INDEPENDENT_AUDIT_STATUS.md',f'''# New exact-instance independent verification

PASS: `audit_independent2.py`, run by the unchanged cumulative controller
as group independent. `run_independent2_result.json` and
`independent_audit2.json` are the receipts. New code uses mutable nodes
with parent pointers and individual rotations; the producer uses immutable
tuple path rewrites. It independently rebuilds leaf transitions, watched
creator events, T19, own-tail, table projections and recursive owner walks.
No producer algorithm module is imported.

This is a distinct implementation operated by the same research agent.
It is not external peer review or formal proof-assistant verification.
Accepted core9 debt DATA and previous theorem scope are inherited, not
independently re-proved from all quotient edges. The exact new W* instance
and all its new physical owner receipts are checked. Prior C15–C26
audit-pending universal claims are not promoted.

Initial `independent` run failed a stronger-than-needed checker assertion,
after agreeing on original source, bank and old Step1 domains. Its code,
log and CPU remain archived. Version2 changes just that assertion and
receipt filenames. The actual source/owners never changed.

The user's explicit later authorization raises cumulative symbolic120→240
and independent300→600; no usage reset. All other caps are unchanged.
New cumulative query count{queries}; globalCPU{global_used}/7200;
symbolic{groups['symbolic']}/240; independent{groups['independent']}/600.
`resources_checkpoint.json` includes both rejected/failed and accepted
runs plus all controller CPU. Metadata byte/provenance work is excluded
only under the inherited convention and measured separately.
''')
write('IAGS_PROOF_TREE.md',f'''# IAGS recursive closure

## Box27 — original frozen existence target

Target: ∃W G27(W). Conditions: all original S1–S13 simultaneously.
Inheritance: unchanged original source; accepted CD6/core9 debt/physical
dispatcher; declared C18/C19/C22 owner-policy specifications.
Ambiguity at entry: selected prehistory versus erased recurrence and real
owner/cut compatibility. Bridge: one fully original exact witness suffices.
Status: CLOSED by W*, source/owner receipt and distinct implementation PASS.

## Box27.B — two selected origins

Target: two pre-j H1/Q2,beta2,z1 creator-unpaid zero lifetimes with next
births e1/e2/e3. Conditions: every creator runs. Inheritance: actual policy
specification, not assumed seed availability. Alter: separate creators
with real A reset/preparations instead of trying the rejected shared
prehistory. Recurse: source-reachable product skeleton + two zero-tail
creator macros. New instance lemma: keys9/5 produce(662,2)/(695,2) and
next births e1/e2. Bridge: actual leaf birth/death alternating per key.
Status: CLOSED at this existential scope.

## Box27.C/D — bank and consumer

Target: actual epsilon1, L_p≥2/rank2 and first e4 consumption.
Conditions: reachable closed auxiliary high core. Inheritance: accepted
fixed-core debt. New instance lemma: recurrent core9 source, debts0→0 at
v/p and0→2 at e. Bridge: exact fresh-prefix bank gives e3=pbit/e4=vbit.
Ambiguity: none on this W*, arbitrary normalized cases unclaimed.
Status: CLOSED.

## Box27.F/G — actual owner and legal period

Target: applicable f6/older-common, every frozen success and original cut.
Conditions: real domains/absolute IDs. Inheritance: accepted dispatcher
and literal frozen-success exchange. New instance lemmas: no extra erasure
is original special Step1 core9; actual maximum-debt cut after body141;
all owner stages retain old values and Bank25. Bridge: rebuild maps on
actual I=[573,771] and verify complete triple closure. Status: CLOSED.

## Parent Gate U — separate OPEN Box

Target: universal source-derived full license and owner-safe storage for
arbitrary support, repeated/shared recoveries and all required receipts.
Conditions: all three original E_r clauses. Inheritance: conditional
I(r−1)+E_r⇒I(r). Ambiguity: source-uniform supplier/escape and mixed-owner
interfaces, not existential nonemptiness. Bridge: NOT supplied by W*.
Status: OPEN. No upward reconstruction past the actually proved bridge.
''')
write('FULL_PROOF.md',f'''# C27-EXISTS — complete proof at the frozen existential scope

{meta}
THEOREM. The full guarded N26.E4 source class is nonempty.

PROOF. Fix physical ordered keys1..13, marks1/3/5/7/9/11/13 and erase
marked C=11 from comparison B processing only. Use the exact R0/W0 words
and common initial vine in GUARDED_E4_SOURCE_WITNESS.md. Execute the572
original reaching accesses followed by the199-operation legal period.
Ordinary bottom-up splay rotations determine a unique triple execution.
The complete operation table in aligned_source_and_owners.json and the
distinct parent-pointer replay agree at each tree/path/rotation. The
period closes all three physical trees exactly; all original KEEPs and
DELETEs remain. Full marked core is13, erased marked core9, and the source
has the declared extreme hard-unary R-first j..e frame. Thus S1/S2 and
S7–S9/S11 hold directly, without a quotient-realization assumption.

The original selected-zero mechanism is evaluated after all mandatory
protected creator payments. Source creator661 makes watched edge7→11;
zero662 destroys it. Source creator694 makes3→7; zero695 destroys it.
Both zero rows have H1/Q2,beta2,z1. Their creators have empty licensed
tails, and actual next same-key leaf births are e1/e2 at771. Thus exactly
two permitted inner, pre-j, distinct selected origins survive the creator
stage. Other successful creator entries stay literal, and first-own-tail
uses only still-unoccupied comparison bits; c_e=0. This proves S6 with
the actual policy, not guessed labels. See TWO_SELECTED_ZERO_LIFETIMES.md.

For the SAME actual source, the accepted core9 debt table and source
projection give a maximum debt2 and legal cut after body141. Realize that
cut at absolute I=[573,771], on both donor and demand endpoints. The bank
receipt has v/p debts0→0 and carry lengths2, then e debt0→2. It puts
u_v=(769,1,1) at rank2 afterp and consumes it FIRST at(771,4), with actual
qE_e=4 and H_e=1. These statements follow from the displayed bank rows
and are independently rebuilt; they prove S3–S5 and the debt/cut part S12.

For every additional erasure from E, the actual recurrent five-key core
is5,6 or7, never9. The original special Step1 core9 selector has no
applicable old map here; the all-domain scalar CD5 theorem is not silently
replaced by an all-core physical selector. Hence the applicable canonical
accepted f6 is the raw high-core map, explicitly materialized in full.
Freeze its common restriction before full natural exchange. Rebuild every
leaf/creator/T19/own-tail/later comparison; append only licensed endpoint
successes and preserve every previous effective value. The unchanged
natural comparison still has h0_F(769,2)=u_v, while the ACTUAL common and
effective owner is e4 throughout. This verifies S10 and the owner portion
of S13. Optional source-gap completion pays the sole remaining effective
root with a directly exhibited unused physical ninth gap unit; it does
not move any success or prove a universal supplier theorem.

The R shadow comparison is nonidentity: omitg..p afterh and its next x
access takes2 A events rather than1. Exact whole-tree rejoin holds. Its
extra event uses the two actual omitted p bits in the comparison debit,
giving corrected R balance0. They are not invented or free credits.
Every actual owner/correction endpoint belongs to I. The raw bank has
working peak10; conservative endpoint-record realizations of f6 and the
completed full witness have peaks4/6 and empty boundaries, all≤Bank25.
Old historical owners/source/certificate bytes are unchanged; only the
two explicitly authorized cumulative CPU caps increased. Thus the rest
of S7/S12/S13, and R1–R4, hold.

All thirteen frozen conditions therefore hold simultaneously for W*.
One exact witness proves ∃W G27(W). QED.

This finite exact construction proves an EXISTENTIAL theorem. It does not
stand in for a finite test of a universal theorem. It neither establishes
nor refutes universal frozen extension, unconditional Gate U, Universal
Coarse-Double or Dynamic Optimality. Existing accepted CD6 is not reopened.
''')
write('E4_ARCHITECTURE_CONSEQUENCE.md',f'''# Exact consequence for the funding architecture

C27 settles the guarded source nonemptiness question positively. Universal
exclusion of this direct-e4 class is false. Any universal next theorem must
handle it rather than invoke its supposed unrealizability.

The actual raw consumer is e4 AND this source's applicable canonical f6
initiating owner is e4. Its full effective owner remains e4 after all
required successes. The R-v survivor is not an extra unowned unit. A
closed original history need not eliminate this owner configuration.

For W* alone, the explicit large source preparation supplies an unused
ninth gap unit paying the remaining effective root. Thus W* is neither
an obstruction to frozen extension nor a Coarse-Double counterexample.
This one-word supplier does not occur by necessity in every hard source.

NEXT BOUNDED THEOREM: guarded direct-e4 common-component escape. Fix the
original seven-key/core13, epsilon1, two-selected-arrival domain, actual
canonical/older-normalized f6 and the frozen post-creator/own-tail a.
Construct a source-defined legal comparison on the actual remaining
ROOTS whose owner walks exit the occupied e4/v2 component at distinct
eligible actual endpoints, preserving every old success and Bank25; or
give an exact source refutation of that proposed escape rule. Start by
tracking the exterior producer(661,3) and its gap supplier in W* to identify
which real source property can replace this deliberately large reset.
Do not equate a comparison birth frontier with its unpaid effective root.
''')
write('REMAINING_RV_SOURCE_CLASSES.md','''# Scope not promoted by the existential decision

C27 closes only the existence of the fully guarded direct-e4 subclass.
Still open unless separately proved: source-uniform direct e3/e5 and
paired q5/q1 first-consumer behavior with all guards; core8 FIFO cases;
unselected exterior producers; arbitrary older-normalized receipt cases;
the c_e=1 two-debt branch; general G deficits; repeated/shared and mixed
recoveries; arbitrary-support eligible supply and frozen noncollision.
Accepted partial lemmas keep their original scopes and pending audits.
W* does not prove all these classes realizable, impossible or fundable.
''')
write('GATE_U_DEPENDENCY_STATUS.md','''# Gate U remains U-OPEN

Recover the exact invariant/transfer from unchanged
SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md:

    I(r-1)+E_r => I(r).

I(r) is witness-rich source LOCAL license A(disjoint seeds) or B(signed
source credit), with natural/common owners, actual period, and Bank25.
It is not merely existence of a global matching or the desired count.

| Original E_r clause | Consequence of C27 |
|---|---|
|1 same original A, legitimate erased recurrence/domain, actual fixed fE and cut/event bijections | Fully explicit for W* at r7→6; basic general erasure correspondence inherited. No new all-r receipt theorem. |
|2 specified uniform full-source license A/B independently from source, fE and CD(r) | OPEN. One constructed witness and optional one-word supplier do not establish this universal clause. |
|3 common pairing/E-only retirement, block eligibility, legal cuts, immutable successes and Bank25 | Explicit for this actual witness; universal repeated/shared/exterior-owner schedule still OPEN. |

CD6/Step1 remain accepted at their own scopes. Strong all-core I(5) was
not silently inferred from scalar CD5. The r-4 width/storage obstruction
to unchanged six-key carry remains. Unconditional arbitrary-support
transfer, Step3, Universal Coarse-Double and Dynamic Optimality remain OPEN.
''')
write('FINAL_VERDICT.md',f'''# OUTCOME A — E4 SOURCE REALIZABLE

Campaign27's frozen existential theorem is proved by one original
199-operation reachable, exactly paired-closed source W*. All guards
S1–S13 are checked simultaneously. The complete proof is FULL_PROOF.md;
source words/trees/rotations/owners are in aligned_source_and_owners.json.

Branch `{entry['branch']}`; HEAD `{entry['head']}`; tracked tree clean.
All {len(pins['pins'])} inherited local pins match and historical work is
preserved. New authoritative work is this continuation; the parent
UNRESOLVED record is the superseded initial snapshot, left unchanged.

G=1<x=7<C=11<R=13; full core13, erased core9. Actual I=[573,771].
The two creator-unpaid T19 origins(662,2)/(695,2), keys9/5, arrive at
distinct e1/e2=(771,1)/(771,2). Actual epsilon1, L_p=2 and carry rank2
hold for u_v=(769,1,1), whose first auxiliary consumer is e4=(771,4).
The applicable canonical f6 and frozen full effective owner are also e4.
All later successful values are preserved. The nonidentity R correction
is retained, with actual p bits and corrected R balance0.

Independent verification: PASS using a distinct parent-pointer/source and
owner implementation operated by the same research agent. This is neither
external peer review nor proof-assistant verification. Inherited CD6 debt
DATA are reused; old pending universal derivations are not promoted.
Raw bank peak10 and full endpoint-buffer peak6 are below Bank25.

Exact consequence: THE GUARDED E4 SOURCE CLASS IS NONEMPTY.
The proposed universal exclusion of this class is false. u_v remains
occupied; no new free donor follows from its bank survival. An optional
explicit source-gap payment completes this one prepared source, not the
universal frozen extension theorem.

Campaign27 is CLOSED at its requested original existential scope.
No invalid source dependency requiring CD6 reopening was found. General
frozen escape, G compensation, repeated/shared arbitrary-support supply,
unconditional Gate U, Universal CD and Dynamic Optimality remain OPEN.

Resource usage is cumulative: global{global_used}/7200,
symbolic{groups['symbolic']}/240, independent{groups['independent']}/600;
new queries{queries}<2000000. Both user-authorized cap increases are
recorded; other caps, Bank25, original owners and semantics are unchanged.
See resources_checkpoint.json for all failed/rejected and accepted charges.
''')
write('CHECKPOINT.md',f'''# Campaign27 CLOSED — Outcome A

Authoritative verdict FINAL_VERDICT.md; proof FULL_PROOF.md; exact source
and physical ownership aligned_source_and_owners.json; distinct-instance
audit independent_audit2.json PASS. Branch `{entry['branch']}`, HEAD
`{entry['head']}`. No old tracked/source/owner/certificate mutation.

Do not repeat solved source-existence checks or accepted prior audits.
The full guarded direct-e4 source class is REALIZABLE by W*:199 operations,
actual I573..771, full core13/auxiliarycore9, two selected pre-j origins,
epsilon1, post-p rank2/L2, actual first e4 consumer, all applicable owner
policies and original legal cut. u_v's actual full owner is e4, not free.

The last independent audit passed after correcting an overstrong checker
assertion only; preserve both failed and passing implementations/receipts.
No universal theorem is inferred from the finite existential witness.

NEXT: the guarded direct-e4 common-component escape theorem stated in
E4_ARCHITECTURE_CONSEQUENCE.md. Source-derive eligibility and distinct free
endpoints for actual unpaid ROOTS while keeping common/creator/own-tail
successes. The witness exposes original exterior root(661,3); its gap
supplier is an explicit diagnostic example, not yet a uniform mechanism.
G deficits, all normalization/c_e cases, repeated/shared noncollision and
Gate U E_r2/E_r3 remain separate open parent obligations.

Continue cumulative resource accounting from resources_checkpoint.json.
No cap reset. Independent symbolic cap240, independent-audit cap600,
global7200 and Bank25=25. Current groups/global include all failed work.
''')
write('C27_RESULT_CERTIFICATE.json',json.dumps({'outcome':'A — E4 SOURCE REALIZABLE','campaign27_closed':True,
    'theorem':'exists original reachable paired-closed W satisfying ALL frozen N26.E4 guards',
    'branch':entry['branch'],'HEAD':entry['head'],'tracked_tree_clean':True,'source_file':'aligned_source_and_owners.json','source_sha256':sourcehash,
    'audit_file':'independent_audit2.json','audit_sha256':audithash,'source_length':199,'actual_interval':[573,771],
    'guards':[{'guard':g,'receipt':r,'status':s} for g,r,s in guard_rows],
    'f6_mode':'applicable accepted canonical raw; no original special five-key/core9 instance exists under extra erasure',
    'frozen_owner':[771,4],'unit':[769,1,1],'new_independent_instance_audit':'PASS distinct implementation, same agent',
    'external_peer_review':False,'formal_proof_assistant':False,'universal_funding_proved':False,'Gate_U':'U-OPEN',
    'Universal_CD':'OPEN','Dynamic_Optimality':'OPEN','resource_caps_preserved_except_two_authorized_increases':True},indent=2))
resources['publication_metadata_CPU_excluded']=time.process_time();jout('resources_checkpoint.json',resources)
pointer='''# Latest Campaign27 result

The initial unresolved snapshot below this directory remains unchanged.
The authorized continuation has closed the frozen existence question:
**OUTCOME A — E4 SOURCE REALIZABLE**.

See [final verdict](CONTINUATION_01/FINAL_VERDICT.md),
[complete existential proof](CONTINUATION_01/FULL_PROOF.md),
[exact source witness](CONTINUATION_01/GUARDED_E4_SOURCE_WITNESS.md),
and [distinct implementation audit](CONTINUATION_01/INDEPENDENT_AUDIT_STATUS.md).
Universal funding, Gate U and Universal CD remain open.
'''
with (C27/'LATEST_CONTINUATION.md').open('x',encoding='utf-8') as f:f.write(pointer)
manifest={'status':'EXACT_INSTANCE_PROOF_AND_AUDIT_CONTENT_CHECKPOINT_NOT_FORMAL_PROOF','branch':entry['branch'],'HEAD':entry['head'],
    'outcome':'A — E4 SOURCE REALIZABLE','inherited_pins_rechecked':len(pins['pins']),
    'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file()],
    'new_parent_pointer':{'path':(C27/'LATEST_CONTINUATION.md').relative_to(ROOT).as_posix(),'sha256':sha(C27/'LATEST_CONTINUATION.md')},
    'historical_root_manifest_unchanged':sha(C27/'campaign_manifest.json')}
jout('campaign_manifest.json',manifest)
print(json.dumps({'outcome':'A — E4 SOURCE REALIZABLE','documents':len(list(B.glob('*.md'))),
    'old_pins_verified':len(pins['pins']),'global_CPU':global_used,'groups':groups,'new_queries':queries,
    'manifest_files':len(manifest['files']),'publication_metadata_CPU':time.process_time()}),flush=True)

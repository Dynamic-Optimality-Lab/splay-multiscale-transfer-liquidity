"""Metadata/provenance only. No mathematical engine is executed."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent
OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
c=read(OLD/'aligned_source_and_owners.json');a=read(OLD/'independent_audit2.json');r=read(OLD/'resources_checkpoint.json')
assert a['status']=='PASS_DISTINCT_IMPLEMENTATION_EXACT_EXISTENTIAL_WITNESS'
assert a['input_sha256'][(OLD/'aligned_source_and_owners.json').relative_to(ROOT).as_posix()]==sha(OLD/'aligned_source_and_owners.json')
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
# First research artifact: immutable frozen witness, including all source data
# by exact path/hash. Full maps are referenced, never replaced by a prefix.
text='''# W199 — frozen source and policy, first C28 research artifact

Date2026-11-04. Target source is exactly Campaign27 CONTINUATION_01's
199 original operations, actual interval[573,771], G1<x7<C11<R13.
Common source inventory keys1..13; seven odd KEEP marks; erase11 from
comparison B processing only. A splays all operations, BF all KEEPs,
BE all retained KEEPs; ordinary bottom-up splay, unchanged physical keys.

Authoritative receipt: ../SE03_STEP3_GUARDED_E4_REALIZABILITY_27/
CONTINUATION_01/aligned_source_and_owners.json
SHA256: SOURCEHASH

This receipt contains initial A/BF/BE trees; complete572-operation common-
vine reaching prefix; all199 KEEP/DELETE operations; every before/after
tree, path, rotation, actual A event, full/erased double, macro/bank/cut
receipt, selected lifetime, comparison map and successful effective map.
It is pinned intact. No original source operation or allocation is changed.

Original period word (K=KEEP, D=A-only access):

```
WORD
```

Exact initial triple (JSON with external gaps Fk):

```
TREES
```

The legal cut is after unrotated body141 at max debt2. Every new source
occurrence ID is in573..771. Original A/BF/BE close exactly. Total A261,
physical bits522, full demands58, auxiliary demands27. Full core13,
auxiliary core9. Selected origin(662,2),key9→(771,1) and
(695,2),key5→(771,2). Actual epsilon1, L_p2, u_v=(769,1,1) rank2 afterp;
e4=(771,4) is its first raw consumer and its actual frozen effective owner.

CRITICAL POLICY FREEZE: final_full_allocation is the inherited COMPLETE
58-demand map. The later original payment(661,3)→(621,2,0) succeeded in
C27 and is therefore frozen too. The historical57-entry policy stage is
not the current a*. Do not remove that successful payment to manufacture
an unpaid root. Determine P* from this full map in the new inventory phase.

Preserve all raw/natural/common/normalized/creator/T19/own-tail comparison
receipts literally. No old five-key/core9 instance applies under any extra
erasure on this witness; the six checked recurrent cores are5,6,6,5,5,7.
Canonical f6=h6 is the applicable accepted dispatcher branch here.
Do not extrapolate that equality to arbitrary older-common receipts.

C23 nonidentity R comparison: omitg..p, shadow e needs2 events versus
original1, exact whole-tree rejoin; debit the two ACTUAL p770 bits.
Corrected R balance0; do not resurrect an identity surplus or spend shadow
credits twice. No selected G-type deficit is part of this R-only instance.

Inherited raw six-key bank peak10, f6 endpoint records4, final-full endpoint
records6, empty seam; Bank25 remains25. This is one-period/block accounting,
not an automatically universal causal schedule or target-specific license.

Verification reused: audit_independent2.py and independent_audit2.json,
distinct mutable-parent-pointer/source/owner implementation by the SAME
agent, PASS; not external review or proof-assistant certification. Do not
rerun these completed checks without a new inconsistency. The independent
audit pins the source receipt. New C28 universal results need their own
proof and precise verification status.

Resources inherited cumulatively: global3676.765625/7200,
symbolic175.03125/240, independent300.359375/600. The two cap increases
were explicitly authorized before C27's continuation. No reset or new
extension. Prior new-source queries1797843 are retained conservatively
against the2M limit. Bank25,32GiB,12h,DAG4M,edges5M remain unchanged.

C28-W: decide funding with ALL current successes frozen. C28-U: universal
original guarded-e4 class, not repetitions of W199. W28 and U28 remain
separate proof targets. Gate U conditional transfer and CD6 scopes frozen.
'''.replace('SOURCEHASH',sha(OLD/'aligned_source_and_owners.json')).replace('WORD',' '.join(m+str(k) for m,k in c['period'])).replace('TREES',json.dumps(c['initial']))
write('W199_FROZEN_SOURCE_AND_POLICY.md',text)
prior=read(OLD/'dependency_pins.json');pins={z['path']:z for z in prior['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256'],'origin':'C27_CONTINUATION'}
for p in (OLD/'campaign_manifest.json',OLD.parent/'LATEST_CONTINUATION.md'):
    pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C27 final publication'}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in prior['external_pins']:assert sha(Path(z['path']))==z['sha256']
directive=Path('C:/Users/Saif malik/.codex/attachments/cccf674b-effb-478b-9ae4-42681021d9c9/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'global_reserve':5,
    'controller_reserve':1,'Bank25':25,'phase_caps':{'inventory':20,'compress':25,'structured':25,'independent':100,'audit_proof':60},
    'inherited_source_queries':r['new_source_queries'],'remaining_conservative_queries':2000000-r['new_source_queries'],
    'inherited_C15_C27_engine_calls':21881,'inherited_pins':len(pins),'usage_reset':False,
    'resource_authorization':'Inherit explicit user cap increases to240/600; no further increases authorized.',
    'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'status':'CONTENT_PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda x:x['path']),
    'external_pins':prior['external_pins']+[{'path':str(directive),'sha256':sha(directive)}]})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
print(json.dumps({'status':'C28_SOURCE_FROZEN','pins':len(pins),'groups':r['cumulative_group_CPU'],'old_source_unchanged':True}))

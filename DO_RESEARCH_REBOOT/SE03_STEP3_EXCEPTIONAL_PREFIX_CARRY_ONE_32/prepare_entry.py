"""Metadata-only checkpoint/source freeze. No original source query."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent;OLD=P/'SE03_STEP3_FIRST_RETURN_7_REPAYMENT_31'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*s):return subprocess.check_output(['git',*s],cwd=ROOT,text=True).strip()
branch=git('branch','--show-current');head=git('rev-parse','HEAD')
assert branch=='coarse-double-branch' and head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
r=read(OLD/'resources_checkpoint.json');prior=read(OLD/'dependency_pins.json')
pins={z['path']:z for z in prior['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256'],'origin':'C31_PUBLICATION'}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C31_FINAL_PUBLICATION'}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in prior['external_pins']:assert sha(Path(z['path']))==z['sha256']
directive=Path('C:/Users/Saif malik/.codex/attachments/93cb50a3-b565-45e4-b459-308b8a218c83/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
write('FR32_FIX_PREFIX_SCOPE_FREEZE.md','''# Frozen source scopes: FIX, PREFIX and EXC

Authority: C31 FR31_SCOPE_STEERING and the current C32 user directive.
FIX retains the ENTIRE saved C30 A tree before critical j117, the exact
B frame and all original guards. Its universal zero-debt theorem remains
OPEN. PREFIX replaces only the prescribed shallow L/RL/LL frame by its
original-source-reachable ordered-term parameterization; deeper A structure
is NOT silently fixed. In particular the subtree below11 may vary. Any
permitted other ordered terms retain the original source conditions, not
arbitrarily independently selected BSTs. Every FIX instance is a PREFIX
instance at its fixed parameter, whenever the same B/other guards apply.

EXC is the exceptional PREFIX continuation: critical predecessor j to7,
Hj1/Qj2/sigma0; weak helper h to11,H1/Q2/beta1/z1/sigma-1; comb e to5,
H1/Q3/sigma0; NO intervening genuine lower KEEP after comb; first upper u
is11 with actual whole-macro H1, Q1 and sigma0. Nongenuine KEEPs and
DELETEs are retained in their actual genuine macro costs. The first later
genuine full KEEP7 is tau. Its root return is not full-state renewal.

Ambient source: reachable finite exactly paired-closed original Pair Access,
seven genuine KEEP marks{1,3,5,7,9,11,13}, full marked ancestor core13,
all-SS marked G/unmarked P transitions, ordinary bottom-up splays. A
receives every original operation, full B every KEEP, erased B its prescribed
subsequence. DELETE is A-only, never physical key deletion. Actual helpers,
signed charts, source periods, legal cuts, physical events and frozen owners
retain their original constraints. No finite population cap replaces the
permitted ordered private terms. A concrete13-key empty-gap counterexample
would suffice to refute a universal statement; abstract reachability would not.

The principal C32 quantifier is EXC, NOT all PREFIX first-upper branches.
FR31-EN's first-upper13 compensation and possible pre-upper debt2 remain
separate outside-EXC interfaces. No claim that later13 accesses in EXC are
excluded. Such accesses are part of the arbitrary finite return path.
''')
write('FR32_FROZEN_PROOF_BOX.md','''# FR32-CARRY1 — immutable entry proof Box

Target: prove or refute D_out<=1 at FIRST genuine full return7 for every
original-source EXC history as frozen in FR32_FIX_PREFIX_SCOPE_FREEZE.
Equivalently the inherited helper..tau signed total must be>=-1, provided
the exact source-derived debt identity is established. This equivalence
will be proved before using it, not assumed as an invented recurrence.

Conditions: exact original paired source, genuine seven-key/core13/all-SS
scope, actual reachable A shallow frame, all permitted deeper variations,
critical j/HQ guards, weak helper, comb, no genuine low, first upper11/H1,
actual first return and every intermediate original operation/chart cost.
No full source/owner reset at root7, no forced next11 or future depth.

Inheritance: C31 PREFIX counter sigma-1 with local mutable execution and
tuple suffix check, literal W101 and symbolic erased completion; FR31-EN
entry reduction and FR31-CL restricted full funding; C30 low/return/reset
proofs, C29 exact E/degree laws and extremal guard, accepted Step1/CD6 and
conditional Gate U14. All source/owner/audit-pending scopes are immutable.

Ambiguities: additional negative upper helpers, arbitrary return length,
deep A geometry, terminal E/topology/carry, nonidentity flips/charts,
source-realization/closure for any candidate, and normalized owner license.

Bridge: proving suffix sigma>=0 AFTER the first-upper u would prove this
specific carry-one bound (the initial helper..u total is-1). A genuine
source suffix sigma<=-1 would give carry>=2 and refute this sufficient
invariant, not Coarse-Double. Terminal state must retain all information
needed for future source evolution. Global eventual repayment, repeated
carry, all normalized owners and Gate U remain separate OPEN theorems.

Execution gate: inherited source queries1999997/2000000 leave3. Begin with
saved source facts and manuscript derivation. No speculative enumeration,
hidden tree operation or new source compiler is authorized by this freeze.
Any necessary exact query must have a stated target and run under the
unchanged cumulative controller. No new cap or independent allowance.
''')
out('entry.json',{'branch':branch,'head':head,'prior_uniform_CPU':r['cumulative_CPU'],
 'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,
 'global_reserve':5,'controller_reserve':1,'Bank25':25,
 'phase_caps':{'source':20,'independent':90,'proof':20,'algebra':20},
 'phase_query_caps':{'source':3,'independent':3,'proof':0,'algebra':0},
 'inherited_conservative_queries':r['conservative_all_queries'],
 'remaining_conservative_queries':r['conservative_remaining_queries'],'usage_reset':False,
 'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'status':'PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda z:z['path']),
 'external_pins':prior['external_pins']+[{'path':str(directive),'sha256':sha(directive)}]})
write('run_phase.py',(OLD/'run_phase.py').read_text())
print(json.dumps({'status':'C32_FROZEN','branch':branch,'HEAD':head,'pins':len(pins),'query_balance':r['conservative_remaining_queries']}),flush=True)

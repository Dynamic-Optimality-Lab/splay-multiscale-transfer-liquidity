"""Metadata-only source/target/resource freeze. No semantic test."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent;OLD=P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*v):return subprocess.check_output(['git',*v],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
# First research artifact, prior to constructing any new example.
write('MC29_FROZEN_SOURCE_BOX.md','''# MC29 — frozen source Box, first C29 research artifact

2026-11-05. Target: source-valid signed repayment of every actual
H1/Q3/beta3/z1 marked comb, including helpers, their debts, actual frozen
owners, Bank25, both reflections and one legally aligned source period.
The target is not changed when a sufficient proof route fails.

Conditions: original reachable finite A/full-B paired-closed history with
seven genuine KEEP keys/maximal full marked core13. A splays EVERY access;
full B every KEEP/root repeat; DELETE is A-only, not node removal. Ordinary
bottom-up rotations and actual ordered physical keys. Original six-key
erasure and every supplied old f5/f6/common/effective owner retain their
own source domains and absolute IDs. All T19/creator/own-tail/flip rules
and old successes remain. No old certificate is overwritten.

H is total actual A StepEv in a genuine full natural macro, Q its actual
full B doubles; beta counts OLD branching marked ancestors and z indicates
the target's old marked-leaf status in the ACTUAL nearest-marked-ancestor
tree. The inherited SS source hypotheses give Q=u+beta, Delta L=u-z.
Freeze c=min(H,3), D_leaf=L-1 and

    rho=2c-Q+Delta D_leaf=2c-beta-z.

On the comb rho=-2, physical price2H-Q=-1, Delta L=-1. They are distinct.
The leaf-channel comparison reserves one actual death bit; its two branch
frontiers are comparison slots, not automatically two unpaid effective
full demands. A complete physical matching alone does not discharge rho.

Inheritance: accepted original Step1/CD6, conditional Gate U14 and exact
C15 path-to-star/leaf-channel identities at their source scopes; C22 every-
producer creator policy, C23 G=-1/R=0 correction, C24 frozen occupancy,
C25 safe G-v, C26 raw consumer/cycle laws with old qualifications, C27
source existence and C28 witness/family/hybrid/count results. Historical
pending labels are not promoted by pin matching or by finite replay.

The four inherited negative profiles are H1:(Q2,beta2,z1),
(Q3,beta2,z1),(Q4,beta2,z1) of rho-1, and(Q3,beta3,z1) of rho-2.
W199 has58/58 frozen successes, Pempty; do not reopen it. The459-source
refutes the pure catchment partition, not funding. V^mW is only its exact
proved family. No source-valid comb is assumed from a count tuple alone.

Ambiguities: exact realizability of the maximal branching comb; source
force of predecessor repayment; new chart debt on helpers; physical
eligibility/frozen owners; collective closure and broader negative classes.
Bridge: a complete signed mechanism with its helper/owner/storage laws
can discharge the marked-comb component of E_r2/E_r3 at its declared
support scope. It does not alone prove all other profiles, all-r transfer,
Universal CD or Dynamic Optimality. Any countercertificate names exactly
the sufficient mechanism it falsifies, not the original cost conjecture.

Initial authorized cumulative CPU3690.671875/7200; symbolic185.15625/240,
audit304.140625/600. Conservative queries1993089/2000000 leave6911.
No reset/extension/reclassification. Bank25=25, live2M,DAG4M,edges5M,
32GiB,12h, global reserve5/controller1 unchanged. Use existing controller.
''')
prior=read(OLD/'dependency_pins.json');pins={z['path']:z for z in prior['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256'],'origin':'C28_PUBLICATION'}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C28_FINAL_PUBLICATION'}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in prior['external_pins']:assert sha(Path(z['path']))==z['sha256']
directive=Path('C:/Users/Saif malik/.codex/attachments/519d0816-2733-43b6-994c-e16bb520a237/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
r=read(OLD/'resources_checkpoint.json')
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),
    'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],
    'global_allowance':7200,'global_reserve':5,'controller_reserve':1,'Bank25':25,
    'phase_caps':{'source':20,'independent':90,'algebra':20,'classify':20},'inherited_conservative_queries':r['conservative_all_queries'],
    'remaining_conservative_queries':r['conservative_remaining_queries'],'usage_reset':False,
    'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'status':'PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda z:z['path']),
    'external_pins':prior['external_pins']+[{'path':str(directive),'sha256':sha(directive)}]})
write('run_phase.py',(OLD/'run_phase.py').read_text())
print(json.dumps({'status':'C29_FROZEN','pins':len(pins),'remaining_queries':r['conservative_remaining_queries']}))

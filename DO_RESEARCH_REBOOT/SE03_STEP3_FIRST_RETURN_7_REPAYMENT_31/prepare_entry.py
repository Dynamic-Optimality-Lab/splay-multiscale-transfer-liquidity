"""Metadata-only first-return target/resource freeze, no semantic queries."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent;OLD=P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*s):return subprocess.check_output(['git',*s],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
write('FR31_FROZEN_SOURCE_BOX.md','''# FR31 frozen source Box — first C31 research artifact

Target: prove or refute the ACTUAL NH30-FR3 first-return signed law, not an
arbitrary fixed-horizon repair. Start with the original critical Qj2 zero
predecessor, H1/Q2/beta1/z1 degree3-root helper h, and following H1 binary
comb e at the NH30-C physical frame (Y7,R11,x5,Z13). The first genuine
full KEEP7 after h is tau. It is a ROOT return, not return of the full
A/B/owner state. Required signed law is sum_{h..tau} sigma_E>=0, including
all original operations in those genuine macros. Equivalently if L is the
complete low-side macro interval after e before first upper macro u, define
B_pre=-1+sum_L sigma_E and D_entry=max(0,-B_pre). Upper interval u..tau
must contribute at least -B_pre when nonnegative total is the exact target;
the max definition is only the outstanding positive debt, not permission
to erase any positive earlier balance. State any stronger R>=D separately.

Conditions: original reachable finite exactly A/full-B paired-closed source,
seven genuine KEEP marks {1,3,5,7,9,11,13}, maximal marked core13/all-SS,
globally ordered keys and ordinary bottom-up splays. A receives ALL original
KEEP/DELETE; full B all KEEP including root identities; erased B its actual
subsequence. DELETE is not physical deletion. Natural macro cuts and H/Q
are the original ones. Private BST terms and permitted anonymous A ancestry
retain their actual source hypotheses; no ambient population cutoff.
Post-comb B is the exact NH30-C anchor frame with its ordered free gaps.
The actual shallow A prefix has paths L,RL,LL in the concrete control;
its corresponding ordered terms must be retained, not replaced by a chart
representative. Broader first-upper/arity/support classes stay separate.

Return existence: every declared genuine marked key occurs as a changing
KEEP in the closed period. After h the root is11; the first later KEEP7
is genuine and occurs in the cyclic source, within one full period. A
linear fragment stopping sooner has not completed the target. If a legal
cyclic cut is crossed, retain actual occurrence/period correspondence.

Inheritance: rho=2min(H,3)-beta-z, E=L-b-1, sigma_E=2min(H,3)-Q+Delta E.
Helper h is-1 and e0. C30 low bound sum_L sigma_E>=-1 and first upper
target11/13 hold at that exact post-comb source frame. The immediate7
RLR control loses marked-core6 and is NOT a closed-core13 counterexample.
The85-source genuinely has triple0,-1,0; actual four-macro return packet
repays, but no universal four-macro horizon is assumed. W0/W1/U mixed
source/reset/chart theorem and conditional normalized owner profile<=9
extension keep their exact scopes. Accepted Step1/CD6/Gate U14 unchanged.

Ambiguities: exhaustive upper/return paths, low-entry sharpness and A
geometry, actual return boundary E/chart/debt, open-segment versus closed
CD6 correspondence, arbitrary return length, shared intervals, normalized
owner eligibility/retirement/storage. Low debt bounded by2 is not upper
repayment. Source root7 returning is not full source/owner reset.

Bridge: a complete first-return signed law with source/helper/period proof
would repay this particular nonextremal degree3 component of E_r2. It does
not prove all normalized E_r3, alpha4/5, two-ternary helpers or all r. Any
physical funding still needs the ACTUAL supplied normalized a and license;
raw owners are not substitutes. All prior successful fE/f6/a, source,
R1-R4, Bank25 and accepted receipts are immutable.

Entry caps: global3704.46875/7200 CPU; symbolic195.25/240;
audit307.84375/600; queries1999930/2000000, remainder70. No reset or
extension. The new source/audit per-phase query caps are30 each, with all
phases sharing the same70 remainder. Static saved-row/proof analysis has
zero new source queries but remains under the cumulative CPU controller.
''')
prior=read(OLD/'dependency_pins.json');pins={z['path']:z for z in prior['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256'],'origin':'C30_PUBLICATION'}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C30_FINAL_PUBLICATION'}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in prior['external_pins']:assert sha(Path(z['path']))==z['sha256']
directive=Path('C:/Users/Saif malik/.codex/attachments/9f4ae8aa-6ded-4b22-94a2-42a13fcf2c3e/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
r=read(OLD/'resources_checkpoint.json')
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'global_reserve':5,'controller_reserve':1,
    'Bank25':25,'phase_caps':{'source':20,'independent':90,'proof':20,'algebra':20},'phase_query_caps':{'source':30,'independent':30,'proof':0,'algebra':0},
    'inherited_conservative_queries':r['conservative_all_queries'],'remaining_conservative_queries':r['conservative_remaining_queries'],
    'usage_reset':False,'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'status':'PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda z:z['path']),
    'external_pins':prior['external_pins']+[{'path':str(directive),'sha256':sha(directive)}]})
write('run_phase.py',(OLD/'run_phase2.py').read_text())
print(json.dumps({'status':'FR31_FROZEN','pins':len(pins),'queries_remaining':r['conservative_remaining_queries']}),flush=True)

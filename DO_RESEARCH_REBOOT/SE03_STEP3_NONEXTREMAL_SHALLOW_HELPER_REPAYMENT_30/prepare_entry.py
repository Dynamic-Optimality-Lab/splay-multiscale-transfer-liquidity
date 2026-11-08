"""Metadata-only frozen target and cumulative controller entry."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent;OLD=P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
write('NH30_FROZEN_SOURCE_BOX.md','''# NH30 frozen source Box — first C30 research artifact

Target: source-exact signed repayment for the inherited shallow high-arity
helper class, including all helper debt, repeated/shared use, supplied
normalized old f5/f6/effective owners, legal period and Bank25. Do not change
the original target to save a sufficient proof mechanism.

Conditions: original reachable finite exactly A/full-B paired-closed
seven-genuine-KEEP/core13/all-SS source of C29's H29-1 Box. A processes all
KEEP/DELETE operations; full B processes KEEP including root identities;
erased B processes its actual subsequence. DELETE is not physical deletion.
Natural macros retain every original intermediate operation. H counts real
A StepEv, Q full doubles, d target old marked degree, beta branching marked
ancestors, k3 ancestors of marked degree>=3. Shallow means H1, not Q1.
The checkpoint priority class has d0,Q>=2,k3=1, sigma_E=-1. Its high-arity
vertex's degree is >=3; exact supported range must be derived. k3=2 is a
separate -2/two-ternary obligation, not silently included in a proved -1 law.

Nonextremal here means NO opposite-extreme comb endpoint guard is available.
In the priority weak-P-before-comb subcase, actual comb endpoints x,R fail
the all-KEEP opposite-extreme premise; helper's own endpoints are a different
pair. General one-high-arity helpers need not precede any marked comb.
The frozen domain includes the known negative helper control; do not exclude
it merely because its FOLLOWING comb is extremal. Quantifiers remain fixed7;
unbounded arity/support would require another source lift.

Inheritance: C29 rho=2min(H,3)-beta-z and E=L-b-1,
sigma_E=rho+Delta(3-b)=2min(H,3)-Q+Delta E; global per-macro E candidate
REFUTED. MC29-P predecessor classification; MC29-X extremal source barrier
and comparison-level disjoint packets; MC29-F specified raw-canonical
returning-word family complete with frozen full owners/Bank5. Accepted
Step1/CD6 and conditional I(r-1)+E_r=>I(r) retain exact original scopes.
W199 is already58/58 paid,Pempty; W459 partition false but funding complete;
neutral V^mW and original G=-1/R=0 corrections/owners remain frozen.

Ambiguities: source forcing of earlier cost for nonextremal weak helpers;
genuine high-arity geometry/realizability; helper coupling; arbitrary supplied
normalized f5/f6 compatibility and physical eligibility/storage; all-source
composition. A comparison deficit is not automatically an unpaid demand.

Bridge: a source-derived packet/state comparison repaying each negative
helper, INCLUDING costs on zero/positive transitions, combined with literal
old-owner extension, legal-period transport and Bank25 could discharge
that component of E_r2/E_r3 at its proved domain. It does not alone prove
all r, all cores or unconditional Gate U. A failed named architecture is
not a counterexample to Coarse-Double or Dynamic Optimality.

R1-R4, Bank25=25 and all old source/maps/caps unchanged. Entry CPU
3698.765625/7200; symbolic191.109375/240; audit306.28125/600.
Conservative queries1998756/2000000 leave1244. No reset or extension.
''')
prior=read(OLD/'dependency_pins.json');pins={z['path']:z for z in prior['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256'],'origin':'C29_PUBLICATION'}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C29_PUBLICATION_SEAL'}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in prior['external_pins']:assert sha(Path(z['path']))==z['sha256']
directive=Path('C:/Users/Saif malik/.codex/attachments/8232a5eb-5d9b-48eb-8502-465e62d24737/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('xb') as f:f.write(directive.read_bytes())
r=read(OLD/'resources_checkpoint.json')
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'global_reserve':5,'controller_reserve':1,
    'Bank25':25,'phase_caps':{'source':20,'independent':90,'geometry':20,'proof':20},
    'inherited_conservative_queries':r['conservative_all_queries'],'remaining_conservative_queries':r['conservative_remaining_queries'],
    'phase_query_caps':{'source':650,'independent':450,'geometry':0,'proof':0},'usage_reset':False,'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'status':'PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda z:z['path']),
    'external_pins':prior['external_pins']+[{'path':str(directive),'sha256':sha(directive)}]})
# Same inherited CPU/memory/wall controller, additionally pass a conservative
# remaining-query bound to the child and validate its charged exit count.
s=(OLD/'run_phase.py').read_text()
s=s.replace('cap=min(entry[',"qremaining=entry['remaining_conservative_queries']-sum(json.loads(p.read_text()).get('source_queries',0) for p in B.glob('run_*_result.json'))\n    qcap=min(qremaining,entry['phase_query_caps'].get(phase,0));assert qcap>=0\n    cap=min(entry[")
s=s.replace("str(B/('audit_'+phase+'.py')),str(cap)]","str(B/('audit_'+phase+'.py')),str(cap),str(qcap)]")
s=s.replace("and used<cap else 'FAILED_OR_UNKNOWN'","and used<cap and ex.get('source_queries',0)<=qcap else 'FAILED_OR_UNKNOWN'")
s=s.replace("'allocated_child_cap':cap,","'allocated_child_cap':cap,'allocated_query_cap':qcap,")
write('run_phase.py',s)
print(json.dumps({'status':'C30_FROZEN','pins':len(pins),'queries_remaining':r['conservative_remaining_queries']}),flush=True)

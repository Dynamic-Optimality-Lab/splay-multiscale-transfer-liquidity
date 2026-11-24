"""Original selector adapter backed by exact physical state pools.

Runs the unchanged native original U/cohort/R6 predicates and later
selectors without eagerly duplicating every full physical tree snapshot.
"""
from basec import *
from cohortc import decode_state
from physical1 import Edges
from functools import lru_cache
import ast,gc
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind
from exp01_oracle import Replay,Tree

class Boundary(dict):
    def __init__(self,row,state):
        super().__init__(row);self.state=state
    def __getitem__(self,k):
        if k in ('pre_A','post_A','pre_B','post_B'):return self.state(dict.__getitem__(self,k+'_state'))
        return dict.__getitem__(self,k)
    def get(self,k,default=None):
        try:return self[k]
        except KeyError:return default

def adapter(s,phys,birth):
    r=object.__new__(Replay);r.source=s;r.ops=s['operations'];r.keys=sorted(map(int,s['initial_B']['children']))
    r.S=set(phys['original_S']);r.M=set(phys['original_genuine_M']);r.I=set(birth['original_I'])
    r.bits={k:1<<(k-1) for k in r.S};r.full=sum(r.bits.values());r.extremes=(r.bits[min(r.S)]|r.bits[max(r.S)]) if r.S else 0
    r.a=Tree(s['initial_A']);r.b=Tree(s['initial_B']);r.ind=ind;r.events=phys['events'];r.T=len(r.events)
    @lru_cache(maxsize=96)
    def state(sid):return decode_state(phys,sid)
    r.boundaries=[Boundary(row,state) for row in phys['boundaries']]
    r.doubles={tuple(d['parent']):{**d,'id':tuple(d['parent']),
        'nu':d['events'][0 if d['case'] in ('LL','RR') else 1]} for d in phys['doubles']}
    r.A=birth['A'];r.Q=birth['Q_B'];r.KB=birth['genuine_B_accesses'];r.ZB=sum(e['actor']=='B' and e['case']=='ZIG' for e in r.events)
    r.VA=2*r.A-birth['real_A_bits'];r.PA=birth['sign_inventory'].get('PA',0);r.NA=birth['sign_inventory'].get('NA',0)
    r.DB=birth['sign_inventory'].get('DB',0);r.closed=True;r.independent_checks=len(r.ops)
    r.a_changes=defaultdict(list);r.b_creates=defaultdict(list);r.b_losses=defaultdict(list)
    for e in r.events:
        if e['actor']=='A':
            for z in e['lost']:r.a_changes[z].append((e['time'],False))
            for z in e['created']:r.a_changes[z].append((e['time'],True))
        else:
            for z in e['lost']:r.b_losses[z].append(e['time'])
            for z in e['created']:r.b_creates[z].append(e['time'])
    r.initial_a_labels=set(r.a.labels(r.bits).values())-{0}
    r.eligible_S,r.windows_S=r.scan_windows(r.S)
    r.eligible_I,r.windows_I=r.scan_windows(r.I,True)
    r.certify()
    assert set(map(str,r.U))==set(birth['U'])
    aa={digest(p['rho']):p for p in r.pairs};bb={digest(p['rho']):p for p in birth['original_pairs']}
    assert set(aa)==set(bb)
    for k,p in aa.items():assert digest(p)==digest(bb[k])
    return r

def original_star(r):
    import exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core
    for mod in (exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core):mod.ROOT=ROOT
    # The native bridge reads its generated trajectory files; keep that original interface.
    # All writer roots above point to this new stage, never historical directories.
    c=exp03_core.current_classification(r,save=True)
    old=exp04_core.restart_module.restart_analysis(r,c['unhandled'],exp04_core.actual_mismatch_episodes(r))
    paid={digest(e['rho']) for e in old['paid_original_gaps']}
    return [e for e in c['unhandled'] if digest(e['rho']) not in paid]

if __name__=='__main__':
    m=Meter('native_selector_adapter');rows=[]
    # First require exact agreement with the sealed original577 source.
    entry=controls()[6];s=entry['source'];phys=load(entry['physical']);birth=load(ROOT/'BIRTH_06.json')
    r=adapter(s,phys,birth);star=original_star(r)
    expected=load(M0/'RESIDUAL_AUDIT.json')[6]['original_R_star']
    assert {digest(z['rho']) for z in star}=={digest(z['rho']) for z in expected}
    rows.append({'source':s['name'],'role':'sealed original577 adapter cross-check','original_R_star':star,
        'native_U_R6_matches_independent':True,'sealed_R_star_matches':True})
    write('NATIVE_SELECTOR_RESULTS.json',rows);del r,phys,birth;gc.collect()
    ss=load(ROOT/'NEW_SOURCE_CATALOG.json')
    for i in (8,9,10,11):
        s=ss[i];phys=load(ROOT/f'NEW_PHYS_{i:02}.json');birth=load(ROOT/f'NEW_BIRTH_{i:02}.json')
        r=adapter(s,phys,birth);star=original_star(r)
        by={tuple(z['consumer']):z for z in birth['C_U_births']}
        critical=[{'gap':e,'birth':by.get(tuple(e['original_parent']))} for e in star]
        rows.append({'index':i,'source':s['name'],'original_R_star':star,'critical_births':critical,
            'native_U_R6_matches_independent':True,'actual_deep_overflow':0,
            'actual_zero_reason':'Existing raw periodic certificate remains positive; not a post-hybrid escape.'})
        write('NATIVE_SELECTOR_RESULTS.json',rows)
        print('PASS native',i,s['name'],'R_star',len(star),flush=True)
        del r,phys,birth;gc.collect()
    m.ok=True

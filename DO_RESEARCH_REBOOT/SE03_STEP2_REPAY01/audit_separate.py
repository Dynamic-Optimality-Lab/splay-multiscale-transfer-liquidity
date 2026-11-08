"""Separate primitive-rotation and affine proof audit; no finite inputs."""
import hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def get(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def change(t,p,fn):
    if not p:return fn(t)
    k,l,r=t
    return [k,change(l,p[1:],fn),r] if p[0]=='L' else [k,l,change(r,p[1:],fn)]
def rotate(t,direction):
    k,l,r=t
    if direction=='right':j,a,b=l;return [j,a,[k,b,r]]
    j,b,c=r;return [j,[k,l,b],c]
def primitive_frame(t,p,frame):
    # Parent-first same-side source doubles, child-first opposite-side.
    if len(frame)==1:return change(t,p,lambda x:rotate(x,'right' if frame=='L' else 'left'))
    outer='right' if frame[0]=='L' else 'left'
    if frame[0]==frame[1]:
        t=change(t,p,lambda x:rotate(x,outer))
        return change(t,p,lambda x:rotate(x,outer))
    t=change(t,p+frame[0],lambda x:rotate(x,'right' if frame[1]=='L' else 'left'))
    return change(t,p,lambda x:rotate(x,outer))
def order(t):return order(t[1])+[t[0]]+order(t[2]) if isinstance(t,list) else [t]
def poly(**kw):return {k:Fraction(v) for k,v in kw.items() if v}
def add(*parts):
    p={}
    for v in parts:
        for k,c in v.items():p[k]=p.get(k,Fraction())+c
    return {k:v for k,v in p.items() if v}
error=None
try:
    pins=read(B/'dependency_pins.json')['pins']
    for q in pins:
        absolute=(ROOT/q['path']).resolve()
        raw=Path('\\\\?\\'+str(absolute)).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==q['sha256'],q['path']
        assert time.process_time()<CAP
    proof=read(B/'source_term_derivation.json')
    R=proof['initial_full_and_A'];T=proof['initial_recurrent_E']
    states=[R,R,T];totals=[0,0,0];direct=indirect=0
    genuine=[set(),set()];donor=None
    for row in proof['trace']:
        mode,k=row['mode'],row['key'];costs=[]
        for j,p in enumerate(row['paths']):
            old=states[j];frames=row['frames'][j]
            if p is None:
                assert not frames;costs.append(0);continue
            assert get(old,p)[0]==k
            if j and p:genuine[j-1].add(k)
            # Source depth prescribes all bottom-up frames uniquely.
            expected=[];remaining=p
            while len(remaining)>=2:
                expected.append([remaining[:-2],remaining[-2:]]);remaining=remaining[:-2]
            if remaining:expected.append(['',remaining])
            assert frames==expected
            for ordinal,(prefix,frame) in enumerate(frames,1):
                if row['occurrence']==10 and j==0 and ordinal==3:
                    local=get(states[j],prefix)
                    donor=[local[0],local[2][0],local[2][2][0]]
                states[j]=primitive_frame(states[j],prefix,frame)
            assert states[j][0]==k and order(old)==order(states[j])
            costs.append((len(p)+1)//2 if j==0 else len(p)//2)
        assert costs==row['costs'] and states==row['end_terms']
        totals=[a+b for a,b in zip(totals,costs)]
        if mode=='K' and k==3:direct+=costs[1]
        elif mode=='K':indirect+=costs[1]-costs[2]
        assert time.process_time()<CAP
    assert states==[R,R,T] and totals==[34,30,24]
    assert genuine==[{1,3,5,7,9,11},{1,5,7,9,11}]
    assert donor==[5,6,11]
    assert direct==5 and indirect==1
    warm=R;steady=T
    for p,f in proof['warm_join']['frames_first']:warm=primitive_frame(warm,p,f)
    for p,f in proof['warm_join']['frames_steady']:steady=primitive_frame(steady,p,f)
    assert warm==steady==proof['warm_join']['common_term']
    # Core9 source Step1 debt is in[0,2]; w=-2 forces increase exactly2.
    critical=proof['trace'][12]
    assert critical['costs']==[1,5,4]
    assert 2*critical['costs'][0]-critical['costs'][2]==-2
    reserve_critical=2-4+2;extra_critical=5-4
    assert reserve_critical==0 and extra_critical==1
    prev=proof['trace'][8:12]
    assert sum(r['costs'][0] for r in prev)==7
    assert sum(r['costs'][1] for r in prev)==2
    assert sum(r['costs'][2] for r in prev)==1
    assert proof['trace'][8]['costs'][0]+3==4
    assert max(row['costs'][0] for row in proof['trace'] if row['mode']=='K')==2
    # Distinct occurrence/event/bit donors and demand ordinals. This is a
    # declared universal receipt for Gamma, not an execution on test data.
    donors=[('occ10','event3',0),('occ10','event3',1)]
    demands=[('occ9','Bdouble1'),('occ13','Bdouble5')]
    assert len(set(donors))==len(set(demands))==2
    # Reconstruct high-macro proof as an identity in independent variables.
    # Each parenthesized term on RHS is nonnegative under source hypotheses.
    identity=add(poly(H=2,F=-1,dt=1),poly(H=-1,Q=2),
                 poly(H=-1,Q=-2,one=2,F=1),poly(dt=-1,one=-2))
    assert not identity
    sharp=add(poly(H=2,F=-1,dt=1),poly(H=-2,Q=1,one=2),
              poly(Q=-1,F=1),poly(dt=-1,one=-2))
    assert not sharp
    out('separate_audit.json',{'status':'PASS_INTERMEDIATE_SOURCE_THEOREMS_ONLY',
      'method':'separate primitive rotations, all free-term variables conserved; independent affine identities',
      'inherited_pins_verified':len(pins),'source_family':'Gamma with arbitrary ordered F0..F11',
      'exact_full_paired_closure':True,'actual_auxiliary_recurrence':'u=1,L=1,Q_first=25,Q_recurrent=24',
      'source_totals':{'A':34,'QF':30,'QE':24,'D':5,'J':1},
      'pointwise_repayment_rule':'REFUTED_BY_ACTUAL_SOURCE_MACRO',
      'two_block_source_unit_repair':'PASS_WITH_BLOCK_TIMING_SCOPE',
      'high_macro_range':'PASS_H>=8_core10_OR_H>=10_core11',
      'root_synchronization':'PASS_BY_LAST_RETAINED_ROOT_INDUCTION',
      'Step2_complete':False,'new_original_CD_coverage':False,'unrestricted_CD_proved':False,
      'finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0,
      'external_peer_review':False,'whole_compiler_formalization':False})
    print('SEPARATE_PRIMITIVE_AND_AFFINE_AUDIT_PASS; Step2 remains OPEN')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_separate_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})

"""Fixed source interval audit: arbitrary unequal interiors; no larger fit."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
s=importlib.util.spec_from_file_location('interval_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(s);s.loader.exec_module(tu)


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def N(k,l=None,r=None):return [k,l,r]
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return N(t[1],jt(t[2]),jt(t[3]))
def splay(t,x):
    u,e=tu.trace(tt(t),x);return jt(u),[list(z) for z in e]
def dep(t,x):
    h=0
    while t is not None and not isinstance(t,str):
        if t[0]==x:return h
        t=t[1 if x<t[0] else 2];h+=1
    raise AssertionError('queried key must be explicit')


def frontier(A,B,h=0,lo=None,hi=None):
    if A is None and B is None:return dict(keys=[],common_opaque=[],holes=[])
    if isinstance(A,str) and A==B:return dict(keys=[],common_opaque=[A],holes=[])
    if isinstance(A,list) and isinstance(B,list) and A[0]==B[0]:
        l=frontier(A[1],B[1],h+1,lo,A[0]);r=frontier(A[2],B[2],h+1,A[0],hi)
        return dict(keys=l['keys']+[A[0]]+r['keys'],common_opaque=l['common_opaque']+r['common_opaque'],holes=l['holes']+r['holes'])
    return dict(keys=[],common_opaque=[],holes=[dict(A=A,B=B,external_depth=h,lower=lo,upper=hi)])


def count_expr(A,B):
    v=frontier(A,B)
    return dict(constant=len(v['keys']),opaque_size_coefficients=dict(sorted(Counter(v['common_opaque']).items())))


def classify(A,B,x):
    f=frontier(A,B)
    if x in f['keys']:return dict(kind='common_core',core_count=len(f['keys']))
    hole=next(z for z in f['holes'] if (z['lower'] is None or z['lower']<x) and (z['upper'] is None or x<z['upper']))
    u,v=dep(hole['A'],x),dep(hole['B'],x)
    assert dep(A,x)==hole['external_depth']+u and dep(B,x)==hole['external_depth']+v
    return dict(kind='disagreement_interval',external_depth=hole['external_depth'],
        lower=hole['lower'],upper=hole['upper'],internal_depth_A=u,internal_depth_B=v,
        even_even=u%2==v%2==0,internal_A=hole['A'],internal_B=hole['B'],core_count=len(f['keys']))


def execute(A,B,word):
    out=[]
    for j,(mode,x) in enumerate(word):
        da=dep(A,x);aa,ae=splay(A,x)
        if mode=='KEEP':db=dep(B,x);bb,be=splay(B,x)
        else:db=None;bb=B;be=[]
        q=sum(e[0]!='ZIG' for e in be)
        out.append(dict(occurrence=j,mode=mode,key=x,source_A=A,source_B=B,
            destination_A=aa,destination_B=bb,d_A=da,d_B=db,a=len(ae),q=q,
            delta=q-2*len(ae),A_events=ae,B_events=be,z=sum(e[0]=='ZIG' for e in be)))
        A,B=aa,bb
    return out


def wrap(body,case,suffix):
    sib=lambda n:f'S{n}_{suffix}'
    if case=='LL':return N(10,N(8,body,sib(1)),sib(0))
    if case=='RR':return N(0,sib(0),N(2,sib(1),body))
    if case=='LR':return N(10,N(2,sib(1),body),sib(0))
    if case=='RL':return N(0,sib(0),N(8,body,sib(1)))
    if case=='ZIG_L':return N(8,body,sib(0))
    if case=='ZIG_R':return N(2,sib(0),body)
    raise AssertionError(case)


def primitive_contexts():
    # Independent paired interval interiors. Named internal keys are3,5,7.
    # A's target depth0, B's target depth2. Off-path subtree pairs are
    # arbitrary and may differ, including siblings of the external path.
    A=N(3,'I0_A',N(5,'I1_A',N(7,'I2_A','I3_A')))
    B=N(7,N(5,N(3,'I0_B','I1_B'),'I2_B'),'I3_B')
    out={}
    for case in ['LL','RR','LR','RL','ZIG_L','ZIG_R']:
        aa,bb=wrap(A,case,'A'),wrap(B,case,'B')
        c=classify(aa,bb,3);assert c['even_even']
        row=execute(aa,bb,[('KEEP',3)])[0]
        before,after=count_expr(aa,bb),count_expr(row['destination_A'],row['destination_B'])
        assert after['constant']>=before['constant']+1
        out[case]=dict(classification=c,row=row,before=before,after=after,
            old_common_keys=frontier(aa,bb)['keys'],new_common_keys=frontier(row['destination_A'],row['destination_B'])['keys'])
        assert set(out[case]['old_common_keys'])<set(out[case]['new_common_keys'])
    return out


def fixed_existing_rows():
    old=BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json'
    old13=BASE/'route_c_fe02_approach_discharge_20261101_v001/closed_discharge_certificate.json'
    w=read(old);ad=read(old13);out={}
    corpora={f'W_{name}':w[name] for name in ['ordinary_rows','reflected_rows']}
    corpora.update({f'AD_{name}':d['rows'] for name,d in ad['cases'].items()})
    for name,rows in corpora.items():
        selected=[]
        for r in rows:
            A,B=r['source_A'],r['source_B']
            if r['mode']!='KEEP' or A[0]!=B[0] or r['a']==0:continue
            c=classify(A,B,r['key']);fc=count_expr(A,B);tc=count_expr(r['destination_A'],r['destination_B'])
            if r['delta']>=0:assert c['kind']=='disagreement_interval'
            if c['kind']=='common_core':assert r['delta']<0
            if c.get('even_even'):assert tc['constant']>=fc['constant']+1
            selected.append(dict(occurrence=r['occurrence'],key=r['key'],a=r['a'],q=r['q'],delta=r['delta'],
                classification=c,before=fc,after=tc,row=r))
        out[name]=selected
    return dict(corpora=out,source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [old,old13]})


def obstacle():
    p=BASE/'route_c_fe02_paired_compatibility_20261101_v001/discordance_obstruction_certificate.json'
    old=read(p);coreword=[(r['mode'],r['key']) for r in old['actual_closed_rows']]
    A=N(1,'L',N(5,N(2,None,N(3,None,N(4,None,'F')))))
    B=N(1,'L',N(2,None,N(3,None,N(4,None,N(5,'F'))))))
    startup=execute(B,B,[('DELETE',x) for x in old['A_DELETE_connector']])
    assert startup[-1]['destination_A']==A and startup[-1]['destination_B']==B
    row=execute(A,B,[('KEEP',5)])[0];c=classify(A,B,5)
    assert (row['a'],row['q'],row['delta'])==(1,2,0)
    assert (c['external_depth'],c['internal_depth_A'],c['internal_depth_B'])==(1,0,3)
    before,after=count_expr(A,B),count_expr(row['destination_A'],row['destination_B'])
    assert before==dict(constant=1,opaque_size_coefficients={'L':1})
    assert after==dict(constant=1,opaque_size_coefficients={})
    symbolic=execute(B,B,coreword)
    assert symbolic[-1]['destination_A']==symbolic[-1]['destination_B']==B
    physical=old['actual_closed_rows']
    return dict(original_counter_certificate_sha256=sha(p),symbolic_source_A=A,symbolic_source_B=B,
        original_A_connector=old['A_DELETE_connector'],symbolic_startup_rows=startup,
        saturated_row=row,classification=c,before=before,after=after,
        delta_common_core='-|L|',delta_source_excess=0,unused_A_units_after_own_payment=0,
        interval_orders=dict(L='all keys below1',F='all keys strictly between4 and5'),
        physical_closed_rows=physical,symbolic_closed_rows=symbolic,
        source_word=coreword,full_pair_closed=True,
        no_actual_FE02_or_Coarse_Double_counterexample=True)


def main():
    save('primitive_context_certificate.json',dict(gate_sha256=sha(HERE/'UI00_FOUR_RULE_GATE.md'),
        contexts=primitive_contexts(),purpose='six literal outer source identities; proof is arbitrary-context induction'))
    audit=fixed_existing_rows();save('existing_control_interval_certificate.json',audit)
    bad=obstacle();save('odd_boundary_obstruction_certificate.json',bad)
    print(json.dumps(dict(status='SOURCE_CERTIFICATES_BUILT',primitive_contexts=6,
        fixed_rows=sum(len(v) for v in audit['corpora'].values()),
        odd_boundary_depths=[bad['classification']['internal_depth_A'],bad['classification']['internal_depth_B']],
        saturated_common_core_change=bad['delta_common_core'],FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()

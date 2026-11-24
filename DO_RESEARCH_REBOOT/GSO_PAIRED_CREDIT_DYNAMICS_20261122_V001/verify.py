"""Independent complete original replay, size coefficients and resource sharing.

Imports no new source generator, gap solver, learner, policy or reserve code.
The physical primitive is pinned old immutable bottom-up splay.
"""
import sys
import json
import gzip
import importlib.util
from collections import Counter,deque
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('paired_credit_immutable_physical',
    HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def read(name):
    p=HERE/name
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def nodes(t):
    stack=[t]
    while stack:
        x=stack.pop()
        if x is not None:yield x;stack.extend((x.l,x.r))


def histogram(A,B):
    aset={(v.lo,v.hi) for v in nodes(A)}
    return Counter(v.hi-v.lo+1 for v in nodes(B) if (v.lo,v.hi) not in aset)


def diff(a,b):return {str(k):a[k]-b[k] for k in a.keys()|b.keys() if a[k]!=b[k]}


def geometry(z,saved,q):
    source=z['source'];m=16*(q+1)+1;embedding=source['embedding'];gaps=embedding['gap_sizes']
    assert len(gaps)==m+1
    expected=[0]*(m+1);expected[m-6]=4
    for j in range(q):expected[16*(q-j)-5]=16*(2**j-1)
    assert gaps==expected
    mapping={};shift=0
    for k in range(1,m+1):shift+=gaps[k-1];mapping[k]=k+shift
    assert {int(k):v for k,v in embedding['mapping'].items()}==mapping
    base=[['D',k] for k in range(2,m+1)]
    base += [['K' if k in (m,m-1,m-3,m-7) else 'D',k] for k in range(m,0,-1)]
    base += [['K',k] for k in range(1,m+1)]+[['K',k] for k in range(m-1,0,-1)]
    assert source['operations']==[[mode,mapping[k]] for mode,k in base]
    assert source['prefix']==[] and source['initial_A']==source['initial_B']==source['diagonal']
    assert len(source['initial_A']['children'])==16*2**q+5
    active=set(mapping.values())
    assert {x for mode,x in source['operations'] if mode=='K'}==active
    assert all(b['promoted'] in active and b['demoted'] in active for s in z['steps'] for b in s['bits'])
    A=V.immutable(source['initial_A']);B=V.immutable(source['initial_B']);at=m+7
    for mode,x in source['operations'][:at-1]:
        A,_=V.V.rebuild(A,x,lambda *args:None,lambda *args:None)
        if mode=='K':B,_=V.V.rebuild(B,x,lambda *args:None,lambda *args:None)
    before=histogram(A,B);target=source['operations'][at-1][1]
    A,depth=V.V.rebuild(A,target,lambda *args:None,lambda *args:None);assert depth==1
    assert diff(before,histogram(A,B))==saved['A_phase_delta']=={}
    aset={(v.lo,v.hi) for v in nodes(A)};deltas={};profiles={}
    def emit(step,bit,typ,promoted,pivot,demoted):
        counter=deltas.setdefault(step,Counter())
        if (promoted.lo,promoted.hi) not in aset:counter[promoted.hi-promoted.lo+1]+=1
        if (demoted.lo,demoted.hi) not in aset:counter[demoted.hi-demoted.lo+1]-=1
        if typ=='RR' and bit==0:
            x=promoted.r;assert x.k==target
            size=lambda v:0 if v is None else v.hi-v.lo+1
            profiles[step]={'a':size(pivot.l),'b':size(promoted.l),'c':size(x.l),'d':size(x.r)}
    B,depth=V.V.rebuild(B,target,emit,lambda *args:None)
    assert depth==2*q+2
    for row in saved['B_steps']:
        step=row['id'][2];actual={str(k):v for k,v in deltas[step].items() if v}
        assert actual==row['delta_Phi_w_coefficients']
        if row['type']=='RR':
            assert profiles[step]==row['branch_sizes']
            j=step-1;c=16*2**j-9
            assert profiles[step]=={'a':7,'b':c,'c':c,'d':7} and actual=={}
    whole=diff(before,histogram(A,B));assert whole==saved['whole_operation_delta_Phi_w_coefficients']
    assert whole=={str(16*2**q-1):1,str(16*2**q+1):1}
    return {'original_RR_size_aliases':q,'whole_Phi_w_coefficients':whole,'new_carrier_vertices':0}


def priorities(z,tape):
    owner={key:i for i,block in enumerate(z['blocks']) for key in block};steps={tuple(s['id']):s for s in z['steps']};out=[]
    for e in tape:
        op=z['operations'][e['id'][1]-1];target=op['target']
        order=[owner[target]]+[b for b in sorted(e['scope']) if b!=owner[target]]
        if e['id'][0]=='B' and steps[tuple(e['id'])]['type'] in ('LL','RR'):
            f,s=steps[tuple(e['id'])]['bits'];order=[]
            for key in (target,s['middle'],f['grandparent'],f['demoted'],s['demoted'],f['middle']):
                if key is not None and owner[key] not in order:order.append(owner[key])
        assert set(order)==set(e['scope']);out.append((e,order))
    return out


def local_credit(z,tape,saved):
    H=5;compiled=priorities(z,tape)
    def run(start,record=False):
        bank=list(start);rows=[];issued=paid=0;failures=[]
        for index,(e,order) in enumerate(compiled):
            before=[bank[b] for b in order];mass=sum(before)
            if e['a'] or e['k']:after=[H]*len(order);issue=sum(after)-mass;pay=unpaid=0
            else:
                pay=min(mass,e['q']);unpaid=e['q']-pay;rest=mass-pay;issue=0
                after=[min(H,max(0,rest-i*H)) for i in range(len(order))]
            assert sum(after)-mass==issue-pay
            for block,value in zip(order,after):bank[block]=value
            issued+=issue;paid+=pay
            if unpaid:failures.append(index)
            if record:rows.append({'event':index,'id':e['id'],'priority':order,'before':before,'after':after,'issued':issue,'paid':pay,'unpaid':unpaid})
        return bank,issued,paid,failures,rows
    start=[H]*len(z['blocks']);passes=[]
    for lap in range(len(start)*H+1):
        new,issue,pay,fail,_=run(start);assert all(x<=y for x,y in zip(new,start))
        passes.append({'pass':lap,'mass_before':sum(start),'mass_after':sum(new),'unpaid':z['Q_B']-pay})
        if new==start:break
        start=new
    else:raise AssertionError('local rank descent')
    end,issue,pay,fail,rows=run(start,True)
    assert end==start and issue==pay and start==saved['initial_greatest_fixed_point']
    assert passes==saved['period_passes'] and rows==saved['rows'] and pay==saved['paid']
    assert len(fail)==len(saved['failures'])==0
    # Distinct original cyclic KEEP gaps justify the real-A voucher interface.
    keeps=[o['id'] for o in z['operations'] if o['k']];used=set();length=len(z['operations'])
    for i,current in enumerate(keeps):
        previous=keeps[i-1];cursor=previous%length+1;found=None
        while True:
            o=z['operations'][cursor-1]
            for step in z['steps'][o['steps'][0]:o['steps'][1]]:
                if step['a'] and found is None:found=tuple(step['id'])
            if cursor==current:break
            cursor=cursor%length+1
        assert found is not None and found not in used;used.add(found)
    assert len(used)==z['K_B']<=z['A']
    return {'local_paid':pay,'local_actual_issued':issue,'unpaid':len(fail)}


def global_credit(z,tape,saved):
    assert saved['C']==4;word=[e['q']-4*e['a'] for e in tape];n=len(word)
    assert sum(word)==z['Q_B']-4*z['A']<0
    # Different complete algorithm from the producer: inspect every cyclic
    # interval directly; no deque, optimiser, or producer reserve function.
    maximum=0
    for start in range(n):
        value=0
        for length in range(1,n+1):
            value+=word[(start+length-1)%n];maximum=max(maximum,value)
    assert maximum==saved['capacity']
    cut=saved['max_cyclic_deficit'];assert 0<=cut['start']<n and 0<=cut['length']<=n
    assert sum(word[(cut['start']+j)%n] for j in range(cut['length']))==maximum
    G=saved['initial_greatest_fixed_point'];initial=G;issued=paid=0;rows=[]
    queue=deque(saved['boundary_credit_labels']);assignments=[];ids={tuple(e['id']):e for e in tape}
    for token in queue:assert tuple(token[:-1]) in ids and ids[tuple(token[:-1])]['a'] and 0<=token[-1]<4
    for e in tape:
        old=G
        if e['a']:
            G=min(maximum,G+4);issue=G-old;pay=0
            for slot in range(issue):queue.append([*e['id'],slot])
        else:
            assert G>=e['q'];pay=e['q'];G-=pay;issue=0
            for _ in range(pay):assignments.append({'B':e['id'],'A_credit':queue.popleft()})
        rows.append({'id':e['id'],'before':old,'after':G,'issued':issue,'paid':pay,'unpaid':0});issued+=issue;paid+=pay
    assert G==initial and issued==paid==z['Q_B']
    assert rows==saved['rows'] and assignments==saved['credit_assignments'] and list(queue)==saved['boundary_credit_labels']
    credits=[tuple(a['A_credit']) for a in assignments];assert len(set(credits))==len(credits)
    assert Counter(tuple(a['B']) for a in assignments)==Counter({tuple(e['id']):e['q'] for e in tape if e['q']})
    assert max(Counter(c[:-1] for c in credits).values())<=4
    return {'global_C4_capacity':maximum,'global_paid':paid,'global_actual_issued':issued,'original_A_credit_slots_unique':True}


def main():
    rows=[]
    for case in read('COMPLETE_SOURCE_AUDIT.json')['cases']:
        q=case['q'];z=read(case['trace']);tape,stats=V.physical(z)
        assert z['A']==64*(q+1) and z['Q_B']==28*q+25
        g=geometry(z,read(case['energy']),q)
        local=local_credit(z,tape,read(case['local_bank']));global_=global_credit(z,tape,read(case['global_credit']))
        rows.append({'q':q,'physical_support':len(z['source']['initial_A']['children']),**stats,**g,**local,**global_})
        print(json.dumps({'q':q,'full_original_source_verified':True,'size_aliases':q,'cyclic_credit_verified':True}),flush=True)
    result={'passed':True,'complete_original_sources':len(rows),'operations':sum(r['operations'] for r in rows),
        'real_rotations':sum(r['real_rotations'] for r in rows),'cases':rows,
        'scope':'Independent original physical events, full pair closure, full-X size coefficients, exact selected local bank, every cyclic reserve interval and unique original-A credit assignment. No producer, gap optimizer, learner or reserve-code import.',
        'new_UF_escape_claim':False,'original_source_counterexample_to_CD':False,
        'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'INDEPENDENT_VERIFICATION.json'
        if p.exists():assert json.loads(p.read_text())==result
        else:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('passed','complete_original_sources','operations','real_rotations','universal_CD')}))


if __name__=='__main__':main()

"""Independent full original source and hybrid global-overflow replay."""
import sys
import json
import gzip
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('joint_original_independent',
          HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def read(path):
    with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:return json.load(f)


def independent_hybrid(z,events,saved):
    p=saved['parameters'];H=p['bank_capacity'];N=sum(map(len,z['blocks']));cap=p['global_capacity_scale']*N
    owner={x:i for i,part in enumerate(z['blocks']) for x in part};steps={tuple(s['id']):s for s in z['steps']}
    prepared=[]
    for e in events:
        x=z['operations'][e['id'][1]-1]['target'];order=[owner[x]]+[i for i in sorted(e['scope']) if i!=owner[x]]
        if p['priority']==1 and e['id'][0]=='B' and steps[tuple(e['id'])]['type'] in ('LL','RR'):
            f,s=steps[tuple(e['id'])]['bits'];order=[]
            for key in (x,s['middle'],f['grandparent'],f['demoted'],s['demoted'],f['middle']):
                if key is not None and owner[key] not in order:order.append(owner[key])
        assert set(order)==set(e['scope']);prepared.append((e,order))
    def run(initial,record=False):
        bank=initial[:-1].copy();G=initial[-1];rows=[];paid=issued=overflow=unfunded=0
        for e,order in prepared:
            before=[bank[i] for i in order];mass=sum(before);old=G
            if e['a'] or e['k']:
                after=[H for _ in order];G=min(cap,G+(p['extra_A_allowance'] if e['a'] else p['overflow_ticket']))
                issue=H*len(order)-mass+G-old;pb=pg=u=0
                assert 0<=issue<=(p['A_coefficient'] if e['a'] else p['KEEP_coefficient'])
            else:
                pb=min(e['q'],mass);u=e['q']-pb;pg=min(G,u);G-=pg;issue=0
                after=[min(H,max(0,mass-pb-H*j)) for j in range(len(order))]
            assert sum(after)-mass+G-old==issue-pb-pg
            for i,v in zip(order,after):bank[i]=v
            paid+=pb+pg;issued+=issue;overflow+=u;unfunded+=u-pg
            if record:rows.append({'id':e['id'],'scope':order,'local_before':before,'local_after':after,
                                  'global_before':old,'global_after':G,'issued':issue,'bank_paid':pb,
                                  'bank_unpaid':u,'overflow_paid':pg,'unfunded':u-pg})
        return bank+[G],{'paid':paid,'issued':issued,'bank_unpaid':overflow,'unfunded':unfunded,'rows':rows}
    state=[H]*len(z['blocks'])+[cap];passes=[]
    for _ in range(len(z['blocks'])*H+cap+1):
        new,r=run(state);assert all(a<=b for a,b in zip(new,state));passes.append([sum(state),sum(new)])
        if new==state:break
        assert sum(new)<sum(state);state=new
    else:raise AssertionError('rank descent')
    final,r=run(state,True);assert final==state and r['paid']==r['issued']
    assert state==saved['initial_greatest_fixed_point'] and passes==saved['passes']
    assert all(r[key]==saved[key] for key in r)
    # Validate the once-per-genuine-KEEP original A resource injection.
    keeps=[op['id'] for op in z['operations'] if op['k']];used=set();length=len(z['operations'])
    for j,op in enumerate(keeps):
        previous=keeps[j-1];at=previous%length+1;chosen=None
        while True:
            record=z['operations'][at-1]
            for step in z['steps'][record['steps'][0]:record['steps'][1]]:
                if step['a'] and chosen is None:chosen=tuple(step['id'])
            if at==op:break
            at=at%length+1
        assert chosen is not None and chosen not in used;used.add(chosen)
    assert len(used)==z['K_B']<=z['A']
    return {key:r[key] for key in ('paid','issued','bank_unpaid','unfunded')}


def main():
    summary=read(HERE/'AUDIT_SUMMARY.json');cases=[];operations=rotations=0
    for row in summary['controls']+[{'tag':'unrestricted_C1'}]:
        tag=row['tag'];z=read(HERE/f'audit/{tag}_trace.json.gz');saved=read(HERE/f'audit/{tag}_hybrid.json.gz')
        events,stats=V.physical(z);result=independent_hybrid(z,events,saved)
        support={x for mode,x in z['source']['operations'] if mode=='K'}
        if tag!='unrestricted_C1':assert len(support)<=2 and result['unfunded']==0 and z['Q_B']<=z['A']
        else:assert z['Q_B']==6 and z['A']==4 and result['unfunded']>0
        operations+=stats['operations'];rotations+=stats['real_rotations']
        cases.append({'tag':tag,**stats,**result})
    other=read(HERE/'ORIGINAL_OTHER_TARGET_WITNESS.json');path=ROOT/other['trace']['path'];hz=read(path)
    _,stats=V.physical(hz);operations+=stats['operations'];rotations+=stats['real_rotations']
    trees={a:V.immutable(hz['source']['initial_'+a]) for a in ('A','B')}
    at=other['burst']['id']
    for mode,x in hz['source']['operations'][:at-1]:
        for a in ('A','B') if mode=='K' else ('A',):trees[a],_=V.V.rebuild(trees[a],x,lambda *x:None,lambda *x:None)
    target=other['burst']['target'];cur=trees['B'];depth=0
    while cur.k!=target:cur=cur.l if target<cur.k else cur.r;depth+=1
    assert depth//2==other['burst']['Q_B_cost'] and trees['B'].k==other['burst']['current_B_root']
    assert target not in (other['burst']['current_B_root'],other['burst']['previous_B_root'])
    result={'passed':True,'complete_sources':9,'operations':operations,'real_rotations':rotations,
            'controls':cases,'real_other_target_depth':depth,'scope':'Independent full physical/prefix/paired-closure and hybrid-account verification. No new U/Pi escape is asserted.',
            'zero_bank_unpaid_required':False,'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'INDEPENDENT_AUDIT_VERIFICATION.json'
        if p.exists():assert read(p)==result
        else:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('passed','complete_sources','operations','real_rotations','real_other_target_depth','universal_CD')}))


if __name__=='__main__':main()

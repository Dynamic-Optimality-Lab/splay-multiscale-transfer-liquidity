"""Complete original controls and historical root rejection witnesses.

Actual physical source compilation is pinned old code. Every new source and
the hybrid bank are independently rechecked in verify_audit.py.
"""
import sys
import json
import gzip
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001'
sys.path.insert(0,str(PREV));import transport as T;sys.path.pop(0)


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    p=HERE/name;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
    with (gzip.open(p,'wt',encoding='utf-8') if p.suffix=='.gz' else p.open('w',encoding='utf-8')) as f:json.dump(value,f)


def inverse_source(n):
    ch={};middle=(n+1)//2
    def gap(lo,hi):
        if lo>hi:return None
        key=(lo+hi)//2;ch[str(key)]=[gap(lo,key-1),gap(key+1,hi)];return key
    lower=gap(2,middle-1);upper=gap(middle+1,n-1)
    ch['1']=[None,middle];ch[str(middle)]=[lower,n];ch[str(n)]=[upper,None]
    tree={'root':1,'children':ch}
    return {'name':f'two_target_inverse_with_full_hangers_N{n}','initial_A':tree,'initial_B':tree,
            'diagonal':tree,'prefix':[],'operations':[['K',n],['K',1]],'expected_A':2,'expected_Q':2}


def interleaved_source(n):
    vine={'root':1,'children':{str(k):[None,k+1 if k<n else None] for k in range(1,n+1)}}
    trees={a:T.B.K.OLD.Tree(vine,list(range(1,n+1))) for a in ('A','B')};prefix=[]
    word=[['K',n],['D',(n+1)//2],['D',2],['K',1]]
    word += [['D',k] for k in range(1,n+1)]+[['D',k] for k in range(n-1,0,-1)]
    def execute(ops):
        for mode,x in ops:
            T.B.K.OLD.plain(trees['A'],x)
            if mode=='K':T.B.K.OLD.plain(trees['B'],x)
    seen={};states=[]
    for lap in range(12):
        state={a:trees[a].state() for a in trees};finger=json.dumps(state,sort_keys=True)
        if finger in seen:
            first=seen[finger]
            return {'name':f'two_target_private_A_interleaving_N{n}',
                    'initial_A':state['A'],'initial_B':state['B'],'diagonal':vine,
                    'prefix':word*first,'operations':word*(lap-first)}
        seen[finger]=lap;states.append(state);execute(word)
    raise AssertionError('bounded reaching-cycle construction did not stabilize')


def hybrid(z,p):
    H=p['bank_capacity'];N=sum(map(len,z['blocks']));cap=p['global_capacity_scale']*N
    events=T.B.events(z);steps={tuple(s['id']):s for s in z['steps']}
    if p['priority']==1:
        # This is the pinned current-role policy, not a newly invented order.
        sys.path.insert(0,str(PREV));import role_synthesis as R;sys.path.pop(0)
        events,_=R.prepared(z,('middle2','external','grandparent','parent'))
    def sweep(initial,record=False):
        local=initial[:-1].copy();G=initial[-1];rows=[];paid=issued=overflow=unfunded=0
        for j,e in enumerate(events):
            before=[local[i] for i in e['priority']];mass=sum(before);oldG=G
            if e['a'] or e['k']:
                after=[H]*len(before);G=min(cap,G+(p['extra_A_allowance'] if e['a'] else p['overflow_ticket']))
                issue=sum(after)-mass+G-oldG;pb=pg=u=0
                assert issue<=(p['A_coefficient'] if e['a'] else p['KEEP_coefficient'])
            else:
                pb=min(mass,e['q']);remaining=mass-pb
                after=[min(H,max(0,remaining-i*H)) for i in range(len(before))]
                u=e['q']-pb;pg=min(G,u);G-=pg;issue=0
            for block,v in zip(e['priority'],after):local[block]=v
            assert sum(after)-mass+G-oldG==issue-pb-pg
            paid+=pb+pg;issued+=issue;overflow+=u;unfunded+=u-pg
            if record:rows.append({'id':e['id'],'scope':e['priority'],'local_before':before,'local_after':after,
                                  'global_before':oldG,'global_after':G,'issued':issue,
                                  'bank_paid':pb,'bank_unpaid':u,'overflow_paid':pg,'unfunded':u-pg})
        return local+[G],{'paid':paid,'issued':issued,'bank_unpaid':overflow,'unfunded':unfunded,'rows':rows}
    state=[H]*len(z['blocks'])+[cap];passes=[]
    for lap in range(len(z['blocks'])*H+cap+1):
        new,r=sweep(state);assert all(a<=b for a,b in zip(new,state));passes.append([sum(state),sum(new)])
        if new==state:break
        assert sum(new)<sum(state);state=new
    else:raise AssertionError('finite coupled monotone descent failed')
    final,r=sweep(state,True);assert final==state and r['paid']==r['issued']
    return {'parameters':p,'initial_greatest_fixed_point':state,'passes':passes,'closed':True,**r}


def main():
    candidate=json.loads((HERE/'run_003/CONTROL_CERTIFICATE.json').read_text())['candidate'];rows=[]
    sources=[inverse_source(n) for n in (3,33,257,1025)]+[interleaved_source(n) for n in (33,129,257)]
    for i,source in enumerate(sources):
        z=T.F.compile_source(source);cert=hybrid(z,candidate)
        assert len({x for mode,x in source['operations'] if mode=='K'})<=2 and not cert['unfunded']
        assert cert['bank_unpaid']==z['Q_B']>0
        write(f'audit/control_{i:02d}_trace.json.gz',z);write(f'audit/control_{i:02d}_hybrid.json.gz',cert)
        rows.append({'tag':f'control_{i:02d}','name':source['name'],'keys':sum(map(len,z['blocks'])),
                     'operations':len(source['operations']),'A':z['A'],'Q_B':z['Q_B'],
                     'bank_unpaid':cert['bank_unpaid'],'overflow_paid':cert['paid'],'unfunded':cert['unfunded']})
    # A historical, complete original witness forbids promoting the scoped C=1
    # proof to an unrestricted statement. It does not reject every finite C.
    path=T.TRACE/'run_001/trace_00.json.gz';z=T.load(path);cert=hybrid(z,candidate)
    assert z['Q_B']>z['A'] and cert['unfunded']>0
    write('audit/unrestricted_C1_trace.json.gz',z);write('audit/unrestricted_C1_hybrid.json.gz',cert)
    # Required target-OTHER branch is real: use a complete original H source,
    # retain every counted operation and identify an A=1, arbitrarily scalable B burst.
    hpath=T.PREV/'scaling_001/trace_16.json.gz';hz=T.load(hpath);oldroot=hz['source']['initial_B']['root'];previous=None;burst=None
    for op in hz['operations']:
        if op['mode']=='K':
            target=op['target']
            if target not in (oldroot,previous) and op['a']==1 and op['q']>2:
                burst={'id':op['id'],'target':target,'current_B_root':oldroot,'previous_B_root':previous,
                       'A_cost':op['a'],'Q_B_cost':op['q'],'scope':'Real target-OTHER branch in the full source; not a complete-period cost counterexample.'};break
            if target!=oldroot:previous,oldroot=oldroot,target
    assert burst
    write('ORIGINAL_OTHER_TARGET_WITNESS.json',{'trace':T.pin(hpath),'source':hz['source']['name'],
          'full_A':hz['A'],'full_Q_B':hz['Q_B'],'burst':burst})
    write('AUDIT_SUMMARY.json',{'controls':rows,'root_C1_counterexample':{'source':z['source']['name'],
          'A':z['A'],'Q_B':z['Q_B'],'unfunded':cert['unfunded'],'status':'REFUTED_EXACT_CANDIDATE_CONSTANT1_ONLY'},
          'other_target_witness':burst,'universal_CD':'OPEN'})
    print(json.dumps({'control_sources':len(rows),'nonzero_bank_unpaid_is_paid_by_overflow':True,
                      'C1_global_counterexample':[z['A'],z['Q_B']],'target_OTHER_burst':burst}))


if __name__=='__main__':main()

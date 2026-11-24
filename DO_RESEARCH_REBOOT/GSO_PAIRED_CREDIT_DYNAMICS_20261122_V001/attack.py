"""Complete original paired-tree execution, energy coefficients and cyclic credit."""
import sys
import json
import gzip
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
from sources import T,inflate
from reserve import cyclic_credit
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(T.HERE));import role_synthesis as S;sys.path.pop(0)


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    p=HERE/name;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
    with (gzip.open(p,'wt',encoding='utf-8') if p.suffix=='.gz' else p.open('w',encoding='utf-8')) as f:json.dump(value,f,indent=None if p.suffix=='.gz' else 2)


def miss(A,B):
    common={(A.lo[k],A.hi[k]) for k in A.keys}
    return Counter(B.hi[k]-B.lo[k]+1 for k in B.keys if (B.lo[k],B.hi[k]) not in common)


def difference(before,after):return {str(k):before[k]-after[k] for k in before.keys()|after.keys() if before[k]!=after[k]}


def observe(source,q):
    keys=sorted(map(int,source['initial_A']['children']));A=T.B.K.OLD.Tree(source['initial_A'],keys);B=T.B.K.OLD.Tree(source['initial_B'],keys)
    m=len(source['embedding']['old_keys']);at=m+7
    for mode,x in source['operations'][:at-1]:
        T.B.K.OLD.plain(A,x)
        if mode=='K':T.B.K.OLD.plain(B,x)
    x=source['operations'][at-1][1];before=miss(A,B);T.B.K.OLD.plain(A,x);after_A=miss(A,B)
    assert difference(before,after_A)=={}
    rows=[];step=0
    while B.parent[x] is not None:
        step+=1;p=B.parent[x];g=B.parent[p];typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
        hist=miss(A,B)
        size=lambda k:0 if k is None else B.hi[k]-B.lo[k]+1
        branch_sizes=None
        if typ=='RR':branch_sizes={'a':size(B.ch[g][0]),'b':size(B.ch[p][0]),'c':size(B.ch[x][0]),'d':size(B.ch[x][1])}
        for key in ([x] if g is None else [p,x] if typ in ('LL','RR') else [x,x]):B.rotate(key)
        delta=difference(hist,miss(A,B))
        if typ=='RR':assert delta=={} and branch_sizes['a']==branch_sizes['d']==7 and branch_sizes['b']==branch_sizes['c']
        rows.append({'id':['B',at,step],'type':typ,'branch_sizes':branch_sizes,'delta_Phi_w_coefficients':delta})
    final=miss(A,B);expected={str(16*2**q-1):1,str(16*2**q+1):1}
    assert len(rows)==q+1 and sum(r['type']=='RR' for r in rows)==q and rows[-1]['type']=='LR'
    assert difference(before,final)==expected
    return {'operation':at,'target':x,'A_cost':1,'Q_B_cost':q+1,'A_phase_delta':{},
        'whole_operation_delta_Phi_w_coefficients':expected,'B_steps':rows,
        'meaning':'Phi_w=-sum of w(size) over full-physical B subtree intervals missing in A. Coefficients apply to every real weight function simultaneously.'}


def main():
    specs=json.loads((HERE/'OPTIMIZATION_RESULT.json').read_text());summary=[]
    selected=T.load(T.HERE/'SELECTED_ROLE_POLICY.json')
    assert selected['H']==5
    for i,opt in enumerate(specs):
        q=opt['q'];base=T.B.K.PARAM.H(3,q);source=inflate(base,opt['gaps']);z=T.F.compile_source(source)
        assert source['embedding']['physical_support']==16*2**q+5
        assert z['A']==64*(q+1) and z['Q_B']==28*q+25
        energy=observe(source,q)
        events,changed=S.prepared(z,tuple(selected['middle_order']))
        policy=T.B.cyclic_events(z,events,5,True,'all_original_Q')
        bank=cyclic_credit(events,4)
        stem='run/source_'+str(i)
        write(stem+'_trace.json.gz',z);write(stem+'_energy.json',energy)
        write(stem+'_local_bank.json.gz',policy);write(stem+'_global_credit.json.gz',bank)
        # These are phase observations on the complete original source, never
        # additional initial credit or a free sum of per-scale allowances.
        opmap={o['id']:o for o in z['operations']};global_rows={tuple(r['id']):r for r in bank['rows']}
        critical=[]
        for op in z['operations']:
            old_id=op['id'];m=opt['old_support']
            if old_id not in (m,m+1,m+3,m+7):continue
            br=[r for r in bank['rows'] if r['id'][0]=='B' and r['id'][1]==old_id]
            critical.append({'operation':old_id,'A':op['a'],'Q_B':op['q'],
                'credit_before_B':br[0]['before'],'credit_after_B':br[-1]['after']})
        row={'index':i,'q':q,'carrier_support':opt['old_support'],'physical_support':opt['physical_support'],
             'A':z['A'],'Q_B':z['Q_B'],'operations':len(z['operations']),'real_rotations':z['real_rotations'],
             'local_H5_paid':policy['paid'],'local_H5_unpaid':len(policy['failures']),
             'global_C4_min_capacity':bank['capacity'],'global_C4_issued':bank['issued'],
             'critical_credit':critical,'trace':stem+'_trace.json.gz','energy':stem+'_energy.json',
             'local_bank':stem+'_local_bank.json.gz','global_credit':stem+'_global_credit.json.gz'}
        predicted=max(8*(q+1),12*(q+1)-4,14*(q+1)-12,15*(q+1)-28)
        assert bank['capacity']==predicted
        summary.append(row)
        print(json.dumps({k:row[k] for k in ('q','physical_support','A','Q_B','local_H5_unpaid','global_C4_min_capacity')}),flush=True)
    write('COMPLETE_SOURCE_AUDIT.json',{'cases':summary,
        'scope':'Complete original sources and exact credit flow; no finite population proves Universal CD.',
        'all_q_mathematics':'Original rigid-gap and H3q recurrences, with separate learned induction certificate.',
        'universal_CD':'OPEN'})


if __name__=='__main__':main()

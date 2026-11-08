"""Complete the one selected closed source witness; no new source search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
KC=BASE/'route_c_seven_core_return_obstruction_20261031_v001'
PF=BASE/'route_c_parent_fringe_obstruction_20261101_v001'


def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')


def main():
    selected=read(HERE/'first_return_obstruction.json')
    table=read(KC/'source_transition_table.json')
    graph=read(KC/'reachable_relation_certificate.json')
    cores,tt,pairs=table['cores'],table['transitions'],graph['pair_ids']
    spec=importlib.util.spec_from_file_location('inherited_pf',PF/'find_zero_offer_returns.py')
    pf=importlib.util.module_from_spec(spec);spec.loader.exec_module(pf)
    def tr(t,y):return tt[7*t+y-1]
    def embed(t,fringe):
        return None if t is None else [t[0],embed(t[1],fringe),fringe if t[0]==7 else embed(t[2],fringe)]
    def mirror(t):
        if t is None:return None
        if isinstance(t,str):return 'F_lower'
        return [14-t[0],mirror(t[2]),mirror(t[1])]
    def expand(r,i,fringe):
        ar,br=tr(pairs[r['source']][0],r['key']),tr(pairs[r['source']][1],r['key'])
        return dict(occurrence=i,mode='KEEP',key=r['key'],source_state=r['source'],target_state=r['target'],
            source_A=embed(cores[pairs[r['source']][0]],fringe),source_B=embed(cores[pairs[r['source']][1]],fringe),
            destination_A=embed(cores[ar['target']],fringe),destination_B=embed(cores[br['target']],fringe),
            d_A=ar['depth'],d_B=br['depth'],a=ar['a'],q=br['q'],z=br['z'],delta=br['q']-2*ar['a'],
            A_events=ar['events'],B_events=br['events'])
    rows=[expand(r,i,table['fringe']) for i,r in enumerate(selected['closed_rows'])]
    formal=[expand(r,i,'F') for i,r in enumerate(selected['closed_rows'])]
    mirrored=[]
    for i,(r,small) in enumerate(zip(rows,selected['closed_rows'])):
        mr=dict(r,key=14-r['key'])
        for field in ['source_A','source_B','destination_A','destination_B']:mr[field]=mirror(r[field])
        mr['A_events']=tr(pairs[small['source']][0],small['key'])['mirror_events']
        mr['B_events']=tr(pairs[small['source']][1],small['key'])['mirror_events']
        mirrored.append(mr)
    startup=list(table['prefix_rows'])
    startup += [expand(r,i+len(startup),table['fringe']) for i,r in enumerate(selected['startup_common_KEEP'])]
    assert rows[-1]['destination_A']==rows[0]['source_A']
    assert rows[-1]['destination_B']==rows[0]['source_B']
    assert startup[-1]['destination_A']==rows[0]['source_A']
    assert startup[-1]['destination_B']==rows[0]['source_B']
    assert all(r['source_A']!=r['source_B'] and r['destination_A']!=r['destination_B'] for r in rows)
    assert [i for i,r in enumerate(rows) if r['delta']>0]==[0]
    T=cores[pairs[selected['closed_rows'][0]['target']][1]]
    profiles={str(y):pf.profile(T,5,y) for y in range(1,8)}
    budgets=[]
    for j,r in enumerate(rows[1:],1):
        pr=profiles[str(r['key'])];k=j-1;C=2*r['a']
        c=pr['source_depth']//2 if k==0 else pr['PF_U']//2+k-1
        rho=min(C,c);f=C-rho
        assert f==0 and r['q']<=rho
        budgets.append(dict(block=j,key=r['key'],capacity=C,own_q=r['q'],k=k,
            h=pr['source_depth'],U_PF=pr['PF_U'],ceiling=c,reservation=rho,offer=f,reserved_loss=rho-r['q']))
    assert sum(b['reserved_loss'] for b in budgets)==29

    def scan(actual_rows,cut,protocol):
        N=len(actual_rows);history=[];pending=[];claims=[];steps=[];usedU=set();usedD=set()
        def assign(d,u,kind):
            assert tuple(d) not in usedD and tuple(u) not in usedU
            usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
        for t in range(N):
            j=(cut+t)%N;r=actual_rows[j];C=2*r['a'];before=len(pending)
            units=[[0,j,e,b] for e in range(r['a']) for b in [0,1]]
            demands=[[0,j,e] for e,ev in enumerate(r['B_events']) if ev[0]!='ZIG']
            cs=[]
            if r['delta']>0:
                for d,u in zip(demands[:C],units):assign(d,u,'positive_own')
                pending+=demands[C:];history.append(j);reserve=C;offer=lam=0;x=r['delta']
            else:
                if history:
                    assert history==[0]
                    k=(j-1)%N;key=rows[j]['key'];pr=profiles[str(key)]
                    c=pr['source_depth']//2 if k==0 else pr['PF_U' if protocol=='PF' else 'old_U']//2+k-1
                    cs=[dict(anchor=0,k=k,ceiling=c)]
                    reserve=min(C,c)
                else:reserve=C
                assert r['q']<=reserve
                for d,u in zip(demands,units[:r['q']]):assign(d,u,'payer_own')
                offer=C-reserve;lam=reserve-r['q'];x=-offer
                take=min(offer,len(pending))
                for d,u in zip(pending[:take],units[reserve:reserve+take]):assign(d,u,'loan')
                pending=pending[take:]
            steps.append(dict(scan_index=t,block=j,key=r['key'],capacity=C,own_q=r['q'],delta=r['delta'],
                history=list(history),facts=cs,reservation=reserve,offer=offer,reserved_loss=lam,
                signed_input=x,debt_before=before,debt_after=len(pending)))
        X=[0]
        for s in steps:X.append(X[-1]+s['signed_input'])
        b=max(i for i,x in enumerate(X) if x==min(X));busy=steps[b:]
        cert=dict(last_minimum_index=b,busy_blocks=[s['block'] for s in busy],
            source_delta_sum=sum(s['delta'] for s in busy),reserved_loss_sum=sum(s['reserved_loss'] for s in busy),
            terminal_debt=len(pending))
        assert len(pending)==1 and all(s['offer']==0 for s in steps)
        assert cert['source_delta_sum']+cert['reserved_loss_sum']==1
        return dict(protocol=protocol,cut=cut,periods=1,accepted=False,final_debt=1,steps=steps,
            assignments=claims,unpaid=pending,busy_suffix=cert,reused_units=0,startup_units_used=0)
    audits={orientation:{p:[scan(rs,cut,p) for cut in range(19)] for p in ['FI','PF']}
            for orientation,rs in [('ordinary',rows),('reflected',mirrored)]}

    def direct(rs):
        claims=[];usedU=set();usedD=set()
        def assign(d,u,kind):
            assert tuple(d) not in usedD and tuple(u) not in usedU
            usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
        residual=None
        for j,r in enumerate(rs):
            us=[[0,j,e,b] for e in range(r['a']) for b in [0,1]]
            ds=[[0,j,e] for e,ev in enumerate(r['B_events']) if ev[0]!='ZIG']
            for d,u in zip(ds,us):assign(d,u,'own')
            if j==0:
                assert len(ds)==3 and len(us)==2;residual=ds[2]
            if j==2:
                # Chosen from the original source-entry proof, never from future q.
                assert len(ds)<=1 and len(us)==2
                assign(residual,us[1],'exact_RL_entry_then_outer_LR_source_loan')
        assert len(claims)==22
        return dict(assignments=claims,paid_demands=22,physical_capacity=50,unused_units=28,
            source_selected_donor=dict(block=2,A_event=0,bit=1,protected_own_bound=1,
                original_h=3,entry_shift=1,outer_shift=-1,source_depth_ceiling=3),
            complete=True,reused_units=0,startup_units_used=0,
            protocol='direct fixed-word source certificate; does not alter FI or PF')
    save('closed_source_certificate.json',dict(selected_audit_sha256=sha(HERE/'first_return_obstruction.json'),
        fixed_completion_scope_sha256=sha(HERE/'PG00A_FIXED_WITNESS_COMPLETION.md'),
        source_table_sha256=sha(KC/'source_transition_table.json'),source_relation_sha256=sha(KC/'reachable_relation_certificate.json'),
        ordinary_rows=rows,reflected_rows=mirrored,formal_opaque_fringe_rows=formal,startup_rows=startup,
        first_intervention_profiles=profiles,fresh_budget_rows=budgets,
        totals=dict(blocks=19,A=25,C=50,Q_B=22,E=1,C_D=0,L_PF_fresh=0,Gamma_PF=1,
                    source_delta=-28,reserved_loss_fresh=29),
        all_cut_audits=audits,direct_injection=dict(ordinary=direct(rows),reflected=direct(mirrored)),
        only_repetition_control=1,no_larger_m_or_n_replayed=True,
        uniform_claims=dict(fringe='arbitrary finite common F with all keys>7, including empty',
            repetitions='every integer m>=1, proved by exact return and unchanged source facts',
            A='25m',Q_B='22m',Gamma_PF='m',PF_final_debt_every_cut='m',
            FI_final_debt_every_cut='m',direct_distinct_units='22m demands injected into 50m units',
            no_synchronization=True),unchanged_FI_PF_algorithms=True))
    print(json.dumps(dict(status='FIXED_CLOSED_SOURCE_CERTIFICATE_WRITTEN',blocks=19,
        orientations=2,cuts_per_protocol_orientation=19,protocols=['FI','PF'],
        all_cuts_rejected=True,Gamma_PF=1,A=25,Q_B=22,
        direct_injection_demands=22,no_larger_m_or_n_replayed=True),indent=2))


if __name__=='__main__':main()

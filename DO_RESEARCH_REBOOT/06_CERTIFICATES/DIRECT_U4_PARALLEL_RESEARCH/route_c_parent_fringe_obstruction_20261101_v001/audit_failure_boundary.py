"""Complete the declared failure audit; no substitute source search."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
KC=HERE.parent/'route_c_seven_core_return_obstruction_20261031_v001'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def mirror(t):return None if t is None else [14-t[0],mirror(t[2]),mirror(t[1])]


def main():
    ret=read(HERE/'fixed_return_certificate.json')
    assert ret['reachable_nodes_count']==1 and ret['allowed_reachable_edges']==0
    assert ret['paths']==dict(anchor_return=None,reset_return=None)
    table=read(KC/'source_transition_table.json');graph=read(KC/'reachable_relation_certificate.json')
    cores,tt,F=table['cores'],table['transitions'],table['fringe'];pp=graph['pair_ids']
    def tr(tree,key):return tt[7*tree+key-1]
    def embed(t):return None if t is None else [t[0],embed(t[1]),F if t[0]==7 else embed(t[2])]
    boundary=[]
    A,B=pp[4327]
    for key,target,delta in graph['outgoing_edges'][4327]:
        ar,br=tr(A,key),tr(B,key);C=2*ar['a'];c=ret['profiles'][str(key)]['old_U']//2+1
        boundary.append(dict(key=key,target=target,target_pair=pp[target],a=ar['a'],q=br['q'],
            delta=delta,C=C,old_ceiling=c,old_offer=C-min(C,c),diagonal_destination=pp[target][0]==pp[target][1]))
    assert [r['key'] for r in boundary]==[2,3,4,5,6,7]
    assert all(r['delta']<=0 for r in boundary)
    assert [r['key'] for r in boundary if r['diagonal_destination']]==[3]
    assert all(r['old_offer']>=1 for r in boundary if r['key']!=3)
    assert next(r for r in boundary if r['key']==3)['old_offer']==0
    def compose(word):
        state=4676;rows=[]
        for i,key in enumerate(word):
            aid,bid=pp[state];ar,br=tr(aid,key),tr(bid,key)
            target=next(e[1] for e in graph['outgoing_edges'][state] if e[0]==key)
            na,nb=ar['target'],br['target']
            assert [na,nb]==pp[target]
            rows.append(dict(occurrence=i,mode='KEEP',key=key,source_state=state,target_state=target,
                source_A=embed(cores[aid]),source_B=embed(cores[bid]),
                destination_A=embed(cores[na]),destination_B=embed(cores[nb]),
                a=ar['a'],q=br['q'],z=br['z'],d_A=ar['depth'],d_B=br['depth'],
                A_events=ar['events'],B_events=br['events'],A_mirror_events=ar['mirror_events'],B_mirror_events=br['mirror_events'],
                delta=br['q']-2*ar['a']))
            state=target
        return rows
    def scan(rows,new=False):
        claims=[];usedU=set();usedD=set();remaining=[];steps=[];loss=0
        def claim(d,u,kind):
            assert tuple(d) not in usedD and tuple(u) not in usedU
            usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
        for i,row in enumerate(rows):
            C=2*row['a'];demands=[[0,i,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
            units=[[0,i,e,b] for e in range(row['a']) for b in [0,1]]
            before=len(remaining)
            if row['delta']>0:
                assert i==0
                for d,u in zip(demands[:C],units):claim(d,u,'positive_own')
                remaining+=demands[C:];reserve=C;offer=0;lam=0;loans=[]
            else:
                if i==1:ceiling=ret['profiles'][str(row['key'])]['source_depth']//2
                else:ceiling=ret['profiles'][str(row['key'])]['PF_U' if new else 'old_U']//2+i-2
                reserve=min(C,ceiling);assert row['q']<=reserve
                for d,u in zip(demands,units[:reserve]):claim(d,u,'payer_own')
                offer=C-reserve;lam=reserve-row['q'];loans=[]
                take=min(offer,len(remaining))
                for d,u in zip(remaining[:take],units[reserve:reserve+take]):claim(d,u,'loan');loans.append(dict(demand=d,unit=u))
                remaining=remaining[take:]
            loss+=lam
            steps.append(dict(occurrence=i,key=row['key'],capacity=C,own_q=row['q'],reservation=reserve,
                offer=offer,reserved_loss=lam,debt_before=before,debt_after=len(remaining),loans=loans))
        return dict(protocol='PF' if new else 'FI',accepted=not remaining,final_debt=len(remaining),
            steps=steps,assignments=claims,unpaid=remaining,source_delta_sum=sum(r['delta'] for r in rows),
            reserved_loss_sum=loss,startup_units_used=0,reused_units=0,
            scope='directed complete-block open source span; no closed-walk classification')
    examples={}
    for name,word in [('three_block',[6,4,1]),('synchronizing_four_block',[6,4,1,3])]:
        rows=compose(word);ordinary=dict(rows=rows,FI=scan(rows),PF=scan(rows,True))
        reflected=[]
        for r in rows:
            mr=dict(r,key=14-r['key'],source_A=mirror(r['source_A']),source_B=mirror(r['source_B']),
                destination_A=mirror(r['destination_A']),destination_B=mirror(r['destination_B']),
                A_events=r['A_mirror_events'],B_events=r['B_mirror_events'])
            reflected.append(mr)
        examples[name]=dict(normal=ordinary,reflected_rows=reflected)
    assert examples['three_block']['normal']['FI']['final_debt']==1
    assert examples['three_block']['normal']['PF']['accepted']
    quad=examples['synchronizing_four_block']['normal']
    assert quad['rows'][-1]['destination_A']==quad['rows'][-1]['destination_B']
    assert quad['FI']['source_delta_sum']==-1 and quad['FI']['reserved_loss_sum']==2 and quad['FI']['final_debt']==1
    save('failure_boundary_certificate.json',dict(status='FIXED_ZERO_OFFER_RETURN_MECHANISM_REFUTED',
        fixed_return_sha256=sha(HERE/'fixed_return_certificate.json'),
        completion_scope_sha256=sha(HERE/'PF00A_FAILURE_BOUNDARY_SCOPE.md'),boundary_state=4327,
        core_successors=boundary,root_noop_key=1,
        fringe_depth_formulas=dict(variable='f=depth within F>=0',current_d_A='5+f',current_d_B='5+f',
            post_anchor_h='2+f',first_entry_role='grandparent outer fringe in final LR',old_U='4+f',
            old_ceiling_at_k2='floor((4+f)/2)+1',
            even_f=dict(f='2u',u_domain='nonnegative integers',C=[6,2],q=[2,1],ceiling=[3,1],offer=[3,1]),
            odd_f=dict(f='2u+1',u_domain='nonnegative integers',C=[6,2],q=[3,1],ceiling=[3,1],offer=[3,1]),
            coefficient_format='[constant,coefficient of u]',minimum_offer=3),
        closed_source_dichotomy='next KEEP pays or synchronizes; leaving diagonal regime before any positive/unequal return requires a KEEP-less block, which offers>=2',
        excluded_run_pattern='positive source anchor4676 followed by KEEP-containing blocks4,1',
        excluded_run_bound='T_i>=e_i=1, hence g_i<=0 on every closed source continuation in this embedding',
        arbitrary_upper_fringe=True,no_new_source_word_search_after_failure=True,
        strict_new_closed_walk_PF_coverage='NOT ESTABLISHED',universal_CD='OPEN'))
    save('directed_span_certificates.json',dict(examples=examples,
        three_block_source_cost=dict(A=3,Q_B=6),four_block_source_cost=dict(A=4,Q_B=7),
        three_block_PF_accepted_FI_rejected=True,
        source_four_block_reserved_loss_certificate=dict(source_sum=-1,reserved_loss=2,final_debt=1),
        closed_walk_counterexample_claimed=False,positive_Gamma_closed_walk_claimed=False,
        new_source_engine_calls=0,larger_finite_fits=0))
    print(json.dumps(dict(status='FIXED_RETURN_REFUTED_WITH_SOURCE_DICHOTOMY',core_successors=boundary,
        three_block_FI_debt=1,three_block_PF_debt=0,
        four_block_source_sum=-1,four_block_reserved_loss=2,four_block_FI_debt=1,
        fringe_minimum_certified_offer=3,new_closed_walk_witness=False),indent=2))


if __name__=='__main__':main()

"""Deterministic lift of the inherited nine-core B cycle into a U4-M counterexample."""
from pathlib import Path
import sys,json,copy,ast,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path[:0]=[str(OUT),str(ROOT/'python'),str(ROOT/'scripts')]
import verify_u4_counterexample as V
from independent import splay as S
import wp6_overflow as O

def main():
    target=OUT/'five_keep_nine_core_counterexample.json'
    V.require(not target.exists(),'append-only output')
    source=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW/DIRECT_CDK5_LOW_nine_node_replay.py'
    # Extract literal input, without executing the historical writer.
    constants={}
    for node in ast.parse(source.read_text()).body:
        if isinstance(node,ast.Assign):
            for name in node.targets:
                if isinstance(name,ast.Name) and name.id in ('T0','WORD'):
                    constants[name.id]=ast.literal_eval(node.value)
    t0=constants['T0'];original=constants['WORD'];a=V.dec(t0);w=[];blocks=[]
    for _,x in original:
        after=S.trace(a,x)[0]
        child=after[2] if after[2]!=S.LEAF else after[3]
        V.require(child!=S.LEAF,'nontrivial tree has a child')
        y=child[1];back=S.trace(S.trace(after,y)[0],x)[0]
        V.require(back==after,'inverse one-rotation detour')
        block=[('D',x),('D',y),('D',x),('K',x)]
        blocks.append({'start':len(w),'target':x,'chosen_child':y,'word':block})
        w+=block;a=after
    V.require(V.serial(a)==t0,'inherited B cycle closed')
    rows=V.replay_both(t0,w);m=len(w)
    rep=O.replay(t0,t0,w*3)
    period=copy.deepcopy(rep['accesses'][2*m:])
    for r in period:
        r['idx']%=m
        if r['setup'] is not None:r['setup']%=m
    cr=copy.deepcopy([d for d in O.creators(rep) if d['acc']>=2*m])
    for d in cr:
        V.require(d['creator'] is not None and not d['genesis'],'cyclic genealogy')
        d['acc']%=m;d['creator']%=m
        V.require(period[d['creator']]['m']=='K' and period[d['creator']]['a']==0,'empty creator')
    charge=O.charge({'accesses':period},copy.deepcopy(cr))
    units=V.credits(rows);adj=[]
    for d in cr:
        t=d['acc'];setup=period[t]['setup']
        V.require(rows[t]['a']==0 and rows[setup]['a']==1,'starved access, unit setup')
        nei=[j for j,u in enumerate(units) if u[0]==setup]
        d['setup']=setup;d['eligible_units']=[units[j] for j in nei];adj.append(nei)
    expected=sum(min(r['q'],2) for r in rows if r['mode']=='K')
    V.require(charge['matched']==expected==16 and len(cr)==18,'original matching vs disjoint-block formula')
    bad=[]
    for block in blocks:
        t=block['start']+3;indices=[j for j,d in enumerate(cr) if d['acc']==t]
        if len(indices)>2:
            X=indices[:3];N=sorted(set().union(*(set(adj[j]) for j in X)))
            V.require(len(N)==2,'minimal triple Hall shortage')
            bad.append({'access':t,'demand_indices':X,'complete_credit_neighborhood':[units[j] for j in N],'deficiency':1})
    marked={x for mode,x in w if mode=='K'}
    def core(t):
        present=set()
        for x in marked:
            cur=t
            while cur is not None:
                present.add(cur[0])
                if cur[0]==x:break
                cur=cur[1] if x<cur[0] else cur[2]
            V.require(cur is not None,'marked target present')
        return sorted(present)
    cores=[core(r['source_B']) for r in rows]+[core(rows[-1]['destination_B'])]
    V.require(marked=={1,3,5,7,9} and all(c==list(range(1,10)) for c in cores),'exact five KEEP / nine core')
    A=sum(r['a'] for r in rows);Q=sum(r['q'] for r in rows)
    V.require((A,Q)==(34,18),'aggregate costs')
    result={'status':'EXACT_COUNTEREXAMPLE_FOUND','target_refuted':'original U4-M',
            'inherited_fixture':str(source.relative_to(ROOT)).replace('\\','/'),
            'inherited_fixture_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'initial_A':t0,'initial_B':t0,'initial_diagonal':True,'reachability_prefix':[],
            'original_B_word':original,'word':w,'blocks':blocks,'full_state_replay':rows,
            'KEEP_support':sorted(marked),'genuine_KEEP_support':sorted(marked),
            'core_sets_at_every_boundary':cores,'core_size':9,'paired_closure':True,
            'A':A,'Q_B':Q,'Z_B':sum(r['z'] for r in rows),'Q_minus_2A':Q-2*A,
            'demands':cr,'credit_units':units,'adjacency':adj,'original_charge':charge,
            'independent_matching_formula':expected,'minimal_Hall_subsets':bad,
            'all_KEEP_A_costs_zero':True,'all_setup_capacities':2,
            'nonstarved_KEEP_competitor_exists':False,'CD_U_refuted':False,
            'abstract_Stage11G_lift_not_asserted':True,
            'logical_scope':'Physical W_5^9 witness; original matching fails despite scalar surplus. No frozen symbolic graph or certificate changed.'}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result[k] for k in ('status','KEEP_support','core_size','A','Q_B','Q_minus_2A','independent_matching_formula','minimal_Hall_subsets')},indent=2))

if __name__=='__main__':main()

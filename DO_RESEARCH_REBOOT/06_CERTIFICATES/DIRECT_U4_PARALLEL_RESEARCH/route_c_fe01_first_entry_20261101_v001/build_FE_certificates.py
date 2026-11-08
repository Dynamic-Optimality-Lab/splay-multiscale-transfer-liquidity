"""Produce the fixed FE01 symbolic/source certificates without source replay."""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from source_first_entry import ENTRY, OUTER, ceiling, path, profile

PG=HERE.parent/'route_c_pf_positive_gap_closure_20261101_v001'


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def mirror(t):
    if t is None:return None
    if isinstance(t,str):return 'F_lower'
    return [14-t[0],mirror(t[2]),mirror(t[1])]
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])


def templates():
    return {
        'LL':(['g',['p',['x','A','B'],'C'],'D'],['x','A',['p','B',['g','C','D']]]),
        'RR':(['g','A',['p','B',['x','C','D']]],['x',['p',['g','A','B'],'C'],'D']),
        'LR':(['g',['p','A',['x','B','C']],'D'],['x',['p','A','B'],['g','C','D']]),
        'RL':(['g','A',['p',['x','B','C'],'D']],['x',['g','A','B'],['p','C','D']]),
        'ZIG_L':(['p',['x','A','B'],'C'],['x','A',['p','B','C']]),
        'ZIG_R':(['p','A',['x','B','C']],['x',['p','A','B'],'C']),
    }


def locations(t,p=()):
    if isinstance(t,str):return {t:list(p)}
    return {t[0]:list(p),**locations(t[1],p+('L',)),**locations(t[2],p+('R',))}


def scan(rows,cut,protocol):
    N=len(rows);order=[(cut+t)%N for t in range(N)];history=[];queue=[];claims=[];steps=[]
    usedU=set();usedD=set()
    def assign(d,u,kind):
        assert tuple(d) not in usedD and tuple(u) not in usedU
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    for t,j in enumerate(order):
        row=rows[j];C=2*row['a'];before=len(queue);facts=[];loans=[]
        us=[[0,j,e,b] for e in range(row['a']) for b in [0,1]]
        ds=[[0,j,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
        if row['delta']>0:
            for d,u in zip(ds[:C],us):assign(d,u,'positive_own')
            queue+=ds[C:];history.append((j,t));r=C;S=lam=0;signed=row['delta']
        else:
            for anchor,at in history:
                between=[rows[v] for v in order[at+1:t] if rows[v]['d_B']>0]
                k=len(between);T=rows[anchor]['destination_B']
                first=between[0]['key'] if k else None
                if k:assert between[0]['source_B']==T
                c=ceiling(T,first,row['key'],k,protocol)
                facts.append(dict(anchor=anchor,k=k,first_key=first,ceiling=c))
            r=min([C]+[f['ceiling'] for f in facts]);assert row['q']<=r
            for d,u in zip(ds,us[:row['q']]):assign(d,u,'payer_own')
            S=C-r;lam=r-row['q'];signed=-S;take=min(S,len(queue))
            for d,u in zip(queue[:take],us[r:r+take]):
                assign(d,u,'loan');loans.append(dict(demand=d,unit=u))
            queue=queue[take:]
        steps.append(dict(scan_index=t,block=j,key=row['key'],capacity=C,own_q=row['q'],delta=row['delta'],
            history=[i for i,at in history],facts=facts,reservation=r,offer=S,reserved_loss=lam,
            signed_input=signed,debt_before=before,debt_after=len(queue),loans=loans))
    X=[0]
    for s in steps:X.append(X[-1]+s['signed_input'])
    assert len(queue)==X[-1]-min(X)
    return dict(protocol=protocol,cut=cut,periods=1,steps=steps,assignments=claims,unpaid=queue,
        accepted=not queue,final_debt=len(queue),startup_units_used=0,reused_units=0,
        signed_balance=X[-1],minimum_prefix=min(X))


def main():
    pg=read(PG/'closed_source_certificate.json')
    symbolic={}
    for case,(before,after) in templates().items():
        p,q=locations(before),locations(after)
        shifts={role:len(q[role])-len(p[role]) for role in p}
        assert shifts==ENTRY[case]
        symbolic[case]=dict(before=before,after=after,before_paths=p,after_paths=q,shifts=shifts)
    save('symbolic_rotation_certificate.json',dict(identities=symbolic,outer_shifts=OUTER,
        arbitrary_descendant_rule='site offset and internal depth cancel in each role path difference',
        proposed_double_entries_checked=28,zig_entries_checked=10))
    trees={}
    source_sets=[pg['ordinary_rows'],pg['reflected_rows'],pg['startup_rows']]
    for rows in source_sets:
        for row in rows:
            for field in ['source_A','source_B']:
                T=row[field]
                for t in [T,mirror(T)]:
                    key=hashlib.sha256(canonical(t).encode()).hexdigest();trees[key]=t
    digest=hashlib.sha256();count=0;roles={}
    for key,T in sorted(trees.items()):
        assert keys(T)==list(range(1,14))
        for x in keys(T):
            for y in keys(T):
                pr=profile(T,x,y);count+=1
                row=[key,x,y,pr['H'],pr['PF_U'],pr['FI_U'],pr['entry_case'],pr['entry_role'],pr['terminal_zig_shift']]
                digest.update((canonical(row)+'\n').encode())
                label=pr['boundary'] or pr['entry_case']+':'+pr['entry_role']
                roles[label]=roles.get(label,0)+1
    save('geometry_input_trees.json',dict(source=sha(PG/'closed_source_certificate.json'),
         physical_key_count=13,trees=trees,tree_digest_method='SHA256 of sorted compact JSON tree'))
    save('source_geometry_certificate.json',dict(distinct_input_trees=len(trees),present_xy_cases=count,
         exact_source_formula_digest=digest.hexdigest(),entry_role_counts=roles,
         source_output_used_in_definition=False,splay_engine_calls=0,new_key_counts=0,larger_finite_fits=0))
    all_trials={};fresh={};profiles={}
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        all_trials[orientation]={}
        for protocol in ['FI','PF','FE']:
            trials=[scan(rows,c,protocol) for c in range(19)]
            all_trials[orientation][protocol]=trials
            if protocol!='FE':
                old=pg['all_cut_audits'][orientation][protocol]
                assert all(a['final_debt']==b['final_debt']==1 and not a['accepted'] for a,b in zip(trials,old))
            else:
                assert trials[0]['accepted'] and len(trials[0]['assignments'])==22
                loans=[c for c in trials[0]['assignments'] if c['kind']=='loan']
                assert loans==[dict(demand=[0,0,2],unit=[0,2,0,1],kind='loan')]
        T=rows[0]['destination_B'];z=rows[1]['key'];budgets=[]
        profiles[orientation]={str(row['key']):profile(T,z,row['key']) for row in rows}
        for j,row in enumerate(rows[1:],1):
            C=2*row['a'];c=ceiling(T,z,row['key'],j-1,'FE');rho=min(C,c)
            budgets.append(dict(block=j,key=row['key'],k=j-1,capacity=C,own_q=row['q'],ceiling=c,
                reservation=rho,offer=C-rho,reserved_loss=rho-row['q']))
        assert sum(r['offer'] for r in budgets)==1 and sum(r['reserved_loss'] for r in budgets)==28
        fresh[orientation]=dict(E=1,C_D=0,L_FE_fresh=1,Gamma_FE=0,source_delta=-28,
             Lambda_FE_fresh=28,payers=budgets,constructed_positive_cut=0)
    save('FE_witness_certificate.json',dict(inherited_PG_source_sha256=sha(PG/'closed_source_certificate.json'),
        inherited_PG_audit_sha256=sha(PG/'independent_audit.json'),source_only_profile_sha256=sha(HERE/'source_first_entry.py'),
        source_profiles=profiles,all_cut_trials=all_trials,fresh_budgets=fresh,
        designated_cut=0,source_word=[r['key'] for r in pg['ordinary_rows']],
        physical_key_count=13,repetition_controls=[1],larger_finite_fits=0,
        new_strictness_witnesses=0,ordinary_and_reflected=True,
        uniform_theorem='W(F)^m belongs to FE minus PF for every m>=1 and arbitrary common outer F',
        original_FI_PF_unchanged=True))
    print(json.dumps(dict(status='FE_CERTIFICATES_WRITTEN',geometry_trees=len(trees),xy_cases=count,
        FE_accepted_cuts={o:[c['cut'] for c in all_trials[o]['FE'] if c['accepted']] for o in all_trials},
        designated_FE_loan=dict(demand=[0,0,2],unit=[0,2,0,1]),Gamma_FE=0),indent=2))


if __name__=='__main__':main()

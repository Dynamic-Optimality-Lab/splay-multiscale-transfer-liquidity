from base1 import *
import copy

def toggle(n,m,tag='K'):
    st={'root':1,'children':{str(k):[None,k+1 if k<n else None] for k in range(1,n+1)}}
    tour=[['K',x] for x in range(2,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    return {'name':f'M1_{tag}_toggle_n{n}_m{m}','family':'matched_root_toggle_volume_test',
        'n':n,'m':m,'body_tag':tag,'initial_A':st,'initial_B':st,'diagonal_initial':st,'reaching_prefix':[],
        'operations':[[tag,2],[tag,1]]*m+tour,
        'analytic_A':2*m+2*(n-1),'analytic_Q_B':0,
        'analytic_A_signed_flux':n*(m+n-1) if tag=='K' else n*(n-1),
        'scope':'A-flux pricing obstruction; no B doubles, no original R6 or R_C.'}

def lift_state(st):
    n=len(st['children']);kids={};stack=[(st['root'],0,n+1)]
    while stack:
        k,lo,hi=stack.pop()
        if k is None:
            assert hi==lo+1;kids[str(2*lo+1)]=[None,None];continue
        l,r=st['children'][str(k)]
        kids[str(2*k)]=[2*l if l is not None else 2*lo+1,2*r if r is not None else 2*k+1]
        stack.append((l,lo,k));stack.append((r,k,hi))
    assert set(map(int,kids))==set(range(1,2*n+2))
    return {'root':2*st['root'],'children':kids}

def lift_source(s,k):
    return {'name':f'M1_private_lift_chain_k{k}','family':'private_hanger_lift_of_C05_chain','k':k,
        'initial_A':lift_state(s['initial_A']),'initial_B':lift_state(s['initial_B']),
        'diagonal_initial':lift_state(s['diagonal_initial']),
        'reaching_prefix':[[tag,2*x] for tag,x in s['reaching_prefix']],
        'operations':[[tag,2*x] for tag,x in s['operations']],
        'core_source_sha256':digest(s),'private_keys':list(range(1,2*len(s['initial_B']['children'])+2,2)),
        'critical_old_g':2,'critical_chain_length':k}

def repeated(s,r):
    z=copy.deepcopy(s);z['name']='M1_repeat'+str(r)+'_'+s['name'];z['family']='repeated_complete_original_word'
    z['base_source_sha256']=digest(s);z['repetitions']=r;z['operations']=s['operations']*r
    for key in ('A','Q_B','trace_hash','closing_A','closing_B'):z.pop(key,None)
    return z

def fresh_sources():
    sys.path.insert(0,str(base0.C5))
    from families import chain
    cat=load(M0/'SOURCE_CATALOG.json')
    out=[toggle(n,n) for n in (7,31,127,511,1027)]
    out.append(toggle(127,127,'D'))
    cores={}
    for k in (4,16,64,256):
        z=chain(k);z['name']='M1_scaled_'+z['name'];cores[k]=z;out.append(z)
    for k in (64,256):out.append(lift_source(cores[k],k))
    for i,r in ((4,4),(3,3),(5,4),(15,2)):out.append(repeated(cat[i]['source'],r))
    assert len(out)==16
    return out

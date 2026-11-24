from coercion import *
import coercion
from fast_physics import physical_replay, skeleton_cost
from independent_path_audit import check as check_physical

def opposite(k):
    x=k+2;y=k+1;n=2*k+2
    chain=[]
    for g in range(1,k+1):chain.extend([g,n-g+1])
    chain.extend([x,y])
    kids={str(z):[None,None] for z in chain}
    for u,v in zip(chain,chain[1:]):kids[str(u)][int(v>u)]=v
    b0={'root':1,'children':kids}
    a0=from_tuple(ind.node(y,ind.balanced(range(1,k+1)),
                          ind.node(x,L,ind.balanced(range(k+3,n+1)))))
    reach,rc=coerce(b0,a0)
    a,aa=advance(a0,[x,y]);b,bq=advance(b0,[x,y]);assert a==a0 and aa==2
    reset,rs=finish_pair(a,b,a0,b0)
    return {'name':f'C05_opposite_retarget_k{k}','family':'opposite_retained_columns','k':k,
        'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,
        'reaching_prefix':[['D',u] for u in reach],
        'operations':[['K',x],['K',y]]+reset,
        'critical_targets':[x,y],'prefix_stats':rc,'measured_restoration':rs}

def mass(m):
    ep1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    archive=load(ep1/'EXP01_SOURCE_WITNESSES.json')
    rows=archive if isinstance(archive,list) else archive.get('sources',archive.get('new_sources',[]))
    g=next(s for s in rows if s['name']=='G_4_1_L31_r1_z1')
    assert g['initial_A']==g['initial_B'] and len(g['operations'])==290
    key=lambda x: x+m if x is not None and x>18 else x
    st={'root':key(g['initial_A']['root']),'children':{str(key(int(k))):[key(z) for z in pair]
                            for k,pair in g['initial_A']['children'].items()}}
    assert st['children'][str(19+m)][0] is None
    st['children'][str(19+m)][0]=19
    for z in range(19,19+m):st['children'][str(z)]=[None,z+1 if z<18+m else None]
    block=[[tag,key(x)] for tag,x in g['operations']]
    visits,rs=finish_pair(st,st,st,st)
    reps=m+1
    return {'name':f'C05_neutral_gain_mass_m{m}','family':'marked_neutral_persistent_gain_mass',
        'm':m,'old_body_source':g['name'],'body_repetitions':reps,
        'old_body_source_sha256':digest(g),'initial_A':st,'initial_B':st,
        'diagonal_initial':st,'reaching_prefix':[],'operations':block*reps+visits,
        'body_length':len(block),'private_actual_marked_keys':list(range(19,19+m)),
        'critical_gained_parent':10,'critical_old_grandparent':18,
        'critical_operation_indices':[132+i*len(block) for i in range(reps)],
        'measured_support_return':rs}

def chain(k):
    n=2*k+1
    kids={str(z):[None,None] for z in range(1,n+1)};kids['1'][1]=2*k
    for i in range(1,k+1):kids[str(2*i)]=[2*i-2 if i>1 else None,2*i+1]
    b0={'root':1,'children':kids}
    kids={str(z):[None,None] for z in range(1,n+1)}
    for i in range(2,k+1):kids[str(2*i+1)][0]=2*i-1;kids[str(2*i-1)][1]=2*i
    kids['3'][0]=2;kids['2'][0]=1
    a0={'root':n,'children':kids};xs=list(range(n,2,-2))
    reach,rc=coerce(b0,a0)
    a,aa=advance(a0,xs);b,bq=advance(b0,xs);assert aa==k-1
    reset,rs=finish_pair(a,b,a0,b0)
    return {'name':f'C05_long_containment_chain_k{k}','family':'one_column_strict_containment_chain',
        'k':k,'critical_targets':xs,'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,
        'reaching_prefix':[['D',u] for u in reach],'prefix_stats':rc,
        'operations':[['K',x] for x in xs]+reset,'measured_restoration':rs}

def upper_restorer():
    # Before K23: 2--10--12--23.  Its bottom RR consumes column 10.
    # K4 subsequently promotes 10 as old parent of its third LL double.
    # The next K22 reuses 10 as its fifth old grandparent.
    kids={str(z):[None,None] for z in range(1,25)}
    kids['2']=[1,10];kids['10']=[9,12];kids['12']=[11,23];kids['23']=[14,24]
    kids['14'][0]=13
    for z in range(14,22):kids[str(z)][1]=z+1
    for z in range(9,6,-1):kids[str(z)][0]=z-1
    kids['6'][0]=4;kids['4']=[3,5]
    b0={'root':2,'children':kids}
    m=ind.node(5,L,ind.balanced(range(6,22)))
    a0=from_tuple(ind.node(23,ind.node(22,ind.node(4,ind.balanced(range(1,4)),m),L),
                          ind.node(24,L,L)))
    reach,rc=coerce(b0,a0)
    body=[['K',23],['K',4],['D',5],['K',22]]
    a,aa=advance(a0,[x for tag,x in body]);b,bq=advance(b0,[x for tag,x in body if tag=='K'])
    assert aa==3
    reset,rs=finish_pair(a,b,a0,b0)
    return {'name':'C05_upper_neutral_restorer_n24','family':'upper_neutral_restorer',
        'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,
        'reaching_prefix':[['D',u] for u in reach],'prefix_stats':rc,'operations':body+reset,
        'critical_old_column':10,'critical_previous_parent':[1,1],
        'critical_restorer':[2,3],'critical_new_parent':[4,5],
        'measured_restoration':rs}

def verify_prefix(s):
    a=Tree(s['diagonal_initial']);ta=as_tuple(s['diagonal_initial']);A=0
    for tag,x in s['reaching_prefix']:
        assert tag=='D';ta,ev=ind.trace(ta,x);A+=len(ev)
        inherited.Replay.plain_splay(a,x);assert a.state()==from_tuple(ta)
    assert a.state()==s['initial_A'] and s['diagonal_initial']==s['initial_B']
    return A

def scan(s):
    f=physical_replay(s)
    s.update(A=f['A'],Q_B=f['Q_B'],closing_A=s['initial_A'],closing_B=s['initial_B'])
    reach=verify_prefix(s)
    v=check_physical(s)
    prev=s['initial_B']['root'];M=set();targets=[]
    for tag,x in s['operations']:
        if tag=='K':
            if x!=prev:M.add(x)
            prev=x;targets.append(x)
    n=len(s['initial_B']['children']);assert M==set(range(1,n+1))
    # Exact raw cyclic rank cost, no assumed coverage of negative tests.
    raw=sum((x!=targets[i-1])+abs(x-targets[i-1]).bit_length() for i,x in enumerate(targets))
    assert raw==skeleton_cost(f,variant='raw')['B_cyclic']
    assert raw<=10*f['A'],(s['name'],raw,f['A'])
    return {'source':s['name'],'population':n,'genuine_support':n,'operations':len(f['rows']),
        'A':f['A'],'Q_B':f['Q_B'],'reaching_prefix_A_excluded':reach,'raw_periodic_cost':raw,
        'old_periodic_paid':True,'prescribed_overflow':0,'physical_verification':v,
        'source_sha256':digest(s),'original_Pi_replayed_here':False}

if __name__=='__main__':
    meter=Meter('families');sources=[];screens=[]
    for s in [opposite(4),opposite(32),opposite(257),mass(7),chain(16),upper_restorer()]:
        z=scan(s);sources.append(s);screens.append(z)
        print(s['name'],z['population'],z['A'],z['Q_B'],z['raw_periodic_cost'],flush=True)
    write('SOURCE_WITNESSES.json',sources);write('PHYSICAL_SCREENS.json',screens)
    write('COERCION_CHECK.json',{'four_key_shapes':14,'ordered_pairs':len(coercion.TABLE),
        'maximum_macro_requests':max(map(len,coercion.TABLE.values())),
        'all_words_independently_replayed_on_four_keys':True,
        'arbitrary_size_argument':'ancestor-closed four-node hull and rigid inorder gap components'})
    meter.success=True

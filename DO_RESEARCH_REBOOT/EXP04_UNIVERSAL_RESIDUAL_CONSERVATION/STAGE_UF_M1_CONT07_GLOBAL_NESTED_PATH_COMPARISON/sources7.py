from base7 import *
from coercion import coerce,advance
from exp01_oracle import Tree

def kernel(L):
    assert L>=0
    names=['1','2','3']+[f'v{i}' for i in range(2*L)]+['4','5','6','7','8','9']+[f'u{i}' for i in range(2*L)]+['10','11']
    key={k:i+1 for i,k in enumerate(names)};n=len(names)
    def state(root,links):
        c={str(k):[None,None] for k in range(1,n+1)}
        for a,(l,r) in links.items():c[str(key[a])]=[key[l] if l else None,key[r] if r else None]
        st={'root':key[root],'children':c};Tree(st);return st
    a_links={'9':('1','10'),'1':(None,'3'),'3':('2','6'),'6':('4','8'),'4':(None,'5'),'8':('7',None),'10':(None,'11')}
    b_links={'1':(None,'11'),'11':('2',None),'2':(None,'5'),'5':('3','10'),'3':(None,'4'),'10':('9',None),'9':('8',None),'8':('6',None),'6':(None,'7')}
    if L:
        a_links['4']=(f'v0','5');a_links['10']=(f'u0','11')
        for i in range(2*L):
            a_links[f'v{i}']=(None,f'v{i+1}' if i+1<2*L else None)
            a_links[f'u{i}']=(None,f'u{i+1}' if i+1<2*L else None)
        b_links['3']=(None,'v0');b_links['10']=(f'u{2*L-1}',None)
        for i in range(2*L):
            b_links[f'v{i}']=(None,f'v{i+1}' if i+1<2*L else '4')
            b_links[f'u{i}']=(f'u{i-1}' if i else '9',None)
    a0=state('9',a_links);b0=state('1',b_links);body=[key[x] for x in ('9','2','10','8','4')]
    b,_=advance(b0,body+list(range(1,n+1)));back,bstats=coerce(b,b0);ks=body+list(range(1,n+1))+back
    assert ks[-1]==key['1'];a,_=advance(a0,ks[:-1]);repair,astats=coerce(a,a0)
    word=[['K',x] for x in ks[:-1]]+[['D',x] for x in repair]+[['K',ks[-1]],['D',key['9']]]
    assert advance(a0,[x for tag,x in word])[0]==a0 and advance(b0,[x for tag,x in word if tag=='K'])[0]==b0
    reach,rstats=coerce(b0,a0)
    return {'name':f'M1C7_merge_kernel_L{L}','family':'outside_attachment_two_side_merge_kernel','L':L,'n':n,
        'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,'reaching_prefix':[['D',x] for x in reach],
        'operations':word,'key_map':key,'critical_g':key['5'],'producer_operation':1,'critical_operation':5,
        'right_inside_operation':4,'producer_double_index':L+1,'critical_double_index':L+1,
        'prefix_stats':rstats,'A_return_stats':astats,'B_return_stats':bstats,
        'scope':'Complete original source; physical kernel predicates are tested. U/R6/R_star/C_old not assumed.'}

def reflect(s):
    s=copy.deepcopy(s);n=s['n'];f=lambda x:n+1-x if x is not None else None
    for k in ('initial_A','initial_B','diagonal_initial'):
        st=s[k];s[k]={'root':f(st['root']),'children':{str(f(int(j))):[f(r),f(l)] for j,(l,r) in st['children'].items()}}
    for k in ('operations','reaching_prefix'):s[k]=[[tag,f(x)] for tag,x in s[k]]
    s['key_map']={k:f(x) for k,x in s['key_map'].items()};s['critical_g']=f(s['critical_g']);s['name']+='_mirror'
    if 'protected_labels' in s:s['protected_labels']=sorted(sum(1<<(n-k) for k in range(1,n+1) if lab>>(k-1)&1) for lab in s['protected_labels'])
    return s

def repeated(T):
    s=copy.deepcopy(load(C6/'FRESH_SOURCE_CATALOG.json')[1]);s['name']=f'M1C7_nested55_periods{T}';s['family']='full_original_period_repetition';s['period_copies']=T
    s['base_period_length']=len(s['operations']);s['operations']=s['operations']*T;s['n']=55
    s['original_source_reference']=str(C6/'FRESH_SOURCE_CATALOG.json')+'#1';s['original_source_sha256']=digest(load(C6/'FRESH_SOURCE_CATALOG.json')[1]);return s

if __name__=='__main__':
    unsealed();m=Meter('fresh_source_generation');a,b=kernel(0),kernel(5);out=[a,b,reflect(a),reflect(b),repeated(2),repeated(4)]
    assert len(out)<=8 and max(s['n'] for s in out)<=1027 and max(len(s['operations']) for s in out)<=40000
    write('FRESH_SOURCE_CATALOG.json',out);m.info['fresh_complete_sources']=len(out);m.ok=True
    print([(s['name'],s['n'],len(s['operations'])) for s in out],flush=True)

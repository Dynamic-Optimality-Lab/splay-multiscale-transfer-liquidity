from base6 import *
from sources2 import padded

def reflect(s):
    s=copy.deepcopy(s);n=len(s['initial_B']['children']);f=lambda x:n+1-x if x is not None else None
    for key in ('initial_A','initial_B','diagonal_initial'):
        st=s[key];s[key]={'root':f(st['root']),'children':{str(f(int(k))):[f(r),f(l)] for k,(l,r) in st['children'].items()}}
    for key in ('reaching_prefix','operations'):s[key]=[[tag,f(x)] for tag,x in s[key]]
    s['critical_g']=f(s['critical_g']);s['name']+='_reflected'
    # Block and guard metadata are diagnostic; remove their unreflected copy.
    for key in ('blocks','low_guard','high_guard','max_core'):s.pop(key,None)
    s['reflection_n_plus_one']=n+1
    return s

def sources():
    out=[]
    for L in (3,5,9,17,65):
        s=padded(4,L);s['name']=f'M1C6_nested_k4_L{L}';s['family']='complete_padded_nested_renewals';out.append(s)
    out.append(reflect(out[1]));return out

if __name__=='__main__':
    assert not (ROOT/'M1_CONT06_DELIVERY_MANIFEST.json').exists(),'Sealed stage.'
    m=Meter('source_generation');out=sources()
    assert max(len(s['initial_B']['children']) for s in out)<=600
    assert max(len(s['operations']) for s in out)<=40000
    write('FRESH_SOURCE_CATALOG.json',out);m.info['fresh_complete_sources']=len(out);m.ok=True
    print([(s['name'],len(s['initial_B']['children']),len(s['operations'])) for s in out],flush=True)

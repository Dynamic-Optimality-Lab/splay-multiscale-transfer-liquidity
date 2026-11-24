from base7 import *
from coercion import coerce,advance

def make():
    b={'root':3,'children':{'1':[None,None],'2':[1,None],'3':[2,4],'4':[None,5],'5':[None,None]}}
    a={'root':3,'children':{'1':[None,None],'2':[1,None],'3':[2,5],'4':[None,None],'5':[4,None]}}
    word=[['K',x] for x in (5,1,2,5,1,5,2,3)]
    assert advance(a,[x for tag,x in word])[0]==a and advance(b,[x for tag,x in word])[0]==b
    reach,stats=coerce(b,a)
    return {'name':'M1C7_epochless5','family':'explicit_epochless_old_g_column','n':5,'initial_A':a,'initial_B':b,
        'diagonal_initial':b,'reaching_prefix':[['D',x] for x in reach],'operations':word,'critical_g':4,'prefix_stats':stats}

def reflected(s):
    s=copy.deepcopy(s);f=lambda x:6-x if x is not None else None
    for k in ('initial_A','initial_B','diagonal_initial'):
        st=s[k];s[k]={'root':f(st['root']),'children':{str(f(int(j))):[f(r),f(l)] for j,(l,r) in st['children'].items()}}
    for k in ('operations','reaching_prefix'):s[k]=[[tag,f(x)] for tag,x in s[k]]
    s['critical_g']=f(s['critical_g']);s['name']+='_mirror';return s

if __name__=='__main__':
    unsealed();m=Meter('epochless_complete_source_generation');s=make();write('EPOCHLESS_SOURCE_CATALOG.json',[s,reflected(s)]);m.info['fresh_complete_sources']=2;m.ok=True;print('PASS two complete5-key epochless controls',flush=True)

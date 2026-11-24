from basec import *
from coercion import coerce,advance
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from adapterc import adapter,original_star
import gc,copy

def make(k):
    n=2*k+1;label={};gaps={};pos=2
    for j in range(1,n+1):
        label[j]=pos;pos+=1
        if j%2==0:gaps[j]=(pos,pos+1);pos+=2
    low,high=1,pos;M=label[n];m=label[1]
    bc={str(j):[None,None] for j in range(1,n+1)};bc['1'][1]=2*k
    for i in range(1,k+1):bc[str(2*i)]=[2*i-2 if i>1 else None,2*i+1]
    ac={str(j):[None,None] for j in range(1,n+1)}
    for i in range(2,k+1):ac[str(2*i+1)][0]=2*i-1;ac[str(2*i-1)][1]=2*i
    ac['3'][0]=2;ac['2'][0]=1
    def expand(root,ch):
        out={'root':label[root],'children':{str(label[j]):[label[x] if x else None for x in v] for j,v in ((int(j),v) for j,v in ch.items())}}
        for p,(z,y) in gaps.items():
            for q in (z,y):
                out['children'][str(q)]=[None,None];u=out['root']
                while True:
                    side=int(q>u);v=out['children'][str(u)][side]
                    if v is None:out['children'][str(u)][side]=q;break
                    u=v
        return out
    Acore=expand(n,ac);Bcore=expand(1,bc)
    a0=copy.deepcopy(Acore);a0['children'][str(m)][0]=low;a0['children'][str(M)][1]=high
    a0['children'][str(low)]=[None,None];a0['children'][str(high)]=[None,None]
    b0=copy.deepcopy(Bcore);b0['root']=low;b0['children'][str(low)]=[None,high];b0['children'][str(high)]=[Bcore['root'],None]
    reach,rs=coerce(b0,a0)
    body=[];critical=[];enclosures=[]
    for i in range(k,0,-1):
        critical.append(len(body)+1);body.append(['K',label[2*i+1]])
        enclosures.append(len(body)+1);body.append(['K',gaps[2*i][1]])
    b,_=advance(b0,[x for tag,x in body])
    corekeys=sorted(map(int,Acore['children']))
    visit=[low]+corekeys+[high,low];b,_=advance(b,visit)
    back,br=coerce(b,b0)
    def guarded(x):
        if x==low:return [['D',m],['K',x],['D',m]]
        if x==high:return [['D',M],['K',x],['D',M]]
        return [['K',x]]
    word=body+[z for x in visit+back for z in guarded(x)]
    a,_=advance(a0,[x for tag,x in word])
    assert a['children'][str(m)][0]==low and a['children'][str(M)][1]==high
    core={'root':a['root'],'children':{j:[None if x in (low,high) else x for x in v]
          for j,v in a['children'].items() if int(j) not in (low,high)}}
    repair,ar=coerce(core,Acore);word += [['D',x] for x in repair]
    assert advance(a0,[x for tag,x in word])[0]==a0
    assert advance(b0,[x for tag,x in word if tag=='K'])[0]==b0
    return {'name':f'M1C1_guarded_R6_chain_k{k}','family':'guarded_full_U_R6_same_column_chain','k':k,
        'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,'reaching_prefix':[['D',x] for x in reach],
        'operations':word,'critical_operations':critical,'enclosure_operations':enclosures,'critical_g':m,
        'low_guard':low,'high_guard':high,'core_labels':{str(j):v for j,v in label.items()},
        'gap_labels':{str(j):v for j,v in gaps.items()},
        'prefix_stats':rs,'B_return_stats':br,'A_core_repair_stats':ar,
        'guard_property':'Every A label containing core minimum contains low guard, except at low-guard root when it contains high guard.'}

if __name__=='__main__':
    meter=Meter('guarded_R6_chains');sources=[];out=[]
    for index,k in enumerate((4,16,64,256)):
        s=make(k);sources.append(s);write('GUARDED_SOURCES.json',sources)
        pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);checks=audit_forest(r,ff)
        phys={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':p,**d} for p,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        forest={'source':s['name'],'vertices':[{'parent':p,**v} for p,v in sorted(ff.items())],**checks}
        assert len(r.S)==4*k+3
        m=s['critical_g'];L=1<<(s['low_guard']-1);H=1<<(s['high_guard']-1);mb=1<<(m-1)
        for e in r.events:
            if e['actor']=='A':
                for lab in e['created']:assert not(lab&mb and not lab&(L|H))
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
        assert raw<=10*r.A
        w={'vertices':[{'parent':p,'type':v['type'],'w':0} for p,v in sorted(ff.items())],
            'R_overflow':0,'zero_reason':'Positive original raw periodic certificate plus cheap quota.'}
        m1=analyze(s,phys,forest,w);birth=reconstruct(s,phys,forest,m1,weights=w)
        native=adapter(s,phys,birth) # native original Pi/cohort/R6 agreement, using actual full states
        star=original_star(native) if k<=16 else None
        U={tuple(map(int,key.strip('()').split(','))):z for key,z in birth['U'].items()}
        critical_ids=[]
        for h in s['critical_operations']:
            ps=[p for p,d in r.doubles.items() if p[0]==h and d['g']==m];assert len(ps)==1
            p=ps[0];assert p in U;critical_ids.append(p)
        assert all(ff[p]['type']=='C' and tuple(ff[p]['predecessor'])==critical_ids[j-1] for j,p in enumerate(critical_ids) if j)
        r6set={tuple(z['parent']) for z in birth['original_R6']}
        assert set(critical_ids[1:])<=r6set
        depths={tuple(z['vertex']):z['distance'] for z in m1['C_fringe_depths']}
        assert sum(depths[p]>2 for p in critical_ids[1:])==k-2
        for label,data in (('PHYS',phys),('FOREST',forest),('WEIGHTS',w),('M1_AUDIT',m1),('BIRTH',birth)):
            write(f'GUARDED_{label}_{index:02}.json',data)
        row={'source':s['name'],'source_sha256':digest(s),'k':k,'population':4*k+3,'operations':len(s['operations']),
            'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,'old_raw_periodic_cost':raw,
            'original_U_count':len(U),'original_R6':len(birth['original_R6']),'critical_ids':critical_ids,
            'critical_U_C_R6_chain_edges':k-1,'deep_critical_U_C_R6_vertices':k-2,
            'original_R_star':star,'R_star_scope':'Native original selector' if star is not None else 'NOT_CLASSIFIED',
            'actual_R_C_deep':0,'actual_zero_reason':'Original periodic certificate remains positive; not a post-hybrid escape.'}
        out.append(row);write('GUARDED_RESULTS.json',out)
        print('PASS guarded',k,'R6',len(birth['original_R6']),'deep chain',k-2,'Rstar',len(star) if star is not None else 'unrun',flush=True)
        del r,pool,phys,forest,w,m1,birth,native,ff;gc.collect()
    meter.info.update(fresh_sources=4);meter.ok=True

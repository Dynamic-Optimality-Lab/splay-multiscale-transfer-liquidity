from base2 import *
from coercion import coerce,advance
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from native2 import adapter,original_star
from residual0 import gap_costs
import ast,gc

def fan(s,helper):
    low=1;gs=list(range(2,s+2));m=s+2;y=s+3;x1=s+4;x0=s+5
    ps=list(range(2*s+5,s+5,-1));high=2*s+6
    ac={str(j):[None,None] for j in range(1,high+1)}
    ac[str(gs[0])][0]=low
    for a,b in zip(gs[1:],gs):ac[str(a)][0]=b
    ac[str(m)][0]=gs[-1];ac[str(y)][0]=m;ac[str(x1)][0]=y;ac[str(x0)][0]=x1
    ac[str(x0)][1]=ps[-1]
    for a,b in zip(list(reversed(ps)),list(reversed(ps))[1:]+[high]):ac[str(a)][1]=b
    a0={'root':x0,'children':ac}
    bc={str(j):[None,None] for j in range(1,high+1)}
    bc[str(low)][1]=high;bc[str(high)][0]=gs[0]
    for i,(g,p) in enumerate(zip(gs,ps)):
        bc[str(g)][1]=p;bc[str(p)][0]=gs[i+1] if i+1<s else x0
    bc[str(x0)][0]=m;bc[str(m)][1]=x1;bc[str(x1)][0]=y
    b0={'root':low,'children':bc};reach,rs=coerce(b0,a0)
    body=[['K',x0],['K',x1],['K',y]]+[['K',g] for g in reversed(gs)]
    visit=[low]+list(range(2,high+1))+[low]
    b,_=advance(b0,[x for tag,x in body]+visit);back,br=coerce(b,b0)
    h=x0 if helper=='x0' else m
    word=body+[['K',x] for x in visit]+[['D',h]]+[['K',x] for x in back]
    a,_=advance(a0,[x for tag,x in word]);repair,ar=coerce(a,a0);word += [['D',x] for x in repair]
    assert advance(a0,[x for tag,x in word])[0]==a0
    assert advance(b0,[x for tag,x in word if tag=='K'])[0]==b0
    return {'name':f'M1C2_local_fan_s{s}_D{helper}','family':'alternating_RL_column_fan_attempt',
        's':s,'helper':helper,'initial_A':a0,'initial_B':b0,'diagonal_initial':b0,
        'reaching_prefix':[['D',x] for x in reach],'operations':word,'prefix_stats':rs,
        'B_return_stats':br,'A_repair_stats':ar,'critical_operation':2,'critical_g_candidates':gs}

if __name__=='__main__':
    meter=Meter('local_packing_fans');ss=[fan(16,'x0'),fan(32,'m')];write('FAN_SOURCE_CATALOG.json',ss);out=[]
    for i,s in enumerate(ss):
        pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
        p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs));assert raw<=10*r.A
        w={'vertices':[{'parent':v,'type':z['type'],'w':0} for v,z in sorted(ff.items())],
            'R_overflow':0,'zero_reason':'Original raw periodic certificate plus cheap-parent quota.'}
        an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b);star=original_star(native)
        U={ast.literal_eval(k):v for k,v in b['U'].items()};gs=gap_costs(s,r.boundaries)
        dep={tuple(z['vertex']):z['distance'] for z in an['C_fringe_depths']};packs=defaultdict(list)
        for v,ud in U.items():
            cr=tuple(ud['creator'])
            if ff[v]['type']=='C' and dep[v]>2 and cr in U and not U[cr]['exposed']:packs[v[0]].append(v)
        for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b)):write(f'FAN_{lab}_{i:02}.json',z)
        row={'index':i,'source':s['name'],'source_sha256':digest(s),'population':len(r.S),'operations':len(s['operations']),
            'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,'raw_periodic_cost':raw,'original_U':len(U),
            'original_R6':len(b['original_R6']),'native_original_R_star':star,'actual_S_UU':0,
            'critical':{'A_gap':gs[2],'B_q':r.boundaries[1]['q'],
                'candidate_old_grandparents':[{'parent':v,'g':d['g'],'U':v in U,'double_class':b['double_classes'][str(v)]}
                    for v,d in r.doubles.items() if v[0]==2]},
            'physical_local_packing_rows':[{'h':h,'parents':vs,'A_gap':gs[h],'bound_2A':2*gs[h],
                'violation':len(vs)>2*gs[h]} for h,vs in sorted(packs.items())]}
        out.append(row);write('FAN_RESULTS.json',out)
        print('PASS fan',s['s'],'U',len(U),'R6',len(b['original_R6']),'packing violations',sum(z['violation'] for z in row['physical_local_packing_rows']),flush=True)
        del r,pool,p,f,w,an,b,native,ff;gc.collect()
    meter.ok=True

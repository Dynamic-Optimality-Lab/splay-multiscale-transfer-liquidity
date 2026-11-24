from base3 import *
from physical1 import Edges
from bisect import bisect_right
from expand_events2 import expanded
import gc

def controls():
    out=load(C2/'INHERITED_SOURCE_CATALOG.json')
    for stem,cat in (('RUN_A','RUN_A_SOURCE_CATALOG.json'),('RUN_B','RUN_B_SOURCE_CATALOG.json'),('FAN','FAN_SOURCE_CATALOG.json')):
        for i,s in enumerate(load(C2/cat)):
            out.append({'source':s,'physical':str(C2/f'{stem}_PHYS_{i:02}.json'),'origin':'C2_'+stem,'index':i})
    boost=load(C2/'BOOST_SOURCE_CATALOG.json')
    out.append({'source':boost[0],'physical':str(C2/'BOOST_SHORT_PHYS.json'),'origin':'C2_boost_short'})
    out.append({'source':boost[1],'physical':None,'origin':'C2_boost_long','expansion':True})
    for stem,cat in (('NEW','NEW_SOURCE_CATALOG.json'),('PROTECTED','PROTECTED_SOURCE_CATALOG.json')):
        for i,s in enumerate(load(ROOT/cat)):
            out.append({'source':s,'physical':str(ROOT/f'{stem}_PHYS_{i:02}.json'),'origin':'C3_'+stem,'index':i})
    return out

def audit(s,S,events):
    a=Edges(s['initial_A']);a0=a.code();Sset=set(S);rank={x:i for i,x in enumerate(S)}
    def cnode():
        if not S:return None
        u=a.root
        while u<S[0] or u>S[-1]:u=a.c[u][int(u<S[0])];assert u
        return u
    c=cnode();q=bisect_right(S,c) if c is not None else 0;q0=q
    Smask=sum(1<<(x-1) for x in S);RA=lam=absvar=signed=0;moving=[];lastKEEP=None;firstKEEP=None;keepcoords=[]
    byop=defaultdict(int);maxjump=0
    for e in events:
        if e['actor']!='A':continue
        u,v=e['pivot'],e['promoted'];middle=e['middle'];m=(a.m[middle]&Smask).bit_count() if middle else 0
        active=bool(S and u==c and S[0]<=v<=S[-1])
        predicted=(m+int(v in Sset)) if active and v>u else -(m+int(u in Sset)) if active else 0
        before=q;a.step(e);c=cnode();q=bisect_right(S,c) if c is not None else 0
        assert q-before==predicted,(s['name'],e['id'],q-before,predicted)
        RA+=1;byop[e['id'][1]]+=1;signed+=predicted;absvar+=abs(predicted);maxjump=max(maxjump,abs(predicted))
        if active:
            lam+=m.bit_length()
            if m:moving.append({'bit':e['id'],'pivot':u,'promoted':v,'middle_S_size':m,'delta_q':predicted})
    a.recompute();assert a.code()==a0 and signed==0 and q==q0
    A=sum((v+1)//2 for v in byop.values()) # each operation has exactly its actual rotation depth
    assert RA<=2*A
    xs=[x for tag,x in s['operations'] if tag=='K']
    raw=sum(int(x!=xs[i-1])+abs(rank[x]-rank[xs[i-1]]).bit_length() for i,x in enumerate(xs)) if S else 0
    assert raw<=2*RA+lam<=4*A+lam
    if not lam:assert raw<=3*A
    return {'source':s['name'],'source_sha256':digest(s),'S_size':len(S),'A':A,'real_A_bits':RA,
        'Lambda_A':lam,'raw_periodic_cost':raw,'cyclic_signed_q_change':signed,'absolute_q_variation':absvar,
        'maximum_q_jump':maxjump,'positive_middle_A_bits':len(moving),'positive_middle_examples':moving[:8],
        'raw_le_4A_plus_Lambda':True,'lambda_le_6A_implies_periodic_paid':lam<=6*A,
        'Lambda_zero_stronger_raw_le_3A':not lam,'actual_z_claim':'No positive z inferred from rank traffic.'}

if __name__=='__main__':
    meter=Meter('original_LCA_rank_law');out=[];cat=controls();assert len(cat)==80
    for i,e in enumerate(cat):
        s=e['source']
        if e.get('expansion'):
            p=load(C2/'BOOST_SHORT_PHYS.json');ev=expanded(p,load(C2/'BOOST_EVENT_EXPANSION.json'))
            row=audit(s,p['original_S'],ev);row['physical_scope']='Exact C2 original-event expansion; full short independent replay and prior whole-word fast replay pinned.'
        else:
            p=load(e['physical']);row=audit(s,p['original_S'],p['events'])
            row['physical_scope']='New edge/mask rank-law reconstruction on sealed complete original primitive word.'
        row.update(index=i,origin=e['origin']);out.append(row);write('LCA_RANK_RESULTS.json',out)
        print('PASS rank law',i,'A',row['A'],'Lambda',row['Lambda_A'],'raw',row['raw_periodic_cost'],flush=True)
        del p;gc.collect()
    write('CONTROL_REFERENCE_CATALOG.json',[{**e,'source_sha256':digest(e['source']),
        'physical_sha256':hfile(e['physical']) if e['physical'] else None} for e in cat])
    meter.info.update(complete_sources=len(out));meter.ok=True

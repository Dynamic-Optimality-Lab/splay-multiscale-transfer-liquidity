"""Global last-promotion forest on all original B doubles."""
from ledger5 import *

def forest(r):
    by_g=defaultdict(list);dem=defaultdict(list);prom=defaultdict(list)
    for p,d in sorted(r.doubles.items()):by_g[d['g']].append(p)
    for e in r.events:
        if e['actor']=='A':dem[e['pivot']].append((e['time'],e))
        else:prom[e['promoted']].append((e['time'],e))
    out={};root_bits=set();used_donor=set();children=defaultdict(list)
    A=r.A;T=r.T
    for g,ps in by_g.items():
        for i,p in enumerate(ps):
            prev=ps[i-1]
            lo=r.boundaries[prev[0]-1]['end_time'];hi=r.boundaries[p[0]-1]['post_A_time']
            if hi<lo:lo-=T
            resets=lifted(dem[g],lo,hi,T);psel=lifted(prom[g],lo,hi,T)
            if resets:
                root=tuple(resets[-1][1]['id']);assert root not in root_bits;root_bits.add(root)
                out[p]={'kind':'actual_A_reset','A_bit':root,'predecessor':None}
                continue
            if psel:
                e=psel[-1][1];assert e['target']!=g and e['id'][3]==0 and e['case'] in ('LL','RR')
                pred=tuple(e['id'][1:3]);assert pred not in used_donor;used_donor.add(pred)
                kind='last_non_target_promotion'
                cap=r.events[r.doubles[pred]['events'][1]-1]['demoted_label']
            else:
                pred=prev;kind='no_promotion_same_column';cap=r.doubles[pred]['J']
            f=r.doubles[p]['F'];F=r.doubles[pred]['F'];x=r.ops[pred[0]-1][1]
            assert f&~cap==0 and cap&~F==0 and F&r.bits[x] and not cap&r.bits[x]
            out[p]={'kind':kind,'predecessor':pred,'frame':r.label_keys(f),
                    'predecessor_frame':r.label_keys(F)}
            children[pred].append(p)
    assert len(root_bits)<=2*A and max(map(len,children.values()),default=0)<=2
    depth={};which={}
    for p in sorted(out,key=lambda p:-r.doubles[p]['F'].bit_count()):
        pred=out[p]['predecessor']
        depth[p]=0 if pred is None else depth[pred]+1
        which[p]=p if pred is None else which[pred]
        out[p]['depth']=depth[p]
    multiplicity=Counter(which.values());violations=[]
    for p,cs in children.items():
        if len(cs)==2:
            a,b=cs;F1=r.doubles[a]['F'];F2=r.doubles[b]['F']
            if F1&F2:
                violations.append({'predecessor':p,'children':cs,'overlap':r.label_keys(F1&F2)})
    return {'rows':[{'parent':p,**out[p]} for p in sorted(out)],'roots':len(root_bits),
            'actual_original_Q_B':len(out),'maximum_depth':max(depth.values(),default=0),
            'max_component_size':max(multiplicity.values(),default=0),
            'number_of_binary_vertices':sum(len(c)==2 for c in children.values()),
            'overlapping_child_frames':violations,
            'proof_scope':'All physical original B doubles; not only residuals. Strict containment, actual cyclic A demotions, and at most two successors.'}

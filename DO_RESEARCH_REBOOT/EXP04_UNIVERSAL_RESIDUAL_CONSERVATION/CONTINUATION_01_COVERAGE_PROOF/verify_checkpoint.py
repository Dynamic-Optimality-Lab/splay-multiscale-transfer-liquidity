from core import *
from return_normalization import guarded_skeleton,irredundant_subcover
from gap_payment import keep_gaps,hard_guarded
from all_intervals import all_intervals_through,materialize


def tuple_rotate(ind,t,u,side):
    assert t[0]=='node'
    _,k,l,rr=t
    if k==u:
        if side==0:
            _,v,vl,vr=l;return ind.node(v,vl,ind.node(k,vr,rr))
        _,v,vl,vr=rr;return ind.node(v,ind.node(k,l,vl),vr)
    return ind.node(k,tuple_rotate(ind,l,u,side),rr) if u<k else ind.node(k,l,tuple_rotate(ind,rr,u,side))


def tuple_data(t,bits):
    if t[0]=='leaf':return 0,set(),set(),{}
    _,k,l,rr=t;ll,ls,le,lm=tuple_data(l,bits);rl,rs,re,rm=tuple_data(rr,bits)
    lab=ll|rl|bits.get(k,0);edges=le|re
    if l[0]=='node':edges.add((k,l[1],0))
    if rr[0]=='node':edges.add((k,rr[1],1))
    return lab,ls|rs|({lab} if lab else set()),edges,{**lm,**rm,k:lab}


def independent_Pi(r):
    """Second SET/Pi reconstruction from immutable primitive tuple rotations.

    This verifies the complete original Pi and U predicates. Frozen scan,
    return and restart selection are deliberately still their pinned engines.
    """
    a=r.as_tuple(Tree(r.source['initial_A']));b=r.as_tuple(Tree(r.source['initial_B']))
    _,aset,_,_=tuple_data(a,r.bits);_,bset,_,_=tuple_data(b,r.bits)
    Asets=[frozenset(aset)];Bcreates=defaultdict(list);Blosses=defaultdict(list)
    pools={};timeline=[]
    def ref(s):
        z=sorted(s);h=digest(z);pools[h]=z;return h
    timeline.append({'time':0,'A':ref(aset),'B':ref(bset)})
    for ev in r.events:
        actor=ev['actor'];before=aset if actor=='A' else bset
        tree=a if actor=='A' else b
        _,_,edges,before_labs=tuple_data(tree,r.bits)
        if actor=='B' and ev['id'][3]==0 and ev['case']!='ZIG':
            cur=tree;path=[]
            while cur[0]=='node':
                path.append(cur[1])
                if cur[1]==ev['target']:break
                cur=cur[2] if ev['target']<cur[1] else cur[3]
            g,p,x=path[-3:];d=r.doubles[tuple(ev['id'][1:3])]
            assert d['g']==g and d['F']==before_labs[g]
            assert d['case']==('R' if p>g else 'L')+('R' if x>p else 'L')
        after_tree=tuple_rotate(r.ind,tree,ev['pivot'],ev['side'])
        _,after,newedges,after_labs=tuple_data(after_tree,r.bits)
        lost=before-after;created=after-before
        assert sorted(lost)==ev['lost'] and sorted(created)==ev['created']
        assert sorted(edges-newedges)==list(map(tuple,ev['deleted']))
        assert sorted(newedges-edges)==list(map(tuple,ev['added']))
        if actor=='A':
            sign=len(lost&bset)-len(created&bset);a=after_tree;aset=after
        else:
            sign=len(after-aset)-len(before-aset);b=after_tree;bset=after
            for lab in lost:Blosses[lab].append(ev['time'])
            for lab in created:Bcreates[lab].append(ev['time'])
            if ev['case']!='ZIG':
                d=r.doubles[tuple(ev['id'][1:3])]
                if d['nu']==ev['time']:assert d['J']==after_labs[ev['pivot']]
        assert sign==ev['sign']
        Asets.append(frozenset(aset));timeline.append({'time':ev['time'],'A':ref(aset),'B':ref(bset)})
    assert a==r.as_tuple(Tree(r.source['initial_A'])) and b==r.as_tuple(Tree(r.source['initial_B']))
    def any_A(lab,lo,hi):
        assert 0<=hi-lo<=r.T
        return any(lab in Asets[i%r.T] for i in range(lo,hi+1))
    def prev(times,before):
        return max(t+((before-1-t)//r.T)*r.T for t in times)
    u={}
    for key,d in r.doubles.items():
        if d['signs']!=[0,0] or d['F']&r.extremes:continue
        post=r.boundaries[key[0]-1]['post_A_time'];gamma=prev(Bcreates[d['F']],post+1);kappa=prev(Blosses[d['F']],gamma)
        assert 0<post-kappa<=r.T
        if any_A(d['F'],kappa,post):continue
        h=next((key[0]+dt-1)%len(r.ops)+1 for dt in range(1,len(r.ops)+1)
               if r.ops[(key[0]+dt-1)%len(r.ops)][0]=='K' and r.bits.get(r.ops[(key[0]+dt-1)%len(r.ops)][1],0)&d['J'])
        hit=r.boundaries[h-1]['post_A_time']+(r.T if h<=key[0] else 0)
        exposed=any_A(d['J'],d['nu'],hit)
        u[key]={'Gamma':gamma,'kappa':kappa,'post_A':post,'h':h,'hit_time':hit,'exposed':exposed}
        assert all(d[k]==v for k,v in u[key].items())
    assert set(u)==set(r.U)
    return {'immutable_tuple_primitive_rotations':len(r.events),'independently_verified_original_U':len(u),
            'Pi_carrier_set_pool':pools,'Pi_after_original_primitive':timeline,
            'qualification':'Independent physical primitive SET/Pi/U verification; frozen R_* selectors use pinned original implementations.'}


def subcover_tests():
    checks=0
    for n in range(1,5):
        arcs=[{'operations':[(s+j)%n+1 for j in range(length)]}
              for length in range(1,n) for s in range(n)]+[{'operations':list(range(1,n+1))}]
        for mask in range(1<<len(arcs)):
            selected=[a for i,a in enumerate(arcs) if mask>>i&1]
            irredundant_subcover(selected,n);checks+=1
    return {'all_cyclic_arc_families_n_le_4':checks,'role':'Implementation sanity only; source-uniform validity is the analytic C1 proof.'}


def compressed_domain_check(r,norm):
    J=set(norm['J']);st=norm['initial_B']
    if not J:return 0
    short={'root':st['root'],'children':{str(k):[v if v in J else None for v in st['children'][str(k)]] for k in J}}
    b=Tree(short);bt=r.as_tuple(b);Q=0
    for t in norm['retained_KEEP']:
        row=r.boundaries[t-1];assert b.path(row['x'])==row['B_path']
        bt,ev=r.ind.trace(bt,row['x']);Replay.plain_splay(b,row['x']);assert bt==r.as_tuple(b)
        Q+=sum(e[0]!='ZIG' for e in ev)
    assert Q==norm['retained_actual_Q']
    return len(norm['retained_KEEP'])


if __name__=='__main__':
    meter=Meter('CONT01_checkpoint_verification');checks=subcover_tests()
    s=json.loads((ROOT/'OWNERSHIP_SOURCES.json').read_text())[0];r=Replay(s)
    expected=json.loads((ROOT/'OWNERSHIP_RESULTS.json').read_text())[0]
    assert digest(r.events)==s['trace_hash'] and r.independent_checks==len(r.ops)
    ev,classification,restarts=original_residual(r);assert ev==expected['R_star'];r.original_R_star=ev
    row=metrics(r,ev);en=enriched(r,row);eps,_=psi_episodes(r);den=density_analysis(r,ev,eps)
    paid={digest(e['rho']) for e in row['new_comparison']['paid']+en['monotone_comparison']['paid']+en['rank_certificate_paid']+den['paid']}
    assert all(digest(e['rho']) not in paid for e in ev)
    audit=all_intervals_through(r,ev[0]['consumer']);old=json.loads((ROOT/'ALL_INTERVALS_ESCAPE_AUDIT.json').read_text())
    assert audit['best']==old['best'] and audit['feasible'][4] is None and audit['exhaustive']
    norm=guarded_skeleton(r,list(range(1,len(r.ops)+1)));gap=keep_gaps(r)
    assert norm['D']<=5*r.A and all(gap[e['consumer']]['cheap_q_le_2A_gap'] for e in ev)
    pi=independent_Pi(r);write('INDEPENDENT_ORIGINAL_PI.json',pi)
    cert={'source':s,'summary':r.summary(),'original_R_star':ev,
          'original_pair_certificates':[p for p in r.pairs if p['rho'] in [e['rho'] for e in ev]],
          'original_U':[{'key':list(k),**v} for k,v in r.U.items()],
          'original_consumer_parents':[r.U[tuple(e['original_parent'])] for e in ev],
          'frozen_combined_escape_verified':True,'all_raw4_intervals_ineligible_verified':True,
          'minimum_raw_interval_ratio':str(Fraction(audit['best']['D'],audit['best']['A'])),
          'guarded_D':norm['D'],'guarded_A':r.A,
          'critical_KEEP_gaps':[gap[e['consumer']] for e in ev],
          'compressed_domain_accesses':compressed_domain_check(r,norm),
          'independent_Pi_artifact':'INDEPENDENT_ORIGINAL_PI.json',**checks}
    write('CRITICAL_WITNESS_CERTIFICATE.json',cert)
    oldmanifest=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    for file,sha in oldmanifest['parent_files'].items():assert file_hash(PARENT/file)==sha,file
    meter.success=True;meter.details.update(parent_files_unchanged=len(oldmanifest['parent_files']),
        immutable_original_operations=len(r.ops),independent_original_primitives=r.T,**checks)
    print('PASS',len(r.ops),'original operations;',r.T,'independent primitive SET/Pi checks;',
          checks['all_cyclic_arc_families_n_le_4'],'subcover implementation families;',flush=True)

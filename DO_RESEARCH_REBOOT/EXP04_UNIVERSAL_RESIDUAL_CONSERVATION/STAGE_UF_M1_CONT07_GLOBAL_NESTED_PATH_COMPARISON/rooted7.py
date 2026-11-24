from base7 import *
from catalog7 import known_inputs
from cohortc import decode_state
from exp01_oracle import Tree,Replay
from model0 import to_tuple
from independent import splay as ind

def substate(st,g):
    cs={};todo=[g]
    while todo:
        k=todo.pop();l,r=st['children'][str(k)];cs[str(k)]=[l,r]
        if l is not None:todo.append(l)
        if r is not None:todo.append(r)
    out={'root':g,'children':cs};Tree(out);return out

def component(st,g):
    if g is None:return []
    cs=substate(st,g)['children'];return sorted([int(k),*v] for k,v in cs.items())

def side_component(st,g,side):
    child=st['children'][str(g)][side];return [child,component(st,child)]

def rooted_test(p,path):
    rows=p['boundaries'];ds={tuple(d['parent']):d for d in p['doubles']};g=path['old_g'];u=tuple(path['path'][0]);initial=decode_state(p,rows[u[0]-1]['post_B_state']);local=substate(initial,g);out=[]
    for side,hs in enumerate((path['left_inside_hits'],path['right_inside_hits'])):
        if not hs:out.append({'side':side,'domain':[],'retained':[],'Q':0,'matches':[]});continue
        tree=Tree(local);immutable=to_tuple(local);J=set();matches=[];Q=0;trace=[]
        for h,x in hs:J.update(Tree(local).path(x))
        assert sorted(J)==path['component_rooted_domains'][side]
        for h,x in hs:
            actual_pre=decode_state(p,rows[h-1]['pre_B_state']);actual_post=decode_state(p,rows[h-1]['post_B_state']);before=tree.state()
            assert side_component(before,g,side)==side_component(actual_pre,g,side)
            old=next((w for w,d in ds.items() if w[0]==h and d['g']==g),None)
            if old:
                distance=len(tree.path(x))-1-tree.path(x).index(g);assert distance==2*old[1];matches.append(list(old))
            immutable,ev=ind.trace(immutable,x);Replay.plain_splay(tree,x);after=tree.state();assert to_tuple(after)==immutable
            assert side_component(after,g,side)==side_component(actual_post,g,side)
            q=sum(e[0]!='ZIG' for e in ev);Q+=q
            trace.append({'h':h,'target':x,'pre_sha256':digest(before),'post_sha256':digest(after),'q':q})
        out.append({'side':side,'domain':sorted(J),'retained':hs,'Q':Q,'matches':matches,'initial_full_g_component':local,'trace':trace})
    return out

if __name__=='__main__':
    unsealed();m=Meter('rooted_component_and_paid_hit_elision');work=load(ROOT/'INHERITED_PATH_WORKLOADS.json');out=[];elision=None
    for z in work:
        if not z['maximal_PF_paths']:continue
        p=load(z['physical']);tests=[]
        for path in z['maximal_PF_paths']:tests.append({'old_g':path['old_g'],'path':path['path'],'side_shadows':rooted_test(p,path)})
        out.append({'source':z['source'],'source_sha256':z['source_sha256'],'tests':tests})
        if z['source']=='M1C6_nested_k4_L3':
            path=z['maximal_PF_paths'][0];assert path['path']==[[3,4],[7,4]];g=path['old_g'];initial=decode_state(p,p['boundaries'][2]['post_B_state']);tree=Tree(initial)
            before=tree.path(p['boundaries'][6]['x']);distance=len(before)-1-before.index(g)
            acc=load(C6/'FRESH_ORDERED_00.json');paid=[e for e in acc['disjoint_original_assignments']['skipped_rank'] if e['consumer']==5]
            assert paid and distance%2==1
            elision={'source_catalog':str(C6/'FRESH_SOURCE_CATALOG.json'),'catalog_index':0,'source_sha256':z['source_sha256'],
                'canonical_path':path,'omitted_original_F_paid_KEEP':5,'omitted_paid_original_gaps':paid,
                'retained_original_KEEP':7,'retained_original_parent':[7,4],'shadow_pre_path_after_elision':before,
                'shadow_g_distance':distance,'original_g_distance':8,'old_g_double_missing_after_elision':True,
                'actual_S_PF':[],'scope':'Exact pre-H original C_old path; not a post-hybrid survivor.'}
        gc.collect()
    assert elision is not None
    write('ROOTED_COMPONENT_SHADOW_AUDIT.json',out);write('EXACT_PAID_HIT_ELISION_REFUTATION.json',elision)
    m.info['complete_sources_with_paths']=len(out);m.ok=True;print('PASS rooted component shadows;',len(out),'sources; exact F-paid hit elision refuted',flush=True)

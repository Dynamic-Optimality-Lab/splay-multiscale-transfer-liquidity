from delivery_support3b import *
from independent_path_audit import check,checked_access
from types import SimpleNamespace
from fast_physics import FullTree,path_hull


def prefix(s):
    diag=s.get('diagonal_initial',s['initial_A']);a=FullTree(diag);b=FullTree(diag)
    from independent import splay as ind
    view=SimpleNamespace(ind=ind);aa=Replay.as_tuple(view,Tree(diag));bb=aa
    for tag,x in s.get('reaching_prefix',[]):
        aa,_,_,_,_,_=checked_access(a,aa,x,b,'A')
        if tag=='K':bb,_,_,_,_,_=checked_access(b,bb,x,a,'B')
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    return len(s.get('reaching_prefix',[]))


if __name__=='__main__':
    meter=Meter('source_append' if '--append' in sys.argv else 'all_complete_sources');sources,rows,_=collect();out=[]
    previous_checks={}
    if '--append' in sys.argv:
        previous_checks={z['source']:z for z in json.loads((ROOT/'ALL_SOURCE_VERIFICATION.json').read_text())}
    for k,s in enumerate(sources,1):
        if s['name'] in previous_checks:
            old=previous_checks[s['name']]
            assert old['A']==s['A'] and old['Q_B']==s['Q_B'] and old['original_operations']==len(s['operations'])
            out.append(old);continue
        z=check(s);z['explicit_common_diagonal_reaching_prefix_operations_verified']=prefix(s)
        M={x for tag,x in s['operations'] if tag=='K'};S=path_hull(Tree(s['initial_B']),M)
        z['original_raw_support']=sorted(S)
        from periodic_payment import periodic_cost
        cost=periodic_cost([x for tag,x in s['operations'] if tag=='K'],S)
        assert cost['B_cyclic']<=10*s['A']
        z['positive_old_raw_periodic_certificate']=cost
        out.append(z)
        if k%25==0 or k==len(sources):
            write('ALL_SOURCE_VERIFICATION.json',out);print('PASS complete original states and reachability',k,'of',len(sources),flush=True)
    write('ALL_SOURCE_VERIFICATION.json',out)
    meter.success=True;meter.details.update(total_complete_original_sources=len(out),
        previous_completed_checks_reused=len(previous_checks),new_full_checks=len(out)-len(previous_checks))

from campaign3b import *
from verify_scoped_classes import subtree


if __name__=='__main__':
    meter=Meter('lifecycle_verification')
    cert=json.loads((ROOT/'COUNTEREXAMPLE_CERTIFICATE.json').read_text())
    t=json.loads((ROOT/cert['complete_original_trace']).read_text());s=t['source']
    assert s['name']==cert['source']
    lo=t['boundaries'][645]['end_time'];hi=t['boundaries'][652]['post_A_time']
    parent=next(p for p in cert['original_parent_certificates'] if p['parent']==[653,4])
    last=parent['original_U']['events'][-1]
    b=Tree(s['initial_B']);fixed=None;changes=[]
    for ev in t['events']:
        before=154 in b.path(120)[:-1]
        if ev['actor']=='B':b.rotate(ev['pivot'],ev['side'])
        after=154 in b.path(120)[:-1]
        if ev['time']==lo:fixed=subtree(b,154);assert after
        if fixed is not None and lo<=ev['time']<=hi:assert subtree(b,154)==fixed
        if lo<ev['time']<=last and before!=after:changes.append({'id':ev['id'],'present_after':after})
        if ev['time']==last:break
    assert changes==[{'id':['B',653,4,1],'present_after':False}]
    write('B_ANCESTRY_LIFECYCLE_VERIFICATION.json',{'source':s['name'],'old_g':154,'later_target':120,
        'B_relation_present_immediately_after_first_consumer':True,
        'full_B_subtree_154_rigid_until_second_B_access_starts':True,
        'B_component_key_interval':[min(fixed),max(fixed)],
        'B_relation_changes_between_consumers':changes,'B_relation_recreated_between_consumers':False,
        'meaning':'The later demand retargets a descendant already below g; no intervening g-to-that-target recreation or A repair is forced.'})
    print('PASS exact B retargeting lifecycle; no recreated g154->120 relation between consumers',flush=True)
    meter.success=True

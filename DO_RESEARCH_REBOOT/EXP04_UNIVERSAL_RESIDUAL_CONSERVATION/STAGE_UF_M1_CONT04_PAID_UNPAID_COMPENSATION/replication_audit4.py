from base4 import *
from probe_long4 import expanded_boundaries

def old_boundaries(p,rule):
    start=rule['template_original_operations'][0];copies=rule['copies_in_long']
    yield from p['boundaries'][:start-1]
    for c in range(copies):
        for row in p['boundaries'][start-1:start+1]:
            z={**row,'t':row['t']+2*c}
            for key in ('start_time','post_A_time','end_time'):z[key]+=4*c
            yield z
    for row in p['boundaries'][start+1:]:
        z={**row,'t':row['t']+2*(copies-1)}
        for key in ('start_time','post_A_time','end_time'):z[key]+=4*(copies-1)
        yield z

def local_audit(s,p,rows):
    states=p['state_pool']['states'];count=0;examples=[];first=None;previous=None;N=len(s['operations'])
    def pair(r,t):
        nonlocal count
        if r['tag']!='K' or t['tag']!='K':return
        if r['a']!=1 or t['a']!=1 or r['q'] or t['q']:return
        ap,bp,at,bt=r['A_path'],r['B_path'],t['A_path'],t['B_path']
        if not (len(ap)==len(bp)==len(at)==len(bt)==2 and ap==bp and at==bt and ap==at[::-1]):return
        if states[r['pre_A_state']]!=states[t['post_A_state']] or states[r['pre_B_state']]!=states[t['post_B_state']]:return
        b0,b1,b2=states[r['pre_B_state']],states[r['post_B_state']],states[t['post_B_state']]
        assert b0==b2 and b1!=b0
        # Exact source-state transducer; this is not a new experimental source.
        for copies in (1,2,3):
            stack=[];locations={b0:0};records=[(0,b0)]
            for state in [b1,b0]*copies:
                if state in locations:
                    j=locations[state];del stack[j:]
                    while records[-1][0]>j:
                        _,old=records.pop();del locations[old]
                else:stack.append(state);locations[state]=len(stack);records.append((len(stack),state))
            assert not stack and locations=={b0:0}
        count+=1
        if len(examples)<6:examples.append({'original_operations':[r['t'],t['t']],'targets':[r['x'],t['x']],
            'first_pre_A_state':r['pre_A_state'],'first_pre_B_state':r['pre_B_state'],'inverse_complete_states_verified':True})
    for r in rows:
        if first is None:first=r
        if previous is not None:pair(previous,r)
        previous=r
    if first is not None:pair(previous,first)
    return {'source':s['name'],'source_sha256':digest(s),'qualifying_exact_two_zig_identity_blocks':count,'examples':examples,
        'checked_law':'Actual two A zigs, no B double/guard, complete paired-state identity, empty local G/H stack after every replicated copy.',
        'scope':'Applicability check only when such a block exists; a positive base periodic certificate is separately required. No actual residual inferred.'}

if __name__=='__main__':
    m=Meter('all_controls_guardfree_replication_law');out=[]
    for e in load(C3/'CONTROL_REFERENCE_CATALOG.json'):
        if e.get('expansion'):
            p=load(C2/'BOOST_SHORT_PHYS.json');rows=old_boundaries(p,load(C2/'BOOST_EVENT_EXPANSION.json'))
        else:p=load(e['physical']);rows=iter(p['boundaries'])
        out.append(local_audit(e['source'],p,rows));del p;gc.collect()
    for stem in ('DEFORM','SHARED'):
        for i,s in enumerate(load(ROOT/f'{stem}_SOURCE_CATALOG.json')):
            p=load(ROOT/f'{stem}_PHYS_{i:02}.json');out.append(local_audit(s,p,iter(p['boundaries'])));del p;gc.collect()
    p=load(ROOT/'PROBE_SHORT_PHYS.json');s=load(ROOT/'PROBE_SHORT_SOURCE.json')
    out.append(local_audit(s,p,iter(p['boundaries'])))
    s=load(ROOT/'PROBE_LONG_SOURCE.json');out.append(local_audit(s,p,expanded_boundaries(p,load(ROOT/'PROBE_EVENT_EXPANSION.json'))))
    assert len(out)==96
    write('GUARDFREE_REPLICATION_RESULTS.json',out);m.info['complete_sources']=len(out);m.ok=True
    print('PASS guarded-return local replication law on96 complete controls; scoped theorem, no finite coverage inference',flush=True)

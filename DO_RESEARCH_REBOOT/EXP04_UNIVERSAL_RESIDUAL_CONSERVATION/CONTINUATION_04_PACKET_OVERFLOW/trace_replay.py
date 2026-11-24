"""Lossless original-event delta trace, preserving every full physical key.

Every complete boundary state is reconstructible from the full initial pair
and ALL primitive pointer changes. No hanger/subtree is contracted.
"""
from campaign4 import *
from packed_states import install

if __name__=='__main__':
    meter=Meter('trace_replay');pool,restore=install(Tree)
    s=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())[0]
    r=Replay(s,independent=False)
    assert digest(r.events)==s['trace_hash']
    boundaries=[]
    for row in r.boundaries:
        z={k:v for k,v in row.items() if k not in ('pre_A','pre_B','post_A','post_B')}
        z.update({k+'_root':row[k]['root'] for k in ('pre_A','pre_B','post_A','post_B')})
        boundaries.append(z)
    trace={'format':'lossless complete original physical state delta stream',
        'source':s,'events':r.events,'boundaries':boundaries,'original_S':sorted(r.S),
        'full_state_reconstruction':'Start from both complete initial dictionaries; apply every actor/pivot/side rotation and its exact deleted/added edges, in original order. Boundary offsets and roots identify every pre/post A/B tree.',
        'independent_check_binding':'Primitive stream hash must equal the source hash used by NEW_INDEPENDENT_PI/R6 and WIDTH_VERIFICATION.',
        'original_event_sha256':digest(r.events)}
    write('ORIGINAL_EVENT_TRACE.json',trace)
    # An event-only reconstruction checks every full labelled pointer field
    # affected by each rotation and all boundary roots, then exact closure.
    a=Tree(s['initial_A']);b=Tree(s['initial_B']);i=0
    for row in boundaries:
        assert (a.root,b.root)==(row['pre_A_root'],row['pre_B_root'])
        for end in (row['post_A_time'],row['end_time']):
            while i<end:
                e=r.events[i];tree=a if e['actor']=='A' else b
                v,c,m,deleted,added=tree.rotate(e['pivot'],e['side'])
                assert sorted(deleted)==list(map(tuple,e['deleted'])) and sorted(added)==list(map(tuple,e['added']))
                assert (v,c,m)==(e['promoted'],e['external'],e['middle']);i+=1
        assert (a.root,b.root)==(row['post_A_root'],row['post_B_root'])
    assert i==r.T and a.state()==s['initial_A'] and b.state()==s['initial_B']
    write('TRACE_CHECK.json',{'source':s['name'],'primitive_count':r.T,'operation_boundary_count':len(boundaries),
        'event_sha256':digest(r.events),'complete_event_delta_state_reconstruction_checked':True,
        'trace_file':'ORIGINAL_EVENT_TRACE.json'})
    restore();meter.success=True;print('PASS lossless complete original delta trace and every operation boundary',flush=True)

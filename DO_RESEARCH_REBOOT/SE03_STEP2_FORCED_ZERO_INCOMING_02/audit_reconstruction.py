"""Reuse sealed control records; reconstruct complete source states, no replay."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def main():
    d=json.loads((OLD/'symbolic_replay.json').read_text());p=json.loads((OLD/'source_proof_audit.json').read_text())
    debt=json.loads((OLD/'debt_v3_audit.json').read_text())
    assert p['status']=='PASS_INDEPENDENT_UNIVERSAL_SOURCE_COUNTERCERTIFICATES'
    records=[]
    for f in d['families']:
        lo,hi=f['critical_occurrences'];start=f['critical_packet']['start_after']
        def state(trees,lru):
            return {'A':trees[0],'BF':trees[1],'BE':trees[2],'M':[1,3,5,7,9,11],
                'erased':f['erased_key'],'recent':lru,'packet_phase':'ready'}
        s=state(f['rows'][lo-1]['before'],f['charts'][lo-1]['recent_before'])
        t=state(f['rows'][hi-1]['after'],f['charts'][hi-1]['recent_after'])
        assert f['critical_packet']['w']==-2 and f['charts'][lo-1]['cold']
        q={'family':f['name'],'F_state':s,'T_state':t,'F_id':digest(s),'T_id':digest(t),
            'M':s['M'],'erased':s['erased'],'negative_packet':f['critical_packet'],
            'known_original_closed_word':f['word'],'prefix_through_T':f['word'][:hi],
            'F_boundary_absolute':len(f['word'])+start,'T_boundary_absolute':len(f['word'])+hi,
            'previous_debt_report':next(x for x in debt['witnesses'] if x['name']==f['name']),
            'membership_proof':'same actual source period; no fact about Dhat is used to force Dstar'}
        records.append(q)
    F={r['F_id'] for r in records};T={r['T_id'] for r in records}
    intersections=sorted(F&T)
    assert not intersections
    # Different full A states cannot be spliced even when B/chart agree.
    a,b=records[0],records[1]
    assert a['F_state']['BF']==b['F_state']['BF'] and a['F_state']['A']!=b['F_state']['A']
    out('forced_regions.json',{'status':'PASS_EXACT_KNOWN_FORCED_REGIONS','records':records,
        'known_F_intersect_T':intersections,'global_F_intersect_T_claimed_empty':False,
        'full_identity_fields':['A','BF','BE','M','erased','recent','packet_phase'],
        'source_occurrences_are_provenance_not_merged_tree_identity':True,
        'old_normalization_is_not_Dstar':True,'repeated_Campaign01_tests':0})
    print('PASS exact known F/T states, genuine chart phases and complete-state inequality; old tests reused')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_reconstruction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'new_finite_tests':0,'source_engine_calls':0})

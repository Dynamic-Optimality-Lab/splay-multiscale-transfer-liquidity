"""Explain and check pre-JSON numeric metadata hashes without changing evidence."""
from basec import *
import copy,gc

if __name__=='__main__':
    m=Meter('source_hash_provenance');ss=load(ROOT/'GUARDED_SOURCES.json');rows=load(ROOT/'GUARDED_RESULTS.json');out=[];quota=[]
    for i,(s,row) in enumerate(zip(ss,rows)):
        original=copy.deepcopy(s)
        for field in ('core_labels','gap_labels'):original[field]={int(k):v for k,v in original[field].items()}
        canonical=digest(s);generator=digest(original)
        assert row['source_sha256'] in (canonical,generator)
        assert {k:v for k,v in s.items() if k not in ('core_labels','gap_labels')}=={
            k:v for k,v in original.items() if k not in ('core_labels','gap_labels')}
        physical={k:s[k] for k in ('initial_A','initial_B','diagonal_initial','reaching_prefix','operations')}
        evidence={}
        for label in ('PHYS','BIRTH'):
            n=f'GUARDED_{label}_{i:02}.json';z=load(ROOT/n)
            assert z['source_sha256']==row['source_sha256']
            if label=='PHYS':
                paid=[]
                for h,j in row['critical_ids'][1:]:
                    assert j==1 and s['operations'][h-2][0]=='K'
                    ah=z['boundaries'][h-1]['a'];assert ah>=1 and j<=2*ah
                    paid.append({'original_parent':[h,j],'original_incoming_KEEP_gap_A':ah,
                        'quota_capacity':2*ah,'necessarily_quota_selected_if_in_D':True})
                quota.append({'source':s['name'],'k':s['k'],'critical_C_parents':paid})
            evidence[n]={'sha256':hfile(ROOT/n),'declared_source_sha256':z['source_sha256']}
            del z;gc.collect()
        out.append({'index':i,'source':s['name'],'canonical_loaded_JSON_source_sha256':canonical,
            'original_generator_numeric_metadata_sha256':generator,'recorded_evidence_source_sha256':row['source_sha256'],
            'physical_input_payload_sha256':digest(physical),'difference_only_numeric_metadata_key_sorting':True,
            'source_and_event_files_mutated':False,'evidence':evidence})
    write('SOURCE_HASH_PROVENANCE.json',out);write('GUARDED_CRITICAL_QUOTA.json',quota);m.ok=True
    print('PASS guarded source-hash provenance; no source/event evidence rewritten',flush=True)

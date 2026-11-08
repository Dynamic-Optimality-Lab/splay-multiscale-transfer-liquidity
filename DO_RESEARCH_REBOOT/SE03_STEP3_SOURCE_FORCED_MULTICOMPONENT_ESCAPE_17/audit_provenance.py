"""Producer: bind NEW donor maps to each inherited actual owner interval.
This corrects C16's overbroad u=1 prose; no source/audit replay is run.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
C15=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def main():
    src=read(B/'preparation_supply_certificates.json');families={}
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        families[name]=read(C15/name)['reports']
    owners=read(C15/'owner_image_source_audit.json')['reports'];reports=[]
    for i,r in enumerate(src['reports']):
        if i<8:
            s=families[r['source_file']][r['report']];u=s['actual_reaching_prefix_copies'];L=s['L']
            block=len(s['base_word']);rows=s['rows'];owner_ref=None
        else:
            s=owners[i-8];u=s['u'];L=s['L'];block=len(rows:=s['rows'])//L
            owner_ref={'path':(C15/'owner_image_source_audit.json').relative_to(ROOT).as_posix(),
                'sha256':sha(C15/'owner_image_source_audit.json'),'report':i-8,'erased':s['erased'],
                'exact_actual_BE_and_f6_source':True,
                'full_A_BF_template_reference_is_not_the_BE_reference':True}
        base=u*block;last=base+L*block
        trans=lambda x:(x[0]+base,*x[1:])
        a=unpack(r['old_a']);f=unpack(r['allocation'])
        aa={trans(d):trans(v) for d,v in a.items()};ff={trans(d):trans(v) for d,v in f.items()}
        U={(t['occurrence']+base,j,b) for t in rows for j in range(1,t['a']+1) for b in (0,1)}
        D={(t['occurrence']+base,k) for t in rows for k in range(1,t['qF']+1)}
        assert set(ff)==D and set(ff.values())<=U and len(set(ff.values()))==len(ff)
        assert all(ff[d]==v for d,v in aa.items())
        assert all(base<z[0]<=last for z in set(ff)|set(ff.values()))
        reports.append({'producer_report':i,'source_erased':r['erased'],'u':u,'L':L,
            'base_word_length':block,'actual_interval':[base+1,last],
            'owner_reference':owner_ref,'actual_allocation':pack(ff),'actual_frozen_old_a':pack(aa),
            'actual_new_escape_pairs':[{'frontier':trans(e['frontier']),'unit':trans(e['unit'])} for e in r['lazy_escapes']]})
    two=next(x for x in reports[8:] if x['source_erased']==13)
    assert two['u']==0 and two['actual_interval']==[1,64]
    assert {tuple(x['unit']) for x in two['actual_new_escape_pairs']}=={(35,2,0),(35,2,1)}
    out('actual_period_certificates.json',{'status':'PRODUCER_PERIOD_TRANSPORT_AUDIT_PENDING','reports':reports,
        'correction':'C16 blanket u=1 language does not describe the erased13 source; its authoritative C15 owner receipt has u=0. No old source map is changed.',
        'C15_and_C16_independent_seals_not_completed':True})
    print(json.dumps({'status':'PRODUCER_ACTUAL_PERIOD_PASS','erased13_interval':two['actual_interval'],
        'u_by_erasure':[[s['erased'],s['u'],s['L']] for s in owners],'source_engine_calls':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_provenance_exit.json',{'whole_process_CPU_seconds':time.process_time(),
        'error':error,'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})

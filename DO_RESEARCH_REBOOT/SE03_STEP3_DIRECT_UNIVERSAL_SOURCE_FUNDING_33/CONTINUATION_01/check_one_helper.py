"""Complete independent sparse constraint check for one ordered helper.
Source grammar separately audited. Producer debt/queue routines not imported.
"""
import json,time,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def check(p,cap):
    start=time.process_time();A=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());F=json.loads((B/'nine_label_native_action_cache.json').read_text());name='one_helper_p%d_certificate.json'%p;C=json.loads((B/name).read_text());S=json.loads((B/'ten_anchor_schema_independent_audit.json').read_text());assert S['status']=='PASS_COMPLETE_TEN_ANCHOR_LOW_SCHEMA_LIFT'
    assert hashlib.sha256((B/'ten_anchor_LOW_source_schemas.json').read_bytes()).hexdigest()==C['source_schema_sha256']==S['input_sha256']['ten_anchor_LOW_source_schemas.json']
    assert hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest()==C['BF_primitive_sha256']
    AT=A['trees'];BT=F['trees'];AD=A['LOW_destination'];AH=A['H'];BD=F['destination'];BQ=F['Q'];N=len(BT);marks=[v for v in range(1,11) if v!=p];M={v:i for i,v in enumerate(marks)};L=dict(C['nonzero_debt']);assert len(L)==len(C['nonzero_debt']) and set(L.values())=={1,2}
    for code,value in L.items():a,b=divmod(code,N);assert 0<=a<len(AT) and AT[a][0]==marks[BT[b][0]-1]
    helper=[];direct=[];terminal=[];cheap=collections.defaultdict(list)
    for a,t in enumerate(AT):
        helper.append([(y,AD[a][y-1]) for y in range(1,11) if AH[a][y-1]==1])
        direct.append([(M[x],AD[a][x-1],AH[a][x-1]) for x in marks if 1<=AH[a][x-1]<=2])
        terminal.append([(M[x],AD[a][x-1]) for x in marks if AH[a][x-1]==1])
        for x in marks:
            if AH[a][x-1]==1:cheap[t[0],x].append(a)
    negative=positive=0;minimum=99
    for b,t in enumerate(BT):
        g=marks[t[0]-1]
        for x in range(9):
            q=BQ[b][x]
            if q<3:continue
            px=marks[x];bt=BD[b][x]
            for a in cheap[g,px]:
                margin=2-q+L.get(AD[a][px-1]*N+bt,0)-L.get(a*N+b,0);assert margin>=0;negative+=1;minimum=min(minimum,margin)
    for j,(code,value) in enumerate(L.items()):
        a,b=divmod(code,N);root=BT[b][0]-1;bb=BD[b];qq=BQ[b]
        for x,at,h in direct[a]:
            if x==root:continue
            margin=2*h-qq[x]+L.get(at*N+bb[x],0)-value;assert margin>=0;positive+=1;minimum=min(minimum,margin)
        for y,at in helper[a]:
            for x,att in terminal[at]:
                if x==root:continue
                margin=4-qq[x]+L.get(att*N+bb[x],0)-value;assert margin>=0;positive+=1;minimum=min(minimum,margin)
        if j%32768==0 and time.process_time()-start>cap-2:raise TimeoutError('INDEPENDENT_HELPER_CASE_CAP')
    assert max(max(v) for v in BQ)==4 and C['width']==2 and C['working_bank_bound']==8
    result={'status':'PASS_COMPLETE_ONE_HELPER_SOURCE_CASE','helper_physical_rank':p,'nonzero_coefficients':len(L),'width':2,'all_negative_LOW_source_rows':negative,'all_positive_source_LOW_rows':positive,'minimum_checked_margin':minimum,'HIGH_any_endpoint_proof':'6-Q+Dt-Ds>=6-4-2=0','working_bank_bound':8,'all_original_h0_selection':'first min(H,3) actual events include every natural own bit','source_scope':'fixed nine B anchors and full ten-anchor A backbone with this retained A-only helper; arbitrary repeated original words and rigid private gap populations','source_queries':0,'new_source_engine_calls':0,'semantic_basis_reused':'separately audited native9 ordinary primitives and uniform off-path free-leaf substitution','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in (name,'ONE_HELPER_SOURCE_THEOREM.md','ten_anchor_LOW_source_schemas.json')},'principal_U33':'OPEN'}
    with (B/('one_helper_p%d_independent_audit.json'%p)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result[k] for k in ('status','helper_physical_rank','nonzero_coefficients','all_negative_LOW_source_rows','all_positive_source_LOW_rows','working_bank_bound')}))

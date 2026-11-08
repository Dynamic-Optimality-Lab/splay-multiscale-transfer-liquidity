"""Accepted debt lower floors from frozen facts; no solver or regenerated rows."""
import json,time
from pathlib import Path
from source_model import shadow
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def decode(t):
    return (t[0],decode(t[1]),decode(t[2])) if isinstance(t,(list,tuple)) else t
def main():
    bank=json.loads((B.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((B.parent/'M3_H1F01/cheap_census.json').read_text())
    ts=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)};psi=[q['psi'] for q in bank['nodes']]
    replay=json.loads((B/'symbolic_replay.json').read_text());answers=[]
    final=json.loads((B.parent/'M3_XFER21/audit_extremal.json').read_text())
    step4=json.loads((B.parent/'M3_XFER19/STEP4_CERTIFICATE.json').read_text())
    h=json.loads((B.parent/'M3_XFER16/debt_definition.json').read_text())
    assert h['H_max']['core_right_child']==8 and h['H_min']['core_left_child']==0
    for f in replay['families']:
        r={'name':f['name'],'endpoints':{}}
        for which,ac,bc in [('source',f['critical_old_A'],f['old_chart']),('target',f['critical_end_A'],f['new_chart'])]:
            t=freeze(bc['tree']);i=ids[t];a=shadow(decode(ac),bc['Scores']);marks={bc['Scores'].index(x) for x in bc['marks']}
            visible={v['index'] for p,v in a.items() if p and v.get('isS') and v['index'] in marks}
            margins=[{'Score':x,'key':bc['Scores'][x],'q':tab['B_depth'][i][x]//2,
                'psi_after':psi[tab['B_destination'][i][x]],'margin':2-tab['B_depth'][i][x]//2+psi[tab['B_destination'][i][x]]} for x in sorted(visible)]
            c=min([2]+[q['margin'] for q in margins]);assert c>=0
            # Literal B part of BOTH tall ceiling predicates is false in these
            # endpoints; no assumption that Lambda is a universal final floor.
            Hmin_B=t[0] in (7,8) and t[1] is not None and t[1][0]==0
            Hmax_B=t[0] in (0,1) and t[2] is not None and t[2][0]==8
            assert not Hmin_B and not Hmax_B
            floor=max(psi[i],c)
            matched=[]
            if which=='target':
                positions=['','L','R','LL','LR','RL','RR']
                av={p:a[positions[p]]['index'] for p in range(7) if a[positions[p]].get('isS')}
                for origin,cert in [('Step4',step4),('Final',final)]:
                    for cid,cl in enumerate(cert['clauses']):
                        if cl['core']!=i:continue
                        if cl['kind']=='positive_anchor':
                            ok=any(r in marks and any(av.get(p)==r for p in ((1,3) if r<t[0] else (2,6))) for r in cert['anchors'][str(i)])
                        elif cl['kind']=='anchor':
                            ok=any(int(r) in marks and value>=cl['level'] and any(av.get(p)==int(r) for p in ((1,3) if int(r)<t[0] else (2,6))) for r,value in cert['anchor_coefficients'][str(i)].items())
                        else:
                            ok=all(av.get(p)==v for p,v in cl['score_equalities']) and set(cl['marks'])<=marks and not(set(cl.get('nonmarks',[]))&marks)
                        if ok:matched.append({'origin':origin,'id':cid,'level':cl['level']});floor=max(floor,cl['level'])
            # The normalized source is a Hamiltonian right vine; its second/
            # third labels are roles1/2, only role2 marked. Authorized R gives
            # role2 in Omega/Sigma, while modified Gamma has no such reading.
            if which=='source':
                hidden=not any(v.get('isS') and v['index']==2 for p,v in a.items() if p)
                dhat=0 if hidden else 1
                assert dhat==f['normalized_source_debt']
                if not hidden:assert floor>=1
                exact=dhat
            else:
                assert 0<=floor<=2
                exact=2 if floor==2 else None
            r['endpoints'][which]={'core_index_reused':i,'visible_marked_Scores':sorted(visible),'margins_reused':margins,
                'psi':psi[i],'capacity_c':c,'tall_H_ceiling_B_conditions_false':True,
                'accepted_D_lower_bound':floor,'normalized_D_exact':exact,'normalized_D_interval':[exact,exact] if exact is not None else [floor,2],'matched_accepted_clauses':matched,'known_real_alpha':a}
        r['H']=f['critical_packet']['H'];r['Q']=f['critical_packet']['Q'];r['w']=-2
        r['residual_upper']=-2+2-r['endpoints']['source']['normalized_D_exact']
        r['residual_exact']=None if r['endpoints']['target']['normalized_D_exact'] is None else -2+r['endpoints']['target']['normalized_D_exact']-r['endpoints']['source']['normalized_D_exact']
        answers.append(r)
    out('debt_v3_audit.json',{'status':'PASS_CERTIFIED_NORMALIZED_ENDPOINTS_AND_REFUTATION',
        'method':'read frozen psi/depth/destination facts; evaluate accepted capacity floor only at states whose old tall ceilings are false; no solver',
        'lineage':'D_exp>=max(psi,c); XFER16 sole ceiling false here; XFER17 marked proper root retained; XFER18/19/21 maxima',
        'source_normalization':'literal Hhidden predicate; marked role2 visible at authorized nonroot R in Omega/Sigma',
        'witnesses':answers,'old_semantic_rows_replayed':0,'new_finite_tests':0,'source_engine_calls':0,
        'whole_width2_architecture_refuted':False,'entire_Step2_proved':False})
    print(json.dumps({'status':'PASS_CERTIFIED_NORMALIZED_ENDPOINTS_AND_REFUTATION','witnesses':[{'name':r['name'],
        'source':r['endpoints']['source']['normalized_D_exact'],'target':r['endpoints']['target']['normalized_D_exact'],
        'residual':r['residual_exact'],'residual_upper':r['residual_upper']} for r in answers]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_debt_v3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'new_finite_tests':0,'source_engine_calls':0})

"""Producer extraction of NEW edge-lifetime source candidates.
Uses old per-operation trees/events; no splay engine or independent audit.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent;C15=B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def parents(t):
    ans={}
    def visit(t,p=None):
        if not isinstance(t,(list,tuple)):return
        ans[t[0]]=p;visit(t[1],t[0]);visit(t[2],t[0])
    visit(t);return ans
def creator_records(rows,M):
    records=[]
    for i,t in enumerate(rows):
        bef=parents(t['before'][0]);aft=parents(t['after'][0]);v=t['target'];events=t['A_events'];groups={}
        for x in sorted(M):
            p=aft[x]
            if x==v or p is None or p in M or p==bef[x]:continue
            operand=x if p==v else p
            jj=[j for j,e in enumerate(events,1) if operand in (e.get('G'),e.get('P'))]
            assert len(jj)==1,(t['occurrence'],p,x,operand,jj)
            groups.setdefault(jj[0],[]).append((p,x))
        for j,edges in groups.items():
            assert len(edges)<=2,(t['occurrence'],j,edges)
            for bit,edge in enumerate(sorted(edges)):
                records.append({'row_index':i,'edge':edge,'unit':(t['occurrence'],j,bit),
                    'creator_access_target':v,'creator_event':events[j-1],
                    'creator_row':t['occurrence']})
    return records
def main():
    reports=[]
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        for index,f in enumerate(read(C15/name)['reports']):
            rows=f['rows'];M={t['target'] for t in rows if t['genuine_F']}
            cc=creator_records(rows,M);by={t['occurrence']:i for i,t in enumerate(rows)}
            h=unpack(f['leaf_partial_h']);hi={u:d for d,u in h.items()}
            a=unpack(f['owners']['prior']) if f['owners'] else {};ai={u:d for d,u in a.items()}
            claims=[];uncovered=[];used=set()
            for raw in sorted(f['branch_frontier']):
                d=tuple(raw);m=next(m for m in f['macros'] if d[0] in m['occurrences'])
                if m['H']!=1:uncovered.append({'demand':d,'reason':'not_H1'});continue
                positives=[by[t] for t in m['occurrences'] if rows[by[t]]['a']]
                assert len(positives)==1
                k=positives[0];t=rows[k];x=m['target'];pp=parents(t['before'][0])[x]
                if pp is None or pp in M:uncovered.append({'demand':d,'reason':'marked_or_absent_A_parent'});continue
                edge=(pp,x);old=[z for z in cc if tuple(z['edge'])==edge and z['row_index']<k]
                c=max(old,key=lambda z:z['row_index']) if old else max((z for z in cc if tuple(z['edge'])==edge),key=lambda z:z['row_index'])
                assert tuple(c['unit']) not in used;used.add(tuple(c['unit']))
                # The chosen lifetime has no intervening access to x before the frontier.
                ci=c['row_index'];segment=rows[ci+1:k] if ci<k else rows[ci+1:]+rows[:k]
                assert not any(s['target']==x for s in segment)
                u=tuple(c['unit'])
                claims.append({'frontier':d,'frontier_positive_A_occurrence':t['occurrence'],
                    'edge':edge,'creator':c,'wraps_given_seam':ci>=k,
                    'old_comparison_preimage':hi.get(u),'old_effective_owner':ai.get(u),
                    'outside_comparison_image':u not in hi,
                    'free_under_actual_a_if_supplied':u not in ai if f['owners'] else None})
            reports.append({'source_file':name,'report':index,'r':f['r'],'mirrored':f['mirrored'],
                'claims':claims,'uncovered_source_classes':uncovered,
                'all_extracted_candidates_distinct':True,
                'all_extracted_candidates_outside_old_comparison':all(q['outside_comparison_image'] for q in claims),
                'source_complete_usable_supply_proved':False})
    out('edge_lineage_candidates.json',{'status':'PRODUCER_PROOF_DERIVATION_AUDIT_PENDING',
        'new_source_histories':0,'source_engine_calls':0,'reports':reports,
        'scope':'raw source-forced candidates; universal comparison-image disjointness and owner escape NOT assumed'})
    print(json.dumps({'status':'LINEAGE_PRODUCER_PASS','reports':len(reports),
        'summary':[{'source':r['source_file'],'r':r['r'],'mirror':r['mirrored'],
            'candidate_units':[[q['frontier'],q['creator']['unit']] for q in r['claims']],
            'comparison_collisions':sum(not q['outside_comparison_image'] for q in r['claims']),
            'uncovered':r['uncovered_source_classes']} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_lineage_exit.json',{'whole_process_CPU_seconds':time.process_time(),
        'error':error,'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})

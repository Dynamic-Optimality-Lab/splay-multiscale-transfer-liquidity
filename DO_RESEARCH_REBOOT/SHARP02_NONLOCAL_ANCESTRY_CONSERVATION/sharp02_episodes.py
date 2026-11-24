"""Complete cyclic A/B relation streams, not one credit per pair reference."""
from collections import defaultdict
from sharp02_common import *
from sharp01_oracle import Tree

def analyze(l):
    wanted=defaultdict(set);gaps=[]
    for g in l['gaps']:
        if g['u']:
            for y in g['B_only_ancestors']:wanted[y].add(g['target'])
            gaps.append({k:g[k] for k in ('gap_index','KEEP_operation_id','previous_KEEP_operation_id','target','u','B_only_ancestors')})
    statuses={}
    for g in l['gaps']:
        reserved=min(g['q'],2*g['p']);ordinal=0
        for sid in g['A_StepEv_ids']:
            for bit in range(2):
                statuses[tuple(sid+[bit])]={'gap_index':g['gap_index'],'reserved':ordinal<reserved};ordinal+=1
    streams=defaultdict(list)
    for ep,e in enumerate(l['events']):
        for key,truth in (('ancestry_removed',False),('ancestry_added',True)):
            y,xx=e[key]
            if y in wanted:
                for x in wanted[y].intersection(xx):
                    units=[]
                    if e['id'][0]=='A' and truth:
                        ids=[e['id']]
                        if e['case']=='ZIG':ids.append(e['id'][:3]+[1])
                        units=[{'id':uid,'virtual':uid!=e['id'],**statuses[tuple(uid)]} for uid in ids]
                    streams[y,x].append({'event_position':ep,'id':e['id'],'actor':e['id'][0],'truth_after':truth,
                                         'pivot':e['pivot'],'promoted':e['promoted'],'middle':e['middle'],
                                         'SET_sign':e['SET_sign'],'accounting_units_if_A_gain':units})
    a=Tree(l['source']['initial_A']);b=Tree(l['source']['initial_B']);relations=[]
    for (y,x),stream in streams.items():
        av=y in a.path(x)[:-1];bv=y in b.path(x)[:-1];initial=(av,bv)
        A_gain=[];A_loss=[];B_gain=[];B_loss=[];birth=[];death=[]
        for e in stream:
            e['A_before']=av;e['B_before']=bv;was=bv and not av
            if e['actor']=='A':
                assert av!=e['truth_after'];av=e['truth_after'];(A_gain if av else A_loss).append(e)
            else:
                assert bv!=e['truth_after'];bv=e['truth_after'];(B_gain if bv else B_loss).append(e)
            e['A_after']=av;e['B_after']=bv
            now=bv and not av
            if now and not was:birth.append(e)
            if was and not now:death.append(e)
        assert (av,bv)==initial and len(A_gain)==len(A_loss) and len(B_gain)==len(B_loss)
        references=[]
        for g in gaps:
            if g['target']!=x or y not in g['B_only_ancestors']:continue
            begin=l['operations'][g['previous_KEEP_operation_id']-1]['event_range'][1]
            end=l['operations'][g['KEEP_operation_id']-1]['event_range'][1]
            def prev(rows,pos):return next((e for e in reversed(rows) if e['event_position']<pos),rows[-1] if rows else None)
            def nxt(rows,pos):return next((e for e in rows if e['event_position']>=pos),rows[0] if rows else None)
            loss=prev(A_loss,begin);gain=nxt(A_gain,end);episode_end=nxt(A_gain,begin);org=prev(birth,begin)
            references.append({'gap_index':g['gap_index'],'last_A_loss':None if loss is None else loss['id'],
                'first_A_recreation_after_KEEP':None if gain is None else gain['id'],
                'first_A_recreation_after_gap_start':None if episode_end is None else episode_end['id'],
                'absence_episode_wraps_display_seam':loss is not None and episode_end is not None and episode_end['event_position']<loss['event_position'],
                'discrepancy_origin':None if org is None else org['id'],
                'B_relation_loss_in_consuming_KEEP':[e['id'] for e in B_loss if e['id'][1]==g['KEEP_operation_id']]})
        relations.append({'ancestor':y,'descendant':x,'initial_A_relation':initial[0],'initial_B_relation':initial[1],
                          'changes':stream,'positive_gap_references':references,
                          'A_absence_episodes':[{'loss':loss['id'],'next_gain':nxt(A_gain,loss['event_position']+1)['id'],
                            'wraps_seam':nxt(A_gain,loss['event_position']+1)['event_position']<loss['event_position']} for loss in A_loss]})
    return {'source':l['source']['name'],'relations':relations,'positive_gaps':gaps,
            'initial_A':l['source']['initial_A'],'initial_B':l['source']['initial_B'],
            'cycle_identity':'A gains=A losses and B gains=B losses for each pair; not a capacity inequality'}

if __name__=='__main__':
    import sys
    with Run(sys.argv[1] if len(sys.argv)>1 else 'complete_ancestry_episodes_v001',limit=60) as run:
        idx=read(OLD/'SHARP01_GAP_LEDGER.json')['ledgers'];out=[]
        for k,it in enumerate(idx):
            out.append(analyze(read(OLD/it['path'])))
            if k%15==0:run.check(source_count=len(out))
        for filename in ('SHARP02_RAW_WITNESS_LEDGER.json','SHARP02_MINIMAL_SOURCE_LEDGER.json'):
            out.append(analyze(read(BASE/filename)))
        write(BASE/'SHARP02_ANCESTRY_EPISODES.json',{'sources':out,'scope':'all 79 inherited sources plus raw and minimized principal counterexamples',
              'capacity_warning':'several relation records can refer to one rotation; an A StepEv still has only two accounting units'})
        run.check(source_count=len(out));print(json.dumps({'sources':len(out),'relation_streams':sum(len(s['relations']) for s in out)}))

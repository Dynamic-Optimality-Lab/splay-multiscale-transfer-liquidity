"""Capacity-unit congestion check on SAVED ledgers; no source replay.

Reserve the first min(q,2p) of the gap's chronological two-per-StepEv units.
Every remaining unit is named, including a zig's virtual companion. This is
a falsifiable bookkeeping choice, never a modification of historical owners.
"""
from sharp01_experiments import *

start=time.process_time();wall=time.perf_counter();output=[]
idx=json.loads((BASE/'SHARP01_GAP_LEDGER.json').read_text())['ledgers']
for item in idx:
    l=json.loads((BASE/item['path']).read_text());gs=l['gaps'];ev={tuple(e['id']):e for e in l['events']}
    pos={tuple(e['id']):k for k,e in enumerate(l['events'])}
    bystep=defaultdict(list)
    for e in l['events']:bystep[tuple(e['id'][:3])].append(e)
    units={};uid=0
    for g in gs:
        budget=min(g['q'],2*g['p']);allunits=[]
        for sid in g['A_StepEv_ids']:
            ee=bystep[tuple(sid)]
            for bit in range(2):
                chosen=ee[min(bit,len(ee)-1)]
                allunits.append({'id':sid+[bit],'gap_index':g['gap_index'],
                                 'rotation_witness':chosen['id'],'virtual':bit==1 and len(ee)==1})
        for u in allunits[budget:]:units[uid]=u;uid+=1
        assert len(allunits)-budget==g['c']
    demands={g['gap_index']:g['u'] for g in gs if g['u']}
    donorcap={k:1 for k in units};graphs={k:{} for k in ('unit_A_recreation','unit_first_A_recreation')}
    reasons={k:[] for k in graphs}
    for g in gs:
        if not g['u']:continue
        gi=g['gap_index'];x=g['target'];ys=set(g['B_only_ancestors'])
        end=l['operations'][g['KEEP_operation_id']-1]['event_range'][1]
        first={}
        for y in ys:
            matches=[k for k,e in enumerate(l['events']) if e['id'][0]=='A' and e['ancestry_added'][0]==y and x in e['ancestry_added'][1]]
            if matches:first[y]=next((k for k in matches if k>=end),matches[0])
        for rule in graphs:graphs[rule][gi]=[]
        for k,u in units.items():
            e=ev[tuple(u['rotation_witness'])];y,xx=e['ancestry_added']
            if y in ys and x in xx:
                graphs['unit_A_recreation'][gi].append(k)
                reasons['unit_A_recreation'].append([gi,k,y,e['id']])
                if pos[tuple(e['id'])]==first[y]:
                    graphs['unit_first_A_recreation'][gi].append(k)
                    reasons['unit_first_A_recreation'].append([gi,k,y,e['id']])
    rules={}
    for rule,adj in graphs.items():
        total,ds,assignment=flow(demands,donorcap,adj)
        if ds:
            for i in list(ds):
                trial=[j for j in ds if j!=i]
                if deficiency(trial,demands,donorcap,adj)>0:ds=trial
        used=Counter(j for i,j,amt in assignment for _ in range(amt))
        assert max([0]+list(used.values()))<=1
        assert all(j in adj[i] for i,j,amt in assignment)
        rules[rule]={'demand':sum(demands.values()),'flow':total,'success':total==sum(demands.values()),
                     'deficient_subset':ds,'Hall_deficiency':deficiency(ds,demands,donorcap,adj) if ds else 0,
                     'subset_minimality':'inclusion-minimal; no minimum-cardinality claim',
                     'edges':adj,'edge_reasons':reasons[rule],'assignment':assignment,
                     'max_eligible_demands_per_unit':max([0]+[sum(j in near for near in adj.values()) for j in units])}
    output.append({'source':item['name'],'units':units if demands else {},'rules':rules})
    assert time.process_time()-start<60,'unit-incidence CPU reserve'
write(BASE/'SHARP01_PHYSICAL_INCIDENCE.json',{'capacity_reservation':'first min(q,2p) chronological A units are reserved; rest equal c exactly',
                                           'owner_policy':'new exploratory units only; no historical owners imported or changed','sources':output,
                                           'cpu_seconds':time.process_time()-start,'wall_seconds':time.perf_counter()-wall})
for rule in graphs:
    fails=[(s['source'],s['rules'][rule]['demand'],s['rules'][rule]['flow'],s['rules'][rule]['deficient_subset'],s['rules'][rule]['Hall_deficiency']) for s in output if not s['rules'][rule]['success']]
    print(rule,'failures',len(fails),'first',fails[:5])
print('CPU',time.process_time()-start)

from exp04_core import *


def edge_audit(r,events):
    a=Tree(r.source['initial_A']);b=Tree(r.source['initial_B']);values=[len(b.edges()-a.edges())];all_doubles={};zero_negative=[]
    byparent={tuple(e['original_parent']) for e in events};records={};max_A=0;B_increases=[]
    for e in r.events:
        parent=tuple(e['id'][1:3]);before=len(b.edges()-a.edges())
        if e['actor']=='B' and parent in byparent and e['id'][3]==0:
            records[parent]={'original_parent':list(parent),'start':before,'bits':[]}
        if e['actor']=='B' and e['case']!='ZIG' and e['id'][3]==0:all_doubles[parent]={'start':before,'signs':[],'bits':[]}
        tree=a if e['actor']=='A' else b;tree.rotate(e['pivot'],e['side']);after=len(b.edges()-a.edges());values.append(after)
        if e['actor']=='A':max_A=max(max_A,abs(after-before));assert abs(after-before)<=3
        else:
            if after>before:B_increases.append({'bit':e['id'],'before':before,'after':after})
            if parent in records:records[parent]['bits'].append({'id':e['id'],'delta':after-before});records[parent]['end']=after
            if parent in all_doubles:
                all_doubles[parent]['signs'].append(e['sign']);all_doubles[parent]['end']=after
                all_doubles[parent]['bits'].append(e['id'])
            if after<before and e['sign']==0:zero_negative.append({'bit':e['id'],'edge_delta':after-before})
    assert values[-1]==values[0]
    return {'source':r.source['name'],'A_primitive_max_absolute_delta':max_A,'original_demand_parents':list(records.values()),
        'B_increases':B_increases,'cycle_telescope':values[-1]-values[0],'neutral_negative_edge_bits':zero_negative,
        'neutral_double_deltas':[{'parent':list(k),'delta':v['end']-v['start'],'in_U':k in r.U} for k,v in all_doubles.items() if v['signs']==[0,0]],
        'full_KEEP_changes':[{'t':row['t'],'delta':len(Tree(row['post_B']).edges()-Tree(row['post_A']).edges())-len(Tree(row['pre_B']).edges()-Tree(row['post_A']).edges())} for row in r.boundaries if row['tag']=='K']}


if __name__=='__main__':
    meter=Meter('EXP04_boundary')
    archive=json.loads((PREV/'EXP03_SOURCE_WITNESSES.json').read_text())
    data=json.loads((PREV/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    by={s['source']:s for s in data['inherited_sources']+data['new_sources']}
    names=['IH_p4_q1_L2_z5_c1','Xprobe_p4_L3_hitNone_boundary1','mixed_p5_Gcopies2']
    results=[]
    for s in archive['inherited_sources']+archive['new_sources']:
        if s['name'] not in names:continue
        r=Replay(s);z=edge_audit(r,by[s['name']]['remaining_after_restart']);results.append(z)
        print(s['name'],'parents',z['original_demand_parents'],'B+bits',len(z['B_increases']),flush=True)
    write('EXP04_EDGE_BOUNDARY_EXPERIMENTS.json',results);meter.success=True

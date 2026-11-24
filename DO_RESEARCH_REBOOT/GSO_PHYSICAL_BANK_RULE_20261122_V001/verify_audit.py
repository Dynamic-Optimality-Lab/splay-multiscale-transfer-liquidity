"""Independent bank descent on upstream independently verified physical traces."""
import sys
import json
sys.dont_write_bytecode=True
import verify as V


def main():
    upstream=V.HERE.parent/'GSO_TRACE_ENGINE_20261122_V001';checked=[]
    for i in range(18):
        z=V.read(upstream/f'run_001/trace_{i:02d}.json.gz');owner={x:j for j,p in enumerate(z['blocks']) for x in p};ev=[]
        for op in z['operations']:
            if op['k']:ev.append({'id':['K',op['id']],'a':0,'q':0,'k':1,'target':op['target'],'scope':[owner[op['target']]],'priority':[owner[op['target']]]})
            for s in z['steps'][op['steps'][0]:op['steps'][1]]:
                target=owner[s['target']];ev.append({k:s[k] for k in ('id','a','q','k','target','scope')}|{'priority':[target]+[j for j in sorted(s['scope']) if j!=target]})
        for H in (1,2,5,8,16):
            r=V.read(V.HERE/f'audit_001/source_{i:02d}_H{H}.json.gz');state=[H]*len(z['blocks']);passes=[]
            for lap in range(len(state)*H+1):
                nxt=state.copy();paid=0
                for e in ev:paid+=V.independent_update(nxt,e,H)['paid']
                assert all(a<=b for a,b in zip(nxt,state));passes.append({'pass':lap,'mass_before':sum(state),'mass_after':sum(nxt),'unpaid':z['Q_B']-paid})
                if nxt==state:break
                state=nxt
            assert state==r['initial_greatest_fixed_point'] and passes==r['period_passes']
            now=state.copy();paid=issued=0;fails=[]
            for j,e in enumerate(ev):
                row=V.independent_update(now,e,H);paid+=row['paid'];issued+=row['issued']
                if row['unpaid']:fails.append({'event':j,'id':e['id'],'target':e['target'],'scope':e['scope'],'priority':e['priority'],'before':row['before'],'q':e['q'],'unpaid':row['unpaid']})
            assert now==state and paid==issued==r['paid']==r['issued'] and fails==r['failures']
            checked.append({'source':i,'H':H,'paid':paid,'unpaid':len(fails)})
    out={'passed':True,'physical_sources':18,'capacity_tests':len(checked),'cases':checked,'scope':'Independent bank checker on sealed full original event traces; the upstream full Pi/physical verification is reused unchanged. New reported counterexamples have a separate full immutable source/Pi replay.','root_status':'OPEN'}
    if not (V.HERE/'FINAL_MANIFEST.json').exists():(V.HERE/'AUDIT_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print({'passed':True,'upstream_original_sources':18,'capacity_tests':len(checked)})


if __name__=='__main__':main()

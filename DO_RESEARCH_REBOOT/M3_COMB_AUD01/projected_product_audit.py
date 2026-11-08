"""Fresh actual frozen Product/projections; independent lexical scope traversal."""
import sys,json,time
from pathlib import Path
PFX='DO_RESEARCH_REBOOT/06_CERTIFICATES/'
sys.path[:0]=[PFX+'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',PFX+'DIRECT_CDK5N_11F_STRICT_CLOSURE',
             PFX+'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE',PFX+'DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS']
from PC_TYPED_DAG import DAG
from CW_PRODUCT_COMPILER import Product
from S03_EDGE_PROJECTIONS import build_projections
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01')

def lexical_free(d,root):
    contexts=[frozenset()];ids={contexts[0]:0};todo=[(root,0)];seen=set();free=set()
    while todo:
        node,ctx=todo.pop()
        if (node,ctx) in seen:continue
        seen.add((node,ctx));kind,typ,args,extra=d.nodes[node]
        if kind=='var':
            if extra[1] not in contexts[ctx]:free.add(extra[1])
        elif kind=='exists':
            combined=contexts[ctx]|frozenset(extra)
            if combined not in ids:ids[combined]=len(contexts);contexts.append(combined)
            todo.extend((a,ids[combined]) for a in args)
        else:todo.extend((a,ctx) for a in args)
    return free

def main():
    output=BASE/'actual_projected_product_audit.json';assert not output.exists();start=time.process_time()
    d=DAG();p=Product(d);assert len(d.nodes)<4000000;edges,_=build_projections(p);assert len(d.nodes)<4000000
    records=[]
    for (s,t,w),edge in edges.items():
        free=lexical_free(d,edge)
        if (s,t)==(0,0):ok=all(n.startswith('QO') for n in free)
        elif (s,t)==(0,1):ok=all((n.startswith('QO') and not n.startswith('QO2')) or n.startswith('QM') for n in free)
        elif (s,t)==(1,0):ok=all(n.startswith('QM') or n.startswith('QO2') for n in free)
        else:ok=not free
        assert ok,(s,t,w,free)
        records.append({'sort_source':s,'sort_destination':t,'weight':w,'lexical_free_count':len(free),'no_private_witness_free':True})
        assert time.process_time()-start<120,'UNKNOWN projected Product audit cap'
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_GAP01/original_audit.json').read_text())
    low=old['records'][0];e={}
    for k,v in low['environment'].items():
        name='CL'+k[3:] if k.startswith('MXL') else k
        if name.startswith('CLs'):name='QO'+name[3:]
        elif name.startswith('CLt'):name='QO2'+name[3:]
        e[name]=v
    assert d.ev_ground(edges[(0,0,low['w'])],e)
    high=json.loads(Path('DO_RESEARCH_REBOOT/M3_OUT01/high_controls.json').read_text())
    r=next(r for r in high['records'] if r['high_root'] and r['w']==-3 and not any(r['sigma']))
    e={}
    for k,v in r['environment'].items():
        name='CH'+k[4:] if k.startswith('DSKF') else k
        if name.startswith('CHs'):name='QO'+name[3:]
        elif name.startswith('CHt'):name='QO2'+name[3:]
        elif name.startswith('CHg'):name='QM'+name[3:]
        e[name]=v
    assert d.ev_ground(edges[(0,1,-3)],e) and d.ev_ground(edges[(1,0,0)],e)
    result={'status':'PASS_ACTUAL_FROZEN_PRODUCT_AND_PROJECTIONS','Product_DAG_nodes':len(d.nodes),
            'projected_sort_weight_cases':records,'actual_projected_membership_checks':3,
            'negative_h0_OM_and_zero_MO_share_original_midpoint':True,
            'independent_lexical_bound_variable_traversal':True,'old_scope_checker_used_for_verdict':False,
            'cpu_seconds':round(time.process_time()-start,3)}
    assert result['cpu_seconds']<120
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='projected_sort_weight_cases'},indent=2))

if __name__=='__main__':main()

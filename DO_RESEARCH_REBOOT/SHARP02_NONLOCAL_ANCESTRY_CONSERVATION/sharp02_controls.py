"""Exact C15 first-return controls, token witnesses, cyclic/copy/hanger tests."""
from sharp02_common import *
from sharp02_graph import graph_data,solve
from sharp01_oracle import replay
from sharp01_validate import validate
from sharp01_sources import reflect
from sharp02_independent import verify
from sharp02_search import zero_run

def run(label='controls_and_parametric_validation_v001'):
    with Run(label,limit=120) as run:
        idx=read(OLD/'SHARP01_GAP_LEDGER.json')['ledgers'];old=read(OLD/'SHARP01_SOURCE_WITNESSES.json')['sources']
        c15=[];extra_sources=[];ledgers=[]
        for kind in ('owner','zero'):
            for r in (7,8):
                name=f'C15_{kind}_r{r}_mirrorFalse';item=next(i for i in idx if i['name']==name)
                l=read(OLD/item['path']);v=verify(l);data=graph_data(l);events=l['events'];pos={tuple(e['id']):k for k,e in enumerate(events)}
                (BASE/'controls').mkdir(exist_ok=True)
                write(BASE/'controls'/f'{name}_ledger.json',l)
                write(BASE/'controls'/f'{name}_independent_geometry.json',v)
                firstadj={};detail=[]
                for g in l['gaps']:
                    if not g['u']:continue
                    x=g['target'];end=l['operations'][g['KEEP_operation_id']-1]['event_range'][1];first={};rr=[]
                    for y in g['B_only_ancestors']:
                        creations=[k for k,e in enumerate(events) if e['id'][0]=='A' and e['ancestry_added'][0]==y and x in e['ancestry_added'][1]]
                        if creations:first[y]=next((k for k in creations if k>=end),creations[0])
                        rr.append({'ancestor':y,'all_A_recreations':[events[k]['id'] for k in creations],
                                   'first_after_demand':None if y not in first else events[first[y]]['id']})
                    eligible={j for j,u in data['free'].items() if u['created_ancestor'] in first and pos[tuple(u['rotation_witness'])]==first[u['created_ancestor']]}
                    firstadj[str(g['gap_index'])]=eligible
                    detail.append({'gap':g,'recreations':rr,'first_eligible_remaining_units':[data['free'][j] for j in sorted(eligible)],
                                   'all_recreation_remaining_units':[data['free'][j] for j in sorted(data['adj'][str(g['gap_index'])])]})
                ff=solve(data['weights'],firstadj,data['free']);aa=solve(data['weights'],data['adj'],data['free'])
                assert ff['unmatched']==r-6 and aa['unmatched']==0
                if kind=='owner' and r==7:
                    assert {tuple(u['id']) for u in detail[0]['first_eligible_remaining_units']}=={('A',18,2,0),('A',18,2,1),('A',21,1,1)}
                c15.append({'source':l['source'],'summary':l['summary'],'first':ff,'all':aa,'detailed_gaps':detail,
                            'all_named_units':data['units'],
                            'complete_ledger':f'controls/{name}_ledger.json','independent_geometry':f'controls/{name}_independent_geometry.json',
                            'independent_primitive_rotations':v['primitive_rotations_checked']})
        # Arbitrarily long known zero-run family: explicit parameterized formula,
        # finite instantiations are independently checked, not called a proof.
        for r in (10,12,16,24,32):
            s=zero_run(r);l=replay(s,features=False);validate(s,l);data=graph_data(l)
            rr=solve(data['weights'],data['adj'],data['free'])
            extra_sources.append(s);c15.append({'source':s,'summary':l['summary'],'all':rr,'parameter_r':r})
        # Export representative source-valid tokenization failures from Stage 0.
        reconstruction=read(BASE/'SHARP02_RECONSTRUCTION.json')['sources'];token=[]
        for mode in ('outermost','innermost','extra_double'):
            candidates=[z for z in reconstruction if z['token_models'][mode]['unmatched']]
            selected=min(candidates,key=lambda z:(z['summary']['n'],z['summary']['operations']))
            l=read(OLD/next(i['path'] for i in idx if i['name']==selected['name']));d=graph_data(l);ww,aa=d['token_models'][mode]
            res=solve(ww,aa,d['free'])
            token.append({'source':l['source'],'mode':mode,'result':res,'tokens':d['tokens'],
                          'eligible_units':{i:[d['free'][j] for j in sorted(aa[i])] for i in res['deficient_subset']}})
        main=read(BASE/'SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json')['source'];mainname=main['name']
        variants=[]
        for repeats,hangers in [(r,0) for r in (1,2,3,7)]+[(r,h) for h in (1,7,31,257) for r in (1,3)]:
            st=json.loads(json.dumps(main['initial_A']))
            if hangers:
                st['children']['10'][1]=11
                for key in range(11,11+hangers):st['children'][str(key)]=[None,key+1 if key<10+hangers else None]
            s={'name':f'S02_family_r{repeats}_h{hangers}','family':'SHARP02_rigid_hanger_copy_family',
               'initial_A':st,'initial_B':st,'diagonal_initial':st,'reaching_prefix':[],
               'operations':main['operations']*repeats,'repeat_parameter':repeats,'hanger_parameter':hangers}
            l=replay(s,features=False);validate(s,l);d=graph_data(l);rr=solve(d['weights'],d['adj'],d['free']);oo=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
            assert all(l['summary'][k]==repeats*v for k,v in {'A':35,'Q':24,'U':1,'C':47,'Delta':-46}.items())
            assert rr['unmatched']==repeats and not oo['unmatched']
            variants.append({'source':s,'summary':l['summary'],'broad':rr,'optimized':oo});extra_sources.append(s)
        for parent in (variants[0]['source'],next(v['source'] for v in variants if v['source']['name']=='S02_family_r3_h31')):
            s=reflect(parent);l=replay(s,features=False);validate(s,l);d=graph_data(l);rr=solve(d['weights'],d['adj'],d['free']);oo=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
            assert rr['unmatched']==parent['repeat_parameter'] and not oo['unmatched']
            variants.append({'source':s,'summary':l['summary'],'broad':rr,'optimized':oo});extra_sources.append(s)
        # Every possible operation seam of the 17-operation principal source.
        mainled=read(BASE/'SHARP02_MINIMAL_SOURCE_LEDGER.json');seams=[]
        for cut in range(1,17):
            st=mainled['operations'][cut-1]['post'];s={'name':f'S02_cut_after_{cut}','family':'SHARP02_cyclic_shift',
                'initial_A':mainled['states'][st[0]],'initial_B':mainled['states'][st[1]],
                'diagonal_initial':main['initial_A'],'reaching_prefix':main['operations'][:cut],
                'operations':main['operations'][cut:]+main['operations'][:cut],
                'original_operation_ids':list(range(cut+1,18))+list(range(1,cut+1))}
            l=replay(s,features=False);validate(s,l);d=graph_data(l);rr=solve(d['weights'],d['adj'],d['free']);oo=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
            assert rr['unmatched']==1 and not oo['unmatched'] and l['summary']['A']==35 and l['summary']['Q']==24
            seams.append({'source':s,'broad':rr,'optimized':oo});extra_sources.append(s)
        write(BASE/'SHARP02_CONTROL_CERTIFICATES.json',{'C15':c15,'token_counterexamples':token,'family_variants':variants,'all_nontrivial_seams':seams})
        write(BASE/'SHARP02_EXTRA_CONTROL_SOURCES.json',extra_sources)
        run.check(C15_controls=len(c15),parametric_variants=len(variants),cyclic_seams=len(seams)+1)
        print(json.dumps({'C15_controls':len(c15),'family_variants':len(variants),'cyclic_cuts_including_original':len(seams)+1,
                          'token_counterexamples':[(z['source']['name'],z['mode'],z['result']['unmatched']) for z in token]}))

if __name__=='__main__':
    import sys
    run(sys.argv[1] if len(sys.argv)>1 else 'controls_and_parametric_validation_v001')

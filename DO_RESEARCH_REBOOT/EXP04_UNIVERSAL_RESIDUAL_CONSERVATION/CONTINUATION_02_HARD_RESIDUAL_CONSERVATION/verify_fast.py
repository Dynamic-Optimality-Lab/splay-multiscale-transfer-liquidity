from fast_physics import *


if __name__=='__main__':
    meter=Meter('independent_fast_screen_verification');out=[]
    own=json.loads((C1/'OWNERSHIP_RESULTS.json').read_text())[0]
    cases=[own['trace_file'],json.loads((C1/'INTRINSIC5_RESULTS.json').read_text())['trace_file']]
    for file in cases:
        tr=json.loads((C1/file).read_text());s=tr['source'];f=physical_replay(s,collect_A=True)
        if 'states' in tr:
            states=tr['states'];code={h:FullTree(st).code for h,st in states.items()}
            for row,old in zip(f['rows'],tr['boundaries']):
                assert row['A_code']==code[old['post_A_state_sha256']]
                assert row['B_code']==code[old['post_B_state_sha256']]
        else:
            for row,old in zip(f['rows'],tr['boundaries']):
                assert row['A_code']==FullTree(old['post_A']).code
                assert row['B_code']==FullTree(old['post_B']).code
        groups=defaultdict(list)
        for e in tr['events']:
            if e['actor']=='B':groups[(e['id'][1],e['id'][2])].append(e)
        extrema=1|(1<<(len(s['initial_B']['children'])-1))
        for row,old in zip(f['rows'],tr['boundaries']):
            assert row['a']==old['a'] and row['q']==old['q']
            expected=[];G=False
            for (t,j),es in groups.items():
                if t!=row['t']:continue
                case=es[0]['case'];p=es[0]['pivot'] if case in ('ZIG','LR','RL') else es[1]['pivot']
                g=None if case=='ZIG' else es[0]['pivot'] if case in ('LL','RR') else es[1]['pivot']
                signs=tuple(e['sign'] for e in es);expected.append((case,p,g,signs))
                G|=case!='ZIG' and signs==(0,0) and not (es[0]['frame']&extrema)
            assert expected==row['B_steps'] and G==row['guard_G']
        if s['name']==own['source']:
            norm=json.loads((C1/'GUARDED_RETURN_RESULTS.json').read_text())[0]['normalized_full_period']
        else:norm=json.loads((C1/'INTRINSIC5_RESULTS.json').read_text())['normalized']
        result=skeleton_cost(f,variant='G')
        assert result['retained_original_operations']==norm['retained_KEEP']
        assert result['J_size']==len(norm['J'])
        out.append({'source':s['name'],'operations':len(f['rows']),'A':f['A'],'Q_B':f['Q_B'],
                    'exact_full_A_and_B_boundary_states_match':True,'all_B_step_cases_grandparents_and_signs_match':True,
                    'G_normalization_matches_pinned_implementation':True})
        print('PASS',s['name'],len(f['rows']),flush=True)
    write('FAST_SCREEN_VERIFICATION.json',out);meter.success=True

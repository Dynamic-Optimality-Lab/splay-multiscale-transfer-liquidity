"""Producer check of the source-derived cross-block leaf-channel permutation.
Stored source rows are reindexed; no rotations or independent audit run.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def shift(z,n):return (z[0]+n,*z[1:])
def main():
    sp=importlib.util.spec_from_file_location('C19_seam_channels',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
    L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L)
    family=read(B/'closed_block_family.json');block={z['label']:z for z in family['blocks']}
    stored={'A80':read(OLD/'rr7_source_candidate.json')['rows'],'B82':read(OLD/'overfull_source_result.json')['rows']}
    M=set(family['source_support']);facts=[]
    for name,rows in stored.items():
        v=L.build(rows,M);first=v['macros'][0]
        assert len(first['branch'])==first['z']==0
        H={tuple(z['demand']):tuple(z['unit']) for z in block[name]['physical_comparison']}
        assert all(H[d]==u for d,u in v['h'].items())
        facts.append({'block':name,'first_genuine_macro_beta':0,'first_genuine_macro_z':0,
          'wrapped_channels':[c for c in v['channels'] if c['wraps_given_seam']],
          'all_leaf_channel_units':[c['unit'] for c in v['channels']],
          'base_complete_map_extends_own_leaf_branch_comparison':True})
    words=[['A80','B82'],['B82','A80'],['A80','B82','B82','A80'],['B82']*3]
    reports=[]
    for letters in words:
        rows=[];H={};offset=0
        for name in letters:
            for t in stored[name]:rows.append(dict(t,occurrence=t['occurrence']+offset))
            H.update({shift(tuple(z['demand']),offset):shift(tuple(z['unit']),offset) for z in block[name]['physical_comparison']})
            offset+=block[name]['length']
        v=L.build(rows,M);fixed=dict(H);changes=[]
        for c in v['channels']:
            d=tuple(c['demand']);u=tuple(c['unit'])
            if fixed[d]!=u:changes.append({'demand':d,'block_local_unit':fixed[d],'global_actual_predecessor_unit':u,'key':c['marked_key']})
            fixed[d]=u
        assert set(fixed)==v['D'] and len(set(fixed.values()))==len(fixed)
        assert set(fixed.values())==set(H.values()) and all(fixed[d]==u for d,u in v['h'].items())
        reports.append({'letters':letters,'length':offset,'QF':len(fixed),'seam_channel_changes':changes,
          'global_comparison':pack(fixed),'extends_global_h_Lambda':True,'physical_image_unchanged':True})
    out('seam_permutation_certificate.json',{'status':'PARAMETERIZED_SOURCE_DERIVATION_PRODUCER_CONTROLS_AUDIT_PENDING',
      'base_facts':facts,'finite_formula_controls':reports,
      'general_rule':'Permute ONLY unary leaf-channel donor values to the global same-key immediately preceding actual death. Every reserved death bit appears once both before and after; all branch and repaired frontier entries stay fixed.',
      'uniform_proof':'MULTIBUNDLE_REPAYMENT.md','Bank25_physical_schedule':'NOT_PROVED',
      'source_engine_calls':0,'new_original_rotations_replayed':0})
    print(json.dumps({'status':'ACTUAL_GLOBAL_SEAM_PERMUTATION_PASS','controls':len(reports),
      'changed_channels':[len(z['seam_channel_changes']) for z in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seam_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})

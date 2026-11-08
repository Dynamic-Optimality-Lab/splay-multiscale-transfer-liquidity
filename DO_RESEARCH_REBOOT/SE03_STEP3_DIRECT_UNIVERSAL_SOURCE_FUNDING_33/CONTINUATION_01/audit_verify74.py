"""Direct owner-course audit: actual H2 provenance, all-stage natural ownership.
Reuses accepted A/B9/B10 and source proofs; new mutable replay is B6/B7/B8.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
from interior_projection_source_tools import fr,isnode,known
B=Path(__file__).resolve().parent;P=B.parent.parent;C=B/'DIRTY_OWNER_COURSE_CORRECTION';START=time.process_time();CAP=float(sys.argv[1]);queries=0
def out(n,z):
    with (C/n).open('x') as f:json.dump(z,f,indent=2)
def mp(v):return {tuple(q['demand']):tuple(q['unit']) for q in v}
def main():
    global queries
    z=json.loads((C/'H2_actual_owner_candidate.json').read_text());old=json.loads((B/'retirement_preimage_closed_source.json').read_text());pin=json.loads((B/'retirement_boundary_independent_audit.json').read_text());assert pin['status']=='PASS_UNIFORM_H1_RETIREMENT_AND_SOURCE_EXACT_H2_NONSIMULATION' and hashlib.sha256((B/'retirement_preimage_closed_source.json').read_bytes()).hexdigest()==pin['input_sha256']['retirement_preimage_closed_source.json'];assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in z['input_sha256'].items())
    assert z['normalization_complete'] and z['joint_period']==old['period']==[102,202] and z['joint_source_prefix_copies']==z['joint_period_copies']==1
    native=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,native['trees']));rows=z['all_source_rows'];initial=fr(old['initial_common_A_B_BE']);physical=sorted(known(initial));rank={k:i+1 for i,k in enumerate(physical)}
    def norm(t):
        def walk(v,hi):return 'F'+str(hi) if not isnode(v) else (v[0],walk(v[1],rank[v[0]]-1),walk(v[2],hi))
        return walk(t,len(physical))
    def embed(b):
        def walk(v):return (5,'E','E') if v=='F2' else v if not isnode(v) else (2*v[0],walk(v[1]),walk(v[2]))
        return norm(walk(T[b]))
    oldrows={r['absolute_t']:r for r in old['period_rows']}
    for row in rows:
        r=oldrows[row['occurrence']];aa=old['A_word_source_rows'][row['word_index']]
        assert (row['original_kind'],row['target'],row['a'])==(r['kind'],r['key'],r['H']) and row['A_before']==aa['before'] and row['A_after']==aa['after']
        for k,pre,post,q,cs,ct in ((10,'BF_before','BF_after','QF','chartF_before','chartF_after'),(9,'BE_before','BE_after','QE','chartE_before','chartE_after')):
            v=row['views'][str(k)];assert (v['B_before'],v['B_after'],v['Q'],v['chart_before'],v['chart_after'])==(r[pre],r[post],r[q],r[cs],r[ct])
    sp=importlib.util.spec_from_file_location('independent_H2_owner74',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=int(sys.argv[2]) or time.process_time()-START>CAP-2:raise TimeoutError('DIRECT_OWNER_AUDIT_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,rank[v.key]-1),walk(v.right,hi))
        return walk(tree.root,len(physical))
    bytime={r['occurrence']:r for r in rows};new_streams={}
    for k in (6,7,8):
        tree=I.Tree(initial);chart=();start=None;marks=set();begin=None
        for copy in range(2):
            for j,(kind,key) in enumerate(old['word']):
                t=copy*len(old['word'])+j+1;before=shape(tree);ch0=chart;q=0;genuine=False
                if t==102:start=(before,chart);begin=before
                if kind=='K' and key//2<=k:
                    genuine=key!=before[0];path,events=tree.access(key);q=len(path)//2
                    if genuine:chart=(key//2,)+tuple(v for v in chart if v!=key//2)
                after=shape(tree)
                if t in bytime:
                    v=bytime[t]['views'][str(k)];assert before==embed(v['B_before']) and after==embed(v['B_after']) and (q,genuine,chart,ch0)==(v['Q'],v['genuine'],tuple(v['chart_after']),tuple(v['chart_before']))
                    if genuine:marks.add(key)
        assert start==(shape(tree),chart) and marks==set(range(2,2*k+1,2));new_streams[k]={'genuine_marks':sorted(marks),'closed':True}
        if k==6:
            core=set()
            for key in marks:
                v=begin
                while v[0]!=key:core.add(v[0]);v=v[1 if key<v[0] else 2]
                core.add(key)
            assert core==marks and z['base6']['core']==6
    allU={(r['occurrence'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)};h0s={};domains={}
    for k in range(6,11):
        ends=[i for i,r in enumerate(rows) if r['views'][str(k)]['genuine']];h0={};D=set()
        for e,end in enumerate(ends):
            pre=ends[e-1];ii=list(range(pre+1,end+1)) if pre<end else list(range(pre+1,len(rows)))+list(range(end+1));uu=[(rows[i]['occurrence'],j,b) for i in ii for j in range(1,rows[i]['a']+1) for b in (0,1)];dd=[(rows[i]['occurrence'],j) for i in ii for j in range(1,rows[i]['views'][str(k)]['Q']+1)]
            assert len(dd)<=len(uu);h0.update(zip(dd,uu));D.update(dd)
        assert set(h0)==D and len(set(h0.values()))==len(D) and set(h0.values())<=allU;h0s[k]=h0;domains[k]=D
        expected=z['solvency_by_support'][str(k)];assert expected['D']==expected['h0_pairs']==len(D) and not expected['natural_excess']
    f=mp(z['base6']['f']);assert f==h0s[6] and len(f)==10
    stages=[]
    for k,stage in zip(range(7,11),z['stages']):
        assert mp(stage['smaller_input'])==f;D=domains[k];locked={d:f[d] for d in D&domains[k-1]};assert locked==mp(stage['common_locked']);inverse={u:d for d,u in locked.items()};natural=h0s[k];memo={}
        def endpoint(d,trail):
            if d in trail:raise AssertionError('ENTERED_OWNER_CYCLE')
            u=natural[d]
            if u not in inverse:return u
            return endpoint(inverse[u],trail|{d})
        answer=dict(locked)
        for d in D-set(locked):answer[d]=endpoint(d,set())
        assert len(set(answer.values()))==len(D) and set(answer.values())<=allU and answer==mp(stage['complete_normalized_f'])==mp(stage['old_natural_effective_prior']) and not stage['unpaid_after_natural'];assert all(answer[d]==u for d,u in locked.items());stages.append({'support':k,'full_demands':len(D),'common_values_preserved':len(locked),'unpaid_after_natural':0});f=answer
    packet=z['H2_packet_owner_ledger'];assert packet['occurrence']==139 and packet['H']==2 and packet['Q_full']==packet['Q_aux9']==2 and not packet['residual_after_natural']
    f9=mp(z['stages'][-1]['smaller_input']);assert all(f9[(139,k)]==f[(139,k)]==(139,1,k-1) for k in (1,2));assert not {(139,2,0),(139,2,1)}&set(f9.values()) and not {(139,2,0),(139,2,1)}&set(f.values())
    files=('H2_actual_owner_candidate.json','ARBITRARY_DIRTY_FRAME_OWNER_THEOREM.md','SOURCE_FORCED_DONOR_EXPANSION.md','DIRTY_FRAME_BANK25_SCHEDULE.md','GLOBAL_H_L_EXCHANGE_APPLICABILITY.md')
    result={'status':'PASS_SOURCE_EXACT_H2_NORMALIZED_OWNER_LINEAGE_AND_EMPTY_RESIDUAL','period':[102,202],'accepted_A_B9_B10_source_audits_reused_without_rerun':True,'new_mutable_B_streams':new_streams,'sealed_base6_core':6,'source_natural_full_maps_at_supports_6_through_10':True,'normalization_stages':stages,'all_archived_inputs_unchanged':True,'packet_actual_demand_units':[[[139,1],[139,1,0]],[[139,2],[139,1,1]]],'packet_second_event_units_unowned_under_aux9_and_full':[[139,2,0],[139,2,1]],'actual_new_donor_required_at_packet':False,'P_after_natural_at_support10':[],'not_a_frozen_owner_obstruction':True,'not_a_universal_donor_theorem':True,'source_queries':queries,'source_engine_calls':queries,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{**{n:hashlib.sha256((C/n).read_bytes()).hexdigest() for n in files},'retirement_boundary_independent_audit.json':hashlib.sha256((B/'retirement_boundary_independent_audit.json').read_bytes()).hexdigest()}}
    assert time.process_time()-START<CAP-1
    out('H2_actual_owner_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify74_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries},f)

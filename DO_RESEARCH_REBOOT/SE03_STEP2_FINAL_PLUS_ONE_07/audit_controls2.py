"""Explicitly authorized historical source-word replays, both immutable engines.
These controls are not the proof of universal FINAL-PLUS1.
"""
import collections,importlib.util,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('final_plus1_auditor',B/'audit_independent2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);a=d.a
sys.path.insert(0,str(B.parent/'SE03_STEP2_COLD_NEG2_01'))
import source_model as p
calls=0;replayed=0;started=time.process_time();CAP=min(60,float(sys.argv[1])-4)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def reflect(v):
    if isinstance(v,str):return 'F'+str(11-int(v[1:]))
    return (12-v[0],reflect(v[2]),reflect(v[1]))
def independent(v):return ('leaf',v) if isinstance(v,str) else a.I.node(v[0],independent(v[1]),independent(v[2]))
def undo(v):return v[1] if v[0]=='leaf' else (v[1],undo(v[2]),undo(v[3]))
def move(v,x):
    global calls
    calls+=2
    z,pa,ev=p.trace(v,x);zz,ee=a.I.trace(independent(v),x)
    assert z==undo(zz) and len(ev)==len(ee)
    assert sum(e['kind']=='DOUBLE' for e in ev)==sum(e[0]!='ZIG' for e in ee)
    assert time.process_time()-started<CAP and calls<1000000
    return z,pa,ev
def norm(v):
    if isinstance(v,dict):return tuple((k,norm(x)) for k,x in sorted(v.items()))
    return tuple(map(norm,v)) if isinstance(v,(tuple,list)) else v
def reflected_chart(c):
    def tree(t):return None if t is None else (c['size']-1-t[0],tree(t[2]),tree(t[1]))
    return {'marks':sorted(12-x for x in c['marks']),'Scores':sorted(12-x for x in c['Scores']),
            'tree':tree(c['tree']),'size':c['size']}
def packets(rows):
    ends=[r['occurrence'] for r in rows if r['genuine_F']];n=len(rows);macros=[]
    for j,end in enumerate(ends):
        prev=ends[j-1];occ=list(range(prev+1,end+1)) if prev<end else list(range(prev+1,n+1))+list(range(1,end+1))
        macros.append({'occ':occ,'H':sum(rows[k-1]['a'] for k in occ),'Q':rows[end-1]['qF']})
    covered=set();result=[]
    for j,m in enumerate(macros):
        if m['Q']!=5:continue
        k=(j+1)%len(macros);assert macros[k]['Q']==1 and j not in covered and k not in covered
        covered.update((j,k));H=m['H']+macros[k]['H'];result.append((tuple(m['occ']+macros[k]['occ']),H,6,2*min(H,4)-6))
    for j,m in enumerate(macros):
        if j not in covered:result.append((tuple(m['occ']),m['H'],m['Q'],2*min(m['H'],4)-m['Q']))
    flat=[i for occ,h,q,w in result for i in occ];assert sorted(flat)==list(range(1,n+1))
    return sorted(result),macros
def replay(name,fam,refl):
    global replayed
    conv=reflect if refl else lambda v:freeze(v)
    key=lambda k:12-k if refl else k
    rows=fam['rows'];charts=fam['charts'];R=conv(rows[0]['before'][0]);E0=conv(rows[0]['before'][2])
    assert R==conv(rows[0]['before'][1])
    z=key(fam.get('erased',fam.get('erased_key',fam.get('predecessor',{}).get('erased',3))))
    source_word=[(v['mode'],v['key']) if isinstance(v,dict) else tuple(v) for v in fam['word']]
    word=[(m,key(k)) for m,k in source_word];A=BF=BE=R;r=();u=None
    # Actual closed-copy reaching prefix, preserving every original operation.
    for j in range(66):
        if j>0 and BE==E0:u=j;break
        for m,x in word:
            A=move(A,x)[0]
            if m=='K':
                BF=move(BF,x)[0];r=(x,)+tuple(k for k in r if k!=x)
                if x!=z:BE=move(BE,x)[0]
        assert A==BF==R
    assert u is not None and set(r)==a.M
    begin=(A,BF,BE,r);cost=[0,0,0];newrows=[];genuine=set();aux_repeat_changes=0
    for i,((m,x),old,c) in enumerate(zip(word,rows,charts),1):
        assert (A,BF,BE)==tuple(conv(v) for v in old['before'])
        before_r=r;gen=m=='K' and x!=BF[0]
        if gen:genuine.add(x)
        A,pa,ae=move(A,x);be=ee=[];pb=''
        if m=='K':
            BF,pb,be=move(BF,x)
            if x!=z:BE,pe,ee=move(BE,x)
            r=(x,)+tuple(k for k in r if k!=x)
        h=len(ae);q=sum(v['kind']=='DOUBLE' for v in be);qe=sum(v['kind']=='DOUBLE' for v in ee)
        assert (h,q,qe)==(old['a'],old['qF'],old['qE']) and gen==old['genuine_F']
        assert (A,BF,BE)==tuple(conv(v) for v in old['after'])
        if m=='K' and q==1:assert len(pb)==2
        if m=='K':assert all(e['kind']=='DOUBLE' and e['case'] in ('LL','RR') for e in be)
        assert before_r==tuple(key(k) for k in c['recent_before']) and r==tuple(key(k) for k in c['recent_after'])
        assert (m=='K' and x not in before_r[:5])==c['cold']
        for fld,t,marks in [('old_chart',conv(old['before'][1]),before_r[:5]),('new_chart',BF,r[:5])]:
            expected=reflected_chart(c[fld]) if refl else c[fld]
            assert norm(p.chart(t,list(marks)))==norm(expected)
        assert BE[0]==next(k for k in r if k!=z)
        newrows.append({'occurrence':i,'mode':m,'target':x,'a':h,'qF':q,'qE':qe,'genuine_F':gen})
        for j,v in enumerate((h,q,qe)):cost[j]+=v
        if m=='K' and not gen and qe>0:aux_repeat_changes+=1
        replayed+=1
    assert (A,BF,BE,r)==begin and genuine==a.M
    pp,macros=packets(newrows)
    want=sorted((tuple(q['occurrences']),q['H'],q['Q'],q['w']) for q in fam['packets'])
    assert pp==want
    normal=collections.Counter()
    for macro in macros:
        if (macro['H'],macro['Q'])!=(1,1):continue
        pos=[i for i in macro['occ'] if newrows[i-1]['a']]
        assert len(pos)==1;event=pos[0];terminal=macro['occ'][-1];target=newrows[terminal-1]['target']
        assert newrows[event-1]['target']==target
        before=True
        for i in macro['occ']:
            row=newrows[i-1]
            if i==event:before=False;continue
            if before:assert row['target']!=target and row['a']==0
            elif i!=terminal:assert row['mode']=='D' and row['target']==target and row['a']==0
        normal[newrows[event-1]['mode']]+=1
    extra={}
    if name=='Sigma_plus1_predecessor':
        old=fam['predecessor'];assert a.L(independent(conv(old['BF'])))==3
        extra['corrected_predecessor_L']=3
    if name=='post_lowering96':
        aa=conv(rows[44]['before'][0]);bb=conv(rows[44]['before'][1]);x=key(11)
        assert len(p.path(aa,x))==8 and len(p.path(bb,x))==8
        assert [a.L(independent(conv(rows[i-1]['after'][1]))) for i in (40,41,42,43,44)]==[4,3,3,2,2]
        extra['Campaign06_canonical_pair_control']='PASS cold q4 A-depth8 after loss/neutral, not forbidden shallow source'
    if name=='zero_restoration70':
        assert [a.L(independent(conv(rows[i-1]['after'][1]))) for i in (37,38,39)]==[3,2,3]
        extra['zero_restoration']='4->3->2->3 retained'
    return {'name':name,'reflected':refl,'original_period_operations':len(word),'reaching_copies_for_audit':u,
        'A':cost[0],'QF':cost[1],'QE':cost[2],'original_CD_slack':2*cost[0]-cost[1],
        'A_BF_BE_recent_and_chart_closure':True,'operations_partitioned_once':True,
        'H1Q1_positive_event_mode_counts':dict(normal),'nongenuine_full_KEEP_aux_double_changes':aux_repeat_changes,**extra}
def main():
    cold=json.loads((B.parent/'SE03_STEP2_COLD_NEG2_01/symbolic_replay.json').read_text())['families']
    controls=[(v['name'],v) for v in cold]
    for name,folder,file in [('Sigma_plus1_predecessor','SE03_STEP2_FORCED_ZERO_INCOMING_02','incoming_family_v2.json'),
        ('zero_restoration70','SE03_STEP2_LEAF_LOWERING_03','pattern_family.json'),
        ('E0_68','SE03_STEP2_FIRST_LOWERING_04','entry_family.json'),
        ('E1_90','SE03_STEP2_FIRST_LOWERING_04','e1_family.json'),
        ('post_lowering96','SE03_STEP2_POST_LOWERING_05','partial_family.json')]:
        controls.append((name,json.loads((B.parent/folder/file).read_text())))
    reports=[]
    for name,fam in controls:
        for refl in (False,True):
            path=B/('control_case_'+name+('_mirror' if refl else '_base')+'.json')
            if path.exists():reports.append(json.loads(path.read_text()))
            else:
                result=replay(name,fam,refl);out(path.name,result);reports.append(result)
    assert all(v['original_CD_slack']>0 for v in reports)
    result={'status':'PASS_ALL_MANDATORY_ORIGINAL_SOURCE_CONTROLS','families':reports,
        'both_immutable_engines':True,'arbitrary_gap_lifting':'unchanged formal gap terms conserved by all rotations',
        'old_normalized_debt_results':'preserved by pins; changing-chart candidate remains refuted',
        'physical_ID_ownership':'original certificates unchanged; no donor assigned or historical ID rewritten',
        'source_engine_calls':calls,'old_semantic_rows_replayed':replayed,'new_finite_tests':0,
        'proof_role':'regression controls only; universal FINAL-PLUS1 uses the complete symbolic language'}
    out('source_control_replay2.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_controls2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'old_semantic_rows_replayed':replayed,'new_finite_tests':0})

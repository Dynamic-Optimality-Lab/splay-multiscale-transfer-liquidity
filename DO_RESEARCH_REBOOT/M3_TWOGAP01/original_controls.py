"""Bounded fresh production-root controls for the new prefix construction."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_TWOGAP01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from prefix_profiles import BASE,KEYS,normalize,core
import interior_original as IN
import outside_original as OUT
S=IN.S;V=IN.V
def labels(t):
    if t is None or t=='G':return set()
    return {t[0]}|labels(t[1])|labels(t[2])
def hasghost(t):return t=='G' or (isinstance(t,list) and (hasghost(t[1]) or hasghost(t[2])))
def expand(t,keys=KEYS,parent=None,side=None,cuts=None,ghosts=None):
    if cuts is None:cuts=[];ghosts=[]
    if t is None:
        if parent is not None:cuts.append((parent,side))
        return S.balanced(list(keys)),cuts,ghosts
    if t=='G':
        assert not keys,keys;ghosts.append((parent,side));return S.LEAF,cuts,ghosts
    k,l,r=t;assert k in keys
    ll,_,_=expand(l,tuple(x for x in keys if x<k),k,0,cuts,ghosts)
    rr,_,_=expand(r,tuple(x for x in keys if x>k),k,1,cuts,ghosts)
    return S.node(k,ll,rr),cuts,ghosts
def main():
    start=time.process_time();out=BASE/'original_controls.json';assert not out.exists()
    c=json.loads((BASE/'relation.json').read_text());N=c['classes'];sid={tuple(map(tuple,a)):i for i,a in enumerate(c['shadows'])}
    ps=json.loads((BASE/'potential_sparse.json').read_text());J={int(k):v for k,v in ps['labels'].items()}
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());psi=[r['psi'] for r in bc['nodes']]
    bids={json.dumps(r['tree'],separators=(',',':')):i for i,r in enumerate(bc['nodes'])}
    cc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text());K=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text());bk={}
    for b,row in enumerate(bc['nodes']):
        r=row['tree'][0]
        for x in range(9):
            h=cc['B_depth'][b][x]
            if h:bk.setdefault((1,2-h//2,r,x),b)
    for row in K['rows']:
        if row['gap0_childless_at_exit']:bk.setdefault((2,row['w'],bc['nodes'][row['entry_core']]['tree'][0],row['target']),row['entry_core'])
    selected={};wanted={(H,w,g) for H,ws in ((1,(-2,-1,0,1)),(2,(0,1))) for w in ws for g in (False,True)}
    for a,options in enumerate(c['options']):
        r=c['shadows'][a][0][2]
        for o in options:
            wi=o['witness'];wit=c['witnesses'][wi];t=wit['tree']
            if not {-8,8}<=labels(t):continue
            g=hasghost(t)
            for H,w,gg in wanted-selected.keys():
                if gg!=g or H!=o['H']:continue
                b=bk.get((H,w,r,o['target']))
                if b is not None:selected[(H,w,g)]=(a,o,b)
            if len(selected)==len(wanted):break
        if len(selected)==len(wanted):break
    assert len(selected)==len(wanted),(len(selected),wanted-selected.keys())
    d=IN.DAG();L=IN.build_slow(d,'MXL');records=[]
    def jvalue(state,b):
        a=sid.get(normalize(state['alpha']));return J.get(b*N+a,-psi[b]) if a is not None else -psi[b]
    def core_serial(t):return None if t[0]=='leaf' else [t[1]//16,core_serial(t[2]),core_serial(t[3])]
    def coreonly(t):
        if t[0]=='leaf':return t
        if not core(t[1]):assert t[2][0]==t[3][0]=='leaf';return S.LEAF
        return S.node(t[1],coreonly(t[2]),coreonly(t[3]))
    for number,((H,w,g),(a,o,b)) in enumerate(sorted(selected.items())):
        wit=c['witnesses'][o['witness']];A,cuts,ghosts=expand(wit['tree']);B=V.from_serial(bc['nodes'][b]['tree'])
        def scaled(t):return S.LEAF if t[0]=='leaf' else S.node(16*t[1],scaled(t[2]),scaled(t[3]))
        B=scaled(B);B=V.insert(V.insert(B,-8),8)
        word=[['K',x] for x in wit['targets']];r=A[1]//16;x=o['target'];marks={x}
        marks.update(k for k in range(9) if k!=r and len(marks)<5);mu=sum(1<<k for k in marks);assert mu.bit_count()==5
        helper=IN if number%2 else OUT;label=f'H{H}_w{w}_ghost{g}_region{number%2}'
        Ad,Bd,record=helper.low(d,L,A,B,cuts,word,label,mu);e=record['environment'];am=helper.model(A,cuts);slots={v['key']:i for i,v in am.slots.items()}
        for gi,(k,side) in enumerate(ghosts):
            slot=slots[k];e[f'MXLw_k{"l" if side==0 else "r"}{slot}']=0;e[f'MXLw_c{"l" if side==0 else "r"}{slot}']=127 if gi%2==0 else 255
        ww=IN.exact_witness(e);st=IN.AState(IN.ED,ww);sa=IN.alpha_prefix(ww,st)
        for ev in range(len(word)):st=IN.splay_event(IN.ED,ww,st,ev,IN.Box(True))
        ta=IN.alpha_prefix(ww,st)
        for state,obj,alpha in ((record['source'],L['s'],sa),(record['destination'],L['t'],ta)):
            state['alpha']=alpha
            for i,(k,s,x) in enumerate(alpha):V.put(d,e,obj.ak[i],k);V.put(d,e,obj.aS[i],bool(s));V.put(d,e,obj.aI[i],x)
        assert normalize(sa)==tuple(map(tuple,c['shadows'][a]));assert normalize(ta)==tuple(map(tuple,c['shadows'][o['destination']]))
        assert d.ev_ground(L['root'],e),label
        bb=bids[json.dumps(core_serial(coreonly(Bd)),separators=(',',':'))]
        js=jvalue(record['source'],b);jt=jvalue(record['destination'],bb);res=w-jt+js;assert res>=0
        assert record['H']==H and record['w']==w
        record.update(prefix_source_class=a,prefix_destination_class=o['destination'],ghost_pairs=ghosts,
                      source_B_core=b,destination_B_core=bb,J_source=js,J_destination=jt,residual=res,
                      chi8_region=bool(number%2),fresh_original_root=True)
        records.append(record);assert time.process_time()-start<300,'UNKNOWN original audit CPU cap'
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_GAPMULTI01/obstruction.json').read_text())
    for record in old['records']:
        rr=copy.deepcopy(record);assert d.ev_ground(L['root'],rr['environment'])
        A=V.from_serial(rr['B_source_codes']);B=V.from_serial(rr['B_destination_codes'])
        b=bids[json.dumps(core_serial(coreonly(A)),separators=(',',':'))];bb=bids[json.dumps(core_serial(coreonly(B)),separators=(',',':'))]
        js=jvalue(rr['source'],b);jt=jvalue(rr['destination'],bb);assert rr['w']-jt+js>=0
        rr.update(J_source=js,J_destination=jt,residual=rr['w']-jt+js,fresh_original_root=True);records.append(rr)
    assert records[-1]['source']==records[-2]['source'] and records[-1]['destination']==records[-2]['destination']
    result={'status':'BOUNDED_FRESH_ORIGINAL_LOW_CONTROLS_PASS','full_original_roots':len(records),'DAG_nodes':len(d.nodes),
      'selected_H_weight_ghost_cases':[list(x) for x in sorted(selected)],'both_chi8_regions':True,
      'equal_state_different_private_splits_same_J':True,'minimum_residual':min(r['residual'] for r in records),
      'cpu_seconds':round(time.process_time()-start,3),'independent_complete_certificate_audit':False,'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()

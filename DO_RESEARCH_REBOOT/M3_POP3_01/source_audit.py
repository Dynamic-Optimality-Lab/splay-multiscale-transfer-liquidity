"""Only new population3 source controls, with immediate checkpoints."""
import sys,json,time,hashlib,copy,importlib.util
from pathlib import Path
from itertools import product
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_POP3_01','DO_RESEARCH_REBOOT/M3_UNITPAIR01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
# Load explicitly: UNITPAIR01 also has a module named decoder.
spec=importlib.util.spec_from_file_location('population_three_decoder',Path('DO_RESEARCH_REBOOT/M3_POP3_01/decoder.py'));D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
from proposal_factory_v2 import proposals
import interior_original as IN
import outside_original as OUT
sp=importlib.util.spec_from_file_location('independent_population_raw',Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01/source_audit.py'));A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_01');S=IN.S
def fullsig(v):return list(v)+[0]*7
def mirror(t):return S.LEAF if t[0]=='leaf' else S.node(128-t[1],mirror(t[3]),mirror(t[2]))
def decode_term(code):
    chars=iter(code)
    def read():
        c=next(chars)
        if c=='a':return None
        if c=='b':return 'G'
        return (int(c,16),read(),read())
    t=read();assert next(chars,None) is None;return t
def positions(t,p=()):
    if not isinstance(t,tuple):return []
    return positions(t[1],p+(0,))+([(p,t[0])] if t[0]==9 else [])+positions(t[2],p+(1,))
def color_and_expand(code,sig,firstpath,nonminimum):
    if 'b' in code:return None
    t=decode_term(code);anons=[p for p,k in positions(t)];support=[g for g,n in enumerate(sig) if n]
    def valid(n,p,lo,hi,allowed,colors):
        if n is None:return True
        if n=='G':return lo>hi
        k,l,r=n
        if k<9:
            return lo<=k<=hi and valid(l,p+(0,),lo,k-1,{g for g in allowed if g<=k},colors) and valid(r,p+(1,),k+1,hi,{g for g in allowed if g>k},colors)
        gap=colors[p]
        return gap in allowed and lo<=gap<=hi+1 and valid(l,p+(0,),lo,gap-1,{g for g in allowed if g<=gap},colors) and valid(r,p+(1,),gap,hi,{g for g in allowed if g>=gap},colors)
    for choices in product(support,repeat=len(anons)):
        colors=dict(zip(anons,choices))
        if firstpath is not None and colors.get(tuple(firstpath))!=0:continue
        if any(choices.count(g)>sig[g] for g in range(3)) or not valid(t,(),0,8,set(support),colors):continue
        assigned={};counts=[0]*3
        for p in anons:
            gap=colors[p];assigned[p]=16*gap-8+counts[gap];counts[gap]+=1
        if nonminimum and (firstpath is None or assigned[tuple(firstpath)]<=-8):continue
        keys=tuple(sorted([16*k for k in range(9)]+[16*g-8+j for g,n in enumerate(sig) for j in range(n)]));cuts=[]
        def fill(n,p,lo,hi,parent=None,side=None):
            available=[x for x in keys if lo<x<hi]
            if n is None:
                if parent is not None:cuts.append((parent,side))
                return S.balanced(available)
            label,left,right=n;k=16*label if label<9 else assigned[p];assert lo<k<hi
            return S.node(k,fill(left,p+(0,),lo,k,k,0),fill(right,p+(1,),k,hi,k,1))
        tree=fill(t,(),-10000,10000);assert S.inorder(tree)==list(keys)
        return tree,cuts,assigned
    return None
def main():
    out=BASE/'source_audit.json';assert not out.exists();start=time.process_time()
    run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL7_LEADING_THREE_UNIT_FINITE_CERTIFICATES_PASS'
    P=D.PopulationThreeCertificate();dl=IN.DAG();L=IN.build_slow(dl,'MXL');dh=IN.DAG();H=IN.build_shigh(dh,'MXH');FIN,FOUT=proposals(IN),proposals(OUT)
    rows=[];cycles=[];completed=[];seen={};source_files=[];z=S.LEAF
    def check(r,kind,require_profile=True,expected_classes=None):
        d,obj=(dl,L) if kind=='LOW' else (dh,H);e=r['environment'];digest=hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest();identity=(kind,digest)
        if identity in seen:return seen[identity]
        assert set(d.vars)<=set(e)
        for name,n in d.vars.items():
            nd=d.nodes[n];v=e[name]
            if nd[1]=='bool':assert v in (False,True)
            else:
                w,sg=nd[3][2:4];assert (-(1<<(w-1))<=v<(1<<(w-1))) if sg else 0<=v<(1<<w)
        assert d.ev_ground(obj['root'],e),r['label']
        s=A.ordinary(d,e,obj['s']);t=A.ordinary(d,e,obj['t']);assert s==r['source'] and t==r['destination'];assert len(A.flat(s))==len(A.flat(t))==147
        si=P.inspect(s);ti=P.inspect(t);js,jt=si['value'],ti['value']
        if require_profile:assert si['profile_found'] and ti['profile_found'],r['label']
        if expected_classes is not None:assert (si['A'],ti['A'])==tuple(expected_classes)
        if kind=='LOW':
            nev=A.val(d,e,L['wit'].nev);hh=sum((A.val(d,e,L['wit'].evd[i])+1)//2 for i in range(nev));q=A.val(d,e,L['bt'].q)
            assert hh==r['H'] and q==r['q'] and 2*hh-q==r['w'];weight=r['w'];res=weight-P.O(t)+P.O(s);assert res>=0;m=None
        else:
            m=A.mid(d,e,H['g']);assert m==r['shared_midpoint'] and len(A.flat(m))==127
            weight=A.val(d,e,H['w1']);q=A.val(d,e,H['q']);assert weight==6-q;res=[weight-P.M(m)+P.O(s),P.M(m)-P.O(t)];assert min(res)>=0
        if s['sigma'][9]:assert not P.chi(s['b']) and not P.chi(t['b'])
        row={'label':r['label'],'kind':kind,'source':s,'destination':t,'midpoint':m,'source_potential':si,'destination_potential':ti,'weight':weight,
          'q':q,'residual':res,'original_root':True,'environment_sha256':digest,'environment':e};rows.append(row);seen[identity]=row
        # Save immediately: an interruption cannot erase an accepted root.
        name=f'root_{len(rows):03d}.json'
        with (BASE/name).open('x',encoding='utf-8') as f:json.dump(row,f,separators=(',',':'))
        source_files.append(name);assert time.process_time()-start<300,'UNKNOWN population source-family CPU cap';return row
    signatures=[]
    for sig in run['completed_signatures']:
        s=fullsig(sig);signatures.extend((s,list(reversed(s))))
    for index,sig in enumerate(signatures):
        label=''.join(map(str,sig));checkpoint=BASE/f'source_{label}.json';assert not checkpoint.exists();first=len(rows)
        helper=FOUT if sig[9] or index%2 else FIN
        core=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])));AA=core;BB=core
        for gap,n in enumerate(sig):
            for j in range(n):AA=IN.V.insert(AA,16*gap-8+j)
            if n:BB=IN.V.insert(BB,16*gap-8)
        _,Bd,low=helper.low(dl,L,AA,BB,[(0,1),(96,0)],[['K',96]],f'population_{label}_cycle_low',341)
        high=helper.high(dh,H,Bd,32,low['destination'],low['source'],f'population_{label}_cycle_high');lo=check(low,'LOW');hi=check(high,'HIGH')
        assert A.flat(lo['source'])==A.flat(hi['destination']) and A.flat(lo['destination'])==A.flat(hi['source']);assert low['w']+high['w']==8
        cycle={'sigma':sig,'weight':8,'full147_O_closure':True,'same127_M':True,'chi8':P.chi(lo['source']['b'])};cycles.append(cycle)
        AA=S.node(0,z,S.node(128,S.balanced([16*k for k in range(1,8)]),z));BB=z
        for k in reversed(range(9)):BB=S.node(16*k,z,BB)
        for gap,n in enumerate(sig):
            for j in range(n):AA=IN.V.insert(AA,16*gap-8+j)
            if n:BB=IN.V.insert(BB,16*gap-8)
        _,_,r=helper.low(dl,L,AA,BB,[(128,0)],[['K',128]],f'population_{label}_negative_low',341);check(r,'LOW');assert r['w']==-2
        with checkpoint.open('x',encoding='utf-8') as f:json.dump({'status':'PASS','sigma':sig,'root_files':source_files[first:],'cycle':cycle},f,indent=2)
        completed.append(sig);print(json.dumps({'population_source_cases':len(completed),'roots':len(rows),'CPU':round(time.process_time()-start,3)}),flush=True)
    # Critical repeated-gap helper controls selected from new rows, not repeated old tests.
    def helper_control(sig,w,nonminimum=False,first_LR=False):
        folder=BASE/('s'+''.join(map(str,sig)));c=json.loads((folder/'relation.json').read_text());B=P.B;choice={}
        for b,row in enumerate(B['kernels']['0']):
            for x,pair in enumerate(row):
                if pair is not None and pair[1]==w:choice.setdefault((B['trees'][b][0],x),b)
        for a,opts in enumerate(c['options']):
            root=c['shadows'][a][0][2]
            for o in opts:
                hh,x,aa,helper,fi,code=o
                if hh!=2:continue
                word=c['families'][fi]['word']
                if first_LR and word[0]!=[0,1]:continue
                b=choice.get((root,x))
                if b is None:continue
                expanded=color_and_expand(code,sig,word[0],nonminimum)
                if expanded is None:continue
                AA,cuts,assigned=expanded
                def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
                BB=scale(B['trees'][b])
                for gap,n in enumerate(sig):
                    if n:BB=IN.V.insert(BB,16*gap-8)
                current=AA;targets=[]
                for path in word:
                    node=current
                    for side in path:node=node[2+side]
                    targets.append(node[1]);current=S.trace(current,node[1])[0]
                assert targets[-1]==16*x
                if nonminimum:assert targets[0]>-8 and targets[0]<0
                marks={x};marks.update(k for k in range(9) if len(marks)<5);mu=sum(1<<k for k in marks)
                _,_,r=FIN.low(dl,L,AA,BB,cuts,[['K',k] for k in targets],f'population_{sig}_helper_w{w}_nonmin{nonminimum}_LR{first_LR}',mu)
                row=check(r,'LOW',expected_classes=(a,aa));assert r['H']==2 and r['w']==w
                return {'row':row,'A':AA,'B':BB,'cuts':cuts,'targets':targets,'mu':mu,'sigma':sig}
        return None
    h0=helper_control((2,1,0),0,True);h1=helper_control((2,1,0),1,True);assert h0 is not None and h1 is not None
    lr=None
    for w in (0,1,2,3,4):
        lr=helper_control((2,1,0),w,True,True)
        if lr is not None:break
    assert lr is not None
    triple=helper_control((1,1,1),1);assert triple is not None
    # DELETE followed by zero-charge KEEP at the SAME nonminimum actual A node.
    item=h1;targets=item['targets'];word=[['D',targets[0]],['K',targets[0]],['K',targets[1]]]
    _,_,r=FIN.low(dl,L,item['A'],item['B'],item['cuts'],word,'population210_nonminimum_DELETE_KEEP_normal_form',item['mu'])
    macro=check(r,'LOW');normal=item['row'];assert A.flat(macro['source'])==A.flat(normal['source']) and A.flat(macro['destination'])==A.flat(normal['destination']) and macro['weight']==normal['weight'] and macro['q']==normal['q']
    # Reflect the actual fixture, then validate the ORIGINAL reflected predicate.
    AA=mirror(item['A']);BB=mirror(item['B']);cuts=[(128-k,1-side) for k,side in item['cuts']];word=[['K',128-k] for k in targets]
    reflected_mu=sum(1<<(8-k) for k in range(9) if item['mu']>>k&1)
    _,_,r=FOUT.low(dl,L,AA,BB,cuts,word,'population_trailing_nonmaximum_gap9_helper',reflected_mu);reflected=check(r,'LOW');assert r['word_codes'][0][1]<136 and r['word_codes'][0][1]>128
    # A repeated interior gap, both anonymous occurrences actually exposed.
    AA=S.node(0,S.node(-8,z,z),S.node(9,S.node(8,z,z),S.node(128,S.balanced([16*k for k in range(1,8)]),z)));BB=z
    for k in reversed(range(9)):BB=S.node(16*k,z,BB)
    BB=IN.V.insert(IN.V.insert(BB,-8),8)
    _,_,r=FIN.low(dl,L,AA,BB,[(128,0)],[['K',128]],'population120_two_visible_same_gap1_nodes',341);check(r,'LOW');assert r['w']==-2
    # Gamma0 H2 permits a charged DELETE at a nonminimum gap0 key; actual B stays unchanged before terminal.
    AA=S.node(128,S.node(-7,S.node(-8,z,z),S.node(0,z,S.balanced([16*k for k in range(1,8)]))),z);AA=IN.V.insert(AA,8);BB=z
    for k in range(9):BB=S.node(16*k,BB,z)
    BB=IN.V.insert(IN.V.insert(BB,-8),8)
    _,_,r=FIN.low(dl,L,AA,BB,[(0,1)],[['D',-7],['K',0]],'population210_Gamma0_DELETE_nonminimum_then_core',341);check(r,'LOW',False);assert r['H']==2 and r['q']==4 and r['w']==0
    # New signature, same high freedoms: correct h=0/declared18 and independent fiber v4.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_TWOGAP01/decoder_and_h0.json').read_text())['records'];r=copy.deepcopy(next(t for t in old if t['fiber_v']==4));r['label']='population210_h0_corrected_weight_minus3_fiber4';sig=fullsig((2,1,0))
    for state in (r['source'],r['destination'],r['shared_midpoint']):state['sigma']=sig
    for obj in (H['s'],H['t'],H['g']):
        for node,n in zip(obj.sig,sig):r['environment'][dh.nodes[node][3][1]]=n
    high=check(r,'HIGH',False);assert high['weight']==-3 and high['midpoint']['v']==4
    report={'status':'POPULATION3_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS','signatures':14,'completed_signatures':completed,'unique_original_roots':len(rows),
      'full_closed_mixed_cycles':len(cycles),'all147_O_coordinates':True,'same_actual127_M':True,'nonminimum_gap0_helper':True,
      'nonmaximum_gap9_helper':True,'new_LR_helper_pattern':True,'charged_DELETE_zero_KEEP_identity':True,'repeated_interior_gap_nodes_exposed':True,
      'Gamma0_actual_terminal_debt_control':True,'h0_correction_and_independent_v4':True,'previous_source_checks_repeated':0,
      'DAG_nodes':[len(dl.nodes),len(dh.nodes)],'CPU_seconds':round(time.process_time()-start,3),'root_files':source_files,'cycles':cycles,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('root_files','cycles','completed_signatures')},indent=2),flush=True)
if __name__=='__main__':main()

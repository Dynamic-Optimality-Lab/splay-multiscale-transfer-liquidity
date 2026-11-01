"""Evaluate one explicit terminal packing function on a frozen source corpus."""
from pathlib import Path
import hashlib,json,subprocess,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def rp(t):return None if t is None else [t['k'],rp(t['l']),rp(t['r'])]
def ints(t):
    if t==S.LEAF:return set()
    ks=S.inorder(t)
    return {(ks[0],ks[-1])}|ints(t[2])|ints(t[3])
def proper(t):
    ks=S.inorder(t);ss=ints(t)
    if ks:ss.remove((ks[0],ks[-1]))
    return sorted(ss)
def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
def pairkey(a,b):return json.dumps([raw(a),raw(b)],separators=(',',':'))
def disjoint(I,J):return I[1]<J[0] or J[1]<I[0]
def ev(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]

def dual(adj,allowed):
    allowed=set(allowed);mr={j:None for j in allowed}
    def aug(i,seen):
        for j in adj[i]:
            if j not in allowed or j in seen:continue
            seen.add(j)
            if mr[j] is None or aug(mr[j],seen):mr[j]=i;return True
        return False
    for i in range(len(adj)):aug(i,set())
    ml={i:j for j,i in mr.items() if i is not None};zl={i for i in range(len(adj)) if i not in ml};zr=set();queue=list(zl)
    while queue:
        i=queue.pop()
        for j in adj[i]:
            if j not in allowed or ml.get(i)==j or j in zr:continue
            zr.add(j)
            if mr[j] is not None and mr[j] not in zl:zl.add(mr[j]);queue.append(mr[j])
    mat=sorted([[i,j] for i,j in ml.items()]);cl=sorted(set(range(len(adj)))-zl);cr=sorted(zr)
    ck(len(mat)==len(cl)+len(cr) and all(i in cl or j in cr for i,row in enumerate(adj) for j in row if j in allowed),'matching cover equality')
    return {'allowed_right':sorted(allowed),'matching':mat,'cover_left':cl,'cover_right':cr,'rank':len(mat)}

TERMINALS=[];TCACHE={};RAW_P=[];PCACHE={}
def terminal(a,c):
    key=pairkey(a,c)
    if key not in TCACHE:
        aa=proper(a);bb=proper(c);common=sorted(set(aa)&set(bb));cs=set(common);l=[I for I in aa if I not in cs];r=[J for J in bb if J not in cs]
        adj=[[j for j,J in enumerate(r) if I[0]==J[0] or I[1]==J[1]] for I in l]
        ants=[]
        for mask in range(1<<len(r)):
            chosen=[j for j in range(len(r)) if (mask>>j)&1]
            if not all(disjoint(r[i],r[j]) for i in chosen for j in chosen if i<j):continue
            if any(all(disjoint(r[i],r[j]) for i in chosen) for j in range(len(r)) if j not in chosen):continue
            ants.append(chosen)
        certs=[dual(adj,a0) for a0 in ants];full=dual(adj,range(len(r)));best=max(range(len(certs)),key=lambda i:certs[i]['rank']);alpha=certs[best]['rank'];f=len(aa)-len(common)
        ck(alpha<=full['rank'] and a[1]==c[1],'terminal roots and alpha comparison')
        g={'A':raw(a),'C':raw(c),'all_A_intervals':[list(I) for I in aa],'all_C_intervals':[list(J) for J in bb],
          'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in l],'right_residual':[list(J) for J in r],
          'adjacency':adj,'unrestricted_dual':full,'maximal_antichain_duals':certs,'maximizing_antichain_index':best,
          'alpha':alpha,'F':f,'K':f-alpha,'Ehat':f-full['rank']}
        TCACHE[key]=len(TERMINALS);TERMINALS.append(g)
    i=TCACHE[key];g=TERMINALS[i]
    return {'terminal_graph':i,'F_terminal':g['F'],'alpha_terminal':g['alpha'],'K_terminal':g['K']}

def raw_p(a,b):
    key=pairkey(a,b)
    if key not in PCACHE:
        aa=proper(a);bb=proper(b);common=sorted(set(aa)&set(bb));cs=set(common);l=[I for I in aa if I not in cs];r=[J for J in bb if J not in cs and not(J[0]<=a[1]<=J[1])]
        adj=[[j for j,J in enumerate(r) if I[0]==J[0] or I[1]==J[1]] for I in l];d=dual(adj,range(len(r)));f=len(aa)-len(common)
        g={'A':raw(a),'B':raw(b),'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in l],
          'eligible_right_residual':[list(J) for J in r],'adjacency':adj,'dual':d,'P':f-d['rank'],'F':f}
        PCACHE[key]=len(RAW_P);RAW_P.append(g)
    i=PCACHE[key];return {'raw_P_graph':i,'P':RAW_P[i]['P']}

def completion(a,b):
    r=a[1];c,es=S.trace(b,r);pc,pes=P.splay_trace(ptr(b),r)
    ck(raw(c)==rp(pc) and [list(e) for e in es]==ev(pes),'completion source engines agree')
    v=terminal(a,c);q=sum(e[0]!='ZIG' for e in es);z=sum(e[0]=='ZIG' for e in es);d=S.lookup(b,r)[1]
    ck(q==d//2 and z==d%2,'completion costs')
    return {'root_A':r,'completed_B':raw(c),'completion_depth':d,'completion_q':q,'completion_z':z,
      'completion_events':ev(pes),**v,'Phi':v['K_terminal']+q}

def edge(label,a,b,mode,x,with_p=False):
    aa,ea=S.trace(a,x)
    if mode=='K':bb,eb=S.trace(b,x)
    else:bb,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ck(raw(aa)==rp(pa) and raw(bb)==rp(pb) and [list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'actual source agreement')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'actual source units')
    v0,vm,v1=completion(a,b),completion(aa,b),completion(aa,bb)
    if mode=='K':ck(v1['Phi']-vm['Phi']==-q,'exact universal B identity finite corroboration')
    delta=v1['Phi']-v0['Phi'];budget=2*ac-q
    row={'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,'destination_A':raw(aa),'destination_B':raw(bb),
      'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),'source_completion':v0,'after_A_completion':vm,
      'destination_completion':v1,'delta_Phi':delta,'budget':budget,'whole_law_holds':delta<=budget}
    if with_p:
        ps,pd=raw_p(a,b),raw_p(aa,bb);row.update({'source_P':ps,'destination_P':pd,'R_source':v0['Phi']-ps['P'],'R_destination':v1['Phi']-pd['P']})
    return aa,bb,row

def main():
    ck((OUT/'AT00_FOUR_RULE_GATE.md').is_file(),'written gate before audit')
    base=OUT.parent
    def read(d,n):return json.loads((base/d/n).read_text(encoding='utf-8'))
    cp=read('route_c_root_completion_20261031_v001','root_completion_certificate.json')
    ja=read('route_c_joint_alignment_correction_20261031_v001','joint_alignment_certificate.json')
    bn=read('route_c_b_normalized_correction_20261031_v001','b_normalization_certificate.json')
    rs=read('route_c_root_safe_matching_20261031_v001','root_matching_certificate.json')
    fx=read('route_c_fixed_exact_pairs_20261031_v001','fixed_exact_pair_certificate.json')
    ra=read('route_c_analytic_20261030_v001','six_key_closed_controls.json')
    prior=base/'route_c_root_completion_20261031_v001';entry=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['CP00_FOUR_RULE_GATE.md','CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md','CP02_ALL_ODD_DELETE_AND_TERMINAL_CLASS_OBSTRUCTION.md','CP03_STRATEGY_REVIEW.md','CP04_FINAL_REPORT.md','root_completion_certificate.json','independent_audit.json','final_integrity.json'])
    pins={p:sha(ROOT/p) for p in sorted(paths)};ck(all(pins[p]==h for p,h in entry['files'].items()),'inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'AT00_FOUR_RULE_GATE.md')})
    lm=next(r for r in fx['controls'] if r['label']=='helper_L_m0');rm=next(r for r in fx['controls'] if r['label']=='helper_R_m0')
    controls_to_test=[(cp['controls'][0],ja['closed_witness']),(cp['controls'][1],bn['closed_witness']),
      (cp['controls'][2],cp['closed_witness']),(lm,ra['controls'][0]),(rm,ra['controls'][1]),(rs['controls'][-1],rs['closed_witness'])]
    controls=[];reflections=[];failure=None;witness=cp['closed_witness'];origin='CP fixed 21-step word after controls'
    for i,(old,w) in enumerate(controls_to_test):
        _,_,r=edge('fixed_control_'+str(i)+'_'+old['label'],dec(old['source_A']),dec(old['source_B']),old['mode'],old['key'],True)
        controls.append(r);n=len(S.inorder(dec(r['source_A'])))
        _,_,m=edge('reflection_'+r['label'],mirror(dec(r['source_A']),n),mirror(dec(r['source_B']),n),r['mode'],n+1-r['key'],True);reflections.append(m)
        if not r['whole_law_holds']:failure=r;witness=w;origin='existing witness for fixed control '+str(i);break
    a,b=dec(witness['initial_A']),dec(witness['initial_B']);ia,ib=a,b;replay=[]
    for i,(mode,x) in enumerate(witness['word']):
        a,b,r=edge('frozen_closed_'+str(i),a,b,mode,x);replay.append(r)
        if failure is None and not r['whole_law_holds']:failure=r
    ck(a==ia and b==ib,'actual paired diagonal closure')
    if failure is not None:
        hits=[i for i,r in enumerate(replay) if (r['source_A'],r['source_B'],r['mode'],r['key'])==(failure['source_A'],failure['source_B'],failure['mode'],failure['key'])]
        ck(hits,'first failure lies on its frozen replay');failed_index=hits[0]
        n=len(S.inorder(dec(failure['source_A'])))
        _,_,failure_mirror=edge('reflection_of_first_failure',mirror(dec(failure['source_A']),n),mirror(dec(failure['source_B']),n),failure['mode'],n+1-failure['key'],True)
        ck(not failure_mirror['whole_law_holds'],'reflected first failure')
    else:failed_index=None;failure_mirror=None
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck(sum(r['delta_Phi'] for r in replay)==0 and Qt<=2*At,'explicit potential telescope and no CD counterexample')
    save('antichain_terminal_certificate.json',{'date':'2026-10-31','controls':controls,'reflections':reflections,'terminal_graphs':TERMINALS,'raw_P_graphs':RAW_P,
      'first_failure':failure,'first_failure_reflection':failure_mirror,'disposition':'REFUTED—EXACT' if failure else 'OPEN',
      'closed_witness':{'origin':origin,'initial_A':raw(ia),'initial_B':raw(ib),'word':witness['word'],'failed_edge_index':failed_index,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'fixed_control_limit':6,'finite_potential_fits':0,'new_BFS_calls':0,'new_pair_graphs':0,'new_metric_graphs':0,'coefficient_searches':0,
      'global_DELETE_not_inferred_from_survival':True})
    print(json.dumps({'disposition':'REFUTED—EXACT' if failure else 'OPEN','controls':[{'label':r['label'],'Phi':[r['source_completion']['Phi'],r['destination_completion']['Phi']],
      'R':[r['R_source'],r['R_destination']],'a':r['a'],'q':r['q'],'budget':r['budget'],'holds':r['whole_law_holds']} for r in controls],
      'first_failure':None if failure is None else {k:failure[k] for k in ['label','mode','key','a','q','delta_Phi','budget']},
      'terminal_graphs':len(TERMINALS),'antichain_duals':sum(len(g['maximal_antichain_duals']) for g in TERMINALS),'raw_P_graphs':len(RAW_P),
      'closed_word_length':len(replay),'totals':[At,Qt,Zt],'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()

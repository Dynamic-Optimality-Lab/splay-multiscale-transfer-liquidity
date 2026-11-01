"""Joint correction audit using only inherited exact matching duals."""
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
def mir(t):return S.LEAF if t==S.LEAF else S.node(7-t[1],mir(t[3]),mir(t[2]))
def pairkey(a,b):return json.dumps([a,b],separators=(',',':'))
PRIOR_GRAPHS={};GRAPHS=[];CACHE={}
def values(a,b):
    ra,rb=raw(a),raw(b);key=pairkey(ra,rb)
    ck(key in PRIOR_GRAPHS,'every evaluated P state already has an inherited dual')
    if key not in CACHE:CACHE[key]=len(GRAPHS);GRAPHS.append(PRIOR_GRAPHS[key])
    i=CACHE[key];g=GRAPHS[i];same=a[1]==b[1];r=0 if same else g['mu_root'];h=g['P']+r
    ck(h==(g['P'] if same else g['F']),'joint selector identity')
    return {'P':g['P'],'F':g['F'],'mu_root':g['mu_root'],'same_roots':same,'R':r,'H':h,'graph_id':i}

def edge(label,a,b,mode,x,evaluate=False):
    aa,ea=S.trace(a,x)
    if mode=='K':bb,eb=S.trace(b,x)
    else:bb,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(raw(aa)==rp(pa) and raw(bb)==rp(pb),'both full source endpoints agree')
    ck([list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'all oriented source events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source units')
    row={'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,'destination_A':raw(aa),'destination_B':raw(bb),
      'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),'budget':2*ac-q}
    if evaluate:
        v0,v1=values(a,b),values(aa,bb);delta=v1['H']-v0['H']
        row.update({'source_values':v0,'destination_values':v1,'delta_H':delta,'whole_law_holds':delta<=row['budget']})
    return aa,bb,row

def main():
    ck((OUT/'JA00_FOUR_RULE_GATE.md').is_file(),'written gate precedes audit')
    base=OUT.parent
    inputs=[('route_c_root_safe_matching_20261031_v001','root_matching_certificate.json'),
      ('route_c_p_envelope_correction_20261031_v001','p_envelope_certificate.json'),
      ('route_c_b_normalized_correction_20261031_v001','b_normalization_certificate.json')]
    data=[]
    for d,f in inputs:
        path=base/d/f;c=json.loads(path.read_text(encoding='utf-8'));data.append(c)
        for i,g in enumerate(c['matching_graphs']):
            key=pairkey(g['A'],g['B'])
            if key in PRIOR_GRAPHS:
                old=PRIOR_GRAPHS[key];ck((old['P'],old['F'],old['mu_root'])==(g['P'],g['F'],g['mu_root']),'inherited dual values consistent')
            else:PRIOR_GRAPHS[key]={**g,'origin_certificate':path.relative_to(ROOT).as_posix(),'origin_graph_index':i}
    rs,pe,bn=data
    prior=base/'route_c_b_normalized_correction_20261031_v001'
    entry=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['BN00_FOUR_RULE_GATE.md','BN01_EXPLICIT_CORRECTION_AND_REPAIRS.md','BN02_STARVED_HELPER_AND_GAUGE_OBSTRUCTION.md','BN03_REACHABLE_REPLAY_AND_VERIFICATION.md','BN04_STRATEGY_REVIEW.md','BN05_FINAL_REPORT.md','b_normalization_certificate.json','independent_audit.json','final_integrity.json'])
    paths.add((base/'route_c_analytic_20261030_v001/RA01_UNIFORM_ROTATION_IDENTITY.md').relative_to(ROOT).as_posix())
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in entry['files'].items()),'all inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'JA00_FOUR_RULE_GATE.md')})
    selected=[r for r in rs['controls'] if r['label'] in ['old_six_key_hook','padded_six_key_hook','six_key_opposite_vines','root_change_DELETE_family_n6']]
    selected += [pe['controls'][2],bn['controls'][4]]
    controls=[]
    for old in selected:
        _,_,row=edge('joint_'+old['label'],dec(old['source_A']),dec(old['source_B']),old['mode'],old['key'],True)
        ck(row['whole_law_holds'],'every registered earlier safeguard repaired');controls.append(row)
    a=dec(pe['matching_graphs'][2]['A']);b=dec(pe['matching_graphs'][2]['B'])
    _,_,bad=edge('new_equal_root_DELETE6',a,b,'D',6,True);controls.append(bad)
    ck((bad['source_values']['P'],bad['destination_values']['P'],bad['source_values']['R'],bad['destination_values']['R'],bad['delta_H'],bad['budget'])==(1,5,0,0,4,2),'new single-zig alignment-breaking failure')
    reflections=[]
    for row in controls:
        _,_,m=edge('reflection_'+row['label'],mir(dec(row['source_A'])),mir(dec(row['source_B'])),row['mode'],7-row['key'],True)
        ck((m['source_values']['H'],m['destination_values']['H'],m['a'],m['q'],m['z'])==(row['source_values']['H'],row['destination_values']['H'],row['a'],row['q'],row['z']),'reflection values and costs');reflections.append(m)
    prefix=pe['closed_witness']['word'][:5]
    ck(prefix==[['D',4],['D',6],['D',3],['D',6],['D',1]],'reuse fixed connector')
    word=prefix+[['K',1],['D',6]]+[['K',x] for x in range(1,7)]+[['K',x] for x in range(5,0,-1)]+[['K',2]]
    aa=dec(pe['closed_witness']['initial_A']);bb=dec(pe['closed_witness']['initial_B']);ia,ib=aa,bb;replay=[]
    for i,(mode,x) in enumerate(word):aa,bb,row=edge('closed_'+str(i),aa,bb,mode,x);replay.append(row)
    ck(aa==ia and bb==ib,'actual paired diagonal closure')
    ck(replay[6]['source_A']==raw(a) and replay[6]['source_B']==raw(b),'new counteredge physically reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck((At,Qt,Zt)==(20,0,12),'closed source totals')
    save('joint_alignment_certificate.json',{'date':'2026-10-31','controls':controls,'reflections':reflections,'matching_graphs':GRAPHS,
      'closed_witness':{'initial_A':raw(ia),'initial_B':raw(ib),'word':word,'failed_edge_index':6,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'all_size_new_family':{'n_min':3,'source_P':1,'destination_P':'n-1','source_R':0,'destination_R':0,'delta_H':'n-2','a':1,'violates_for':'n>=5'},
      'general_correction_necessary_difference':'R(T_n,R_n)-R(A_n,R_n)<=4-n',
      'excluded_class':'nonnegative joint corrections vanishing on every equal-root pair; not merely vanishing on A=B',
      'no_other_replay_H_values_claimed':True,'finite_potential_fits':0,'matching_solver_calls':0,'new_BFS_calls':0,
      'new_metric_graphs':0,'new_pair_graphs':0,'auxiliary_trees_enumerated':0})
    print(json.dumps({'controls':[{ 'label':r['label'],'H_source':r['source_values']['H'],'H_destination':r['destination_values']['H'],
      'R_source':r['source_values']['R'],'R_destination':r['destination_values']['R'],'a':r['a'],'q':r['q'],'budget':r['budget'],'holds':r['whole_law_holds']} for r in controls],
      'local_duals':len(GRAPHS),'closed_word':word,'totals':[At,Qt,Zt],'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()

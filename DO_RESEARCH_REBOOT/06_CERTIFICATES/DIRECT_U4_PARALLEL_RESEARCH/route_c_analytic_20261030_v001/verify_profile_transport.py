"""Exact controls for the analytic profile-transport identity; no potential fitting.

Whole-access controls: four prescribed fringe sizes, two branches and mirrors.
An exact formal arbitrary-fringe proof is supplied in RA01/RA02; finite controls
only verify the source wiring and algebra. All output paths are exclusive.
"""
from pathlib import Path
from collections import Counter,deque
import sys,json,hashlib,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P
from independent import splay as S

def ck(condition,detail):
    if not condition:raise AssertionError(detail)

def save(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)

def clean(poly):return {k:v for k,v in poly.items() if v}
def add(*terms):
    out=Counter()
    for coefficient,poly in terms:
        for k,v in poly.items():out[k]+=coefficient*v
    return clean(out)
def shift(poly,a=0,b=0):return {(i+a,j+b):v for (i,j),v in poly.items()}
def delta(poly,axis,amount):return add((1,shift(poly,amount if axis=='A' else 0,amount if axis=='B' else 0)),(-1,poly))
def encode(poly):return [[i,j,v] for (i,j),v in sorted(poly.items()) if v]
def mono(a,b):return {(a,b):1}
def decode(raw):return S.LEAF if raw is None else S.node(raw[0],decode(raw[1]),decode(raw[2]))
def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]

def pointer(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],pointer(t[2]),pointer(t[3]))
    if p['l'] is not None:p['l']['p']=p
    if p['r'] is not None:p['r']['p']=p
    return p
def fromptr(t):return S.LEAF if t is None else S.node(t['k'],fromptr(t['l']),fromptr(t['r']))
def pdepth(root):
    out={};stack=[(root,0)]
    while stack:
        t,d=stack.pop()
        if t is None:continue
        out[t['k']]=d;stack.extend([(t['l'],d+1),(t['r'],d+1)])
    return out
def keyset(root):
    if root is None:return set()
    return {root['k']}|keyset(root['l'])|keyset(root['r'])
def profile(da,db,keys=None):
    return clean(Counter((da[x],db[x]) for x in (da if keys is None else keys)))
def hist(a,b):
    da={x:S.lookup(a,x)[1] for x in S.inorder(a)}
    db={x:S.lookup(b,x)[1] for x in S.inorder(b)}
    return profile(da,db)

def controlled_access(A,B,mode,x):
    pa=pointer(A);pb=pointer(B);steps=[];da0=pdepth(pa);db0=pdepth(pb)
    for axis in ('A','B'):
        if axis=='B' and mode=='D':continue
        root=pa if axis=='A' else pb
        _,path=P._depth_to(root,x);node=path[-1]
        while node['p'] is not None:
            p=node['p'];g=p['p'];da=pdepth(pa);db=pdepth(pb);before=profile(da,db)
            def singleton(k):return mono(da[k],db[k])
            def region(q):return profile(da,db,keyset(q))
            def change(q,amount):return delta(q,axis,amount)
            if g is None:
                left=p['l'] is node;pat='ZL' if left else 'ZR'
                outer=region(node['l'] if left else node['r'])
                far=region(p['r'] if left else p['l'])
                down=add((1,singleton(node['k'])),(1,outer))
                up=add((1,singleton(p['k'])),(1,far))
                prediction=add((1,change(down,-1)),(1,change(up,1)))
                if left:P._rot_right(p)
                else:P._rot_left(p)
            else:
                if p['l'] is node and g['l'] is p:
                    pat='LL';L=region(node['l']);M=region(node['r']);R=region(p['r']);F=region(g['r'])
                    prediction=add((1,change(add((1,singleton(node['k'])),(1,L)),-2)),(1,change(M,-1)),(1,change(R,1)),(1,change(add((1,singleton(g['k'])),(1,F)),2)))
                    P._rot_right(g);P._rot_right(p)
                elif p['r'] is node and g['r'] is p:
                    pat='RR';L=region(g['l']);M=region(p['l']);R=region(node['l']);F=region(node['r'])
                    prediction=add((1,change(add((1,singleton(node['k'])),(1,F)),-2)),(1,change(R,-1)),(1,change(M,1)),(1,change(add((1,singleton(g['k'])),(1,L)),2)))
                    P._rot_left(g);P._rot_left(p)
                elif p['r'] is node and g['l'] is p:
                    pat='LR';XL=region(node['l']);XR=region(node['r']);F=region(g['r'])
                    prediction=add((1,change(singleton(node['k']),-2)),(1,change(add((1,singleton(g['k'])),(1,F)),1)),(1,change(add((1,XL),(1,XR)),-1)))
                    P._rot_left(p);P._rot_right(g)
                else:
                    pat='RL';XL=region(node['l']);XR=region(node['r']);F=region(g['l'])
                    prediction=add((1,change(singleton(node['k']),-2)),(1,change(add((1,singleton(g['k'])),(1,F)),1)),(1,change(add((1,XL),(1,XR)),-1)))
                    P._rot_right(p);P._rot_left(g)
            root=node
            while root['p'] is not None:root=root['p']
            if axis=='A':pa=root
            else:pb=root
            after=profile(pdepth(pa),pdepth(pb));actual=add((1,after),(-1,before))
            ck(actual==prediction,('formal transport/source step',axis,pat,encode(actual),encode(prediction)))
            steps.append({'axis':axis,'pattern':pat,'actual_histogram_change':encode(actual),'formula_change':encode(prediction)})
    ap,ae=S.trace(A,x)
    if mode=='K':bp,be=S.trace(B,x)
    else:bp=B;be=[]
    ck(fromptr(pa)==ap and fromptr(pb)==bp,'independent frame endpoints')
    ck([z['pattern'] for z in steps if z['axis']=='A']==[('ZL' if e[3]=='L' else 'ZR') if e[0]=='ZIG' else e[0] for e in ae],'A trace')
    ck([z['pattern'] for z in steps if z['axis']=='B']==[('ZL' if e[3]=='L' else 'ZR') if e[0]=='ZIG' else e[0] for e in be],'B trace')
    a=len(ae);q=sum(e[0]!='ZIG' for e in be)
    return {'mode':mode,'key':x,'source_A':serial(A),'source_B':serial(B),
            'destination_A':serial(ap),'destination_B':serial(bp),'dA':da0[x],
            'dB':db0[x] if mode=='K' else None,'a':a,'q':q,'signed_weight':2*a-q,
            'source_H':encode(hist(A,B)),'destination_H':encode(hist(ap,bp)),
            'source_roots':[A[1],B[1]],'destination_roots':[ap[1],bp[1]],'StepEvs':steps}

def vine(keys,left=False):
    t=S.LEAF
    for x in (keys if left else reversed(keys)):
        t=S.node(x,t,S.LEAF) if left else S.node(x,S.LEAF,t)
    return t

def family(m):
    keys=list(range(5,m+5));ca=S.balanced(keys);cb=vine(keys,left=True)
    c5=m+5;c6=m+6;leaf=S.LEAF
    A=S.node(c6,S.node(2,S.node(1,leaf,leaf),S.node(3,leaf,S.node(4,leaf,S.node(c5,ca,leaf)))),leaf)
    low=S.node(1,leaf,S.node(2,leaf,S.node(3,leaf,leaf)))
    high=S.node(3,S.node(2,S.node(1,leaf,leaf),leaf),leaf)
    BL=S.node(c6,S.node(c5,S.node(4,low,cb),leaf),leaf)
    BR=S.node(c6,S.node(c5,S.node(4,high,cb),leaf),leaf)
    return A,BL,BR,keys

def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))

def formulas(C):
    pre=add((1,mono(0,0)),(1,mono(1,4)),(1,mono(2,3)),(1,mono(2,5)),(1,mono(3,2)),(1,mono(4,1)),(1,C))
    L=add((1,mono(0,0)),(1,mono(1,1)),(1,mono(1,2)),(1,mono(2,3)),(1,mono(3,2)),(1,mono(4,1)),(1,C))
    R=add((1,mono(0,0)),(1,mono(1,1)),(1,mono(1,2)),(1,mono(2,2)),(1,mono(3,3)),(1,mono(4,1)),(1,shift(C,b=1)))
    return pre,L,R

def tree_word(start,goal):
    # Fixed six-key reachability witness only; no pair graph and no potential fit.
    if start==goal:return []
    parent={start:None};queue=deque([start]);found=False;keys=S.inorder(start)
    while queue and not found:
        t=queue.popleft()
        for x in keys:
            v=S.trace(t,x)[0]
            if v not in parent:
                parent[v]=(t,x)
                if v==goal:found=True;break
                queue.append(v)
    ck(found,'six-key source tree reachability')
    word=[];v=goal
    while parent[v] is not None:
        t,x=parent[v];word.append(x);v=t
    return word[::-1]

def closed_control(A,B,x):
    Ap=S.trace(A,x)[0];Bp=S.trace(B,x)[0]
    prefix=[('D',k) for k in tree_word(B,A)]
    word=prefix+[('K',x)]+[('D',k) for k in tree_word(Ap,Bp)]+[('K',k) for k in tree_word(Bp,B)]
    a=b=B;rows=[]
    for mode,key in word:
        r=controlled_access(a,b,mode,key);rows.append(r);a=decode(r['destination_A']);b=decode(r['destination_B'])
    ck(a==b==B,'complete closed physical control')
    marked=rows[len(prefix)]
    ck(marked['source_A']==serial(A) and marked['source_B']==serial(B) and marked['a']==1 and marked['q']==2,'claimed zero helper realized inside closed word')
    return {'initial_A':serial(B),'initial_B':serial(B),'word':word,'zero_helper_index':len(prefix),
            'full_replay':rows,'A':sum(r['a'] for r in rows),'Q_B':sum(r['q'] for r in rows),
            'paired_closure':True,'reachability_source':'explicit six-key source replay; BFS used only to locate connecting request words'}

def main():
    inputs=['python/liquidity/legacy_embedding.py','python/independent/splay.py','scripts/wp6_jointupdate.py','scripts/wp6_symtable.py',
            'audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md','DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
            'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_run_20261030_v001/finite_summary_potential.json',
            'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
            'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
            'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    pins={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs}
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    save('entry_source_pins.json',{'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins,'tracked_status':git('status','--porcelain=v1','--untracked-files=no')})
    old=json.loads((ROOT/inputs[6]).read_text(encoding='utf-8'));lookup={tuple(f):p for f,p in zip(old['encoded_class_features'],old['labels'])}
    records=[];patterns=Counter();primitive_checks=0
    for m in (0,1,2,5):
        a,l,r,carrier=family(m);pre,L,R=formulas(hist(a,l) if False else {})
        da={k:S.lookup(a,k)[1] for k in S.inorder(a)};db={k:S.lookup(l,k)[1] for k in S.inorder(l)}
        C=profile(da,db,carrier);H0,HL,HR=formulas(C)
        ck(hist(a,l)==hist(a,r)==H0,('same global H',m))
        difference=add((1,shift(add((1,C),(1,mono(3,2)),(-1,mono(2,2))),b=1)),(-1,add((1,C),(1,mono(3,2)),(-1,mono(2,2)))))
        ck(add((1,HR),(-1,HL))==difference,'factorized symbolic difference')
        for reflected in (False,True):
            n=m+6;aa=mirror(a,n) if reflected else a;bb=[mirror(l,n),mirror(r,n)] if reflected else [l,r];x=n-1 if reflected else 2
            pair=[]
            for branch,b,pred in zip(('L','R'),bb,(HL,HR)):
                rec=controlled_access(aa,b,'K',x)
                ck((rec['dA'],rec['dB'],rec['a'],rec['q'],rec['signed_weight'])==(1,4,1,2,0),'zero-weight access costs')
                ck(rec['source_H']==encode(H0) and rec['destination_H']==encode(pred),'arbitrary-fringe formula in source control')
                rec.update(fringe_nodes=m,branch=branch,reflected=reflected,fringe_profile=encode(C))
                if m==1:
                    def value(aa0,bb0):
                        aa0=decode(aa0);bb0=decode(bb0);keys=S.inorder(aa0)
                        key=(aa0[1],bb0[1],*sorted(7*S.lookup(aa0,k)[1]+S.lookup(bb0,k)[1] for k in keys))
                        return lookup[key]
                    ps=value(rec['source_A'],rec['source_B']);pt=value(rec['destination_A'],rec['destination_B'])
                    ck(ps>=pt,'inherited Phi7 zero-helper inequality')
                    rec['inherited_Phi7']={'source':ps,'destination':pt,'drop':ps-pt,'table_refitted':False}
                patterns.update(s['pattern'] for s in rec['StepEvs']);primitive_checks+=len(rec['StepEvs']);pair.append(rec)
            ck(pair[0]['source_H']==pair[1]['source_H'] and pair[0]['source_roots']==pair[1]['source_roots'] and pair[0]['key']==pair[1]['key'],'exact same summary/action inputs')
            ck(pair[0]['destination_H']!=pair[1]['destination_H'],'different successor histograms')
            records.extend(pair)
    save('profile_transport_controls.json',{'status':'PASS','whole_access_controls':len(records),'source_StepEv_identities_checked':primitive_checks,'pattern_counts':dict(patterns),
        'fringe_sizes':[0,1,2,5],'mirrors_checked':True,'potential_fits':0,'records':records,
        'universal_claim_basis':'structural arbitrary-fringe proof in RA01/RA02; these controls only check implementation/algebra'})
    a,l,r,_=family(0);closures=[closed_control(a,b,2) for b in (l,r)]
    save('six_key_closed_controls.json',{'status':'PASS','controls':closures,'finite_fitting_performed':False,'physical_CoarseDouble_counterexample_claimed':False})
    changes=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    save('integrity.json',{'status':'PASS' if not changes and not git('status','--porcelain=v1','--untracked-files=no') else 'FAIL',
        'source_files_compared':len(pins),'source_changes':changes,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'Stage11G_modified':False})
    print(json.dumps({'status':'PASS','whole_access_controls':len(records),'StepEv_identity_checks':primitive_checks,'patterns':dict(patterns),
        'closed_physical_controls':len(closures),'closed_costs':[{'A':c['A'],'Q_B':c['Q_B']} for c in closures],
        'all_size_potential_proved':False,'larger_finite_fits':0},indent=2))

if __name__=='__main__':main()

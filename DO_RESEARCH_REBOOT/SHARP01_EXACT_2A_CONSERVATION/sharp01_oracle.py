"""SHARP-01 v1: exact complete pointer trees; original occurrence identities.

No old engine is imported. Immutable verification is a separate module.
Physical states use the original sorted key list and child dictionaries.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
import hashlib
import json

VERSION = 'SHARP01-1.0'

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

class Tree:
    def __init__(self, state):
        self.root = state['root']
        self.ch = {int(k): list(v) for k,v in state['children'].items()}
        self.keys = sorted(self.ch)
        self.par = {k: None for k in self.keys}
        for k,cs in self.ch.items():
            for c in cs:
                if c is not None:
                    assert c in self.par and self.par[c] is None
                    self.par[c] = k
        self.validate()

    def validate(self):
        if not self.keys:
            assert self.root is None
            return
        assert self.par[self.root] is None
        seen=set(); stack=[(self.root,None,None)]
        while stack:
            k,lo,hi=stack.pop()
            assert k not in seen and (lo is None or lo<k) and (hi is None or k<hi)
            seen.add(k)
            for s,c in enumerate(self.ch[k]):
                if c is not None:
                    assert self.par[c]==k
                    stack.append((c,lo if s==0 else k,k if s==0 else hi))
        assert seen==set(self.keys)

    def state(self):
        return {'root':self.root,'children':{str(k):list(self.ch[k]) for k in self.keys}}

    def path(self,x):
        ans=[]; k=self.root
        while k!=x:
            assert k is not None
            ans.append(k); k=self.ch[k][int(x>k)]
        return ans+[x]

    def subtree(self,k):
        ans=[]; todo=[] if k is None else [k]
        while todo:
            z=todo.pop(); ans.append(z)
            todo.extend(c for c in self.ch[z] if c is not None)
        return sorted(ans)

    def labels(self,carrier):
        bits={k:1<<i for i,k in enumerate(self.keys) if k in carrier}
        labs={}; stack=[] if self.root is None else [(self.root,False)]
        while stack:
            k,done=stack.pop()
            if done:
                l,r=self.ch[k]; labs[k]=bits.get(k,0)|labs.get(l,0)|labs.get(r,0)
            else:
                stack.append((k,True)); stack.extend((c,False) for c in self.ch[k] if c is not None)
        return set(labs.values())-{0}

    def edges(self):
        return {(p,c,s) for p,cs in self.ch.items() for s,c in enumerate(cs) if c is not None}

    def rotate(self,u,s):
        v=self.ch[u][s]; assert v is not None
        ext=self.par[u]; middle=self.ch[v][1-s]
        removed=[u, [v]+self.subtree(self.ch[v][s])]
        added=[v, [u]+self.subtree(self.ch[u][1-s])]
        minus={(u,v,s)}; plus={(v,u,1-s)}
        if ext is None:
            self.root=v
        else:
            es=int(self.ch[ext][1]==u)
            assert self.ch[ext][es]==u
            minus.add((ext,u,es)); plus.add((ext,v,es)); self.ch[ext][es]=v
        self.par[v]=ext; self.ch[u][s]=middle
        if middle is not None:
            self.par[middle]=u
            minus.add((v,middle,1-s)); plus.add((u,middle,s))
        self.ch[v][1-s]=u; self.par[u]=v
        return {'pivot':u,'promoted':v,'side':s,'external':ext,'middle':middle,
                'edges_removed':sorted(minus),'edges_added':sorted(plus),
                'ancestry_removed':removed,'ancestry_added':added}

def plain_splay(tree,x):
    while tree.par[x] is not None:
        p=tree.par[x]; g=tree.par[p]; s=int(x>p)
        if g is None: tree.rotate(p,s)
        else:
            z=int(p>g)
            if s==z: tree.rotate(g,z); tree.rotate(p,s)
            else: tree.rotate(p,s); tree.rotate(g,z)

class Replay:  # Constructor compatibility for the pinned source formulas.
    plain_splay=staticmethod(plain_splay)

def vine(keys):
    ks=sorted(keys)
    return {'root':ks[0] if ks else None,'children':{str(k):[None,ks[i+1] if i+1<len(ks) else None] for i,k in enumerate(ks)}}

def geometry(a,b,carrier):
    # DFS computes exact complete depths and ancestry, with no projected edges.
    def anc(t):
        ans={}; depths={}; todo=[] if t.root is None else [(t.root,frozenset())]
        while todo:
            x,aa=todo.pop(); ans[x]=aa; depths[x]=len(aa)
            todo.extend((c,aa|{x}) for c in t.ch[x] if c is not None)
        return ans,depths
    aa,da=anc(a); ab,db=anc(b)
    diff=[db[k]-da[k] for k in a.keys]
    return {'edges':len(b.edges()-a.edges()),
            'ancestry':sum(len(ab[k]-aa[k]) for k in a.keys),
            'SET':len(b.labels(carrier)-a.labels(carrier)),
            'depth_sum':sum(max(0,x) for x in diff),
            'depth_max':max([0]+diff)}

def replay(source,features=True):
    a,b=Tree(source['initial_A']),Tree(source['initial_B'])
    assert a.keys==b.keys
    diag=source.get('diagonal_initial',source['initial_A'])
    ra,rb=Tree(diag),Tree(diag)
    for tag,x in source.get('reaching_prefix',[]):
        assert tag in ('D','K'); plain_splay(ra,x)
        if tag=='K': plain_splay(rb,x)
    assert ra.state()==a.state() and rb.state()==b.state(), (source['name'],'unreachable saved pair')
    probe=Tree(b.state()); genuine=set()
    for tag,x in source['operations']:
        if tag=='K':
            if probe.root!=x:genuine.add(x)
            plain_splay(probe,x)
    carrier=set()
    for x in genuine:carrier.update(b.path(x))
    states={}; state_lookup={}
    def save(t):
        st=t.state(); h=digest(st)
        if h not in state_lookup:
            sid=f'T{len(states)}'; states[sid]=st; state_lookup[h]=sid
        return state_lookup[h]
    events=[]; steps=[]; rows=[]; costs=Counter({k:0 for k in ('A','Q','VA','ZB','KB')})
    def splay(t,x,actor,op):
        j=0
        while t.par[x] is not None:
            j+=1; p=t.par[x]; g=t.par[p]; s=int(x>p); z=None if g is None else int(p>g)
            case='ZIG' if g is None else ('R' if z else 'L')+('R' if s else 'L')
            rotations=[(p,s)] if g is None else ([(g,z),(p,s)] if s==z else [(p,s),(g,z)])
            ids=[]
            for bit,(u,side) in enumerate(rotations):
                old=t.labels(carrier); other=(b if actor=='A' else a).labels(carrier)
                info=t.rotate(u,side); new=t.labels(carrier)
                sign=len((old-new)&other)-len((new-old)&other) if actor=='A' else len(new-other)-len(old-other)
                if actor=='B':assert sign in (-1,0)
                eid=[actor,op,j,bit]; ids.append(eid)
                events.append({'id':eid,'target':x,'case':case,'SET_sign':sign,
                               'SET_removed':sorted(old-new),'SET_added':sorted(new-old),**info})
            steps.append({'id':[actor,op,j],'case':case,'real_rotation_ids':ids,
                          'virtual_companion':actor=='A' and case=='ZIG'})
    initial=[save(a),save(b)]
    for op,(tag,x) in enumerate(source['operations'],1):
        assert tag in ('K','D')
        pre=[save(a),save(b)]; ap=a.path(x); bp=b.path(x)
        cost=(len(ap))//2; q=(len(bp)-1)//2 if tag=='K' else 0
        begin=len(events); sbegin=len(steps)
        splay(a,x,'A',op); amid=len(events)
        if tag=='K':splay(b,x,'B',op)
        post=[save(a),save(b)]
        costs['A']+=cost; costs['Q']+=q; costs['VA']+=(len(ap)-1)%2
        costs['ZB']+=(len(bp)-1)%2 if tag=='K' else 0
        costs['KB']+=int(tag=='K' and len(bp)>1)
        row={'operation_id':op,'tag':tag,'target':x,'pre':pre,'post':post,
             'A_path':ap,'B_path':bp,'a':cost,'q':q,
             'event_range':[begin,len(events)],'A_end_event':amid,'step_range':[sbegin,len(steps)]}
        rows.append(row)
    assert [save(a),save(b)]==initial,(source['name'],'not exactly paired closed')
    assert sum(e['id'][0]=='A' for e in events)==2*costs['A']-costs['VA']
    assert costs['KB']<=costs['A']
    pa=sum(e['id'][0]=='A' and e['SET_sign']==1 for e in events)
    na=sum(e['id'][0]=='A' and e['SET_sign']==-1 for e in events)
    db=sum(e['id'][0]=='B' and e['SET_sign']==-1 for e in events)
    assert db==pa-na
    keeps=[i for i,r in enumerate(rows) if r['tag']=='K']; gaps=[]
    for i,t in enumerate(keeps):
        prev=keeps[i-1]; inds=[]; k=(prev+1)%len(rows)
        while True:
            inds.append(k)
            if k==t:break
            k=(k+1)%len(rows)
        start=rows[prev]['post']; end=rows[t]['post']; x=rows[t]['target']
        ga,gb=Tree(states[start[0]]),Tree(states[start[1]])
        ap,bp=ga.path(x),gb.path(x)
        H=sum(rows[k]['a'] for k in inds); p=len(ap)//2; q=(len(bp)-1)//2
        u=max(q-2*p,0); c=2*H-min(q,2*p); d=q-2*H
        assert p<=H and c>=0 and u-c==d and q==rows[t]['q']
        ac=set(ap[:-1]); bc=set(bp[:-1]); pref=0
        for av,bv in zip(ap,bp):
            if av!=bv:break
            pref+=1
        gap={'gap_index':i+1,'previous_KEEP_operation_id':rows[prev]['operation_id'],
             'previous_target':rows[prev]['target'],'KEEP_operation_id':rows[t]['operation_id'],
             'target':x,'operation_ids':[rows[k]['operation_id'] for k in inds],
             'DELETE_operation_ids':[rows[k]['operation_id'] for k in inds if rows[k]['tag']=='D'],
             'start':start,'end':end,'A_path':ap,'B_path':bp,'dA':len(ap)-1,'dB':len(bp)-1,
             'H':H,'p':p,'q':q,'u':u,'c':c,'d':d,'preparation_capacity':2*(H-p),
             'baseline_capacity':max(2*p-q,0),'B_only_ancestors':sorted(bc-ac),
             'A_only_ancestors':sorted(ac-bc),'common_path_prefix_length':pref,
             'target_LCA_in_A_of_B_path':min(bp,key=lambda v:len(ga.path(v))),
             'target_LCA_in_B_of_A_path':min(ap,key=lambda v:len(gb.path(v))),
             'A_StepEv_ids':[s['id'] for k in inds for s in steps[slice(*rows[k]['step_range'])] if s['id'][0]=='A'],
             'B_double_ids':[s['id'] for s in steps[slice(*rows[t]['step_range'])] if s['id'][0]=='B' and s['case']!='ZIG'],
             'B_terminal_zig_ids':[s['id'] for s in steps[slice(*rows[t]['step_range'])] if s['id'][0]=='B' and s['case']=='ZIG']}
        if features:
            gap['Phi_start']=geometry(ga,gb,carrier)
            gap['Phi_end']=geometry(Tree(states[end[0]]),Tree(states[end[1]]),carrier)
        gaps.append(gap)
    U=sum(g['u'] for g in gaps); C=sum(g['c'] for g in gaps)
    if keeps:
        assert sorted(k for g in gaps for k in g['operation_ids'])==list(range(1,len(rows)+1))
        assert sum(g['H'] for g in gaps)==costs['A'] and sum(g['q'] for g in gaps)==costs['Q']
        assert U-C==costs['Q']-2*costs['A']
    else:assert costs['Q']==0 and not gaps  # A work is outside a KEEP partition.
    if costs['A']==0:assert costs['Q']==0
    summary={'name':source['name'],'family':source.get('family','control'),'n':len(a.keys),
             'operations':len(rows),'genuine_support':sorted(genuine),'carrier':sorted(carrier),
             **dict(costs),'U':U,'C':C,'Delta':costs['Q']-2*costs['A'],
             'no_KEEP_unpartitioned_A':costs['A'] if not keeps else 0,
             'U_over_A':str(Fraction(U,costs['A'])) if costs['A'] else None,
             'C_over_A':str(Fraction(C,costs['A'])) if costs['A'] else None,
             'Q_over_A':str(Fraction(costs['Q'],costs['A'])) if costs['A'] else None,
             'positive_excess_gaps':sum(g['u']>0 for g in gaps),
             'positive_net_gaps':sum(g['d']>0 for g in gaps),
             'neutral_changed_gaps':sum(g['d']==0 and g['start']!=g['end'] for g in gaps),
             'PA':pa,'NA':na,'DB':db,'initial':initial,'end':initial,'closed':True}
    return {'summary':summary,'source':source,'states':states,'operations':rows,'steps':steps,'events':events,'gaps':gaps}

def canonical_gap(g,ledger):
    # Original IDs are supplied by source tags through a cyclic re-cut.
    ids=ledger['source'].get('original_operation_ids',list(range(1,len(ledger['operations'])+1)))
    ans={k:v for k,v in g.items() if k not in ('gap_index','start','end','Phi_start','Phi_end','A_StepEv_ids','B_double_ids','B_terminal_zig_ids')}
    for k in ('KEEP_operation_id','previous_KEEP_operation_id'):ans[k]=ids[ans[k]-1]
    for k in ('operation_ids','DELETE_operation_ids'):ans[k]=[ids[v-1] for v in ans[k]]
    ans['start']=[ledger['states'][sid] for sid in g['start']]
    ans['end']=[ledger['states'][sid] for sid in g['end']]
    ans['physical_events']=[]
    for op in g['operation_ids']:
        for e in ledger['events'][slice(*ledger['operations'][op-1]['event_range'])]:
            ee=dict(e); ee['id']=[e['id'][0],ids[e['id'][1]-1],*e['id'][2:]]
            ans['physical_events'].append(ee)
    return digest(ans)

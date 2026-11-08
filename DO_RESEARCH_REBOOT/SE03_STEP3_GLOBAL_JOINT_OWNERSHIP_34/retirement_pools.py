"""C34 candidate physical layer. Reads accepted source snapshots; no splay.
This is not a verifier of the full original source-license/Bank25 system.
"""
import collections,hashlib,json
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(t):return tuple(map(freeze,t)) if isinstance(t,list) else t
def isnode(t):return isinstance(t,(tuple,list)) and len(t)==3 and isinstance(t[0],(int,float))
def ancestors(t,x):
    a=[]
    while isnode(t) and t[0]!=x:a.append(t[0]);t=t[1 if x<t[0] else 2]
    assert isnode(t) and t[0]==x
    return frozenset(a)
def core(t,M):
    if not isnode(t):return set()
    c=core(t[1],M)|core(t[2],M)
    if c or t[0] in M:c.add(t[0])
    return c
def mp(z):return {tuple(x['demand']):tuple(x['unit']) for x in z}
def pairs(z):return [{'demand':d,'unit':u} for d,u in sorted(z.items())]
def normalize(z,style):
    rows=[]
    for r in (z['period_rows'] if style in ('c33','frame') else z['rows']):
        if style=='c33':
            row={'t':r['t'],'mode':r['kind'],'x':r['key'],'a':r['a'],'q':r['qF'],'A0':r['A_before'],'A1':r['A_after'],'B0':r['BF_before'],'B1':r['BF_after']}
        elif style=='frame':
            a=z['A_word_source_rows'][r['word_index']];assert a['key']==r['key'] and a['H']==r['H']
            row={'t':r['absolute_t'],'mode':r['kind'],'x':r['key'],'a':r['H'],'q':r['QF'],'A0':a['before'],'A1':a['after'],'B0':r['BF_before'],'B1':r['BF_after']}
        else:row={'t':r['occurrence'],'mode':r['mode'],'x':r['target'],'a':r['a'],'q':r['qF'],'A0':r['before'][0],'A1':r['after'][0],'B0':r['before'][1],'B1':r['after'][1]}
        row={k:freeze(v) for k,v in row.items()};row['gen']=row['mode']=='K' and row['B0'][0]!=row['x'];rows.append(row)
    assert len({r['t'] for r in rows})==len(rows)
    assert rows[0]['A0']==rows[-1]['A1'] and rows[0]['B0']==rows[-1]['B1']
    assert all(a['A1']==b['A0'] and a['B1']==b['B0'] for a,b in zip(rows,rows[1:]))
    assert all(r['a']>=0 and (r['a']>0 or r['A0']==r['A1']) for r in rows)
    return rows
def cases():
    C=B/'SOURCE_JOINT_REPAIR_03'
    specs=[('C33_36',C/'actual_monotone_return_source.json','c33',C/'independent_source_audit.json','input_sha256',None),
      ('frame13',B/'core13_framed_activation_closed_source.json','frame',B/'framed_return_and_core13_independent_audit.json','input_sha256',None),
      ('W199',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/aligned_source_and_owners.json','triple',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/independent_audit2.json','input_sha256','final_full_allocation'),
      ('W459',P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/catchment_forcing_countercertificate.json','triple',P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/family_independent_audit.json','sha256','current_complete_a'),
      ('N85',P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json','triple',P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/independent_audit.json','input_sha256',None)]
    result=[]
    for name,path,style,receipt,field,ownerfield in specs:
        z=json.loads(path.read_text());rec=json.loads(receipt.read_text());hashes=rec[field]
        expected=next((v for k,v in hashes.items() if str(k).replace('\\','/').endswith('/'+path.name) or k==path.name),None)
        assert expected==pin(path)
        data={'name':name,'path':str(path),'receipt':str(receipt),'input_sha256':pin(path),'receipt_sha256':pin(receipt),'rows':normalize(z,style),'current_owner':mp(z[ownerfield]) if ownerfield else None}
        if name=='C33_36':
            op=C/'actual_auxiliary_owner_extension.json';a=json.loads(op.read_text());data.update(current_owner=mp(a['full_allocation']),archive_prior=mp(a['old_canonical_effective_a0']),accepted_additions=mp(a['new_actual_pairs']),owners_path=str(op),owners_sha256=pin(op))
        result.append(data)
    return result

def build(rows):
    M={r['x'] for r in rows if r['gen']};r=len(M);assert r>=7
    cores={tuple(sorted(core(z['B0'],M))) for z in rows};assert len(cores)==1
    size=len(next(iter(cores)))
    if size!=2*r-1:return {'scope':'NOT_MAXIMAL_CORE','r':r,'core':size}
    n=len(rows);a0=[{x:ancestors(z['A0'],x) for x in M} for z in rows];a1=[{x:ancestors(z['A1'],x) for x in M} for z in rows]
    units_by_t={z['t']:{(z['t'],j,b) for j in range(1,z['a']+1) for b in (0,1)} for z in rows}
    ends=[i for i,z in enumerate(rows) if z['gen']];macros=[];h0={};D=set();U=set().union(*units_by_t.values());neigh={};dm={}
    for mi,e in enumerate(ends):
        prev=ends[mi-1];ix=list(range(prev+1,e+1)) if prev<e else list(range(prev+1,n))+list(range(e+1))
        ownops={rows[i]['t'] for i in ix};own=set().union(*(units_by_t[t] for t in ownops));target=rows[e]['x'];ga=sorted(ancestors(rows[e]['B0'],target)&M)
        Q=rows[e]['q'];assert len(ga)==Q and len(own)//2>=1
        retire=set();proof=[];first_counts=collections.Counter()
        for g in ga:
            j=(e-1)%n
            while not (rows[j]['gen'] and rows[j]['x']==g):j=(j-1)%n;assert j!=e
            born=rows[j]['t'];j=(j+1)%n;loss=[]
            while True:
                if g in a0[j][target] and g not in a1[j][target]:loss.append(rows[j]['t']);assert rows[j]['a']>0
                if j==e:break
                j=(j+1)%n
            assert loss;first_counts[loss[0]]+=1;retire.update(loss);proof.append({'g':g,'born_after':born,'all_retiring_operations':loss})
        by={z['t']:z for z in rows};assert all(count<=2*by[t]['a'] for t,count in first_counts.items())
        T=set().union(*(units_by_t[t] for t in retire)) if retire else set();N=own|T;assert len(T)>=Q
        dd=[(rows[e]['t'],k) for k in range(1,Q+1)];uu=[(rows[i]['t'],j,b) for i in ix for j in range(1,rows[i]['a']+1) for b in (0,1)]
        h0.update(zip(dd,uu));D.update(dd)
        for d in dd:neigh[d]=N;dm[d]=mi
        macros.append({'index':mi,'end':rows[e]['t'],'target':target,'H':len(own)//2,'Q':Q,'own_operations':sorted(ownops),'retiring_operations':sorted(retire),'retirement_proof':proof,'T':sorted(T),'N':sorted(N),'demands':dd})
    assert sum(m['Q'] for m in macros)==len(D) and len(D)+len(U)<=2000000 and sum(len(x) for x in neigh.values())<=5000000
    return {'scope':'MAXIMAL_CORE','r':r,'core':size,'M':sorted(M),'macros':macros,'D':D,'U':U,'h0':h0,'N':neigh,'dm':dm}

def cover(model,fixed=None,free_allowed=None):
    D,U,N=model['D'],model['U'],model['N'];fixed=fixed or {};assert set(fixed)<=D and len(set(fixed.values()))==len(fixed) and set(fixed.values())<=U
    allowed=U if free_allowed is None else set(fixed.values())|set(free_allowed)
    J={d:((N[d]&allowed)|({fixed[d]} if d in fixed else set())) for d in D}
    match=dict(fixed);iv={u:d for d,u in match.items()}
    def visit(d,seen):
        for u in sorted(J[d]):
            if u in seen:continue
            seen.add(u);old=iv.get(u)
            if old is None or visit(old,seen):match[d]=u;iv[u]=d;return True
        return False
    for d in sorted(D-set(match)):visit(d,set())
    if set(match)==D:
        inv={u:d for d,u in fixed.items()};extra={};paths=[];seen=set()
        for p in sorted(D-set(fixed)):
            d=p;steps=[]
            while True:
                assert d not in seen;seen.add(d);u=match[d];assert u in N[d];steps.append((d,u))
                if u not in inv:extra[p]=u;paths.append({'root':p,'steps':steps,'terminal':u});break
                d=inv[u]
        assert len(set(extra.values()))==len(extra) and not set(extra.values())&set(fixed.values())
        return {'complete':True,'matching':pairs(match),'extra':pairs(extra),'paths':paths,'all_actual_old_owners_fixed':True}
    left=set(D-set(match));right=set();queue=collections.deque(left)
    while queue:
        d=queue.popleft()
        for u in J[d]:
            if u in right:continue
            right.add(u)
            if u in iv and iv[u] not in left:left.add(iv[u]);queue.append(iv[u])
    assert len(right)<len(left)
    coalition={model['dm'][d] for d in left};X={d for d in D if model['dm'][d] in coalition};NX=set().union(*(J[d] for d in X));assert len(NX)<len(X)
    return {'complete':False,'matched':len(match),'cut_demands':sorted(left),'cut_units':sorted(right),'cut_deficiency':len(left)-len(right),'macro_coalition':sorted(coalition),'macro_complete_demands':sorted(X),'macro_complete_neighborhood':sorted(NX),'macro_deficiency':len(X)-len(NX),'counterexample_scope':'candidate pooled physical layer only, not all original licenses or JIO34'}

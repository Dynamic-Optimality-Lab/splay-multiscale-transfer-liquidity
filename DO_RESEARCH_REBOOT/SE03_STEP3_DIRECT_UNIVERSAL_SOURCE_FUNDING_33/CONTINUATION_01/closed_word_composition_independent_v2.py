"""Independent original-source proof composition for source counterwords.
Every operation is either a checked G4 free-term identity, a literal identity,
or a fresh mutable ordinary-splay access. Full/erased B reuse the COMPLETE
independently checked ten-anchor source basis with the same rigid private gap.
"""
from audit_verify37 import fr,node,delete,renumber
def audit_word(z,native,G4,I,tick):
    private=z['candidate']['private_key'];assert private%2==1 and 2<private<20;physical=sorted(list(range(2,21,2))+[private]);rank={k:i+1 for i,k in enumerate(physical)};initial=fr(z['initial_common_A_B_BE']);T=list(map(fr,native['trees']));idx={t:i for i,t in enumerate(T)};core=idx[renumber(delete(initial,private)[0])]
    def normalize(t):
        def walk(v,hi):return 'F'+str(hi) if not node(v) else (v[0],walk(v[1],rank[v[0]]-1),walk(v[2],hi))
        return walk(t,11)
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,rank[v.key]-1),walk(v.right,hi))
        return walk(tree.root,11)
    Gtrees=list(map(fr,G4['trees']));current=initial;hulls=fresh=0;H=[]
    for modekey,row in zip(z['word'],z['A_word_source_rows']):
        mode,key=modekey;before,after=fr(row['before']),fr(row['after']);assert (row['mode'],row['key'])==(mode,key) and before==current
        if 'hull_keys' in row:
            keys=row['hull_keys'];assert keys==sorted(set(keys)) and len(keys)==4;kr={k:i+1 for i,k in enumerate(keys)};payload={}
            def compress(v,hi):
                if not node(v) or v[0] not in kr:payload[hi]=v;return 'F'+str(hi)
                k=kr[v[0]];return k,compress(v[1],k-1),compress(v[2],hi)
            c=compress(before,4);s=row['G4_before'];x=row['G4_key'];dest=row['G4_after'];assert c==Gtrees[s] and key==keys[x-1] and dest==G4['destinations'][s][x-1]
            v=before;depth=0
            while v[0]!=key:assert v[0] in kr;v=v[1 if key<v[0] else 2];depth+=1
            assert (depth+1)//2==row['H']==G4['H'][s][x-1]
            def expand(v):return payload[int(v[1:])] if not node(v) else (keys[v[0]-1],expand(v[1]),expand(v[2]))
            assert expand(Gtrees[dest])==after;hulls+=1
        elif before[0]==key:
            assert row['H']==0 and before==after
        else:
            tree=I.Tree(before);pa,ea=tree.access(key);assert len(ea)==(len(pa)+1)//2==row['H'] and shape(tree)==after;fresh+=1
        H.append(row['H']);current=after
    assert current==initial
    # All original A rows now compose exactly once to a closed word. The same
    # deterministic word has identical actual A rows on each period copy.
    def update(c,k):return (k,)+tuple(v for v in c if v!=k)
    F=E=core;cf=();ce=();period={r['absolute_t']:r for r in z['period_rows']};begin=end=None;AA=QF=QE=0;bf_instances=be_instances=0;genuine=set();packet=None;n=len(z['word'])
    for copy in range(z['source_prefix_copies']+z['period_copies']):
        assert F==core
        for j,(mode,key) in enumerate(z['word']):
            absolute=copy*n+j+1;f0,e0=F,E;cf0,ce0=cf,ce;q=qe=0
            if absolute==z['period'][0]:begin=(initial,F,E,cf,ce)
            if mode=='K':
                assert key%2==0;k=key//2;F=native['destination'][F][k-1];q=native['Q'][f0][k-1];bf_instances+=1
                if T[f0][0]!=k:cf=update(cf,k)
                if k!=10:
                    E=native['destination'][E][k-1];qe=native['Q'][e0][k-1];be_instances+=1
                    if T[e0][0]!=k:ce=update(ce,k)
            if absolute in period:
                r=period[absolute];assert (j,mode,key,H[j],q,qe,F,E)==(r['word_index'],r['kind'],r['key'],r['H'],r['QF'],r['QE'],r['BF_after'],r['BE_after']);assert (f0,e0)==(r['BF_before'],r['BE_before']);assert (cf0,cf,ce0,ce)==tuple(tuple(r[k]) for k in ('chartF_before','chartF_after','chartE_before','chartE_after'));AA+=H[j];QF+=q;QE+=qe
                if mode=='K' and k!=T[f0][0]:genuine.add(k)
            if absolute==z['packet_absolute_t']:
                e=z['candidate'];assert (key,H[j],q,f0,F)==(e['target_actual_key'],e['H'],e['Q'],e['source_B_core_index'],e['B_target_core_index']);assert fr(z['A_word_source_rows'][j]['before'])==normalize(fr(e['source_A'])) and fr(z['A_word_source_rows'][j]['after'])==normalize(fr(e['actual_A_target']));packet=True
            if absolute==z['period'][1]:end=(initial,F,E,cf,ce)
        assert F==core
    assert begin==end and packet and len(genuine)==10 and (AA,QF,QE)==(z['A_period'],z['QF_period'],z['QE_period'])
    return {'period':z['period'],'packet_t':z['packet_absolute_t'],'costs':[AA,QF,QE],'CD_margin':2*AA-QF,'new_fresh_A_accesses':fresh,'checked_G4_hull_instances':hulls,'checked_full_B_rigid_gap_instances':bf_instances,'checked_erased_B_rigid_gap_instances':be_instances,'genuine_KEEP_anchors':sorted(genuine),'all_original_operations_accounted_for':True,'all_A_B_BE_and_recency_seams_close':True}

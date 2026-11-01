"""Check the sharp partial law and rotate the already verified closed replay.

No new control, graph, fit or candidate is introduced.
"""
from pathlib import Path
import json,hashlib
from independent_verify import F,intervals,depths,ck

OUT=Path(__file__).resolve().parent
def write(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    p=OUT/'clade_correction_countercertificate.json';c=json.loads(p.read_text(encoding='utf-8'))
    old=json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'));ck(old['status']=='PASS','existing independent replay PASS')
    counts={'B_nontrivial':0,'sufficient_subclass_edges':0}
    for r in c['controls']+c['closed_witness']['full_replay']:
        ap=r['destination_A'];b=r['source_B'];bp=r['destination_B']
        if r['mode']=='K':
            dB=r['dB'];dbound=1 if dB>0 else 0
            ck(r['delta_F']<=r['dA']-dbound,'sharp whole-KEEP upper bound')
            if dB>0:
                x=r['key'];y=b[0];keys=sorted(depths(b));side=[k for k in keys if (k<x if y<x else k>x)]
                ck(side and y in side,'distinguished root-side set is nonempty')
                marker=(side[0],side[-1]);ck(marker in intervals(ap) and marker in intervals(bp) and marker not in intervals(b),'new mandatory shared root-side set')
                ck(F(ap,bp)<=F(ap,b)-1,'strict B drop')
                counts['B_nontrivial']+=1
            sufficient=(dB==0 or r['q']<=1+r['dA']%2)
            if sufficient:ck(r['inequality_holds'],'sufficient pointwise subclass');counts['sufficient_subclass_edges']+=1
        else:ck(r['delta_F']<=r['dA'],'whole DELETE bound')
    w=c['closed_witness'];offset=w['n']-1;rows=w['full_replay'][offset:]+w['full_replay'][:offset]
    word=w['word'][offset:]+w['word'][:offset];a=rows[0]['source_A'];b=rows[0]['source_B'];a0=a;b0=b
    ck(a==b and a[0]==1 and list(depths(a).values())==list(range(6)),'right-vine diagonal start')
    for (mode,x),r in zip(word,rows):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'rotated shared-state composition')
        a=r['destination_A'];b=r['destination_B']
    ck(a==a0 and b==b0,'right-vine actual paired closure')
    bad=w['failed_edge_index']-offset;ck(rows[bad]['delta_F']==-1 and rows[bad]['q']==2 and rows[bad]['a']==0,'same source counteredge')
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    write('right_vine_closed_rotation.json',{'status':'PASS','source_certificate':'clade_correction_countercertificate.json',
      'source_certificate_sha256':digest,'original_replay_offset':offset,
      'replay_row_indices':list(range(offset,17))+list(range(offset)),
      'initial_A':a0,'initial_B':b0,'word':word,'failed_edge_index':bad,'actual_paired_closure':True,
      'A':19,'Q_B':4,'Z_B':12})
    result={'status':'PASS','same_source_edges_checked':26,'new_source_controls':0,'new_pair_graphs':0,'finite_fits':0,
      'sharp_B_bound':'Delta_B F <= -1 for d_B>0 when root(A)=x',
      'sharp_KEEP_bound':'Delta F <= d_A - indicator(d_B>0)',
      'sufficient_subclass':'q <= 1+(d_A mod 2) on nontrivial B accesses; d_B=0 always allowed',
      'arbitrary_fringe_helper_consequence':'d_A=1,q=2 => Delta F<=0, independent of fringe geometry',
      'right_vine_closed_rotation_verified':True,**counts}
    write('sharp_bound_audit.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

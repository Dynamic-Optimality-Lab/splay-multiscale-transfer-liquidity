"""Shared independently rebuilt mathematical B bank, both outer helpers."""
import sys,json,time
from pathlib import Path
from collections import deque,Counter
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def mirror(t):return None if t is None else (8-t[0],mirror(t[2]),mirror(t[1]))
def strip(t,f):
    if t is None:return None
    k,l,r=t
    if k==f:assert l is None and r is None;return None
    return (k,strip(l,f),strip(r,f))
def main():
    out=BASE/'B_bank.json';assert not out.exists();start=time.process_time()
    m=json.loads(Path('DO_RESEARCH_REBOOT/M3_TWOGAP01/decoder_metadata.json').read_text());bt=list(map(R.frozen,m['B_trees']));bid={t:i for i,t in enumerate(bt)}
    assert len(bt)==4862 and set(bt)==set(R.bsts(tuple(range(9))))
    dest=[];depth=[];neg=[[] for t in bt];ind=[0]*4862;queries=0
    for b,t in enumerate(bt):
        ds=[];hs=[]
        for x in range(9):
            h=R.depth(t,x);bb=bid[R.splay(t,x)];ds.append(bb);hs.append(h);w=2-h//2;queries+=1
            if w<0:neg[b].append((bb,-w));ind[bb]+=1
        dest.append(ds);depth.append(hs)
    q=deque(b for b,n in enumerate(ind) if n==0);psi=[0]*4862;visited=0
    while q:
        b=q.popleft();visited+=1
        for bb,w in neg[b]:
            psi[bb]=max(psi[bb],psi[b]+w);ind[bb]-=1
            if ind[bb]==0:q.append(bb)
    assert visited==4862 and psi==m['psi'] and max(psi)==2
    kernels={}
    for gap,f in ((0,-1),(9,9)):
        rows=[]
        for b,t in enumerate(bt):
            pre=R.splay(R.insert(t,f),f);row=[]
            for x in range(9):
                h=R.depth(pre,x);dt=R.splay(pre,x);fn=R.find(dt,f);queries+=1
                row.append([bid[strip(dt,f)],4-h//2] if fn[1] is None and fn[2] is None else None)
            rows.append(row)
        kernels[str(gap)]=rows
    mirrors=[bid[mirror(t)] for t in bt]
    for b,bb in enumerate(mirrors):
        assert psi[b]==psi[bb]
        for x in range(9):
            assert depth[b][x]==depth[bb][8-x] and mirrors[dest[b][x]]==dest[bb][8-x]
            a=kernels['0'][b][x];c=kernels['9'][bb][8-x]
            assert (a is None)==(c is None)
            if a is not None:assert mirrors[a[0]]==c[0] and a[1]==c[1] and a[1]>=0
    result={'status':'INDEPENDENT_B_BANK_PASS','queries':queries,'trees':bt,'psi':psi,'destinations':dest,'depths':depth,
      'kernels':kernels,'mirror':mirrors,'core_debt_reflection_mismatches':0,'cpu_seconds':round(time.process_time()-start,3)}
    assert queries==131274 and result['cpu_seconds']<120
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k not in ('trees','psi','destinations','depths','kernels','mirror')},indent=2),flush=True)
if __name__=='__main__':main()

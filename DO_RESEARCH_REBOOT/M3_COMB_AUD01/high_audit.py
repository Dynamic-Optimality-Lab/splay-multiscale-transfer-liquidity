"""Independent source-normal-form generation and original-DAG partial evaluation."""
import sys,json,time,itertools,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BState,BTrace,b_splay_event,b_single_rot
BASE=Path('DO_RESEARCH_REBOOT/M3_COMB_AUD01')

def geometries():
    for h in range(9):
        for bits in itertools.product((False,True),repeat=h):
            a=[8-j for j in range(h+1)];source={'S_broot':a[-1],'S_bkr8':0,'S_brr8':19}
            for j in range(h):
                k,r=('kr','rr') if bits[j] else ('kl','rl')
                source[f'S_b{k}{a[j+1]}']=0;source[f'S_b{r}{a[j+1]}']=a[j]
            yield {'family':'RIGHT_SELF','h':h,'bits':list(bits),'target':8,'claimant':8},source,a+[19],list(bits)+[False,True]
    for n in range(1,9):
        for h in range(n):
            s=n-h
            for bits in itertools.product((False,True),repeat=h):
                for mode in ('ON','OFF') if n<8 else ('ON',):
                    zero=max([j+1 for j,b in enumerate(bits) if b],default=0) if mode=='ON' else None
                    labels=iter(range(1,9));a=[0 if j==zero else next(labels) for j in range(h+1)];b=[next(labels) for _ in range(s)]
                    source={'S_broot':a[-1],f'S_bkl{b[0]}':0,f'S_brl{b[0]}':19,f'S_bkr{a[0]}':0,f'S_brr{a[0]}':b[-1]}
                    for j in range(h):
                        k,r=('kr','rr') if bits[j] else ('kl','rl')
                        source[f'S_b{k}{a[j+1]}']=0;source[f'S_b{r}{a[j+1]}']=a[j]
                    for j in range(s-1):source[f'S_bkl{b[j+1]}']=0;source[f'S_brl{b[j+1]}']=b[j]
                    yield {'family':'LEFT_SUCCESSOR','h':h,'s':s,'bits':list(bits),'zero_mode':mode,
                           'zero_position':zero,'target':a[0],'claimant':b[0]},source,a+[19]+b,list(bits)+[False]*(s+1)+[True]

def main():
    output=BASE/'high_source_audit.json';assert not output.exists();start=time.process_time()
    d=DAG();bs=BState(d,'S');bt=BTrace(d,'T');out=b_splay_event(d,bs,bt,0,d.const_bool(False))
    claims=d.OR(*[d.AND(d.EQ(getattr(out,k)[i],d.const_int(0,2)),d.EQ(getattr(out,r)[i],bt.bT[0]))
                  for i in range(19) for k,r in (('kl','rl'),('kr','rr'))])
    prop=d.AND(d.EQ(out.root,bt.bT[0]),claims)
    preserve=d.AND(d.EQ(out.kr[8],d.const_int(0,2)),d.EQ(out.rr[8],d.const_int(19,5)))
    nodes=list(d.nodes);table=dict(d.tab);rows=[]
    old={}
    for folder in ['M2_DSK01','M3_OUT01']:
        j=json.loads((Path('DO_RESEARCH_REBOOT')/folder/'proof_certificate.json').read_text())
        for r in j['rows']:old[(r['family'],r['h'],r.get('s'),tuple(r['bits']),r.get('zero_mode'),r['d'])]=r['pins_sha256']
    def evaluate(pins,property):
        n=d.simplify(property,pins);v=d.nodes[n]
        assert v[0]=='const' and v[1]==BOOL and bool(v[3]),(pins,repr(v))
        d.nodes=list(nodes);d.tab=dict(table)
    for meta,source,path,dirs in geometries():
        for length in range(10,19):
            pins={**source,'T_bT0':meta['target'],'T_bd0':length}
            pins.update({f'T_bp0_{j}':path[j%len(path)] for j in range(length+1)})
            pins.update({f'T_bdir0_{j}':dirs[j%len(dirs)] for j in range(length)})
            key=(meta['family'],meta['h'],meta.get('s'),tuple(meta['bits']),meta.get('zero_mode'),length)
            sha=hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest();assert sha==old[key]
            evaluate(pins,prop);rows.append({**meta,'d':length,'pins_sha256':sha,'root_claim':True})
            if len(rows)%512==0:print(json.dumps({'identities':len(rows),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
            assert time.process_time()-start<300,'UNKNOWN high audit cap'
    assert len(rows)==11340
    absorption=[]
    for h in range(9):
        a=[8-j for j in range(h+1)];path=a+[19];dirs=[True]*h+[False,True]
        source={'S_broot':a[-1],'S_bkr8':0,'S_brr8':19}
        for j in range(h):source[f'S_bkr{a[j+1]}']=0;source[f'S_brr{a[j+1]}']=a[j]
        for length in range(19):
            pins={**source,'T_bT0':8,'T_bd0':length}
            pins.update({f'T_bp0_{j}':path[j%len(path)] for j in range(length+1)})
            pins.update({f'T_bdir0_{j}':dirs[j%len(dirs)] for j in range(length)})
            evaluate(pins,preserve if length<=h+1 else prop)
            absorption.append({'h':h,'d':length,'property':'preserve_chi8' if length<=h+1 else 'invalid_root_claim'})
    # Clean-source last primitive identity: arbitrary pre-final state, all nine targets.
    d2=DAG();b2=BState(d2,'C');clean=[]
    for x in range(9):
        result=b_single_rot(d2,b2,d2.const_int(x,5),d2.const_int(19,5),d2.const_int(19,5),d2.const_bool(False),d2.const_bool(False),d2.const_bool(True))
        property=d2.AND(d2.EQ(result.root,d2.const_int(x,5)),d2.EQ(result.kr[x],d2.const_int(0,2)),d2.EQ(result.rr[x],d2.const_int(19,5)))
        v=d2.nodes[d2.simplify(property,{})];assert v[0]=='const' and v[1]==BOOL and bool(v[3]);clean.append(x)
    result={'status':'PASS_INDEPENDENT_ORIGINAL_DAG_AUDIT','dirty_root_claim_identities':len(rows),
            'chi8_absorption_identities':len(absorption),'clean_last_write_targets':clean,
            'literal_slot0_ON_and_OFF':True,'off_spine_source_fields':'UNFIXED',
            'all_inherited_pin_hashes_reconstructed':True,'production_DAG_nodes':len(nodes),
            'old_case_generator_or_checker_imported':False,'cpu_seconds':round(time.process_time()-start,3),
            'rows':rows,'absorption':absorption}
    assert result['cpu_seconds']<300
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ['rows','absorption']},indent=2))

if __name__=='__main__':main()

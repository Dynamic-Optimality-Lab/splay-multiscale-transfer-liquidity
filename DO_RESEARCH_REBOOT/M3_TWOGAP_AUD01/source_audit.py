"""Independent extraction and source predicate audit; factories only propose witnesses."""
import json,sys,time,hashlib
from pathlib import Path
import reference as R
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01');OLD=Path('DO_RESEARCH_REBOOT/M3_TWOGAP01')
PC='DO_RESEARCH_REBOOT/06_CERTIFICATES/'
sys.path[:0]=[PC+'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',PC+'DIRECT_CDK5N_11F_STRICT_CLOSURE',PC+'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BTrace
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
FIELDS=('kl','rl','kr','rr','lo','hi');SIG=[1,1]+[0]*8
def val(d,e,n):
    z=d.nodes[n];assert z[0]=='var';return e[z[3][1]]
def bstate(d,e,b):return {'root':val(d,e,b.root),**{f:[val(d,e,n) for n in getattr(b,f)] for f in FIELDS}}
def ordinary(d,e,s):return {'mu':val(d,e,s.mu),'sigma':[val(d,e,n) for n in s.sig],
  'alpha':[[val(d,e,s.ak[i]),int(val(d,e,s.aS[i])),val(d,e,s.aI[i])] for i in range(7)],'b':bstate(d,e,s.b)}
def mid(d,e,g):return {'mu':val(d,e,g.mu),'sigma':[val(d,e,n) for n in g.sig],'v':val(d,e,g.v),'b':bstate(d,e,g.b)}
def flat(s):
    a=[s['mu'],*s['sigma'],s['b']['root']]
    for f in FIELDS:a.extend(s['b'][f])
    if 'alpha' in s:
        for x in s['alpha']:a.extend(x)
        assert len(a)==147
    else:a.append(s['v']);assert len(a)==127
    return tuple(a)
def chi(b):return b['kr'][8]==0 and b['rr'][8]==19
class Decoder:
    def __init__(self):
        m=json.loads((OLD/'decoder_metadata.json').read_text());p=json.loads((OLD/'potential_sparse.json').read_text())
        self.N=m['classes'];self.ai={R.frozen(a):i for i,a in enumerate(m['shadows'])};self.bi={R.frozen(b):i for i,b in enumerate(m['B_trees'])}
        self.psi=m['psi'];self.p={int(k):v for k,v in p['labels'].items()}
    def J(self,s):
        assert s['sigma']==SIG and s['mu'].bit_count()==5
        b=self.bi[R.core_view(s['b'])];a=self.ai.get(R.raw_normalize(s['alpha']))
        if a is None or not s['alpha'][0][1] or s['alpha'][0][2]!=s['b']['root']:return -self.psi[b]
        return self.p.get(b*self.N+a,-self.psi[b])
    def O(self,s):return self.J(s)-5*int(chi(s['b']))
    def M(self,m):assert m['sigma']==SIG;return -5*int(chi(m['b']))
def proper_B(b):
    seen=set()
    def go(i):
        assert i not in seen and i in range(19);seen.add(i)
        k=16*i if i<9 else 16*(i-9)-8;ch=[]
        for typ,ref in (('kl','rl'),('kr','rr')):
            c=b[ref][i];ch.append(go(c) if b[typ][i]==0 and c<19 else None)
        return (k,*ch)
    t=go(b['root']);assert seen==set(range(9))|{9,10};return t
def main():
    out=BASE/'source_audit.json';assert not out.exists();start=time.process_time()
    assert json.loads((BASE/'finite_audit.json').read_text())['status']=='INDEPENDENT_FINITE_EXACT_PASS'
    dl=DAG();L=build_slow(dl,'MXL');dh=DAG();H=build_shigh(dh,'MXH');bt=BTrace(dh,'MXHbt');P=Decoder();rows=[]
    def check(record,kind,label):
        d,obj=(dl,L) if kind=='LOW' else (dh,H);e=record['environment'];assert set(d.vars)<=set(e)
        for name,n in d.vars.items():
            node=d.nodes[n];v=e[name]
            if node[1]==BOOL:assert v in (False,True)
            else:
                w,sg=node[3][2:4];assert (-(1<<(w-1))<=v<(1<<(w-1))) if sg else 0<=v<(1<<w)
        assert d.ev_ground(obj['root'],e),label
        s=ordinary(d,e,obj['s']);t=ordinary(d,e,obj['t']);assert s==record['source'] and t==record['destination']
        assert len(flat(s))==len(flat(t))==147 and s['sigma']==t['sigma']==SIG and s['mu']==t['mu']
        js,jt=P.J(s),P.J(t);assert -2<=js<=0 and -2<=jt<=0
        if kind=='LOW':
            nv=val(d,e,L['wit'].nev);hh=sum((val(d,e,L['wit'].evd[j])+1)//2 for j in range(nv));q=val(d,e,L['bt'].q)
            assert hh==record['H']==val(d,e,L['H']);assert q==record['q'] and val(d,e,L['w'])==record['w']==2*hh-q
            current=proper_B(s['b']);last=None
            for j,(mode,x) in enumerate(record['word_codes']):
                dep=R.depth(current,x);assert dep==val(d,e,L['bt'].bd[j]);last=dep
                if mode=='K':current=R.splay(current,x)
            assert last//2==q and current==proper_B(t['b']);assert chi(s['b'])==chi(t['b'])
            residual=record['w']-P.O(t)+P.O(s);assert residual>=0;g=None
        else:
            g=mid(d,e,H['g']);assert g==record['shared_midpoint'];assert len(flat(g))==127
            assert s['mu']==g['mu']==t['mu'] and g['sigma']==SIG
            assert all(g['b'][f]==t['b'][f] for f in ('root',)+FIELDS[:4]);q=val(d,e,H['q']);w=val(d,e,H['w1'])
            assert q==val(d,e,bt.bd[0])//2 and w==6-q
            r1=w-P.M(g)+P.O(s);r2=P.M(g)-P.O(t);assert r1>=0 and r2>=0;residual=[r1,r2]
            if record.get('actual_depth')==0:assert R.depth(proper_B(s['b']),128)==0 and q==9 and w==-3
        row={'label':label,'kind':kind,'source':s,'destination':t,'midpoint':g,'J_source':js,'J_destination':jt,'residual':residual,
          'root':True,'environment_sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()}
        rows.append(row);assert time.process_time()-start<300,'UNKNOWN source audit CPU cap';return row
    for filename in ('original_controls.json','macro_controls.json','decoder_and_h0.json'):
        obj=json.loads((OLD/filename).read_text())
        for j,r in enumerate(obj['records']):check(r,'HIGH' if filename=='decoder_and_h0.json' else 'LOW',r.get('label',f'{filename}_{j}'))
    # Fresh factories propose two actual mixed cycles. PASS depends only on original roots
    # and the independently extracted full interfaces, not their claimed states.
    sys.path[:0]=['DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
    import interior_original as IN
    import outside_original as OUT
    S=IN.S;z=S.LEAF
    A=S.node(32,S.node(8,S.node(0,S.node(-8,z,z),z),S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
    B=S.node(32,S.node(0,z,S.node(16,z,z)),S.node(96,S.balanced([48,64,80]),S.balanced([112,128])))
    B=IN.V.insert(IN.V.insert(B,-8),8);cycles=[]
    for helper,name in ((OUT,'outside'),(IN,'inside')):
        Ad,Bd,lo=helper.low(dl,L,A,B,[(8,0),(8,1)],[['K',96]],'fresh_two_gap_mixed_'+name,341)
        hi=helper.high(dh,H,Bd,32,lo['destination'],lo['source'],'fresh_two_gap_return_'+name)
        lrow=check(lo,'LOW',lo['label']);hrow=check(hi,'HIGH',hi['label'])
        assert flat(lrow['source'])==flat(hrow['destination']) and flat(lrow['destination'])==flat(hrow['source'])
        assert hi['w']+lo['w']==8
        cycles.append({'region':name,'full_147_coordinate_O_closure':True,'same_actual_127_coordinate_midpoint':True,
          'weight':8,'low_source':lrow['source'],'low_destination':lrow['destination'],'midpoint':hrow['midpoint'],
          'low_environment':lo['environment'],'high_environment':hi['environment']})
    assert len(rows)==22
    result={'status':'INDEPENDENT_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS','original_roots':len(rows),'low_roots':18,'high_roots':4,
      'fresh_full_mixed_cycles':2,'ordinary_raw_coordinates':147,'midpoint_raw_coordinates':127,'DAG_nodes':[len(dl.nodes),len(dh.nodes)],
      'h0_correction_retained':True,'fiber_v_independent_of_B_target_retained':True,'cpu_seconds':round(time.process_time()-start,3),
      'rows':rows,'cycles':cycles,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','cycles')},indent=2),flush=True)
if __name__=='__main__':main()

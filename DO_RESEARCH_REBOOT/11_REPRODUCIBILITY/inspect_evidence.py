"""Read-only evidence metadata, exact saved certificate check, and paper text."""
import sys,json,hashlib,ast,math
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
WS=Path(__file__).resolve().parents[1]; ROOT=WS.parent
DM=ROOT/'artifacts/v04/wp6_present/0909c74a/dual_mine'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def short(v):
    if isinstance(v,dict): return {k:short(w) for k,w in v.items() if not isinstance(w,list) or len(w)<8}
    if isinstance(v,list): return v if len(str(v))<1500 else {'length':len(v)}
    return v
metadata={}
for p in sorted(DM.glob('*.json')):
    if p.name.startswith(('j4_','joint_texact')):
        obj=json.loads(p.read_text(encoding='utf-8'))
        if isinstance(obj,dict):
            summary={k:short(v) for k,v in obj.items() if not isinstance(v,list) or len(v)<8}
            metadata[p.name]={'sha256':digest(p),'summary':summary}
npzmeta={}
import numpy as np
for name in ['j4_levelblocks.npz','j4_rednorm_mat.npz','j4_sh567_A.npz']:
    p=DM/name
    if not p.exists():continue
    with np.load(p,allow_pickle=False) as z:
        npzmeta[name]={'sha256':digest(p),'arrays':{k:{'shape':list(z[k].shape),'dtype':str(z[k].dtype)} for k in z.files}}
        if name=='j4_levelblocks.npz':
            import sympy as sp
            for k in z.files:
                arr=z[k]
                if arr.ndim==2 and arr.shape[1]<=120 and arr.shape[0]<=2000:
                    assert np.array_equal(arr,arr.astype(np.int64))
                    rank=sp.Matrix(arr.astype(np.int64).tolist()).rank()
                    npzmeta[name]['arrays'][k]['rank_Q']=rank
                    npzmeta[name]['arrays'][k]['nullity_Q']=arr.shape[1]-rank

# Recover all 15 saved LRF inequality multipliers and three equality
# multipliers as rationals, then check every saved reduced-matrix column.
# This is a certificate for that matrix only, not an all-depth J4 refutation.
cert=json.loads((DM/'j4_lrffarkas.json').read_text())
eqs=json.loads((DM/'j4_lrflist.json').read_text())
with np.load(DM/'j4_rednorm_mat.npz',allow_pickle=False) as z:
    assert np.array_equal(z['A'],z['A'].astype(np.int64))
    assert np.array_equal(z['rhs'],z['rhs'].astype(np.int64))
    A=z['A'].astype(np.int64);rhs=z['rhs'].astype(np.int64)
    keys=[ast.literal_eval(str(k)) for k in z['keys']]
rv={k:i for i,k in enumerate(keys)}
offset={5:0,6:42*25,7:42*25+132*36}
rowdata=[];residual=[Fraction(0) for _ in keys];yrhs=Fraction(0)
for weight,meta,_ in cert['rows']:
    w=Fraction(str(weight)).limit_denominator(10000)
    assert abs(float(w)-weight)<1e-12 and w>=0
    kind=meta[0];n=int(meta[1]);bi=int(meta[2]);r=int(meta[3])
    if kind=='SELF': idx=offset[n]+bi*n*n+r-1
    else:
        x=int(meta[4]);idx=offset[n]+bi*n*n+n+(r-1)*(n-1)+x-1-int(x>r)
    for j,coef in enumerate(A[idx]):residual[j]+=w*int(coef)
    yrhs+=w*int(rhs[idx])
    rowdata.append({'index':idx,'multiplier':str(w),'source_meta':meta,'reduced_rhs':int(rhs[idx])})
eqdata=[]
for i,weight in cert['eqw']:
    w=Fraction(str(weight)).limit_denominator(10000)
    assert abs(float(w)-weight)<1e-12
    if i==len(eqs):
        t0=next(j for j,k in enumerate(keys) if k[0]=='t');residual[t0]+=w
        eqdata.append({'index':i,'multiplier':str(w),'gauge_index':t0})
        continue
    e=eqs[i]
    def tau(t):return ('t',(ast.literal_eval(t[0]),t[1],t[2],t[3]))
    ia,ib=rv[tau(e['tau'])],rv[tau(e['tau2'])]
    residual[ib]+=w;residual[ia]-=w
    eqdata.append({'index':i,'multiplier':str(w),'minus_key':repr(keys[ia]),'plus_key':repr(keys[ib])})
certificate={'matrix_shape':list(A.shape),'inequality_rows':rowdata,'equality_rows':eqdata,
             'zero_residual':all(x==0 for x in residual),'positive_rhs':str(yrhs),
             'nonzero_residuals':[[repr(keys[i]),str(x)] for i,x in enumerate(residual) if x],
             'scope':'saved reduced SH567 matrix + listed LRF homogeneous equalities',
             'source_row_provenance':'original J4 generator shape order and SELF/DIAM row index; reduced rows/rhs read from pinned matrix'}
assert certificate['zero_residual'] and yrhs>0,certificate
(WS/'06_CERTIFICATES').mkdir(exist_ok=True)
(WS/'06_CERTIFICATES/LRF_EXACT_RECHECK.json').write_text(json.dumps(certificate,indent=2),encoding='utf-8')

from pypdf import PdfReader
papers=[]
paper=ROOT/'v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf'
if paper.exists():
    reader=PdfReader(paper)
    pages=[]
    for i,page in enumerate(reader.pages):
        txt=page.extract_text() or ''
        pages.append(f'--- PDF PAGE {i+1} ---\n{txt}')
    (WS/'11_REPRODUCIBILITY/L3_local_extracted.txt').write_text('\n\n'.join(pages),encoding='utf-8')
    papers.append({'path':str(paper.relative_to(ROOT)),'sha256':digest(paper),'pages':len(reader.pages)})
summary={'json_metadata':metadata,'npz_metadata':npzmeta,'papers':papers,'LRF_certificate':{
    'zero_residual':certificate['zero_residual'],'positive_rhs':certificate['positive_rhs'],'matrix_shape':list(A.shape)}}
(WS/'11_REPRODUCIBILITY/evidence_metadata.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({'npz_metadata':npzmeta,'papers':papers,'LRF_certificate':summary['LRF_certificate']},indent=2))

# 26O coupling block: derive the actual 970x79 matrix from xclean rather
# than trusting its floating SVD report. A modular rank supplies the lower
# bound; 31 independent rational null vectors supply the exact upper bound.
xc=DM/'j4_xclean_mat.npz'
if xc.exists():
    with np.load(xc,allow_pickle=False) as z:
        full=z['A']; e0=int(z['E0'][0])
        assert np.array_equal(full,full.astype(np.int64))
        old=np.flatnonzero(np.any(full[:e0]!=0,axis=0))
        touched=[int(j) for j in old if np.any(full[e0:,j]!=0)]
        C=full[e0:,touched].astype(np.int64)
    prime=1000003; M=C.copy()%prime;order=list(range(len(C)));rank=0;pivots=[]
    for col in range(C.shape[1]):
        nz=np.flatnonzero(M[rank:,col])
        if not len(nz):continue
        i=rank+int(nz[0]);M[[rank,i]]=M[[i,rank]];order[rank],order[i]=order[i],order[rank]
        M[rank,col:]=(M[rank,col:]*pow(int(M[rank,col]),prime-2,prime))%prime
        for j in range(rank+1,len(C)):
            if M[j,col]:M[j,col:]=(M[j,col:]-int(M[j,col])*M[rank,col:])%prime
        pivots.append(col);rank+=1
    import sympy as sp
    basis=sp.Matrix(C[order[:rank]].tolist()).nullspace()
    assert len(basis)==C.shape[1]-rank
    exactC=sp.Matrix(C.tolist())
    assert all(exactC*v==sp.zeros(len(C),1) for v in basis)
    assert sp.Matrix.hstack(*basis).rank()==len(basis)
    out={'source_npz':str(xc.relative_to(ROOT)).replace('\\','/'),'sha256':digest(xc),
         'shape':list(C.shape),'E0':e0,'touched_global_columns':touched,
         'modular_prime':prime,'rank_mod_prime':rank,'independent_source_rows':order[:rank],
         'pivot_columns':pivots,'rational_nullity':len(basis),'rank_Q':rank,
         'full_exact_zero_residual':True,'kernel_basis':[[str(x) for x in v] for v in basis],
         'scope':'finite xclean coupling block; no all-depth inference'}
    assert C.shape==(970,79) and rank==48 and len(basis)==31
    (WS/'06_CERTIFICATES/C0_RANK_EXACT_RECHECK.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('kernel_basis','touched_global_columns','independent_source_rows','pivot_columns')},indent=2))

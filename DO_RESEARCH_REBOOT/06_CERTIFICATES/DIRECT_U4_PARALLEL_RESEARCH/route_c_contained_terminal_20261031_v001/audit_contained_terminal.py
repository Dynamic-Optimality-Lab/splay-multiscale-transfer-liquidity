"""Two analytic families, four local rows, exact matching/cover certificates; no fits."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT = HERE.parent
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def main():
    old = json.loads((PARENT / 'route_c_exact_b_architecture_20261031_v001/entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(old['files'])
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    for rel in ('DO_RESEARCH_REBOOT/RESEARCH_RULES.md', 'python/independent/splay.py', 'python/liquidity/legacy_embedding.py'):
        pins[rel] = sha(ROOT / rel)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    for rel, val in old['files'].items():
        assert sha(ROOT / rel) == val, rel
    assert len(stage) == 125
    for rel, val in pins.items():
        assert sha(ROOT / rel) == val, rel
    entry = dict(date='2026-10-31', head=git('rev-parse','HEAD'), branch=git('branch','--show-current'),
                 tracked_status=git('status','--porcelain=v1','--untracked-files=no'),
                 files=pins, stage_files=stage, inherited_pins=len(old['files']))
    assert not entry['tracked_status']
    save('entry_source_pins.json', entry)
    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF
    def leaf(k):
        return s.node(k,L,L)
    def vine(lo, hi):
        t = L
        for k in range(hi,lo-1,-1):
            t = s.node(k,L,t)
        return t
    def raw(t):
        return None if t == L else [t[1],raw(t[2]),raw(t[3])]
    def mirror(t,n):
        return L if t == L else s.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
    def intervals(t):
        if t == L:
            return [],set()
        kl,sl = intervals(t[2]); kr,sr = intervals(t[3])
        ks = kl+[t[1]]+kr
        assert ks == sorted(set(ks))
        return ks, sl | sr | {(ks[0],ks[-1])}
    def proper(t):
        ks,ss = intervals(t)
        if ks:
            ss.remove((ks[0],ks[-1]))
        assert len(ss) == max(0,len(ks)-1)
        return ks, sorted(ss)
    def match_cover(adj,nr):
        owner = [-1]*nr
        def augment(i,seen):
            for j in adj[i]:
                if j in seen:
                    continue
                seen.add(j)
                if owner[j] < 0 or augment(owner[j],seen):
                    owner[j] = i
                    return True
            return False
        for i in range(len(adj)):
            augment(i,set())
        matching = sorted([[i,j] for j,i in enumerate(owner) if i >= 0])
        left_match = {i:j for i,j in matching}
        zl = {i for i in range(len(adj)) if i not in left_match}
        zr = set()
        queue = list(zl)
        for i in queue:
            for j in adj[i]:
                if left_match.get(i) == j or j in zr:
                    continue
                zr.add(j)
                if owner[j] >= 0 and owner[j] not in zl:
                    zl.add(owner[j]);queue.append(owner[j])
        cl,cr = sorted(set(range(len(adj)))-zl),sorted(zr)
        assert len(matching) == len(cl)+len(cr)
        assert all(i in cl or j in cr for i,row in enumerate(adj) for j in row)
        return dict(matching=matching,cover_left=cl,cover_right=cr,rank=len(matching))
    graphs, graph_index = [],{}
    def graph(a,c):
        key = (a,c)
        if key in graph_index:
            return graph_index[key]
        ka,aa = proper(a);kc,cc = proper(c)
        assert ka == kc and a[1] == c[1]
        common = sorted(set(aa)&set(cc));fixed = set(common)
        ll = [I for I in aa if I not in fixed]
        rr = [J for J in cc if J not in fixed]
        adj = [[j for j,J in enumerate(rr) if J != I and I[0] <= J[0] <= J[1] <= I[1]
                and (I[0] == J[0] or I[1] == J[1])] for I in ll]
        dual = match_cover(adj,len(rr))
        f = len(aa)-len(common)
        g = dict(A=raw(a),C=raw(c),n=len(ka),all_A_intervals=aa,all_C_intervals=cc,
                 forced_exact_pairs=common,left_residual=ll,right_residual=rr,
                 adjacency=adj,dual=dual,F=f,beta=dual['rank'],D=f-dual['rank'])
        idx = len(graphs);graph_index[key] = idx;graphs.append(g)
        return idx
    def completion(a,b):
        r = a[1]
        c, ev = s.trace(b,r)
        d = s.lookup(b,r)[1]
        q = sum(e[0] != 'ZIG' for e in ev)
        z = sum(e[0] == 'ZIG' for e in ev)
        assert q == d//2 and z == d%2 and len(ev) == (d+1)//2
        gi = graph(a,c)
        return dict(root_A=r,completed_B=raw(c),depth=d,q=q,z=z,events=ev,
                    terminal_graph=gi,D=graphs[gi]['D'],Phi=graphs[gi]['D']+q)
    def row(name,a,b,x):
        ap, ev = s.trace(a,x)
        da = s.lookup(a,x)[1]
        v0,v1 = completion(a,b),completion(ap,b)
        ac = len(ev)
        assert ac == (da+1)//2
        return dict(name=name,mode='D',key=x,n=len(s.inorder(a)),source_A=raw(a),source_B=raw(b),
                    destination_A=raw(ap),destination_B=raw(b),d_A=da,a=ac,actual_q=0,actual_z=0,
                    A_events=ev,source_completion=v0,destination_completion=v1,
                    delta_Phi=v1['Phi']-v0['Phi'],budget=2*ac,
                    DELETE_holds=v1['Phi']-v0['Phi'] <= 2*ac)
    n = 7
    middle = leaf(n-1)
    for k in range(n-2,2,-2):
        middle = s.node(k,leaf(k-1),middle)
    a7,b7 = s.node(1,L,s.node(n,middle,L)),vine(1,n)
    parity = row('odd_parity_comb_repair',a7,b7,n)
    assert (parity['source_completion']['D'],parity['destination_completion']['D'],parity['delta_Phi']) == (5,3,1)
    n = 14
    h = L
    for k in range(n,1,-2):
        h = s.node(k,leaf(k-1),h)
    a14 = s.node(1,L,s.node(n,vine(2,n-1),L))
    counter = row('fully_fringed_spine_counterexample',a14,h,n)
    assert (counter['source_completion']['D'],counter['destination_completion']['D'],counter['delta_Phi']) == (6,6,3)
    rows = [parity,row('odd_parity_comb_reflection',mirror(a7,7),mirror(b7,7),1),
            counter,row('fully_fringed_spine_reflection',mirror(a14,14),mirror(h,14),1)]
    assert [r['DELETE_holds'] for r in rows] == [True,True,False,False]
    cert = dict(schema='contained-terminal-two-analytic-families-v1',date='2026-10-31',
                terminal_rule='force exact pairs; residual J strictly contained in I and equal minimum or maximum',
                terminal_graphs=graphs,controls=rows,coefficient_fits=0,state_graphs=0,
                sizes_evaluated=[7,14],finite_size_sweep=False,
                n14_is_analytic_witness_not_fit=True,
                universal_B='PROVED—UNIVERSAL',universal_DELETE='REFUTED—EXACT',
                diagonal_reachability_new_counter='NOT ESTABLISHED OR CLAIMED',
                actual_closed_pair_walk_claimed=False,new_CD_counterexample=False)
    save('contained_terminal_certificate.json',cert)
    print(json.dumps(dict(terminal_graphs=len(graphs),controls=[dict(name=r['name'],n=r['n'],
         D0=r['source_completion']['D'],D1=r['destination_completion']['D'],
         Q0=r['source_completion']['q'],Q1=r['destination_completion']['q'],
         delta=r['delta_Phi'],budget=r['budget']) for r in rows],
         preserved_files=len(pins),stage_files=len(stage)),indent=2))

if __name__ == '__main__':
    main()

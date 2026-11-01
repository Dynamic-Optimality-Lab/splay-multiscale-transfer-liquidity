"""Independent pointer replay and primal/dual checking of four specified local rows."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def ck(ok,msg):
    if not ok:
        raise AssertionError(msg)

def main():
    cp = HERE / 'contained_terminal_certificate.json'
    c = json.loads(cp.read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('pointer_source', ROOT / 'python/liquidity/legacy_embedding.py')
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
    def ptr(t):
        if t is None:
            return None
        z = p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if z[side] is not None:
                z[side]['p'] = z
        return z
    def raw(t):
        return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
    def depth(t,x):
        d = 0
        while t is not None:
            if t[0] == x:
                return d
            t = t[1] if x < t[0] else t[2]
            d += 1
        raise AssertionError('absent request')
    def events(es):
        return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    def mirror(t,n):
        return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]
    def vine(lo,hi):
        t = None
        for k in range(hi,lo-1,-1):
            t = [k,None,t]
        return t
    def inspect(t):
        if t is None:
            return [],set()
        kl,sl = inspect(t[1]);kr,sr = inspect(t[2])
        ks = kl+[t[0]]+kr
        ck(ks == sorted(set(ks)), 'valid BST keys')
        return ks, sl | sr | {(ks[0],ks[-1])}
    def proper(t):
        ks,ss = inspect(t)
        if ks:
            ss.remove((ks[0],ks[-1]))
        ck(len(ss) == max(0,len(ks)-1), 'distinct proper interval multiplicity')
        return ks, sorted(ss)
    def left_links(t):
        return 0 if t is None else (t[1] is not None)+left_links(t[1])+left_links(t[2])
    graphs = c['terminal_graphs']
    ck(len(graphs) == 8, 'exactly eight local terminal graphs')
    duals = 0
    for g in graphs:
        ka,aa = proper(g['A']); kc,cc = proper(g['C'])
        ck(ka == kc == list(range(1,g['n']+1)) and g['A'][0] == g['C'][0], 'terminal same ranked keys/root')
        common = sorted(set(aa)&set(cc));fixed = set(common)
        l,r = [I for I in aa if I not in fixed],[J for J in cc if J not in fixed]
        ck(g['all_A_intervals'] == [list(I) for I in aa] and g['all_C_intervals'] == [list(J) for J in cc], 'complete proper intervals')
        ck(g['forced_exact_pairs'] == [list(I) for I in common] and
           g['left_residual'] == [list(I) for I in l] and g['right_residual'] == [list(J) for J in r], 'forced pairs and residuals')
        adj = [[j for j,J in enumerate(r) if J != I and I[0] <= J[0] <= J[1] <= I[1]
                and (I[0] == J[0] or I[1] == J[1])] for I in l]
        ck(g['adjacency'] == adj, 'every and only contained endpoint edge')
        d = g['dual']; mat,cl,cr = d['matching'],d['cover_left'],d['cover_right']
        ck(len({i for i,j in mat}) == len({j for i,j in mat}) == len(mat), 'matching distinct endpoints')
        ck(all(type(i) is type(j) is int and 0 <= i < len(l) and 0 <= j < len(r) and j in adj[i] for i,j in mat), 'genuine matching edges')
        ck(len(set(cl)) == len(cl) and len(set(cr)) == len(cr) and
           all(type(i) is int and 0 <= i < len(l) for i in cl) and
           all(type(j) is int and 0 <= j < len(r) for j in cr), 'cover dimensions and distinctness')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row), 'all edges covered')
        ck(len(mat) == len(cl)+len(cr) == d['rank'] == g['beta'], 'exact optimum by matching/cover equality')
        ck((g['F'],g['D']) == (len(aa)-len(common),len(aa)-len(common)-g['beta']), 'one unchanged terminal formula')
        duals += 1
    calls = completions = 0
    def source(t,x):
        nonlocal calls
        d = depth(t,x)
        out,ev = p.splay_trace(ptr(t),x)
        q,z = sum(e['case'] != 'ZIG' for e in ev),sum(e['case'] == 'ZIG' for e in ev)
        ck(q == d//2 and z == d%2 and len(ev) == (d+1)//2, 'exact grouped event units')
        calls += 1
        return raw(out),ev,d,q,z
    def completion(a,b,v):
        nonlocal completions
        r = a[0]
        bt,ev,d,q,z = source(b,r)
        g = graphs[v['terminal_graph']]
        ck(g['A'] == a and g['C'] == bt, 'correct graph at actual completed pair')
        expected = dict(root_A=r,completed_B=bt,depth=d,q=q,z=z,events=events(ev),
                        terminal_graph=v['terminal_graph'],D=g['D'],Phi=g['D']+q)
        ck(v == expected and bt[0] == r, 'source completion evaluation')
        again,noop,d2,q2,z2 = source(bt,r)
        ck(again == bt and not noop and d2 == q2 == z2 == 0, 'source idempotence')
        ck(g['D']-v['Phi'] == -q, 'exact B law at this source pair')
        completions += 1
    rows = c['controls']
    ck(len(rows) == 4 and c['coefficient_fits'] == c['state_graphs'] == 0 and
       not c['finite_size_sweep'] and c['n14_is_analytic_witness_not_fit'], 'frozen analytic audit scope')
    for row in rows:
        a,b,x = row['source_A'],row['source_B'],row['key']
        ap,ev,d,q,z = source(a,x)
        ck(row['mode'] == 'D' and row['destination_B'] == b and row['destination_A'] == ap, 'physical DELETE leaves B frozen')
        ck(d == row['d_A'] == 1 and row['a'] == 1 and row['actual_q'] == row['actual_z'] == 0, 'one A root zig; no physical B cost')
        ck(events(ev) == row['A_events'] and len(ev) == 1 and ev[0]['case'] == 'ZIG', 'full oriented A source event')
        completion(a,b,row['source_completion']);completion(ap,b,row['destination_completion'])
        delta = row['destination_completion']['Phi']-row['source_completion']['Phi']
        ck((row['delta_Phi'],row['budget'],row['DELETE_holds']) == (delta,2,delta <= 2), 'correct source bound verdict')
    n = 7
    middle = [6,None,None]
    for k in (5,3):
        middle = [k,[k-1,None,None],middle]
    a7,b7 = [1,None,[7,middle,None]],vine(1,7)
    ck(rows[0]['source_A'] == a7 and rows[0]['source_B'] == b7 and rows[0]['key'] == 7, 'specified repaired parity member')
    ck((rows[0]['source_completion']['D'],rows[0]['destination_completion']['D'],rows[0]['delta_Phi']) == (5,3,1), 'unbounded-drop formula at n7')
    g0,g1 = [graphs[rows[0][v]['terminal_graph']] for v in ('source_completion','destination_completion')]
    ck((g0['F'],g0['beta'],g1['F'],g1['beta']) == (5,0,5,2), 'parity repair exact rank values')
    n = 14
    h = None
    for k in range(14,1,-2):
        h = [k,[k-1,None,None],h]
    a14 = [1,None,[14,vine(2,13),None]]
    bad = rows[2]
    ck((bad['source_A'],bad['source_B'],bad['key']) == (a14,h,14), 'specified fringed spine counterexample')
    v0,v1 = bad['source_completion'],bad['destination_completion']
    ck((v0['D'],v1['D'],v0['q'],v1['q'],v0['Phi'],v1['Phi']) == (6,6,0,3,6,9), 'exact false DELETE inequality')
    ck(v0['depth'] == 1 and v0['z'] == 1 and v1['depth'] == 6 and v1['z'] == 0, 'completion versus physical counts')
    ck(all(e[0] == 'RR' for e in v1['events']) and len(v1['events']) == 3, 'source consumes three right-right groups')
    ck(left_links(h) == left_links(v1['completed_B']) == 7 and left_links(v1['completed_B'][1]) == 6, 'fringed RR left-link identity')
    g0,g1 = [graphs[bad[v]['terminal_graph']] for v in ('source_completion','destination_completion')]
    ck((g0['F'],g0['beta'],g1['F'],g1['beta']) == (11,5,9,3), 'counterexample exact rank values')
    ck(bad['delta_Phi'] == 3 > bad['budget'] == 2, 'universal DELETE refutation on stated all-pair domain')
    for i,j,n in ((0,1,7),(2,3,14)):
        ck(rows[j]['source_A'] == mirror(rows[i]['source_A'],n) and
           rows[j]['source_B'] == mirror(rows[i]['source_B'],n) and
           rows[j]['destination_A'] == mirror(rows[i]['destination_A'],n) and
           rows[j]['key'] == n+1-rows[i]['key'], 'exact key-order reflection')
        ck(rows[j]['delta_Phi'] == rows[i]['delta_Phi'], 'both orientations same verdict')
    ck(c['diagonal_reachability_new_counter'] == 'NOT ESTABLISHED OR CLAIMED' and
       not c['actual_closed_pair_walk_claimed'] and not c['new_CD_counterexample'], 'domain limitation not hidden')
    result = dict(status='PASS',date='2026-10-31',terminal_graphs=8,matching_cover_equalities=duals,
                  complete_source_DELETE_rows=4,completion_evaluations=completions,
                  pointer_source_accesses=calls,producer_imported=False,matching_optimizer_imported=False,
                  parity_terminal_values=[5,3],parity_completed_increment=1,
                  counterexample_n=14,counterexample_terminal_values=[6,6],
                  counterexample_completion_q=[0,3],counterexample_Phi=[6,9],DELETE_budget=2,
                  both_orientations_verified=True,counterexample_domain='all finite same-key pairs',
                  diagonal_reachability_not_claimed=True,CD_counterexample=False,
                  coefficient_fits=0,new_state_graphs=0,finite_size_sweeps=0,
                  all_size_claims_supported_by='CT01 and CT02 analytic proofs, not extrapolation',
                  certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE / 'independent_audit.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()

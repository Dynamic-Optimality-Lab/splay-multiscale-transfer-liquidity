"""Pointer-source verification of an existing walk and the full-form incidence lift."""
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
    cp = HERE / 'full_form_source_certificate.json'
    cert = json.loads(cp.read_text(encoding='utf-8'))
    oldpath = ROOT / cert['inherited_control_file']
    ck(hashlib.sha256(oldpath.read_bytes()).hexdigest() == cert['inherited_control_sha256'], 'old control bytes pinned')
    old = json.loads(oldpath.read_text(encoding='utf-8'))['controls'][0]
    spec = importlib.util.spec_from_file_location('pointer_source',ROOT / 'python/liquidity/legacy_embedding.py')
    p = importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
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
    def mirror(t):
        return None if t is None else [7-t[0],mirror(t[2]),mirror(t[1])]
    def keys(t):
        if t is None:
            return []
        ks = keys(t[1])+[t[0]]+keys(t[2])
        ck(ks == sorted(set(ks)), 'valid BST')
        return ks
    def depth(t,x):
        d = 0
        while t is not None:
            if t[0] == x:
                return d
            t = t[1] if x < t[0] else t[2];d += 1
        raise AssertionError('absent request')
    def evs(es):
        return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    calls = 0
    def access(t,x):
        nonlocal calls
        d = depth(t,x);out,ev = p.splay_trace(ptr(t),x)
        q = sum(e['case'] != 'ZIG' for e in ev);z = sum(e['case'] == 'ZIG' for e in ev)
        ck(q == d//2 and z == d%2 and len(ev) == (d+1)//2, 'source grouped units')
        calls += 1
        return raw(out),ev,d,q,z
    total_full = total_split = total_states = total_lift_edges = 0
    for ci,control in enumerate(cert['controls']):
        states = control['states'];full = control['full_rows'];phases = control['split_rows']
        ck(len(full) == 11 and len(phases) == 15 and len(states) == 17, 'fixed control dimensions')
        initial = old['initial_A'] if ci == 0 else mirror(old['initial_A'])
        word = old['word'] if ci == 0 else [[m,7-x] for m,x in old['word']]
        ck(control['initial_A'] == control['initial_B'] == initial and control['word'] == word, 'existing word or reflection')
        ck(len({json.dumps([v['A'],v['B']],separators=(',',':')) for v in states}) == len(states), 'distinct physical pair states')
        for i,v in enumerate(states):
            a,b = v['A'],v['B'];r = a[0]
            ck(keys(a) == keys(b) == list(range(1,7)), 'same six ranked keys')
            cb,ev,d,q,z = access(b,r)
            pi = v['projection'];ck(type(pi) is int and 0 <= pi < len(states), 'projection index')
            ck((states[pi]['A'],states[pi]['B']) == (a,cb), 'projection is actual source completion')
            ck((v['root_A'],v['terminal'],v['Q'],v['completion_depth'],v['completion_z'],v['completion_events']) ==
               (r,a[0] == b[0],q,d,z,evs(ev)), 'normal-form source data')
            same,noops,dd,qq,zz = access(cb,r)
            ck(same == cb and not noops and dd == qq == zz == 0 and states[pi]['projection'] == pi,
               'completion idempotence and terminal index')
        state_index = control['initial_state'];A=Q=Z=W=0
        ck((states[state_index]['A'],states[state_index]['B']) == (initial,initial), 'actual diagonal start')
        for wi,((mode,x),row) in enumerate(zip(word,full)):
            ck((row['source'],row['mode'],row['key']) == (state_index,mode,x), 'whole-word physical sharing')
            u = states[state_index];a,b = u['A'],u['B']
            ap,ae,da,_,_ = access(a,x)
            if mode == 'K':
                bp,be,db,q,z = access(b,x)
            else:
                bp,be,db,q,z = b,[],None,0,0
            ac = len(ae);v = states[row['target']];mid = states[row['intermediate']]
            ck((mid['A'],mid['B'],v['A'],v['B']) == (ap,b,ap,bp), 'correct A intermediate and full endpoints')
            ck((row['d_A'],row['d_B'],row['a'],row['q'],row['z'],row['A_events'],row['B_events'],row['weight']) ==
               (da,db,ac,q,z,evs(ae),evs(be),2*ac-q), 'whole-row source costs and events')
            indices = row['phase_indices']
            ck(len(indices) == (2 if mode == 'K' else 1) and phases[indices[0]]['mode'] == 'D', 'exact source split')
            ck(phases[indices[0]]['source'] == row['source'] and phases[indices[-1]]['target'] == row['target'], 'split endpoint identity')
            ck(sum(phases[j]['a'] for j in indices) == ac and sum(phases[j]['q'] for j in indices) == q and
               sum(phases[j]['z'] for j in indices) == z and sum(phases[j]['weight'] for j in indices) == row['weight'], 'split preserves all costs')
            if ci == 0:
                prior = old['full_replay'][wi]
                ck((u['A'],u['B'],v['A'],v['B']) == (prior['source_A'],prior['source_B'],prior['destination_A'],prior['destination_B']), 'inherited actual row endpoints')
                ck((ac,q,2*ac-q) == (prior['a'],prior['q'],prior['signed_weight']), 'inherited cost units')
            A+=ac;Q+=q;Z+=z;W+=2*ac-q;state_index=row['target']
        ck(state_index == control['final_state'] == control['initial_state'] and
           (A,Q,Z,W) == (16,4,2,28) == (control['A'],control['Q_B'],control['Z_B'],control['weight']), 'actual pair closure and CD weight')
        state_index = control['initial_state'];walk_nodes = {state_index}
        for pi,e in enumerate(phases):
            ck(e['source'] == state_index and e['mode'] in ('D','K'), 'split physical walk sharing')
            u,v = states[e['source']],states[e['target']];a,b=u['A'],u['B'];x=e['key']
            ap,ae,da,_,_ = access(a,x)
            if e['mode'] == 'K':
                bp,be,db,q,z = access(b,x)
                ck(a[0] == x and ap == a and da == 0 and not ae and e['a'] == 0, 'B edge is legal root-aligned KEEP')
                ck(e['target'] == u['projection'] and u['Q'] == q, 'B edge realizes source projection and Q')
            else:
                bp,be,db,q,z = b,[],None,0,0
            ck((v['A'],v['B']) == (ap,bp), 'split actual endpoints')
            ck((e['d_A'],e['d_B'],e['a'],e['q'],e['z'],e['A_events'],e['B_events'],e['weight']) ==
               (da,db,len(ae),q,z,evs(ae),evs(be),2*len(ae)-q), 'split source costs and events')
            walk_nodes.update((e['source'],e['target']));state_index=e['target']
        ck(state_index == control['initial_state'], 'split walk closes')
        ck(all(i in walk_nodes or any(states[j]['projection'] == i for j in walk_nodes) for i in range(len(states))), 'every listed state is source-reachable by prefix plus optional root KEEP')
        ds = [i for i,e in enumerate(phases) if e['mode'] == 'D']
        ck(ds == control['DELETE_phase_indices'] and control['DELETE_multipliers'] == [1]*len(ds), 'explicit nonnegative multipliers')
        coeff = [0]*len(states)
        for j in ds:
            e=phases[j];coeff[e['target']]+=1;coeff[e['source']]-=1
        proj = [0]*len(states)
        for i,value in enumerate(coeff):
            proj[states[i]['projection']] += value
        ck(coeff == control['H_coefficients'] and proj == control['projected_Theta_coefficients'] and not any(proj), 'all terminal coefficients cancel with multiplicity')
        ck(all(value >= 0 for i,value in enumerate(coeff) if not states[i]['terminal']), 'valid nonnegative H signs')
        mu = [[i,value] for i,value in enumerate(coeff) if not states[i]['terminal'] and value > 0]
        ck(mu == control['added_B_multipliers'], 'precise source KEEP multipliers for slack elimination')
        wd = sum(phases[j]['weight'] for j in ds)
        grad = sum(states[phases[j]['target']]['Q']-states[phases[j]['source']]['Q'] for j in ds)
        ck((wd,grad,wd-grad) == (control['DELETE_weight_sum'],control['DELETE_Q_gradient'],control['contradiction_rhs']), 'constant and completion-gradient identities')
        expected_lift = [dict(kind='DELETE',phase_index=j,source=phases[j]['source'],target=phases[j]['target'],multiplier=1,weight=phases[j]['weight']) for j in ds]
        expected_lift += [dict(kind='ROOT_KEEP',source=i,target=states[i]['projection'],key=states[i]['root_A'],multiplier=value,weight=-states[i]['Q']) for i,value in mu]
        ck(expected_lift == control['lifted_circulation'], 'every lifted edge is an exact source edge')
        incidence = [0]*len(states);lw=0
        for e in expected_lift:
            ck(type(e['multiplier']) is int and e['multiplier'] > 0, 'multiplier sign')
            incidence[e['source']]-=e['multiplier'];incidence[e['target']]+=e['multiplier']
            lw += e['multiplier']*e['weight']
        ck(incidence == control['lifted_incidence'] and not any(incidence), 'physical incidence zero, not merely projected balance')
        ck(grad == sum(value*states[i]['Q'] for i,value in mu) == Q and
           lw == control['lifted_weight'] == wd-grad == 2*A-Q == 28 and not control['negative_certificate'], 'same exact constant; positive control is not a contradiction')
        total_full+=len(full);total_split+=len(phases);total_states+=len(states);total_lift_edges+=len(expected_lift)
    ck(len(cert['controls']) == 2 and cert['potential_fits'] == cert['state_graph_searches'] == cert['larger_key_sizes'] == 0 and
       not cert['new_CD_counterexample'] and cert['matching_terminal_line'] == 'FROZEN BY USER', 'scope and freeze')
    result = dict(status='PASS',date='2026-10-31',existing_control_and_reflection=True,
                  complete_whole_source_rows=total_full,complete_split_source_rows=total_split,
                  state_records_with_multiplicity=total_states,lifted_edge_records=total_lift_edges,
                  pointer_source_accesses=calls,producer_imported=False,optimizer_used=False,
                  terminal_coefficient_residuals=[0,0],physical_incidence_residuals=[0,0],
                  H_coefficient_signs_valid=True,closed_walk_weights=[28,28],
                  all_listed_states_source_reachable=True,new_CD_counterexample=False,
                  potential_fits=0,source_graph_searches=0,larger_key_sizes=0,
                  matching_terminal_line='FROZEN BY USER',
                  universal_lifting_theorem='analytic proof in FF02, not inferred from finite controls',
                  certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE / 'independent_audit.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()

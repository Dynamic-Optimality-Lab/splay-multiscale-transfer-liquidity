"""Preflight source/incidence audit on an existing closed word; no potential search."""
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

def save(name,value):
    with (HERE / name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    oldpins = json.loads((PARENT / 'route_c_contained_terminal_20261031_v001/entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(oldpins['files'])
    for rel,value in oldpins['files'].items():
        assert sha(ROOT / rel) == value, rel
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert len(stage) == 125
    status = git('status','--porcelain=v1','--untracked-files=no')
    assert not status
    save('entry_source_pins.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),
         branch=git('branch','--show-current'),tracked_status=status,files=pins,
         stage_files=stage,inherited_pins=len(oldpins['files'])))
    spec = importlib.util.spec_from_file_location('tuple_source',ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    L = s.LEAF
    def tup(t):
        return L if t is None else s.node(t[0],tup(t[1]),tup(t[2]))
    def raw(t):
        return None if t == L else [t[1],raw(t[2]),raw(t[3])]
    def mirror(t):
        return L if t == L else s.node(7-t[1],mirror(t[3]),mirror(t[2]))
    oldpath = PARENT / 'route_c_analytic_20261030_v001/six_key_closed_controls.json'
    old = json.loads(oldpath.read_text(encoding='utf-8'))['controls'][0]
    def audit(name,initial,word):
        nodes,tuples,index = [],[],{}
        def state(a,b,origin):
            pair = a,b
            if pair not in index:
                index[pair] = len(nodes);tuples.append(pair)
                nodes.append(dict(A=raw(a),B=raw(b),origin=origin))
            return index[pair]
        a,b = initial,initial
        start = state(a,b,dict(kind='diagonal_start'))
        full,phases = [],[]
        A=Q=Z=0
        for wi,(mode,x) in enumerate(word):
            u = state(a,b,dict(kind='walk_prefix',phase=len(phases)))
            ap,ae = s.trace(a,x);da = s.lookup(a,x)[1];ac = len(ae)
            ck = (da+1)//2
            assert ac == ck and ap[1] == x
            mid = state(ap,b,dict(kind='walk_prefix',phase=len(phases)+1))
            phase_start = len(phases)
            phases.append(dict(mode='D',key=x,source=u,target=mid,d_A=da,d_B=None,
                               a=ac,q=0,z=0,A_events=ae,B_events=[],weight=2*ac,
                               original_row=wi))
            if mode == 'K':
                bp,be = s.trace(b,x);db = s.lookup(b,x)[1]
                q = sum(e[0] != 'ZIG' for e in be);z = sum(e[0] == 'ZIG' for e in be)
                assert q == db//2 and z == db%2
                same,noop = s.trace(ap,x)
                assert same == ap and not noop
                v = state(ap,bp,dict(kind='walk_prefix',phase=len(phases)+1))
                phases.append(dict(mode='K',key=x,source=mid,target=v,d_A=0,d_B=db,
                                   a=0,q=q,z=z,A_events=[],B_events=be,weight=-q,
                                   original_row=wi,root_aligned=True))
            else:
                bp,be,db,q,z,v = b,[],None,0,0,mid
            full.append(dict(mode=mode,key=x,source=u,intermediate=mid,target=v,
                             d_A=da,d_B=db,a=ac,q=q,z=z,A_events=ae,B_events=be,
                             weight=2*ac-q,phase_indices=list(range(phase_start,len(phases)))))
            A+=ac;Q+=q;Z+=z;a,b=ap,bp
        end = state(a,b,dict(kind='walk_prefix',phase=len(phases)))
        assert end == start and (A,Q,Z) == (16,4,2)
        # Add only deterministic completions of the visited states. No graph search.
        i = 0
        while i < len(nodes):
            a,b = tuples[i];r = a[1]
            cb,ev = s.trace(b,r);d = s.lookup(b,r)[1]
            q = sum(e[0] != 'ZIG' for e in ev);z = sum(e[0] == 'ZIG' for e in ev)
            assert q == d//2 and z == d%2
            pi = state(a,cb,dict(kind='completion',of_state=i,key=r))
            nodes[i].update(root_A=r,terminal=a[1] == b[1],projection=pi,
                            Q=q,completion_depth=d,completion_z=z,completion_events=ev)
            i += 1
        c = [0]*len(nodes)
        d_indices = [i for i,e in enumerate(phases) if e['mode'] == 'D']
        for j in d_indices:
            e = phases[j];c[e['target']]+=1;c[e['source']]-=1
        projected = [0]*len(nodes)
        for i,value in enumerate(c):
            projected[nodes[i]['projection']] += value
        assert not any(projected)
        assert all(value >= 0 for i,value in enumerate(c) if not nodes[i]['terminal'])
        rhs_D = sum(phases[i]['weight'] for i in d_indices)
        q_gradient = sum(nodes[phases[i]['target']]['Q']-nodes[phases[i]['source']]['Q'] for i in d_indices)
        mu = {i:value for i,value in enumerate(c) if not nodes[i]['terminal'] and value > 0}
        lift = [dict(kind='DELETE',phase_index=i,source=phases[i]['source'],target=phases[i]['target'],
                     multiplier=1,weight=phases[i]['weight']) for i in d_indices]
        for i,mult in sorted(mu.items()):
            lift.append(dict(kind='ROOT_KEEP',source=i,target=nodes[i]['projection'],
                             key=nodes[i]['root_A'],multiplier=mult,weight=-nodes[i]['Q']))
        incidence = [0]*len(nodes)
        for e in lift:
            incidence[e['source']]-=e['multiplier'];incidence[e['target']]+=e['multiplier']
        lift_weight = sum(e['weight']*e['multiplier'] for e in lift)
        assert not any(incidence)
        assert rhs_D-q_gradient == lift_weight == 2*A-Q == 28
        assert q_gradient == sum(value*nodes[i]['Q'] for i,value in mu.items()) == Q
        return dict(name=name,n=6,initial_A=raw(initial),initial_B=raw(initial),word=word,
                    states=nodes,full_rows=full,split_rows=phases,initial_state=start,final_state=end,
                    A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,paired_closure=True,
                    DELETE_phase_indices=d_indices,DELETE_multipliers=[1]*len(d_indices),
                    H_coefficients=c,projected_Theta_coefficients=projected,
                    added_B_multipliers=[[i,m] for i,m in sorted(mu.items())],
                    DELETE_weight_sum=rhs_D,DELETE_Q_gradient=q_gradient,
                    contradiction_rhs=rhs_D-q_gradient,lifted_circulation=lift,
                    lifted_incidence=incidence,lifted_weight=lift_weight,
                    negative_certificate=False)
    initial = tup(old['initial_A']);word = old['word']
    first = audit('existing_six_key_L_closed_word',initial,word)
    # Compare only inherited physical replay fields; old histogram/matching data are not imported.
    for new,prior in zip(first['full_rows'],old['full_replay']):
        u,v = first['states'][new['source']],first['states'][new['target']]
        assert (u['A'],u['B'],v['A'],v['B']) == (prior['source_A'],prior['source_B'],prior['destination_A'],prior['destination_B'])
        assert (new['a'],new['q'],new['weight']) == (prior['a'],prior['q'],prior['signed_weight'])
    reflected = audit('existing_six_key_L_reflection',mirror(initial),[[mode,7-x] for mode,x in word])
    cert = dict(schema='full-form-source-lifting-preflight-v1',date='2026-10-31',
                inherited_control_file=oldpath.relative_to(ROOT).as_posix(),
                inherited_control_sha256=sha(oldpath),controls=[first,reflected],
                normal_form_restriction='none beyond weak B inequality',
                unrestricted_obstruction_campaign='NOT LAUNCHED—FAILED PREFLIGHT',
                new_CD_counterexample=False,potential_fits=0,state_graph_searches=0,
                larger_key_sizes=0,matching_terminal_line='FROZEN BY USER')
    save('full_form_source_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),
         controls=[dict(name=v['name'],full_rows=len(v['full_rows']),split_rows=len(v['split_rows']),
              states=len(v['states']),A=v['A'],Q_B=v['Q_B'],weight=v['weight'],
              H_signs_valid=True,Theta_residual=0,lifted_incidence_residual=0) for v in cert['controls']]),indent=2))

if __name__ == '__main__':
    main()

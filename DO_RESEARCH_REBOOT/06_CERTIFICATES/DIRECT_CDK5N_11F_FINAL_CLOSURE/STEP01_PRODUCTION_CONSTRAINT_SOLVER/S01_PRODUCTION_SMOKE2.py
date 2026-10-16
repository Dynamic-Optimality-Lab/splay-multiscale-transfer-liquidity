# S01_PRODUCTION_SMOKE2.py — grounded production tests (S2-S5), incremental (S6),
# adversarial extras + Step-02 capped preview (optional), resource accounting (S8).
import sys, json, time, ctypes
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER/'
RES = {}
FAIL = []


def rec(section, name, ok, detail=''):
    RES.setdefault(section, []).append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
    print('%-10s %-46s %s %s' % (section, name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append((section, name, detail))


def proc_peak_mb():
    try:
        class PM(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                        ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
        pm = PM()
        pm.cb = ctypes.sizeof(PM)
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        h = k32.GetCurrentProcess()
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PM), ctypes.c_ulong]
        if psapi.GetProcessMemoryInfo(h, ctypes.byref(pm), pm.cb):
            return round(pm.PeakWorkingSetSize / 1048576, 1)
    except Exception:
        pass
    return None


import splay as S
from PC_TYPED_DAG import DAG
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S01_INCREMENTAL_ENGINE import IncrementalEngine
from S01_INDEPENDENT_ORACLE import witness_check
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc, abs_pins


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def canon(env):
    out = {}
    for k, v in env.items():
        out[k] = bool(v) if isinstance(v, bool) else int(v)
    return out


if __name__ == '__main__':
    T = {}
    t0 = time.process_time()
    d = DAG()
    L = build_slow(d, 'SL')
    T['build_s'] = round(time.process_time() - t0, 1)
    print('low nodes=%d build_cpu=%.1fs' % (d.count(), T['build_s']), flush=True)
    Sset = set(range(1, 10))
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    A9 = S.balanced(list(range(1, 10)))
    cases = [
        ('E3', A, B, set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1, 1, 3, -1),
        ('plain', A9, A9, Sset, {1, 2, 3, 4, 5}, [('K', 3)], 1, 1, 0, 2),
        ('delkeep', A9, A9, Sset, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2, 2, 0, 4),
    ]
    eng = IncrementalEngine(d, seed=17, timeout_ms=120000)
    t0 = time.process_time()
    h = eng.compile_once(L['root'], 'slow')
    T['compile_s'] = round(time.process_time() - t0, 1)
    print('compiled decls=%d bounds=%d translate=%ss' % (h['comp']['stats']['decls'], h['comp']['stats']['int_bounds'], h['comp']['stats']['translate_s']), flush=True)
    G = []
    for (name, AA, BB, SS, M, word, H, eH, eq, ew) in cases:
        st, info = ssertify(d, L, serial(AA), serial(BB), SS, M, word, H)
        okg = (st == 'ok' and info['H'] == eH and info['q'] == eq and info['w'] == ew)
        rec('S2-S4', name + ' grounded H/q/w', okg, '%s H=%s q=%s w=%s' % (st, info.get('H'), info.get('q'), info.get('w')))
        if not okg:
            G.append({'case': name, 'grounded': st})
            continue
        full = canon(info['env'])
        # oracle confirms the claimed witness on the ORIGINAL formula (independent)
        ow = witness_check(d, L['root'], full)
        rec('S2-S4', name + ' oracle witness', ow is True, str(ow))
        # original interpreter agreement on the TRUE ground witness (quantifier-free root)
        ev = d.ev_iter(L['root'], full)
        rec('S2-S4', name + ' interpreter agrees', ev is True, str(ev))
        t0 = time.process_time()
        r = eng.query('slow', full)
        dt = round(time.process_time() - t0, 2)
        ok = r['status'] == SAT
        mh = {}
        if ok:
            m = eng.ps.extract_model(h, r)
            mh = {'H': m.get('SL_H'), 'q': m.get('SLbt_q'), 'w': info['w']}
            ok = (mh['H'] == eH and mh['q'] == eq and mh['w'] == ew)
        rec('S2-S4', name + ' compiled SAT H/q exact', ok, '%s cpu=%s model=%s' % (r['status'], dt, mh))
        G.append({'case': name, 'grounded': 'ok', 'H': eH, 'q': eq, 'w': ew,
                  'compiled': r['status'], 'cpu_s': dt, 'model_Hq': mh,
                  'oracle': True if ow is True else str(ow)})
    J('S01_GROUNDED_PRODUCTION_TESTS.json', G)

    # ---------- S5: invalid rejection ----------
    I = []
    full_e3 = None
    st, info = ssertify(d, L, serial(A), serial(B), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    assert st == 'ok'
    full_e3 = canon(info['env'])
    # (a) contradictory session pins (assumption machinery soundness)
    with eng.session('slow') as ses:
        ses.pin({'SL_H': 1})
        r = ses.query({'SL_H': 2})
        oka = (r['status'] == UNSAT)
        rec('S5', 'contradictory pins UNSAT', oka, r['status'])
        I.append({'test': 'contradiction', 'status': r['status']})
    # (b) out-of-domain pin violates width bounds
    r = eng.query('slow', dict(full_e3, SL_H=1 << 40))
    okb = (r['status'] == UNSAT)
    rec('S5', 'out-of-domain UNSAT', okb, r['status'])
    I.append({'test': 'out-of-domain', 'status': r['status']})
    # (c) semantic invalid: flip H (functionally determined H=1 -> H=2 must reject)
    r = eng.query('slow', dict(full_e3, SL_H=2))
    okc = (r['status'] == UNSAT)
    rec('S5', 'flipped-H rejected', okc, r['status'])
    I.append({'test': 'flipped-H', 'status': r['status']})
    # (d) corrupt a target-identity bit: probe candidate flips, gate on a rejecting one
    bad = None
    for tk in sorted(k for k in full_e3 if k.startswith('SLt_')):
        v = full_e3[tk]
        nv = (not v) if isinstance(v, bool) else (1 - v if v in (0, 1) else v + 1)
        r = eng.query('slow', dict(full_e3, **{tk: nv}))
        if r['status'] == UNSAT:
            bad = (tk, r['status'])
            break
    rec('S5', 'corrupt-target rejected', bad is not None, str(bad))
    I.append({'test': 'corrupt-target', 'key': bad[0] if bad else None, 'status': bad[1] if bad else 'SAT-all'})

    # ---------- S6: incremental, one compile, many queries ----------
    NCOMP = len(eng.ps.handles)
    r_a = eng.query('slow', full_e3)
    pins_plain = canon(ssertify(d, L, serial(A9), serial(A9), Sset, {1, 2, 3, 4, 5}, [('K', 3)], 1)[1]['env'])
    r_b = eng.query('slow', pins_plain)
    r_c = eng.query('slow', dict(full_e3, SL_H=2))
    with eng.session('slow') as ses:
        ses.pin(abs_pins(full_e3))
        r_d = ses.query(timeout_ms=30000)
        r_e = ses.query({'SL_H': 2})
    indep = (r_a['status'] == SAT and r_b['status'] == SAT and r_c['status'] == UNSAT and r_d['status'] in (SAT, UNKNOWN) and r_e['status'] == UNSAT)
    rec('S6', 'one compile many queries independent', indep and len(eng.ps.handles) == NCOMP,
        'A=%s B=%s C=%s D=%s E=%s handles=%d' % (r_a['status'], r_b['status'], r_c['status'], r_d['status'], r_e['status'], len(eng.ps.handles)))
    INC = {'handles': len(eng.ps.handles), 'A': r_a['status'], 'B': r_b['status'], 'C': r_c['status'],
           'D_session': r_d['status'], 'E_session': r_e['status'],
           'stats': eng.ps.solver_statistics(h)}
    J('S01_INCREMENTAL_RESULTS.json', INC)

    # ---------- optional Step-02 preview: endpoint pins only, tight cap ----------
    ep = abs_pins(full_e3)
    rp = eng.query('slow', ep, timeout_ms=60000)
    preview = {'pins': len(ep), 'status': rp['status'], 'reason': rp.get('reason', ''), 'cpu_s': rp.get('cpu_s')}
    rec('PREV', 'endpoint-only preview recorded', True, str(preview))
    J('S01_PREVIEW.json', preview)

    # ---------- S8 resource accounting ----------
    ledger = {'build_cpu_s': T['build_s'], 'compile_cpu_s': T['compile_s'],
              'solve_cpu_s_total': round(eng.ps.cpu_s, 1),
              'queries': eng.ps.query_count, 'peak_ram_mb': proc_peak_mb(),
              'caps': {'cpu_h_step01': 4.0, 'mem_gib': 32, 'dag_nodes': 4000000},
              'dag_nodes_used': d.count()}
    J('S01_RESOURCE_LEDGER.json', ledger)
    rec('S8', 'caps respected', ledger['dag_nodes_used'] <= 4000000 and (ledger['build_cpu_s'] + ledger['compile_cpu_s'] + ledger['solve_cpu_s_total']) / 3600.0 <= 4.0, str(ledger))
    J('S01_PART2.json', {'RES': RES, 'FAIL': FAIL})
    print('PART2 done', ledger, flush=True)
    assert not FAIL, FAIL

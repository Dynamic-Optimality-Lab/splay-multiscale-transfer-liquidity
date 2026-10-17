# G01_CONTRACTED_EDGE_CHECKER.py — C1/C2 executable check (Phase C/K3).
# check_contraction(dag, EOM, EMO, contracted, m, s_pins, t_pins, decide):
# verifies expansion direction on grounded witnesses (m given): EOM(s,m) and
# EMO(m,t) both SAT. Contraction direction is structural (same conjunction).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')


def check_contraction(EOM_w, EMO_0, contracted, s_pins, m_pins, t_pins, decide):
    """decide(root, pins) -> (status, model, reason). Returns dict of sub-verdicts."""
    r1 = decide(EOM_w, dict(s_pins, **m_pins))
    r2 = decide(EMO_0, dict(m_pins, **t_pins))
    r3 = decide(contracted, dict(s_pins, **t_pins))
    return {'EOM_sat': r1[0], 'EMO_sat': r2[0], 'contracted': r3[0],
            'expansion_holds': r1[0] == 'SAT' and r2[0] == 'SAT',
            'detail': (r1[2], r2[2], r3[2])}

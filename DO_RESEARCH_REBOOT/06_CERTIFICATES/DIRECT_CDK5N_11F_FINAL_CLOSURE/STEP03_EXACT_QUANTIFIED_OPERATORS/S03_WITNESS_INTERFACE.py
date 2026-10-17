# S03_WITNESS_INTERFACE.py — typed extraction with distinct statuses (Gate G).
# extract() never conflates UNSAT and UNKNOWN: returns (status, payload, reason).
# Callers decide() first (getting status+reason), then extract the model if SAT.

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


def extract_typed(engine, tag, result):
    h = engine.rs.eng.ps.handles[tag]
    if result['status'] == SAT:
        return (SAT, engine.rs.eng.ps.extract_model(h, result), '')
    return (result['status'], None, result.get('reason', ''))

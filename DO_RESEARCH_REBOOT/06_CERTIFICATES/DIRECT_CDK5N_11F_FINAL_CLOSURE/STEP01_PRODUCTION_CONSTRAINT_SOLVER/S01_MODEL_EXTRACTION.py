# S01_MODEL_EXTRACTION.py — model recovery + independent re-check.
# A solver SAT is never presented as source-valid on its own word: the extracted free
# assignment is re-evaluated by the independent scoped oracle (and, on ground formulas,
# by the historical interpreter) before any downstream use.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')


def extract_and_verify(ps, handle, result, oracle_truth):
    """Returns (assignment, oracle_verdict). oracle_truth: callable(assign)->True/False/None.
    Raises unless the oracle independently confirms True."""
    assign = ps.extract_model(handle, result)
    v = oracle_truth(assign)
    if v is not True:
        raise AssertionError(('model failed independent re-check', v))
    return assign, v

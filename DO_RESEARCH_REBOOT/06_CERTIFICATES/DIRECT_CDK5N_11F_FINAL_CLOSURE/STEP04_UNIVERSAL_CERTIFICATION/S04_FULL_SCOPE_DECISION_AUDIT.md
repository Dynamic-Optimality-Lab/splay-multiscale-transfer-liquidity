# S04_FULL_SCOPE_DECISION_AUDIT.md — F04-21/F04-26 (Gates A4/B/F)

No free CL/CH/SL/event/port/atom/B-trace/q/H/root variables in any projected
edge (24/24 audits re-passed on fresh rebuild). Step-02 a-incomplete and
word-truncated Branco return UNKNOWN at every call site audited (engine,
MinPreDecider, production tests): grep-verified no path coerces them to UNSAT;
CERTIFIED_UNSAT membership is closed and documented. Tier-1 const decisions are
exact (simplify semantics); Tier-2/z3-tiny decisions are solver-complete on
their queries; UNKNOWN carries backend reasons. Mandatory execution list
(J1-J10, 4070 small-graph, G2/Q1/Q2/high/chain re-runs) all decided.

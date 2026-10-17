# S04_OPERATOR_EXECUTION_AUDIT.md — F04-22/F04-23/F04-24/F04-25/F04-26

Pre/Post/MinPre + 15-function algebra executed: 4070/4070 small-graph decisions
(pre/post/minpre/empty/equiv/extract/nested/complement, exhaustive X subsets)
plus production memberships (J1-J5/J9 engine SAT, J10a Tier-1 UNSAT), MinPre
decisions (J7 FALSE via certified lower edge, J8 TRUE via certified absences),
general target predicates (disjunctions via OR-predicates, complements,
mixed-sort, empty/full, nested — all in the 4070). Mandatory queries all
decided (zero mandatory UNKNOWN). Lazy MinPre == eager symbolic (alpha-equivalence
+ procedure equivalence proof). Two capture defects found and repaired additively
in Step 03. No formula merely constructed where execution was required: every
cited verdict names its decision path (engine/Tier-1/Z3-tiny).

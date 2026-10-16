# S01_ACCEPTANCE_GATES.md — S01-G01..G20 evaluation (evidence-linked)

| Gate | Requirement | Verdict | Evidence |
|---|---|---|---|
| G01 | entry HEAD + hashes | PASS | `a76354b`, 4/4 SHA256 match (S01_ENTRY_AUDIT.md) |
| G02 | stack frozen | PASS | S01_BACKEND_FREEZE.json + RATIONALE (Z3 5.1.0, no switch) |
| G03 | rules + caps | PASS | four-rule freeze; S8 caps check |
| G04 | all operators translated | PASS | 13/13 kinds; unknown kinds raise; 150/150 agreement |
| G05 | exact arithmetic/signedness | PASS | width audit (1 signed var); overflow UNSAT; signed tests |
| G06 | existential/negation scope | PASS | Q1 UNSAT, Q3/Q6/Q7 (compiled + oracle) |
| G07 | free/bound collisions | PASS | Q2 model z=0; double-bind ±; rename roundtrip |
| G08 | nested quantifiers | PASS | Q3/Q4/Q5; MinPre control pair |
| G09 | sharing preserved | PASS | nid->expr cache; sharing factor; norm_growth=0 on production |
| G10 | full product compiles | PASS | 1,603,069 nodes; low/high/Esm/Emt/Elow handles |
| G11 | incremental, no recompile | PASS | 1 handle, 6 query shapes; session independence |
| G12 | E3 SAT H=1,q=3,w=-1 | PASS | compiled SAT 2.5 s + oracle + interpreter triple agreement |
| G13 | ordinary KEEP SAT | PASS | H=1,q=0,w=2, same triple agreement |
| G14 | DELETE+KEEP SAT | PASS | H=2,q=0,w=4, same triple agreement |
| G15 | invalid rejected | PASS | 4/4 (contradiction, domain, flipped-H, corrupt-target) |
| G16 | oracle agreement | PASS | 150/150 + 9/9 Q + 12/12 AR + 3 grounded triples |
| G17 | SAT/UNSAT/UNKNOWN correct | PASS | all three with reasons; preview UNKNOWN `canceled` honest |
| G18 | reproducible evidence | PASS | scripts + 12 JSONs + manifest (below) |
| G19 | caps respected | PASS | DAG 1.70M/4M; RAM 2.43/32 GiB; Step-01 CPU ~1.0/4.0 h |
| G20 | independent verification | PASS | separate oracle implementation; every claim cross-checked |

STEP 01 COMPLETE <=> all 20 PASS: **HOLDS (20/20)**.
Full free-witness synthesis was NOT attempted (reserved Step 02); the 60 s
endpoint-only preview returned UNKNOWN `canceled` and is recorded as such.

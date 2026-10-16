# FINAL_CLOSURE_DEPENDENCY_PLAN.md

1. **Step 01 (authorized now)**: production constraint solver — compile 1.6M-node DAG once,
   exact Int semantics, scoped EXISTS, incremental push/pop + assumptions, model extraction,
   20 acceptance gates. Output: frozen solver stack + compiled product + smoke evidence.
2. **Step 02 (not authorized)**: free-witness synthesis on abstract endpoint pins only,
   using the Step 01 engine. Depends on: compiled product handle, assumption interface,
   resource remainder (4.0 CPU-h).
3. **Step 03 (not authorized)**: exact quantified Pre/Post/MinPre over the compiled backend.
   Depends on: scoped-binder correctness (Q1–Q8), incremental quantified queries.
4. **Step 04 (not authorized)**: universal certification + Stage 11F closure verdict.
   Depends on: Steps 01–03 evidence + 15% verification reserve. HARD STOP after each step.

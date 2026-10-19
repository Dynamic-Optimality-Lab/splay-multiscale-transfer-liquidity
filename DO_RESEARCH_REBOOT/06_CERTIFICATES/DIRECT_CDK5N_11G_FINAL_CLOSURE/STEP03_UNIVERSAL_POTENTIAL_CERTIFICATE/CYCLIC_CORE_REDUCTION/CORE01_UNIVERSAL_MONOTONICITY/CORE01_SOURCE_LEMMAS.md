# CORE-01 Source DELETE + Nongenuine KEEP Lemmas (Gate B)

DELETE: b_splay_event gated by is_delete -> all blends select old state;
B identical -> C_M identical. PROVED (code). Nongenuine KEEP: splay runs
(isK=True -> eff_del False); if target unmarked and outside C_M, the
rotation corollary does NOT apply. Characterization (PROVED, same
machinery): an unmarked-target splay can add AT MOST its target to C_M
(only the target can gain marked descendants; all other nodes hold or
shrink — same proof with x possibly outside). Measured (imported):
0 growth / 1118 marked splays; growth in 978/1882 unmarked splays
(STRICT_CORE_Q_TESTS.json). Minimal refuting source operation: nongenuine
KEEP of unmarked non-ancestor key to root (e.g. B=10(1,20), M={20},
KEEP(1): C_M {10,20} -> {1,10,20}; replay-verified). So universal
SOURCE-level monotonicity is REFUTED; marked-target case PROVED.

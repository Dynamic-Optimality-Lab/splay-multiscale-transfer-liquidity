# PP_SOURCE_AUDIT.md — source integrity + Bank25 + entry HEAD

## Entry HEAD (frozen)
- Local HEAD `63140243e710eb7d504bca172e0181f43ae3a727` == FETCH_HEAD `63140243e710eb7d504bca172e0181f43ae3a727` (matches mission reference checkpoint; no reset performed).

## Source hashes (SHA256, verified 2026-10-14)
| File | SHA256 | Status |
|---|---|---|
| scripts/wp6_eventflow.py | d7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053 | MATCH |
| scripts/wp6_coarse_double.py | b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f | MATCH |
| python/independent/splay.py | 3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01 | MATCH |
| python/liquidity/legacy_embedding.py | 20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2 | MATCH |

Note: `git rev-parse` (SHA1 blob) differs textually from these SHA256 values; comparison done via `hashlib.sha256` over working-tree bytes. Last source modification predates all coarse-double campaigns (commits 88d3007/2e925b2/b9a52d0). Working tree clean for `scripts/`, `python/`.

## Bank25
- `BANK25_NAMES` (GLOB_bank25.py:36-39) enumerates exactly 25 lemmas: RT2, CDK4, CDK5L, NP, S1, S2, VR, MR, MSINK, DLSS, UESINK, ZULR, SELR, AJ, AK, ALG, ALS, AMG, AMS, AN, AO, AP, AQ, AR, AS. Count = 25. No promotions since SELR (all intervening verdicts: no promotion). **Bank25 remains at 25.**

## Persistent-port diagnostic directory
- `DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_CAUSAL_GATE/` is **ABSENT** (confirmed by listing). No attached experiment package was delivered in-session. Construction below is built source-directly from `python/independent/splay.py` + AFSP cone/ordered-hole results; nothing is pretended to be imported.

## Gate PP-01: PASS (4/4 sources, Bank25@25, HEAD frozen).

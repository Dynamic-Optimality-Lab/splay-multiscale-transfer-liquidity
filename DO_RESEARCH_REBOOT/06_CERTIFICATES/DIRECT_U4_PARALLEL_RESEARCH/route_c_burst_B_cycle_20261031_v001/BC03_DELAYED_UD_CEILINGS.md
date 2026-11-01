# Delayed guard facts do not force minimum-pool repayment

Status: FINITE-EXACT for all 48 entries on the source cycle. The interpretation via the already established UD rule and earlier-lap monotonicity is PROVED—RESTRICTED DOMAIN. This is not an all-cut UD rejection certificate for any actual A/B walk.

The B cycle has exactly two potential positive anchors: occurrence 0, K13 with q=6, and occurrence 1, K11 with q=3. Every other KEEP has q<=2 and could be a nonpositive minimum-capacity payer. Every B access changes B, including all fifteen zig-only accesses.

For an anchor i and a forward cyclic payer j, the old-UD ceiling is

    c_i(j)=floor(h_i(key_j)/2)+k_i(j),

where h_i is the exact depth in the post-anchor B tree and k_i(j) counts genuine intervening B changes. DELETEs do not change this value. The independent pointer audit evaluates all 24 nonpositive-potential positions from each of the two anchors, at forward separations 1,...,25. It does not select only the former-root or collar keys.

| Anchor | Number of evaluated potential payers | Minimum UD own-work ceiling |
| --- | ---: | ---: |
| K13 at occurrence 0 | 24 | 3 |
| K11 at occurrence 1 | 24 | 2 |

All 48 ceilings are >=2. A cyclic cut can discard an unavailable positive history fact; taking a minimum over fewer facts cannot reduce these values. If an anchor is actually nonpositive it supplies no UD fact, which likewise cannot reduce a minimum. An earlier-period copy of the same source anchor adds 26 genuine B changes per lap to its ceiling, so it cannot create a smaller value. The one-period recognizer does not use preceding-lap history anyway; this observation rules out a hidden low ceiling from periodic repetition.

Therefore every minimum two-unit nonpositive KEEP pool reserves all of its units under old UD, whether the applicable history contains either anchor, both, or neither. It has no guaranteed outgoing suffix. This is a statement about UD's conservative reservation formula; it does not say that a low-q access has no actual unused units.

The immediate next queries illustrate the distinction. K11 has q=3 and fresh ceiling 3; it may itself be positive with a two-unit pool. K9 has q=2 and fresh ceiling 2, exhausting a two-unit pool. A larger actual A pool could lend, and would change possible excess. No actual A costs have been assigned by this B calculation.

## Literal old-root returns

For K13, the old B root is key 1. Its post-anchor depth is 2, but its next occurrence is only after two intervening genuine B changes, K11 and K9. At the later K1,

    c_13(K1)=floor(2/2)+2=3.

The other anchor's fact lowers the combined ceiling there to 2, still exhausting a minimum two-unit pool.

For K11, the old B root is key 13. Its post-anchor depth is 1, but its next occurrence is the hot K13 of the next B period, after 24 intervening B changes. Its old-UD ceiling is 24 and its actual B cost is q=6; it is not a cheap guard return.

The sole turnaround ABA 11,12,11 is centered at a nonpositive-potential access with q=1. It does not supply a fresh positive-anchor fact. Renaming guards or ignoring zig changes was not used to avoid the old obstruction.

## Quantifiers and remaining burden

The complete 48-row table is delayed_UD_ceiling_profile.json. Both source engines agree on all input/post trees, and the pointer engine checks exact reflected source symmetry. The arbitrary-fringe substitution in BC01 preserves the requested-key depths and all intervening-change counts, so these conclusions extend to every finite untouched outer fringe without another finite replay.

This removes the automatic repayment that follows just from the existing positive-anchor facts plus minimum two-unit KEEP pools. It does not prove that an actual closed paired source walk can realize those minimum pools, that two pure resets suffice, that its true excess E exceeds C_D, or that all larger A pools are unhelpful. A-only PURE blocks themselves have ceiling zero and do repay pending debt. Nonpositive high-q positions with larger A pools can also lend. Those coupling possibilities remain open. No A history, FI first-intervention ledger or cut recognizer is executed in this run.

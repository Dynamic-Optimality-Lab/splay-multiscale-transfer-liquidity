# Actual-state repayment on the overwritten-setup witness

**Scope: the seven-key saved source witness; this is a finite pointwise consequence of the complete certificate.**

The original eligibility graph still fails at K7: its three demands have only the two D7 setup units. The new state potential does not use that eligibility graph or latest-setup identifiers.

|Operation|a|q|Phi source|Phi destination|drop-(q-2a)|
|---|---|---|---|---|---|
|D6|3|0|-2|0|4|
|D7|1|0|0|0|2|
|K7|0|3|0|-3|0|
|D6|1|0|-3|-1|0|
|K6|0|1|-1|-3|1|
|D5|2|0|-3|-1|2|
|K5|0|1|-1|-3|1|
|D4|1|0|-3|-1|0|
|K4|0|0|-1|-3|2|
|D3|1|0|-3|-1|0|
|K3|0|1|-1|-3|1|
|D2|1|0|-3|-1|0|
|K2|0|0|-1|-2|1|
|D1|1|0|-2|0|0|
|K1|0|0|0|-2|2|

At the beginning Phi=-2. D6 has a=3 and raises Phi from -2 to0; the following D7 has a=1 and leaves Phi0 unchanged. K7 has a=0,q=3 and drops Phi from0 to-3, paying its entire demand. Thus the D6 state change remains visible through the overwritten D7 setup. Nothing restricts payment to D7's two units.

Equivalently, the shifted bank Phi+3 starts at1, receives2 during D6, stays at3 during D7 and consumes3 at K7. These are potential values, not an asserted injection into specific historical credit IDs. No credit matching theorem is inferred from this bank description.

The entire closed word has reward Q-2A=-16 and total potential drop0. Every inequality was checked independently. Potential decreases on some weight-zero operations too: K4 has a=q=0 but executes a B zig and drops the potential by2. Weight zero does not mean inert state or neutral future reserve.

The five-KEEP/nine-core physical witness was independently replayed as an INPUT REGRESSION only (32 accesses,A34,Q18,exact closure). Phi7 is undefined for its nine-key states. Its potential payment was NOT checked or claimed. The all-n overwritten-setup family likewise remains an all-size acceptance test, not a domain covered by this finite table.

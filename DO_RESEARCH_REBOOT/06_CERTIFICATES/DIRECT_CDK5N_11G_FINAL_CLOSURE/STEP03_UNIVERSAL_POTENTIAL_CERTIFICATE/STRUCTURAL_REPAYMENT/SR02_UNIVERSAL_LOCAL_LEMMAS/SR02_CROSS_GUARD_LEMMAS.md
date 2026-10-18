# SR02 Cross-Guard Lemmas

01 (shallow->deep, DC5+d(t)<=w): NO grounded samples in 166 edges; NOT
proved impossible (rotation pushdown can in principle raise dmax; +2 jumps
observed at lower depths, e.g. 4->6). First unresolved structural case.
10 (deep->shallow, DC5-d(s)<=w): 57 grounded samples, 0 violations; d(s)
= R_M-D+M with D>=7 gives d(s) <= R_M+M-7 (bounded above; sign/magnitude
depend on R_M+M, unbounded a priori) — universal bound OPEN.
Required for SR-03: either an impossibility proof for 01-crossings, or a
universal d(t)/DC5 coupling bound, or a verified symbolic UNSAT of V
(01-class violation query). None available in SR-02 budget (symbolic
0->1 probes exceed cap; recorded with Rescue-02 pinned-query timeouts as
supporting evidence of cost).

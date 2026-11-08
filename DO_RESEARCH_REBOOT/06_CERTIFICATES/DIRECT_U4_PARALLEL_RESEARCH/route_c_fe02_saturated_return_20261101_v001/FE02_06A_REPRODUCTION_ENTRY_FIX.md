# Saved entry helper clarification

For fresh reproduction, use `capture_entry_v002.py` in place of the first
command's `capture_entry.py` in FE02_06. All remaining commands are unchanged.

The retained scientific entry capture succeeded inline before implementation.
The later, unexecuted saved V001 helper had an incorrect dictionary key in
its final progress print ONLY. V002 transparently fixes that print, retains
V001, and changes no capture predicate, input, source theorem, audit or result.
Neither helper is run over the already sealed entry pins. This clarification
is append-only, like all other FE02 artifacts.

# Reproduction and preservation

Use Python with -B. Do not rerun writer commands in a sealed historical directory. No installation is required. All source, native predicate and independent-engine paths are inherited from base6.py and its sealed parent chain. All new native report ROOTs are redirected by native6.py.

Read-only verification in THIS delivered directory:

```powershell
python -B finalize6.py --verify-only
```

This checks the exact C6 inventory, all recursive historical seals and unchanged Git HEAD/branch/tracked bytes. It writes no receipt or cache. The expected principal result is E and M1 remains OPEN.

For a fresh semantic reproduction, copy this directory's .py and .md inputs to a NEW unsealed scratch sibling under the SAME EXP04 base (so the relative inherited paths resolve). Do not copy any manifests, receipts, generated JSON or old native reports into that scratch directory. Then run these commands sequentially IN THE SCRATCH DIRECTORY:

```powershell
python -B base6.py
python -B sources6.py
python -B audit6.py 0
python -B audit6.py 1
python -B audit6.py 2
python -B audit6.py 3
python -B audit6.py 4
python -B audit6.py 5
python -B shadow6.py --historical-only
python -B shadow6.py --fresh-only
python -B finalize6.py
python -B finalize6.py --verify-only
```

Generation constructs full exact paired-closed sources; no truncated core substitutes for the restoration word. The maximum535-key native audit is substantially slower than the small controls. Operational allocation was1800 measured script CPU seconds,6 fresh complete sources, population<=600, word<=40000 and per-process peak aim2GiB. RESOURCE_RECORD gives actual measurements and unmetered scopes; these are execution limits, not theorem premises.

audit6.py saves full PHYS/FOREST/WEIGHTS/M1_AUDIT/BIRTH/ORDERED/REDUCTION/RENEWAL/NESTED records for each fresh index. local6.py uses the frozen original raw/G/H local functions; independent6.py independently rechecks the source, original predecessor and prices. shadow6.py audits only the stated selected history scopes. finalize6.py reconciles every native original rho and disjoint assignment, regenerates final witness summaries, verifies all new physical traces and inherited hashes, then seals the exact inventory once. It refuses to overwrite an existing seal. Mathematical proof documents require human review; running scripts does not formally verify the universal proofs.

The single unmetered duplicate independent local55-key prototype is disclosed rather than repeated as a required command; its checks run again under finalization's meter. Resource receipt CPU and wall values naturally differ in a reproduction. Complete source/event/cost identities and theorem/refutation status should agree. Moving the whole repository without rebasing its inherited absolute control references requires a separately reviewed path migration; it is not silently performed here.

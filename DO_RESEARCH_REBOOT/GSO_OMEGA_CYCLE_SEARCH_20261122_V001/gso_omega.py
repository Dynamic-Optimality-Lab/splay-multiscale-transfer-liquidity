"""CLI for the complete-history Omega5 teacher and scope-safe proof gate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from core import HERE, evaluate, read, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("search")
    p.add_argument("--output", required=True)
    p.add_argument("--supports", nargs="+", type=int, default=[17, 33, 65, 129])
    p.add_argument("--evaluations", type=int, default=1200)
    p.add_argument("--seconds", type=int, default=240)
    p.add_argument("--seed", type=int, default=120661)
    p.add_argument("--keep", type=int, default=6)
    p.add_argument("--seed-certificate", nargs="*", default=[])
    p = sub.add_parser("evaluate")
    p.add_argument("source")
    p.add_argument("--output", required=True)
    p = sub.add_parser("verify")
    p.add_argument("certificates", nargs="+")
    p = sub.add_parser("accept")
    p.add_argument("certificate")
    sub.add_parser("status")
    args = parser.parse_args()
    if args.command == "search":
        from search import run
        initial = [read(path)["source"] for path in args.seed_certificate]
        result = run(args.output, supports=args.supports, evaluations=args.evaluations,
                     seconds=args.seconds, seed=args.seed, keep=args.keep, initial_sources=initial)
        print(json.dumps(result))
    elif args.command == "evaluate":
        loaded = read(args.source)
        result = evaluate(loaded.get("source", loaded), detail=True)
        write(args.output, result)
        print(json.dumps({k: result[k] for k in ("A", "Q_B", "Omega_5", "Omega_5_over_A")}))
    elif args.command == "verify":
        import verify
        for path in args.certificates:
            print(json.dumps({"file": path, **verify.check(verify.load(path))}))
    elif args.command == "accept":
        import verify
        print(json.dumps(verify.accept_unrestricted(read(args.certificate))))
    else:
        print(json.dumps({"engine": "WORKING_COMPLETE_HISTORY_OMEGA5_SEARCH",
                          "policy_changed": False, "primary_objective": "complete-period Omega5/A",
                          "unbounded_physical_support_accepted_as_input": True,
                          "finite_search_is_universal_proof": False,
                          "general_invariant_invention_implemented": False,
                          "root_proof": "OPEN"}))


if __name__ == "__main__":
    main()

"""H5 generator: fresh same-distribution replication of H4L (bank H5-R1).

ALL distributional semantics are mechanically inherited from the frozen
holdout.h4l_generate module (strata, quotas, tree-shape mix, history laws,
DRBG construction, dedup, serialization, ordering, compression level).
The ONLY scientific differences from H4L are: bank identity/namespace, the
stream domain prefix ('h5|' vs 'h4l|'), and an independently generated secret
256-bit seed — hence independent episode bytes from the same distribution.

Candidate-blindness: this module imports ONLY holdout.h4l_generate + stdlib.
It MUST NOT import solver/cleanroom/independent/adversary/candidate/result
namespaces and MUST NOT read specialized_survivors.json, phase_diagram.json,
or any artifacts/v04/wp5x_k6c2/ bytes. Enforced by tests/test_h5_holdout.py.
"""
from __future__ import annotations
import hashlib
import json

from holdout import h4l_generate as H4L

BANK = "H5"
BANK_ID = "H5-R1"
SIZES = list(H4L.SIZES)
PER_SIZE = H4L.PER_SIZE
STRATA = list(H4L.STRATA)
QUOTA = dict(H4L.QUOTA)
HIST_MIN, HIST_MAX = H4L.HIST_MIN, H4L.HIST_MAX
SHAPE_MIX = {k: tuple(v) for k, v in H4L.SHAPE_MIX.items()}
# Domain separation: identical DRBG construction, distinct stream namespace.
DOMAIN = "h5"
ZSTD_LEVEL = 3


def stream(n: int, stratum: str, ctr: int) -> bytes:
    return ("%s|%d|%s|%d" % (DOMAIN, n, stratum, ctr)).encode()


def generate_bank(seed: bytes, sizes=SIZES, quotas=None):
    """H5 bank generation: same loop/laws as H4L.generate_bank, H5 stream domain."""
    if len(seed) != 32:
        raise ValueError("seed is not 256-bit")
    quotas = quotas or QUOTA
    print("[H5] Generating H5 bank %s: sizes=%s" % (BANK_ID, list(sizes,)))
    out = {}
    for n in sizes:
        eps = []
        seen = set()
        for s in STRATA:
            q = quotas[s]
            got = 0
            ctr = 0
            resamples = 0
            while got < q:
                ctr += 1
                rng = H4L.DRBG(seed, stream(n, s, ctr))
                shape = SHAPE_MIX[s][rng.randbelow(4)]
                T0 = H4L.build_tree(shape, n, rng)
                H = H4L.gen_history(s, n, T0, rng)
                ep = {"size": n, "stratum": s, "shape": shape, "T0": T0, "H": H}
                h = H4L.episode_hash(ep)
                if h in seen:
                    resamples += 1
                    if resamples > 100 * q:
                        raise RuntimeError("dedup resample cap exceeded")
                    continue
                seen.add(h)
                ep["hash"] = h
                eps.append(ep)
                got += 1
        out[n] = eps
        print("[H5] size %d: %d episodes" % (n, len(eps)))
    return out


def generator_hash() -> str:
    from pathlib import Path
    return hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()


def inherited_hash() -> str:
    from pathlib import Path
    return hashlib.sha256(
        (Path(__file__).parent / "h4l_generate.py").read_bytes()).hexdigest()

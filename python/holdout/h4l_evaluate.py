"""WP-3 STEP 91: H4L evaluation stub. Evaluation is WP-5-owned; this stub always refuses.

Even post-reveal, WP-5 builds its own evaluator. This module never evaluates.
"""
from __future__ import annotations


def evaluate(*args, **kwargs):
    """WP-3 STEP 91: fail closed — evaluation forbidden in WP-3."""
    raise RuntimeError("H4L evaluation forbidden before WP-5 reveal (stub always refuses)")

"""WP-1 STEP 16b: independent pair dynamics (KEEP/DELETE, regret)."""
from __future__ import annotations

from .splay import cost

C_PAIR = 2


def keep_costs(A, B, x):
    return cost(A, x), cost(B, x)


def delete_cost(A, x):
    return cost(A, x), 0


def regret(y, a):
    return y - C_PAIR * a


def required(y, a):
    return max(regret(y, a), 0)

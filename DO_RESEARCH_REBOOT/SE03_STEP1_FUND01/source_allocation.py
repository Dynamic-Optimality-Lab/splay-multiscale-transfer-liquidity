"""Source-indexed auxiliary allocation, with no tree engine or graph calls.

Input is an already rotated, source-certified auxiliary period. Every item
in a_events is an actual A StepEv ID; every b_doubles item is an actual
auxiliary B DOUBLE ID. The imported M3/source proof supplies the ordinary
debts. This module does not evaluate a proof-only floor or execute sources.
It is delivered as an algorithm; no finite input examples are run here.
"""
from collections import deque
from dataclasses import dataclass
from typing import Hashable, Iterator, Sequence

Unit = tuple[Hashable, int]

@dataclass(frozen=True)
class Macro:
    macro_id: Hashable
    a_events: tuple[Hashable, ...]
    b_doubles: tuple[Hashable, ...]

@dataclass(frozen=True)
class Payment:
    macro_id: Hashable
    demand: Hashable
    unit: Unit

@dataclass(frozen=True)
class Reserve:
    macro_id: Hashable
    cause: str
    unit: Unit

def canonical_cut(debts: Sequence[int]) -> int:
    """Earliest maximum boundary; caller realizes the actual source rotation."""
    if len(debts) < 2 or debts[0] != debts[-1]:
        raise ValueError('A nonempty closed ordinary-boundary sequence is required')
    if any(type(d) is not int or not 0 <= d <= 2 for d in debts):
        raise ValueError('Use the actual sealed ordinary M3 debt in [0,2]')
    return max(range(len(debts)-1), key=debts.__getitem__)

def allocate(macros: Sequence[Macro], debts: Sequence[int]) -> Iterator[Payment | Reserve]:
    """Fund all auxiliary doubles and release disjoint actual source units.

    Source validity, event-ID uniqueness and actual timestamp ordering are
    input-certificate premises. Signed inequalities are checked before any
    receipt is yielded. No assertion of original marginal repayment or
    native matching-terminal eligibility is made.
    """
    if not macros or len(debts) != len(macros)+1:
        raise ValueError('Need one ordinary boundary before and after each macro')
    if canonical_cut(debts) != 0:
        raise ValueError('Realize the maximum-debt source rotation first')
    for i, macro in enumerate(macros):
        h, q = len(macro.a_events), len(macro.b_doubles)
        if 2*min(h,3)-q+debts[i+1]-debts[i] < 0:
            raise ValueError('Input does not carry the required signed M3/source certificate')

    d_star = debts[0]
    bank: deque[Unit] = deque()
    for i, macro in enumerate(macros):
        assert len(bank) == d_star-debts[i]
        h = len(macro.a_events)
        c = min(h,3)
        # All actual A replay in the macro precedes its sole double demand
        # batch at the terminal auxiliary KEEP. Other B demands are zero.
        for ordinal, event in enumerate(macro.a_events):
            for bit in (0,1):
                unit = (event,bit)
                if ordinal < c:
                    bank.append(unit)
                else:
                    yield Reserve(macro.macro_id,'tail_after_first_three_events',unit)
        for demand in macro.b_doubles:
            yield Payment(macro.macro_id,demand,bank.popleft())
        keep = d_star-debts[i+1]
        while len(bank) > keep:
            yield Reserve(macro.macro_id,'certified_surplus',bank.pop())
        assert len(bank) == keep
    assert not bank

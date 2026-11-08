"""Explicit global glue on the proved single-gap domain; no new fitting."""
from potential import OutsidePotential

def chi(b):return b['kr'][8]==0 and b['rr'][8]==19

class GlobalSingleGapPotential:
    def __init__(self):self.low=OutsidePotential()
    def ordinary(self,s):return self.low(s)-5*int(chi(s['b']))
    def midpoint(self,m):return -5*int(chi(m['b']))

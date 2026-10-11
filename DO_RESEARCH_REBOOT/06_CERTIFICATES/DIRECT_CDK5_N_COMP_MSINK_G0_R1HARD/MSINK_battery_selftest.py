# Membership battery self-tests: synth positives + real-word matrix.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M

Fails = []
def chk(name, got, want):
    print("%s: got=%s want=%s %s" % (name, got, want, "OK" if got == want else "FAIL"), flush=True)
    if got != want:
        Fails.append(name)

def SB(key, a, q, genuine, dB, rb, keeps, l1=1):
    return {"key": key, "keys": [key], "a": a, "q": q, "delta": q - 2 * a,
            "genuine": genuine, "dB": dB, "rb": rb, "keeps": keeps,
            "dA": 2 * a - 1, "push": [], "l0": l1 - 1, "l1": l1, "nleg": 1}

# AJ synth: positive + former-root successor with capacity
mb = [SB(6, 1, 3, True, 7, 1, [6]),
      SB(1, 2, 1, True, 2, 6, [1])]
chk("AJ-synth-pos", M.member_AJ(mb), True)
mb2 = [SB(6, 1, 3, True, 7, 1, [6]),
       SB(8, 2, 1, True, 2, 6, [8])]
chk("AJ-synth-negsucc", M.member_AJ(mb2), False)
# AK synth: positive, genuine intervener opposite-side, delayed r, capacity
sn = {0: {1: 2, 6: 0, 7: 3}}
mb = [SB(6, 1, 3, True, 7, 1, [6], l1=1),
      SB(7, 1, 0, True, 0, 6, [7], l1=2),
      SB(1, 2, 1, True, 2, 6, [1], l1=3)]
chk("AK-synth-pos", M.member_AK(mb, sn), True)
chk("ALG-synth-pos", M.member_ALG(mb, sn), True)
mb3 = [SB(6, 1, 3, True, 7, 1, [6], l1=1),
       SB(7, 1, 0, True, 0, 6, [7], l1=2),
       SB(5, 2, 1, True, 2, 6, [5], l1=3)]
chk("AK-synth-negr", M.member_AK(mb3, sn), False)
# same-side intervener: AK false, ALG true
mb4 = [SB(6, 1, 3, True, 7, 1, [6], l1=1),
       SB(4, 1, 0, True, 0, 6, [4], l1=2),
       SB(1, 2, 1, True, 2, 6, [1], l1=3)]
chk("AK-synth-sameside", M.member_AK(mb4, sn), False)
chk("ALG-synth-sameside", M.member_ALG(mb4, sn), True)
# ALS synth: delta in {1,2}, intervener delta==0, delayed r a>=2
mb = [SB(6, 1, 3, True, 7, 1, [6]),
      SB(7, 1, 2, True, 4, 6, [7]),
      SB(1, 2, 1, True, 2, 6, [1])]
chk("ALS-synth-pos", M.member_ALS(mb), True)
# AMG synth
sn = {0: {1: 2}}
mb = [SB(6, 1, 3, True, 7, 1, [6], l1=1),
      SB(7, 1, 0, True, 0, 6, [7], l1=2),
      SB(4, 1, 0, True, 0, 6, [4], l1=3),
      SB(1, 2, 1, True, 2, 6, [1], l1=4)]
chk("AMG-synth-pos", M.member_AMG(mb, sn), True)
mb5 = [SB(6, 1, 3, True, 7, 1, [6], l1=1),
       SB(7, 1, 0, True, 0, 6, [7], l1=2),
       SB(4, 1, 0, True, 0, 6, [4], l1=3),
       SB(5, 2, 1, True, 2, 6, [5], l1=4)]
chk("AMG-synth-negr", M.member_AMG(mb5, sn), False)
# AMS synth
mb = [SB(6, 1, 1, True, 3, 1, [6]),
      SB(7, 1, 2, True, 4, 6, [7]),
      SB(4, 1, 2, True, 4, 6, [4]),
      SB(1, 2, 1, True, 2, 6, [1])]
chk("AMS-synth-pos", M.member_AMS(mb), True)
# AN synth packet
mb = [SB(6, 1, 3, True, 7, 1, [6]),
      SB(4, 1, 1, True, 2, 6, [4]),
      SB(2, 1, 3, True, 7, 4, [2]),
      SB(1, 2, 2, True, 4, 2, [1])]
chk("AN-synth-pos", M.member_AN(mb), True)
mb6 = [SB(6, 1, 3, True, 7, 1, [6]),
       SB(4, 1, 1, True, 2, 6, [4]),
       SB(2, 1, 3, True, 7, 4, [2]),
       SB(5, 2, 2, True, 4, 2, [5])]
chk("AN-synth-negr", M.member_AN(mb6), False)

# real words
NPW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('K', 1), ('D', 4), ('K', 9),
       ('D', 6), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 2),
       ('D', 1), ('D', 6), ('D', 9)]
# NOTE (battery fixture audit): S1_G0/S1_authoritative_replay.py at HEAD asserts
# A=33 for its INC word, but current engines give A=29 (script FAILS if run;
# stale assert, never the proved witness). The PROVED S1 witness is the
# S1P-certificate word ff156d94 (S1W, 17 accesses, A=33) -- used below as S1I.
# NP WIT (29/18) is a different word that happens to equal S1_G0's stale INC.
S1I = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
S2I = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 9), ('D', 5), ('K', 1),
       ('D', 4), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 1), ('D', 6), ('D', 9)]
VRI = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
MRI = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]

def products(word):
    r = B.replay(word)
    assert r is not None and r["S1"] == r["S0"]
    legs = r["legs"]
    mb = B.merged_blocks(legs)
    assert isinstance(mb, list)
    iv = B.intervals_of(legs)
    return legs, mb, iv, r["bdep"]

def batt(name, word, expect):
    legs, mb, iv, bdep = products(word)
    got = {"NP": M.member_NP(iv, legs), "S1": M.member_S1(iv, legs),
           "S2": M.member_S2(iv, legs), "VR": M.member_VR(iv, legs),
           "MR": M.member_MR(iv, legs), "AJ": M.member_AJ(mb),
           "AK": M.member_AK(mb, bdep), "ALG": M.member_ALG(mb, bdep),
           "ALS": M.member_ALS(mb), "AMG": M.member_AMG(mb, bdep),
           "AMS": M.member_AMS(mb), "AN": M.member_AN(mb)}
    for k, w in expect.items():
        chk("%s-%s" % (name, k), got[k], w)
    print("  full:", got, flush=True)

batt("NPW", NPW, {"NP": True, "S1": False, "S2": False, "VR": False,
                  "MR": False})
batt("S1I", S1I, {"NP": False, "S1": True, "S2": False, "VR": False,
                  "MR": False})
batt("S2I", S2I, {"NP": False, "S1": False, "S2": True, "VR": False,
                  "MR": False})
batt("VRI", VRI, {"NP": False, "S1": False, "S2": False, "VR": True,
                  "MR": False})
batt("MRI", MRI, {"NP": False, "S1": False, "S2": False, "VR": False,
                  "MR": True})
# AJ/AK/AL/AM/AN on real words: all five INCs are outside those classes
for name, w in (("S1I", S1I), ("VRI", VRI), ("MRI", MRI), ("NPW", NPW)):
    legs, mb, iv, bdep = products(w)
    for k, fn in (("AJ", lambda: M.member_AJ(mb)),
                  ("AK", lambda: M.member_AK(mb, bdep)),
                  ("ALG", lambda: M.member_ALG(mb, bdep)),
                  ("ALS", lambda: M.member_ALS(mb)),
                  ("AMG", lambda: M.member_AMG(mb, bdep)),
                  ("AMS", lambda: M.member_AMS(mb)),
                  ("AN", lambda: M.member_AN(mb))):
        chk("%s-%s-out" % (name, k), fn(), False)

print("BATTERY:", "PASS" if not Fails else "FAIL %s" % Fails, flush=True)
sys.exit(0 if not Fails else 1)

# Exact new post-loss witness and frontier

Fi are arbitrary independent finite ordered gap BSTs; k(L,R) retains actual nodes.

Period96; actual reaching prefix96; erase3. Costs `{'A': 139, 'QF': 54, 'QE': 16, 'CD_slack': 224}`.

Original recurrent word:

```text
K9 K1 K3 K5 K3 K1 K11 K1 K3 K5 K9 K11 K9 K5 K3 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D6 D1 K1 K7 K1 K3 K5 K1 K11 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D9 D1 D3 D5 D3 D1 D11 D1 D3 D5 D9 D11 D9 D5 D3 D1 D7 D1 D3 D5 D1 D11 K1 K5 K7 K9 K7 K5 K3 K1
```

## T11

Boundary after relative40, absolute136; SHA256 `34939ef5ea7107275c8f61290d89285edf12392ab6c1b7120b2c8b5b3438e28f`.
M `[1, 3, 5, 7, 9, 11]`, erased `3`, recent `[7, 1, 3, 5, 9, 11]`, phase `ready`.

A:

```text
7(6(1(F0,3(2(F1,F2),5(4(F3,F4),F5))),F6),8(F7,9(F8,10(F9,11(F10,F11)))))
```

BF:

```text
7(2(1(F0,F1),4(3(F2,F3),6(5(F4,F5),F6))),8(F7,9(F8,10(F9,11(F10,F11)))))
```

BE:

```text
7(5(1(F0,2(F1,4(3(F2,F3),F4))),6(F5,F6)),9(8(F7,F8),10(F9,11(F10,F11))))
```

## first-loss source

Boundary after relative42, absolute138; SHA256 `4d8c0f0647b8b52fa7820aeebe02fb0a361841a1e3a908bfa2dde0dd0b7afd9f`.
M `[1, 3, 5, 7, 9, 11]`, erased `3`, recent `[3, 1, 7, 5, 9, 11]`, phase `ready`.

A:

```text
3(1(F0,2(F1,F2)),6(5(4(F3,F4),F5),7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))
```

BF:

```text
3(2(1(F0,F1),F2),4(F3,7(6(5(F4,F5),F6),8(F7,9(F8,10(F9,11(F10,F11)))))))
```

BE:

```text
1(F0,5(2(F1,4(3(F2,F3),F4)),7(6(F5,F6),9(8(F7,F8),10(F9,11(F10,F11))))))
```

## P1 after3->2

Boundary after relative43, absolute139; SHA256 `b10c76a23daaa0b0cbb2e761fe659d0a12f85c9532e64147901c4f00326b15a0`.
M `[1, 3, 5, 7, 9, 11]`, erased `3`, recent `[5, 3, 1, 7, 9, 11]`, phase `ready`.

A:

```text
5(3(1(F0,2(F1,F2)),4(F3,F4)),6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))
```

BF:

```text
5(4(3(2(1(F0,F1),F2),F3),F4),6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))
```

BE:

```text
5(1(F0,2(F1,4(3(F2,F3),F4))),7(6(F5,F6),9(8(F7,F8),10(F9,11(F10,F11)))))
```

## RELAXED Fork41 frontier

Boundary after relative44, absolute140; SHA256 `3527bf2e5689bf5180faeaf8008755c4533af9a7098539c38f8a315e0f803416`.
M `[1, 3, 5, 7, 9, 11]`, erased `3`, recent `[1, 5, 3, 7, 9, 11]`, phase `ready`.

A:

```text
1(F0,3(2(F1,F2),5(4(F3,F4),6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))))
```

BF:

```text
1(F0,4(2(F1,3(F2,F3)),5(F4,6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))))
```

BE:

```text
1(F0,5(2(F1,4(3(F2,F3),F4)),7(6(F5,F6),9(8(F7,F8),10(F9,11(F10,F11))))))
```

## Critical physical accesses

| Occurrence | Request | A path | BF path | a | qF | Cold |
|---|---|---|---|---:|---:|---|
| 40 | K7 | `RR` | `RRRRRRLL` | 1 | 4 | True |
| 41 | K1 | `LL` | `LL` | 1 | 1 | False |
| 42 | K3 | `RL` | `RRLL` | 1 | 2 | False |
| 43 | K5 | `RL` | `RRLL` | 1 | 2 | False |
| 44 | K1 | `LL` | `LLLL` | 1 | 2 | False |
| 45 | K11 | `RRRRRRRR` | `RRRRRRRR` | 4 | 4 | True |

The relaxed frontier is NOT F11 or certified B0. The true cold key11 has A-depth8 and requires H>=4.

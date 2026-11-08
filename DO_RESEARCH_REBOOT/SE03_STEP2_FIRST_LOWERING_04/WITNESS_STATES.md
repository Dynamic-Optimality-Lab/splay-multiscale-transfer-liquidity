# Exact witness trees, charts and state identities

Notation k(L,R) means an actual node. Fi are distinct arbitrary finite ordered gap BSTs.
Full states are never identified only by projected Scores. Absolute IDs follow the stated reaching prefix.

## E0 — entry_family.json

Period 68; reaching prefix 68; erase3. Exact costs `{'A': 81, 'QF': 28, 'QE': 22, 'original_CD_slack': 134}`.

Complete original recurrent-period word:

```text
K3 K5 K7 K9 K11 K9 K7 K5 K3 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D10 D1 K1 K11 K1 K3 K5 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D11 D1 D3 D5 K7 K9 K7 K5 K3 K1
```

### NEG2 source

Boundary after relative33, absolute101; SHA256 `ed04f27255e321ba8f6e53ea1476df83cacbacb348e673b00b7d74e979e27fc1`.
Recent-six `[1, 3, 5, 7, 9, 11]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
1(F0,10(3(2(F1,F2),5(4(F3,F4),7(6(F5,F6),9(8(F7,F8),F9)))),11(F10,F11)))
```

BF:

```text
1(F0,2(F1,3(F2,4(F3,5(F4,6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))))))
```

BE:

```text
1(F0,2(F1,5(4(3(F2,F3),F4),6(F5,7(F6,8(F7,9(F8,10(F9,11(F10,F11)))))))))
```

### t in T11

Boundary after relative35, absolute103; SHA256 `a71e1d4d33b1449450f5cee511f6e440d583e50d7a4fa5182ed426f499fe2740`.
Recent-six `[1, 11, 3, 5, 7, 9]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
1(F0,10(3(2(F1,F2),5(4(F3,F4),7(6(F5,F6),9(8(F7,F8),F9)))),11(F10,F11)))
```

BF:

```text
1(F0,2(F1,11(4(3(F2,F3),6(5(F4,F5),8(7(F6,F7),10(9(F8,F9),F10)))),F11)))
```

BE:

```text
1(F0,2(F1,11(6(5(4(3(F2,F3),F4),F5),8(7(F6,F7),10(9(F8,F9),F10))),F11)))
```

### ell in L11

Boundary after relative36, absolute104; SHA256 `31d9711e08428ab5434f9bf86dd94d2e448d4fe851e64ffa53f35d1e25215080`.
Recent-six `[3, 1, 11, 5, 7, 9]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
3(1(F0,2(F1,F2)),10(5(4(F3,F4),7(6(F5,F6),9(8(F7,F8),F9))),11(F10,F11)))
```

BF:

```text
3(2(1(F0,F1),F2),4(F3,11(6(5(F4,F5),8(7(F6,F7),10(9(F8,F9),F10))),F11)))
```

BE:

```text
1(F0,2(F1,11(6(5(4(3(F2,F3),F4),F5),8(7(F6,F7),10(9(F8,F9),F10))),F11)))
```

### ell prime

Boundary after relative37, absolute105; SHA256 `512fc925cb141ddd53541fae3ef5964aabf1036ed7f20bc271356dbb47c6aa38`.
Recent-six `[5, 3, 1, 11, 7, 9]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
5(3(1(F0,2(F1,F2)),4(F3,F4)),10(7(6(F5,F6),9(8(F7,F8),F9)),11(F10,F11)))
```

BF:

```text
5(4(3(2(1(F0,F1),F2),F3),F4),6(F5,11(8(7(F6,F7),10(9(F8,F9),F10)),F11)))
```

BE:

```text
5(2(1(F0,F1),4(3(F2,F3),F4)),6(F5,11(8(7(F6,F7),10(9(F8,F9),F10)),F11)))
```

| Occurrence | Mode/key | A path | BF path | a | qF | recent before -> after |
|---|---|---|---|---:|---:|---|
| 34 | K11 | `RR` | `RRRRRRRRRR` | 1 | 5 | `[1, 3, 5, 7, 9, 11]` -> `[11, 1, 3, 5, 7, 9]` |
| 35 | K1 | `LL` | `LL` | 1 | 1 | `[11, 1, 3, 5, 7, 9]` -> `[1, 11, 3, 5, 7, 9]` |
| 36 | K3 | `RL` | `RRLL` | 1 | 2 | `[1, 11, 3, 5, 7, 9]` -> `[3, 1, 11, 5, 7, 9]` |
| 37 | K5 | `RL` | `RRLL` | 1 | 2 | `[3, 1, 11, 5, 7, 9]` -> `[5, 3, 1, 11, 7, 9]` |

The full physical before/after chart objects and all intervening operations are retained in the family JSON.

## E1 — e1_family.json

Period 90; reaching prefix 90; erase3. Exact costs `{'A': 125, 'QF': 44, 'QE': 14, 'original_CD_slack': 206}`.

Complete original recurrent-period word:

```text
K9 K1 K3 K5 K3 K1 K11 K1 K3 K5 K9 K11 K9 K5 K3 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D10 D7 D1 K1 K7 K9 K1 D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D9 D1 D3 D5 D3 D1 D11 D1 D3 D5 D9 D11 D9 D5 D3 D1 D7 D9 D1 K9 K7 K1 K3 K5 K3 K1
```

### NEG2 source

Boundary after relative40, absolute130; SHA256 `99ce9379b0440e712c72c59b61a9468990d8b6393ee5281090faaf353b5e7630`.
Recent-six `[1, 3, 5, 9, 11, 7]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
1(F0,7(5(3(2(F1,F2),4(F3,F4)),6(F5,F6)),10(9(8(F7,F8),F9),11(F10,F11))))
```

BF:

```text
1(F0,2(F1,3(F2,4(F3,5(F4,6(F5,9(8(7(F6,F7),F8),10(F9,11(F10,F11)))))))))
```

BE:

```text
1(F0,5(2(F1,4(3(F2,F3),F4)),7(6(F5,F6),9(8(F7,F8),10(F9,11(F10,F11))))))
```

### t in T11

Boundary after relative41, absolute131; SHA256 `7c5eae8e3af684885560ffced7d474d02050c25248d34dd3ceba2e8ee7c4bed4`.
Recent-six `[7, 1, 3, 5, 9, 11]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
7(1(F0,5(3(2(F1,F2),4(F3,F4)),6(F5,F6))),10(9(8(F7,F8),F9),11(F10,F11)))
```

BF:

```text
7(2(1(F0,F1),4(3(F2,F3),6(5(F4,F5),F6))),8(F7,9(F8,10(F9,11(F10,F11)))))
```

BE:

```text
7(5(1(F0,2(F1,4(3(F2,F3),F4))),6(F5,F6)),9(8(F7,F8),10(F9,11(F10,F11))))
```

### ell in L11

Boundary after relative42, absolute132; SHA256 `6f70f5ee69af298afa91e4b4314a604754125882c621eaf507b1b1ab88138888`.
Recent-six `[9, 7, 1, 3, 5, 11]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
9(7(1(F0,5(3(2(F1,F2),4(F3,F4)),6(F5,F6))),8(F7,F8)),10(F9,11(F10,F11)))
```

BF:

```text
9(8(7(2(1(F0,F1),4(3(F2,F3),6(5(F4,F5),F6))),F7),F8),10(F9,11(F10,F11)))
```

BE:

```text
9(7(5(1(F0,2(F1,4(3(F2,F3),F4))),6(F5,F6)),8(F7,F8)),10(F9,11(F10,F11)))
```

### ell prime

Boundary after relative43, absolute133; SHA256 `594527131cbbce799f3beab58515b4215573b99c8f0824e15b5d80604284c872`.
Recent-six `[1, 9, 7, 3, 5, 11]`, M `[1, 3, 5, 7, 9, 11]`, erased `3`, phase `ready`.

A:

```text
1(F0,7(5(3(2(F1,F2),4(F3,F4)),6(F5,F6)),9(8(F7,F8),10(F9,11(F10,F11)))))
```

BF:

```text
1(F0,8(2(F1,7(4(3(F2,F3),6(5(F4,F5),F6)),F7)),9(F8,10(F9,11(F10,F11)))))
```

BE:

```text
1(F0,9(5(2(F1,4(3(F2,F3),F4)),7(6(F5,F6),8(F7,F8))),10(F9,11(F10,F11))))
```

| Occurrence | Mode/key | A path | BF path | a | qF | recent before -> after |
|---|---|---|---|---:|---:|---|
| 41 | K7 | `R` | `RRRRRRLL` | 1 | 4 | `[1, 3, 5, 9, 11, 7]` -> `[7, 1, 3, 5, 9, 11]` |
| 42 | K9 | `RL` | `RR` | 1 | 1 | `[7, 1, 3, 5, 9, 11]` -> `[9, 7, 1, 3, 5, 11]` |
| 43 | K1 | `LL` | `LLLL` | 1 | 2 | `[9, 7, 1, 3, 5, 11]` -> `[1, 9, 7, 3, 5, 11]` |

The full physical before/after chart objects and all intervening operations are retained in the family JSON.


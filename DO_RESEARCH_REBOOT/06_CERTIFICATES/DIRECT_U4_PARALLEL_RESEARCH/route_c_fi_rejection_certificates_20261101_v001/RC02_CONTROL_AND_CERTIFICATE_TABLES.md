# Fixed-source budgets and exact rejected-cut certificates

These are14 previously source-verified controls and their636 previously checked cuts. Every control is FI-accepted at some cut. The44 rows below describe individual rejected cuts; none is asserted to be an all-cut counterexample. Source names and full trees are in fixed_corpus_sources.json.

## Source-local budget controls

|Control|E|C_D|L_fresh|Gamma|Constructed positive cut|
|---:|---:|---:|---:|---:|---:|
|0|4|26|4|-26|0|
|1|4|26|4|-26|0|
|2|5|28|6|-29|0|
|3|5|28|6|-29|0|
|4|3|12|5|-14|0|
|5|3|12|5|-14|0|
|6|3|8|5|-10|0|
|7|3|8|5|-10|0|
|8|1|10|5|-14|0|
|9|1|10|5|-14|0|
|10|1|10|6|-15|0|
|11|1|10|6|-15|0|
|12|5|4|5|-4|17|
|13|5|4|5|-4|17|

Controls0..11 are the twelve old ordinary/reflected FI witnesses. Controls12/13 are H5 and its reflection. All budgets are strictly negative. Controls6/7 have run gaps2 and-12, so an individually starved run is paid through later physical pools; private repayment of every run is not assumed.

## All44 rejected-cut certificates

|Control|Cut|Busy source blocks|Final debt|Source delta sum|Reserved loss|Paid facts retained at start|
|---:|---:|---|---:|---:|---:|---:|
|0|1|0|4|4|0|0|
|0|2|0,1|1|1|0|0|
|1|1|0|4|4|0|0|
|1|2|0,1|1|1|0|0|
|2|1|0|4|4|0|1|
|2|3|2|1|1|0|1|
|3|1|0|4|4|0|1|
|3|3|2|1|1|0|1|
|4|1|0|2|2|0|1|
|4|3|2|1|1|0|1|
|4|4|2,3|1|1|0|1|
|5|1|0|2|2|0|1|
|5|3|2|1|1|0|1|
|5|4|2,3|1|1|0|1|
|6|1|0|2|2|0|1|
|6|2|0,1|3|3|0|0|
|6|3|0,1,2|3|3|0|0|
|7|1|0|2|2|0|1|
|7|2|0,1|3|3|0|0|
|7|3|0,1,2|3|3|0|0|
|8|1|0|1|1|0|0|
|9|1|0|1|1|0|0|
|10|1|0|1|1|0|0|
|11|1|0|1|1|0|0|
|12|18|17|1|1|0|4|
|12|19|17,18|1|1|0|4|
|12|35|34|1|1|0|4|
|12|36|34,35|1|1|0|4|
|12|52|51|1|1|0|4|
|12|53|51,52|1|1|0|4|
|12|69|68|1|1|0|4|
|12|70|68,69|1|1|0|4|
|12|86|85|1|1|0|4|
|12|87|85,86|1|1|0|4|
|13|18|17|1|1|0|4|
|13|19|17,18|1|1|0|4|
|13|35|34|1|1|0|4|
|13|36|34,35|1|1|0|4|
|13|52|51|1|1|0|4|
|13|53|51,52|1|1|0|4|
|13|69|68|1|1|0|4|
|13|70|68,69|1|1|0|4|
|13|86|85|1|1|0|4|
|13|87|85,86|1|1|0|4|

All indices are zero-based physical block indices. The44 canonical suffixes have lengths1(26 cases),2(16 cases),or3(2 cases). All44 controls have zero reserved loss on the final busy suffix;32 retain earlier paid source facts. The universal certificate split permits nonzero reserved loss, but this fixed corpus does not supply that failure type. No extra source word or size was added to seek it.

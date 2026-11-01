# Reproducibility and preservation

The producer is [audit_exact_b.py](audit_exact_b.py); the verifier is [independent_verify.py](independent_verify.py). Both use Python's standard library only, disable bytecode generation, read old sources without changing them, and create outputs with exclusive mode x. Their repository root is derived from the script's location.

The original run used Python with `-X utf8 -B`. To reproduce, create another fresh versioned directory under the same DIRECT_U4_PARALLEL_RESEARCH parent, copy the scripts and the gate into it, run the producer there, then the independent verifier. Do not rerun them over these sealed outputs: exclusive writes intentionally reject overwriting. The new run will additionally pin this run as prior research.

The producer uses the tuple splay to construct one frozen 429-B by five-A by three-request classification. No external solver, package installation, coefficient fitting, larger key size, or alternate minor is used. Bellman-Ford only audits the integer cancellation constraints and exports labels verifying the absence of a negative cycle. The independent verifier uses the pointer engine and checks every row and certificate inequality without importing the producer or using a graph optimizer.

The existing seven-key antichain countercertificate is pinned and read for its fixed source pair. Its terminal K values are independently checked using complete proper-subtree sets and nested active right intervals. The six-DELETE reachability prefix is replayed with B frozen. No new connector search is needed.

Entry hashes cover 464 inherited/source/previous-run files and all 125 Stage 11G final-closure files. The final seal checks contents and the Stage inventory, repository branch/HEAD, and tracked status. The delivery manifest hashes every new artifact except itself. No Stage 11G code, old status writer, Git mutation, or installation was executed. Untracked historical material is preserved, not removed or described as a clean worktree.

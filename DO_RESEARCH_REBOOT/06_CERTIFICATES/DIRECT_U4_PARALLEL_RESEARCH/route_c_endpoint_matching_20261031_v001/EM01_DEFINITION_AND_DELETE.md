# Nonlinear endpoint matching and the universal DELETE law

This candidate replaces exact subtree agreement in F by a joint one-to-one endpoint matching. It has a universal DELETE bound and pays the opposite-vine demand (EM02). Those statements do not establish its helper or general B law.

For a finite n-key ordered BST T let C0(T) be the exact key sets of its proper nonempty node-rooted subtrees. Exclude the full set and include a singleton only for an actual leaf. For n>=1 there are n-1 such sets; different subtrees have distinct nonempty sets. All extrema below are actual keys, not numerical distances or cardinalities.

Build a bipartite graph with vertex sets C0(A),C0(B). Join I to J if

    min(I)=min(J) OR max(I)=max(J).

This compares minimum with minimum and maximum with maximum; an un-oriented equality between opposite endpoints does not suffice. Let nu(A,B) be its maximum matching cardinality. Define

    E(A,B)=(n-1)-nu(A,B), n>=1; E(empty,empty)=0.

The full subtree sets are fixed to each other implicitly; they cannot act as extra hubs among the proper sets. E is a completely specified finite function of the current trees. A maximum matching always exists, including the empty matching. No global potential-feasibility premise or source history is involved. The formula is nonlinear because endpoint matches compete for one-to-one capacity.

Let c=|C0(A) intersection C0(B)|. Exact common sets give c distinct diagonal matching edges, hence nu>=c and

    0<=E<=F=(n-1)-c,
    H:=E-F=c-nu<=0.

H is an explicit nonlinear repair to F. Pointwise domination E<=F alone says nothing about transition differences.

## One vertex replacement controls A motion

A primitive rotation retains the full local key set and every fringe/outside subtree set. It replaces exactly one proper subtree set J with one different set K (CC01 of the previous audit). Thus its endpoint graph replaces only one LEFT vertex and that vertex's incident edges.

Take any old maximum matching. Delete its edge at the removed vertex if necessary. At most one edge is lost, and the remaining matching is valid in the new graph. Therefore nu_new>=nu_old-1. Applying the same argument to the inverse rotation gives nu_old>=nu_new-1. Consequently

    |E(A_new,B)-E(A_old,B)|<=1.

An actual source A splay at present x uses exactly d_A(x) primitive rotations, with two per double and one for a final zig. Summing yields

    Delta_DELETE E<=d_A(x)<=2 ceil(d_A(x)/2)=2a.

This proves DELETE for every finite same-key pair, every fringe shape and both orientations. No-op accesses, one-key trees and empty trees cause no exception. Reversing key order exchanges minimum and maximum and preserves the graph, so reflection preserves all values.

## What is not inherited

The old F root-conditioned proof counted new exact common sets. A new exact edge in a maximum matching need not increase its cardinality: it can displace a prior inexact match or share capacity with another edge. Therefore neither F's strict one-unit B drop nor its arbitrary-fringe helper law transfers to E without proof. The source audit checks that precise issue.

from itertools import product
from networkx import minimum_cut, DiGraph
from mip import Model, xsum, BINARY, OptimizationStatus, CutType


# N - Nodes
# A - Distance Matrix

def cutting_planes_main(N, A):
    Aout = {n: [a for a in A if a[0] == n] for n in N} # store output and input arcs per node
    Ain = {n: [a for a in A if a[1] == n] for n in N}

    m = Model()
    x = {a: m.add_var(name="x({},{})".format(a[0], a[1]), var_type=BINARY) for a in A}

    m.objective = xsum(c * x[a] for a, c in A.items()) # create the objective function

    for n in N:
        m += xsum(x[a] for a in Aout[n]) == 1, "out({})".format(n)
        m += xsum(x[a] for a in Ain[n]) == 1, "in({})".format(n)

    newConstraints = True

    while newConstraints:
        m.optimize(relax=True)
        print("status: {} objective value : {}".format(m.status, m.objective_value))

        G = DiGraph()
        for a in A:
            G.add_edge(a[0], a[1], capacity=x[a].x)

        newConstraints = False
        for (n1, n2) in [(i, j) for (i, j) in product(N, N) if i != j]:
            cut_value, (S, NS) = minimum_cut(G, n1, n2)
            if cut_value <= 0.99:
                m += (xsum(x[a] for a in A if (a[0] in S and a[1] in S)) <= len(S) - 1)
                newConstraints = True
        if not newConstraints and m.solver_name.lower() == "cbc":
            cp = m.generate_cuts([CutType.GOMORY, CutType.MIR,
                                  CutType.ZERO_HALF, CutType.KNAPSACK_COVER])
            if cp.cuts:
                m += cp
                newConstraints = True

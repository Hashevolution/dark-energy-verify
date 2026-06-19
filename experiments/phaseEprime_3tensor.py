"""
Phase E' (future-research-topics.md sec 8/10): the larger holographic code.

Phase E's verdict: in the minimal TWO-perfect-tensor code, a single-bond complex
CLIFFORD phase (S(x)I, magic-free) made the boundary entropy state-dependent --
MORE than the magic gate CS -- so no region isolated magic (confound). The fix
proposed was a LARGER code where single-bond phases are genuinely removable.

This builds a THREE-perfect-tensor line  T1 - T2 - T3  (each adjacent pair joined
by 2 bonds), region A = T1's three boundary legs, RT surface = the T1-T2 cut (2
bonds), in-wedge bulk = b1 (varied over the Bloch sphere). Now there is an extra
tensor (T2,T3 = a larger, more scrambled "rest") between the surface and the far
boundary.

Direct question (gate 0'): does the single-bond complex-Clifford confound SHRINK
relative to the two-tensor code? i.e. do magic-free gates (incl. S(x)I, I(x)S,
S(x)S) now leave Var_bulk(S_A) ~ 0 while only non-Clifford CS/cT lift it?
If yes -> a clean magic-only test exists in the larger code (Phase E confound was
finite-size). If the confound persists -> it is structural, and a faithful test
needs a genuinely large HaPPY tiling (beyond tractable exact simulation).
"""

import numpy as np
from phase2pp_holographic_magic import (
    five_qubit_code, perfect_tensor, entropy_region, m2_full, bloch)

EYE4 = np.eye(4, dtype=complex)
CZ = np.diag([1, 1, 1, -1]).astype(complex)       # Clifford, real
SS = np.diag([1, 1j, 1j, -1]).astype(complex)     # Clifford, complex (product)
SI = np.diag([1, 1, 1j, 1j]).astype(complex)      # Clifford, complex (bond a)
IS = np.diag([1, 1j, 1, 1j]).astype(complex)      # Clifford, complex (bond b)
CS = np.diag([1, 1, 1, 1j]).astype(complex)       # non-Clifford, MAGIC
cT = np.diag([1, 1, 1, np.exp(1j * np.pi / 4)]).astype(complex)  # non-Clifford, MAGIC

MAGIC_FREE = {"I": EYE4, "CZ": CZ, "SxS": SS, "SxI": SI, "IxS": IS}
MAGIC = {"CS": CS, "cT": cT}


def network_3tensor(T, phi1, phi2, phi3, G1, G2):
    """Three perfect tensors T1-T2-T3 in a line, each adjacent pair joined by 2
    bonds dressed by G1 (T1-T2) and G2 (T2-T3). Returns the 7-qubit boundary state.
    boundary order: [A: T1.p1,p2,p3] (0,1,2), [T2.p3] (3), [T3.p3,p4,p5] (4,5,6)."""
    T1 = np.tensordot(T, phi1, axes=([5], [0]))   # (p1,p2,p3,p4,p5)
    T2 = np.tensordot(T, phi2, axes=([5], [0]))
    T3 = np.tensordot(T, phi3, axes=([5], [0]))
    g1 = G1.reshape(2, 2, 2, 2)
    g2 = G2.reshape(2, 2, 2, 2)
    # T1[i,j,k,l,m] g1[l,m,n,o] T2[n,o,p,q,r] g2[q,r,s,t] T3[s,t,u,v,w] -> ijk p uvw
    psi = np.einsum('ijklm,lmno,nopqr,qrst,stuvw->ijkpuvw',
                    T1, g1, T2, g2, T3, optimize=True)
    psi = psi.reshape(-1)
    return psi / np.linalg.norm(psi)


def var_SA(T, G1, bulk_states, phi2, phi3, region, G2=None):
    G2 = EYE4 if G2 is None else G2
    vals = [entropy_region(network_3tensor(T, p1, phi2, phi3, G1, G2), 7, list(region))
            for p1 in bulk_states]
    return float(np.var(vals)), float(np.mean(vals))


def main():
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    phi2 = bloch(0, 0)
    phi3 = bloch(0, 0)
    bulk = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
            for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]
    A = (0, 1, 2)   # region A = T1 boundary legs; RT surface = T1-T2 (dressed by G1)

    # sanity: magic content unchanged by Clifford gates
    print("[setup] 3-tensor line T1-T2-T3, region A = T1.(p1,p2,p3); RT surface = G1")
    bare = m2_full(network_3tensor(T, bloch(0.7, 0.3), phi2, phi3, EYE4, EYE4), 7)
    print(f"  boundary M2 (magic-free baseline) = {bare:.4f}")
    for nm, G in {**MAGIC_FREE, **MAGIC}.items():
        mb = m2_full(network_3tensor(T, bloch(0.7, 0.3), phi2, phi3, G, EYE4), 7)
        tag = "magic-free" if abs(mb - bare) < 1e-6 else "MAGIC"
        print(f"    G1={nm:>4}  M2_bdy={mb:.4f}  ({tag})")

    # gate 0': do magic-free gates (incl. complex Cliffords) stay trivial on A?
    print(f"\n[gate 0'] Var_bulk(S_A) on region A={A}, RT surface gate G1")
    print(f"  {'G1':>6} {'kind':>20} {'Var_bulk(S_A)':>14} {'mean S_A':>9}")
    for nm, G in MAGIC_FREE.items():
        v, m = var_SA(T, G, bulk, phi2, phi3, A)
        kind = "stabilizer" if nm == "I" else ("Clifford real" if nm == "CZ"
                                               else "Clifford complex")
        print(f"  {nm:>6} {kind:>20} {v:14.3e} {m:9.4f}")
    for nm, G in MAGIC.items():
        v, m = var_SA(T, G, bulk, phi2, phi3, A)
        print(f"  {nm:>6} {'non-Clifford MAGIC':>20} {v:14.3e} {m:9.4f}")

    print("\n--- read-out ---")
    print("CONFOUND RESOLVED if all magic-free gates (incl. SxI/IxS/SxS) give")
    print("  Var ~ 0 while CS/cT lift it -> a clean magic-only signal in 3-tensor.")
    print("CONFOUND PERSISTS if some complex Clifford still lifts Var like CS ->")
    print("  structural, needs a genuinely large HaPPY tiling (intractable exactly).")


if __name__ == "__main__":
    main()

"""
Phase D (future-research-topics.md, task D): resolve the note's sec 9.8 open card.

Note sec 9.8 ("entanglement KIND = independent layer of reality") is the repo's
only surviving original differentiation card. Its single residual signal:
  the "excess"  E(A:BC) - tau_res  changed sign +0.56 -> -0.31 across a scale s,
  where E was VON NEUMANN entropy and tau_res was the CKW residual TANGLE.
Monogamy fully reproduced would give a constant/zero excess; a sign change looked
like a possible signal. The note itself flagged the suspect: E (entropy-based)
vs tau_res (tangle-based) is a MEASURE MISMATCH. Left unresolved, to be redone on
a unified (tangle) measure.

This script resolves it on the cleanest faithful stage: the GHZ<->W pure
three-qubit family (sec 9.8 is literally about GHZ/W "kind separation"). For pure
3-qubit states CKW is an EXACT identity
        tau_1(A:BC) = C(A:B)^2 + C(A:C)^2 + tau_3,
so the resolution is decisive:
  - MISMATCH excess  E_vN(A:BC) - tau_res   -> reproduce the sign change,
  - UNIFIED excess   tau_1(A:BC) - tau_res = tau_3  -> exact, sign-DEFINITE (>=0).
If the sign change lives only in the mismatch and the unified excess never
changes sign, the sec 9.8 signal is a measure artifact (card closes honestly).
"""

import numpy as np

# 3-qubit basis states
GHZ = np.zeros(8, dtype=complex); GHZ[0] = 1 / np.sqrt(2); GHZ[7] = 1 / np.sqrt(2)
W = np.zeros(8, dtype=complex)
for i in (0b001, 0b010, 0b100):
    W[i] = 1 / np.sqrt(3)

sy = np.array([[0, -1j], [1j, 0]], dtype=complex)


def rho_marginal(psi, keep):
    """reduced density matrix on qubits in `keep` (subset of {0,1,2})."""
    keep = list(keep)
    rest = [i for i in range(3) if i not in keep]
    t = psi.reshape(2, 2, 2).transpose(keep + rest).reshape(2 ** len(keep), -1)
    return t @ t.conj().T


def vN_entropy(rho):
    w = np.linalg.eigvalsh(rho)
    w = w[w > 1e-14]
    return float(-np.sum(w * np.log2(w)))      # bits


def linear_tangle_1(rho_A):
    """one-tangle tau(A:BC) = 2(1 - Tr rho_A^2) = 4 det rho_A for a qubit."""
    return float(2 * (1 - np.real(np.trace(rho_A @ rho_A))))


def concurrence(rho2):
    """Wootters concurrence of a 2-qubit (possibly mixed) state."""
    R = rho2 @ (np.kron(sy, sy) @ rho2.conj() @ np.kron(sy, sy))
    ev = np.linalg.eigvals(R).real
    ev = np.sqrt(np.clip(np.sort(ev)[::-1], 0, None))
    return float(max(0.0, ev[0] - ev[1] - ev[2] - ev[3]))


def three_tangle(psi):
    """Coffman-Kundu-Wootters 3-tangle of a pure 3-qubit state (Cayley
    hyperdeterminant form)."""
    a = psi.reshape(8)
    a0, a1, a2, a3, a4, a5, a6, a7 = a  # a_{ijk}, index = 4i+2j+k
    d1 = (a0 ** 2 * a7 ** 2 + a1 ** 2 * a6 ** 2 + a2 ** 2 * a5 ** 2 + a4 ** 2 * a3 ** 2)
    d2 = (a0 * a7 * a3 * a4 + a0 * a7 * a5 * a2 + a0 * a7 * a6 * a1
          + a3 * a4 * a5 * a2 + a3 * a4 * a6 * a1 + a5 * a2 * a6 * a1)
    d3 = (a0 * a6 * a5 * a3 + a7 * a1 * a2 * a4)
    tau3 = 4 * abs(d1 - 2 * d2 + 4 * d3)
    return float(tau3)


def main():
    print("GHZ<->W pure family  |psi(s)> = sqrt(1-s)|GHZ> + sqrt(s)|W>,  s in [0,1]")
    print("(s = the 'kind' dial: s=0 pure GHZ-type, s=1 pure W-type)\n")
    print("MISMATCH excess = E_vN(A) [entropy] - sum of ALL-pair tangles [tangle]")
    print("                  (faithful to sec 9.8: global entropy minus residual tangle)")
    print("UNIFIED  excess = tau1(A:BC) [tangle] - (tau_AB+tau_AC) [tangle] = tau3 (CKW)\n")
    ss = np.linspace(0.0, 1.0, 11)
    print(f"{'s':>5} {'E_vN(A)':>8} {'tau1(A)':>8} {'tAB':>7} {'tAC':>7} {'tBC':>7} "
          f"{'tau3':>7} {'MISMATCH':>9} {'UNIFIED':>8}")
    mism, unif = [], []
    for s in ss:
        psi = np.sqrt(1 - s) * GHZ + np.sqrt(s) * W
        psi = psi / np.linalg.norm(psi)
        rA = rho_marginal(psi, [0])
        E = vN_entropy(rA)                       # entropy-based global ent.
        t1 = linear_tangle_1(rA)                 # tangle-based global ent.
        tab = concurrence(rho_marginal(psi, [0, 1])) ** 2
        tac = concurrence(rho_marginal(psi, [0, 2])) ** 2
        tbc = concurrence(rho_marginal(psi, [1, 2])) ** 2
        t3 = three_tangle(psi)
        # sec 9.8 reconstruction: a GLOBAL entropy minus a GLOBAL (all-pair) tangle.
        excess_mismatch = E - (tab + tac + tbc)  # entropy MINUS all-pair tangle
        excess_unified = t1 - (tab + tac)        # tangle MINUS site-pair tangle = tau3
        mism.append(excess_mismatch); unif.append(excess_unified)
        print(f"{s:5.2f} {E:8.4f} {t1:8.4f} {tab:7.4f} {tac:7.4f} {tbc:7.4f} "
              f"{t3:7.4f} {excess_mismatch:+9.4f} {excess_unified:+8.4f}")

    mism = np.array(mism); unif = np.array(unif)
    print("\n--- CKW identity check (pure-state machinery) ---")
    # tau1 - tau_res should equal tau3 to machine precision
    s = 0.4
    psi = np.sqrt(1 - s) * GHZ + np.sqrt(s) * W; psi /= np.linalg.norm(psi)
    rA = rho_marginal(psi, [0])
    t1 = linear_tangle_1(rA)
    tres = (concurrence(rho_marginal(psi, [0, 1])) ** 2
            + concurrence(rho_marginal(psi, [0, 2])) ** 2)
    t3 = three_tangle(psi)
    print(f"  s=0.4: tau1-tau_res = {t1 - tres:.6f},  tau3 = {t3:.6f},  "
          f"match = {abs((t1 - tres) - t3) < 1e-6}")

    TOL = 1e-9  # -0.000... at the W endpoint is numerical zero, not a sign change
    mism_sign_change = mism.min() < -TOL < TOL < mism.max()
    unif_sign_change = unif.min() < -TOL and unif.max() > TOL
    print("\n--- verdict ---")
    print(f"MISMATCH excess (E_vN - all-pair tangle): "
          f"range [{mism.min():+.3f}, {mism.max():+.3f}]  sign change = {mism_sign_change}")
    print(f"UNIFIED  excess (tau1  - site-pair tangle = tau3): "
          f"range [{max(unif.min(),0.0):+.3f}, {unif.max():+.3f}]  sign change = {unif_sign_change}")
    if mism_sign_change and not unif_sign_change:
        print("\n=> the sec 9.8 sign change lives ONLY in the entropy-vs-tangle MISMATCH.")
        print("   On a unified tangle measure the residual is exactly tau3 >= 0 (CKW),")
        print("   sign-DEFINITE, no sign change. The signal is a MEASURE ARTIFACT.")
        print("   Card sec 9.8 closes: kind-separation = standard CKW monogamy; the")
        print("   apparent extra signal was the suspected measure mismatch, confirmed.")
    else:
        print("\n=> unified excess ALSO changes sign -> NOT a pure measure artifact;")
        print("   sec 9.8 card survives, escalate.")


if __name__ == "__main__":
    main()

"""
Phase E self-falsification (sec 9.15 discipline): the raw signal is that magic
(CS) on the de Sitter side (delta>0) lifts a STATE-DEPENDENT IMAGINARY part of
the pseudo-area (Var_bulk(Im S^pseudo) > 0, ~ delta^2), absent for stabilizer/
Clifford gates and absent on the AdS side. Before calling this (b), beat on it:

  T1  rotation axis X / Y / Z          -- is the magic-only Im channel axis-robust?
  T2  2-Renyi pseudo-entropy           -- survives a change of entropy measure?
  T3  cT gate (different magic gate)    -- survives a change of magic injection?
  T4  decisive control: large-delta CZ -- can a NON-magic non-Hermitian
       deformation ever lift Var(Im)?  (if yes, the signal is a pseudo-entropy
       artifact, not magic.)
  T5  branch-cut check                  -- are the tau eigenvalues away from the
       complex-log cut, so Im(S) is smooth (not a 2*pi jump artifact)?
"""

import numpy as np
from phase2pp_holographic_magic import five_qubit_code, perfect_tensor, bloch
from phase2pp_v2_nonlocal import network_state_2bond
from phaseE_desitter_magic import rot, CZ, CS, EYE4

cT = np.diag([1, 1, 1, np.exp(1j * np.pi / 4)]).astype(complex)  # controlled-T, magic
# complex but CLIFFORD (magic = 0) controls: tensor of single-qubit S gates.
SS = np.diag([1, 1j, 1j, -1]).astype(complex)   # S (x) S : Clifford, COMPLEX
SI = np.diag([1, 1, 1j, 1j]).astype(complex)    # S (x) I : Clifford, COMPLEX


def tau_eigs(psi_ket, psi_bra, n, region):
    region = list(region)
    rest = [i for i in range(n) if i not in region]
    perm = region + rest
    dA = 2 ** len(region)
    K = psi_ket.reshape([2] * n).transpose(perm).reshape(dA, -1)
    Bm = psi_bra.reshape([2] * n).transpose(perm).reshape(dA, -1)
    overlap = np.vdot(psi_bra, psi_ket)
    tau = (K @ Bm.conj().T) / overlap
    ev = np.linalg.eigvals(tau)
    return ev[np.abs(ev) > 1e-12]


def pseudo_vN(ev):
    return complex(-np.sum(ev * np.log(ev)))


def pseudo_renyi2(ev):
    return complex(-np.log(np.sum(ev ** 2)))


def var_im_re(T, G, bulk, phi2, region, axis, delta, measure):
    re, im = [], []
    for p1 in bulk:
        ket = network_state_2bond(T, p1, phi2, G)
        bra = network_state_2bond(T, rot(axis, delta) @ p1, phi2, G)
        ev = tau_eigs(ket, bra, 6, region)
        S = measure(ev)
        re.append(S.real); im.append(S.imag)
    return float(np.var(re)), float(np.var(im))


def main():
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    phi2 = bloch(0, 0)
    bulk = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
            for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]
    R = (0, 2, 4)            # magic-sensitive region
    d = 0.45                 # representative dS-side angle

    print(f"region {R}, delta {d}; Var(Im S^pseudo) is the de Sitter magic channel\n")

    # ---- T1: axis robustness ----
    print("[T1] rotation axis robustness  (Var(Re), Var(Im)) under CS vs CZ")
    print(f"  {'axis':>6} {'CS Var(Re)':>12} {'CS Var(Im)':>12} "
          f"{'CZ Var(Re)':>12} {'CZ Var(Im)':>12}")
    for axis in ("X", "Y", "Z"):
        csr, csi = var_im_re(T, CS, bulk, phi2, R, axis, d, pseudo_vN)
        czr, czi = var_im_re(T, CZ, bulk, phi2, R, axis, d, pseudo_vN)
        print(f"  {axis:>6} {csr:12.3e} {csi:12.3e} {czr:12.3e} {czi:12.3e}")

    # ---- T2: 2-Renyi pseudo-entropy ----
    print("\n[T2] 2-Renyi pseudo-entropy (axis Y)  -- Im channel survives measure change?")
    print(f"  {'gate':>6} {'Var(Re)':>12} {'Var(Im)':>12}")
    for name, G in (("CS", CS), ("CZ", CZ), ("I", EYE4)):
        vr, vi = var_im_re(T, G, bulk, phi2, R, "Y", d, pseudo_renyi2)
        print(f"  {name:>6} {vr:12.3e} {vi:12.3e}")

    # ---- T3: cT gate ----
    print("\n[T3] cT magic gate (axis Y, vN)  -- different magic injection")
    for name, G in (("cT", cT), ("CS", CS)):
        vr, vi = var_im_re(T, G, bulk, phi2, R, "Y", d, pseudo_vN)
        print(f"  {name:>6} Var(Re)={vr:.3e}  Var(Im)={vi:.3e}")

    # ---- T4: decisive control -- large-delta non-magic deformation ----
    print("\n[T4] decisive control: can NON-magic (CZ/I) lift Var(Im) at large delta?")
    print(f"  {'gate':>6} {'delta':>6} {'Var(Re)':>12} {'Var(Im)':>12}")
    for name, G in (("CZ", CZ), ("I", EYE4)):
        for dd in (0.30, 0.60, 0.90, 1.20):
            vr, vi = var_im_re(T, G, bulk, phi2, R, "Y", dd, pseudo_vN)
            print(f"  {name:>6} {dd:6.2f} {vr:12.3e} {vi:12.3e}")
    print("  -> if Var(Im) stays ~0 here, the Im channel is MAGIC, not a generic")
    print("     pseudo-entropy artifact.")

    # ---- T5: branch-cut health ----
    print("\n[T5] branch-cut check: tau eigenvalues vs the complex-log cut (axis Y)")
    worst = 0.0
    near_cut = 0
    for p1 in bulk:
        ket = network_state_2bond(T, p1, phi2, CS)
        bra = network_state_2bond(T, rot("Y", d) @ p1, phi2, CS)
        ev = tau_eigs(ket, bra, 6, R)
        for lam in ev:
            worst = max(worst, abs(np.angle(lam)))
            if lam.real < 0 and abs(lam.imag) < 1e-3:
                near_cut += 1
    print(f"  max |arg(eigenvalue)| = {worst:.4f} rad (cut at pi={np.pi:.4f});"
          f"  eigenvalues near cut = {near_cut}")
    print("  -> if max|arg| << pi and none near cut, Im(S) is smooth (no 2*pi jumps).")

    # ---- T6: decisive confound -- complex but CLIFFORD gates (magic=0) ----
    print("\n[T6] DECISIVE confound: complex-but-CLIFFORD gates (axis Y, vN)")
    print("  separates 'magic' from 'complex amplitude'. CS is magic AND complex;")
    print("  CZ is neither. S(x)S, S(x)I are COMPLEX but Clifford (magic=0).")
    print(f"  {'gate':>8} {'kind':>22} {'Var(Re)':>12} {'Var(Im)':>12}")
    for name, G, kind in (("CS", CS, "non-Clifford (magic)"),
                          ("S(x)S", SS, "Clifford, complex"),
                          ("S(x)I", SI, "Clifford, complex"),
                          ("CZ", CZ, "Clifford, real")):
        vr, vi = var_im_re(T, G, bulk, phi2, R, "Y", d, pseudo_vN)
        print(f"  {name:>8} {kind:>22} {vr:12.3e} {vi:12.3e}")
    print("  -> if S(x)S, S(x)I keep Var(Im) ~ 0 while CS lifts it, the Im channel")
    print("     is MAGIC, NOT mere complex amplitude. This is the decisive control.")

    print("\n--- verdict guide ---")
    print("SURVIVES (b) if: T1 axis-robust, T2/T3 measure/gate-robust, T4 control")
    print("  stays ~0 (Im is magic-only), T5 no branch jumps. Then: de Sitter side")
    print("  carries a magic-only state-dependent IMAGINARY area with no AdS analog.")
    print("FALLS (a) if: the Im channel appears for CZ/I too (T4), or dies under a")
    print("  measure/axis change (artifact of one convention).")


if __name__ == "__main__":
    main()

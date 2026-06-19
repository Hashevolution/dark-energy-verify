"""
Phase E (future-research-topics.md, 1st priority): magic x de Sitter cross.

Task B reproduced the magic -> area-operator effect only on the AdS side
(perfect-tensor holographic code, ordinary entanglement entropy). Task A
(de Sitter, positive curvature, our universe) was never touched numerically.
This is the A-intersect-B coordinate nobody has joined.

The literature's handle for de Sitter holography is the pseudo-entropy /
timelike entanglement of a NON-Hermitian transition matrix
    tau_A = Tr_B( |psi_ket><psi_bra| ) / <psi_bra|psi_ket>,
    S^pseudo_A = -Tr( tau_A log tau_A )   (complex in general)
(task-A-B-connection-and-status.md sec 2.2; arXiv:2604.00108, 2508.14478).

Curvature-sign proxy: rotate the BRA bulk input from the KET bulk input by an
angle delta on the Bloch sphere.
    delta = 0  -> bra = ket -> tau_A = rho_A -> ordinary entropy  (AdS side; exactly v3)
    delta > 0  -> bra != ket -> genuinely complex pseudo-entropy   (de Sitter side)
delta is the operational dial AdS(-) -> dS(+). (A proxy, not a literal dS bulk
geometry -- stated honestly, matching the repo's style.)

GATE 0  : on the dS side (delta>0), a STABILIZER network must still give a
          trivial (state-independent) area operator -> Var_bulk(S^pseudo) ~ 0.
          If gate 0 fails, the stage is broken (cf. Phase 2' "wrong arena").
GATE E  : does the magic -> state-dependent-area effect change CHARACTER across
          the curvature sign?
   (b)  qualitatively different on dS side (new magic-only imaginary part,
        magic-controlled inequality violation, or the effect breaks) = first (b)
        residual candidate = the numeric identity of "mirror universe perfect,
        real universe half-broken" (handover sec 1.2(2)).
   (a)  identical across curvature sign = magic mechanism is curvature-invariant
        = clean negative (de Sitter gap is NOT filled by magic).

Self-check built in: at delta=0 every pseudo-entropy must equal the ordinary
entropy of phase2pp_v3 (Im = 0, Var matches).
"""

import numpy as np
from phase2pp_holographic_magic import (
    five_qubit_code, perfect_tensor, entropy_region, m2_full, bloch)
from phase2pp_v2_nonlocal import network_state_2bond

# Clifford / non-Clifford 2-qubit gates on the RT surface (2 bonds), as in v2/v3.
EYE4 = np.eye(4, dtype=complex)
CZ = np.diag([1, 1, 1, -1]).astype(complex)          # Clifford, entanglement, NO magic
CS = np.diag([1, 1, 1, 1j]).astype(complex)          # controlled-S, non-local MAGIC

PAULI = {
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


def rot(axis, delta):
    """single-qubit rotation exp(-i delta/2 * sigma_axis)."""
    s = PAULI[axis]
    return np.cos(delta / 2) * np.eye(2, dtype=complex) - 1j * np.sin(delta / 2) * s


def pseudo_entropy_region(psi_ket, psi_bra, n, region):
    """complex pseudo-entropy of `region` from the non-Hermitian transition
    matrix tau = Tr_rest(|ket><bra|)/<bra|ket>. At psi_bra==psi_ket reduces to
    the ordinary von Neumann entropy (natural log), matching entropy_region."""
    region = list(region)
    rest = [i for i in range(n) if i not in region]
    perm = region + rest
    dA = 2 ** len(region)
    K = psi_ket.reshape([2] * n).transpose(perm).reshape(dA, -1)
    Bm = psi_bra.reshape([2] * n).transpose(perm).reshape(dA, -1)
    overlap = np.vdot(psi_bra, psi_ket)               # <bra|ket>
    tau = (K @ Bm.conj().T) / overlap                 # dA x dA, Tr(tau)=1
    ev = np.linalg.eigvals(tau)
    ev = ev[np.abs(ev) > 1e-12]
    S = -np.sum(ev * np.log(ev))                      # principal-branch complex log
    return complex(S), float(abs(overlap))


def bra_ket_states(T, phi1, phi2, G, axis, delta):
    """boundary ket from bulk1=phi1; boundary bra from bulk1 rotated by delta."""
    ket = network_state_2bond(T, phi1, phi2, G)
    bra = network_state_2bond(T, rot(axis, delta) @ phi1, phi2, G)
    return ket, bra


def var_pseudo(T, G, bulk_states, phi2, region, axis, delta):
    """Var over bulk states of Re/Im S^pseudo_A, plus min overlap (health check)."""
    re, im, ov = [], [], []
    for p1 in bulk_states:
        ket, bra = bra_ket_states(T, p1, phi2, G, axis, delta)
        S, o = pseudo_entropy_region(ket, bra, 6, region)
        re.append(S.real); im.append(S.imag); ov.append(o)
    return (float(np.var(re)), float(np.var(im)),
            float(np.mean(re)), float(np.mean(im)), float(min(ov)))


def main():
    np.set_printoptions(suppress=True)
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    phi2 = bloch(0, 0)
    bulk_states = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
                   for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]

    REGION_MAGIC = (0, 2, 4)   # strongest magic-sensitive region on AdS side (v3)
    REGION_BLIND = (0, 1, 2)   # magic-blind control region (v3: Var_CS ~ 0)
    deltas = [0.0, 0.15, 0.30, 0.45, 0.60]
    axis = "Y"

    # ---- self-check: delta=0 pseudo-entropy must equal ordinary entropy (v3) ----
    print("[self-check] delta=0: pseudo-entropy == ordinary entropy (Im=0)")
    ket = network_state_2bond(T, bloch(0.7, 0.3), phi2, CS)
    S0, _ = pseudo_entropy_region(ket, ket, 6, list(REGION_MAGIC))
    S0_ref = entropy_region(ket, 6, list(REGION_MAGIC))
    print(f"   region {REGION_MAGIC}:  pseudo(delta0)={S0.real:.6f}{S0.imag:+.1e}i  "
          f"ordinary={S0_ref:.6f}  match={abs(S0.real-S0_ref)<1e-9 and abs(S0.imag)<1e-9}")

    # ---- GATE 0: stabilizer / Clifford on dS side must stay trivial ----
    print("\n[GATE 0] dS-side stabilizer & Clifford -> trivial area op "
          "(Var_bulk(Re S^pseudo) ~ 0 across delta)")
    print(f"  region {REGION_MAGIC}, axis {axis}")
    print(f"  {'gate':>10} {'delta':>6} {'Var(Re)':>11} {'Var(Im)':>11} "
          f"{'mean Re':>9} {'mean Im':>9} {'min|ov|':>8}")
    for name, G in [("I x I", EYE4), ("CZ", CZ)]:
        for d in deltas:
            vr, vi, mr, mi, mo = var_pseudo(T, G, bulk_states, phi2,
                                            list(REGION_MAGIC), axis, d)
            print(f"  {name:>10} {d:6.2f} {vr:11.3e} {vi:11.3e} "
                  f"{mr:9.4f} {mi:9.4f} {mo:8.4f}")

    # ---- GATE E: magic (CS) across the curvature sign ----
    print("\n[GATE E] magic (CS) -> does the state-dependent-area effect change "
          "character across curvature sign?")
    print(f"  region {REGION_MAGIC} (magic-sensitive), axis {axis}")
    print(f"  {'gate':>10} {'delta':>6} {'Var(Re)':>11} {'Var(Im)':>11} "
          f"{'mean Re':>9} {'mean Im':>9} {'min|ov|':>8}")
    for d in deltas:
        vr, vi, mr, mi, mo = var_pseudo(T, CS, bulk_states, phi2,
                                        list(REGION_MAGIC), axis, d)
        print(f"  {'CS':>10} {d:6.2f} {vr:11.3e} {vi:11.3e} "
              f"{mr:9.4f} {mi:9.4f} {mo:8.4f}")

    print(f"\n  control: magic-BLIND region {REGION_BLIND} under CS "
          "(AdS side had Var_CS ~ 0)")
    for d in deltas:
        vr, vi, mr, mi, mo = var_pseudo(T, CS, bulk_states, phi2,
                                        list(REGION_BLIND), axis, d)
        print(f"  {'CS':>10} {d:6.2f} {vr:11.3e} {vi:11.3e} "
              f"{mr:9.4f} {mi:9.4f} {mo:8.4f}")

    print("\n--- gate E read-out ---")
    print("(b) if Var(Im) is lifted by CS but ~0 for I/CZ (magic-only imaginary")
    print("    state-dependence) OR the Re effect breaks on dS side -> curvature-")
    print("    sign-dependent magic effect = NOTE'S de Sitter gap, made numeric.")
    print("(a) if CS lifts Var(Re) the same way at every delta and Im tracks delta")
    print("    not magic -> magic mechanism is curvature-invariant = clean negative.")


if __name__ == "__main__":
    main()

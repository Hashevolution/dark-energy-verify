"""
Phase E decisive control: complex-Clifford confound scan.

phase2pp_v3 used only CZ (a REAL Clifford) as the "entanglement, no magic"
control and concluded that the state-dependent area operator is caused by MAGIC.
This script adds the missing controls: single-bond / product COMPLEX Clifford
gates (S(x)I, I(x)S, S(x)S), which are magic-free (boundary M2 unchanged) but
COMPLEX. If any of them reproduces the "state-dependence" that v3 attributed to
magic, the magic attribution is confounded.

Result (see phaseE_RESULTS.md): in this minimal two-perfect-tensor code there is
NO region where CS (magic) lifts Var_bulk(S_A) while ALL magic-free gates leave
it ~0. For every magic-sensitive region, some local complex Clifford phase lifts
it MORE than CS. The minimal code cannot separate magic from local complex phase
= finite-size artifact. Same failure mode that retracted Phase 2's first verdict.
"""

import itertools
import numpy as np
from phase2pp_holographic_magic import five_qubit_code, perfect_tensor, m2_full, bloch
from phase2pp_v2_nonlocal import network_state_2bond
from phaseE_desitter_magic import rot, pseudo_entropy_region

# magic-free controls (all leave boundary M2 unchanged) + the magic gate CS
NONMAGIC = {
    "I":   np.eye(4, dtype=complex),
    "CZ":  np.diag([1, 1, 1, -1]).astype(complex),    # Clifford, real
    "SxS": np.diag([1, 1j, 1j, -1]).astype(complex),  # Clifford, complex (product)
    "SxI": np.diag([1, 1, 1j, 1j]).astype(complex),   # Clifford, complex (bond a)
    "IxS": np.diag([1, 1j, 1, 1j]).astype(complex),   # Clifford, complex (bond b)
}
CS = np.diag([1, 1, 1, 1j]).astype(complex)           # non-Clifford, MAGIC


def setup():
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    phi2 = bloch(0, 0)
    bulk = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
            for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]
    return T, phi2, bulk


def var_re(T, phi2, bulk, G, region, delta=0.0, axis="Y"):
    re = []
    for p1 in bulk:
        ket = network_state_2bond(T, p1, phi2, G)
        bra = network_state_2bond(T, rot(axis, delta) @ p1, phi2, G) if delta else ket
        S, _ = pseudo_entropy_region(ket, bra, 6, list(region))
        re.append(S.real)
    return float(np.var(re))


def main():
    T, phi2, bulk = setup()

    # confirm all controls are magic-free on the boundary
    print("[magic content] boundary M2 of each gate (magic-free controls = bare value)")
    bare = m2_full(network_state_2bond(T, bloch(0.7, 0.3), phi2, NONMAGIC["I"]), 6)
    for nm, G in {**NONMAGIC, "CS": CS}.items():
        mb = m2_full(network_state_2bond(T, bloch(0.7, 0.3), phi2, G), 6)
        tag = "magic-free" if abs(mb - bare) < 1e-9 else "MAGIC"
        print(f"   {nm:>4}  M2_bdy={mb:.4f}  ({tag})")

    print("\n[AdS side, delta=0] Var_bulk(S_A); looking for a CLEAN magic region")
    print("CLEAN = CS>1e-6 AND every magic-free gate <1e-9\n")
    print(f"{'region':>12} " + " ".join(f"{k:>9}" for k in NONMAGIC) + f"{'CS':>10}  verdict")
    clean = []
    for sz in (2, 3):
        for r in itertools.combinations(range(6), sz):
            vals = {k: var_re(T, phi2, bulk, G, r) for k, G in NONMAGIC.items()}
            cs = var_re(T, phi2, bulk, CS, r)
            nm_max = max(vals.values())
            is_clean = cs > 1e-6 and nm_max < 1e-9
            if cs > 1e-6:  # only print regions where magic does something
                verdict = "CLEAN" if is_clean else "confounded"
                print(f"{str(r):>12} " + " ".join(f"{vals[k]:9.1e}" for k in NONMAGIC)
                      + f"{cs:10.2e}  {verdict}")
            if is_clean:
                clean.append(r)

    print(f"\nclean magic-only regions: {len(clean)}  -> {clean}")
    print("\n--- verdict ---")
    if not clean:
        print("(a) / INCONCLUSIVE by confound: NO region isolates magic. For every")
        print("    magic-sensitive region a LOCAL COMPLEX CLIFFORD phase (magic-free)")
        print("    reproduces/exceeds the state-dependence. The minimal 2-tensor code")
        print("    conflates magic with local complex phase = finite-size artifact.")
        print("    => the de Sitter Im channel inherits the same confound; GATE E")
        print("       cannot certify a magic-specific de Sitter effect HERE.")
        print("    => and Phase 2'' is retroactively downgraded: v3's real-Clifford")
        print("       (CZ) control was insufficient; magic attribution fails the")
        print("       complex-Clifford control. Next stage: LARGER holographic code")
        print("       where single-bond phases are genuinely removable.")
    else:
        print("clean region(s) exist: re-run phaseE on them for an unconfounded test.")


if __name__ == "__main__":
    main()

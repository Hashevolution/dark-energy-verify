"""
Phase E' verification: are the 3-tensor "clean" regions REALLY magic-only?

Phase E's lesson: an under-powered control set fakes a clean signal. The scan used
only 4 magic-free gates. Here we test the candidate clean regions against the FULL
set of DIAGONAL 2-qubit gates diag(1, i^a, i^b, i^c) (a,b,c in 0..3 -> 64 gates),
matched to the magic gate CS = diag(1,1,1,i)'s structure. Each is classified
magic-free (Clifford) vs magic by the boundary stabilizer-2-Renyi entropy, then we
demand:
    every MAGIC-FREE diagonal gate -> Var_bulk(S_R) < 1e-9   (trivial area)
    every MAGIC      diagonal gate -> Var_bulk(S_R) > 1e-6   (state-dependent)
A region passing BOTH is genuinely magic-only: the confound is resolved.

Also robustness: repeat with randomized bulk references phi2, phi3 (the scan fixed
them to |0>), since a clean region must not depend on that choice.
"""

import itertools
import numpy as np
from phase2pp_holographic_magic import (
    five_qubit_code, perfect_tensor, entropy_region, m2_full, bloch)
from phaseEprime_3tensor import network_3tensor, EYE4


def diagonal_gates():
    """all 64 diag(1, i^a, i^b, i^c); returns list of (label, 4x4 gate)."""
    out = []
    for a, b, c in itertools.product(range(4), repeat=3):
        g = np.diag([1, 1j ** a, 1j ** b, 1j ** c]).astype(complex)
        out.append((f"({a}{b}{c})", g))
    return out


def classify(T, gates, phi2, phi3, place):
    """split diagonal gates into magic-free vs magic by boundary M2."""
    bare = m2_full(network_3tensor(T, bloch(0.7, 0.3), phi2, phi3, EYE4, EYE4), 7)
    free, magic = [], []
    for lbl, g in gates:
        G1 = g if place[0] else EYE4
        G2 = g if place[1] else EYE4
        mb = m2_full(network_3tensor(T, bloch(0.7, 0.3), phi2, phi3, G1, G2), 7)
        (free if abs(mb - bare) < 1e-6 else magic).append((lbl, g))
    return free, magic


def var_region(T, g, place, bulk, phi2, phi3, region):
    G1 = g if place[0] else EYE4
    G2 = g if place[1] else EYE4
    vals = [entropy_region(network_3tensor(T, p1, phi2, phi3, G1, G2), 7, list(region))
            for p1 in bulk]
    return float(np.var(vals))


def verify_region(T, region, place, bulk, phi2, phi3, gates, label=""):
    free, magic = classify(T, gates, phi2, phi3, place)
    free_vars = [var_region(T, g, place, bulk, phi2, phi3, region) for _, g in free]
    magic_vars = [var_region(T, g, place, bulk, phi2, phi3, region) for _, g in magic]
    max_free = max(free_vars)
    min_magic = min(magic_vars) if magic_vars else float("nan")
    clean = max_free < 1e-9 and min_magic > 1e-6
    print(f"  region {str(region):>14} [{label}]  "
          f"#free={len(free)} max Var_free={max_free:.2e} | "
          f"#magic={len(magic)} min Var_magic={min_magic:.2e}  "
          f"-> {'CLEAN' if clean else 'CONFOUNDED'}")
    return clean


def main():
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    bulk = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
            for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]
    gates = diagonal_gates()
    z = bloch(0, 0)

    candidates = [
        ((2, 4), (True, False), "G1"),
        ((1, 2, 5), (False, True), "G2"),
        ((0, 3, 4, 6), (False, True), "G2"),
        ((0, 2, 5), (True, True), "both"),
        ((1, 3, 4, 6), (True, True), "both"),
    ]

    print("### full diagonal-gate control (64 gates), bulk refs phi2=phi3=|0> ###")
    survivors = []
    for region, place, lbl in candidates:
        if verify_region(T, region, place, bulk, z, z, gates, lbl):
            survivors.append((region, place, lbl))

    print("\n### robustness: randomized bulk references phi2, phi3 ###")
    rng = np.random.default_rng(0)
    for region, place, lbl in survivors:
        ok = True
        for _ in range(3):
            phi2 = bloch(rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi))
            phi3 = bloch(rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi))
            ok &= verify_region(T, region, place, bulk, phi2, phi3, gates, lbl + "/rnd")
        if ok:
            print(f"  -> region {region} robustly clean under randomized bulk refs")

    print("\n--- verdict ---")
    if survivors:
        print(f"{len(survivors)} region(s) pass the FULL diagonal-gate control:")
        print("  every magic-free diagonal gate -> trivial area; every magic diagonal")
        print("  gate -> state-dependent. The 3-tensor (larger) code RESOLVES the")
        print("  Phase E confound -> magic is isolated as the cause of the state-")
        print("  dependent area operator (Cao et al. reproduced cleanly).")
    else:
        print("No region survives the full control -> the confound persists; the scan's")
        print("'clean' regions were artifacts of the under-powered 4-gate control set.")


if __name__ == "__main__":
    main()

"""
Phase E' confound scan on the 3-tensor code.

region A = T1.(0,1,2) saturates (S_A = 2 ln2, RT surface = 2 bonds) so NOTHING
lifts Var there -- no room for a state-dependent area. Following Phase E, scan ALL
sub-maximal boundary regions and classify magic-sensitivity vs the complex-Clifford
confound, with magic injected on the RT surfaces (G1 = T1-T2, G2 = T2-T3).

For each region R and each surface choice, compute Var_bulk(S_R) under:
  magic-free gates {I, CZ, SxS, SxI, IxS}   and   magic gate CS.
A region is:
  CLEAN magic-sensitive  if Var_CS > 1e-6 AND every magic-free gate < 1e-9,
  CONFOUNDED             if Var_CS > 1e-6 but some magic-free gate also > 1e-9.
The decisive question: does the 3-tensor code yield ANY clean magic-only region
(Phase E had zero), i.e. does enlarging the code resolve the confound?
"""

import itertools
import numpy as np
from phase2pp_holographic_magic import five_qubit_code, perfect_tensor, entropy_region, bloch
from phaseEprime_3tensor import (
    network_3tensor, MAGIC_FREE, CS, EYE4)


def var_region(T, G1, G2, bulk, phi2, phi3, region):
    vals = [entropy_region(network_3tensor(T, p1, phi2, phi3, G1, G2), 7, list(region))
            for p1 in bulk]
    return float(np.var(vals)), float(np.mean(vals))


def scan(T, bulk, phi2, phi3, surfaces):
    """surfaces: dict label -> (G1_is_surface, G2_is_surface) telling where the
    scanned gate is placed."""
    clean, confounded = [], []
    for sz in (2, 3, 4):
        for region in itertools.combinations(range(7), sz):
            place = surfaces  # (which of G1/G2 carries the gate)
            def G1G2(gate):
                return (gate if place[0] else EYE4, gate if place[1] else EYE4)
            vcs, mcs = var_region(T, *G1G2(CS), bulk, phi2, phi3, region)
            if vcs <= 1e-6:
                continue
            nm_max = 0.0
            worst = ""
            for nm, G in MAGIC_FREE.items():
                if nm == "I":
                    continue
                v, _ = var_region(T, *G1G2(G), bulk, phi2, phi3, region)
                if v > nm_max:
                    nm_max, worst = v, nm
            if nm_max < 1e-9:
                clean.append((region, vcs))
            else:
                confounded.append((region, vcs, nm_max, worst))
    return clean, confounded


def main():
    zeroL, oneL = five_qubit_code()
    T = perfect_tensor(zeroL, oneL)
    phi2 = bloch(0, 0); phi3 = bloch(0, 0)
    bulk = [bloch(t, p) for t in np.linspace(0, np.pi, 4)
            for p in np.linspace(0, 2 * np.pi, 4, endpoint=False)]

    for label, place in [("magic on G1 (T1-T2)", (True, False)),
                         ("magic on G2 (T2-T3)", (False, True)),
                         ("magic on BOTH surfaces", (True, True))]:
        print(f"\n### scan: {label} ###")
        clean, confounded = scan(T, bulk, phi2, phi3, place)
        print(f"  CS-sensitive regions: {len(clean) + len(confounded)}  "
              f"(clean: {len(clean)}, confounded: {len(confounded)})")
        for region, vcs in clean[:8]:
            print(f"    CLEAN      {str(region):>14}  Var_CS={vcs:.2e}")
        for region, vcs, nmmax, worst in confounded[:8]:
            print(f"    confounded {str(region):>14}  Var_CS={vcs:.2e}  "
                  f"{worst}={nmmax:.2e}")

    print("\n--- verdict ---")
    print("If CLEAN > 0 for any surface: the 3-tensor code RESOLVES the Phase E")
    print("  confound -> magic isolated -> Cao et al. reproduced cleanly (larger code")
    print("  works; magic hypothesis pathway validated, modulo it being a rediscovery).")
    print("If CLEAN == 0 everywhere: the confound is STRUCTURAL at this size too ->")
    print("  faithful separation needs a genuinely large HaPPY tiling (intractable")
    print("  exactly) -> magic hypothesis stays unproven by tractable simulation.")


if __name__ == "__main__":
    main()

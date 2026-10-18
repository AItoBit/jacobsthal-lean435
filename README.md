# Jacobsthal Lean 4.35 compatibility candidate

**Status: candidate port; not yet verified on this toolchain.** A successful CI
run and the recorded final axiom reports are required before claiming verification.

This repository preserves the complete 819-module Jacobsthal import closure from
[OpenAI's mathematical development](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/NumberTheory/Jacobsthal).
The mathematics and original Lean proofs are OpenAI's work. This is dependency
curation and a compatibility port, not a claim of new mathematics.

The two actual closed targets are:

* `OAI.Erdos970.Erdos970Final.erdos_970_quadratic`
* `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log`

They are imported through `OAI.NumberTheory.Jacobsthal.Main`. Their statements
and mathematical hypotheses are retained. `Audit.lean` checks both target names
and prints their transitive axioms.

## Reproduce

Lean is pinned to `v4.35.0-rc2`; Mathlib is pinned to
`065356127b1dc0016f66b7283ce0ce2c4055aa55`.

```sh
python3 scripts/bootstrap_strongpnt.py
lake update
lake exe cache get
LEAN_NUM_THREADS=2 lake --wfail build OAI.NumberTheory.Jacobsthal.Main Audit
lake env lean -j2 -DwarningAsError=true Audit.lean
```

The Lake configuration also runs the external-source bootstrap before dependency
resolution. The bootstrap requires Python 3, Git and network access. No local
Lean build was run while preparing this candidate on the constrained Windows host.

## Dependency and license provenance

`provenance.json` records original package pins and the exact retained module
lists. `patches/` contains OpenAI's substantial original compatibility patches,
normalized only to LF line endings. These patches contain mathematical code;
they are not described as merely mechanical edits.

* OpenAI sources: commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, Apache 2.0.
* PrimeNumberTheoremAnd: commit `c39a751132c88b6e8080b74c74023fd95b3d8be0`,
  with OpenAI's patch. Only the 19 imported modules are vendored; upstream
  Apache license is retained in `vendor/PrimeNumberTheoremAnd/LICENSE`.
* AbsorptionCutoff: commit `41c45c6d72e979419e46224bb7b4be5cee31f2b5`, with
  OpenAI's patch. Only five imported modules are vendored; upstream license
  and notice are retained in `vendor/AbsorptionCutoff/`.
* StrongPNT: commit `2f5835c322314f55f1026ec2f139d704b7c45c69`, with OpenAI's
  patch. The pinned upstream repository has no explicit license file. Its source
  is therefore fetched from upstream at build time, rather than redistributed
  as vendored text here. The upstream README credits Math Inc.'s Gauss agent
  and adaptations of PrimeNumberTheoremAnd; the bootstrap preserves that README.
  This port does not assign an Apache license to the underlying StrongPNT source.

The root `LICENSE` reproduces OpenAI's Apache license for its materials. Original
notices and applicable upstream licenses take precedence for third-party content.
No unrelated packages from OpenAI's larger development are requested.

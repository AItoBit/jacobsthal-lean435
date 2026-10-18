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

The initial recovered 819 files matched all original Git blob hashes after LF
normalization. The compatibility changes recorded in `provenance.json` currently
disambiguate two singleton sets by parenthesizing their elements, replace deprecated order
and coercion API names, and raise one theorem-local elaboration heartbeat budget. These edits preserve the mathematical statements and hypotheses.

## Reproduce

Lean is pinned to `v4.35.0-rc2`; Mathlib is pinned to
`065356127b1dc0016f66b7283ce0ce2c4055aa55`.

```sh
lake update
lake exe cache get
LEAN_NUM_THREADS=2 lake --wfail build OAI.NumberTheory.Jacobsthal.Main Audit
lake env lean -j2 -DwarningAsError=true Audit.lean
```

All twelve root manifest entries are immutable Git dependencies. There are no
local path dependencies, runtime source generators, patch hooks, or untracked
source requirements. After fetching the manifest dependencies and Mathlib cache,
the proof can be built without network access. No local Lean build was run while
preparing this candidate on the constrained Windows host.

## Dependency and license provenance

`provenance.json` records original package pins, curated Git pins, and the exact
module lists. `patches/` contains OpenAI's substantial original compatibility patches,
normalized only to LF line endings. These patches contain mathematical code;
they are not described as merely mechanical edits.

* OpenAI sources: commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, Apache 2.0.
* PrimeNumberTheoremAnd: commit `c39a751132c88b6e8080b74c74023fd95b3d8be0`,
  with OpenAI's patch. Only the 19 imported modules are retained in
  [the curated Git package](https://github.com/AItoBit/jacobsthal-pnt-lean435/tree/4698982c635e019c83b6216cbd9777e0a7f89198).
  Its upstream Apache license and provenance are preserved.
* AbsorptionCutoff: commit `41c45c6d72e979419e46224bb7b4be5cee31f2b5`, with
  OpenAI's patch. Only five imported modules are retained in
  [the curated Git package](https://github.com/AItoBit/jacobsthal-absorption-lean435/tree/4cab242c97bd91d5452af8e5f5f25cf23810fa97),
  with its upstream license and notice.
* StrongPNT's original build-context pin is
  `2f5835c322314f55f1026ec2f139d704b7c45c69`. The
  [curated Git package](https://github.com/AItoBit/jacobsthal-strongpnt-lean435/tree/b96d1670fb7fabf7ea55d67cc3bb69ce1f054953)
  reconstructs only the seven full **new-file additions** distributed in OpenAI's
  Apache-licensed patch. These were compared byte-for-byte after LF normalization;
  see `strongpnt-patch-additions.json`. No original unpatched StrongPNT files are
  included. Its notice preserves Math Inc./Gauss and PrimeNumberTheoremAnd credits.
  The original upstream repository has no explicit license file. This port makes
  no claim to assign a license to that entire repository or provide an independent
  legal determination concerning underlying third-party material.

The root `LICENSE` reproduces OpenAI's Apache license for its materials. Original
notices and applicable upstream licenses take precedence for third-party content.
No unrelated packages from OpenAI's larger development are requested.

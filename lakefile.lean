import Lake
open Lake DSL

package jacobsthalLean435 where
  version := v!"0.1.0"
  leanOptions := #[⟨`autoImplicit, false⟩]

require PrimeNumberTheoremAnd from git
  "https://github.com/AItoBit/jacobsthal-pnt-lean435.git" @ "4698982c635e019c83b6216cbd9777e0a7f89198"
require StrongPNT from git
  "https://github.com/AItoBit/jacobsthal-strongpnt-lean435.git" @ "b96d1670fb7fabf7ea55d67cc3bb69ce1f054953"
require AbsorptionCutoff from git
  "https://github.com/AItoBit/jacobsthal-absorption-lean435.git" @ "4cab242c97bd91d5452af8e5f5f25cf23810fa97"
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "065356127b1dc0016f66b7283ce0ce2c4055aa55"

@[default_target] lean_lib OAI where
  roots := #[`OAI.NumberTheory.Jacobsthal.Main]
  globs := #[`OAI.NumberTheory.Jacobsthal.+]

lean_lib Audit where
  roots := #[`Audit]

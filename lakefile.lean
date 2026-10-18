import Lake
open System Lake DSL

package jacobsthalLean435 where
  version := v!"0.1.0"
  leanOptions := #[⟨`autoImplicit, false⟩]

-- Fetch the externally pinned StrongPNT source before resolving its curated
-- package configuration. This follows OpenAI's pre-resolution patch ordering.
run_cmd do
  let env ← Lean.getEnv
  if let some root := Lake.dirExt.getState env then
    let result ← Lean.Elab.Command.liftIO <| IO.Process.output {
      cmd := "python3"
      args := #[(root / "scripts" / "bootstrap_strongpnt.py").toString]
    }
    unless result.exitCode == 0 do
      throwError "StrongPNT source preparation failed:\n{result.stderr}"

require PrimeNumberTheoremAnd from "vendor/PrimeNumberTheoremAnd"
require StrongPNT from "external/StrongPNT"
require AbsorptionCutoff from "vendor/AbsorptionCutoff"
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "065356127b1dc0016f66b7283ce0ce2c4055aa55"

@[default_target] lean_lib OAI where
  roots := #[`OAI.NumberTheory.Jacobsthal.Main]
  globs := #[`OAI.NumberTheory.Jacobsthal.+]

lean_lib Audit where
  roots := #[`Audit]

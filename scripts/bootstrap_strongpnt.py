"""Fetch StrongPNT at the recorded pin and apply OpenAI's exact mathematical patch.

The underlying StrongPNT source is intentionally not redistributed by this port.
No Lean compiler is invoked here.
"""
from pathlib import Path
import json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
PIN = "2f5835c322314f55f1026ec2f139d704b7c45c69"
URL = "https://github.com/math-inc/strongpnt.git"

def run(*args): subprocess.run(args, check=True)

def main():
    cache = ROOT / ".source-cache" / "StrongPNT"
    cache.mkdir(parents=True, exist_ok=True)
    if not (cache / ".git").exists():
        run("git", "init", str(cache))
        run("git", "-C", str(cache), "remote", "add", "origin", URL)
        run("git", "-C", str(cache), "config", "core.sparseCheckout", "true")
        (cache / ".git/info/sparse-checkout").write_text("*.lean\n/README.md\n/lakefile.toml\n/lean-toolchain\n")
        run("git", "-C", str(cache), "fetch", "--depth=1", "--filter=blob:none", "origin", PIN)
        run("git", "-C", str(cache), "checkout", "--detach", "FETCH_HEAD")
    actual = subprocess.check_output(["git", "-C", str(cache), "rev-parse", "HEAD"], text=True).strip()
    if actual != PIN: raise RuntimeError("StrongPNT checkout has unexpected commit " + actual)
    patch = ROOT / "patches/StrongPNT-lean4341.patch"
    reverse = subprocess.run(["git", "-C", str(cache), "apply", "--reverse", "--check", str(patch)], capture_output=True)
    if reverse.returncode:
        # Git on Windows can convert patch-added files to CRLF. Ignore only
        # whitespace when recognizing that already-applied mathematical patch.
        reverse = subprocess.run(["git", "-C", str(cache), "apply", "--ignore-space-change", "--reverse", "--check", str(patch)], capture_output=True)
    if reverse.returncode:
        run("git", "-C", str(cache), "apply", "--check", str(patch))
        run("git", "-C", str(cache), "apply", str(patch))
    package = ROOT / "external/StrongPNT"
    package.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "provenance.json").read_text())
    for relative in manifest["packages"]["StrongPNT"]["files"]:
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cache / relative, target)
    readme = subprocess.check_output(["git", "-C", str(cache), "show", "HEAD:README.md"])
    (package / "UPSTREAM-README.md").write_bytes(readme)
    config = '''name = "StrongPNT"
version = "0.1.0"

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "065356127b1dc0016f66b7283ce0ce2c4055aa55"

[[require]]
name = "PrimeNumberTheoremAnd"
path = "../../vendor/PrimeNumberTheoremAnd"

[[lean_lib]]
name = "StrongPNT"
roots = ["StrongPNT.Erdos970.PNT5_Strong"]
globs = ["StrongPNT.+"]
'''
    (package / "lakefile.toml").write_text(config, newline="\n")
    (package / "lean-toolchain").write_text("leanprover/lean4:v4.35.0-rc2\n")
    print("StrongPNT: pinned source + OpenAI patch ready (candidate compatibility port)", flush=True)

if __name__ == "__main__": main()

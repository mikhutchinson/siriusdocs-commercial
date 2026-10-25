#!/usr/bin/env python3
"""Explicit macOS app assembly; all downloads happen before app execution."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--binary", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--cache", type=Path, required=True)
parser.add_argument("--executable-name", default="DocumentExample")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
assert not args.output.exists(), "output must be new"
args.cache.mkdir(parents=True, exist_ok=True)
manifest = json.loads((root / "artifact-manifest.json").read_text())
resources = next(x for x in manifest["artifacts"] if x["filename"] == "SiriusDocsResources.zip")
downloads = [
    (resources["filename"], "https://github.com/mikhutchinson/siriusdocs-commercial/releases/download/0.1.0/SiriusDocsResources.zip", resources["sha256"]),
    ("SwiftPythonCommercial-0.7.0.zip", "https://github.com/mikhutchinson/swiftpython-commercial/releases/download/v0.7.0/SwiftPythonCommercial-0.7.0.zip", "b98db5aff4d1195310efaec85377c6c0b194baf84dedc8719a3d8500a20dc2f5"),
]
for name, url, digest in downloads:
    target = args.cache / name
    if not target.exists():
        subprocess.run(["curl", "--fail", "--location", "--output", str(target), url], check=True)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, name + " checksum mismatch"
    destination = args.cache / (name + ".unpacked")
    if not destination.exists():
        with zipfile.ZipFile(target) as archive:
            assert all(not n.startswith("/") and ".." not in Path(n).parts for n in archive.namelist())
        subprocess.run(["ditto", "-x", "-k", str(target), str(destination)], check=True)
runtime = args.cache / "SwiftPythonCommercial-0.7.0.zip.unpacked/swiftpython-commercial-0.7.0"
subprocess.run([sys.executable, str(root / "Integration/package_swift_consumer.py"),
    "--binary", str(args.binary.resolve()), "--runtime", str(runtime.resolve()),
    "--modules", str((args.cache / "SiriusDocsResources.zip.unpacked/PythonPackages").resolve()),
    "--swiftpython-license", str(runtime / "LICENSE"), "--output", str(args.output.resolve()),
    "--executable-name", args.executable_name], check=True)
print("Packaged " + str(args.output))

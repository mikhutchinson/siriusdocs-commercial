#!/usr/bin/env python3
"""Create a local, ad-hoc signed consumer app from exact built inputs."""

import argparse
import hashlib
import json
import plistlib
import shutil
import subprocess
from pathlib import Path

from macho_commands import external_absolute, parse_commands

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--binary", type=Path, required=True)
parser.add_argument("--runtime", type=Path, required=True)
parser.add_argument("--modules", type=Path, required=True)
parser.add_argument(
    "--swiftpython-license",
    type=Path,
    required=True,
    help="license supplied with this exact SwiftPython candidate",
)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--executable-name", default="SiriusPDFConsumer")
parser.add_argument("--bundle-id", default="dev.siriuspdf.sdk.local-consumer")
args = parser.parse_args()
license_bytes = args.swiftpython_license.read_bytes()
if not license_bytes.strip():
    parser.error("SwiftPython license must not be empty")
app = args.output.resolve()
if app.exists():
    parser.error("output already exists; use a new candidate path")
contents = app / "Contents"
executables = contents / "MacOS"
frameworks = contents / "Frameworks"
resources = contents / "Resources"
for directory in (executables, frameworks, resources):
    directory.mkdir(parents=True, exist_ok=True)
licenses = resources / "Licenses"
licenses.mkdir()
(licenses / "SwiftPython.txt").write_bytes(license_bytes)
binary = executables / args.executable_name
shutil.copy2(args.binary, binary)
load_commands = subprocess.check_output(["otool", "-l", str(binary)], text=True)
if "@executable_path/../Frameworks" not in load_commands:
    subprocess.run(
        [
            "install_name_tool",
            "-add_rpath",
            "@executable_path/../Frameworks",
            str(binary),
        ],
        check=True,
    )
for name in ("Python", "SwiftPythonEngine"):
    source = args.runtime / f"{name}.xcframework/macos-arm64_x86_64/{name}.framework"
    subprocess.run(
        ["ditto", str(source), str(frameworks / f"{name}.framework")], check=True
    )
shutil.copy2(args.runtime / "SwiftPythonWorker", executables / "SwiftPythonWorker")
packages = resources / "PythonPackages"
shutil.copytree(
    args.modules,
    packages,
    ignore=shutil.ignore_patterns(
        "__pycache__",
        "direct_url.json",
    ),
)
# The host uses callbacks, so it must not contain or invoke the standalone helper.
native = packages / "sirius_pdf/_native"
if native.exists():
    shutil.rmtree(native)
normalizations = []
for path in sorted(packages.rglob("*")):
    if path.suffix in {".so", ".dylib"}:
        commands = parse_commands(
            subprocess.check_output(["otool", "-l", str(path)], text=True)
        )
        if any(external_absolute(load) for load in commands["loads"]):
            raise ValueError(
                "Packaged native dependency has an external absolute load: "
                + str(path.relative_to(app))
            )
        for rpath in commands["rpaths"]:
            if external_absolute(rpath):
                subprocess.run(
                    ["install_name_tool", "-delete_rpath", rpath, str(path)], check=True
                )
                normalizations.append(
                    {"file": str(path.relative_to(app)), "removed_rpath": rpath}
                )
        subprocess.run(["codesign", "--force", "--sign", "-", str(path)], check=True)
subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
(contents / "Info.plist").write_bytes(
    plistlib.dumps(
        {
            "CFBundleExecutable": args.executable_name,
            "CFBundleIdentifier": args.bundle_id,
            "CFBundleName": args.executable_name,
            "CFBundlePackageType": "APPL",
            "CFBundleVersion": "1",
            "LSMinimumSystemVersion": "26.0",
        }
    )
)
subprocess.run(["codesign", "--force", "--sign", "-", str(app)], check=True)
subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)
hashes = {
    str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(app.rglob("*"))
    if p.is_file() and not p.is_symlink()
}
app.with_suffix(".sha256.json").write_text(json.dumps(hashes, indent=2) + "\n")
app.with_suffix(".normalization.json").write_text(
    json.dumps(normalizations, indent=2) + "\n"
)
print(json.dumps({"files": len(hashes), "distribution_qualified": False}))

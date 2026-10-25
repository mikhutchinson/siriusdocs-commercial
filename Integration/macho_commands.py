"""Distinguish Mach-O dependency loads, install identity and runtime search paths."""

from __future__ import annotations

import re

DEPENDENCY_COMMANDS = {
    "LC_LOAD_DYLIB",
    "LC_LOAD_WEAK_DYLIB",
    "LC_REEXPORT_DYLIB",
    "LC_LOAD_UPWARD_DYLIB",
}


def parse_commands(text: str) -> dict[str, list[str]]:
    records: dict[str, set[str]] = {
        "loads": set(),
        "install_ids": set(),
        "rpaths": set(),
    }
    for block in re.split(r"(?m)^Load command \d+\s*$", text)[1:]:
        command = re.search(r"(?m)^\s*cmd (LC_\w+)\s*$", block)
        if command is None:
            continue
        kind = command[1]
        field = "path" if kind == "LC_RPATH" else "name"
        value = re.search(rf"(?m)^\s*{field} (.+?) \(offset \d+\)\s*$", block)
        if value is None:
            continue
        if kind in DEPENDENCY_COMMANDS:
            records["loads"].add(value[1])
        elif kind == "LC_ID_DYLIB":
            records["install_ids"].add(value[1])
        elif kind == "LC_RPATH":
            records["rpaths"].add(value[1])
    return {key: sorted(values) for key, values in records.items()}


def external_absolute(value: str) -> bool:
    return value.startswith("/") and not value.startswith(
        ("/usr/lib/", "/System/Library/")
    )

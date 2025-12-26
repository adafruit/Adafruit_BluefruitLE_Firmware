#!/usr/bin/env python3
"""Update releases.xml with a new firmware (or beta) entry.

Usage:
  python make-release.py <version> [--beta|--promote-beta]

The script scans the firmware files under either ``<version>/`` or
``beta/<version>/`` (when ``--beta`` is provided) and injects the
corresponding <firmwarerelease> or <firmwarebeta> entries into
``releases.xml`` for each board it finds.

When ``--promote-beta`` is provided, the script moves ``beta/<version>/``
to ``<version>/``, removes the corresponding <firmwarebeta> entries, and
adds <firmwarerelease> entries.

Assumptions:
- Board directory names map to XML board names as follows:
    blefriend    -> BLEFRIEND
    blefriend32  -> BLEFRIEND32
    blespifriend -> BLESPIFRIEND
- Each board directory contains exactly one .hex (excluding *_signature.hex)
  and one *_init.dat file to publish.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import shutil
from typing import Optional
import xml.etree.ElementTree as ET


BOARD_NAME_MAP = {
    "blefriend": "BLEFRIEND",
    "blefriend32": "BLEFRIEND32",
    "blespifriend": "BLESPIFRIEND",
}

BASE_URL = (
    "https://github.com/adafruit/Adafruit_BluefruitLE_Firmware/raw/master"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add a firmware entry")
    parser.add_argument("version", help="Version string, e.g. 0.9.0")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--beta",
        action="store_true",
        help="Insert as <firmwarebeta> from beta/<version>/",
    )
    mode.add_argument(
        "--promote-beta",
        action="store_true",
        help="Move beta/<version>/ to <version>/ and promote to <firmwarerelease>",
    )
    return parser.parse_args()


def load_tree(path: Path) -> ET.ElementTree:
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    try:
        return ET.parse(path, parser=parser)
    except FileNotFoundError:
        sys.exit(f"releases.xml not found at {path}")


def indent_fallback(elem: ET.Element, level: int = 0) -> None:
    """Basic pretty-printer for Python versions without ET.indent."""

    spaces = "  " * level
    children = list(elem)
    if children:
        if not elem.text or not elem.text.strip():
            elem.text = "\n" + spaces + "  "
        for child in children:
            indent_fallback(child, level + 1)
        if not children[-1].tail or not children[-1].tail.strip():
            children[-1].tail = "\n" + spaces
    else:
        if elem.text is None or not elem.text.strip():
            elem.text = ""
    if level and (elem.tail is None or not elem.tail.strip()):
        elem.tail = "\n" + "  " * (level - 1)
    elif level == 0 and elem.tail is None:
        elem.tail = "\n"


def find_board_element(root: ET.Element, board_name: str) -> ET.Element:
    for board in root.findall(".//board"):
        if board.get("name") == board_name:
            return board
    sys.exit(f"Board '{board_name}' not present in releases.xml")


def get_min_bootloader(board_elem: ET.Element) -> str:
    # Prefer bootloaderrelease version, fall back to first firmware entry.
    boot = board_elem.find("bootloader/bootloaderrelease")
    if boot is not None and boot.get("version"):
        return boot.get("version")  # type: ignore[return-value]

    firmware = board_elem.find("firmware")
    if firmware is not None:
        for entry in firmware:
            if entry.tag in {"firmwarerelease", "firmwarebeta"}:
                if entry.get("minbootloader"):
                    return entry.get("minbootloader")  # type: ignore[return-value]

    return "0.0"


def pick_single_file(pattern: str, directory: Path, exclude_signature: bool = False) -> Path:
    matches = [p for p in directory.glob(pattern) if not (
        exclude_signature and "signature" in p.name.lower()
    )]
    if len(matches) != 1:
        sys.exit(
            f"Expected exactly one file matching '{pattern}' in {directory}, "
            f"found {len(matches)}"
        )
    return matches[0]


def build_entry(tag: str, version: str, board_dir: Path, min_boot: str, beta: bool) -> ET.Element:
    hex_path = pick_single_file("*.hex", board_dir, exclude_signature=True)
    init_path = pick_single_file("*_init.dat", board_dir)

    prefix = f"beta/{version}" if beta else version
    hex_url = f"{BASE_URL}/{prefix}/{board_dir.name}/{hex_path.name}"
    init_url = f"{BASE_URL}/{prefix}/{board_dir.name}/{init_path.name}"

    return ET.Element(
        tag,
        {
            "version": version,
            "hexfile": hex_url,
            "initfile": init_url,
            "minbootloader": min_boot,
        },
    )


def insert_entry(board_elem: ET.Element, entry: ET.Element) -> None:
    firmware = board_elem.find("firmware")
    if firmware is None:
        sys.exit(f"Board '{board_elem.get('name')}' lacks <firmware> section")

    # Avoid duplicates
    existing = [
        e for e in firmware
        if e.tag == entry.tag and e.get("version") == entry.get("version")
    ]
    if existing:
        print(
            f"Skipping {board_elem.get('name')} ({entry.get('version')} already present)",
            file=sys.stderr,
        )
        return

    firmware.insert(0, entry)


def remove_beta_entries(board_elem: ET.Element, version: str) -> Optional[str]:
    firmware = board_elem.find("firmware")
    if firmware is None:
        sys.exit(f"Board '{board_elem.get('name')}' lacks <firmware> section")

    min_boot = None
    for entry in list(firmware):
        if entry.tag == "firmwarebeta" and entry.get("version") == version:
            if min_boot is None and entry.get("minbootloader"):
                min_boot = entry.get("minbootloader")
            firmware.remove(entry)
    return min_boot


def main() -> None:
    args = parse_args()

    if args.promote_beta:
        source_dir = Path("beta") / args.version
        target_dir = Path(args.version)
        if not source_dir.is_dir():
            sys.exit(f"Firmware directory '{source_dir}' not found")
        if target_dir.exists():
            sys.exit(
                f"Target firmware directory '{target_dir}' already exists; "
                "refusing to overwrite"
            )
        scan_dir = source_dir
    else:
        scan_dir = Path("beta") / args.version if args.beta else Path(args.version)
        if not scan_dir.is_dir():
            sys.exit(f"Firmware directory '{scan_dir}' not found")

    tree = load_tree(Path("releases.xml"))
    root = tree.getroot()

    for board_dir in sorted([p for p in scan_dir.iterdir() if p.is_dir()]):
        board_name = BOARD_NAME_MAP.get(board_dir.name)
        if board_name is None:
            print(f"Unknown board dir '{board_dir.name}', skipping", file=sys.stderr)
            continue

        board_elem = find_board_element(root, board_name)
        min_boot = get_min_bootloader(board_elem)
        if args.promote_beta:
            removed_min_boot = remove_beta_entries(board_elem, args.version)
            if removed_min_boot:
                min_boot = removed_min_boot
            else:
                print(
                    f"Warning: no firmwarebeta {args.version} entry for "
                    f"{board_elem.get('name')}",
                    file=sys.stderr,
                )
        tag = "firmwarebeta" if args.beta else "firmwarerelease"

        entry = build_entry(tag, args.version, board_dir, min_boot, args.beta)
        insert_entry(board_elem, entry)

    if args.promote_beta:
        shutil.move(str(source_dir), str(target_dir))

    # Pretty-print while keeping comments. ET.indent is available in Python 3.9+.
    try:  # type: ignore[attr-defined]
        ET.indent(tree, space="  ")
    except AttributeError:
        indent_fallback(root)

    output = ET.tostring(root, encoding="unicode")
    Path("releases.xml").write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

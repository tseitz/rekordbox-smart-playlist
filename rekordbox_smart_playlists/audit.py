"""Offline resolver + audit for playlist-data JSON configs.

Mirrors PlaylistManager's resolution semantics (base injection, folder links,
mainConditions accumulation) WITHOUT touching the Rekordbox database, so playlist
structure, leaf counts, and broken links can be verified in isolation.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class Leaf:
    """A resolved smart playlist (leaf node)."""

    path: Tuple[str, ...]          # folder chain from root context to this leaf's parent
    name: str
    conditions: frozenset          # ANDed MyTag CONTAINS conditions
    negatives: frozenset           # NOT-CONTAINS conditions


@dataclass
class AuditResult:
    leaves: List[Leaf] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def _load(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_base(category: dict, base_dir: Path, errors: List[str]) -> List[dict]:
    base_ref = category.get("base")
    if not base_ref:
        return []
    base_path = base_dir / base_ref
    if not base_path.exists():
        errors.append(f"Missing base file: {base_ref}")
        return []
    data = _load(base_path).get("data", {})
    return list(data.get("playlists", []))


def _process_category(
    category: dict,
    base_dir: Path,
    inherited_main: frozenset,
    inherited_neg: frozenset,
    folder_path: Tuple[str, ...],
    out: AuditResult,
) -> None:
    main = inherited_main | set(category.get("mainConditions", []))
    neg = inherited_neg | set(category.get("negativeConditions", []))
    playlists = _resolve_base(category, base_dir, out.errors) + list(category.get("playlists", []))

    for pl in playlists:
        if pl.get("playlistType") == "folder":
            name = pl.get("name", "")
            link = pl.get("link")
            here = "/".join(folder_path)
            if not link:
                out.errors.append(f"Folder '{name}' missing link (in {here})")
                continue
            link_path = base_dir / link
            if not link_path.exists():
                out.errors.append(f"Broken link: {link} (in {here}/{name})")
                continue
            child_path = folder_path + (name,)
            linked = _load(link_path).get("data", [])
            categories = linked if isinstance(linked, list) else [linked]
            for sub in categories:
                _process_category(sub, base_dir, main, neg, child_path, out)
        else:
            conditions = main | set(pl.get("contains", []))
            negatives = neg | set(pl.get("doesNotContain", []))
            out.leaves.append(
                Leaf(folder_path, pl.get("name", ""), frozenset(conditions), frozenset(negatives))
            )


def resolve_context(path: Path, base_dir: Path) -> AuditResult:
    """Resolve a single top-level context file into its leaf playlists."""
    out = AuditResult()
    data = _load(path).get("data", [])
    categories = data if isinstance(data, list) else [data]
    for cat in categories:
        parent = cat.get("parent", "")
        _process_category(cat, base_dir, frozenset(), frozenset(), (parent,), out)
    return out


# --- CLI -------------------------------------------------------------------

def _context_files(directory: Path) -> List[Path]:
    return sorted(
        f for f in directory.glob("*.json")
        if not f.name.startswith(".") and not f.name.startswith("_")
    )


def _signature(leaves: List[Leaf]) -> Tuple:
    """Structural fingerprint ignoring the root context name (path[0])."""
    return tuple(sorted((leaf.path[1:], leaf.name) for leaf in leaves))


def main(argv: List[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    directory = Path(argv[0]) if argv else Path("playlist-data")

    total = 0
    errors: List[str] = []
    sigs = {}
    for f in _context_files(directory):
        res = resolve_context(f, directory)
        total += len(res.leaves)
        errors.extend(res.errors)
        sigs[f.stem] = _signature(res.leaves)
        print(f"{f.name:28s} {len(res.leaves):5d} leaves")

    print("-" * 36)
    print(f"{'TOTAL':28s} {total:5d} leaves")

    uniform = [
        "daytime", "nighttime", "late-night", "sunrise", "chillin", "afterparty",
        "morningtime-vibes", "pool-party", "crispy-speakers", "missy", "b2b",
        "silent-disco",
    ]
    present = {name: sigs[name] for name in uniform if name in sigs}
    distinct = set(present.values())
    if len(present) == len(uniform) and len(distinct) == 1:
        print(f"Uniformity: OK ({len(uniform)} contexts identical)")
    elif present:
        print(f"Uniformity: MISMATCH ({len(distinct)} distinct shapes among "
              f"{len(present)}/{len(uniform)} present)")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print("  -", e)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json
from pathlib import Path

from rekordbox_smart_playlists.audit import resolve_context, Leaf


def _write(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj), encoding="utf-8")


def test_top_level_conditions_and_base(tmp_path: Path):
    # base file (dict-style) with two genre playlists
    _write(tmp_path / "_genres.json", {
        "data": {"playlists": [
            {"name": "Dub", "operator": 1, "contains": ["Dub"]},
            {"name": "House", "operator": 1, "contains": ["House"]},
        ]}
    })
    # a Genre lens that injects the base
    _write(tmp_path / "lens-genre.json", {
        "data": [{"mainConditions": [], "base": "_genres.json", "playlists": []}]
    })
    # context linking to the Genre folder + a direct "All"
    _write(tmp_path / "nighttime.json", {
        "data": [{
            "parent": "Nighttime",
            "mainConditions": ["Nighttime"],
            "negativeConditions": ["Archive"],
            "playlists": [
                {"name": "All", "operator": 1, "contains": []},
                {"name": "Genre", "operator": 1, "playlistType": "folder",
                 "link": "lens-genre.json"},
            ],
        }]
    })

    result = resolve_context(tmp_path / "nighttime.json", tmp_path)

    assert result.errors == []
    by_name = {leaf.name: leaf for leaf in result.leaves}
    # 1 "All" + 2 injected genres
    assert set(by_name) == {"All", "Dub", "House"}
    # "All" lives directly under the context, carries only the context tag
    assert by_name["All"].path == ("Nighttime",)
    assert by_name["All"].conditions == frozenset({"Nighttime"})
    assert by_name["All"].negatives == frozenset({"Archive"})
    # genres live under Nighttime/Genre and AND the context tag
    assert by_name["Dub"].path == ("Nighttime", "Genre")
    assert by_name["Dub"].conditions == frozenset({"Nighttime", "Dub"})


def test_mainconditions_accumulate_across_nested_links(tmp_path: Path):
    _write(tmp_path / "_genres.json", {
        "data": {"playlists": [{"name": "Dub", "operator": 1, "contains": ["Dub"]}]}
    })
    _write(tmp_path / "lens-genre.json", {
        "data": [{"mainConditions": [], "base": "_genres.json", "playlists": []}]
    })
    # caliber sub-tree that adds "My Set" and re-links the Genre lens
    _write(tmp_path / "caliber-my-set.json", {
        "data": [{"mainConditions": ["My Set"], "playlists": [
            {"name": "Genre", "operator": 1, "playlistType": "folder",
             "link": "lens-genre.json"},
        ]}]
    })
    _write(tmp_path / "nighttime.json", {
        "data": [{
            "parent": "Nighttime", "mainConditions": ["Nighttime"],
            "negativeConditions": ["Archive"],
            "playlists": [
                {"name": "My Set", "operator": 1, "playlistType": "folder",
                 "link": "caliber-my-set.json"},
            ],
        }]
    })

    result = resolve_context(tmp_path / "nighttime.json", tmp_path)

    assert result.errors == []
    assert len(result.leaves) == 1
    dub = result.leaves[0]
    assert dub.name == "Dub"
    assert dub.path == ("Nighttime", "My Set", "Genre")
    assert dub.conditions == frozenset({"Nighttime", "My Set", "Dub"})


def test_broken_link_is_reported_not_raised(tmp_path: Path):
    _write(tmp_path / "nighttime.json", {
        "data": [{
            "parent": "Nighttime", "mainConditions": ["Nighttime"],
            "playlists": [
                {"name": "Genre", "operator": 1, "playlistType": "folder",
                 "link": "does-not-exist.json"},
            ],
        }]
    })

    result = resolve_context(tmp_path / "nighttime.json", tmp_path)

    assert result.leaves == []
    assert len(result.errors) == 1
    assert "does-not-exist.json" in result.errors[0]

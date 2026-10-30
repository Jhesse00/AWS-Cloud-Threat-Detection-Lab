"""Tests for analyze.py.

Verify that the statistics recomputed from the raw CSV data match the
figures recorded in data/project_stats.json, and that the helper
functions behave on small synthetic inputs.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analyze  # noqa: E402


def load_recorded_stats():
    with open(ROOT / "data" / "project_stats.json", encoding="utf-8") as handle:
        return json.load(handle)


def test_numeric_stats_match_recorded_file():
    computed = analyze.compute_stats()
    recorded = load_recorded_stats()
    for key in (
        "total_events",
        "unique_ips",
        "top_ip",
        "top_attempts",
        "username_attempts",
        "unique_usernames",
    ):
        assert computed[key] == recorded[key], key


def test_attacker_ips_sorted_descending():
    rows = analyze.read_attacker_ips()
    attempts = [count for _, count in rows]
    assert attempts == sorted(attempts, reverse=True)


def test_top_pair_text_is_well_formed():
    stats = analyze.compute_stats()
    # The busiest IP has several usernames tied on attempts, so the exact
    # username can vary; assert the structure instead of a fixed value.
    assert "\u2192" in stats["top_pair_text"]
    assert "attempts)" in stats["top_pair_text"]
    assert stats["top_ip"] in stats["top_pair_text"]


def test_top_usernames_limit_and_order():
    ranked = analyze.top_usernames(limit=3)
    assert len(ranked) == 3
    counts = [count for _, count in ranked]
    assert counts == sorted(counts, reverse=True)


def test_compute_stats_on_synthetic_data(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "attacker_ips.csv").write_text(
        "src_ip,attempts\n10.0.0.1,30\n10.0.0.2,10\n", encoding="utf-8"
    )
    (data_dir / "ssh_usernames_by_ip.csv").write_text(
        "src_ip,username,attempts\n10.0.0.1,root,20\n10.0.0.1,admin,10\n10.0.0.2,root,10\n",
        encoding="utf-8",
    )
    stats = analyze.compute_stats(data_dir)
    assert stats["total_events"] == 40
    assert stats["unique_ips"] == 2
    assert stats["top_ip"] == "10.0.0.1"
    assert stats["top_attempts"] == 30
    assert stats["username_attempts"] == 40
    assert stats["unique_usernames"] == 2  # root, admin
    assert stats["top_pair_text"] == "10.0.0.1 \u2192 root (20 attempts)"

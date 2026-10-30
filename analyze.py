#!/usr/bin/env python3
"""Recompute the lab's SSH honeypot statistics from the raw CSV data.

Reads the CSV files in data/ and reproduces the figures recorded in
data/project_stats.json: total failed-login events, unique source IPs,
the top attacking IP, and username-guessing totals. Useful for verifying
the published numbers and for re-running the analysis on fresh captures.

Standard library only; no external dependencies.
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def read_attacker_ips(data_dir=DATA_DIR):
    """Return a list of (src_ip, attempts) sorted by attempts descending."""
    path = data_dir / "attacker_ips.csv"
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append((row["src_ip"], int(row["attempts"])))
    rows.sort(key=lambda item: item[1], reverse=True)
    return rows


def read_username_attempts(data_dir=DATA_DIR):
    """Return a list of (src_ip, username, attempts) from the username CSV."""
    path = data_dir / "ssh_usernames_by_ip.csv"
    rows = []
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append((row["src_ip"], row["username"], int(row["attempts"])))
    return rows


def compute_stats(data_dir=DATA_DIR):
    """Compute the headline statistics from the raw CSV data."""
    attacker_ips = read_attacker_ips(data_dir)
    username_rows = read_username_attempts(data_dir)

    total_events = sum(attempts for _, attempts in attacker_ips)
    unique_ips = len(attacker_ips)
    top_ip, top_attempts = attacker_ips[0] if attacker_ips else ("", 0)

    username_attempts = sum(attempts for _, _, attempts in username_rows)
    unique_usernames = len({username for _, username, _ in username_rows})

    # Several usernames can tie on attempts for the busiest IP; sort by
    # (attempts desc, username) so the chosen pair is deterministic.
    top_pair = (
        sorted(username_rows, key=lambda row: (-row[2], row[1]))[0]
        if username_rows
        else ("", "", 0)
    )
    top_pair_text = f"{top_pair[0]} \u2192 {top_pair[1]} ({top_pair[2]} attempts)"

    return {
        "total_events": total_events,
        "unique_ips": unique_ips,
        "top_ip": top_ip,
        "top_attempts": top_attempts,
        "username_attempts": username_attempts,
        "unique_usernames": unique_usernames,
        "top_pair_text": top_pair_text,
    }


def top_usernames(data_dir=DATA_DIR, limit=10):
    """Return the most-guessed usernames across all source IPs."""
    totals = defaultdict(int)
    for _, username, attempts in read_username_attempts(data_dir):
        totals[username] += attempts
    ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    return ranked[:limit]


def format_summary(stats):
    lines = [
        "SSH Honeypot Analysis",
        "=" * 30,
        f"Total failed SSH events : {stats['total_events']:,}",
        f"Unique source IPs       : {stats['unique_ips']}",
        f"Top attacker IP         : {stats['top_ip']} ({stats['top_attempts']} attempts)",
        f"Username attempts        : {stats['username_attempts']}",
        f"Unique usernames guessed: {stats['unique_usernames']}",
        f"Top IP/username pair    : {stats['top_pair_text']}",
    ]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Recompute SSH honeypot statistics.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help="Directory containing the lab CSV files (default: ./data).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the computed statistics as JSON instead of a summary table.",
    )
    parser.add_argument(
        "--top-usernames",
        type=int,
        metavar="N",
        help="Also print the top N most-guessed usernames.",
    )
    args = parser.parse_args(argv)

    stats = compute_stats(args.data_dir)
    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(format_summary(stats))

    if args.top_usernames:
        print("\nTop usernames:")
        for username, attempts in top_usernames(args.data_dir, args.top_usernames):
            print(f"  {username:<20} {attempts}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

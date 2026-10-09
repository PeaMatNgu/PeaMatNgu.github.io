#!/usr/bin/env python3
"""Synchronize Lighth0use's public CTFtime results into Jekyll data."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


TEAM_ID = 410831
FIRST_YEAR = 2026
CUTOFF_EVENT_ID = 3133  # UTCTF 2026
API_ROOT = "https://ctftime.org/api/v1"
OUTPUT = Path(__file__).resolve().parents[1] / "_data" / "ctftime.json"
USER_AGENT = "PeaMatNgu-achievements-sync/1.0 (+https://peamatngu.github.io)"


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def clean_points(value: str) -> str:
    return value.rstrip("0").rstrip(".") if "." in value else value


def load_existing() -> dict:
    if not OUTPUT.exists():
        return {}
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def main() -> None:
    current_year = datetime.now(timezone.utc).year
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--years",
        nargs="*",
        type=int,
        default=list(range(FIRST_YEAR, current_year + 1)),
        help="Years to synchronize (defaults to every year since 2025).",
    )
    args = parser.parse_args()

    team_payload = fetch_json(f"{API_ROOT}/teams/{TEAM_ID}/")
    events = []

    for year in sorted(set(args.years), reverse=True):
        yearly_results = fetch_json(f"{API_ROOT}/results/{year}/")
        for event_id, event in yearly_results.items():
            team_score = next(
                (
                    score
                    for score in event.get("scores", [])
                    if int(score.get("team_id", -1)) == TEAM_ID
                ),
                None,
            )
            if not team_score:
                continue

            timestamp = int(float(event.get("time", 0)))
            events.append(
                {
                    "id": int(event_id),
                    "title": event.get("title", f"CTF event {event_id}"),
                    "date": datetime.fromtimestamp(timestamp, timezone.utc).date().isoformat(),
                    "year": year,
                    "place": int(team_score["place"]),
                    "points": clean_points(str(team_score["points"])),
                    "url": f"https://ctftime.org/event/{event_id}",
                    "timestamp": timestamp,
                }
            )

    cutoff_event = next(
        (event for event in events if event["id"] == CUTOFF_EVENT_ID), None
    )
    if cutoff_event is None:
        raise RuntimeError("UTCTF 2026 was not found in the CTFtime results")
    events = [
        event for event in events if event["timestamp"] >= cutoff_event["timestamp"]
    ]
    events.sort(key=lambda item: (item["timestamp"], item["id"]), reverse=True)
    for event in events:
        event.pop("timestamp", None)

    rating_by_year = team_payload.get("rating", {})
    rating_year = str(current_year)
    if not rating_by_year.get(rating_year, {}).get("rating_place"):
        candidates = [
            year
            for year, values in rating_by_year.items()
            if values.get("rating_place")
        ]
        rating_year = max(candidates, key=int) if candidates else str(current_year)
    rating = rating_by_year.get(rating_year, {})

    payload = {
        "team": {
            "id": TEAM_ID,
            "name": team_payload.get("name", "Lighth0use"),
            "country": team_payload.get("country", "VN"),
            "url": f"https://ctftime.org/team/{TEAM_ID}",
            "rating_year": int(rating_year),
            "rating_place": rating.get("rating_place"),
            "country_place": rating.get("country_place"),
            "rating_points": round(float(rating.get("rating_points", 0)), 3),
            "event_count": len(events),
            "best_place": min((event["place"] for event in events), default=None),
        },
        "years": sorted(set(args.years), reverse=True),
        "events": events,
    }

    existing = load_existing()
    comparable_existing = {key: value for key, value in existing.items() if key != "updated_at"}
    if comparable_existing == payload and existing.get("updated_at"):
        payload["updated_at"] = existing["updated_at"]
    else:
        payload["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(events)} CTFtime results")


if __name__ == "__main__":
    main()

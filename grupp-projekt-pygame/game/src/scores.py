import json
import os
from datetime import datetime

# game/src -> game/data/scores.json
SCORES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "scores.json")


def _load():
    if not os.path.exists(SCORES_PATH):
        return {"runs": []}
    try:
        with open(SCORES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "runs" not in data or not isinstance(data["runs"], list):
            return {"runs": []}
        return data
    except Exception:
        return {"runs": []}


def _save(data):
    os.makedirs(os.path.dirname(SCORES_PATH), exist_ok=True)
    tmp_path = SCORES_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, SCORES_PATH)


def add_score(score: int):
    """Spara ett avslutat run-score."""
    score = int(score)
    data = _load()
    data["runs"].append(
        {
            "score": score,
            "ts": datetime.now().isoformat(timespec="seconds"),
        }
    )
    _save(data)


def get_last_scores(n: int = 3):
    """Senaste n scores (nyast först)."""
    data = _load()
    runs = sorted(data["runs"], key=lambda r: r.get("ts", ""), reverse=True)
    return [int(r.get("score", 0)) for r in runs[:n]]


def get_high_score():
    """Högsta score någonsin."""
    data = _load()
    if not data["runs"]:
        return 0
    return max(int(r.get("score", 0)) for r in data["runs"])

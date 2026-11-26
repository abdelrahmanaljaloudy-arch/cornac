"""Lab 7: a small application-facing recommendation function built on Cornac.

The function answers the question an application asks: "which k items should
we show to this user?". It trains Cornac's MostPop model on a tiny, fixed
interaction log and asks the model for top-k recommendations.

Run it as a script to print a run report (used by the GitHub Actions job):

    python -m lab7.recommend_app
"""

import json
import os
import subprocess
import sys

import cornac
from cornac.data import Dataset
from cornac.models import MostPop

# Tiny implicit-feedback log: (user, item, rating).
# Item popularity is i1=6, i2=5, i3=4, i4=3, i5=2, i6=1, so the ranking has no ties.
# u1 has already consumed i1, i2 and i3; u6 has only consumed i1.
INTERACTIONS = [
    ("u1", "i1", 1.0), ("u1", "i2", 1.0), ("u1", "i3", 1.0),
    ("u2", "i1", 1.0), ("u2", "i2", 1.0), ("u2", "i3", 1.0),
    ("u2", "i4", 1.0), ("u2", "i5", 1.0), ("u2", "i6", 1.0),
    ("u3", "i1", 1.0), ("u3", "i2", 1.0), ("u3", "i3", 1.0),
    ("u3", "i4", 1.0), ("u3", "i5", 1.0),
    ("u4", "i1", 1.0), ("u4", "i2", 1.0), ("u4", "i3", 1.0), ("u4", "i4", 1.0),
    ("u5", "i1", 1.0), ("u5", "i2", 1.0),
    ("u6", "i1", 1.0),
]


def build_model(interactions=INTERACTIONS, seed=123):
    """Build a Cornac training set from the log and fit a MostPop model on it."""
    train_set = Dataset.from_uir(interactions, seed=seed)
    model = MostPop().fit(train_set)
    return model, train_set


def recommend_for_user(model, train_set, user_id, k=3):
    """Return the top-k item IDs to show to `user_id`, most popular first.

    Items the user has already consumed in `train_set` are not recommended
    again, so every slot shows the user something new.
    """
    return model.recommend(user_id, k=k, remove_seen=True, train_set=train_set)


def item_popularity(model):
    """Map each item ID to its popularity count learned by the model."""
    return {item_id: int(model.item_pop[idx]) for idx, item_id in enumerate(model.item_ids)}


def _git_sha():
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        return sha
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def main():
    model, train_set = build_model()
    report = {
        "commit_sha": _git_sha(),
        "python": sys.version.split()[0],
        "cornac_version": cornac.__version__,
        "cornac_loaded_from": os.path.dirname(cornac.__file__),
        "model": model.name,
        "item_popularity": item_popularity(model),
        "recommendations_k3": {
            user: recommend_for_user(model, train_set, user, k=3) for user in ("u1", "u6")
        },
    }
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()

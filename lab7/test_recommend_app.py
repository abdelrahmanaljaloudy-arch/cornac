"""Lab 7 behavioural checks for lab7.recommend_app.recommend_for_user."""

import os

import cornac
import pytest

from lab7.recommend_app import build_model, item_popularity, recommend_for_user

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def fitted():
    return build_model()


# --- Deployment evidence -----------------------------------------------------

def test_cornac_is_loaded_from_this_fork_checkout():
    # The code under test must be the fork's source, not a package from PyPI.
    assert os.path.abspath(cornac.__file__).startswith(REPO_ROOT)


# --- Behaviour that this version is expected to show -------------------------

def test_u1_top3(fitted):
    model, train_set = fitted
    # Baseline: the plain popularity ranking, including items u1 already consumed.
    assert recommend_for_user(model, train_set, "u1", k=3) == ["i1", "i2", "i3"]


def test_u6_top3(fitted):
    model, train_set = fitted
    assert recommend_for_user(model, train_set, "u6", k=3) == ["i1", "i2", "i3"]


# --- Invariants that must hold before and after any change -------------------

def test_learned_popularity_matches_the_log(fitted):
    model, _ = fitted
    assert item_popularity(model) == {"i1": 6, "i2": 5, "i3": 4, "i4": 3, "i5": 2, "i6": 1}


@pytest.mark.parametrize("user_id", ["u1", "u6"])
def test_returns_k_distinct_known_items_in_popularity_order(fitted, user_id):
    model, train_set = fitted
    recs = recommend_for_user(model, train_set, user_id, k=3)
    pop = item_popularity(model)
    assert len(recs) == 3
    assert len(set(recs)) == 3
    assert all(item in pop for item in recs)
    assert [pop[i] for i in recs] == sorted((pop[i] for i in recs), reverse=True)


def test_unknown_user_is_rejected(fitted):
    model, train_set = fitted
    with pytest.raises(ValueError):
        recommend_for_user(model, train_set, "nobody", k=3)

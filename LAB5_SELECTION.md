# Lab #5 - System Selection and Reproducibility Record

## People and collaboration

- Working mode: [x] Solo  [ ] Pair
- Student A (name / GitHub): Abdelrahman Aljaloudy / [abdelrahmanaljaloudy-arch](https://github.com/abdelrahmanaljaloudy-arch)
- Student B (name / GitHub; if pair): Not applicable
- Fork owner: abdelrahmanaljaloudy-arch
- Collaborator invitation accepted? Not applicable (solo)
- Individual work differentiation: `QUALITY_INVESTIGATION.md` will be created in this branch from Lab #6 onwards.

## First shortlist - catalogue only

| Candidate | Catalogue-based reason | One concern to investigate |
|---|---|---|
| **A. Cornac** (#1, Core) | Recommender framework with several algorithms; MovieLens ratings and held-out recommendations as ground truth; tests contain functional oracles; Apache-2.0 | Native (Cython) extensions: will it install and run on Windows? |
| **B. Surprise** (#4, Core) | Simple explicit-rating prediction; built-in MovieLens; cross-validation with MAE/RMSE; unit-test assertions; BSD-3-Clause | "Maintenance mode": is there enough recent history for later labs? |
| **C. LensKit** (#2, Core) | Research toolkit for recommendation pipelines and ranking evaluation; MIT | "Recent source builds require Rust; compatible Python needed" |

Recommender systems were preferred over computer vision because they run on a CPU-only laptop and MovieLens gives real user ratings as ground truth.

## Evidence-based candidate assessment

Use Y = Yes; P = Partial; N = No; U = Unknown. **Attach links or file paths for factual claims.**

| Criterion | Candidate A: Cornac + evidence | Candidate B: Surprise + evidence | Candidate C: LensKit + evidence | Candidate D + evidence (pairs) |
|---|---|---|---|---|
| C1 Public repository / licence / data rights | **Y**: public, [Apache-2.0](https://github.com/PreferredAI/cornac/blob/master/LICENSE), fork created. Datasets are downloaded at runtime from their owners (e.g. GroupLens) with their own terms | **Y**: public, [BSD-3-Clause](https://github.com/NicolasHug/Surprise/blob/master/LICENSE.md); MovieLens downloaded at runtime | **Y**: public, [MIT](https://github.com/lenskit/lkpy/blob/main/LICENSE.md); `data/` sets have separate terms | - |
| C2 Pinned revision / runtime | **Y**: tag [`v3.1.0`](https://github.com/PreferredAI/cornac/releases/tag/v3.1.0) (30 Oct 2026); requires Python ≥ 3.10; Windows wheels for 3.10–3.14 on [PyPI](https://pypi.org/project/cornac/3.1.0/) | **Y**: tag `v1.1.5`; Windows wheels for Python 3.10–3.14 on [PyPI](https://pypi.org/project/scikit-surprise/) | **P**: tag `v2026.4.0`; requires Python ≥ 3.12.5; source builds need Rust ([README](https://github.com/lenskit/lkpy#readme)) | - |
| C3 Nontrivial source + refactoring | **Y**: ~55k lines Python/Cython, 69 model packages in [`cornac/models`](https://github.com/PreferredAI/cornac/tree/master/cornac/models); 248 `.py` + 24 `.pyx` files | **P**: small codebase (~5k lines) in [`surprise/`](https://github.com/NicolasHug/Surprise/tree/master/surprise) | **Y**: ~36k lines Python + Rust in [`src/`](https://github.com/lenskit/lkpy/tree/main/src) | - |
| C4 Tests and expected-output **oracle** | **Y**: 48 test files in [`tests/cornac`](https://github.com/PreferredAI/cornac/tree/master/tests/cornac) (data, datasets, eval_methods, experiment, metrics, models, serving, utils); e.g. [`test_rating.py`](https://github.com/PreferredAI/cornac/blob/master/tests/cornac/metrics/test_rating.py) asserts metric values on known inputs | **Y**: 18 test files, e.g. [`tests/test_accuracy.py`](https://github.com/NicolasHug/Surprise/blob/master/tests/test_accuracy.py) (`test_mae`, `test_rmse`) | **Y**: 164 test files, e.g. [`tests/eval/test_rank_dcg.py`](https://github.com/lenskit/lkpy/tree/main/tests/eval) | - |
| C5 AI/recommender **ground-truth** source and terms | **Y**: built-in loaders in [`cornac/datasets`](https://github.com/PreferredAI/cornac/tree/master/cornac/datasets) (MovieLens, Netflix, Amazon, FilmTrust, Epinions, CiteULike…); MovieLens 100K from GroupLens, research use, no redistribution | **Y**: built-in MovieLens 100K/1M (same GroupLens terms) | **P**: MovieLens loaders, but data must be downloaded and prepared by the user | - |
| C6 Evaluation procedure and metrics | **Y**: [`eval_methods`](https://github.com/PreferredAI/cornac/tree/master/cornac/eval_methods) (RatioSplit, CrossValidation, StratifiedSplit…); [`metrics`](https://github.com/PreferredAI/cornac/tree/master/cornac/metrics): MAE, MSE, RMSE, Precision, Recall, NDCG, AUC, MAP, MRR, HitRatio, F-measure | **P**: cross-validation with mainly MAE/RMSE/FCP | **Y**: ranking and prediction metrics, evaluation pipelines | - |
| C7 Upstream GitHub history | **Y**: 1,450 commits; 72 commits and 19 authors since 2025 on `master`; PRs closed on the day of the lab ([commits](https://github.com/PreferredAI/cornac/commits/master), [PRs](https://github.com/PreferredAI/cornac/pulls?q=is%3Apr+is%3Aclosed)) | **N**: 0 commits in 2025, 1 author; 2 maintenance commits in 2026 | **Y**: very active, 3,700+ commits since 2025 | - |
| C8 CI/DevOps possibility | **Y**: 4 workflows in [`.github/workflows`](https://github.com/PreferredAI/cornac/tree/master/.github/workflows); `python-package.yml` runs flake8 + pytest-cov on 3 OS × Python 3.10–3.14 | **Y**: 6 workflows (wheels, docs, lint, benchmarks) | **Y**: 7 workflows (tests, docs, eval, package) | - |
| C9 Laptop setup feasibility | **Y** (verified): `pip install cornac==3.1.0` worked on Windows 11, CPU only. Blocker found and solved: Windows Smart App Control blocked the compiled extension (see below) | **U**: not installed; prebuilt wheels exist | **P**: needs Python ≥ 3.12.5 and possibly Rust | - |
| C10 Continuation to Labs 6-9 / credible question | **Y**: static analysis on Python code, existing CI matrix, MovieLens ground truth, long history; credible question: *Are the default recommendations accurate and diverse, or biased toward popular items?* | **P**: weak for Lab #9 (almost no recent history) | **Y**, but higher setup risk | - |

### Ground-truth verification notes

- **Candidate A (Cornac):** functional test assertion: [`tests/cornac/metrics/test_rating.py`](https://github.com/PreferredAI/cornac/blob/master/tests/cornac/metrics/test_rating.py) and [`test_ranking.py`](https://github.com/PreferredAI/cornac/blob/master/tests/cornac/metrics/test_ranking.py); rating source: MovieLens 100K user ratings (1–5 stars) via `cornac.datasets.movielens.load_feedback()` from [GroupLens](https://grouplens.org/datasets/movielens/100k/); train/test protocol: `RatioSplit(test_size=0.2, rating_threshold=4.0, seed=123)` ([README example](https://github.com/PreferredAI/cornac#getting-started-your-first-cornac-experiment)); data terms: GroupLens licence, research use, no redistribution without permission → dataset is **not** committed to the fork.
- **Candidate B (Surprise):** functional test assertion: [`tests/test_accuracy.py`](https://github.com/NicolasHug/Surprise/blob/master/tests/test_accuracy.py); rating source: built-in MovieLens 100K (`Dataset.load_builtin('ml-100k')`); protocol: k-fold `cross_validate`; data terms: same GroupLens terms.
- **Candidate C (LensKit):** functional test assertion: [`tests/eval/`](https://github.com/lenskit/lkpy/tree/main/tests/eval) (e.g. `test_rank_dcg.py`); rating source: MovieLens via `load_movielens` (manual download); protocol: user-based holdout splits in `lenskit.splitting`; data terms: same GroupLens terms.
- **Important distinction:** passing unit tests (functional oracle) shows the code computes values correctly on small inputs; it does **not** show that recommendations are good. That needs the MovieLens ground truth and a held-out test set.

## Decision

- **Final SUT and short description:** **Cornac v3.1.0**, a Python/Cython framework for building and evaluating recommender systems with many algorithms, datasets and metrics.
- **Why it is better suited than rejected alternatives:** it is the only candidate with **Y** on every criterion: it installs and runs on my laptop, reproduces the README results exactly, and combines tests, CI, ground-truth data, rich metrics and an active history.
- **Rejected alternatives and reasons:** **Surprise**: easy, but no development in 2025 (weak for Lab #9) and fewer metrics. **LensKit**: strong and very active, but needs Python ≥ 3.12.5 and Rust, so a higher setup risk → kept as backup.
- **Backup SUT and trigger for switching:** **LensKit**. Switch if Cornac cannot be built from source for the refactoring work in Lab #6, or if its CI cannot run on the fork in Lab #7.
- **Biggest unresolved risk / mitigation:** an editable/source install (`pip install -e .`) compiles Cython and may need Microsoft C++ Build Tools. Mitigation: install the Build Tools or use WSL (Ubuntu) before Lab #6.

## Repository provenance and pair access

- Original upstream repo URL: https://github.com/PreferredAI/cornac
- Selected original tag (if any): `v3.1.0`, commit `8e81b0bf4e2cb995b9c35dfa3b5dac4a4fa67b57`
- Fork URL: https://github.com/abdelrahmanaljaloudy-arch/cornac
- Working branch: [`semester-investigation`](https://github.com/abdelrahmanaljaloudy-arch/cornac/tree/semester-investigation) (created from `v3.1.0`)
- Git and runtime versions: Git 2.54.0.windows.1; Python 3.13 (venv); cornac 3.1.0; Windows 11
- Applicable code licence (link + note): [Apache-2.0](https://github.com/PreferredAI/cornac/blob/master/LICENSE): permits use, modification and redistribution with attribution
- External dataset licence/limits: MovieLens ([GroupLens terms](https://files.grouplens.org/datasets/movielens/ml-100k-README.txt)): research use, citation required, no redistribution → cached locally in `~/.cornac`, never committed
- Partner collaborator invitation accepted? (pair only): Not applicable

## Actual execution - not just installation

| Check | Official documentation link | Exact local command / path + input | Observed output / short log + evidence link | Status |
|---|---|---|---|---|
| Install/build source-aware baseline | [README → Installation](https://github.com/PreferredAI/cornac#installation) | `py -3.13 -m venv .venv` → `python -m pip install cornac==3.1.0` → `python -c "import cornac; print(cornac.__version__)"` | First import failed: `ImportError: DLL load failed while importing recom_vebpr: An Application Control policy has blocked this file.` (Windows Smart App Control). After turning Smart App Control off: prints `3.1.0`. Editable install (`pip install -e .`) not yet attempted | **Partial** |
| Functionality 1 (real behaviour) | [README → Getting started: your first Cornac experiment](https://github.com/PreferredAI/cornac#getting-started-your-first-cornac-experiment) | `python C:\Lab5\run1_experiment.py`: MovieLens 100K, `RatioSplit(test_size=0.2, rating_threshold=4.0, seed=123)`, models MF, PMF, BPR, metrics MAE, RMSE, AUC, MAP, NDCG@10, Precision@10, Recall@10 | MF: MAE 0.7430, RMSE 0.8998, AUC 0.7445, NDCG@10 0.0761 · PMF: MAE 0.7534, RMSE 0.9138, AUC 0.7744, NDCG@10 0.0969 · BPR: AUC 0.8695, NDCG@10 0.1500, Precision@10 0.1110. All accuracy values **identical to the README**; only times differ. Note: BPR prints MAE 2.0143 / RMSE 2.2267 although the README shows N/A (not meaningful for a ranking model) | **Success** |
| Functionality 2 (different behaviour) | [API reference: `Recommender.recommend`](https://cornac.readthedocs.io/en/stable/api_ref/models.html) | `python C:\Lab5\run2_recommend.py`: BPR trained on all MovieLens 100K (`seed=123`), `recommend(user_id="196", k=10, remove_seen=True)` | `['50', '181', '100', '258', '174', '1', '294', '121', '288', '56']`; user 196 had rated 39 movies, none repeated. Mostly very popular titles (Star Wars, Return of the Jedi, Toy Story, Pulp Fiction…) → possible popularity bias | **Success** |

- **Is the installed code from the local source fork, or only a separately installed wheel/image?** Only the **prebuilt wheel** `cornac==3.1.0` from PyPI. It matches the pinned tag `v3.1.0`, but it is not built from my fork. A source-aware install is needed before I modify code in Lab #6.
- **Blockers and fallback date/action:** (1) Smart App Control blocked compiled `.pyd` files → solved on 12 Nov 2026 by disabling it (alternative: WSL). (2) Source build needs a C++ compiler → install Microsoft C++ Build Tools or use WSL **before Lab #6**; if neither works, switch to the backup (LensKit).

## Future-lab feasibility (Task 5 - LLM-assisted, then verified)

LLM used: Claude (Anthropic), with the prompt from the handout. Each claim was checked against the repository at `v3.1.0`.

| Future lab | Suitable? | Possible investigation / tools | Main concern |
|---|---|---|---|
| #6 - Static analysis / refactoring | **Yes** | Ruff/flake8, Radon or Lizard, pylint on 248 Python files; refactor one complex function and re-run `tests/cornac` | 24 Cython `.pyx` files are not analysed by Python-only tools; changes need a rebuild |
| #7 - DevOps / CI/CD | **Yes** | Existing `python-package.yml` (3 OS × Python 3.10–3.14, flake8 + pytest-cov); enable and extend on the fork | 15 slow matrix jobs; publishing workflows must stay disabled |
| #8 - AI quality | **Yes** | MovieLens 100K ground truth; RMSE/MAE and NDCG/Precision/Recall/AUC; compare models, seeds, splits; popularity bias | BPR outputs rating metrics that are not meaningful; dataset cannot be redistributed |
| #9 - Empirical study | **Yes (with care)** | Git history (1,450 commits, tags, authors) + upstream PRs/issues via GitHub CLI | Activity dropped in 2022 (6 commits) and recovered later; PRs/issues exist only upstream |

**LLM claims found incorrect or unsupported:** (1) it expected `pip install cornac` to work without problems on Windows, but Smart App Control blocked the compiled extension; (2) it suggested running pylint/Radon on "the whole codebase", which ignores the Cython files; (3) "the editable install may need C++ Build Tools" is still an untested assumption.

**Confidence:** high that Cornac can support Labs #6–#9; remaining risks are the source build (Lab #6), CI runtime (Lab #7), dataset terms (Lab #8) and uneven history (Lab #9).

## Approval / action

- Instructor status: Pending
- Changes needed before Lab #6: build Cornac from the fork (`pip install -e .`) so that code changes are actually used; then enable CI on the fork with care (publishing workflows disabled).
- Date of record: 12 November 2026

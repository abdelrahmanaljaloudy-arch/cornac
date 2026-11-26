# Lab #7 — From Code to Operation: Investigation Record

**Team:** Individual — Abdelrahman Aljaloudy  
**Student(s) / GitHub handle(s):** Abdelrahman Aljaloudy — [@abdelrahmanaljaloudy-arch](https://github.com/abdelrahmanaljaloudy-arch)  
**Fork / working branch:** https://github.com/abdelrahmanaljaloudy-arch/cornac/tree/semester-investigation (Lab #7 work on branch `lab7-abdelrahman`, merged by PR)  
**Upstream project and pinned version:** https://github.com/PreferredAI/cornac — tag `v3.1.0`, SHA `8e81b0bf4e2cb995b9c35dfa3b5dac4a4fa67b57` (Lab #5). The fork also contains the Lab #6 `normalize` refactoring (`87027b4`), which does not touch the code used here.

## 1. Stakeholder, goal and selected functionality

**Stakeholder concern:** Sam, the release engineer, needs to trust two things: (1) that our Cornac fork can be built from source and executed in a clean Ubuntu machine, not only on a developer laptop, and (2) that when we change what the recommender shows to a user, our delivery checks make that change visible, so Sam can decide if the new version is acceptable.

**GQM goal:** Analyze **the top-k recommendation path of the Cornac fork (an application-facing function `recommend_for_user` that calls Cornac's `MostPop` model and `Recommender.recommend`)** for the purpose of **evaluation**, with respect to **deployability in a clean environment and detectability of an intended behavior change**, from the viewpoint of **Sam, the release engineer**, in the context of **the `semester-investigation` / `lab7-abdelrahman` branches of my fork, built and executed by GitHub Actions on a GitHub-hosted `ubuntu-24.04` runner**.

| Question | Question in your own words | Evidence / measurement and why it helps |
|---|---|---|
| Q1 | Can the fork's code be built, installed and run on a clean GitHub Ubuntu runner, and can we prove that the code that ran is exactly our commit (not a PyPI package)? | Workflow step results (checkout, build, run, verify); commit SHA printed by the runner vs. the pushed commit; `cornac.__file__` inside the checkout (automated check); build duration; JSON run report. Shows *what* was executed and *where it came from*. |
| Q2 | When we intentionally change the recommendation rule, do the checks show the new behavior, reject the old expectation, and still confirm the parts that must not change? | Top-3 lists for the same users before/after; result of the version-specific checks; result of the unchanged invariant checks; two run URLs on two identified commits. Shows if the pipeline *detects* a behavior change instead of just turning green. |

**Selected function/component:** `recommend_for_user` in [`lab7/recommend_app.py`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/semester-investigation/lab7/recommend_app.py). It fits Cornac's [`MostPop`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/8e81b0bf4e2cb995b9c35dfa3b5dac4a4fa67b57/cornac/models/most_pop/recom_most_pop.py) model on a training set built with `cornac.data.Dataset.from_uir` and calls Cornac's [`Recommender.recommend`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/8e81b0bf4e2cb995b9c35dfa3b5dac4a4fa67b57/cornac/models/recommender.py#L536-L583).  
**Why this represents the software's purpose:** Cornac is a recommender-systems library; its main job is to learn from user–item interactions and return a ranked list of items for a user. `recommend_for_user` answers exactly the question an application asks: "which k items should we show to this user?".  
**Representative input and baseline expectation:** A fixed log of 21 implicit interactions (6 users, 6 items; popularity i1=6, i2=5, i3=4, i4=3, i5=2, i6=1, no ties). User `u1` has already consumed i1, i2, i3; user `u6` has consumed only i1. Baseline expectation with k=3: `u1 → [i1, i2, i3]` and `u6 → [i1, i2, i3]` (plain popularity ranking, already-consumed items included).  
**Planned small behavior change:** Exclude items the user has already consumed (Cornac's `remove_seen=True` with the training set). Reason: recommending something the user already bought/watched wastes a recommendation slot. Expected after change: `u1 → [i4, i5, i6]`, `u6 → [i2, i3, i4]`.  
**What must still work unchanged?** (a) Cornac is loaded from the fork checkout; (b) the learned popularity counts match the log; (c) the result has exactly k distinct, known items in non-increasing popularity order; (d) an unknown user is rejected with `ValueError`.

## 2. Baseline: deploy and execute on GitHub

| Evidence | Baseline |
|---|---|
| Baseline commit SHA and link | [`df06560ed230bab7d590f210d6a1aa330dd72f4f`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/df06560ed230bab7d590f210d6a1aa330dd72f4f) on `lab7-abdelrahman` (adds the Lab #7 function, checks and workflow; Cornac library code unchanged) |
| Actions workflow file link | [`.github/workflows/lab7-deploy.yml`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/semester-investigation/.github/workflows/lab7-deploy.yml) |
| Ubuntu/runtime and relevant dependency versions | GitHub-hosted runner `ubuntu-24.04` (Ubuntu 24.04.5 LTS, image version 20261116.376.1, runner 2.338.2); Python 3.12.16; pytest 9.2.0; Cornac 3.1.0 built from source; latest `numpy>2.0.0`, SciPy and Cython from PyPI at run time |
| How the fork's code is installed/built and verified as the executed code | `actions/checkout@v4` checks out the pushed commit; the job prints `GITHUB_SHA`; `pip install -e .` compiles Cornac's Cython extensions from the fork source; a step prints `cornac.__file__`; the test `test_cornac_is_loaded_from_this_fork_checkout` asserts that Cornac is imported from the checkout folder. |
| Functional case executed (command/script/test or local endpoint) | `python -m lab7.recommend_app` (prints a JSON report, uploaded as artifact `lab7-report`), then `python -m pytest lab7/test_recommend_app.py` (7 checks). |
| Expected vs observed behavior | Expected `u1 → [i1, i2, i3]`, `u6 → [i1, i2, i3]`, popularity `i1=6 … i6=1`. Observed (JSON report in the log): exactly the same. Note: all three items shown to `u1` are items `u1` already consumed. |
| Check result and meaningful measurement(s), if any | **7 passed** in 1.05 s. Runner printed `GITHUB_SHA=df06560…` (= pushed commit) and `loaded from /home/runner/work/cornac/cornac/cornac/__init__.py` (the checkout, not site-packages). Job time 5 min 26 s, of which building Cornac from source took 5 min 4 s, installing build tools 12 s, running the case 2 s. |
| Exact GitHub Actions run URL | https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/45823312432/job/139920906411 |

**What does this establish, and what does it not establish?** It shows that the fork's commit `df06560` can be checked out, compiled (Cython extensions) and executed on a clean Ubuntu runner, and that the executed Cornac is the fork's source, not a PyPI package. It also shows that the recommendation path gives the expected ranking for a known input. It does not show that Cornac works on other OSs or Python versions, with other models, or on realistic data sizes; it is one small, fixed case.

## 3. Controlled change and verification

**Source/function changed:** `recommend_for_user` in [`lab7/recommend_app.py`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/e16693ba2318e6c9971e032902a817afd6d9cf23/lab7/recommend_app.py#L43-L49). It now calls Cornac's `Recommender.recommend(user_id, k=k, remove_seen=True, train_set=train_set)` instead of `recommend(user_id, k=k)`. Cornac's own library code was not modified.  
**Reason for change:** Recommending an item the user has already bought/watched wastes a slot; showing only new items is a common product rule for a "recommended for you" list.  
**Code-change commit(s):** behaviour change [`e16693b`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/e16693ba2318e6c9971e032902a817afd6d9cf23) (1 file, +6/−2); updated checks [`2648ae5`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/2648ae578c6f3575cd3bfe51361124952c244894). Baseline: [`df06560`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/df06560ed230bab7d590f210d6a1aa330dd72f4f).

To show that the pipeline detects the change by itself, I pushed the code change **first, with the old checks unchanged** (run 2), and updated the expectations only afterwards (run 3).

| Item | Before change | After change |
|---|---|---|
| Same input/case | Fixed 21-interaction log, MostPop, k=3, users `u1` (seen i1–i3) and `u6` (seen i1) | Same log, model, k and users |
| Expected behavior under each version's stated contract | "Top-k most popular items": `u1 → [i1, i2, i3]`, `u6 → [i1, i2, i3]` | "Top-k most popular items the user has not consumed yet": `u1 → [i4, i5, i6]`, `u6 → [i2, i3, i4]` |
| Observed behavior on GitHub runner | `u1 → [i1, i2, i3]`, `u6 → [i1, i2, i3]` (JSON report, run 1) | `u1 → ['i4', 'i5', 'i6']`, `u6 → ['i2', 'i3', 'i4']` (pytest assertion output, run 2; asserted again in run 3) |
| Automated case check/result | `test_u1_top3`, `test_u6_top3` passed (old expectation) | Run 2 (new code, old checks): **2 failed, 5 passed**, both failures are the old expectations. Run 3 (new checks): `test_u1_top3`, `test_u6_top3` with the new lists and `test_no_already_consumed_item_is_recommended[u1/u6]` passed |
| Unchanged regression/invariant check | 5 passed: Cornac loaded from the checkout; popularity `i1=6 … i6=1`; 3 distinct known items in popularity order (u1, u6); unknown user → `ValueError` | The same 5 checks, **unchanged in code**, passed in run 2 and run 3 |
| Exact Actions run URL | Run 1 ✅ 7 passed, 5 min 26 s: https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/45823312432/job/139920906411 | Run 2 ❌ (expected, old checks): https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/45825526060/job/139928564146 <br> Run 3 ✅ 9 passed, 6 min 21 s: https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/45826833259/job/139933038972 |
| Commit SHA | `df06560ed230bab7d590f210d6a1aa330dd72f4f` | `e16693ba2318e6c9971e032902a817afd6d9cf23` (code) · `2648ae578c6f3575cd3bfe51361124952c244894` (checks) |

**How do your checks distinguish the two versions?** `test_u1_top3` and `test_u6_top3` compare the exact top-3 list with the expected list of the version; `test_no_already_consumed_item_is_recommended` checks that no item from the user's history appears in the output. In run 2 the old exact-list assertions failed with `assert ['i4', 'i5', 'i6'] == ['i1', 'i2', 'i3']` and `assert ['i2', 'i3', 'i4'] == ['i1', 'i2', 'i3']`: this informative failure shows the old contract no longer describes the changed case, and the pytest diff shows exactly which items moved. In the same run the 5 unchanged invariants passed, so the change did not break the model, the ranking order or the input validation. Run 3 shows the new expectations and the same invariants passing together; the new version was therefore not accepted just because every expectation was rewritten.

**Did anything fail unexpectedly? What did you learn or fix?** None unexpected. Run 2 failed on purpose (2 failures, both expected and explained above); the final version (run 3) is green. Learned: building Cornac's Cython extensions dominates the job time (5 min 4 s of 5 min 26 s in run 1), so the functional check itself is cheap, but each verification still costs about 5–6 minutes.

## 4. Engineering judgment and submission

**Answer Q1:** Yes, for this case. All three runs checked out the pushed commit, printed its SHA (`GITHUB_SHA=df06560…` in run 1, matching the commit), compiled Cornac from the fork source with `pip install -e .`, and loaded it from `/home/runner/work/cornac/cornac/cornac/__init__.py` — the checkout, not a PyPI package (also asserted by `test_cornac_is_loaded_from_this_fork_checkout`). The fresh `ubuntu-24.04` runner needed no manual steps; the build took about 5 minutes.  
**Answer Q2:** Yes. When only the code changed, the pipeline went red with exactly the two version-specific checks failing and the pytest diff showing the new lists (`[i4, i5, i6]`, `[i2, i3, i4]`), while the five unchanged invariants passed. After updating the expectations, all 9 checks passed. So the change was both visible and verified, and the unchanged checks show that nothing else in the tested behaviour moved.

**Release decision:** **Accept the changed version** for this function. The new behaviour is executed from the identified commit `2648ae5`, matches its stated contract on GitHub, and the invariants that should not change still hold. The red run 2 is an intended experiment, not the final state.  
**One important limitation or missing check:** The evidence covers one tiny, hand-made dataset, one non-personalised model (MostPop), k=3 and two users, on one OS and Python version. It does not show behaviour for a user who has seen almost all items (the list can become shorter than k — e.g. `u2` would get an empty list), for other Cornac models, for realistic data sizes, or performance; the `remove_seen` logic itself is Cornac's and is only tested through this case.

| GitHub evidence | Link |
|---|---|
| Lab #7 pull request (within your fork) | ⏳ added after merge |
| **Merged commit** on `semester-investigation` | ⏳ added after merge |
| Final `LAB7_ANALYSIS.md` on merged branch | https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/semester-investigation/LAB7_ANALYSIS.md |
| Student 1 meaningful commit(s) | Abdelrahman Aljaloudy: [`df06560`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/df06560ed230bab7d590f210d6a1aa330dd72f4f) (function, checks, workflow) · [`e16693b`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/e16693ba2318e6c9971e032902a817afd6d9cf23) (behaviour change) · [`2648ae5`](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/2648ae578c6f3575cd3bfe51361124952c244894) (updated checks) |
| Student 2 meaningful commit(s), if a pair | Not applicable (individual) |

**LLM assistance (if used):** Claude (Anthropic) helped draft the workflow YAML, the small `recommend_app.py` case, the pytest checks and this record. I verified them myself: I read `Recommender.recommend` and `MostPop` in the fork to confirm what `remove_seen` does, checked every number in this file against the GitHub Actions logs (SHA, Cornac path, recommendations, test results, durations), and confirmed that the red run 2 failed only on the two expected assertions.

**Submission reminder:** Each student submits `Lab7_YOUR_GITHUB_HANDLE.txt` to the Lab #7 MS Teams submit folder, containing their name, fork URL, merged-commit URL and final analysis URL.

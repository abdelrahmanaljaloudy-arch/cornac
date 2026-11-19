# Lab #6 - Investigation Record

**Team / student(s):** Abdelrahman Aljaloudy ([abdelrahmanaljaloudy-arch](https://github.com/abdelrahmanaljaloudy-arch))  
**Mode:** individual  
**Approved upstream project:** https://github.com/PreferredAI/cornac  
**Fork / working branch:** https://github.com/abdelrahmanaljaloudy-arch/cornac/tree/semester-investigation  
**Original Lab #5 version:** `8e81b0bf4e2cb995b9c35dfa3b5dac4a4fa67b57` (tag `v3.1.0`)  
**Lab #6 pre-refactoring baseline:** `39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7` ([commit](https://github.com/abdelrahmanaljaloudy-arch/cornac/commit/39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7)) - source code identical to `v3.1.0`; only the Lab #5/#6 records and the three `lab6-*` workflows were added.

> Keep this file short and evidence-based. Replace the placeholders as you go. Every analysis/test link must point to your **fork's GitHub-visible results**. Do not submit unsupported local-only tool screenshots.

## Task 1 - Stakeholder, GQM, and Code Smell Selection

**Selected stakeholder and exact fictional concern from handout:** Scenario B - Maya, Technical-Debt Manager: "We have limited development time, and some implementation choices could make future changes more expensive. We cannot improve everything. Please investigate suspected technical debt, compare its likely impact and the effort to address it, and justify which small improvements are worth making now."

**GQM goal:** Analyze **the handwritten Python source of Cornac v3.1.0 (package `cornac/`)** for the purpose of **prioritizing small technical-debt repayments**, with respect to **maintainability symptoms (method complexity and size, parameter lists, duplicated and repeated logic)**, from the viewpoint of **Maya, the technical-debt manager**, in the context of **the `semester-investigation` branch of my fork at the baseline commit, analyzed with GitHub Actions**.

| Initial question | Question wording | Relevant metric(s) / observation(s) | Why useful? |
|---|---|---|---|
| **Q1** | Where are the strongest smell symptoms (complex/long functions, long parameter lists, duplicated code), and are they in code that is widely used or likely to change? | Ruff: C901 (McCabe complexity), PLR0912 (branches), PLR0915 (statements), PLR0913 (arguments); jscpd: clones and duplicated lines; number of callers; commits per file in the upstream history | Shows *where* debt might cost money in the future. A smell in widely used or often changed code has a higher expected cost than one in an isolated model. |
| **Q2** | For the top candidates, how much effort and behaviour risk would a small refactoring need, and is the code protected by existing tests? | Size of the change (lines/functions touched); existing tests that call the code; outcome of the targeted test workflow before/after; rule result before/after | Maya can only afford small improvements. This tells her which repayment is cheap and safe *now* and which should be deferred. |

**Code-smell types chosen from the lecture:** 4 (individual)

| Smell type | Lecture slide(s) | Why relevant to our GQM? | How we plan to investigate it (tool/rule/metric/inspection) |
|---|---|---|---|
| 1. Long Method (Brain Method) | 32, 34-37 | Long, branchy methods are harder to understand and change, so every future change there is more expensive. | **Metric-based indication:** Ruff C901, PLR0912, PLR0915; then source inspection (slide 37: size + complexity together). |
| 2. Duplicated Code | 32, 73-77 | Every fix must be repeated in each copy; copies can drift apart and cause defects (slide 73). | **Automatic detection:** jscpd clone report (exact clones, duplicated lines); then source inspection. |
| 3. Long Parameter List | 32, 43-44 | Many parameters make calls error-prone and hard to change. | **Automatic rule:** Ruff PLR0913; then inspection of whether parameters are justified (e.g. model hyper-parameters). |
| 4. Switch Statements | 32, 50-52 | The same type-based decision logic repeated in several places means one new option needs several edits. | **Manual inspection** of repeated `if/elif` chains, supported by Ruff C901 on the same function (no direct rule exists). |

**Primary GitHub-integrated tool:** [Ruff](https://docs.astral.sh/ruff/) 0.14.4 in GitHub Actions (`.github/workflows/lab6-python-ruff.yml`)  
**Complementary tool (only if needed):** [jscpd](https://github.com/kucherenko/jscpd) 5.3.2 in GitHub Actions (`.github/workflows/lab6-duplication.yml`)  
**Why these tools match our questions and selected smells:** Ruff gives per-function complexity, branch, statement and argument counts (Long Method, Long Parameter List, Q1) directly on GitHub. Ruff has no duplication rule, so jscpd is needed for Duplicated Code. A third workflow (`lab6-tests.yml`) builds Cornac from the fork and runs existing tests to answer Q2 (behaviour risk).

## Task 2 - Detect and Investigate Code Smells

**Analysis configuration:**

- Fork branch and **baseline SHA**: `semester-investigation` @ `39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7`
- Source directory/directories analyzed: Ruff: `cornac/` (handwritten `.py` only). jscpd: whole repository with the exclusions below; interpretation restricted to the **Python** format.
- Exclusions (generated/test/vendor/weight data, etc.): jscpd ignores `tests/`, `docs/`, `examples/`, `*.pyx` (Cython), `*.md`, `*.yml`, `.venv/`, `build/`, `dist/`. Ruff does not parse `.pyx` files. **Not excluded but discussed below:** vendored C++ libraries in `cornac/utils/external/` (Boost, Eigen).
- Tool(s), versions and relevant enabled rules/settings: Ruff 0.14.4, rules `C901` (McCabe complexity > 10), `PLR0912` (branches > 12), `PLR0913` (arguments > 5), `PLR0915` (statements > 50), default thresholds; jscpd 5.3.2 (default min. tokens), reporters console/json/sarif; Python 3.12 + pytest for the targeted tests.
- **Baseline GitHub scan / Actions run link(s):**
  - Ruff: [Lab6 - Python Ruff #2](https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/44531553866) - success, commit `39c29b6`, artifact `lab6-ruff-report`
  - jscpd: [Lab6 - Duplication #1](https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/44531553963) - success, commit `39c29b6`, artifact `lab6-duplication-report`
  - Tests: [Lab6 - Targeted tests #1](https://github.com/abdelrahmanaljaloudy-arch/cornac/actions/runs/44531554126) - success (126 passed), commit `39c29b6`

**Baseline numbers (preserved here because artifacts expire):** Ruff found **213** findings in `cornac/`: 166 × PLR0913, 20 × C901, 15 × PLR0915, 12 × PLR0912. jscpd, Python format: **188 clones, 3,682 duplicated lines (8.7 %)**; all formats together: 4,150 clones, 25.4 % (dominated by vendored C++ headers).

| Selected smell type | Found / not found / not assessable | Tool result or source link | Interpretation / limitations |
|---|---|---|---|
| Long Method | **Found (candidates)** | Ruff C901/PLR0912/PLR0915: 20 / 12 / 15 functions, e.g. `next_item_evaluation.ranking_eval` (complexity 20, 22 branches, 67 statements), `utils/common.normalize` (complexity 12) | Most hits are in optional deep-learning models (`causalrec`, `diffgrm`, `hypar`…). Complexity is a symptom; only inspection shows whether a method really mixes several responsibilities (slide 37). |
| Duplicated Code | **Found** | jscpd: 188 Python clones; e.g. `UserKNN.__init__` and `ItemKNN.__init__` in `models/knn/recom_knn.py` share a 60-line clone (lines 131-190 vs 307-366) plus a 25-line clone in `fit` | Real copy-paste between two sibling classes, but the copies differ in one condition (`pearson`), so merging needs care. Many other clones are between independent model implementations. |
| Long Parameter List | **Found, mostly not a design problem** | Ruff PLR0913: 166 functions, 134 of them in `cornac/models` | Mostly model constructors whose parameters are documented hyper-parameters (e.g. `k`, `max_iter`, `learning_rate`, `lambda_reg`, `seed`). This is a normal API style for ML libraries → an ordinary rule violation for Maya, not priority debt. |
| Switch Statements | **Found (manual inspection)** | No direct rule. In `normalize` ([source](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7/cornac/utils/common.py#L216-L238)) the same `if norm == 'l1' / 'l2' / 'max'` decision appears **twice** (sparse and dense branch) | Matches slide 50: "the same decision logic repeated in several places". Adding a new norm requires two edits. Small scale (one function), so the cost is moderate. |

**Candidate issues inspected in source (at least two):**

| Candidate ID | File/entity permalink | What was actually observed? | Why it might matter / why uncertain |
|---|---|---|---|
| C1 | [`cornac/utils/common.py` → `normalize`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7/cornac/utils/common.py#L176-L241) | One function does validation, copying/type conversion, transposing **and** two complete normalisation algorithms (sparse and dense), each with its own `l1/l2/max` chain. Ruff C901: complexity 12 > 10. | Public utility exported as `cornac.utils.normalize` and used by `cornac/data/text.py` (text-modality features) → reached by user code and data loading, not one model only. Uncertain: the function is still readable and has been stable (1 commit since 2024), so the future cost is moderate. |
| C2 | [`cornac/eval_methods/next_item_evaluation.py` → `ranking_eval`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7/cornac/eval_methods/next_item_evaluation.py#L80) | Very long evaluation loop: complexity 20, 22 branches, 67 statements; mixes data preparation, scoring, optional semantic-ID metrics and result collection. | Core evaluation code that is **actively changing** (5 of its 6 commits are since 2024). High future cost, but also the riskiest to touch: results feed every next-item experiment. |
| C3 (optional) | [`cornac/models/knn/recom_knn.py` → `UserKNN` / `ItemKNN`](https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/39c29b638d1f8a14c19cdf7e0d1b8fc0a9b48de7/cornac/models/knn/recom_knn.py#L129-L166) | `__init__` of both classes is a 60-line copy; `fit` shares 25 more lines. The copies differ in one condition. | Any change to parameters must be made twice. Uncertain: there are **no dedicated KNN tests** in `tests/cornac/models`, so behaviour preservation would be hard to show. |

**One warning we challenged, or one potentially missed issue:** The jscpd run reports **25.4 % duplication**, but this number is misleading: almost all of it comes from **vendored third-party C++ headers** in `cornac/utils/external/boost` (e.g. `rational_horner3_9.hpp` vs `rational_horner3_14.hpp`, 774 duplicated lines). That code is not written or maintained by the Cornac team, so it is not their technical debt. I therefore interpret only the **Python** figure (8.7 %). A second limitation: neither tool analyses the 24 Cython `.pyx` files (most of the fast models), so debt there is **not assessed**.

## Task 3 - Prioritize Technical Debt and Plan Refactoring

| Candidate | Expected future impact / relevance | Estimated effort and behavior risk | Prioritize now or defer? Why? |
|---|---|---|---|
| C1 `normalize` | Moderate: a public utility (`cornac.utils.normalize`, used by `data/text.py`); anyone adding a norm or fixing a bug must understand both branches and edit two chains. | **Low effort** (one function, ~30 lines moved, no API change). **Low risk**: existing test `test_common.py::test_normalize` checks all three norms, both axes, sparse and dense, against expected values. | **Now.** Best value for small effort, and the change can be verified on GitHub. |
| C2 `ranking_eval` (next-item) | High: core evaluation code that is changing often; complexity makes each change expensive. | **High effort** (one 67-statement function with many interacting branches). **High risk**: any slip silently changes evaluation numbers. | **Defer.** Worth repaying, but it needs a planned change with extra characterisation tests first. |
| C3 KNN duplicated `__init__` | Moderate: two copies of the same parameter handling can drift apart. | **Medium effort**: needs a shared base class or helper. **Medium-high risk**: no dedicated tests; one condition differs between the copies. | **Defer.** First add KNN tests, then extract the shared part. |

**Selected documented issue(s) and individual ownership:** 1 issue (C1), owned by Abdelrahman Aljaloudy.

| Contributor / GitHub handle | Candidate ID | Planned refactoring | Expected benefit | GitHub regression check planned |
|---|---|---|---|---|
| Abdelrahman Aljaloudy / abdelrahmanaljaloudy-arch | C1 | **Extract Method** (slide 36): move the sparse and dense normalisation into two private helpers `_normalize_sparse_rows(X, norm)` and `_normalize_dense_rows(X, norm)`; `normalize` keeps only validation, copy/transposition and the choice between the two. | Each function has one job; the `norm` decision is now in small, named units; lower complexity in `normalize`. Public signature and results unchanged. | `Lab6 - Targeted tests` (builds Cornac from the fork; runs `tests/cornac/utils/test_common.py`, `tests/cornac/eval_methods`, `tests/cornac/metrics`) + `Lab6 - Python Ruff` to compare C901 before/after. |

## Task 4 - Refactor, Verify, and Commit

**Baseline test/check run(s) on GitHub:** [URL(s) and outcomes]  
**After-refactoring SHA(s):** [full SHA(s)]  
**After-refactoring scan / workflow run(s):** [URL(s)]  
**After-refactoring test/check run(s):** [URL(s) and outcomes]

| Issue / contributor | Before (same scope and measurement) | After | Test / verification result | What does this actually establish? |
|---|---|---|---|---|
| | | | | |

**Answers to the original GQM questions:**

- **Q1:** [answer based on evidence, not only a warning count]
- **Q2:** [answer based on evidence, not only a warning count]

**Conclusion and limits:** [What was improved? Did any measurements worsen or remain unchanged? What cannot be claimed about maintainability or preserved behavior?]

### Individual implementation commits - permanent GitHub links

| Contributor / GitHub account | Documented issue (C1, C2, ...) | What was refactored? | **Permanent commit link** | PR or GitHub Actions push-run link |
|---|---|---|---|---|
| Abdelrahman Aljaloudy / abdelrahmanaljaloudy-arch | | | | |

**Completed template location on `semester-investigation`:** https://github.com/abdelrahmanaljaloudy-arch/cornac/blob/semester-investigation/LAB6_ANALYSIS.md  
**Template/report commit link:** [GitHub `/commit/FULL_SHA` URL]

**Evidence preservation note:** [If any GitHub Actions artifact is relevant, provide a run link and preserve its essential figures here because workflow artifacts can expire.]

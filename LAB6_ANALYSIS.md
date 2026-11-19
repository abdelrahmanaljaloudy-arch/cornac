# Lab #6 - Investigation Record

**Team / student(s):** [names and GitHub handles]  
**Mode:** [individual / pair]  
**Approved upstream project:** [URL]  
**Fork / working branch:** [link to `semester-investigation`]  
**Original Lab #5 version:** [full SHA from LAB5_SELECTION.md]  
**Lab #6 pre-refactoring baseline:** [full SHA and commit link]

> Keep this file short and evidence-based. Replace the placeholders as you go. Every analysis/test link must point to your **fork's GitHub-visible results**. Do not submit unsupported local-only tool screenshots.

## Task 1 - Stakeholder, GQM, and Code Smell Selection

**Selected stakeholder and exact fictional concern from handout:** [copy one statement]

**GQM goal:** Analyze **[object]** for the purpose of **[purpose]**, with respect to **[quality focus]**, from the viewpoint of **[stakeholder]**, in the context of **[environment]**.

| Initial question | Question wording | Relevant metric(s) / observation(s) | Why useful? |
|---|---|---|---|
| **Q1** | | | |
| **Q2** | | | |

**Code-smell types chosen from the lecture:** [individual: 3-4; pair: 5-6; selection does NOT guarantee they exist]

| Smell type | Lecture slide(s) | Why relevant to our GQM? | How we plan to investigate it (tool/rule/metric/inspection) |
|---|---|---|---|
| 1. | | | |
| 2. | | | |
| 3. | | | |
| 4. (if applicable) | | | |
| 5. (pair, if applicable) | | | |
| 6. (pair, if applicable) | | | |

**Primary GitHub-integrated tool:** [name / official link]  
**Complementary tool (only if needed):** [name / link or N/A]  
**Why these tools match our questions and selected smells:** [1-3 sentences]

## Task 2 - Detect and Investigate Code Smells

**Analysis configuration:**

- Fork branch and **baseline SHA**: [full SHA]
- Source directory/directories analyzed: [paths]
- Exclusions (generated/test/vendor/weight data, etc.): [paths or none]
- Tool(s), versions and relevant enabled rules/settings: [details]
- **Baseline GitHub scan / Actions run link(s):** [direct links]

| Selected smell type | Found / not found / not assessable | Tool result or source link | Interpretation / limitations |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**Candidate issues inspected in source (at least two):**

| Candidate ID | File/entity permalink | What was actually observed? | Why it might matter / why uncertain |
|---|---|---|---|
| C1 | | | |
| C2 | | | |
| C3 (optional) | | | |

**One warning we challenged, or one potentially missed issue:** [brief explanation of tool limitations, possible false alarm or incomplete coverage]

## Task 3 - Prioritize Technical Debt and Plan Refactoring

| Candidate | Expected future impact / relevance | Estimated effort and behavior risk | Prioritize now or defer? Why? |
|---|---|---|---|
| C1 | | | |
| C2 | | | |
| Additional (if needed) | | | |

**Selected documented issue(s) and individual ownership:** [1-2 per student; pair total 2-4]

| Contributor / GitHub handle | Candidate ID | Planned refactoring | Expected benefit | GitHub regression check planned |
|---|---|---|---|---|
| | | | | |
| [second member if pair] | | | | |

## Task 4 - Refactor, Verify, and Commit

**Baseline test/check run(s) on GitHub:** [URL(s) and outcomes]  
**After-refactoring SHA(s):** [full SHA(s)]  
**After-refactoring scan / workflow run(s):** [URL(s)]  
**After-refactoring test/check run(s):** [URL(s) and outcomes]

| Issue / contributor | Before (same scope and measurement) | After | Test / verification result | What does this actually establish? |
|---|---|---|---|---|
| | | | | |
| | | | | |

**Answers to the original GQM questions:**

- **Q1:** [answer based on evidence, not only a warning count]
- **Q2:** [answer based on evidence, not only a warning count]

**Conclusion and limits:** [What was improved? Did any measurements worsen or remain unchanged? What cannot be claimed about maintainability or preserved behavior?]

### Individual implementation commits - permanent GitHub links

> Each student creates and pushes **their own** changes from **their own machine/account**. Include direct `/commit/FULL_SHA` links, **not just repository or PR URLs**. Do not squash individual source commits into a single partner-authored commit.

| Contributor / GitHub account | Documented issue (C1, C2, ...) | What was refactored? | **Permanent commit link** | PR or GitHub Actions push-run link |
|---|---|---|---|---|
| Student 1 | | | `https://github.com/OWNER/REPO/commit/FULL_SHA` | |
| Student 1 (second issue, if applicable) | | | | |
| Student 2 (pair only) | | | | |
| Student 2 (second issue, if applicable) | | | | |

**Completed template location on `semester-investigation`:** [GitHub file URL]  
**Template/report commit link:** [GitHub `/commit/FULL_SHA` URL]

**Evidence preservation note:** [If any GitHub Actions artifact is relevant, provide a run link and preserve its essential figures here because workflow artifacts can expire.]

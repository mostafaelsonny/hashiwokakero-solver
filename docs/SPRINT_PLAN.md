# Sprint Plan (4 أسابيع)

| Sprint | الأسبوع | التركيز | النتيجة (Milestone) |
|---|---|---|---|
| 1 | الأول | Understanding + Core Foundation | أساس المشروع جاهز: Data Model + Core Validation + واجهة إدخال مبدئية + تصميم الخوارزميات |
| 2 | التاني | Backtracking | أول Algorithm شغالة: إدخال Puzzle وحلها بـ Backtracking |
| 3 | التالت | GA + MA | كل الخوارزميات الأساسية موجودة وبتشتغل على نفس الـ Data Model |
| 4 | الرابع | Integration + Testing | مشروع جاهز للتسليم + Demo |

**تواريخ الـ Sprints:** Sprint 1: ____ → ____  •  Sprint 2: ____ → ____  •  Sprint 3: ____ → ____  •  Sprint 4: ____ → ____ (املاها لما تتحدد)

القاعدة: **آخر 20% من كل Sprint للمراجعة والاختبار، مش لـ Features جديدة.** Daily Standup 10 دقايق: عملت إيه؟ هعمل إيه؟ إيه اللي معطلني؟

---
## Sprint 1 — Understanding & Core Foundation
**الهدف:** نفهم المشكلة، نثبّت شكل بيانات واحد، ونبني أدوات التحقق اللي الخوارزميات التلاتة هتعتمد عليها. **مش مطلوب نحل اللغز في الـ Sprint ده.**

### المهام (ربط مع كروت Trello)
| ID | المهمة | المسؤول | المراجع | الملفات | Branch |
|---|---|---|---|---|---|
| S1-01 ✅ | Requirements & Rule Alignment | Mostafa | الفريق | `docs/PROJECT_REQUIREMENTS.md` | — |
| S1-02 | Approve Shared Data Model | Mostafa + Monzer | الفريق | `docs/DATA_MODEL.md` | `docs/data-model` |
| S1-03 | Candidate Edge Generator | Monzer | Mostafa | `core/candidate_generator.py` + test | `feature/candidate-generator` |
| S1-04 | Degree Validator | Ebrahim | Mostafa | `core/degree_validator.py` + test | `feature/degree-validator` |
| S1-05 | Crossing Detection | Monzer | Mostafa | `core/crossing_detector.py` + test | `feature/crossing-detector` |
| S1-06 | Connectivity Checker | Ebrahim | Mostafa | `core/connectivity_checker.py` + test | `feature/connectivity-checker` |
| S1-07 | Final Solution Validator | Ebrahim | Mostafa + Monzer | `core/solution_validator.py` + test | `feature/solution-validator` |
| S1-08 | Backtracking Design & Pseudocode | Ebrahim | Mostafa | `docs/BACKTRACKING_DESIGN.md` | `docs/backtracking-design` |
| S1-09 | Genetic Algorithm Design | Rovan | Mostafa | `docs/GA_OVERVIEW.md`, `CHROMOSOME_SPEC.md`, `GA_DESIGN.md` | `docs/ga-design` |
| S1-10 | Memetic Algorithm & Local Search Design | Febronia | Mostafa + Rovan | `docs/MA_OVERVIEW.md`, `MA_DESIGN.md` | `docs/ma-design` |
| S1-11 | Basic Puzzle Editor UI | Febronia | Mostafa | `frontend/`, `docs/UI_DATA_SPEC.md` | `feature/puzzle-editor` |
| S1-12 | Sprint 1 Integration & Test Cases | Mostafa | — | `tests/`، تقرير Integration | `feature/core-integration-tests` |

مهام Febronia (S1-10 وS1-11) من غير assignee لحد ما يتضاف. لحد وقتها Mostafa بيتابع الجزء النظري.

### الجدول اليومي
| العضو | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |
|---|---|---|---|---|---|
| Mostafa | Setup + Kickoff + Requirements | Data Model Approval (S1-02) | Review PRs + Test Cases مشتركة | Integration (S1-12) | Sprint Review |
| Monzer | دراسة Graph + Crossing (`GRAPH_ENGINE_NOTES.md`) | `CANDIDATE_EDGES_SPEC.md` | كود S1-03 وS1-05 | Fix & Test | Acceptance + عرض |
| Ebrahim | دراسة Degree/BFS/DFS/Backtracking (`VALIDATION_NOTES.md`) | `VALIDATOR_SPEC.md` | كود S1-04 وS1-06 + هيكل S1-07 | S1-07 النهائي + `BACKTRACKING_DESIGN.md` | Acceptance + عرض |
| Rovan | دراسة GA (`GA_OVERVIEW.md`) | `CHROMOSOME_SPEC.md` | `GA_DESIGN.md` + Fitness | التصميم النهائي | عرض Chromosome وFitness |
| Febronia | دراسة MA + Wireframe | `UI_DATA_SPEC.md` | MA_DESIGN + UI Scaffold | إكمال UI + Pseudocode | عرض |

**مفيش كود قبل نهاية Day 2** (اعتماد الـ Data Model). Day 5 مفيش Features جديدة.

### Definition of Done لـ Sprint 1
| ID | المعيار | أولوية |
|---|---|---|
| S1-01 | الكل فاهم قواعد اللعبة | Critical |
| S1-02 | Data Model موحد ومتجمّد | Critical |
| S1-03 | Candidate Edge Generator شغال | Critical |
| S1-04 | Degree Validation شغال (Partial + Final) | Critical |
| S1-05 | Crossing Detection شغال | Critical |
| S1-06 | Connectivity Checker شغال | Critical |
| S1-07 | Final Validator شغال | Critical |
| S1-08 / 09 / 10 | تصميمات Backtracking وGA وMA جاهزة | High |
| S1-11 | واجهة إدخال Puzzle شغالة | Medium |
| S1-12 | كل الأجزاء عدّت الاختبارات الأساسية واتدمجت | Critical |

**لو S1-03 لـ S1-07 مش شغالين، Sprint 1 ما حققش هدفه حتى لو خلصنا الباقي.**
الحالة في Sprint Review: **Accepted** / **Needs Fixes** / **Blocked**.

---
## Sprint 2 — Backtracking
تفاصيل المهام في Trello (S2-01 → S2-06): Search State & Pruning • Implement Backtracking Solver • Integrate with Core Engine • Unit Tests • Connect to UI • Integration & Acceptance.
- Ebrahim ينفّذ Backtracking. Monzer يكمّل Core ويساعد. Rovan يجهّز GA على الـ Data Model. Febronia: Puzzle Input وعرض الحل. Mostafa: مراجعة وربط الواجهة.
- يتعلموا: Recursion • Backtracking • Pruning فقط.
- **Milestone:** تطبيق بيدخّل Puzzle ويحلها بـ Backtracking والنتيجة بتعدّي على Validator.

## Sprint 3 — GA & MA
تفاصيل المهام في Trello (S3-01 → S3-10): Chromosome & Gene Mapping • Fitness & Penalties • Population & Operators • Complete GA • Local Search Operators • Memetic Algorithm • Integrate Final Validator • GA/MA Test Suite • Connect to UI • Acceptance.
- Rovan: GA. Febronia: Local Search وتحويل GA لـ MA. Monzer: مراجعة قيود الـ Fitness والـ Validator. Ebrahim: اختبار Backtracking والمساعدة في الأخطاء. Mostafa: مراجعة وIntegration.
- GA: Tournament + Uniform Crossover + Random Gene Mutation. MA: Hill Climbing على GA.
- **Milestone:** الخوارزميات التلاتة بتتعامل مع نفس الـ Data Model وبترجّع نتيجة قابلة للتحقق.

## Sprint 4 — Integration & Final Testing
تفاصيل المهام في Trello (S4-01 → S4-09): Integrate All • Enforce Unified Validation • End-to-End Tests • Edge Cases & Regression • Final Visualization • Invalid Input & No-Solution Handling • Bug Fixes & Code Freeze • README & Docs • Final Demo.
- مفيش Features جديدة. تجهيز 4-5 Puzzles للعرض (انظر `TESTING_STRATEGY.md`) + شرح: الفكرة، الخوارزميات والفرق بينها، Architecture، Demo.

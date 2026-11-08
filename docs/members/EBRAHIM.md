# Ebrahim: Validation & Backtracking

**الدور:** Validation (Degree + Connectivity + Final Validator) وتجهيز Backtracking

إنت المسؤول عن **الحَكَم**: الدوال اللي بتقول هل الحل صح ولا لأ. ومنها بتتبني Backtracking (Sprint 2). في Sprint 1 بتنفّذ الـ Validators وبتصمم Backtracking على الورق.

## 1) اللي لازم تفهمه (مفاهيم مهمتك بس)
- Node Degree: عدد الجسور على الجزيرة، والمزدوج بيتحسب **2** على الجزيرتين.
- **Partial** Validation (أثناء البحث: `actual <= required`) مقابل **Final** (`actual == required`).
- Connected Components بـ BFS أو DFS، من **الجسور الفعلية بس** (عدد أكبر من 0)، مش من الـ Candidate Edges.
- Recursion وBacktracking وPruning (3 مفاهيم بس).
- ليه الحل ممكن يحقق الأرقام وهو غلط (شبكة مقسومة).
- Validation Report: شكله وإنه لازم يجمع كل المخالفات مرة واحدة.

## 2) مهامك في Sprint 1
| Task | المهمة | الملفات | Branch | اختبارها |
|---|---|---|---|---|
| S1-04 | Degree Validator | `core/degree_validator.py` | `feature/degree-validator` | `python -m pytest tests/test_degree_validator.py -q` |
| S1-06 | Connectivity Checker | `core/connectivity_checker.py` | `feature/connectivity-checker` | `python -m pytest tests/test_connectivity.py -q` |
| S1-07 | Final Solution Validator | `core/solution_validator.py` | `feature/solution-validator` | `python -m pytest tests/test_solution_validator.py -q` |
| S1-08 | Backtracking Design & Pseudocode | `docs/BACKTRACKING_DESIGN.md` | `docs/backtracking-design` | Trace يدوي على P1 |

الوصف الكامل والـ Acceptance Criteria لكل مهمة في **كارت Trello** بتاعها. اقراه بالكامل قبل ما تبدأ.

## 3) جدولك اليومي
| Day | المطلوب |
|---|---|
| Day 1 | ادرس Degree وBFS/DFS وBacktracking، واكتب `docs/VALIDATION_NOTES.md` |
| Day 2 | `docs/VALIDATOR_SPEC.md` + راجع Data Model. **لسه مفيش كود** |
| Day 3 | كود S1-04 وS1-06 (على Test Data ثابتة لو S1-03 لسه ماخلصتش) + هيكل S1-07 |
| Day 4 | S1-07 النهائي (بعد ما S1-03/04/05/06 يتدمجوا) + `docs/BACKTRACKING_DESIGN.md` |
| Day 5 | Acceptance + عرض Validators وتصميم Backtracking |

## 4) تفاصيل كل مهمة
**S1-04 Degree Validator:** `compute_degrees(...)` و`check_degrees(..., mode)` حيث mode = `"partial"` أو `"final"`. بترجع violations بشكل `{island, required, actual}`. قيمة جسر مش 0/1/2 = `ValueError`.

**S1-06 Connectivity Checker:** `find_connected_components(...)` و`is_connected(...)`. جزيرة من غير جسور = مكوّن لوحدها. جزيرة واحدة = متصلة.

**S1-07 Final Validator:** `validate_solution(puzzle, solution)` بترجع التقرير. **لازم تنادي دوال S1-03/04/05/06، ماتعيدش كتابة منطقهم.** `valid` = true لو مفيش قيم غلط ومفيش degree violations ومفيش تقاطعات والمكونات = 1. Puzzle P1: الحل الوحيد الصحيح `[1,1,1,1]`، و`[2,0,0,2]` مرفوض (مكونين).

**S1-08 Backtracking Design (تصميم بس، من غير كود):** المتغيرات = الـ Edges، الـ Domain = {0,1,2}. فحص Partial بعد كل اختيار + Pruning، فحص Final في الآخر، شروط الإيقاف (`No Solution Exists` بعد بحث كامل مقابل `Search Limit Reached`)، الإحصائيات، Pseudocode، وTrace يدوي على P1.
## 5) اللي هتسلمه بالظبط
- `docs/VALIDATION_NOTES.md` (Day 1) و`docs/VALIDATOR_SPEC.md` (Day 2)
- `core/degree_validator.py` و`core/connectivity_checker.py` و`core/solution_validator.py` + اختباراتهم بتعدّي (xfail اتشالت)
- `docs/BACKTRACKING_DESIGN.md` فيه كل الأقسام + Trace على P1
- PR لكل مهمة، وS1-07 بعد ما S1-03 وS1-04 وS1-05 وS1-06 يتعملهم Merge

## 6) ازاي تبدأ (أول 30 دقيقة)
```bash
git clone REPO_URL && cd hashiwokakero-solver
git config user.name "اسمك" && git config user.email "ايميلك-على-GitHub"
git checkout develop
python -m venv .venv            # Windows: .venv\Scripts\activate   |  Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q             # المتوقع: passed + xfailed، مفيش failed
```
بعدها اقرا بالترتيب: [START_HERE.md](../START_HERE.md) ← [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) ← الكروت بتاعتك في Trello.

وبعدين لكل مهمة: [GIT_WORKFLOW.md](../GIT_WORKFLOW.md) خطوة 2 (branch جديدة من `develop`).

## 7) قبل ما تفتح الـ PR (Checklist)
- [ ] `git fetch origin && git merge origin/develop` وحليت أي Conflict.
- [ ] `python -m pytest -q` بيعدّي، وشلت علامة `xfail` من ملف الاختبار الخاص بمهمتك.
- [ ] الكود/المستند متوافق مع [DATA_MODEL.md](../DATA_MODEL.md).
- [ ] مفيش منطق متكرر من `core/`.
- [ ] قادر أشرح الكود بكلامي من غير ما أرجع للـ AI.
- [ ] الـ PR Template متملي، وكارت Trello اتحرّك لـ Code Review.

## 8) اختبر فهمك (لازم تجاوب قبل الـ PR)
1. إيه الفرق بين Partial وFinal؟ وإمتى بنستخدم كل واحد؟
2. ليه الجسر المزدوج بيتحسب 2 على الجزيرتين؟
3. ليه الاتصال بيتحسب من الجسور الفعلية مش الـ Candidate؟
4. إيه اللي بيحصل في `validate_solution` لو الحل فيه خطأ في الـ Degree وكمان شبكة مقسومة؟
5. إيه قاعدة الـ Pruning اللي بتحس إن الجزيرة مش هتوصل لرقمها؟
6. إمتى مسموح Backtracking تقول `No Solution Exists`؟

## 9) مين بيراجعك ومين مستنيك
- **بيراجعك:** Mostafa (وS1-07 كمان Monzer).
- **مستنيك:** كل المشروع: Backtracking (Sprint 2) والـ Fitness (Sprint 3) بيعتمدوا على `validate_solution`.
- **ملاحظة:** حمل Sprint 1 عليك أعلى من الباقي (4 مهام). لو اتأخرت في حاجة، قول لـ Mostafa بدري عشان نعيد التوزيع.

## 10) القواعد
- كل الشغل على branch بتاعتك، وبـ PR على `develop`. **ممنوع Merge ذاتي.** Mostafa هو الوحيد اللي بيراجع ويعمل Merge.
- مفيش كود قبل اعتماد الـ Data Model (S1-02، نهاية Day 2). قبلها: دراسة وSpecs بس.
- الـ Data Model بالحرف: `required_bridges`, `from`, `to`, `orientation`, `bridge_counts`.
- الـ AI بيكتب الكود والمسؤولية عليك: لازم تفهمه، وتشغّل الاختبارات، وتقدر تشرحه (انظر [AI_WORKFLOW.md](../AI_WORKFLOW.md)).
- أي تغيير في الـ Data Model بيروح لـ Mostafa الأول.

> **S1-07** مش بتتدمج قبل S1-03 وS1-04 وS1-05 وS1-06. ابدأ الهيكل بـ stubs واربطه بالدوال الحقيقية في Day 4.

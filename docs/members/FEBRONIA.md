# Febronia: Memetic Algorithm & Frontend

**الدور:** Memetic Algorithm (تصميم) + Puzzle Editor (الواجهة)

> أول خطوة: اقبل دعوة الـ repo على GitHub، واقرا [START_HERE.md](../START_HERE.md) و[GIT_WORKFLOW.md](../GIT_WORKFLOW.md)، واتبع الخطوات هنا. تاسكاتك في Trello (Mostafa بيعيّنهم ليك).

إنت المسؤول عن الجزء اللي بيحوّل GA لـ Memetic (Local Search)، وعن الواجهة اللي المستخدم بيتعامل معاها.

## 1) اللي لازم تفهمه (مفاهيم مهمتك بس)
- الفرق بين GA (Global Search) وMA (GA + Local Search).
- Local Search وNeighborhood وHill Climbing: خد حل، جرّب تعديلات صغيرة، احتفظ بالأحسن لو حسّن الـ Fitness، كرر عدد محدود.
- الـ Local Search **مش Mutation عشوائي**: تعديلات مدروسة بتفهم قواعد اللعبة. الـ Operators: Degree Repair، Crossing Repair، Connectivity Repair، Bridge Reallocation.
- نفس الـ Chromosome ونفس الـ Fitness بتوع GA (من Rovan).
- React + TypeScript + Vite، وSVG للرسم، وإن الـ JSON اللي بتطلعه الواجهة لازم يطابق Data Model.

## 2) مهامك في Sprint 1
| Task | المهمة | الملفات | Branch | اختبارها |
|---|---|---|---|---|
| S1-10 | Memetic Algorithm & Local Search Design | `docs/MA_OVERVIEW.md` و`docs/MA_DESIGN.md` | `docs/ma-design` | مثال يدوي `[1,0,1,1]` ← `[1,1,1,1]` |
| S1-11 | Basic Puzzle Editor UI | `frontend/` و`docs/UI_DATA_SPEC.md` | `feature/puzzle-editor` | `cd frontend && npm test` + اختبار يدوي |

الوصف الكامل والـ Acceptance Criteria لكل مهمة في **كارت Trello** بتاعها. اقراه بالكامل قبل ما تبدأ.

## 3) جدولك اليومي
| Day | المطلوب |
|---|---|
| Day 1 | ادرس MA وLocal Search، واكتب `docs/MA_OVERVIEW.md` + Wireframe بسيط للواجهة |
| Day 2 | `docs/UI_DATA_SPEC.md` (الـ JSON اللي الواجهة بتطلعه) |
| Day 3 | `docs/MA_DESIGN.md` + Scaffold الواجهة وبداية Puzzle Editor |
| Day 4 | إكمال الواجهة + Pseudocode الـ Local Search |
| Day 5 | عرض الواجهة وشرح الـ Local Search في الـ Sprint Review |

## 4) تفاصيل كل مهمة
**S1-10 MA Design (تصميم بس):** ازاي GA هي الأساس، Hill Climbing، الـ 4 Operators بشروطهم، **إمتى** بنطبق Local Search (بعد Mutation؟ على الأحسن بس؟ نسبة من الـ Population؟ واكتب السبب)، حد أقصى لخطوات الـ Local Search، ازاي بنقيس التحسن، Pseudocode، ومثال P1: `[1,0,1,1]` (Penalty 2) بتتحول بـ Degree Repair لـ `[1,1,1,1]` (Penalty 0).

**S1-11 Puzzle Editor (إدخال وعرض بس، من غير ربط بخوارزمية):** إدخال Rows وColumns، الضغط على خلية يضيف جزيرة، رقمها من 1 لـ 8، تعديل وحذف، عرض الجزر في أماكنها، اختيار Algorithm (عرض بس)، مكان للنتيجة، ورفض المدخلات الغلط (نفس الخلية، برا الشبكة). الـ JSON الناتج: `{rows, cols, islands:[{id,row,col,required_bridges}]}` بالحرف. من غير Animation أو تصميم متقدم.
## 5) اللي هتسلمه بالظبط
- `docs/MA_OVERVIEW.md` و`docs/MA_DESIGN.md` و`docs/UI_DATA_SPEC.md`
- واجهة Puzzle Editor شغالة والـ JSON مطابق للـ Data Model (جرّب P1)
- عرض في الـ Sprint Review

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
1. إيه الفرق بين Local Search وMutation؟
2. إيه الـ 4 Operators وإيه شرط كل واحد؟
3. إمتى بنطبق Local Search؟ وليه اخترت كده؟
4. إيه شكل الـ JSON اللي الواجهة بتطلعه لـ P1؟
5. إيه اللي لازم الواجهة ترفضه؟

## 9) مين بيراجعك ومين مستنيك
- **بيراجعك:** Mostafa (وRovan للتوافق مع تصميم GA في MA).
- **مستنيك:** Sprint 2 (ربط الواجهة بـ Backtracking) وSprint 3 (تنفيذ MA والواجهة لـ GA وMA).

## 10) القواعد
- كل الشغل على branch بتاعتك، وبـ PR على `develop`. **ممنوع Merge ذاتي.** Mostafa هو الوحيد اللي بيراجع ويعمل Merge.
- مفيش كود قبل اعتماد الـ Data Model (S1-02، نهاية Day 2). قبلها: دراسة وSpecs بس.
- الـ Data Model بالحرف: `required_bridges`, `from`, `to`, `orientation`, `bridge_counts`.
- الـ AI بيكتب الكود والمسؤولية عليك: لازم تفهمه، وتشغّل الاختبارات، وتقدر تشرحه (انظر [AI_WORKFLOW.md](../AI_WORKFLOW.md)).
- أي تغيير في الـ Data Model بيروح لـ Mostafa الأول.

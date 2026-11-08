# Monzer: Core Graph Engine

**الدور:** Core Graph Engine (مولّد الجسور المحتملة + اكتشاف التقاطعات)

إنت المسؤول عن **أساس المشروع**: تحديد الجسور المسموح بيها بين الجزر، واكتشاف الجسور المتقاطعة. كل الخوارزميات (Backtracking وGA وMA) هتبني على شغلك، وأي خطأ فيه هيأثر عليهم كلهم.

## 1) اللي لازم تفهمه (مفاهيم مهمتك بس)
- Graph: Vertex = جزيرة، Edge = جسر محتمل، Degree.
- الجسر المحتمل: **أفقي أو رأسي بس**، بين **أقرب جزيرتين** في نفس الصف/العمود، **من غير جزيرة بينهم** (A–B وB–C مسموح، A–C لأ لو B بينهم).
- الإحداثيات: `row` للأسفل، `col` لليمين، **بتبدأ من 0**.
- قاعدة التقاطع الصارمة: أفقي في الصف r بين c1<c2، ورأسي في العمود c بين r1<r2: `c1 < c < c2` و`r1 < r < r2`. الجسور اللي بتتلاقى عند جزيرة مش تقاطع.
- الجسر اللي عدده 0 مش موجود، والجسر المزدوج بيتحسب **تقاطع واحد**.
- ترتيب الـ Candidate Bridges ثابت (قاعدته في DATA_MODEL.md) لأن GA هتحوّله لـ Genes.

## 2) مهامك في Sprint 1
| Task | المهمة | الملفات | Branch | اختبارها |
|---|---|---|---|---|
| S1-02 | مراجعة واعتماد Data Model (مع Mostafa) | `docs/DATA_MODEL.md` | `docs/data-model` | مراجعة |
| S1-03 | Candidate Edge Generator | `core/candidate_generator.py` | `feature/candidate-generator` | `python -m pytest tests/test_candidate_generator.py -q` |
| S1-05 | Crossing Detection | `core/crossing_detector.py` | `feature/crossing-detector` | `python -m pytest tests/test_crossing_detector.py -q` |

الوصف الكامل والـ Acceptance Criteria لكل مهمة في **كارت Trello** بتاعها. اقراه بالكامل قبل ما تبدأ.

## 3) جدولك اليومي
| Day | المطلوب |
|---|---|
| Day 1 | ادرس Graph + اكتشاف التقاطع، واكتب `docs/GRAPH_ENGINE_NOTES.md` |
| Day 2 | `docs/CANDIDATE_EDGES_SPEC.md` + مراجعة Data Model مع Mostafa (S1-02). **لسه مفيش كود** |
| Day 3 | كود S1-03 وS1-05 (بالـ AI بعد Spec وPseudocode) + اختباراتهم |
| Day 4 | تصليح ملاحظات Mostafa وEbrahim، ونسخة نهائية |
| Day 5 | Acceptance + عرض شغلك في الـ Sprint Review |

## 4) تفاصيل كل مهمة
**S1-03 Candidate Edge Generator:** `generate_candidate_edges(islands)` ترجع كل الجسور المحتملة.
- رتّب الجزر بـ `(row, col)`. لكل جزيرة بالترتيب: جسرها **الأفقي ناحية اليمين** ثم **الرأسي ناحية الأسفل**. الترقيم E1, E2, ...
- كل زوج مرة واحدة. `from` = الأعلى/اليسار. نفس الجزر بأي ترتيب إدخال = نفس النتيجة.
- Puzzle P1 لازم تدي بالظبط: E1=A–B أفقي، E2=A–C رأسي، E3=B–D رأسي، E4=C–D أفقي.

**S1-05 Crossing Detection:** `detect_crossings(islands, edges, solution)` و`get_crossing_pairs(islands, edges)`.
- `detect_crossings`: أزواج الـ Edges اللي بتتقاطع **فعليًا** (عدد الاتنين أكبر من 0).
- `get_crossing_pairs`: كل الأزواج اللي **لو اتحطوا مع بعض هيتقاطعوا** (بتتحسب مرة واحدة، وهتتستخدم في Sprint 2 و3).
- مثال P2: E1 رأسي C–D بيقطع E2 أفقي A–B عند (1,2).
## 5) اللي هتسلمه بالظبط
- `docs/GRAPH_ENGINE_NOTES.md` (Day 1) و`docs/CANDIDATE_EDGES_SPEC.md` (Day 2)
- `core/candidate_generator.py` + اختباراته بتعدّي (علامة xfail اتشالت)
- `core/crossing_detector.py` + اختباراته بتعدّي
- PR لكل مهمة (مش PR واحد كبير) + شرح مختصر لطريقة عمل كل دالة في وصف الـ PR

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
1. إمتى جزيرتين ينفع يتوصلوا بجسر؟ وإمتى لأ؟
2. ليه A–C مش Candidate Bridge لو B بينهم؟
3. إيه شرط التقاطع بالإحداثيات؟ وليه المقارنة صارمة (`<` مش `<=`)؟
4. جسرين بيتقابلوا عند جزيرة: تقاطع ولا لأ؟ ولية؟
5. جسر مزدوج بيقطع جسر تاني: كام تقاطع؟
6. ليه ترتيب الـ Edges لازم يبقى ثابت؟

## 9) مين بيراجعك ومين مستنيك
- **بيراجعك:** Mostafa.
- **مستنيك:** Ebrahim (الـ Validators بتتجرب على Edges حقيقية. بلّغه أول ما S1-03 تتدمج، وهو ممكن يبدأ على Test Data ثابتة)، Rovan (الـ Chromosome بيتبني على ترتيب الـ Edges)، Mostafa (الـ Integration).

## 10) القواعد
- كل الشغل على branch بتاعتك، وبـ PR على `develop`. **ممنوع Merge ذاتي.** Mostafa هو الوحيد اللي بيراجع ويعمل Merge.
- مفيش كود قبل اعتماد الـ Data Model (S1-02، نهاية Day 2). قبلها: دراسة وSpecs بس.
- الـ Data Model بالحرف: `required_bridges`, `from`, `to`, `orientation`, `bridge_counts`.
- الـ AI بيكتب الكود والمسؤولية عليك: لازم تفهمه، وتشغّل الاختبارات، وتقدر تشرحه (انظر [AI_WORKFLOW.md](../AI_WORKFLOW.md)).
- أي تغيير في الـ Data Model بيروح لـ Mostafa الأول.

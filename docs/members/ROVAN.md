# Rovan: Genetic Algorithm

**الدور:** Genetic Algorithm (تصميم Sprint 1، تنفيذ Sprint 3)

إنت المسؤول عن الخوارزمية التطورية. في Sprint 1 بتفهمها وبتكتب تصميمها كامل على الورق (Chromosome وFitness...)، والتنفيذ في Sprint 3. الـ Memetic Algorithm هتتبني فوق شغلك.

## 1) اللي لازم تفهمه (مفاهيم مهمتك بس)
- Population وChromosome وGene وFitness وSelection وCrossover وMutation وElitism.
- الـ Chromosome عندنا: Array من 0/1/2 بنفس طول وترتيب الـ Candidate Bridges (index i ↔ E(i+1)).
- Fitness = Penalty: `W1*Degree + W2*Crossings + W3*(Components-1)`. **الحساب بيستخدم دوال `core/`، مش منطق جديد.**
- Penalty = 0 **مش كفاية** نعلن بيه إن الحل صح. لازم `validate_solution`.
- GA احتمالية: لو فشلت الرسالة `No Valid Solution Found Within Search Limits` (مش 'مستحيلة').
- Premature Convergence وElitism.

## 2) مهامك في Sprint 1
| Task | المهمة | الملفات | Branch | اختبارها |
|---|---|---|---|---|
| S1-09 | Genetic Algorithm Design | `docs/GA_OVERVIEW.md` و`docs/CHROMOSOME_SPEC.md` و`docs/GA_DESIGN.md` | `docs/ga-design` | الحساب اليدوي على P1 |

الوصف الكامل والـ Acceptance Criteria لكل مهمة في **كارت Trello** بتاعها. اقراه بالكامل قبل ما تبدأ.

## 3) جدولك اليومي
| Day | المطلوب |
|---|---|
| Day 1 | ادرس GA (6 مفاهيم) واكتب `docs/GA_OVERVIEW.md` |
| Day 2 | `docs/CHROMOSOME_SPEC.md` + مراجعة Data Model. **مفيش كود** |
| Day 3 | مسودة `docs/GA_DESIGN.md` مع الـ Fitness والمثال اليدوي |
| Day 4 | التصميم النهائي + راجعه مع Febronia (MA مبنية عليه) |
| Day 5 | عرض الـ Chromosome والـ Fitness على مثال في الـ Sprint Review |

## 4) تفاصيل كل مهمة
**S1-09 GA Design (تصميم بس، من غير كود):** اكتب القرارات دي بقيم واضحة: Chromosome، حجم الـ Population، Fitness (المعادلة والأوزان قابلة للتعديل)، Selection (Tournament)، Crossover (Uniform) + Rate، Mutation (غيّر Gene لقيمة تانية من 0/1/2) + Rate، Elitism، Termination، والإحصائيات (Best/Avg Fitness، الأجيال، الوقت).

**الحساب اليدوي على P1 (أوزان = 1)، لازم حسابك يطابق:**
| Chromosome | Degree | Crossings | Components | Penalty |
|---|---|---|---|---|
| `[1,1,1,1]` | 0 | 0 | 1 | **0** |
| `[1,0,1,1]` | 2 | 0 | 1 | **2** |
| `[2,0,0,2]` | 0 | 0 | 2 | **1** |
| `[2,2,0,0]` | 4 | 0 | 2 | **5** |
## 5) اللي هتسلمه بالظبط
- `docs/GA_OVERVIEW.md` و`docs/CHROMOSOME_SPEC.md` و`docs/GA_DESIGN.md` بكل الأقسام والمثال اليدوي
- عرض 3 دقايق في الـ Sprint Review

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
1. إيه شكل الـ Chromosome لـ P1؟ وليه طوله 4؟
2. إيه مكونات الـ Fitness؟ وليه الاتصال جزء منها؟
3. ليه `[2,0,0,2]` Penalty = 1 مع إن الـ Degree سليم؟
4. إيه الفرق بين Crossover وMutation؟ وإيه خطر Mutation Rate العالي؟
5. ليه Penalty = 0 مش كفاية نقول 'Solution Found'؟
6. ليه GA مينفعش تقول 'اللغز مستحيل'؟

## 9) مين بيراجعك ومين مستنيك
- **بيراجعك:** Mostafa (وهتنسّق مع Febronia لما ينضم، MA مبنية على GA).
- **مستنيك:** Sprint 3 (تنفيذ GA) وتصميم MA (S1-10).
- **لو خلصت بدري:** دي مهمة تصميم، فاستخدم الوقت في: حساب Fitness يدوي لأمثلة إضافية، ومراجعة تصميم Backtracking (S1-08) عشان تفهم الصورة الكاملة. **مفيش كود GA في Sprint 1.**

## 10) القواعد
- كل الشغل على branch بتاعتك، وبـ PR على `develop`. **ممنوع Merge ذاتي.** Mostafa هو الوحيد اللي بيراجع ويعمل Merge.
- مفيش كود قبل اعتماد الـ Data Model (S1-02، نهاية Day 2). قبلها: دراسة وSpecs بس.
- الـ Data Model بالحرف: `required_bridges`, `from`, `to`, `orientation`, `bridge_counts`.
- الـ AI بيكتب الكود والمسؤولية عليك: لازم تفهمه، وتشغّل الاختبارات، وتقدر تشرحه (انظر [AI_WORKFLOW.md](../AI_WORKFLOW.md)).
- أي تغيير في الـ Data Model بيروح لـ Mostafa الأول.

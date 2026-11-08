# Hashiwokakero (Bridges) Puzzle Solver

مشروع فريق (5 أعضاء) لمادة AI310 / CS361 — Fall 2026. بنحل لعبة **Hashiwokakero** بتلات خوارزميات:
**Backtracking** (دقيقة) و**Genetic Algorithm** و**Memetic Algorithm** (GA + Local Search)،
مع **Graph Theory** للتحقق من التقاطعات والاتصال، وواجهة بتدخّل فيها اللغز وتختار الخوارزمية وتشوف الحل.

> الوقت المتاح: **4 أسابيع** (4 Sprints). الهدف: Core شغال وكل الفريق فاهمه، مش الكمال.

## 👋 عضو جديد في الفريق؟ ابدأ من هنا
1. [docs/START_HERE.md](docs/START_HERE.md): إحنا بنشتغل على إيه والمشكلة اللي بنحلها وكل اللي لازم تعرفه.
2. [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md): ازاي تعمل branch، تحدّث شغلك، تفتح PR، وتستقبل المراجعة.
3. دليلك الشخصي: [Monzer](docs/members/MONZER.md) • [Ebrahim](docs/members/EBRAHIM.md) • [Rovan](docs/members/ROVAN.md) • [Febronia](docs/members/FEBRONIA.md) • [Mostafa (القائد)](docs/members/MOSTAFA.md)
4. كارت مهمتك في Trello (فيه الوصف الكامل والـ Acceptance Criteria).

## قواعد اللعبة (باختصار)
1. كل جزيرة عليها رقم = عدد الجسور اللي لازم تتوصل بيها بالظبط (الجسر المزدوج بيتحسب 2 على الجزيرتين).
2. الجسور أفقية أو رأسية بس، ومن أقرب جزيرة لأقرب جزيرة في نفس الصف/العمود من غير جزيرة بينهم.
3. أقصى عدد بين أي جزيرتين = جسرين.
4. ممنوع جسرين يتقاطعوا.
5. كل الجزر لازم تبقى شبكة واحدة متصلة.

التفاصيل الكاملة: [docs/PROJECT_REQUIREMENTS.md](docs/PROJECT_REQUIREMENTS.md)

## الـ Stack
| الجزء | التقنية |
|---|---|
| Core + Algorithms | Python 3.11+ |
| API | FastAPI + Pydantic |
| Tests | Pytest (backend)، Vitest (frontend) |
| Frontend | React + TypeScript + Vite، والرسم بـ SVG |
| Version control | Git + GitHub (الكود)، Trello (المهام) |

مفيش Database ولا Authentication ولا ML ولا Deployment (خارج الـ Scope). التفاصيل: [docs/RISKS_AND_SCOPE.md](docs/RISKS_AND_SCOPE.md)

## الهيكل
```
core/          محرك القواعد المشترك: candidate edges, degree, crossings, connectivity, validator
algorithms/    backtracking.py, genetic.py, memetic.py  (كلهم بيستخدموا core بس)
api/           FastAPI (/health, /algorithms, /validate, /solve)
frontend/      React + TypeScript + Vite (Puzzle Editor + Visualization)
tests/         اختبارات + fixtures مشتركة (P1, P2) في tests/helpers.py
docs/          المتطلبات، Data Model، المعمارية، الخطة، مستندات التصميم
scripts/       setup_github.sh (إنشاء الـ repo والـ branches والـ labels)
.github/       PR template, Issue templates, CI
```

## تشغيل سريع
```bash
# Backend
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\activate
make install            # أو: pip install -r requirements.txt
make test               # كل الاختبارات
make status             # مين لسه stub (XFAIL) ومين خلص (XPASS)
make api                # http://127.0.0.1:8000/docs

# Frontend
make frontend-install
make frontend-dev
```
**الاختبارات المكتوبة مسبقًا:** كل Module في `core/` ليه ملف اختبار جاهز عليه علامة `xfail`.
لما تخلص تنفيذ الـ Module بتاعك: شغّل الاختبارات، ولما تعدّي **امسح سطر `pytestmark = pytest.mark.xfail(...)`** من ملف الاختبار.

## الفريق والمسؤوليات
| العضو | الدور | الـ Modules |
|---|---|---|
| Mostafa | Project Manager & Tech Lead | Data Model، Architecture، Integration، Code Review |
| Monzer | Core Graph Engine | `core/candidate_generator.py`، `core/crossing_detector.py` |
| Ebrahim | Validation & Backtracking | `core/degree_validator.py`، `core/connectivity_checker.py`، `core/solution_validator.py`، `algorithms/backtracking.py` |
| Rovan | Genetic Algorithm | `algorithms/genetic.py` + تصميم GA |
| Febronia | Memetic + Frontend | `algorithms/memetic.py`، `frontend/` |

التفاصيل: [docs/TEAM_AND_ROLES.md](docs/TEAM_AND_ROLES.md)

## قواعد الشغل (لازم الكل يلتزم)
1. **ممنوع كود قبل اعتماد الـ Data Model** (S1-02).
2. **One Module, One Owner.**
3. **ممنوع Merge ذاتي**، كل PR يتراجع من Mostafa.
4. **ممنوع Merge من غير فهم الكود + Tests + تجربة فعلية** (الـ AI بيكتب الكود، المسؤولية علينا).
5. **أي Algorithm ممنوع تعلن "Solution Found" قبل ما `validate_solution` يوافق.**
6. ما نوسّعش الـ Scope: هل غيابها بيمنعنا من المتطلبات الأساسية؟ لو لأ، تتأجل.

دليل المساهمة: [CONTRIBUTING.md](CONTRIBUTING.md) • دليل القائد: [docs/LEADER_GUIDE.md](docs/LEADER_GUIDE.md) • الخطة: [docs/SPRINT_PLAN.md](docs/SPRINT_PLAN.md) • فهرس المستندات: [docs/README.md](docs/README.md)

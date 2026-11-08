# الفريق والمسؤوليات

| العضو | الدور | Owner لـ | المطلوب منه تعلمه (Sprint 1) |
|---|---|---|---|
| **Mostafa** (Leader) | Project Manager + Tech Lead + Code Review | Data Model، Architecture، Integration | Problem Modeling + Software Architecture + Git Workflow (≈3 ساعات) |
| **Monzer** | Core Graph Engine | `candidate_generator.py`، `crossing_detector.py` | Graph Representation + Crossing Detection + BFS/DFS (≈4 ساعات) |
| **Ebrahim** | Validation & Backtracking | `degree_validator.py`، `connectivity_checker.py`، `solution_validator.py`، `backtracking.py` | Degree + Connectivity + Backtracking Basics (≈4 ساعات) |
| **Rovan** | Genetic Algorithm | `genetic.py` + تصميم GA | GA Fundamentals (≈4 ساعات) |
| **Febronia**  | Memetic + Frontend | `memetic.py`، `frontend/` | Local Search + Hill Climbing + SVG Basics (≈4 ساعات) |

بالإضافة لجلسة مشتركة لكل الفريق لفهم قواعد اللعبة، وحوالي 14 ساعة تعلم مشترك موزعة على أول أسبوعين: قواعد اللعبة (2) • Graph Basics (3) • BFS/DFS (2) • Backtracking Overview (2) • GA Overview (3) • MA Overview (2).

## مبادئ
- **كل عضو Owner لجزء محدد**، لكن مفيش جزء يفهمه شخص واحد بس. لازم شخص تاني على الأقل يقدر يشرح ويراجع كل Module.
- **مفيش حد مسؤول عن جزء مش فاهمه**، حتى لو الـ AI كتب 100% من الكود: لازم يفهم المدخلات والمخرجات والـ Edge Cases.
- **Testing مسؤولية الكل.**
- **One Module, One Owner:** مفيش شخصين يعدلوا نفس الملفات في نفس الوقت.

## مصفوفة مستوى المعرفة المطلوب
| الموضوع | Mostafa | Monzer | Ebrahim | Rovan | Febronia |
|---|---|---|---|---|---|
| Problem Modeling | متقدم | متقدم | متوسط | متوسط | متوسط |
| Graph Theory | متوسط | متقدم | متوسط | متوسط | متوسط |
| Backtracking | متوسط | متوسط | متقدم | أساسي | أساسي |
| Genetic Algorithm | متوسط | متوسط | أساسي | متقدم | متوسط |
| Memetic Algorithm | متوسط | متوسط | أساسي | متقدم | متقدم |
| Architecture | متقدم | متوسط | أساسي | أساسي | أساسي |
| Testing | متقدم | متقدم | متقدم | متقدم | متقدم |
| Visualization | متوسط | أساسي | أساسي | أساسي | متقدم |

## مصفوفة المراجعة
| الـ Module | Owner | Reviewer |
|---|---|---|
| Data Model | Mostafa + Monzer | الفريق |
| Candidate Generator / Crossing Detector | Monzer | Mostafa |
| Degree / Connectivity | Ebrahim | Mostafa |
| Final Validator | Ebrahim | Mostafa + Monzer |
| Backtracking | Ebrahim | Mostafa |
| GA | Rovan | Mostafa |
| MA | Febronia | Mostafa + Rovan |
| Frontend | Febronia | Mostafa |

> ملاحظة: `.github/CODEOWNERS` متجهّز بس متعلّق (commented). لما كل عضو يديك الـ GitHub username بتاعه، فعّله.

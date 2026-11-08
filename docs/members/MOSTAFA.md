# Mostafa: Project Manager & Tech Lead

**الدور:** القائد، الوحيد المسؤول عن **مراجعة الكود والـ Merge**. تفاصيل الإدارة والمراجعة في [../LEADER_GUIDE.md](../LEADER_GUIDE.md).

## مهامك في Sprint 1
| Task | المهمة | الملفات | Branch |
|---|---|---|---|
| S1-01 ✅ | Requirements & Rule Alignment | `docs/PROJECT_REQUIREMENTS.md` | خلصت |
| S1-02 | اعتماد Data Model (مع Monzer) | `docs/DATA_MODEL.md` | `docs/data-model` |
| S1-12 | Integration & Test Cases | `tests/`، تقرير Integration | `feature/core-integration-tests` |
| متابعة | S1-10 وS1-11 لحد ما Febronia ينضم | `docs/MA_*`, `frontend/` | — |

## جدولك اليومي
| Day | المطلوب |
|---|---|
| Day 1 | Setup + Kickoff + Requirements (خلص) |
| Day 2 | اجتماع Design Review، استلام الـ 4 Specs، اعتماد وتجميد Data Model، **إعلان "Data Model Frozen"** |
| Day 3 | مراجعة أول PRs، تجهيز Test Cases مشتركة |
| Day 4 | دمج بالترتيب، Integration Test، تجميع المشاكل |
| Day 5 | Sprint Review، تحديد حالة كل Task (Accepted / Needs Fixes / Blocked)، ودمج `develop` في `main` لو Sprint 1 اتقبل |

## أهم 3 حاجات
1. **ماتبقاش Bottleneck:** ثبّت الـ Interfaces مرة واحدة، وراجع الـ PRs مرتين في اليوم على الأقل.
2. **متقبلش كود لمجرد إنه اشتغل:** اتأكد إن صاحبه فاهمه (اسأله يشرحه).
3. **ادمج كل يوم:** مستنيش آخر الـ Sprint.

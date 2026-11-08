# Testing Strategy

## المبدأ
مفيش Algorithm بتعلن "Solution Found" إلا بعد `validate_solution`. وبنقارن نتائج GA وMA بحلول Backtracking على Puzzles معروفة الحل.

## الاختبارات الجاهزة (Sprint 1)
| الملف | يغطي | المسؤول |
|---|---|---|
| `tests/test_candidate_generator.py` | S1-03 | Monzer |
| `tests/test_degree_validator.py` | S1-04 | Ebrahim |
| `tests/test_crossing_detector.py` | S1-05 | Monzer |
| `tests/test_connectivity.py` | S1-06 | Ebrahim |
| `tests/test_solution_validator.py` | S1-07 | Ebrahim |
| `tests/test_fixtures.py` + `tests/test_api.py` | سلامة الـ fixtures والـ API | دايمًا شغالة |

الاختبارات متعلّمة `xfail` لحد ما الـ Module يتنفذ. **لما تخلص امسح سطر `pytestmark`.** `make status` بيوريك الحالة.

## Puzzles مرجعية (في `tests/helpers.py`)
- **P1:** شبكة 3×3، 4 جزر رقم 2 في الأركان. الحل الصحيح الوحيد `[1,1,1,1]`. الحلول `[2,0,0,2]` و`[0,2,2,0]` بتحقق الأرقام لكن الشبكة مقسومة.
- **P2:** مثال تقاطع: `E1` رأسي يقطع `E2` أفقي عند (1,2).

## Fitness يدوي على P1 (أوزان = 1)
| Chromosome | Degree | Crossings | Components | Penalty |
|---|---|---|---|---|
| `[1,1,1,1]` | 0 | 0 | 1 | **0** |
| `[1,0,1,1]` | 2 | 0 | 1 | **2** |
| `[2,0,0,2]` | 0 | 0 | 2 | **1** |
| `[2,2,0,0]` | 4 | 0 | 2 | **5** |

## Sprint 4: Puzzles للاختبار النهائي
| Puzzle | الهدف |
|---|---|
| Easy | الحل الأساسي |
| Double Bridges | الجسور المزدوجة |
| Crossing Case | اكتشاف التقاطعات |
| Disconnected Case | اكتشاف الاتصال |
| Difficult | الأداء |
بالإضافة: Impossible (مجموع فردي) • Duplicate Islands • Out of Bounds • Invalid Island Value.

## GA وMA
- شغّل كل Puzzle بأكتر من **Random Seed** وسجّل: هل لقت حل صحيح؟ الوقت، عدد الأجيال، Best Fitness، عدد مرات الفشل، نسبة النجاح.
- قارن MA بـ GA على نفس الـ Puzzle وبنفس الإعدادات عشان نقول فعلًا هل Local Search بتحسّن.
- فشل GA/MA = `No Valid Solution Found Within Search Limits`، **مش** "مستحيلة".

## Backtracking
سجّل `execution_time_s` و`explored_states` و`backtracks`. "No Solution Exists" مسموحة بس بعد بحث كامل.

# System Architecture

## الفكرة
3 خوارزميات مختلفة بتحل **نفس المشكلة** فوق **محرك قواعد واحد مشترك**. الاختلاف بينهم في طريقة البحث بس، مش في فهم القواعد.

```
        المستخدم
           │
   Frontend (React + TS)
           │  JSON
      API (FastAPI)
           │
   ┌───────┼────────┐
Backtracking  GA    MA          algorithms/
   └───────┼────────┘
     Shared Core Engine          core/
 ┌─────────┼──────────┐
Candidate  Degree   Crossing   Connectivity   Final
 Edges    Validator Detector    Checker      Validator
```

## المسؤوليات
| الطبقة | الملف/المجلد | المسؤولية |
|---|---|---|
| Frontend | `frontend/` | إدخال Puzzle، اختيار Algorithm، عرض الشبكة والحل والنتيجة |
| API | `api/main.py` | استقبال الطلب، التحقق من الشكل (Pydantic)، استدعاء الـ Solver |
| Algorithms | `algorithms/` | البحث عن حل. **ممنوع** منطق قواعد خاص بيهم |
| Core | `core/` | القواعد: Candidate Edges، Degree، Crossings، Connectivity، Validator |

## قواعد معمارية (مش للنقاش)
1. **Single rule engine:** كل Algorithm بتنادي دوال `core/` فقط. مفيش حد يعيد كتابة منطق التقاطع أو الاتصال.
2. **Single judge:** `validate_solution` هو الحَكَم الوحيد. أي Solver ممنوع يرجّع `Solution Found` قبل موافقته.
3. **Shared data model:** `docs/DATA_MODEL.md` هو المرجع. الـ Chromosome بيتبني على ترتيب الـ Candidate Bridges.
4. **Stateless API:** مفيش Database. الحالة في الذاكرة أثناء التشغيل.
5. **الشغل الثقيل:** GA/MA بتستهلك CPU، فيتشغّلوا بعيد عن حلقة استقبال الطلبات لو احتجنا Progress Updates (WebSocket أو SSE، قرار Sprint 3 و4).

## API Contract (مسودة)
| Method | Path | الغرض |
|---|---|---|
| GET | `/health` | `{"status":"ok"}` |
| GET | `/algorithms` | `["backtracking","genetic","memetic"]` |
| POST | `/validate` | body: `{puzzle, solution}` ← Validation Report |
| POST | `/solve` | body: `{puzzle, algorithm, config?}` ← `{status, solution, stats}` |

`/solve` و`/validate` بيرجّعوا **501** لحد ما الـ Modules تتنفذ.

شكل ناتج `/solve`:
```json
{ "status": "Solution Found",
  "solution": { "bridge_counts": { "E1": 1 } },
  "stats": { "execution_time_s": 0.8, "explored_states": 120, "backtracks": 35 } }
```
- Backtracking stats: `execution_time_s`, `explored_states`, `backtracks`.
- GA/MA stats: `execution_time_s`, `generations`, `best_fitness`, `avg_fitness`، وفي MA كمان أثر الـ Local Search.

## الـ Stack ولية
| الاختيار | السبب |
|---|---|
| Python للخوارزميات | تنفيذ Backtracking وGA وGraph بسهولة |
| FastAPI + Pydantic | API سريع والتحقق من المدخلات |
| React + TypeScript + Vite | واجهة تفاعلية وأخطاء أقل في التعامل مع البيانات |
| SVG | الجزر دواير والجسور خطوط، وسهل نحدّثها مع كل خطوة |
| Pytest / Vitest | اختبار كل Constraint وكل Algorithm منفصل |

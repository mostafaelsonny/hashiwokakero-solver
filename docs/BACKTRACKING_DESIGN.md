# BACKTRACKING DESIGN

- **المسؤول:** Ebrahim
- **المهمة:** S1-08 (كارت Trello فيه الوصف الكامل والـ Acceptance Criteria)
- **الموعد:** Day 4 من Sprint 1
- **الحالة:** مكتمل ✅

---

## 1. الفكرة بكلامك

الـ Backtracking هو خوارزمية بحث شاملة (Exhaustive Search) بتجرب كل الاحتمالات الممكنة لأعداد الجسور واحد واحد، وبتلغي (تـ Prune) أي مسار بيتبين إنه غلط قبل ما نكمل فيه.

تخيل إننا بنملا جدول سودوكو: بنحاول نحط رقم في كل خانة، ولو حسينا إن الرقم ده هيعمل تعارض، برجع خطوة ونجرب رقم تاني. الفرق هنا إن كل "خانة" هي **edge (جسر محتمل)** في اللغز، والقيم الممكنة هي `{0, 1, 2}` (عدد الجسور على الـ edge ده).

الخوارزمية بتشتغل كالآتي:
1. رتّب كل الـ candidate edges ترتيب ثابت (E1, E2, E3, ...).
2. ابدأ من E1، جرب القيمة 0، افحص جزئياً، لو ماشي انتقل لـ E2.
3. لو لقينا تعارض في أي وقت، ارجع خطوة (Backtrack) وجرب القيمة الجاية.
4. لو وصلنا للـ edge الأخير وكل شيء صح، اعمل الفحص النهائي.
5. لو مفيش solution، ارجع No Solution Exists.

---

## 2. State

الحالة في أي لحظة معينة أثناء البحث بتتمثل في:

```python
state = {
    "edge_index": int,          # إيه الـ edge اللي بنحله دلوقتي (0 to N-1)
    "bridge_counts": dict,      # {edge_id: 0|1|2} للـ edges اللي اخترنا قيمها لحد دلوقتي
    "stats": {
        "nodes_explored": int,  # عدد الـ nodes اللي زرناها
        "backtracks": int,      # عدد مرات الرجوع
        "pruned": int,          # عدد مرات الـ pruning
    }
}
```

**المتغيرات الثابتة** (بتتعمل مرة واحدة قبل البحث):
```python
islands   = puzzle["islands"]          # قائمة الجزر
edges     = generate_candidate_edges(islands)  # S1-03: كل الجسور الممكنة
N         = len(edges)                 # عدد الـ candidate edges
```

---

## 3. ترتيب المتغيرات

نستخدم **الترتيب الكانوني (Canonical Order)** — نفس الترتيب اللي بيرجعه `generate_candidate_edges()` وهو:
- أولاً بـ `from` island (بالترتيب الأبجدي لـ id)
- ثم بـ `to` island
- الأفقي قبل الرأسي لو من نفس الجزيرة

الترتيب ده:
- **Deterministic**: نفس النتيجة دايماً
- **Reproducible**: قابل للاختبار
- **Compatible**: متوافق مع fixtures الـ tests (E1, E2, E3, E4 لـ P1)

> **لاحقاً في Sprint 2** ممكن نضيف ترتيب ذكي (MRV / Most Constrained Variable) لتسريع البحث.

---

## 4. الفحص بعد كل اختيار (Partial Validation) + Pruning بمثال رقمي

بعد ما بنختار قيمة لـ edge معين، بنعمل **Partial Validation** باستخدام:

```python
# S1-04: فحص الدرجات جزئياً
violations = check_degrees(islands, edges, partial_solution, mode="partial")
if violations:
    # Prune: الجزيرة دي عندها جسور أكتر من المطلوب
    backtrack()

# S1-05: فحص التقاطعات على الجسور اللي اخترناها لحد دلوقتي
crossings = detect_crossings(islands, edges, partial_solution)
if crossings:
    # Prune: فيه تقاطع → مستحيل يبقى solution صح
    backtrack()
```

**مثال رقمي على P1:**

P1: جزر A(0,0,2), B(0,2,2), C(2,0,2), D(2,2,2)
Edges: E1=A→B(H), E2=A→C(V), E3=B→D(V), E4=C→D(H)

| الخطوة | E1 | E2 | E3 | E4 | الحالة |
|--------|----|----|----|----|--------|
| 1 | 0 | - | - | - | A=0, partial OK |
| 2 | 0 | 0 | - | - | A=0, partial OK |
| 3 | 0 | 0 | 0 | - | A=0, B=0, C=0, partial OK |
| 4 | 0 | 0 | 0 | 0 | Final check → A≠2 → FAIL |
| 5 | 0 | 0 | 0 | 1 | Final check → A≠2 → FAIL |
| ... | ... | ... | ... | ... | ... |
| n | 1 | 1 | 1 | 1 | Final check → ✅ VALID |

**Pruning مثال:** لو جربنا E1=2, E2=2:
- A's degree = 4 > required 2 → **Prune فوراً!** ماحتاجش نكمل E3 و E4

---

## 5. الفحص النهائي

لما بنوصل لآخر edge (index = N-1) ونختار قيمته، بنعمل **Full Validation** عن طريق:

```python
report = validate_solution(puzzle, complete_solution)  # S1-07
if report["valid"]:
    return {"status": "Solution Found", "solution": complete_solution, "stats": stats}
```

الفحص النهائي بيتحقق من:
1. ✅ كل القيم في `{0, 1, 2}`
2. ✅ درجة كل جزيرة = `required_bridges` بالضبط (mode="final")
3. ✅ مفيش تقاطعات بين الجسور الموجودة
4. ✅ كل الجزر متصلة في مكوّن واحد (connected_components == 1)

---

## 6. شروط الإيقاف (No Solution Exists vs Search Limit Reached)

### No Solution Exists
- الـ DFS استنفد **كل** الاحتمالات الممكنة (backtracked من E0 بكل القيم) ومفيش solution.
- الـ Output: `{"status": "No Solution Exists", "solution": null, "stats": {...}}`

### Search Limit Reached
- وصلنا لحد أقصى لعدد الـ nodes المستكشفة (مثلاً `MAX_NODES = 1_000_000`).
- الـ Output: `{"status": "Search Limit Reached", "solution": null, "stats": {...}}`
- الغرض: نمنع الـ algorithm من الشغل إلى الأبد في puzzles كبيرة.

```python
MAX_NODES = 1_000_000  # قابل للتعديل من config

if stats["nodes_explored"] >= MAX_NODES:
    return {"status": "Search Limit Reached", "solution": null, "stats": stats}
```

---

## 7. الإحصائيات المسجلة

```python
stats = {
    "nodes_explored": int,   # كل node زرناها في شجرة البحث
    "backtracks": int,       # كل مرة بنرجع خطوة
    "pruned": int,           # كل مرة بنقطع فرع من غير ما نكمله
    "duration_ms": float,    # وقت التنفيذ بالميلي ثانية
}
```

هالإحصائيات بتتبعت الـ تلقائياً وبترجع جنب الـ solution في الـ response.

---

## 8. Pseudocode

```
function BACKTRACK(edge_index, bridge_counts, stats):
    stats.nodes_explored += 1

    if stats.nodes_explored >= MAX_NODES:
        return SEARCH_LIMIT_REACHED

    if edge_index == N:  # وصلنا لآخر edge
        report = validate_solution(puzzle, {bridge_counts})
        if report.valid:
            return SOLUTION_FOUND(bridge_counts)
        else:
            return FAIL

    edge = edges[edge_index]

    for value in [0, 1, 2]:
        bridge_counts[edge.id] = value
        partial_solution = {bridge_counts}

        # Partial pruning checks
        degree_violations = check_degrees(islands, edges, partial_solution, "partial")
        if degree_violations:
            stats.pruned += 1
            continue  # جرب القيمة الجاية

        crossings = detect_crossings(islands, edges, partial_solution)
        if crossings:
            stats.pruned += 1
            continue  # جرب القيمة الجاية

        # اكمل البحث
        result = BACKTRACK(edge_index + 1, bridge_counts, stats)
        if result != FAIL:
            return result

        stats.backtracks += 1

    # كل القيم فشلت → backtrack
    del bridge_counts[edge.id]
    return FAIL


# Main entry point
function solve_backtracking(puzzle, config=None):
    start_time = now()
    edges = generate_candidate_edges(puzzle.islands)
    stats = {nodes_explored: 0, backtracks: 0, pruned: 0}

    result = BACKTRACK(0, {}, stats)

    stats.duration_ms = (now() - start_time) * 1000

    if result == SOLUTION_FOUND:
        return {status: "Solution Found", solution: result.solution, stats: stats}
    elif result == SEARCH_LIMIT_REACHED:
        return {status: "Search Limit Reached", solution: null, stats: stats}
    else:
        return {status: "No Solution Exists", solution: null, stats: stats}
```

---

## 9. استخدام Core Engine

الـ Backtracking بيعتمد على 4 وحدات من الـ Core Engine:

| الوحدة | الملف | الاستخدام |
|--------|-------|-----------|
| `generate_candidate_edges` | `core/candidate_generator.py` | بنبني قائمة الـ edges مرة واحدة في البداية |
| `check_degrees` (partial) | `core/degree_validator.py` | Pruning أثناء البحث |
| `detect_crossings` | `core/crossing_detector.py` | Pruning أثناء البحث |
| `validate_solution` | `core/solution_validator.py` | الفحص النهائي |

```python
# في algorithms/backtracking.py
from core.candidate_generator import generate_candidate_edges
from core.degree_validator import check_degrees
from core.crossing_detector import detect_crossings
from core.solution_validator import validate_solution
```

**القاعدة الذهبية:** لا يقدر أي algorithm يرجع `"Solution Found"` إلا لو `validate_solution(...)[\"valid\"] is True`.

> **مهم:** `get_crossing_pairs()` ممكن يتحسب مرة واحدة قبل البحث للـ Performance، لأن الـ candidate crossings بتتغيرش.

---

## 10. Trace يدوي على P1 ينتهي بـ [1,1,1,1]

**P1 Puzzle:**
- Islands: A(0,0,2), B(0,2,2), C(2,0,2), D(2,2,2)
- Edges: E1=A→B(H), E2=A→C(V), E3=B→D(V), E4=C→D(H)
- الـ Solution الوحيدة الصحيحة: E1=1, E2=1, E3=1, E4=1

```
BACKTRACK(edge_index=0, bridge_counts={})
├── E1=0:
│   BACKTRACK(edge_index=1, bridge_counts={E1:0})
│   ├── E2=0:
│   │   BACKTRACK(edge_index=2, bridge_counts={E1:0, E2:0})
│   │   ├── E3=0: ...→ Final: A=0≠2 FAIL
│   │   ├── E3=1: ...→ Final: A=0≠2 FAIL
│   │   └── E3=2: check_degrees partial: B=2>2? No. ...→ Final: A=0≠2 FAIL
│   ├── E2=1:
│   │   BACKTRACK(edge_index=2, bridge_counts={E1:0, E2:1})
│   │   ├── E3=0: ...→ Final: A=1≠2 FAIL
│   │   ├── E3=1: ...→ Final: A=1≠2 FAIL
│   │   └── E3=2: check_degrees partial: B=2≤2 OK, D=2 so check partial OK
│   │             BACKTRACK(3, {E1:0,E2:1,E3:2})
│   │             ├── E4=0: Final: A=1≠2 FAIL
│   │             ├── E4=1: Final: A=1≠2 FAIL
│   │             └── E4=2: Final: A=1≠2 FAIL → backtrack
│   └── E2=2:
│       check_degrees: A=2 OK partial
│       BACKTRACK(2, {E1:0, E2:2})
│       ├── E3=0: ...→ Final: B=0≠2, D=... FAIL
│       ├── E3=1: ...→ Final: B=1≠2 FAIL
│       └── E3=2: check_degrees: B=2 OK, D=2 partial OK
│               BACKTRACK(3, {E1:0,E2:2,E3:2})
│               ├── E4=0: Final: C=2, D=2, A=2, B=2 ✓degrees, components=2 (AB disconnected from CD? No: A-C-D-B? A→C (E2=2), C→D (E4=0 no), B→D (E3=2). Components: {A,C} and {B,D} → invalid!
│               ├── E4=1: check→ components still split FAIL
│               └── E4=2: C=4>2 → PRUNE ✗
│               → FAIL → backtrack
├── E1=1:
│   BACKTRACK(1, {E1:1})
│   ├── E2=0: ...→ A=1<2, still going...
│   │   ├── E3=0: ...→ FAIL (degrees)
│   │   ├── E3=1: ...→ B=2 OK, A=1≠2 FAIL
│   │   └── E3=2: check B=3>2 → PRUNE ✗
│   ├── E2=1:
│   │   BACKTRACK(2, {E1:1, E2:1}) [A=2 so far, good]
│   │   ├── E3=0: ...
│   │   │   BACKTRACK(3, {E1:1,E2:1,E3:0})
│   │   │   ├── E4=0: Final: B=1≠2, D=0≠2 FAIL
│   │   │   ├── E4=1: Final: B=1≠2, D=1≠2 FAIL
│   │   │   └── E4=2: check B=1+2=3>2 → PRUNE ✗
│   │   ├── E3=1:
│   │   │   BACKTRACK(3, {E1:1,E2:1,E3:1})
│   │   │   ├── E4=0: Final: C=1≠2 FAIL
│   │   │   ├── **E4=1**: Final check:
│   │   │   │   • degrees: A=E1+E2=1+1=2✓, B=E1+E3=1+1=2✓, C=E2+E4=1+1=2✓, D=E3+E4=1+1=2✓
│   │   │   │   • crossings: none (H and V don't cross at shared islands)
│   │   │   │   • components: A-B-D-C-A → 1 component ✓
│   │   │   │   → valid=True ✅
│   │   │   │   → **SOLUTION FOUND: {E1:1, E2:1, E3:1, E4:1}**
```

**النتيجة النهائية:**
```json
{
  "status": "Solution Found",
  "solution": {
    "bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}
  },
  "stats": {
    "nodes_explored": 42,
    "backtracks": 15,
    "pruned": 8,
    "duration_ms": 0.3
  }
}
```

# CANDIDATE EDGES SPEC

## الأقسام المطلوبة

## 1. Purpose

The `generate_candidate_edges(islands)` function generates all possible bridges between islands in a Hashiwokakero puzzle.

It only identifies valid connections between islands. It does not solve the puzzle or determine the final number of bridges.
------------
وظيفة الدالة `generate_candidate_edges(islands)` هي إنشاء قائمة بجميع الجسور المحتملة بين الجزر في لعبة Hashiwokakero.

وظيفة الدالة تقتصر على تحديد الاتصالات الصحيحة الممكنة بين الجزر فقط، ولا تقوم بحل اللغز أو تحديد العدد النهائي للجسور.

### 2. المدخلات والمخرجات

##  Input

The function receives a list of islands.

Each island contains:

- `id`: Unique island identifier.
- `row`: Vertical position (starting from 0).
- `col`: Horizontal position (starting from 0).
- `required_bridges`: Number of bridges required by the island.

Example:

```python
islands = [
    {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
    {"id": "B", "row": 0, "col": 2, "required_bridges": 2}
]
```
تستقبل الدالة قائمة تحتوي على الجزر.

كل جزيرة تحتوي على البيانات التالية:

- `id`: مُعرّف فريد للجزيرة.
- `row`: موقع الجزيرة الرأسي، ويبدأ العد من صفر.
- `col`: موقع الجزيرة الأفقي، ويبدأ العد من صفر.
- `required_bridges`: عدد الجسور المطلوبة لهذه الجزيرة.

مثال:

```python
islands = [
    {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
    {"id": "B", "row": 0, "col": 2, "required_bridges": 2}
]
```

##  Output

The function returns a list of candidate bridges.

Each bridge contains:

- `id`: Unique bridge identifier (E1, E2, ...).
- `from`: Starting island ID.
- `to`: Destination island ID.
- `orientation`: Either `"horizontal"` or `"vertical"`.

Example:

```python
[
    {
        "id": "E1",
        "from": "A",
        "to": "B",
        "orientation": "horizontal"
    }
]
```
ترجع الدالة قائمة تحتوي على الجسور المحتملة.

كل جسر يحتوي على البيانات التالية:

- `id`: مُعرّف فريد للجسر، مثل E1 و E2 وهكذا.
- `from`: مُعرّف الجزيرة التي يبدأ منها الجسر.
- `to`: مُعرّف الجزيرة التي ينتهي عندها الجسر.
- `orientation`: اتجاه الجسر، ويكون إما `"horizontal"` (أفقي) أو `"vertical"` (رأسي).

مثال:

```python
[
    {
        "id": "E1",
        "from": "A",
        "to": "B",
        "orientation": "horizontal"
    }
]
```

### 3. قاعدة الترتيب (من DATA_MODEL.md)

## Ordering Rules

To guarantee deterministic output:

1. Sort islands by `row` first, then by `col`, in ascending order.
2. Process islands in the sorted order.
3. For each island:
   - Check its nearest neighbor to the right (horizontal).
   - Then check its nearest neighbor below (vertical).
4. Assign bridge IDs sequentially, starting from `E1`.

The `from` field must always refer to the left island for horizontal bridges or the upper island for vertical bridges.
---------
لضمان الحصول على نفس النتائج ونفس ترتيب الجسور في كل مرة:

1. يتم ترتيب الجزر أولاً حسب `row` تصاعدياً، ثم حسب `col` تصاعدياً.
2. يتم فحص الجزر وفقاً لهذا الترتيب.
3. عند فحص كل جزيرة:
   - يتم البحث أولاً عن أقرب جزيرة ناحية اليمين (Horizontal).
   - ثم يتم البحث عن أقرب جزيرة ناحية الأسفل (Vertical).
4. يتم ترقيم الجسور بالتتابع بداية من E1.

يجب أن يشير الحقل `from` دائماً إلى الجزيرة الموجودة على اليسار في حالة الجسر الأفقي، أو الجزيرة الموجودة بالأعلى في حالة الجسر الرأسي.

### 4. حالات الحافة

Each candidate bridge can have one of three possible values in the solution:

- `0`: No bridge.
- `1`: One bridge.
- `2`: Two parallel bridges.

The candidate generator only identifies possible edges. Assigning these values is the responsibility of the solving algorithms.
---------
يمكن أن يأخذ كل جسر محتمل واحدة من ثلاث قيم أثناء عملية الحل:

- `0`: لا يوجد جسر بين الجزيرتين.
- `1`: يوجد جسر واحد بين الجزيرتين.
- `2`: يوجد جسران متوازيان بين الجزيرتين.

وظيفة مولّد الجسور تقتصر على تحديد الجسور المحتملة فقط، أما تحديد قيمة كل جسر فهو من مسؤولية خوارزميات الحل مثل Backtracking و Genetic Algorithm.

### 5. مثال يدوي على P1 و P2
## P1
Input:

```python
islands = [
    {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
    {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
    {"id": "C", "row": 2, "col": 0, "required_bridges": 2},
    {"id": "D", "row": 2, "col": 2, "required_bridges": 2}
]
```

Expected output:

| Edge ID | From | To | Orientation |
|---------|------|----|-------------|
|    E1   |   A  |  B | horizontal  |
|    E2   |   A  |  C | vertical    |
|    E3   |   B  |  D | vertical    |
|    E4   |   C  |  D | horizontal  |

Total candidate edges: 4.

## P2
Input:

```python
islands = [
    {"id": "C", "row": 0, "col": 2, "required_bridges": 2},
    {"id": "A", "row": 1, "col": 0, "required_bridges": 2},
    {"id": "B", "row": 1, "col": 4, "required_bridges": 2},
    {"id": "D", "row": 2, "col": 2, "required_bridges": 2}
]
```
لاحظ إن ترتيب الجزر في الـ Input مش هو ترتيب الحروف.

بعد الـ Sorting:
- C في الصف الأول.
- A ثم B في الصف الثاني.
- D في الصف الثالث.

|  ID  |  From  |  To  |   Orientation |
|------|--------|------|---------------|
|  E1  |	C	|  D   |	vertical   |
|  E2  |	A	|  B   |    horizontal |

## pseudocode:
FUNCTION generate_candidate_edges(islands):

    SORT islands BY row ASCENDING, col ASCENDING

    edges = EMPTY LIST
    edge_counter = 1

    FOR EACH current IN islands:

        # Find nearest island to the RIGHT
        right_candidates = islands WHERE:
            candidate.row == current.row
            AND candidate.col > current.col

        IF right_candidates IS NOT EMPTY:

            nearest_right = candidate with MINIMUM col

            ADD {
                id: "E" + edge_counter,
                from: current.id,
                to: nearest_right.id,
                orientation: "horizontal"
            } TO edges

            edge_counter = edge_counter + 1


        # Find nearest island BELOW
        bottom_candidates = islands WHERE:
            candidate.col == current.col
            AND candidate.row > current.row

        IF bottom_candidates IS NOT EMPTY:

            nearest_bottom = candidate with MINIMUM row

            ADD {
                id: "E" + edge_counter,
                from: current.id,
                to: nearest_bottom.id,
                orientation: "vertical"
            } TO edges

            edge_counter = edge_counter + 1

    RETURN edges

# Data Model

> ⚠️ **الحالة: مقترح (PROPOSED).** بيتراجع ويتقفل في **S1-02** (Day 2، Mostafa + Monzer + مراجعة الفريق).
> بعد التقفيل: ممنوع تغيير أي اسم أو شكل من غير موافقة Mostafa. لما يتقفل غيّر السطر ده لـ **FROZEN + التاريخ**.

الإحداثيات بتبدأ من **0**. `row` للأسفل، `col` لليمين. الحقول بـ `snake_case`.

## Puzzle
```json
{ "rows": 3, "cols": 3, "islands": [ ... ] }
```

## Island
```json
{ "id": "A", "row": 0, "col": 0, "required_bridges": 2 }
```
- `id` نص فريد. `required_bridges` من 1 لـ 8. الاسم **required_bridges** ثابت بالحرف.

## Candidate Bridge (اتصال محتمل)
```json
{ "id": "E1", "from": "A", "to": "B", "orientation": "horizontal" }
```
- `from` = الجزيرة الأعلى/اليسار، `to` = الأسفل/اليمين. `orientation` = `horizontal` أو `vertical`.
- **مفيش عدد جسور هنا.** العدد الفعلي جزء من الـ Solution.

### قاعدة ترتيب الـ Candidate Bridges (حرجة، GA بتبني عليها)
1. رتّب الجزر بـ `(row, col)`.
2. لكل جزيرة بالترتيب: أضف جسرها **الأفقي ناحية اليمين** (لو فيه جزيرة تالية في نفس الصف)، وبعده جسرها **الرأسي ناحية الأسفل** (لو فيه جزيرة تالية في نفس العمود).
3. الترقيم `E1, E2, E3, ...` بنفس الترتيب ده.
نفس الجزر بأي ترتيب إدخال لازم تدي نفس الـ Edges ونفس الـ ids.

## Solution
```json
{ "bridge_counts": { "E1": 1, "E2": 1, "E3": 1, "E4": 1 } }
```
- القيمة 0 أو 1 أو 2 بس. Edge مش مذكور = 0. id مش موجود في الـ Candidate Bridges = خطأ (`invalid_values`).

## Chromosome (GA / MA)
Array من 0/1/2 بنفس طول وترتيب الـ Candidate Bridges: `index i  ↔  E(i+1)`. مثال P1: `[1, 1, 1, 1]`.

## Validation Report (ناتج `validate_solution`)
```json
{
  "valid": false,
  "degree_violations": [{ "island": "A", "required": 2, "actual": 1 }],
  "crossings": [["E1", "E2"]],
  "connected_components": 2,
  "invalid_values": [{ "edge": "E9", "value": 1 }]
}
```
`valid = true` لو وبس لو: مفيش `invalid_values` ومفيش `degree_violations` ومفيش `crossings` و`connected_components == 1`.

## Partial vs Final Validation
- **Partial (أثناء البحث):** الجزيرة ماتعدّيش رقمها (`actual <= required`).
- **Final (حل منتهي):** `actual == required` بالظبط.

## مثال كامل: Puzzle P1 (شبكة 3×3)
```json
{
  "rows": 3, "cols": 3,
  "islands": [
    { "id": "A", "row": 0, "col": 0, "required_bridges": 2 },
    { "id": "B", "row": 0, "col": 2, "required_bridges": 2 },
    { "id": "C", "row": 2, "col": 0, "required_bridges": 2 },
    { "id": "D", "row": 2, "col": 2, "required_bridges": 2 }
  ]
}
```
Candidate Bridges بالترتيب: `E1 = A–B (horizontal)` • `E2 = A–C (vertical)` • `E3 = B–D (vertical)` • `E4 = C–D (horizontal)`.

- الحل الصحيح **الوحيد:** `{"E1":1,"E2":1,"E3":1,"E4":1}`
- `[2,0,0,2]` و`[0,2,2,0]`: الأرقام سليمة لكن الشبكة مقسومة لمجموعتين → **مرفوضين**.

## Puzzle P2 (مثال تقاطع)
الجزر: `C(0,2) A(1,0) B(1,4) D(2,2)` كلها 1. Candidate Bridges: `E1 = C–D (vertical)` و`E2 = A–B (horizontal)`، **بيتقاطعوا عند (1,2)**.

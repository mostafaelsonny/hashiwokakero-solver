# UI DATA SPEC

- **المسؤول:** Febronia
- **المهمة:** S1-11 (Puzzle Editor UI Data Contract)
- **الموعد:** Day 2 من Sprint 1
- **الحالة:** مكتمل ومطابق للـ Data Model المعتمد ✅

---

## 1. الـ JSON اللي الواجهة بتطلّعه (Puzzle JSON)

الواجهة (Puzzle Editor) بتطلع الـ Puzzle JSON بالشكل المعتمد والمطابق بنسبة 100% للـ Shared Data Model في `docs/DATA_MODEL.md`:

```json
{
  "rows": 7,
  "cols": 7,
  "islands": [
    { "id": "I1", "row": 0, "col": 2, "required_bridges": 3 },
    { "id": "I2", "row": 0, "col": 6, "required_bridges": 4 }
  ]
}
```

### القواعد الإلزامية:
1. **Dimensions:** حقلان مسطحان (flat fields) في جذر الـ Object: `rows` و `cols` (أعداد صحيحة موجبة >= 1). لا نستخدم كائن فرعي مثل `dimensions: {rows, cols}`.
2. **Islands:** مصفوفة `islands`، وكل عنصر فيها يحتوي على:
   - `id`: المعرف الفريد للجزيرة (مثال: `"I1"`, `"I2"`).
   - `row`: رقم الصف (0-indexed يبدأ من 0 وينمو لأسفل).
   - `col`: رقم العمود (0-indexed يبدأ من 0 وينمو يميناً).
   - `required_bridges`: عدد الجسور المطلوب للجزيرة (عدد صحيح من 1 إلى 8). الحقل اسمه بالضبط `required_bridges` وليس `value`.
3. **عدم تضمين حقول إضافية:**
   - **لا نضع مصفوفة `bridges`** داخل الـ Puzzle؛ الجسور المحتملة (Candidate Bridges) بيولدها الـ Backend تلقائياً عبر `generate_candidate_edges` (S1-03)، والجسور الفعلية تنتمي إلى كائن الحل `Solution` وليس الـ `Puzzle`.
   - **لا نضع حقل `algorithm`** داخل الـ Puzzle؛ تحديد الخوارزمية يتم إرساله منفصلاً في طلب الـ Solve (`SolveRequest: {puzzle, algorithm, config}`).

---

## 2. توليد الـ IDs (Island IDs Generation)

كل جزيرة تُضاف إلى الشبكة تأخذ مُعرّفاً فريداً ومميزاً (Unique Identifier) لتسهيل تتبعها وربطها بالجسور:

1. **Auto-Increment Counter:** نستخدم عداداً داخلياً يبدأ من 1 (`I1`, `I2`, `I3`, ...).
2. **عدم إعادة التدوير (No ID Reuse):** في الجلسة الواحدة، لو حُذفت جزيرة (مثلاً `I2`)، العداد يستمر في الزيادة (`I3`, `I4`) لمنع أي تداخل أو ارتباك في الـ references.
3. **إعادة التصفير (Reset):** يتم تصفير العداد والبدء من `I1` فقط عند الضغط على زر **"New Grid"** أو تفريغ الشبكة بالكامل.

---

## 3. التحقق من المدخلات (Input Validation)

الواجهة تطبق قواعد تحقق صارمة لحماية الـ Data Model:

1. **نفس الخلية (Cell Uniqueness):**
   - يمنع تماماً وضع أكثر من جزيرة في نفس الإحداثيات `(row, col)`.
   - النقر على خلية مشغولة بجزيرة يقوم بتدوير قيمة `required_bridges` (1 ← 2 ← ... ← 8 ← 1) ولا يضيف جزيرة مكررة.
2. **حدود الشبكة (Boundary Enforcement):**
   - كل جزيرة يجب أن تقع داخل نطاق الشبكة: `0 <= row < rows` و `0 <= col < cols`.
   - عند تصغير أبعاد الشبكة، تُحذف تلقائياً أي جزر أصبحت خارج الحدود الجديدة.
3. **القيم المسموح بها (Allowed Bridge Counts):**
   - قيمة `required_bridges` مقيدة دائماً في النطاق `[1, 8]`.
   - لا يمكن إدخال 0 أو قيم سالبة أو أكبر من 8.

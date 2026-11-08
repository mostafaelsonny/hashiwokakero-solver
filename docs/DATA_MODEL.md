# Shared Data Model — Hashiwokakero Puzzle Solver

> **حالة المستند (Document Status):** Draft for team design review — لسه مقترح وبيحتاج مراجعة الفريق.
> **Owner:** Mostafa (Data Model Owner)
> **Reviewers:** Monzer, Ebrahim, Rovan, وعضو الـ UI team
> **مكان الملف في الـ Repository:** `docs/DATA_MODEL.md`
> **بيغطي:** UI, Candidate Bridge Generation, Backtracking, Genetic Algorithm (GA), Memetic Algorithm (MA), وValidation.

---

## 1. Purpose — الهدف من الملف

الملف ده بيحدد الـ **Shared Data Contract** الموحد لمشروع Hashiwokakero. كل أجزاء المشروع **MUST** تستخدم الـ structures والـ rules الموجودة هنا لما تتبادل بيانات الـ Puzzle، والاتصالات المحتملة، والـ solutions، والـ chromosomes، ونتائج الـ validation.

الهدف الأساسي إننا نمنع إن كل عضو يمثل نفس الجزيرة أو نفس الجسر بطريقة مختلفة عن باقي الفريق، وده هيخلّي الـ integration بين الـ components أوضح وأسهل.

المشروع بيحل ألغاز **Hashiwokakero**، والحل الصحيح لازم يحقق كل القواعد دي:

1. إجمالي عدد الجسور المتصلة بكل جزيرة لازم يساوي قيمة `required_bridges` الخاصة بالجزيرة دي.
2. الجسور لازم تكون أفقية أو رأسية فقط (`horizontal` أو `vertical`).
3. مينفعش أي جسرين مختارين يتقاطعوا.
4. مينفعش يكون فيه أكتر من جسرين بين نفس زوج الجزر.
5. كل الجزر لازم تكون متصلة ببعض في شبكة واحدة (connected network).

الملف ده هو **Source of Truth** لطريقة تمثيل البيانات بين أجزاء المشروع. لكنه مش بيفرض على كل Algorithm طريقة الـ implementation الداخلية بتاعته.

### 1.1 Normative Language — معنى كلمات الإلزام

الكلمات دي مستخدمة في المستند بمعاني محددة، ولازم الفريق يلتزم بيها:

- **MUST / MUST NOT:** شرط إجباري لازم يتنفذ / ممنوع تنفيذه.
- **SHOULD:** توصية قوية؛ لو فيه سبب لعدم الالتزام بيها، لازم نناقشه في الـ Design Review.
- **MAY:** اختيار اختياري مسموح، بشرط إنه ميغيّرش الـ Data Contract.

---

## 2. Global Conventions — قواعد عامة

### 2.1 Naming — تسمية الحقول

- أسماء الحقول في الـ JSON **MUST** تكون باستخدام `snake_case`.
- الـ Island IDs والـ Candidate Bridge IDs **MUST** تكون Strings.
- القيم الرقمية الخاصة بالأبعاد والإحداثيات ومتطلبات الجزر وأعداد الجسور **MUST** تكون Integers، مش Floating-point values.
- أسماء الحقول Case-sensitive؛ يعني الحروف الكبيرة والصغيرة بتفرق.
- اسم حقل الجزيرة **MUST** يكون بالضبط `required_bridges`. مينفعش نستخدم أسماء بديلة زي `bridges` أو `requiredBridges` أو `bridge_count`.

### 2.2 Coordinates — نظام الإحداثيات

الإحداثيات عندنا بتبدأ من **0 (Zero-based indexing)**:

- `row = 0` هو أول صف فوق، وكل ما قيمة `row` تزيد بننزل لتحت.
- `col = 0` هو أول عمود على الشمال، وكل ما قيمة `col` تزيد بنتحرك لليمين.
- لو الـ Puzzle أبعادها `rows = R` و`cols = C`، يبقى الإحداثيات الصحيحة لازم تحقق: `0 <= row < R` و`0 <= col < C`.

### 2.3 Identity — الـ IDs والتمييز بين العناصر

- كل Island لازم يكون ليها `id` فريد داخل نفس الـ Puzzle.
- كل Candidate Bridge لازم يكون ليه `id` فريد داخل قائمة الـ Candidate Bridges اللي اتولدت لنفس الـ Puzzle.
- الـ Candidate Bridge بيشير للجزر عن طريق الـ String IDs بتاعتها، ومينفعش يكرر الـ Island objects كاملة جواه.
- الـ Candidate Bridge IDs هي IDs deterministic مرتبطة بنسخة الـ Puzzle اللي اتولدت منها. مش IDs دائمة تفضل ثابتة بين كل تعديلات الـ Puzzle.

### 2.4 Separation of Responsibilities — مسؤولية كل Structure

كل Structure ليها مسؤولية محددة:

- `Puzzle`: بيوصف أبعاد الـ Grid والجزر الموجودة فيها.
- `CandidateBridge`: بيوصف اتصال مباشر محتمل بين جزيرتين.
- `Solution`: بيوصف عدد الجسور اللي اتختارت فعليًا لكل اتصال محتمل.
- `Chromosome`: هو الـ positional representation للـ Solution المستخدم في GA/MA.
- `ValidationReport`: بيوضح هل الـ Solution المقترح محقق قيود اللغز ولا لأ.

**مهم:** عدد الجسور المختارة فعليًا **MUST NOT** يتخزن جوه `CandidateBridge`.

---

## 3. Puzzle

الـ `Puzzle` بيحتوي على أبعاد الـ Grid والجزر الموجودة عليها. أما الـ Candidate Bridges فبيتم توليدها من الـ Puzzle، وبتفضل Collection منفصلة عنه.

### 3.1 Structure

```json
{
  "rows": 3,
  "cols": 3,
  "islands": []
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `rows` | integer | Yes | عدد صفوف الـ Grid، ولازم يكون أكبر من صفر. |
| `cols` | integer | Yes | عدد أعمدة الـ Grid، ولازم يكون أكبر من صفر. |
| `islands` | array of Island | Yes | كل الجزر التابعة للـ Puzzle. |

### 3.2 Rules

1. `rows` و`cols` **MUST** يكونوا Positive Integers.
2. الـ `islands` **MUST** تحتوي على الجزر التابعة للـ Puzzle.
3. إحداثيات كل Island **MUST** تكون داخل حدود الـ Grid.
4. مينفعش جزيرتين يكونوا في نفس `(row, col)`.
5. كل Island **MUST** يكون ليها `id` فريد ومش فارغ.
6. ترتيب عناصر `islands` وقت الإدخال **MUST NOT** يأثر على توليد الـ Candidate Bridges أو الـ IDs بتاعتها. الـ Generator لازم يطبق الترتيب المحدد في Section 5.

---

## 4. Island

الـ `Island` بتمثل دائرة مرقمة واحدة موجودة في الـ Puzzle.

### 4.1 Structure

```json
{
  "id": "A",
  "row": 0,
  "col": 0,
  "required_bridges": 2
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | Yes | ID فريد للجزيرة داخل الـ Puzzle. |
| `row` | integer | Yes | رقم الصف، وبيبدأ من 0. |
| `col` | integer | Yes | رقم العمود، وبيبدأ من 0. |
| `required_bridges` | integer | Yes | إجمالي عدد الجسور الفردية اللي لازم تكون متصلة بالجزيرة دي. |

### 4.2 Rules

- الـ `id` **MUST** يكون Unique داخل الـ Puzzle. أمثلة مقبولة: `A`, `B`, `C` أو `I1`, `I2`, `I3`.
- `row` و`col` **MUST** يكونوا إحداثيات صحيحة داخل أبعاد الـ Puzzle.
- `required_bridges` **MUST** يكون Integer في الـ standard Hashiwokakero range من `1` لـ `8`.
- اسم الحقل `required_bridges` **MUST** يتكتب بنفس الشكل ده في كل Components المشروع.

`required_bridges` معناها إجمالي الـ **Degree** المطلوب للجزيرة. يعني مش عدد الجزر المجاورة ليها؛ لأن الاتصال الواحد لو عدد جسوره `2` بيضيف 2 للعدد المطلوب من الجزيرة.

---

## 5. Candidate Bridge — اتصال محتمل بين جزيرتين

الـ `Candidate Bridge` بيمثل اتصال مباشر محتمل بين جزيرتين. هو بيحدد الـ identity والـ endpoints والـ orientation بتاع الاتصال فقط، لكنه **مش** بيحدد عدد الجسور اللي اتختارت في الـ Solution.

قائمة الـ Candidate Bridges بتتولد من الـ Puzzle، وبتتمثل كـ Collection منفصلة عنه.

### 5.1 Structure

```json
{
  "id": "E1",
  "from": "A",
  "to": "B",
  "orientation": "horizontal"
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | string | Yes | Candidate Bridge ID deterministic، زي `E1`. |
| `from` | string | Yes | ID الجزيرة اللي بتمثل نقطة البداية. |
| `to` | string | Yes | ID الجزيرة اللي بتمثل نقطة النهاية. |
| `orientation` | string | Yes | إما `horizontal` أو `vertical`. |

### 5.2 Endpoint Direction — اتجاه الـ Endpoints

ترتيب `from` و`to` **MUST** يمشي مع اتجاه الـ Grid:

- لو الـ Candidate Bridge أفقي (`horizontal`)، يبقى `from` هي الجزيرة اللي على الشمال، و`to` هي الجزيرة اللي على اليمين.
- لو الـ Candidate Bridge رأسي (`vertical`)، يبقى `from` هي الجزيرة اللي فوق، و`to` هي الجزيرة اللي تحت.

القيم الموجودة في `from` و`to` **MUST** تكون Island IDs، مش Island objects كاملة ومش Array indexes.

### 5.3 Which Connections Are Candidates? — إمتى الاتصال يبقى Candidate؟

بنولّد Candidate Bridge بس بين **أقرب الجزر الظاهرة لبعض** في واحد من الاتجاهات الأربعة الأساسية (يمين، شمال، فوق، تحت).

بالنسبة لكل جزيرة:

- الـ Horizontal Candidate، لو موجود، بيربطها بأقرب جزيرة على يمينها في نفس الـ Row.
- الـ Vertical Candidate، لو موجود، بيربطها بأقرب جزيرة تحتها في نفس الـ Column.

مينفعش نتخطى جزيرة موجودة بين جزيرتين علشان نعمل اتصال مع جزيرة أبعد في نفس الصف أو العمود. يعني الجسر مينفعش يعدّي من خلال جزيرة تانية.

كل زوج جزر ينطبق عليه الشرط ده **MUST** ينتج عنه Candidate Bridge واحد بالضبط. عدد الجسور الفعلي (صفر أو واحد أو اتنين) بيتحدد بعد كده في الـ `Solution`.

### 5.4 Deterministic Candidate Bridge Ordering and IDs — ترتيب وترقيم ثابت

**الترتيب ده جزء أساسي من الـ Data Contract، والـ GA والـ MA MUST يستخدموه بنفس الشكل من غير أي تغيير.**

الـ Candidate Bridge Generator **MUST** ينفذ الخطوات دي بالترتيب:

1. يرتب كل الجزر حسب `row` تصاعديًا، وبعدها `col` تصاعديًا.
2. يزور الجزر بالترتيب اللي طلع من الخطوة الأولى.
3. لكل جزيرة، يضيف الأول الـ Horizontal Candidate Bridge لأقرب جزيرة على يمينها في نفس الصف، لو موجودة.
4. بعده يضيف الـ Vertical Candidate Bridge لأقرب جزيرة تحتها في نفس العمود، لو موجودة.
5. يدي الـ Candidate Bridge IDs بشكل sequential حسب ترتيب الإضافة بالضبط: `E1`, وبعده `E2`, وبعده `E3`، وهكذا.

الـ Generator **MUST NOT** يضيف جسور ناحية الشمال أو لفوق بشكل منفصل؛ لأن الاتصالات دي بتتولد بالفعل لما نزور الجزيرة اللي على الشمال أو اللي فوق.

ترتيب الـ List الناتجة **MUST** يفضل زي ما هو. ممنوع أي Component يعمل Re-sort لقائمة الـ Candidate Bridges بعد ما الـ IDs تتحدد.

#### Determinism Guarantees — ضمان ثبات النتيجة

لو عندنا نفس محتوى الـ Puzzle (نفس Island IDs ونفس الإحداثيات)، فتوليد الـ Candidate Bridges **MUST** ينتج نفس القائمة بنفس الترتيب ونفس IDs من `E1` لحد `En` كل مرة، بغض النظر عن ترتيب الجزر الأصلي داخل Array الـ `islands`.

لو الـ Puzzle اتغير، مثلًا جزيرة اتضافت أو مكان جزيرة اتغير، فمن الممكن الـ Candidate Bridge IDs تتغير؛ لأنها بتتحدد بالتسلسل من القائمة الجديدة. علشان كده، أي `Solution` أو `Chromosome` لازم يتفسر باستخدام نفس قائمة الـ Candidate Bridges اللي اتولد منها بالضبط.

#### Ordering Example — مثال على الترتيب

عندنا الجزر دي:

| Island | Row | Col |
|---|---:|---:|
| A | 0 | 0 |
| B | 0 | 2 |
| C | 2 | 0 |
| D | 2 | 2 |

ترتيب الجزر بعد الـ Sorting هيكون `A, B, C, D`.

- لما نزور A: نضيف A→B أفقي، وبعده A→C رأسي.
- لما نزور B: نضيف B→D رأسي.
- لما نزور C: نضيف C→D أفقي.
- لما نزور D: مش هنضيف أي Candidate Bridge.

الترتيب النهائي للـ Candidate Bridges لازم يكون بالضبط كده:

| Order | ID | From | To | Orientation |
|---:|---|---|---|---|
| 1 | `E1` | `A` | `B` | `horizontal` |
| 2 | `E2` | `A` | `C` | `vertical` |
| 3 | `E3` | `B` | `D` | `vertical` |
| 4 | `E4` | `C` | `D` | `horizontal` |

---

## 6. Solution — الحل المختار

الـ `Solution` بتحدد عدد الجسور اللي اتختارت لكل Candidate Bridge. وهي Structure منفصلة عن تعريفات الـ Candidate Bridges نفسها.

### 6.1 Structure

```json
{
  "bridge_counts": {
    "E1": 1,
    "E2": 0,
    "E3": 2,
    "E4": 1
  }
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `bridge_counts` | object / map | Yes | Map بيربط كل Candidate Bridge ID بعدد الجسور المختارة ليه. |

### 6.2 Rules

- كل Key داخل `bridge_counts` **MUST** يكون Candidate Bridge ID موجود في قائمة الـ Candidate Bridges المرتبطة بالـ Solution دي.
- كل Value **MUST** يكون Integer وقيمته `0` أو `1` أو `2` فقط.
- القيمة `0` معناها مفيش أي جسر مختار للـ Candidate Bridge ده.
- القيمة `1` معناها فيه جسر واحد مختار.
- القيمة `2` معناها فيه جسرين متوازيين مختارين.
- لو Candidate Bridge ID مش موجود داخل `bridge_counts`، لازم نتعامل معاه على إن عدد جسوره `0`.
- لو فيه Candidate Bridge ID مش معروف، لازم يتسجل كـ Invalid؛ ومينفعش نتجاهله بصمت.
- عدد الجسور المختارة **MUST** يتخزن هنا، مش جوه الـ `CandidateBridge` object.

علشان نخلي الـ Output مختصر وNormalized، الـ Producers **SHOULD** متضيفش entries قيمتها `0`. لكن الـ Consumers **MUST** تقبل وجود `0` بشكل صريح وتتعامل معاه بنفس طريقة الـ ID اللي مش موجود في الـ Map.

### 6.3 Degree Calculation — حساب درجة الجزيرة

الـ Actual Degree لأي جزيرة بيساوي مجموع أعداد الجسور المختارة في كل Candidate Bridges المتصلة بالجزيرة دي.

مثال: لو الجزيرة A متصلة عن طريق `E1` وعدده `1`، وعن طريق `E2` وعدده `2`، يبقى:

`actual_degree(A) = 1 + 2 = 3`.

الـ Solution يحقق شرط الـ Degree للجزيرة فقط لما:

`actual_degree(island) == island.required_bridges`.

---

## 7. Chromosome (GA and MA)

الـ `Chromosome` عبارة عن Array من Integer genes. كل Gene بيمثل عدد الجسور المختارة للـ Candidate Bridge الموجود في نفس الـ Position داخل قائمة الـ Candidate Bridges المرتبة بشكل Deterministic.

### 7.1 Structure

```json
[1, 0, 2, 1]
```

### 7.2 Mapping Rules — قواعد الربط

- طول الـ Chromosome **MUST** يساوي عدد الـ Candidate Bridges.
- كل Gene **MUST** يكون Integer في المدى من `0` لـ `2`.
- الـ Candidate Bridge اللي عنده List index رقم `i` بيقابله Gene عنده Chromosome index رقم `i`، والاتنين Zero-based.
- الـ Gene عند Index `0` بيمثل `E1`، والـ Gene عند Index `1` بيمثل `E2`، والـ Gene عند Index `2` بيمثل `E3`، وهكذا؛ لأن الـ IDs بتتحدد من `E1` حسب ترتيب الـ List.
- الـ Candidate Bridge list **MUST** تكون نفس القائمة المرتبة بالطريقة المحددة في Section 5. ممنوع الـ GA أو الـ MA يعملوا Sorting مستقل ليها.

### 7.3 Conversion Between Chromosome and Solution

لو قائمة الـ Candidate Bridges المرتبة هي:

```text
[E1, E2, E3, E4]
```

والـ Chromosome هو:

```text
[1, 0, 2, 1]
```

فالـ Solution المكافئ ليه هيكون:

```json
{
  "bridge_counts": {
    "E1": 1,
    "E2": 0,
    "E3": 2,
    "E4": 1
  }
}
```

التحويل العكسي بيستخدم نفس قائمة الـ Candidate Bridges المرتبة. لكل Candidate Bridge عند Index رقم `i`، بنحط في الـ Gene القيمة المقابلة ليه من `bridge_counts`، أو `0` لو الـ ID مش موجود في الـ Map.

الـ Chromosome هو مجرد Algorithm representation للـ Solution، مش معنى مختلف للـ Puzzle. علشان كده الـ GA والـ MA **MUST** يقيّموا الـ genes باستخدام نفس ترتيب الـ Candidate Bridges.

---

## 8. Validation Report

الـ Validator بيرجع `ValidationReport` علشان يوضح نتيجة فحص Solution مقترح مقابل Puzzle وقائمة الـ Candidate Bridges المرتبطة بيه وبنفس ترتيبها.

### 8.1 Structure

```json
{
  "valid": true,
  "degree_violations": [],
  "crossings": [],
  "connected_components": 1,
  "invalid_values": []
}
```

| Field | Type | Description |
|---|---|---|
| `valid` | boolean | بتكون `true` بس لما كل شروط الـ Validation المطلوبة تنجح. |
| `degree_violations` | array | الجزر اللي الـ Actual Degree بتاعها مختلف عن قيمة `required_bridges`. |
| `crossings` | array of two-element arrays | أزواج الـ Candidate Bridges المختارة اللي بتتقاطع مع بعض. |
| `connected_components` | integer | عدد الـ Connected Components في الـ Graph المكوّن من كل الجزر والاتصالات المختارة. |
| `invalid_values` | array | أي قيم غير صحيحة في الـ Solution أو الـ Chromosome، أو أي Candidate Bridge references غير صحيحة تم اكتشافها. |

### 8.2 `degree_violations`

كل Entry داخل `degree_violations` **MUST** يكون بالشكل ده:

```json
{
  "island": "A",
  "required": 2,
  "actual": 1
}
```

- `island`: الـ Island ID.
- `required`: قيمة `required_bridges` المطلوبة للجزيرة.
- `actual`: مجموع أعداد الجسور المختارة والمتصلة بالجزيرة.
- الجزيرة **MUST** تظهر في الـ Array دي لو وفقط لو الـ Actual Degree مختلف عن الـ Required Degree.
- ترتيب الـ Entries **SHOULD** يمشي مع الترتيب Deterministic للجزر: `row` تصاعديًا وبعده `col` تصاعديًا.

### 8.3 `crossings`

كل Crossing **MUST** يتم تمثيله كـ Array فيها اتنين Candidate Bridge IDs بالضبط:

```json
[
  ["E1", "E3"]
]
```

بنبلغ عن Crossing بس لما يكون كل واحد من الـ Candidate Bridges الاتنين عنده Selected count أكبر من صفر، وخط الـ Horizontal وخط الـ Vertical يتقاطعوا في نقطة موجودة **داخل** القطعتين، مش عند الـ endpoints.

- لو الجسرين بيشتركوا في نفس Island كـ endpoint، ده مش بيتحسب Crossing.
- الـ Candidate Bridge اللي Count بتاعه `0` مينفعش يعمل Crossing.
- لو Count بتاع جسر هو `2`، ده مش معناه إننا نكرر نفس الـ Crossing مرتين؛ زوج الجسور المتقاطع يتسجل مرة واحدة.
- ترتيب كل Pair **MUST** يتبع ترتيب الـ Candidate Bridge list، وترتيب قائمة أزواج الـ Crossings **SHOULD** يكون Deterministic.

للتوضيح: لو عندنا Horizontal Candidate Bridge موجود على Row رقم `r` وبين Column رقم `c1` و`c2`، وعندنا Vertical Candidate Bridge موجود على Column رقم `c` وبين Row رقم `r1` و`r2`، يبقى الخطين بيتقاطعوا لما:

`r1 < r < r2` **and** `c1 < c < c2`.

استخدام Strict inequalities (`<`) معناه إن نقطة التقاطع لازم تكون داخل القطعتين، وده بيستبعد التقاطع عند الـ endpoints.

### 8.4 `connected_components`

الـ Validator **MUST** يبني Undirected Graph بالقواعد دي:

- كل Island تعتبر Graph Vertex، حتى الجزر اللي مفيش أي جسور مختارة متصلة بيها.
- الـ Candidate Bridge بيعمل Graph Connection بين جزيرتي الـ Endpoints بتوعه لما يكون Selected count أكبر من `0`.
- لو عدد الجسور المختارة `2`، ده برضه بيتحسب كـ Graph adjacency واحدة لأغراض الـ Connectivity؛ مش بنضيف Graph Vertex تاني أو Component إضافي.

قيمة `connected_components` هي عدد الـ Connected Components في الـ Graph ده. الحل اللي كل جزره متصلة ببعض **MUST** يكون عدد الـ Components فيه يساوي `1` بالضبط.

### 8.5 `invalid_values`

كل Entry داخل `invalid_values` **MUST** يستخدم الـ Structure الموحدة دي:

```json
{
  "path": "solution.bridge_counts.E3",
  "value": 3,
  "reason": "bridge_count_must_be_integer_0_1_or_2"
}
```

| Field | Type | Description |
|---|---|---|
| `path` | string | مكان العنصر غير الصحيح داخل الـ Input representation. |
| `value` | any JSON value | القيمة الفعلية غير الصحيحة، أو الطول الفعلي لو الخطأ متعلق بالطول. |
| `reason` | string | Reason code ثابت وقابل للقراءة آليًا (machine-readable). |

الـ Reason codes دي **SHOULD** يتم استخدامها بشكل موحد في كل أجزاء المشروع:

| Reason code | Meaning |
|---|---|
| `bridge_count_must_be_integer_0_1_or_2` | قيمة عدد الجسور في الـ Solution مش Integer من `0` لـ `2`. |
| `unknown_candidate_bridge_id` | الـ Solution بيشير لـ ID مش موجود في قائمة الـ Candidate Bridges. |
| `chromosome_length_mismatch` | طول الـ Chromosome مختلف عن عدد الـ Candidate Bridges. |
| `chromosome_gene_must_be_integer_0_1_or_2` | واحدة من قيم الـ Chromosome genes مش Integer من `0` لـ `2`. |

أمثلة على قيم `path`: `solution.bridge_counts.E99` و`solution.bridge_counts.E2` و`chromosome[3]`.

القيم غير الصحيحة **MUST NOT** يتم تحويلها تلقائيًا (coerced)، أو تعديلها لأقرب قيمة صحيحة (clamped)، أو قبولها كأنها صحيحة. ولأمان حساب الـ Metrics، الـ Invalid bridge-count entries والـ Unknown IDs **SHOULD** يتم استبعادهم من حسابات الـ Degree والـ Crossings والـ Connectivity؛ ووجود الـ Entry المقابل في `invalid_values` بيضمن إن التقرير النهائي يفضل Invalid.

### 8.6 Definition of `valid`

قيمة `valid` **MUST** تكون `true` لو وفقط لو كل الشروط دي متحققة:

1. الـ `invalid_values` فاضية.
2. الـ `degree_violations` فاضية.
3. الـ `crossings` فاضية.
4. قيمة `connected_components` تساوي `1`.

لو أي شرط من دول مش متحقق، يبقى `valid` **MUST** تكون `false`.

الـ Report ده مسؤول عن وصف صلاحية الـ Solution. أما لو الـ Puzzle أو قائمة الـ Candidate Bridges نفسها فيها مشكلة في الـ Structure، زي Duplicate Island IDs أو Coordinates خارج حدود الـ Grid أو Duplicate Candidate Bridge IDs أو Endpoint بيشير لجزيرة مش موجودة، فلازم يتم رفضها عن طريق Input/Model Validation قبل ما نبدأ الـ Normal Solution Validation.

---

## 9. Canonical P1 Example — المثال الأساسي المتفق عليه

المثال ده بيستخدم الـ P1 Puzzle اللي الفريق اتفق عليه في Sprint 1 task.

### 9.1 Grid

الـ Grid أبعادها `3` Rows و`3` Columns، والإحداثيات بتبدأ من صفر.

```text
      col 0   col 1   col 2
row 0   A       .       B
row 1   .       .       .
row 2   C       .       D
```

| Island | Row | Col | Required Bridges |
|---|---:|---:|---:|
| A | 0 | 0 | 2 |
| B | 0 | 2 | 2 |
| C | 2 | 0 | 2 |
| D | 2 | 2 | 2 |

### 9.2 Puzzle JSON

```json
{
  "rows": 3,
  "cols": 3,
  "islands": [
    {
      "id": "A",
      "row": 0,
      "col": 0,
      "required_bridges": 2
    },
    {
      "id": "B",
      "row": 0,
      "col": 2,
      "required_bridges": 2
    },
    {
      "id": "C",
      "row": 2,
      "col": 0,
      "required_bridges": 2
    },
    {
      "id": "D",
      "row": 2,
      "col": 2,
      "required_bridges": 2
    }
  ]
}
```

### 9.3 Candidate Bridges JSON

ترتيب التوليد هنا هو: الجسر اليمين بتاع A، وبعده الجسر لتحت بتاع A، وبعده الجسر لتحت بتاع B، وبعده الجسر اليمين بتاع C.

```json
[
  {
    "id": "E1",
    "from": "A",
    "to": "B",
    "orientation": "horizontal"
  },
  {
    "id": "E2",
    "from": "A",
    "to": "C",
    "orientation": "vertical"
  },
  {
    "id": "E3",
    "from": "B",
    "to": "D",
    "orientation": "vertical"
  },
  {
    "id": "E4",
    "from": "C",
    "to": "D",
    "orientation": "horizontal"
  }
]
```

### 9.4 Solution JSON

```json
{
  "bridge_counts": {
    "E1": 1,
    "E2": 1,
    "E3": 1,
    "E4": 1
  }
}
```

### 9.5 Equivalent Chromosome

```json
[1, 1, 1, 1]
```

الـ Gene-to-Edge mapping كالتالي:

| Chromosome Index | Gene | Candidate Bridge |
|---:|---:|---|
| 0 | 1 | E1 (A–B) |
| 1 | 1 | E2 (A–C) |
| 2 | 1 | E3 (B–D) |
| 3 | 1 | E4 (C–D) |

### 9.6 Validation Report JSON

```json
{
  "valid": true,
  "degree_violations": [],
  "crossings": [],
  "connected_components": 1,
  "invalid_values": []
}
```

### 9.7 Why P1 Is Valid — ليه الحل ده صحيح؟

| Island | Incident Candidate Bridges | Actual Degree | Required Degree | Result |
|---|---|---:|---:|---|
| A | E1 + E2 | 2 | 2 | Pass |
| B | E1 + E3 | 2 | 2 | Pass |
| C | E2 + E4 | 2 | 2 | Pass |
| D | E3 + E4 | 2 | 2 | Pass |

مفيش أي Crossings، وكل الجزر متصلة ببعض في Network واحدة. علشان كده الـ Validation Report نتيجته `valid`.

لو بصينا على Degree constraints لوحدها، ممكن أعداد الجسور الأربعة تنتج Configurations تانية، لكن الـ Configurations دي بتقسم الـ Puzzle لزوجين منفصلين من الجزر. شرط الـ Connectivity هو اللي بيخلّي الـ All-ones configuration هي الحل الصحيح الوحيد للـ P1.

### 9.8 Complete P1 Bundle

الـ Object الجاي بيجمع الـ Structures اللي اتعرفت بشكل منفصل في مكان واحد، وده ممكن نستخدمه كـ Example أو Test Fixture أو أثناء مناقشة الـ Integration. أسماء الـ Properties الخارجية هنا هدفها تجميع المثال فقط، ومش بتغيّر تعريف أي Structure من اللي فوق.

```json
{
  "puzzle": {
    "rows": 3,
    "cols": 3,
    "islands": [
      { "id": "A", "row": 0, "col": 0, "required_bridges": 2 },
      { "id": "B", "row": 0, "col": 2, "required_bridges": 2 },
      { "id": "C", "row": 2, "col": 0, "required_bridges": 2 },
      { "id": "D", "row": 2, "col": 2, "required_bridges": 2 }
    ]
  },
  "candidate_bridges": [
    { "id": "E1", "from": "A", "to": "B", "orientation": "horizontal" },
    { "id": "E2", "from": "A", "to": "C", "orientation": "vertical" },
    { "id": "E3", "from": "B", "to": "D", "orientation": "vertical" },
    { "id": "E4", "from": "C", "to": "D", "orientation": "horizontal" }
  ],
  "solution": {
    "bridge_counts": { "E1": 1, "E2": 1, "E3": 1, "E4": 1 }
  },
  "chromosome": [1, 1, 1, 1],
  "validation_report": {
    "valid": true,
    "degree_violations": [],
    "crossings": [],
    "connected_components": 1,
    "invalid_values": []
  }
}
```

---

## 10. Component Integration Contract — قواعد الـ Integration

كل Components المشروع **MUST** تتبادل الـ Shared Structures اللي متعرفة في المستند ده. مسموح إن الـ Internal Data Structures تختلف من Component للتاني، لكن أي Data بتعدّي من Component للتاني **MUST** تكون مطابقة للـ Contract ده.

| Component | Input | Output / Shared representation |
|---|---|---|
| UI | أبعاد الـ Grid والجزر اللي المستخدم دخلها | `Puzzle` |
| Candidate Bridge Generator | `Puzzle` | Ordered `CandidateBridge[]` |
| Backtracking | `Puzzle` وOrdered `CandidateBridge[]` | `Solution` (`bridge_counts`) |
| GA | `Puzzle` وOrdered `CandidateBridge[]` | `Chromosome`، ويكون قابل للتحويل إلى `Solution` |
| MA | GA-compatible chromosome/solution ونفس Ordered Candidate Bridges | Improved `Chromosome` / `Solution` |
| Validator | `Puzzle` وOrdered `CandidateBridge[]` و`Solution`، أو Chromosome تم تحويله باستخدام نفس الترتيب | `ValidationReport` |
| UI visualization | `Puzzle` وOrdered `CandidateBridge[]` و`Solution` | رسم الـ Puzzle والجسور المختارة؛ الـ Visual state مينفعش يغيّر تعريف الـ Data Contract |

### 10.1 Recommended Shared Function Boundaries

الأسماء دي مجرد أمثلة مقترحة للـ Functions. الفريق **MAY** يختار أسماء مختلفة، لكن الـ Input/Output contracts **MUST** تفضل زي ما هي.

```text
generate_candidate_bridges(puzzle: Puzzle) -> CandidateBridge[]

chromosome_to_solution(
    chromosome: Chromosome,
    candidate_bridges: CandidateBridge[]
) -> Solution

solution_to_chromosome(
    solution: Solution,
    candidate_bridges: CandidateBridge[]
) -> Chromosome

validate_solution(
    puzzle: Puzzle,
    candidate_bridges: CandidateBridge[],
    solution: Solution
) -> ValidationReport
```

### 10.2 Important Integration Rules

1. أي `Solution` أو `Chromosome` **MUST** يفضل مرتبط بنفس قائمة الـ Candidate Bridges اللي اتعمل منها بالضبط.
2. ممنوع أي Algorithm يفترض إن أي Array order عشوائي يعتبر هو نفس الـ Canonical Candidate Bridge order.
3. ممنوع أي Component يغيّر أسماء الـ Shared fields وقت ما يبعت Data لـ Component تاني.
4. أي Internal conversion **MUST** يحصل عند حدود الـ Component، ولازم يحافظ على نفس معنى الـ Shared Data.
5. الـ Validator لازم يستخدم نفس الـ Bridge counts ونفس تعريفات الـ Endpoints في فحوصات الـ Degree والـ Crossing والـ Connectivity كلها.

---

## 11. Input Validation and Edge Cases

الـ Checks الجاية **SHOULD** تتنفذ قبل Candidate Generation أو Solution Validation.

### 11.1 Puzzle Checks

- `rows` و`cols` لازم يكونوا Positive Integers.
- `islands` لازم تكون Array.
- الـ Island IDs لازم تكون Non-empty وUnique.
- كل `row` و`col` لازم يكونوا Integers وداخل حدود الـ Grid.
- مينفعش جزيرتين يشتركوا في نفس الإحداثيات.
- `required_bridges` لازم يكون Integer من `1` لـ `8`.

ممكن الـ Puzzle يكون صحيح من ناحية الـ Structure، لكنه في نفس الوقت غير قابل للحل (Unsolvable). مثال: جزيرة محتاجة عدد جسور أكبر من عدد الجسور المتاحة ليها من الـ Neighboring Candidate Bridges. الـ Structural validity والـ Puzzle solvability حاجتين مختلفتين، و**MUST NOT** نتعامل معاهم على إنهم نفس الـ Check.

### 11.2 Candidate Bridge Checks

- كل Candidate Bridge ID لازم يكون Unique.
- `from` و`to` لازم يشاوروا على Islands موجودة فعلًا.
- `from` و`to` لازم يكونوا جزيرتين مختلفتين.
- قيمة `orientation` لازم تكون بالضبط `horizontal` أو `vertical`.
- الـ Horizontal bridge لازم تكون الـ Endpoints بتاعته في نفس الـ Row، و`from` تكون على الشمال من `to`.
- الـ Vertical bridge لازم تكون الـ Endpoints بتاعته في نفس الـ Column، و`from` تكون فوق `to`.
- الـ Generated Candidate Bridge لازم يتصل بأقرب جزيرة ظاهرة في اتجاهه، ومينفعش يتخطى جزيرة موجودة في النص.
- القائمة لازم تتبع الـ Deterministic ordering والـ ID assignment المحددين في Section 5.

### 11.3 Solution and Chromosome Checks

- الـ Solution لازم يحتوي على Object اسمه `bridge_counts`.
- كل Bridge count موجود لازم يكون Integer من `0` لـ `2`.
- كل Bridge ID موجود في الـ Solution لازم يكون موجود في قائمة الـ Candidate Bridges المرتبطة بيه.
- أي Bridge ID مش موجود في الـ Map معناه إن عدد جسوره `0`.
- الـ Chromosome لازم يكون فيه Gene واحدة بالضبط لكل Candidate Bridge.
- كل Chromosome gene لازم تكون Integer من `0` لـ `2`.

أي Invalid values **MUST** يتم الإبلاغ عنها. وممنوع الـ Implementations تحوّل قيم زي `"2"` أو `2.5` أو `-1` أو `3` بشكل تلقائي لقيم Bridge counts صحيحة.

---

## 12. Design Decisions That Must Remain Consistent

القرارات دي أساسية ولازم تفضل موحدة في كل أجزاء المشروع:

1. اسم حقل الـ Island هو `required_bridges` بالضبط.
2. الإحداثيات Zero-based وبتستخدم `row` و`col`.
3. الـ Candidate Bridge endpoints بتكون Island ID strings داخل `from` و`to`.
4. `from` هي الجزيرة اللي على الشمال أو فوق، و`to` هي الجزيرة اللي على اليمين أو تحت.
5. قيمة Candidate Bridge orientation لازم تكون `horizontal` أو `vertical` بالضبط.
6. توليد الـ Candidate Bridges بيعتمد على أقرب الجزر الظاهرة فقط.
7. ترتيب توليد الـ Candidate Bridges هو: ترتيب الجزر حسب `row` وبعده `col`؛ ولكل جزيرة نضيف Right/Horizontal الأول وبعده Down/Vertical.
8. الـ Candidate Bridge IDs بتتحدد بالتسلسل `E1..En` حسب نفس ترتيب الإضافة.
9. عدد الجسور الفعلي بيتخزن في `Solution.bridge_counts` أو في الـ positional Chromosome المقابل ليه فقط، ومش داخل تعريف الـ Candidate Bridge.
10. كل Solution bridge count وكل Chromosome gene لازم يكون Integer من `0` لـ `2`.
11. أي Solution bridge ID مش موجود بيتحسب كأنه `0`، لكن أي ID غير معروف يعتبر Invalid.
12. الـ Chromosome index رقم `i` لازم يطابق Candidate Bridge list index رقم `i` دائمًا.
13. الـ Validation لازم يستخدم نفس الـ Canonical Structures ويرجع الخمس Fields المطلوبة في الـ Validation Report.

---

## 13. Review and Approval — المراجعة والاعتماد

المستند ده عبارة عن Proposed Shared Contract، ولازم الفريق يراجعه قبل ما يبدأ Implementation.

كل Reviewer المفروض يأكد إن الـ Data Model مناسب للـ Component المسؤول عنه، ويضيف Approval comment واضح على الـ Pull Request.

| Reviewer | Review focus | Approval |
|---|---|---|
| Monzer | Candidate Bridge generation، وقواعد الـ endpoints، والـ deterministic ordering والـ IDs | Pending |
| Ebrahim | Degree calculation، وCrossing detection، والـ Connectivity، والـ Validation Report | Pending |
| Rovan | Candidate Bridge-to-Gene mapping، وطول الـ Chromosome، وقيم الـ genes | Pending |
| UI team member | توافق الـ UI output مع `Puzzle` و`Island` | Pending |
| Mostafa | مراجعة الاتساق العام والـ cross-component integration | Owner review pending |

### Suggested Review Questions

- **Candidate Bridge Generator:** هل الـ Generator يقدر ينتج نفس القائمة المرتبة دي بالضبط من الـ Puzzle، من غير أي غموض في قاعدة أقرب جزيرة ظاهرة أو طريقة تحديد الـ IDs؟
- **Validator:** هل كل Validation checks المطلوبة ممكن تتحسب من الـ Puzzle وقائمة الـ Candidate Bridges والـ Solution؟ وهل الـ Report fields والـ invalid-value entries كفاية؟
- **GA / MA:** هل كل Candidate Bridge ممكن يرتبط بـ Gene واحدة بالضبط، ويحتفظ بنفس المعنى أثناء الـ initialization والـ crossover والـ mutation والـ local search؟
- **UI:** هل الـ UI يقدر يطلع Puzzle وIsland JSON بنفس الـ Fields المطلوبة، من غير إعادة تسمية أو إضافة Fields خاصة بالـ Algorithms؟

### Approval Condition

الـ Data Model يعتبر Approved فقط بعد ما أعضاء الفريق المسؤولين يراجعوا الـ Pull Request ويأكدوا بشكل صريح إن الـ Contract متوافق مع الـ Components بتاعتهم. لحد ما ده يحصل، المستند يفضل في حالة Design-review Draft.

---

## 14. Change Control — Data Model Freeze

بعد ما الـ Pull Request ياخد Approval ويتعمله Merge إلى `develop`، المستند ده هيبقى الـ Official Shared Data Model للمشروع، وهيعتبر **FROZEN** أثناء مرحلة الـ Implementation.

بعد الـ Freeze:

1. ممنوع أي Component يغيّر بشكل منفصل اسم أو Type أو Meaning أو Ordering rule أو JSON shape لأي Shared Field.
2. أي Change مقترح **MUST** يتناقش الأول مع Mostafa (Data Model Owner) قبل الـ Implementation.
3. اقتراح التغيير **MUST** يوضح السبب، والـ Structures المتأثرة، والـ Components المتأثرة، وتأثير التغيير على الـ Integration.
4. الـ Component owners المتأثرين بالتغيير **MUST** يراجعوا الاقتراح.
5. أي Change تتم الموافقة عليه **MUST** يتنفذ من خلال Pull Request، ولازم يتم إبلاغ الفريق كله بيه.
6. الـ Implementations لازم تتحدث مع بعض، علشان الـ Repository ميبقاش فيه Components بتستخدم Versions مختلفة وغير متوافقة من الـ Contract.

**Freeze Announcement — يتبعت بعد ما الـ Approved PR يتعمله Merge:**

> Data Model Frozen. الـ Shared Contract الموجود في `docs/DATA_MODEL.md` تمت مراجعته وعمل Merge ليه في `develop`. كل Components المشروع لازم تلتزم بيه باعتباره الـ Single Source of Truth. أي تغيير مقترح لازم يتناقش مع الـ Data Model Owner ويتراجع تأثيره على باقي الـ Components قبل تنفيذه.

---

## 15. Definition of Done (DoD)

- [ ] ملف `docs/DATA_MODEL.md` موجود في الـ Repository.
- [ ] الـ Puzzle والـ Island structures موضحين بكل أسماء الـ Fields والـ Types الصحيحة.
- [ ] الـ Candidate Bridge structure واتجاه الـ endpoints موضحين.
- [ ] قاعدة أقرب جزيرة ظاهرة (nearest visible island) مكتوبة بشكل صريح.
- [ ] الـ Deterministic Candidate Bridge ordering وطريقة ترقيم `E1..En` موضحين بمثال.
- [ ] تم توضيح تمثيل الـ Solution وقاعدة أعداد الجسور `0` و`1` و`2`.
- [ ] الـ Candidate Bridge IDs غير الموجودة في الـ Solution بتتعامل كأنها `0`، والـ Unknown IDs بتعتبر Invalid.
- [ ] طول الـ Chromosome وقاعدة الـ Gene-to-Edge mapping موضحين.
- [ ] الـ Validation Report structure ومعنى كل Field موضحين.
- [ ] مثال P1 كامل موجود، وبيشمل Puzzle وCandidate Bridges وSolution وChromosome وValidation Report.
- [ ] Monzer وEbrahim وRovan وUI owner راجعوا الـ PR ووافقوا عليه بشكل صريح.
- [ ] الـ PR اتعمله Merge إلى `develop` قبل Implementation PRs.
- [ ] الفريق استلم إعلان إن الـ Data Model بقى Frozen.

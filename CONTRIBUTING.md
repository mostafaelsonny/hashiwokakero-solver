# دليل المساهمة

> الشرح التفصيلي خطوة بخطوة (مع الأوامر) في [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md). الملف ده ملخص القواعد.

**حماية الـ repo:** `main` و`develop` عليهم Rulesets (PR إجباري، موافقة واحدة من Mostafa، إلغاء الموافقة القديمة عند أي تعديل، حل كل التعليقات قبل الـ Merge، منع Force Push وحذف الـ branch). الأعضاء بصلاحية Write، و**Mostafa Admin وهو الوحيد المراجع والمسؤول عن الـ Merge**.

## الـ Branches
```
main      النسخة المستقرة (بتتحدّث في آخر كل Sprint بعد Sprint Review)
develop   اللي بنجمع عليه الشغل كل يوم
feature/* كل مهمة ليها branch من develop   (مثال: feature/candidate-generator)
docs/*    مستندات وتصميمات                  (مثال: docs/ga-design)
fix/*     إصلاح أخطاء
```
أسماء الـ branches الرسمية لمهام Sprint 1: `docs/data-model` • `feature/candidate-generator` • `feature/crossing-detector` • `feature/degree-validator` • `feature/connectivity-checker` • `feature/solution-validator` • `docs/backtracking-design` • `docs/ga-design` • `docs/ma-design` • `feature/puzzle-editor` • `feature/core-integration-tests`

**ممنوع** الـ push المباشر على `main` أو `develop`. كله بـ Pull Request.

## ازاي تشتغل على تاسك (Workflow)
1. خد التاسك من Trello (الكارت فيه الوصف الكامل والـ Acceptance Criteria).
2. `git checkout develop && git pull && git checkout -b feature/<اسم-المهمة>`
3. اتبع [docs/AI_WORKFLOW.md](docs/AI_WORKFLOW.md): افهم ← Spec ← Pseudocode ← Tests ← AI ← مراجعة ← تجربة.
4. commits صغيرة برسائل واضحة، مثال: `S1-03: generate candidate edges for horizontal links`
5. شغّل `make test` قبل ما تفتح PR. لو الاختبارات بتاعتك بتعدي، **امسح علامة xfail** من ملف الاختبار.
6. افتح PR على `develop` واملا الـ Template بالكامل.
7. استنى مراجعة Mostafa. ماتعملش Merge بنفسك.
8. حرّك الكارت في Trello: In Progress ← Code Review ← Testing ← Done.

## قواعد الـ Pull Request
- PR واحد لكل Task صغيرة. مفيش PR بـ 1000 سطر في آخر الأسبوع.
- لازم الكود يستخدم نفس الـ Data Model بالحرف (`docs/DATA_MODEL.md`).
- لازم Tests: Normal + Invalid + Edge.
- صاحب الـ PR لازم يقدر يشرح الكود بكلامه.

## قائمة مراجعة Mostafa (5 نقاط)
1. **Requirements:** الكود بينفذ فعلًا المطلوب؟
2. **Data Compatibility:** الحقول مطابقة للـ Data Model بالحرف؟
3. **Logic Correctness:** المنطق صح (مش بس شغال)؟
4. **Testing:** Normal / Invalid / Edge موجودين وبيعدّوا؟
5. **Integration:** بيتوصل بسهولة بباقي الـ Modules؟ لو لأ، مفيش Merge.

## ترتيب الـ Merge في Sprint 1
1. `docs/data-model`  2. `feature/candidate-generator`  3. `feature/crossing-detector`  4. `feature/degree-validator`  5. `feature/connectivity-checker`  6. `feature/solution-validator`  7. `feature/puzzle-editor`  8. `docs/ga-design` و`docs/ma-design` و`docs/backtracking-design`

## تغيير الـ Data Model
بعد ما S1-02 يتقفل، **ممنوع** حد يغيّر أسماء حقول أو طريقة التمثيل. أي اقتراح يتبعت لـ Mostafa الأول، وهو يراجع تأثيره على كل الأجزاء، وبعدها يتعدّل `docs/DATA_MODEL.md` في PR مستقل.

## Definition of Done (لأي تاسك)
- [ ] الكود/المستند متراجع ومتعمله Merge على `develop`.
- [ ] Tests موجودة وبتعدّي (وعلامة xfail اتشالت).
- [ ] صاحب التاسك فاهم الكود ويقدر يشرحه.
- [ ] متوافق مع `docs/DATA_MODEL.md`.
- [ ] الـ Acceptance Criteria في كارت Trello كلها متحققة.

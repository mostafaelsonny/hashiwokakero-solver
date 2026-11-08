# دليل القائد (Mostafa)

إنت **Admin** والوحيد المسؤول عن مراجعة الكود والـ Merge. باقي الأعضاء **Write** وبيشتغلوا على branches بتاعتهم بـ PRs.

## 1) إنشاء الـ repo وضبطه (مرة واحدة)
**بالسكريبت (الأسرع):** من جذر المشروع، بعد `gh auth login`:
```bash
COLLABORATORS="monzer-username ebrahim-username rovan-username febronia-username" ./scripts/setup_github.sh hashiwokakero-solver public
```
بيعمل: repo + `main` + `develop` (default = develop) + Labels + Milestones + **Rulesets** + دعوات Write.

**يدويًا:** ارفع المشروع، أنشئ `develop`، `Settings → Rules → Rulesets → New ruleset → Import` للملفين في `.github/rulesets/`، وادعُ الأعضاء بصلاحية **Write** (`Settings → Collaborators`).

**بعد الإنشاء:**
1. استبدل `REPO_URL` في `docs/GIT_WORKFLOW.md` والـ guides برابط الـ repo (`grep -rn REPO_URL docs`).
2. فعّل `.github/CODEOWNERS` لما كل واحد يديك الـ username.
3. راجع **Bypass list** في كل Ruleset: لازم تحتوي **Admin role بس** (إنت)، ومفيش أي عضو فريق.

## 2) مراجعة PR (الروتين)
1. افتح الـ PR، اقرا الوصف (اللي اتعمل، شرح الكود، الاختبارات، التوافق مع Data Model).
2. تبويب **Files changed**: راجع بالـ 5 نقاط:
   1. **Requirements:** بينفذ المطلوب فعلًا؟
   2. **Data Compatibility:** الحقول مطابقة للـ Data Model بالحرف؟
   3. **Logic Correctness:** المنطق صح (مش بس شغال)؟ (مثلاً الاتصال من الجسور الفعلية)
   4. **Testing:** Normal / Invalid / Edge موجودين، وعلامة `xfail` اتشالت؟
   5. **Integration:** بيتوصل بباقي الـ Modules بسهولة؟ مفيش منطق متكرر من `core/`؟
3. اسأل صاحب الـ PR سؤال أو اتنين عن الكود (يتأكد إنه فاهمه).
4. **Review changes** ← **Approve** أو **Request changes** (وحط تعليق على كل نقطة).
5. بعد ما صاحب الـ PR يصلّح ويحل التعليقات (القاعدة بتمنع الـ Merge من غير كده): راجع التعديلات ← **Approve**.
6. **Squash and merge** ← **Delete branch**. وحرّك كارت Trello لـ Done.

> ⚠️ لو صاحب الـ PR عدّل بعد Approve، الـ Approve بيتلغي تلقائيًا (Dismiss stale approvals). راجع تاني.

## 3) ترتيب الـ Merge في Sprint 1
1. `docs/data-model`  2. `feature/candidate-generator`  3. `feature/crossing-detector`  4. `feature/degree-validator`  5. `feature/connectivity-checker`  6. `feature/solution-validator`  7. `feature/puzzle-editor`  8. `docs/backtracking-design` و`docs/ga-design` و`docs/ma-design`
**S1-07 مابتتدمجش قبل S1-03/04/05/06.**

## 4) لو حصل Conflict في PR
اطلب من صاحب الـ PR يعمل `git merge origin/develop` على branch بتاعته ويحلّه (الخطوات في GIT_WORKFLOW.md خطوة 4). لو الـ Conflict في ملف Core أو Data Model، اقعد معاه وحلّوه سوا، وبعدها شغّل الاختبارات.

## 5) آخر كل Sprint
بعد الـ Sprint Review وقبول المهام: افتح PR من `develop` إلى `main` (ده ال Release بتاع الـ Sprint).

## 6) PRs بتاعتك إنت (القرار اتاخد)
GitHub مابيسمحش لصاحب الـ PR يوافق على PR بتاعه، فالـ Rulesets فيها **Bypass لـ Admin role بنمط `pull_request`**: إنت بس (كـ Admin) تقدر تدمج PR بتاعك (S1-02 وS1-12 والدمج في `main`) بعد ما تراجعه بنفسك. الأعضاء Write مالهمش أي Bypass، وإنت كمان **مش بتقدر تـ push مباشرة**، لازم PR.
في الـ JSON: `"bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request"}]`

## 7) روتينك اليومي
- راجع الـ PRs مرتين في اليوم (ماتبقاش Bottleneck).
- حدّث Trello، وراجع الـ Standup.
- كل يوم: `develop` لازم يبقى بيعدّي `python -m pytest -q`.
- أي تغيير في Data Model بييجي ليك الأول.

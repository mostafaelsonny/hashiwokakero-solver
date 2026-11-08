# دليل Git و GitHub لكل عضو

> اتبع الخطوات بالترتيب. لو حاجة مش واضحة، اسأل Mostafa **قبل** ما تجرب حاجة مش فاهمها.
> الرابط الفعلي للـ repo: `REPO_URL` (هيتحدّث هنا بعد الإنشاء).

## 0) الإعداد مرة واحدة بس
```bash
git clone REPO_URL
cd hashiwokakero-solver
git config user.name  "اسمك"
git config user.email "ايميل-حسابك-على-GitHub"
git checkout develop

python -m venv .venv
# Windows:    .venv\Scripts\activate
# Mac/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q          # لازم يطلع: passed + xfailed (مفيش failed)
```
الـ Frontend (للي هيشتغل عليه): `cd frontend && npm install && npm run dev`.

## 1) الصلاحيات والقواعد (اتطبقت على الـ repo)
| الدور | الصلاحية |
|---|---|
| Mostafa | **Admin**، وهو الوحيد المسؤول عن المراجعة والـ Merge |
| باقي الأعضاء | **Write**: تعمل branches وتـ push عليها وتفتح PRs، لكن **مش بتتحكم في إعدادات الحماية** |

القواعد على `main` و`develop` (Rulesets: "Protect Main Branch" و"Protect Develop Branch"):
| القاعدة | الحالة | معناها ليك |
|---|---|---|
| Require a pull request before merging | ON | **ممنوع push مباشر**، كله عن طريق PR |
| Require approvals (1) | ON | لازم موافقة من Mostafa |
| Dismiss stale approvals | ON | لو عدّلت كود بعد الموافقة، الموافقة بتتلغي ولازم مراجعة تانية |
| Require conversation resolution | ON | ممنوع Merge لو فيه تعليقات مراجعة لسه ما اتحلتش |
| Block force pushes | ON | `git push --force` مش هيشتغل |
| Restrict deletions | ON | محدش يقدر يحذف `main` أو `develop` |

يعني الشغل **بيتعمل بس على branch بتاعتك**، وبيوصل لـ `develop` بـ PR.

## 2) تبدأ تاسك جديدة (Branch خاصة بيك)
**كل Task ليها Branch لوحدها.** ماتشتغلش على `develop` ولا على branch حد تاني.
```bash
git checkout develop
git pull origin develop                      # الأول: آخر نسخة
git checkout -b feature/candidate-generator  # اسم الـ branch من كارت Trello
```
الأسماء الرسمية لـ Sprint 1: `docs/data-model` • `feature/candidate-generator` • `feature/crossing-detector` • `feature/degree-validator` • `feature/connectivity-checker` • `feature/solution-validator` • `docs/backtracking-design` • `docs/ga-design` • `docs/ma-design` • `feature/puzzle-editor` • `feature/core-integration-tests`

## 3) الشغل اليومي (commit و push)
```bash
git status                       # شوف إيه اللي اتغيّر
git add core/candidate_generator.py tests/test_candidate_generator.py
git commit -m "S1-03: generate candidate edges for horizontal links"
git push -u origin feature/candidate-generator     # أول مرة بس
git push                                           # بعد كده
```
- commits صغيرة وكتير، ورسالة واضحة فيها رقم التاسك.
- **ادفع (push) آخر كل يوم** عشان شغلك يبقى محفوظ.
- ماتعملش `git add .` من غير ما تشوف `git status` (ماتضيفش ملفات مش بتاعتك).

## 4) حدّث branch بتاعتك أول بأول (عشان ماتشتغلش على حاجة قديمة)
**أول كل يوم وقبل ما تفتح PR:**
```bash
git checkout feature/candidate-generator
git fetch origin
git merge origin/develop
python -m pytest -q
git push
```
### لو ظهر Conflict
Git هيقولك `CONFLICT` وهيعلّم الملفات. ده طبيعي:
1. افتح الملف وادوّر على العلامات:
   ```
   <<<<<<< HEAD
   (كودك)
   =======
   (الكود اللي جاي من develop)
   >>>>>>> origin/develop
   ```
2. قرر الصح (ممكن تجمع الاتنين)، **وامسح العلامات الـ 3**.
3. `git add <الملف>` ثم `git commit` (بيكمّل الـ merge).
4. شغّل `python -m pytest -q` وتأكد إن كله سليم.
5. `git push`.

لو اتلخبطت: `git merge --abort` بيرجعك لقبل الـ merge. ولو الـ Conflict في ملف مش بتاعك أو مش فاهمه، **كلّم Mostafa قبل ما تحله**.

## 5) تفتح Pull Request صح
1. اتأكد إنك عملت خطوة (4) وكل الاختبارات بتعدّي، وإنك شلت علامة `xfail` من ملف الاختبار الخاص بالـ Module لو اتنفذ.
2. على GitHub هتلاقي شريط أصفر **Compare & pull request** بعد الـ push (أو من تبويب Pull requests ← New).
3. **base: `develop`  ←  compare: branch بتاعتك.** (مش `main`!)
4. العنوان: `S1-03: Candidate Edge Generator`.
5. املا الـ Template كله (اللي اتعمل، الكود بيشتغل ازاي بكلامك، الاختبارات، التوافق مع Data Model).
6. على اليمين: **Reviewers: Mostafa**، **Assignees: إنت**، وحط Label الـ Sprint.
7. اربط كارت Trello في الوصف وحرّكه لـ **Code Review**.
8. الـ PR الصغير (Task واحدة) أحسن بكتير من PR كبير. لو لسه شغال، افتحه **Draft**.

## 6) تستقبل نتيجة المراجعة
افتح الـ PR ← تبويب **Conversation**. هتلاقي واحدة من الحالات دي:

| الحالة | تعمل إيه |
|---|---|
| ✅ **Approved** | Mostafa بيعمل Merge (**إنت ماتعملش Merge بنفسك**). حرّك الكارت لـ Testing/Done بعد الدمج |
| 🔁 **Changes requested** | اقرا كل تعليق، عدّل **على نفس الـ branch**، `git add` + `commit` + `push` (الـ PR بيتحدّث تلقائيًا) |
| 💬 تعليقات بس | ردّ على كل تعليق |

بعد ما تصلّح تعليق:
1. ردّ عليه: "اتعدّل في commit كذا".
2. دوس **Resolve conversation** (القاعدة بتمنع الـ Merge قبل ما كل التعليقات تتحل).
3. اطلب من Mostafa **Re-request review** (أو بلّغه).

> ⚠️ لو عدّلت بعد الـ Approve، الـ Approve بيتلغي (Dismiss stale approvals). ده طبيعي، اطلب مراجعة تانية.
> لو الـ PR ظهر عليه **"This branch has conflicts"**: نفّذ خطوة (4) وادفع.

## 7) بعد الـ Merge
```bash
git checkout develop
git pull origin develop
git branch -d feature/candidate-generator      # امسح الـ branch المحلية
```
(الـ branch على GitHub بتتمسح بزرار **Delete branch** بعد الـ Merge.) وبعدها ابدأ التاسك اللي بعدها من خطوة (2).

## 8) روتين يومي (5 دقايق)
- **أول اليوم:** `git checkout develop && git pull origin develop` ← ارجع لـ branch بتاعتك ← `git merge origin/develop` ← `pytest`.
- **أثناء الشغل:** commits صغيرة، شغّل `pytest` قبل كل push.
- **آخر اليوم:** commit + push + حدّث كارت Trello + اكتب في الـ Standup: عملت إيه / هعمل إيه / إيه معطلني.

## 9) لو حصلت غلطة
| المشكلة | الحل |
|---|---|
| `git push` على develop اترفض | **ده مقصود**. اعمل branch وافتح PR |
| عدّلت كود على `develop` ولسه ماعملتش commit | `git checkout -b feature/اسم-المهمة` (التعديلات بتيجي معاك) |
| عملت commit على `develop` بالغلط (من غير push) | `git branch feature/اسم-المهمة` ثم `git reset --hard origin/develop` ثم `git checkout feature/اسم-المهمة` |
| عايز ألغي آخر commit (من غير push) | `git reset --soft HEAD~1` |
| عايز أرجّع ملف لآخر commit | `git restore <الملف>` |
| محتاج أبدّل branch ومعايا تعديلات مش جاهزة | `git stash` ثم `git checkout ...` ثم `git stash pop` |
| مش عارف أنا فين | `git status` و`git branch` و`git log --oneline -5` |

**ممنوع:** `git push --force`، الشغل على `main` أو `develop` مباشرة، `git reset --hard` من غير ما تفهمه، تعديل ملفات شخص تاني بدون اتفاق.

## 10) Cheat sheet
```
git status                     حالة الشغل
git branch                     الـ branches المحلية
git checkout <branch>          انتقل لـ branch
git pull origin develop        نزّل آخر تحديثات develop
git fetch origin               هات آخر المعلومات من GitHub من غير دمج
git merge origin/develop       ادمج تحديثات develop في branch بتاعتك
git add <files>                جهّز الملفات للـ commit
git commit -m "S1-xx: ..."     احفظ commit
git push                       ارفع على GitHub
git log --oneline -5           آخر 5 commits
```

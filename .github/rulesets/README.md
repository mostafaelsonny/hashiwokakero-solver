# Rulesets (حماية main و develop)

الملفين `protect-main.json` و`protect-develop.json` بيطبّقوا **بالظبط** القواعد المتفق عليها:

| إعداد GitHub | الحالة | في الـ JSON |
|---|---|---|
| Ruleset Name | Protect Main Branch / Protect Develop Branch | `name` |
| Enforcement Status | Active | `"enforcement": "active"` |
| Target Branches | `main` / `develop` | `conditions.ref_name.include` |
| Require a pull request before merging | ON | قاعدة `pull_request` |
| Require approvals | ON، عدد 1 | `required_approving_review_count: 1` |
| Dismiss stale approvals | ON | `dismiss_stale_reviews_on_push: true` |
| Require conversation resolution | ON | `required_review_thread_resolution: true` |
| Block force pushes | ON | قاعدة `non_fast_forward` |
| Restrict deletions | ON | قاعدة `deletion` |
| Bypass list | **Admin role فقط (Mostafa)** بنمط `pull_request`، مفيش أعضاء فريق | `bypass_actors` |
| Require status checks | **مش مفعّلة** لحد ما CI يشتغل | (مش موجودة) |

## تطبيقها يدويًا
`Settings → Rules → Rulesets → New ruleset → Import a ruleset`، اختار الملف، وراجع إن Enforcement = Active، وكرر لـ develop.

## تطبيقها بالسكريبت
`scripts/setup_github.sh` بيعملها تلقائيًا (بعد ما بيرفع `main` و`develop`).

## ملاحظات
- الـ repo **Public** (Rulesets مجانية على الـ Public repos).
- GitHub مابيسمحش لصاحب الـ PR إنه يوافق على PR بتاعه، فـ Mostafa (Admin) هو الوحيد في الـ Bypass list بنمط `pull_request`: يقدر يدمج PR بتاعه بعد ما يراجعه، **ومش بيقدر يـ push مباشرة**. الأعضاء Write مالهمش أي Bypass.

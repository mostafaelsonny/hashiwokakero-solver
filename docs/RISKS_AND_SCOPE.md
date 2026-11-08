# Scope & Risks

## الـ Scope
| الحاجة | القرار |
|---|---|
| Backtracking، GA، MA، Graph Theory، Puzzle Input، Algorithm Selection، Visualization | **Must Have** |
| Live Animation، إحصائيات متقدمة، تحسينات Optimization | Optional (بعد ما كل الـ Must يخلصوا) |
| Database، Authentication، Cloud Deployment، UI/UX متقدم | **مش مطلوب** |
| ML / Deep Learning / Neural Networks / LLM | **استبعاد** |
| Microservices، Docker Orchestration | استبعاد |
| Advanced Graph Theory / Advanced GA / Advanced Math Optimization | استبعاد |

**قاعدة تغيير الـ Scope:** هل غيابها بيمنعنا من تحقيق متطلبات المشروع الأساسية؟ لو لأ، تتأجل لما بعد الـ MVP.

## القرارات الإدارية الثلاثة
1. نبدأ بأبسط Implementation لكل Algorithm، ومفيش Optimization قبل ما الأساسية تشتغل.
2. الـ Frontend أبسط شكل يحقق المتطلبات.
3. Integration بدري، مش في الأسبوع الرابع.

## Risk Register
| الخطر | التأثير | العلاج |
|---|---|---|
| Incorrect Mathematical Model | فشل الخوارزميات التلاتة | مراجعة الـ Model والـ Data Model قبل التنفيذ (S1-02) |
| Poor Fitness Function | GA وMA مش هيوصلوا لحلول صحيحة | تجارب وقياس ومراجعة الأوزان، وFitness بيستخدم دوال Core |
| Different Data Structures | مشاكل Integration | Data Model واحد متجمّد + `docs/DATA_MODEL.md` |
| AI-generated Bugs | نتائج غير صحيحة | Tests + Code Review + قاعدة "ممنوع Merge من غير فهم" |
| Delayed Integration | مشاكل كتير في الآخر | دمج كل يوم وPRs صغيرة |
| Pruning غلط في Backtracking | يقول "مفيش حل" وهو موجود | مقارنة النتائج بحلول معروفة + Tests |
| GA/MA مش بيلاقوا حل | حالة فشل | نعرض `No Valid Solution Found Within Search Limits` ونقارن مع Backtracking |
| Scope Creep | مانخلصش في 4 أسابيع | قاعدة الـ Scope فوق |
| عضو متأخر أو غايب | Bottleneck | أي Module لازم شخص تاني يفهمه ويقدر يكمله |
| انضمام Febronia متأخر | S1-10 وS1-11 متأخرين | Mostafa بيتابع الجزء النظري لحد ما ينضم |

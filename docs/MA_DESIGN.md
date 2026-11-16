# MA DESIGN

- **المسؤول:** Febronia
- **المهمة:** S1-10 (كارت Trello فيه الوصف الكامل والـ Acceptance Criteria)
- **الموعد:** Day 3-4 من Sprint 1
- **الحالة:** TODO

> مستند فاضي (Template). امسح الملاحظة دي واملا الأقسام المطلوبة بكلامك. لازم تفهم اللي بتكتبه.

## الأقسام المطلوبة

### 1. ازاي بنستخدم GA كأساس

الـ GA بتعتمد على فكرة التطور في الطبيعة.

بتعمل الأول Population (مجموعة حلول عشوائية) بناءً على الـ Chromosomes (الكروموسومات).

الكروموسوم ده عبارة عن:

0: يعني مفيش جسر.

1: يعني جسر واحد.

2: يعني جسرين.

وبناءً على الحلول العشوائية (Random Solutions) دي، بنعمل Crossover (تزاوج) وMutation (طفرة) عشان نختار أحسن حل.

بنختار أحسن حل إزاي؟ بـ Function اسمها Fitness، واللي بتقيس إيه أحسن حاجة بناءً على الـ Penalty (يعني كل ما الأخطاء تقيل والـ Penalty يقل، يبقى ده أحسن حل).

إيه بقى التغيير والتطوير في الـ MA؟
عشان نحيد البطء ده، الفكرة في الـ MA إننا مش هنكتفي بس بالحلول العشوائية والطفرات بتاعة الـ GA ونستنى كتير، لا.. إحنا بنحسن الـ Population دي بـ تكنيك اسمه Local Search:

إيه هو الـ Local Search؟

فكرته إنه بيبدأ من النقطة اللي أنا واقفة فيها.

وبناءً على النقطة دي، بيشوف إيه الحلول الممكنة عن طريق إنه بيص على الجيران اللي حواليه (Neighborhood).

بيشوف كل جار فيهم، وياخد أفضل واحد مناسب بيحسن الـ Fitness وبيقلل الـ Penalty.

طب بيشتغل بـ Algorithm إيه؟

الـ Local Search بيكون معتمد على خوارزمية اسمها Hill Climbing.

يعني وأنا شغالة بالـ Local Search بفضل ماشية بمبدأ الـ Hill Climbing: إني هفضل آخد أحسن واقرب جار

### 2. Hill Climbing


هو التكنيك الأساسي اللي أنا بمشي بيه جوه الـ Local Search.

فكرة الـ Hill Climbing وعمومها:
فكرتها ببساطة كأننا بنحاول نوصل لأحسن نقطة (القمة)، بس الفكرة إننا مش بتبقا شايفين الطريق كله قدامنا مرة واحدة.

عشان كده بتمشي بطريقة ذكية: بمسك الحل اللي أنا واقفة عنده، وبشوف إيه أحسن حلول حواليا اللي هما الجيران (Neighborhood)، وبختار أفضل واحد فيهم.

إزاي بوصل للهدف بالـ Hill Climbing جوه الـ Local Search؟
ببدأ من الحل الحالي اللي وصلتلنا الـ GA.

بطبق الـ Local Search، وخلال الشغل ده بعتمد على تكنيك الـ Hill Climbing.

الـ Hill Climbing بيخليني أبص حواليا على الحلول الممكنة (الجيران)، وأقارن بينهم.

بختار أحسن جار يوصلني للهدف (اللي هو يقلل الأخطاء ويوصل الـ Penalty لـ 0)، وأفضل ماشية بالخطوة دي لحد ما أوصل لأحسن نتيجة ممكنة.

### 3. الـ 4 Operators: Degree Repair / Crossing Repair / Connectivity Repair / Bridge Reallocation (كل واحد: بيعمل إيه، إمتى، شروطه)

):
Degree Repair (علاج الدرجات)
دي بتبسط بناءً على إني بشوف كل جزيرة، لو العدد اللي فيها زايد (أكتر من المطلوب) أو ناقص (عجز)، بصلحه وأظبطه.

Crossing Repair (فك التقاطعات):

دي لو لقيت فيه تقاطع بين جسرين، بصلحه فوراً، لأننا عارفين من قواعد اللعبة إنه ممنوع منعاً باتاً إن أي جسرين يقطعوا على بعض.

Connectivity Repair (توصيل الشبكة):

دي لما ألاقي الجسور أو الجزر متفرقة عن بعض، بقوم أربطهم وأسوّي الرسمة على بعضها عشان تبقوا مناسبة للحل، وأقدر أوصل ما بين كل جزيرة والثانية بسهولة ومن غير عزل.

Bridge Reallocation (إعادة توجيه الجسور):

دي بقى لما ألاقي مكان عليه ضغط وجسور زيادة، فبأخد جسر من الزحمة دي وأنقله لمكان تاني محتاجه وفيها عجز عشان أظبط الدنيا.

### 4. إمتى نطبق Local Search ولية

بنطبقه عشان نتخلص من مشكلة البطء اللي بتحصل في الخوارزمية، ولأننا عايزين نسرّع من عملية البحث ونوصل للحل الصح بسرعة، بدل ما نفضل مستنيين العشوائية تاخد وقت طويل

بنطبقه بناءً على الـ Population (المجتمع والحلول اللي بتظهر عندنا) من الـ GA، فبدل ما نسيب الحلول دي عشوائية أو بطيئة، بندخل الـ Local Search في اللحظة دي عشان يمسك الحلول دي ويحسّنها ويجيب من الآخر وبأسرع وقت.

### 5. حد أقصى لعدد خطوات الـ Local Search

الـ Max Local Search، أو إيه هو الحد الأقصى بتاع الـ Local Search، هو كل فكرته إن أنا مش هينفع أسيب الـ Local Search من غير حد معين أو من غير رقم من غير حاجة معينة، لازم أحدد له حاجة يقف عندها. ليه؟ لأني لو ما حددتلهوش هيفضل يلف في الـ Infinite Loop وكده مش هيخلص وهيفضل ياكل من الجهاز ويتعب وياخد من الـ RAMs والحاجات اللي زي كده، فهو مش هيقدر فلازم أحط له Max Iterations رقم معين يقف عنده.

### 6. ازاي بنقيس التحسن

دلوقتي إزاي بنقيس التحسن؟ إحنا بنقيس التحسن بناءً على Function اسمها الـ Fitness Function.

الـ Fitness Function دي زي الحكم أو زي القاضي، بتقيس كل حاجة تحسنت وبتقيس درجة التحسن بتاعها قد إيه.

طب الـ Fitness Function دي بتقيس بناءً على إيه؟
بتقيس بناءً على الـ Penalty.

إيه هي الـ Penalty؟
الـ Penalty دي هي عدد الغرامات أو عدد الأخطاء، يعني إيه؟ يعني عدد الحاجات الموجودة في النظام الغلط، زي إيه؟

يعني مثلاً جزيرة مكتوب جواها رقم 3 وجينا بصينا لقيناها متوصلة بـ 2 بس، فدي طبعاً غلطة وهتزود الـ Penalty بـ 1.

لو جسرين قاطعين على بعض، فدي غلطة وهتزود الـ Penalty بـ 1.

لو الشبكة مفصولة ومفروضة وكل جزء بعيد عن الثاني، فدي Penalty وهتزود الـ Penalty بـ 1.

فكده عرفنا إن:
الـ Penalty العالي: معناه إن فيه غلطات كتير وده مش بختاره خالص.

الـ Penalty القليل: معناه إن عدد غلطاته قليل وده بيكون أحسن حل عندي.

وبنقول إن حصل تحسن (Improvement) لما الحل الجديد أو الجار الناتج من الـ Local Search يطلع بـ Penalty أقل من الحل القديم، ونفضل مستمرين لحد ما نوصل لـ Penalty = 0 وده الحل المثالي للغز

### 7. Pseudocode

ـ Pseudocode بتاع الـ Memetic Algorithm (MA)
السودوكود عندنا بيتقسم لأكتر من حاجة:

أول حاجة، الـ Population المبدئي: دي إحنا أصلاً بنتكلم على إن إحنا بنولد الـ Solutions عشوائية وبنحسب لكل واحدة الـ Penalty بتاعها، إزاي بنحسبها؟ بالـ Fitness Function.

تاني حاجة، الـ Evolutionary Loop: إيه هو الـ Loop بتاعنا أصلاً بتاع الـ GA؟ إن إحنا نطلع أحسن حاجة، بنطلع أحسن حاجة إزاي؟ إننا بنختار جزء منهم (Selection)، بعد ما بنعمله بنعمل إن إحنا نجوزهم لبعض (Crossover)، وبعد كده بنعمل الـ Mutation عشان نطلع طفرة وتبقى حاجة أجدد كمان من كله. يعني إحنا بنعمل تلات حاجات: Selection، Crossover، ممكن نعمل حاجة اسمها الـ Mutation اللي هي الطفرات.

تالت حاجة، الـ Local Search: لا إحنا تالت حاجة هنعملها بقى الـ Local Search، ده إيه؟ ده تطوير للـ GA! يعني بدل ما أنا بعمل Crossover وMutation بس، لا، أنا بطلع فعلاً شوية حلول بس أنا ببدأ من النقطة اللي أنا فيها، بحط Max Local Iterations عشان الجهاز ما يفضلش يدخل في Infinite Loop ويفضل ياكل في الرامات والحاجات دي، وبقول له اشتغل بالـ Hill Climbing (يعني اشتغل من النقطة اللي أنت فيها وابتدي أنك بص على الجيران اللي حواليك واختار أحسن حل بالنسبة لك بناءً على الـ Penalty اللي اسمه Fitness Function). بناءً على الـ Penalty ده بص حواليهم واختار الـ Best Solution، وإيه هدف الـ Hill Climbing؟ إن أنا بوصل لأقصى حاجة أو أوصل لأقصى عمق وأحسن نتيجة.

Algorithm MemeticAlgorithmForHashi:
    Input: Hashi Puzzle Grid
    Output: Best Solution (Bridge Configuration)

    // 1. Initial Population Generation (GA Phase)
    Population = GenerateInitialPopulationRandomly()
    EvaluateFitness(Population) // Calculate Penalty for each chromosome

    // 2. Evolutionary Loop
    While TerminationConditionNotMet (Generation < MaxGenerations AND BestPenalty > 0):

        // Selection, Crossover, and Mutation (GA Core)
        Parents = Selection(Population)
        Offspring = Crossover(Parents)
        Offspring = Mutation(Offspring)

        // 3. Local Search Phase (MA Upgrade)
        For Each Solution in Offspring:
            LocalSteps = 0
            
            // Hill Climbing Search loop with limit
            While (LocalSteps < MaxLocalIterations AND Solution.Penalty > 0):
                
                // Generate neighbors using the 4 Operators:
                // (Degree Repair, Crossing Repair, Connectivity Repair, Bridge Reallocation)
                Neighbors = GenerateNeighborsUsingOperators(Solution)
                BestNeighbor = FindSolutionWithLowestPenalty(Neighbors)

                // Hill Climbing Condition: Accept only if strictly improved
                If BestNeighbor.Penalty < Solution.Penalty:
                    Solution = BestNeighbor // Step to the better neighbor
                    LocalSteps = LocalSteps + 1
                Else:
                    Break // Reached Local Optimum (No better neighbors)
                EndIf
            EndWhile
        EndFor

        // Update Population with improved offspring
        Population = SelectNewGeneration(Population, Offspring)

    EndWhile

    Return Best Solution in Population

### 8. مثال يدوي على P1: [1,0,1,1] → [1,1,1,1]
 أول حاجة عندنا الـ $V_1$ (اللي هو [1, 0, 1, 1]) والـ $V_2$ (اللي هو [1, 1, 1, 1]):
 دلوقتي بنشوف الأخطاء، فإحنا بنفترض إن الـ 
V 
1
​
 
 الـ Penalty بتاعتها 3، والـ 
V 
2
​
 
 الـ Penalty بتاعتها 2. وطبعاً بنحسب الـ Penalty دي بناءً على إيه؟ بنشوف مثلاً الأربع حاجات اللي قولنا عليهم فوق اللي هما بتوع الـ Repair: هل عددها مظبوط ولا لا؟ لو فيه اتنين قاطعين على بعض ولا لا؟ متصلة ولا مش متصلة؟ وبشوف كل حاجة. تمام؟ وبعد كده بختار الحل الأحسن. إزاي الحل الأحسن؟ إن الـ Penalty بتاعتها أقل.

تاني حاجة، الخطوة التانية اللي هي الـ Crossover:
الـ Crossover إن أنا بجوزهم لبعض وببدل أجزاء، يعني باخد رقمين من الجزء الأول مع رقمين من الجزء التاني. وببقى حريصة على إن أنا أطلع Generation مختلف عن اللي عندي من الاتنين.

تالت حاجة، الـ Mutation:
إن أنا بغير في الموجود عندي ما بين رقمين بحيث إن أنا أعمل طفرة، ودي بتطلع طبعاً Generation أحسن.

رابع حاجة، إني بعمل إيه؟ بدخلها على الـ Local Search:
الـ Local Search مش هنسى وأنا بدخلها عليه إن أنا أول حاجة أحط الـ Max Local Iterations عشان الجهاز ما يفضلش يلف في الـ Infinite Loops. بعد كده بنعتمد الألجوريزم بتاع الـ Local Search إن أنا في النقطة اللي أنا واقفة فيها دلوقتي ببص إيه الجيران القريبة مني باستخدام الـ 4 Operators. ببتدي بقى نصلح ونختار أحسن واحد بناءً على الجيران اللي عندي، ليه؟ عشان أنا بستخدم هنا في الـ Local Search مبدأ الـ Hill Climbing.



A(0, 0) = 2
B(0, 2) = 2
C(2, 0) = 2
D(2, 2) = 2
E 
1
​
 
: الجسر الأفقي المتصل ما بين 
A
 و 
B
.

E 
2
​
 
: الجسر الرأسي الشمال المتصل ما بين 
A
 و 
C
.

E 
3
​
 
: الجسر الرأسي اليمين المتصل ما بين 
B
 و 
D
.

E 
4
​
 
: الجسر الأفقي المتصل ما بين 
C
 و 
D
.
لِ نحسب بقى كل جزيرة طالع منها كام جسر في الحل ده ([1, 0, 1, 1]):جزيرة $A$ (مطلوب منها 2): متوصلة بـ $E_1$ و $E_2$.طالع منها $E_1(1) + E_2(0) = 1$ جسر بس $\leftarrow$ عندها عجز (ناقصة 1).جزيرة $C$ (مطلوب منها 2): متوصلة بـ $E_2$ و $E_4$.طالع منها $E_2(0) + E_4(1) = 1$ جسر بس $\leftarrow$ عندها عجز (ناقصة 1).جزيرة $B$ (مطلوب منها 2): متوصلة بـ $E_1$ و $E_3$.طالع منها $E_1(1) + E_3(1) = 2$ جسر $\leftarrow$ مظبوطة تماماً (2/2).جزيرة $D$ (مطلوب منها 2): متوصلة بـ $E_3$ و $E_4$.طالع منها $E_3(1) + E_4(1) = 2$ جسر $\leftarrow$ مظبوطة تماماً (2/2).
الـ Local Search بييجي يفحص الشبكة، يلقى إن الجزيرة $A$ والجزيرة $C$ عندهم عجز (كل واحدة واصلها 1 بدل 2).
يقوم يبص على الجسر المشترك اللي بينهم اللي هو $E_2$، يلقى قيمته حالياً 0.تقوم الـ Local Search مجربة تعديل الـ $E_2$ من 0 إلى 1. 
وجينا هنا لجأنا للـ Local Search عشان يحل المشكلة دي، وصلحها لنا باستخدام الـ Degree Repair Operator


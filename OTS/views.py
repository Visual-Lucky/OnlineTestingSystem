import json
import random

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.models import User, Permission

from OTS.models import Candidate, Question, Result, Subject, Test

MIN_QUESTIONS_PER_TEST = 10
MAX_QUESTIONS_PER_TEST = 50
PRACTICE_QUESTIONS_PER_SUBJECT = 25
PRACTICE_SESSION_QUESTION_COUNT = 10
PRACTICE_SUBJECTS = [
    "DSA",
    "Operating System",
    "DBMS",
    "OOPs",
    "Digital Logic",
    "Aptitude",
    "Logical Reasoning",
]
PRACTICE_TEST_PREFIX = "Practice Test - "


def _build_practice_question_bank(subject_name):
    """Build question bank using predefined subject data."""
    practice_data = {
        "Operating System": [
            {"question":"Which condition is not required for deadlock?","options":["Mutual Exclusion","Hold and Wait","No Preemption","Circular Wait"],"answer":"No Preemption"},
            {"question":"Which scheduling avoids starvation?","options":["FCFS","SJF","Priority","Round Robin"],"answer":"Round Robin"},
            {"question":"Paging eliminates?","options":["External fragmentation","Internal fragmentation","Deadlock","Thrashing"],"answer":"External fragmentation"},
            {"question":"Thrashing occurs when?","options":["High CPU","Low paging","Excessive paging","Low memory"],"answer":"Excessive paging"},
            {"question":"Context switching means?","options":["Process change","Memory change","Disk swap","Thread kill"],"answer":"Process change"},
            {"question":"Semaphore is used for?","options":["Memory","Synchronization","Scheduling","File"],"answer":"Synchronization"},
            {"question":"Banker’s algorithm is for?","options":["Deadlock prevention","Deadlock avoidance","Detection","Recovery"],"answer":"Deadlock avoidance"},
            {"question":"Which is preemptive?","options":["FCFS","SJF","Round Robin","FIFO"],"answer":"Round Robin"},
            {"question":"Virtual memory uses?","options":["RAM","Disk","Cache","Register"],"answer":"Disk"},
            {"question":"Process is?","options":["Program in execution","File","Memory","Thread"],"answer":"Program in execution"},
            {"question":"PCB stores?","options":["Process info","File data","Memory data","None"],"answer":"Process info"},
            {"question":"Page fault occurs when?","options":["Page in memory","Page missing","Disk error","CPU error"],"answer":"Page missing"},
            {"question":"LRU is?","options":["Scheduling","Page replacement","Memory alloc","Disk"],"answer":"Page replacement"},
            {"question":"Which causes internal fragmentation?","options":["Paging","Segmentation","Both","None"],"answer":"Paging"},
            {"question":"Thread is?","options":["Lightweight process","Heavy process","File","Program"],"answer":"Lightweight process"},
            {"question":"Critical section problem is?","options":["Synchronization","Memory","Disk","CPU"],"answer":"Synchronization"},
            {"question":"Which is not scheduling?","options":["FCFS","RR","Paging","Priority"],"answer":"Paging"},
            {"question":"Fork() creates?","options":["Thread","Process","File","Memory"],"answer":"Process"},
            {"question":"Zombie process is?","options":["Running","Terminated but not removed","Waiting","Blocked"],"answer":"Terminated but not removed"},
            {"question":"Deadlock detection uses?","options":["Graph","Stack","Queue","Tree"],"answer":"Graph"},
            {"question":"Time sharing system?","options":["Interactive","Batch","Real-time","None"],"answer":"Interactive"},
            {"question":"Kernel mode means?","options":["Privileged","User","Idle","Sleep"],"answer":"Privileged"},
            {"question":"System call used for I/O?","options":["Read","Exec","Fork","Wait"],"answer":"Read"},
            {"question":"Multiprogramming improves?","options":["CPU utilization","Memory","Disk","None"],"answer":"CPU utilization"},
            {"question":"Swap memory means?","options":["Disk memory","RAM","Cache","Register"],"answer":"Disk memory"},
        ],
        "DBMS": [
            {"question":"Which NF removes transitive dependency?","options":["1NF","2NF","3NF","BCNF"],"answer":"3NF"},
            {"question":"Primary key is?","options":["Unique","Duplicate","Null","Optional"],"answer":"Unique"},
            {"question":"ACID 'A' stands for?","options":["Atomicity","Accuracy","Access","Action"],"answer":"Atomicity"},
            {"question":"Which join shows matching rows?","options":["Inner","Left","Right","Outer"],"answer":"Inner"},
            {"question":"Foreign key ensures?","options":["Integrity","Speed","Security","None"],"answer":"Integrity"},
            {"question":"Index improves?","options":["Search","Insert","Delete","None"],"answer":"Search"},
            {"question":"Which SQL removes table?","options":["DELETE","DROP","TRUNCATE","REMOVE"],"answer":"DROP"},
            {"question":"Transaction means?","options":["Single unit","Multiple","None","Process"],"answer":"Single unit"},
            {"question":"Deadlock in DBMS?","options":["Lock wait","CPU","Disk","None"],"answer":"Lock wait"},
            {"question":"Which is DML?","options":["SELECT","CREATE","ALTER","DROP"],"answer":"SELECT"},
            {"question":"Which is DDL?","options":["INSERT","UPDATE","CREATE","DELETE"],"answer":"CREATE"},
            {"question":"BCNF handles?","options":["Functional dep","Multivalued","Join","None"],"answer":"Functional dep"},
            {"question":"Which avoids redundancy?","options":["Normalization","Indexing","Join","View"],"answer":"Normalization"},
            {"question":"View is?","options":["Virtual table","Real table","Index","Key"],"answer":"Virtual table"},
            {"question":"Which ensures durability?","options":["Log","Cache","Index","None"],"answer":"Log"},
            {"question":"Which command updates data?","options":["UPDATE","SELECT","DROP","CREATE"],"answer":"UPDATE"},
            {"question":"Which key is composite?","options":["Multiple attrs","Single","None","Null"],"answer":"Multiple attrs"},
            {"question":"Which avoids phantom reads?","options":["Serializable","Read committed","Read uncommitted","None"],"answer":"Serializable"},
            {"question":"ER diagram shows?","options":["Entities","Code","Memory","Disk"],"answer":"Entities"},
            {"question":"Which is not constraint?","options":["Primary","Foreign","Unique","Select"],"answer":"Select"},
            {"question":"Which join shows all rows?","options":["Full","Inner","Cross","None"],"answer":"Full"},
            {"question":"Which is TCL?","options":["COMMIT","SELECT","CREATE","DROP"],"answer":"COMMIT"},
            {"question":"Which uses hashing?","options":["Hash index","Tree","List","Stack"],"answer":"Hash index"},
            {"question":"Which is not anomaly?","options":["Insert","Delete","Update","Select"],"answer":"Select"},
            {"question":"Tuple means?","options":["Row","Column","Table","Index"],"answer":"Row"},
        ],
        "DSA": [
            {"question":"Binary search complexity?","options":["O(n)","O(log n)","O(n log n)","O(1)"],"answer":"O(log n)"},
            {"question":"Stack follows?","options":["FIFO","LIFO","Both","None"],"answer":"LIFO"},
            {"question":"Queue follows?","options":["FIFO","LIFO","Both","None"],"answer":"FIFO"},
            {"question":"Worst quicksort?","options":["O(n^2)","O(n)","O(log n)","O(n log n)"],"answer":"O(n^2)"},
            {"question":"Merge sort complexity?","options":["O(n log n)","O(n)","O(n^2)","O(log n)"],"answer":"O(n log n)"},
            {"question":"Heap used in?","options":["Priority queue","Stack","Graph","Tree"],"answer":"Priority queue"},
            {"question":"BST inorder gives?","options":["Sorted","Reverse","Random","None"],"answer":"Sorted"},
            {"question":"Graph BFS uses?","options":["Queue","Stack","Tree","Array"],"answer":"Queue"},
            {"question":"DFS uses?","options":["Stack","Queue","Heap","None"],"answer":"Stack"},
            {"question":"Hashing gives?","options":["O(1)","O(n)","O(log n)","O(n^2)"],"answer":"O(1)"},
            {"question":"Linked list access?","options":["O(n)","O(1)","O(log n)","O(n log n)"],"answer":"O(n)"},
            {"question":"Which is linear DS?","options":["Array","Tree","Graph","Heap"],"answer":"Array"},
            {"question":"AVL tree is?","options":["Balanced BST","Heap","Graph","Queue"],"answer":"Balanced BST"},
            {"question":"Collision occurs in?","options":["Hashing","Sorting","Searching","Traversal"],"answer":"Hashing"},
            {"question":"Which is non-linear?","options":["Tree","Array","Stack","Queue"],"answer":"Tree"},
            {"question":"Recursion uses?","options":["Stack","Queue","Heap","Array"],"answer":"Stack"},
            {"question":"Topological sort is for?","options":["DAG","Tree","List","Stack"],"answer":"DAG"},
            {"question":"Min heap root?","options":["Smallest","Largest","Random","None"],"answer":"Smallest"},
            {"question":"Cycle detection uses?","options":["DFS","BFS","Both","None"],"answer":"DFS"},
            {"question":"Which is greedy?","options":["Dijkstra","DFS","BFS","Binary search"],"answer":"Dijkstra"},
            {"question":"Dynamic programming avoids?","options":["Recalculation","Sorting","Searching","None"],"answer":"Recalculation"},
            {"question":"Trie is used for?","options":["Strings","Numbers","Graph","Heap"],"answer":"Strings"},
            {"question":"Graph edges stored in?","options":["Adj list","Stack","Queue","Heap"],"answer":"Adj list"},
            {"question":"Which is divide & conquer?","options":["Merge sort","DFS","BFS","Heap"],"answer":"Merge sort"},
            {"question":"Which is stable sort?","options":["Merge sort","Quick sort","Heap sort","Selection"],"answer":"Merge sort"},
        ],
        "Aptitude": [
            {"question":"A can do work in 12 days, B in 18 days. Together?","options":["7.2","8","6","9"],"answer":"7.2"},
            {"question":"SI on 2000 at 5% for 3 years?","options":["300","200","400","250"],"answer":"300"},
            {"question":"Speed 60 km/h = m/s?","options":["16.67","20","15","10"],"answer":"16.67"},
            {"question":"Ratio 3:4 becomes 6:8, change?","options":["0%","50%","100%","25%"],"answer":"0%"},
            {"question":"Average of 5 numbers is 20, sum?","options":["100","80","90","120"],"answer":"100"},
            {"question":"Profit 20% on cost 100?","options":["120","110","130","140"],"answer":"120"},
            {"question":"Time = Distance/Speed, D=100, S=50?","options":["2","1","3","4"],"answer":"2"},
            {"question":"LCM of 12 and 18?","options":["36","24","48","12"],"answer":"36"},
            {"question":"HCF of 24 and 36?","options":["12","6","18","24"],"answer":"12"},
            {"question":"Train 100m at 50 m/s time?","options":["2s","3s","4s","5s"],"answer":"2s"},
            {"question":"Discount 10% on 1000?","options":["900","950","800","850"],"answer":"900"},
            {"question":"Compound interest formula uses?","options":["Power","Log","Sum","Diff"],"answer":"Power"},
            {"question":"If x=2, 2x+3?","options":["7","5","6","4"],"answer":"7"},
            {"question":"Boat speed 10, stream 2, downstream?","options":["12","8","10","14"],"answer":"12"},
            {"question":"Upstream speed?","options":["8","12","10","6"],"answer":"8"},
            {"question":"Probability max value?","options":["1","0","2","10"],"answer":"1"},
            {"question":"Permutation formula?","options":["nPr","nCr","n^2","n!"],"answer":"nPr"},
            {"question":"Combination formula?","options":["nCr","nPr","n^2","n!"],"answer":"nCr"},
            {"question":"Simple interest depends on?","options":["Time","Speed","Distance","None"],"answer":"Time"},
            {"question":"Area of square side 4?","options":["16","8","12","20"],"answer":"16"},
            {"question":"Volume of cube side 2?","options":["8","4","6","10"],"answer":"8"},
            {"question":"Odd number?","options":["3","4","6","8"],"answer":"3"},
            {"question":"Even number?","options":["2","3","5","7"],"answer":"2"},
            {"question":"Prime number?","options":["7","8","9","10"],"answer":"7"},
            {"question":"Square root of 49?","options":["7","6","8","9"],"answer":"7"},
        ],
        "Digital Logic": [
            {"question":"Universal gate?","options":["NAND","AND","OR","XOR"],"answer":"NAND"},
            {"question":"NOR is also?","options":["Universal","Basic","Complex","None"],"answer":"Universal"},
            {"question":"Flip flop stores?","options":["1 bit","2 bit","4 bit","8 bit"],"answer":"1 bit"},
            {"question":"Binary of 15?","options":["1111","1010","1100","1001"],"answer":"1111"},
            {"question":"Decimal 10 binary?","options":["1010","1111","1001","1100"],"answer":"1010"},
            {"question":"Full adder inputs?","options":["3","2","4","1"],"answer":"3"},
            {"question":"Half adder inputs?","options":["2","3","4","1"],"answer":"2"},
            {"question":"K-map used for?","options":["Minimization","Storage","Count","Add"],"answer":"Minimization"},
            {"question":"AND gate output 1 when?","options":["All 1","Any 1","None","Mixed"],"answer":"All 1"},
            {"question":"OR gate output 1 when?","options":["Any 1","All 1","None","Mixed"],"answer":"Any 1"},
            {"question":"NOT gate output?","options":["Complement","Same","Random","None"],"answer":"Complement"},
            {"question":"XOR output 1 when?","options":["Different","Same","All 1","None"],"answer":"Different"},
            {"question":"XNOR output 1 when?","options":["Same","Different","All 1","None"],"answer":"Same"},
            {"question":"SR flip flop invalid?","options":["S=1,R=1","S=0,R=0","S=1,R=0","S=0,R=1"],"answer":"S=1,R=1"},
            {"question":"Clock used in?","options":["Sequential","Combinational","Both","None"],"answer":"Sequential"},
            {"question":"Register stores?","options":["Data","Code","Memory","None"],"answer":"Data"},
            {"question":"Counter counts?","options":["Pulses","Memory","Code","None"],"answer":"Pulses"},
            {"question":"Multiplexer selects?","options":["One input","All","None","Two"],"answer":"One input"},
            {"question":"Demultiplexer does?","options":["One to many","Many to one","None","Both"],"answer":"One to many"},
            {"question":"Encoder converts?","options":["2^n to n","n to 2^n","Binary","Decimal"],"answer":"2^n to n"},
            {"question":"Decoder converts?","options":["n to 2^n","2^n to n","Binary","Decimal"],"answer":"n to 2^n"},
            {"question":"RAM is?","options":["Volatile","Non-volatile","Both","None"],"answer":"Volatile"},
            {"question":"ROM is?","options":["Non-volatile","Volatile","Both","None"],"answer":"Non-volatile"},
            {"question":"Boolean algebra uses?","options":["Binary","Decimal","Hex","Octal"],"answer":"Binary"},
            {"question":"Logic gate output is?","options":["Binary","Decimal","Hex","None"],"answer":"Binary"},
        ],
        "Logical Reasoning": [
            {"question":"Series: 2,6,12,20,?","options":["30","28","26","24"],"answer":"30"},
            {"question":"Odd one: 3,5,7,9","options":["9","7","5","3"],"answer":"9"},
            {"question":"A:B=1:2, B:C=2:3, A:C?","options":["1:3","2:3","3:4","1:2"],"answer":"1:3"},
            {"question":"Mirror of 3?","options":["Ɛ","3","E","M"],"answer":"Ɛ"},
            {"question":"Next: A,C,F,J,?","options":["O","N","P","M"],"answer":"O"},
            {"question":"Coding: CAT=24, DOG?","options":["26","24","30","20"],"answer":"26"},
            {"question":"Direction: N→E→S, final?","options":["South","North","East","West"],"answer":"South"},
            {"question":"Clock 3:00 angle?","options":["90","180","45","0"],"answer":"90"},
            {"question":"Blood: Father’s brother?","options":["Uncle","Grandfather","Cousin","None"],"answer":"Uncle"},
            {"question":"Alphabet position of Z?","options":["26","25","24","23"],"answer":"26"},
            {"question":"Series: 1,4,9,16,?","options":["25","20","18","30"],"answer":"25"},
            {"question":"Odd: Apple,Banana,Carrot,Mango","options":["Carrot","Apple","Banana","Mango"],"answer":"Carrot"},
            {"question":"Water:Drink :: Food:?","options":["Eat","Cook","Buy","Make"],"answer":"Eat"},
            {"question":"If 5x=20,x=?","options":["4","5","3","2"],"answer":"4"},
            {"question":"Series: 5,10,20,40,?","options":["80","60","50","90"],"answer":"80"},
            {"question":"Cube faces?","options":["6","8","4","12"],"answer":"6"},
            {"question":"Triangle angles sum?","options":["180","90","360","270"],"answer":"180"},
            {"question":"Odd: Pen,Pencil,Ink,Book","options":["Ink","Pen","Book","Pencil"],"answer":"Ink"},
            {"question":"Day after Monday?","options":["Tuesday","Sunday","Wednesday","Friday"],"answer":"Tuesday"},
            {"question":"Opposite of North?","options":["South","East","West","Up"],"answer":"South"},
            {"question":"Series: 2,3,5,8,?","options":["13","12","11","10"],"answer":"13"},
            {"question":"Vowels count?","options":["5","4","6","3"],"answer":"5"},
            {"question":"Even numbers?","options":["2","3","5","7"],"answer":"2"},
            {"question":"Prime number?","options":["11","12","15","18"],"answer":"11"},
            {"question":"Square of 6?","options":["36","30","40","25"],"answer":"36"},
        ],
        "OOPs": [
            {"question":"Encapsulation means?","options":["Data hiding","Inheritance","Polymorphism","Abstraction"],"answer":"Data hiding"},
            {"question":"Inheritance allows?","options":["Reuse","Hide","Delete","None"],"answer":"Reuse"},
            {"question":"Polymorphism means?","options":["Many forms","One form","No form","None"],"answer":"Many forms"},
            {"question":"Abstraction hides?","options":["Details","Data","Code","None"],"answer":"Details"},
            {"question":"Class is?","options":["Blueprint","Object","Data","Function"],"answer":"Blueprint"},
            {"question":"Object is?","options":["Instance","Class","Function","None"],"answer":"Instance"},
            {"question":"Constructor is?","options":["Initialize object","Destroy","Delete","None"],"answer":"Initialize object"},
            {"question":"Destructor used for?","options":["Cleanup","Create","Run","None"],"answer":"Cleanup"},
            {"question":"Function overloading?","options":["Compile time","Runtime","Both","None"],"answer":"Compile time"},
            {"question":"Overriding occurs?","options":["Runtime","Compile","Both","None"],"answer":"Runtime"},
            {"question":"Access specifier?","options":["Public","Run","Exec","None"],"answer":"Public"},
            {"question":"Private means?","options":["Restricted","Open","Public","None"],"answer":"Restricted"},
            {"question":"Protected used in?","options":["Inheritance","Loop","Condition","None"],"answer":"Inheritance"},
            {"question":"Virtual function?","options":["Runtime binding","Compile","None","Both"],"answer":"Runtime binding"},
            {"question":"Static keyword?","options":["Shared","Private","Public","None"],"answer":"Shared"},
            {"question":"Friend function?","options":["Access private","No access","Public","None"],"answer":"Access private"},
            {"question":"This pointer refers?","options":["Current object","Parent","Child","None"],"answer":"Current object"},
            {"question":"Interface is?","options":["Abstract","Concrete","None","Both"],"answer":"Abstract"},
            {"question":"Multiple inheritance?","options":["Many parents","One parent","None","Both"],"answer":"Many parents"},
            {"question":"Exception handling?","options":["Error handling","Compile","Run","None"],"answer":"Error handling"},
            {"question":"Abstract class?","options":["Cannot instantiate","Can","None","Both"],"answer":"Cannot instantiate"},
            {"question":"Method is?","options":["Function in class","Variable","Object","None"],"answer":"Function in class"},
            {"question":"Data member?","options":["Variable","Function","Object","None"],"answer":"Variable"},
            {"question":"Operator overloading?","options":["Custom operator","Normal","None","Both"],"answer":"Custom operator"},
            {"question":"Binding means?","options":["Link method","Delete","Run","None"],"answer":"Link method"},
        ],
    }
    source = practice_data.get(subject_name, [])
    rows = []
    key_map = {0: "a", 1: "b", 2: "c", 3: "d"}
    for item in source[:PRACTICE_QUESTIONS_PER_SUBJECT]:
        options = item.get("options", [])
        answer_text = item.get("answer", "")
        answer_key = "a"
        for idx, opt in enumerate(options):
            if str(opt).strip().lower() == str(answer_text).strip().lower():
                answer_key = key_map[idx]
                break
        rows.append({
            "question": item.get("question", "").strip(),
            "options": [str(options[0]), str(options[1]), str(options[2]), str(options[3])],
            "answer": answer_key,
        })
    return rows


def ensure_practice_bank():
    """Ensure fixed subject-wise practice bank exists (25 questions each)."""
    for subject_name in PRACTICE_SUBJECTS:
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        test_name = f"{PRACTICE_TEST_PREFIX}{subject_name}"
        test, _ = Test.objects.get_or_create(subject=subject, name=test_name)
        if not test.is_active:
            test.is_active = True
            test.save(update_fields=["is_active"])
        desired = _build_practice_question_bank(subject_name)
        existing = list(
            Question.objects.filter(test=test).order_by("qid").values("que", "a", "b", "c", "d", "ans")
        )
        should_refresh = len(existing) != len(desired)
        if not should_refresh:
            for idx, row in enumerate(existing):
                exp = desired[idx]
                if (
                    row["que"] != exp["question"]
                    or row["a"] != exp["options"][0]
                    or row["b"] != exp["options"][1]
                    or row["c"] != exp["options"][2]
                    or row["d"] != exp["options"][3]
                    or row["ans"] != exp["answer"]
                ):
                    should_refresh = True
                    break
        if not should_refresh:
            continue
        Question.objects.filter(test=test).delete()
        for q in desired:
            opts = q["options"]
            Question.objects.create(
                test=test,
                que=q["question"],
                a=opts[0],
                b=opts[1],
                c=opts[2],
                d=opts[3],
                ans=q["answer"],
            )


# ── JSON APIs (bulk upload) ─────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def add_subject(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    name = (data.get("name") or "").strip()
    if not name:
        return JsonResponse({"error": "Field 'name' is required"}, status=400)
    subject = Subject.objects.create(name=name)
    return JsonResponse({"msg": "Subject added", "id": subject.id})


@csrf_exempt
@require_http_methods(["POST"])
def add_test(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    name = (data.get("name") or "").strip()
    subject_id = data.get("subject_id")
    if not name or subject_id is None:
        return JsonResponse({"error": "Fields 'name' and 'subject_id' are required"}, status=400)
    if not Subject.objects.filter(pk=subject_id).exists():
        return JsonResponse({"error": "Subject not found"}, status=404)
    duration_minutes = data.get("duration_minutes", 30)
    try:
        duration_minutes = int(duration_minutes)
    except (TypeError, ValueError):
        duration_minutes = 30
    teacher_id = request.session.get("_auth_user_id")
    test = Test.objects.create(subject_id=subject_id, name=name, duration_minutes=duration_minutes, teacher_id=teacher_id)
    return JsonResponse({"msg": "Test added", "id": test.id})


@csrf_exempt
@require_http_methods(["POST"])
def add_questions(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    test_id   = data.get("test_id")
    questions = data.get("questions")
    if test_id is None or not isinstance(questions, list):
        return JsonResponse({"error": "Fields 'test_id' and 'questions' (list) are required"}, status=400)
    if not Test.objects.filter(pk=test_id).exists():
        return JsonResponse({"error": "Test not found"}, status=404)
    test = Test.objects.get(pk=test_id)
    for q in questions:
        if not isinstance(q, dict):
            continue
        opts = q.get("options") or []
        if len(opts) < 4 or not q.get("question"):
            return JsonResponse({"error": "Each question needs text and 4 options"}, status=400)
        Question.objects.create(test=test, que=q["question"],
            a=opts[0], b=opts[1], c=opts[2], d=opts[3], ans=q.get("answer", ""))
    return JsonResponse({"msg": "Questions added successfully"})


@csrf_exempt
@require_http_methods(["POST"])
def full_upload(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    if not isinstance(payload, list):
        return JsonResponse({"error": "Body must be a JSON array"}, status=400)

    seen_keys = set()
    summary   = []

    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            return JsonResponse({"error": f"Item {idx} must be an object"}, status=400)
        subj_name = (item.get("subject") or "").strip()
        test_name = (item.get("test") or "").strip()
        questions = item.get("questions")
        if not subj_name or not test_name:
            return JsonResponse({"error": f"Item {idx}: 'subject' and 'test' are required"}, status=400)
        if not isinstance(questions, list):
            return JsonResponse({"error": f"Item {idx}: 'questions' must be a list"}, status=400)
        n = len(questions)
        if n < MIN_QUESTIONS_PER_TEST or n > MAX_QUESTIONS_PER_TEST:
            return JsonResponse(
                {"error": f"Item {idx} ('{test_name}'): need {MIN_QUESTIONS_PER_TEST}-{MAX_QUESTIONS_PER_TEST} questions, got {n}"},
                status=400,
            )
        dedupe = (subj_name.lower(), test_name.lower())
        if dedupe in seen_keys:
            return JsonResponse({"error": f"Duplicate pair: {subj_name} / {test_name}"}, status=400)
        seen_keys.add(dedupe)

        subject, _ = Subject.objects.get_or_create(name=subj_name)
        test, _    = Test.objects.get_or_create(subject=subject, name=test_name)
        
        teacher_id = request.session.get("_auth_user_id")
        if teacher_id and test.teacher_id != teacher_id:
            test.teacher_id = teacher_id
            test.save(update_fields=["teacher"])
            
        Question.objects.filter(test=test).delete()

        for q_idx, q in enumerate(questions):
            if not isinstance(q, dict):
                return JsonResponse({"error": f"Item {idx}, Q{q_idx}: invalid object"}, status=400)
            opts = q.get("options") or []
            text = (q.get("question") or "").strip()
            if len(opts) != 4 or not text:
                return JsonResponse({"error": f"Item {idx}, Q{q_idx}: need 'question' and 4 options"}, status=400)
            ans = (q.get("answer") or "").strip().lower()
            if ans not in ("a", "b", "c", "d"):
                return JsonResponse({"error": f"Item {idx}, Q{q_idx}: 'answer' must be a/b/c/d"}, status=400)
            Question.objects.create(test=test, que=text,
                a=str(opts[0]), b=str(opts[1]), c=str(opts[2]), d=str(opts[3]), ans=ans)

        summary.append({"subject": subj_name, "test": test_name, "question_count": n, "test_id": test.id})

    return JsonResponse({"msg": "Upload complete", "items": summary})


# ── Toggle test active/inactive ─────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def update_duration(request, test_id):
    if not request.session.get("_auth_user_id"):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    try:
        data = json.loads(request.body)
        duration = int(data.get("duration_minutes", 30))
        if duration < 5 or duration > 180:
            return JsonResponse({"error": "Invalid duration (must be 5-180)"}, status=400)
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid data"}, status=400)

    test = get_object_or_404(Test, pk=test_id)
    teacher_id = request.session.get("_auth_user_id")
    if test.teacher_id and str(test.teacher_id) != str(teacher_id):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    test.duration_minutes = duration
    test.save(update_fields=["duration_minutes"])
    return JsonResponse({"msg": "success", "duration_minutes": duration})

@csrf_exempt
@require_http_methods(["POST"])
def toggle_test(request, test_id):
    if not request.session.get("_auth_user_id"):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    try:
        test = Test.objects.get(pk=test_id, teacher=teacher)
    except Test.DoesNotExist:
        return JsonResponse({"error": "Test not found or not owned by teacher"}, status=404)
    test.is_active = not test.is_active
    test.save()
    return JsonResponse({"is_active": test.is_active, "test_id": test.id})


# ── Student pages ───────────────────────────────────────────

def welcome(request):
    return render(request, "welcome.html")


def studentPortal(request):
    return render(request, "student_portal.html")


def teacherPortal(request):
    return render(request, "teacher_portal.html")


def teacherLoginView(request):
    if request.session.get("_auth_user_id"):
        return redirect("/teacher/")
    if request.method == "POST":
        from django.contrib.auth import authenticate, login
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            # Backfill OTS permissions for existing staff users created before this fix.
            if user.is_staff and not user.is_superuser:
                permissions = Permission.objects.filter(content_type__app_label="OTS")
                user.user_permissions.add(*permissions)
            login(request, user)
            return redirect("/teacher/")
        return render(request, "teacher_login.html", {"loginError": "Invalid credentials or not a staff account."})
    return render(request, "teacher_login.html")


def teacherRegistrationForm(request):
    if request.session.get("_auth_user_id"):
        return redirect("/teacher/")
    return render(request, "teacher_registration.html")


def teacherRegistration(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        name = (request.POST.get("name") or "").strip()

        if not username or not password or not name:
            return render(request, "teacher_registration.html", {
                "teacherStatus": "invalid",
                "message": "All fields are required.",
            })

        if User.objects.filter(username=username).exists():
            return render(request, "teacher_registration.html", {
                "teacherStatus": "exists",
                "message": "Username already exists. Please choose another username.",
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name,
            is_staff=True,
        )
        # Give teacher access to admin pages used by dashboard quick links.
        permissions = Permission.objects.filter(content_type__app_label="OTS")
        user.user_permissions.set(permissions)
        user.save()
        return render(request, "teacher_registration.html", {
            "teacherStatus": "success",
            "message": "Teacher account created successfully. Please login.",
        })

    return render(request, "teacher_registration.html", {
        "teacherStatus": "invalid",
        "message": "Improper request.",
    })


def candidateRegistrationform(request):
    return render(request, "registrationform.html")


def candidateRegistration(request):
    if request.method == "POST":
        username = request.POST["username"]
        if Candidate.objects.filter(username=username).exists():
            user_status = 1
        else:
            Candidate.objects.create(
                username=username,
                password=request.POST["password"],
                name=request.POST["name"],
            )
            user_status = 2
    else:
        user_status = 3
    return render(request, "registration.html", {"userStatus": user_status})


def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        candidate = Candidate.objects.filter(username=username, password=password)
        if not candidate.exists():
            return render(request, "login.html", {"loginError": "Invalid username or password"})
        request.session["username"] = candidate[0].username
        request.session["name"]     = candidate[0].name
        pending = request.session.pop("pending_token", None)
        if pending:
            return redirect("OTS:test_by_token", token=pending)
        return HttpResponseRedirect(reverse("OTS:home"))
    return render(request, "login.html")


def candidateHome(request):
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    ensure_practice_bank()
    tests_api_template = reverse("OTS:api_tests", kwargs={"subject_id": 0}).replace("/0/", "/__SID__/")
    practice_url_template = reverse("OTS:practice") + "?test_id=__TID__"
    return render(request, "home.html", {
        "subjects_api_url":   reverse("OTS:api_subjects"),
        "tests_api_template": tests_api_template,
        "practice_url_template": practice_url_template,
    })


def testByToken(request, token):
    test = get_object_or_404(Test, token=token, is_active=True)
    if "name" not in request.session:
        request.session["pending_token"] = str(token)
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    questions_api_url = reverse("OTS:api_questions", kwargs={"test_id": test.id})
    return render(request, "Test_paper.html", {
        "test_id":           test.id,
        "test_name":         test.name,
        "questions_api_url": questions_api_url,
        "duration_minutes":  test.duration_minutes,
    })


def testPaper(request):
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    raw = request.GET.get("test_id")
    try:
        test_id = int(raw)
    except (TypeError, ValueError):
        return HttpResponseRedirect(reverse("OTS:home"))
    test = get_object_or_404(Test, pk=test_id)
    questions_api_url = reverse("OTS:api_questions", kwargs={"test_id": test_id})
    return render(request, "Test_paper.html", {
        "test_id":           test_id,
        "test_name":         test.name,
        "questions_api_url": questions_api_url,
        "duration_minutes":  test.duration_minutes,
    })


def calculateTestResult(request):
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    if request.method != "POST":
        return HttpResponseRedirect(reverse("OTS:home"))

    qid_list = []
    for key in request.POST:
        if key.startswith("qno"):
            try:
                qid_list.append(int(request.POST[key]))
            except (TypeError, ValueError):
                pass

    # FIX: Prevent ZeroDivisionError when no questions found in POST data
    if not qid_list:
        return HttpResponseRedirect(reverse("OTS:home"))

    test_id  = request.POST.get("test_id")
    test_obj = None
    if test_id:
        try:
            test_obj = Test.objects.get(pk=int(test_id))
        except (Test.DoesNotExist, ValueError):
            pass

    total_right   = 0
    total_wrong   = 0
    total_attempt = 0

    for qid in qid_list:
        try:
            question = Question.objects.get(qid=qid)
        except Question.DoesNotExist:
            continue
        chosen = request.POST.get("q" + str(qid))
        if chosen is None:
            continue
        total_attempt += 1
        if question.ans == chosen:
            total_right += 1
        else:
            total_wrong += 1

    # FIX: Safe division — total_questions guaranteed > 0 here, but guard anyway
    total_questions = len(qid_list)
    points = ((total_right - total_wrong) / total_questions * 10) if total_questions > 0 else 0.0

    result = Result(
        username = Candidate.objects.get(username=request.session["username"]),
        test     = test_obj,
        teacher  = test_obj.teacher if test_obj else None,
        attempt  = total_attempt,
        right    = total_right,
        wrong    = total_wrong,
        points   = points,
    )
    try:
        result.tab_switches     = int(request.POST.get("tab_switches", 0))
        result.copy_attempts    = int(request.POST.get("copy_attempts", 0))
        result.fullscreen_exits = int(request.POST.get("fullscreen_exits", 0))
    except (ValueError, TypeError):
        pass
    result.save()

    candidate = Candidate.objects.get(username=request.session["username"])
    candidate.testattemped += 1
    n = candidate.testattemped
    candidate.points = (candidate.points * (n - 1) + points) / n
    candidate.save()

    return HttpResponseRedirect(reverse("OTS:result"))


def testResultHistory(request):
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    candidate = Candidate.objects.get(username=request.session["username"])
    result    = Result.objects.filter(username=candidate).order_by("-date", "-time")
    return render(request, "candidate_history.html", {"candidate": candidate, "result": result})


def showTestResult(request):
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    try:
        latest = Result.objects.filter(username_id=request.session["username"]).latest("resultid")
        result = [latest]
    except Result.DoesNotExist:
        result = []
    return render(request, "show_result.html", {"result": result})


def logOutView(request):
    request.session.flush()
    return HttpResponseRedirect("/")


# ── Read APIs ───────────────────────────────────────────────

@require_GET
def api_subjects(request):
    rows = list(
        Subject.objects.filter(name__in=PRACTICE_SUBJECTS)
        .order_by("name")
        .values("id", "name")
    )
    return JsonResponse(rows, safe=False)


@require_GET
def api_tests(request, subject_id):
    if not Subject.objects.filter(pk=subject_id).exists():
        return JsonResponse({"error": "Subject not found"}, status=404)
    rows = list(
        Test.objects.filter(
            subject_id=subject_id,
            is_active=True,
            name__startswith=PRACTICE_TEST_PREFIX,
        )
        .order_by("name").values("id", "name", "subject_id", "token", "duration_minutes")
    )
    for r in rows:
        r["token"] = str(r["token"])
    return JsonResponse(rows, safe=False)


@require_GET
def api_questions(request, test_id):
    if not Test.objects.filter(pk=test_id).exists():
        return JsonResponse({"error": "Test not found"}, status=404)
    qs    = Question.objects.filter(test_id=test_id).order_by("qid")
    count = qs.count()
    if count < MIN_QUESTIONS_PER_TEST:
        return JsonResponse(
            {"error": f"This test must have at least {MIN_QUESTIONS_PER_TEST} questions.", "question_count": count},
            status=400,
        )
    rows = list(qs.values("qid", "que", "a", "b", "c", "d"))
    return JsonResponse(rows, safe=False)


@require_GET
def api_leaderboard(request, test_id):
    results = (
        Result.objects.filter(test_id=test_id)
        .select_related("username")
        .order_by("-points", "date")
    )
    data = [
        {"rank": i + 1, "name": r.username.name, "score": round(r.points, 2),
         "correct": r.right, "attempted": r.attempt}
        for i, r in enumerate(results)
    ]
    return JsonResponse(data, safe=False)


@require_GET
def api_all_students(request):
    if not request.session.get("_auth_user_id"):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    students = list(
        Candidate.objects.filter(result__teacher=teacher).distinct().order_by("name")
        .values("username", "name", "testattemped", "points")
    )
    for s in students:
        s["points"] = round(s["points"], 2)
    return JsonResponse(students, safe=False)


@require_GET
def api_test_results(request, test_id):
    if not request.session.get("_auth_user_id"):
        return JsonResponse({"error": "Unauthorized"}, status=401)
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    try:
        test = Test.objects.get(pk=test_id, teacher=teacher)
    except Test.DoesNotExist:
        return JsonResponse({"error": "Test not found or not owned by teacher"}, status=404)
        
    results = (
        Result.objects.filter(test=test)
        .select_related("username")
        .order_by("-points", "date")
    )
    data = [
        {
            "rank":         i + 1,
            "name":         r.username.name,
            "username":     r.username.username,
            "score":        round(r.points, 2),
            "correct":      r.right,
            "wrong":        r.wrong,
            "attempted":    r.attempt,
            "tab_switches": r.tab_switches,
            "date":         str(r.date),
            "time":         str(r.time)[:5],
        }
        for i, r in enumerate(results)
    ]
    return JsonResponse(data, safe=False)


# ── Teacher Dashboard ────────────────────────────────────────

def teacher_dashboard(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")

    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))

    # FIX 1: Convert queryset to list FIRST so prefetch_related works properly
    # and we can safely use len() instead of .count() on prefetched relations
    tests_by_teacher = Test.objects.filter(teacher=teacher)
    subjects = list(Subject.objects.filter(test__in=tests_by_teacher).distinct().prefetch_related("test_set__question_set"))

    test_rows = []
    for subj in subjects:
        teacher_tests_in_subj = [t for t in subj.test_set.all() if t.teacher_id == teacher.id]
        for test in teacher_tests_in_subj:
            # FIX 2: Use len() on the prefetched relation cache — avoids extra DB query
            # Previously .count() was bypassing the prefetch cache entirely
            q_count      = len(test.question_set.all())
            result_count = Result.objects.filter(test=test).count()
            test_rows.append({
                "subject_name": subj.name,
                "test_name":    test.name,
                "test_id":      test.id,
                "token":        str(test.token),
                "q_count":      q_count,
                "result_count": result_count,
                "ready":        q_count >= MIN_QUESTIONS_PER_TEST,
                "need_more":    max(0, MIN_QUESTIONS_PER_TEST - q_count),
                "is_active":    test.is_active,
                "duration":     test.duration_minutes,
            })

    all_results = (
        Result.objects.filter(teacher=teacher).select_related("username", "test")
        .order_by("-date", "-time")[:200]
    )

    # FIX 3: subject_count from len(list) — no extra DB call, always accurate
    return render(request, "teacher_dashboard.html", {
        "subjects":        subjects,
        "subject_count":   len(subjects),
        "candidate_count": Candidate.objects.filter(result__teacher=teacher).distinct().count(),
        "results_count":   Result.objects.filter(teacher=teacher).count(),
        "test_rows":       test_rows,
        "all_results":     all_results,
    })


def teacher_add_subject(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    msg = None
    kind = "success"
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if not name:
            msg = "Subject name is required."
            kind = "danger"
        else:
            subject, created = Subject.objects.get_or_create(name=name)
            msg = "Subject added successfully." if created else "Subject already exists."
            kind = "success" if created else "warning"
    return render(request, "teacher_add_subject.html", {"message": msg, "kind": kind})


def teacher_add_test(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    msg = None
    kind = "success"
    subjects = Subject.objects.order_by("name")
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        subject_id = request.POST.get("subject_id")
        try:
            subject = Subject.objects.get(pk=int(subject_id))
        except (Subject.DoesNotExist, TypeError, ValueError):
            subject = None
        if not name or not subject:
            msg = "Please select a subject and enter test name."
            kind = "danger"
        else:
            duration = request.POST.get("duration")
            duration_val = 30
            if duration and duration.isdigit():
                duration_val = int(duration)
            
            teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
            test = Test.objects.create(subject=subject, name=name, teacher=teacher, duration_minutes=duration_val)
            msg = f"Test created: {test.name}"
            kind = "success"
    return render(request, "teacher_add_test.html", {"subjects": subjects, "message": msg, "kind": kind})


def teacher_add_question(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    msg = None
    kind = "success"
    tests = Test.objects.select_related("subject").order_by("subject__name", "name")
    if request.method == "POST":
        test_id = request.POST.get("test_id")
        que = (request.POST.get("que") or "").strip()
        a = (request.POST.get("a") or "").strip()
        b = (request.POST.get("b") or "").strip()
        c = (request.POST.get("c") or "").strip()
        d = (request.POST.get("d") or "").strip()
        ans = (request.POST.get("ans") or "").strip().lower()
        try:
            test = Test.objects.get(pk=int(test_id))
        except (Test.DoesNotExist, TypeError, ValueError):
            test = None
        if not test or not que or not a or not b or not c or not d or ans not in ("a", "b", "c", "d"):
            msg = "All fields are required and answer must be a/b/c/d."
            kind = "danger"
        else:
            Question.objects.create(test=test, que=que, a=a, b=b, c=c, d=d, ans=ans)
            msg = "Question added successfully."
            kind = "success"
    return render(request, "teacher_add_question.html", {"tests": tests, "message": msg, "kind": kind})


def teacher_students(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    students = Candidate.objects.filter(result__teacher=teacher).distinct().order_by("name")
    return render(request, "teacher_students.html", {"students": students})


def teacher_results(request):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    test_id = request.GET.get("test_id")
    tests = Test.objects.filter(teacher=teacher).select_related("subject").order_by("subject__name", "name")
    results = Result.objects.filter(teacher=teacher).select_related("username", "test").order_by("-date", "-time")[:200]
    selected_test = None
    if test_id:
        try:
            selected_test = Test.objects.get(pk=int(test_id), teacher=teacher)
            results = Result.objects.filter(test=selected_test).select_related("username", "test").order_by("-date", "-time")[:500]
        except (Test.DoesNotExist, TypeError, ValueError):
            selected_test = None
    return render(request, "teacher_results.html", {
        "tests": tests,
        "results": results,
        "selected_test": selected_test,
    })


@require_http_methods(["POST"])
def teacher_delete_test(request, test_id):
    if not request.session.get("_auth_user_id"):
        return redirect("/teacher/login/")
    teacher = User.objects.get(pk=request.session.get("_auth_user_id"))
    test = get_object_or_404(Test, pk=test_id, teacher=teacher)
    test.delete()
    return redirect("/teacher/")


# ── Practice Questions ───────────────────────────────────────

def practice_questions(request):
    """Practice mode: shows questions from a chosen test with instant answer feedback.
    No result is saved. Accessible to logged-in candidates only."""
    if "name" not in request.session:
        return HttpResponseRedirect(reverse("OTS:Loginform"))
    ensure_practice_bank()
    tests_api_template = reverse("OTS:api_tests", kwargs={"subject_id": 0}).replace(
        "/0/", "/__SID__/"
    )
    practice_questions_template = reverse("OTS:api_practice_questions", kwargs={"test_id": 0}).replace(
        "/0/", "/__TID__/"
    )
    initial_test_id = request.GET.get("test_id", "")
    return render(request, "practice_questions.html", {
        "subjects_api_url":   reverse("OTS:api_subjects"),
        "tests_api_template": tests_api_template,
        "practice_questions_template": practice_questions_template,
        "initial_test_id": initial_test_id,
    })


@require_GET
def api_practice_check(request):
    """Return the correct answer for a single question (practice mode only).
    Does NOT expose answers in bulk — only one at a time on demand."""
    raw = request.GET.get("qid")
    try:
        qid = int(raw)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid qid"}, status=400)
    try:
        q = Question.objects.get(qid=qid)
    except Question.DoesNotExist:
        return JsonResponse({"error": "Question not found"}, status=404)
    return JsonResponse({"answer": q.ans})


@require_GET
def api_practice_questions(request, test_id):
    """Return random 10 practice questions from a test."""
    if not Test.objects.filter(pk=test_id, is_active=True).exists():
        return JsonResponse({"error": "Test not found"}, status=404)
    qs = list(Question.objects.filter(test_id=test_id).values("qid", "que", "a", "b", "c", "d"))
    if len(qs) < PRACTICE_SESSION_QUESTION_COUNT:
        return JsonResponse(
            {"error": f"This practice set needs at least {PRACTICE_SESSION_QUESTION_COUNT} questions."},
            status=400,
        )
    random.shuffle(qs)
    return JsonResponse(qs[:PRACTICE_SESSION_QUESTION_COUNT], safe=False)


@require_GET
def api_subject_question_bank(request, subject_id):
    """Return full 25-question bank for one practice subject."""
    subject = Subject.objects.filter(pk=subject_id, name__in=PRACTICE_SUBJECTS).first()
    if not subject:
        return JsonResponse({"error": "Subject not found"}, status=404)
    test = Test.objects.filter(
        subject=subject,
        is_active=True,
        name__startswith=PRACTICE_TEST_PREFIX,
    ).first()
    if not test:
        return JsonResponse({"error": "Practice test not found for this subject"}, status=404)
    rows = list(Question.objects.filter(test=test).values("qid", "que", "a", "b", "c", "d"))
    return JsonResponse(rows, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def api_practice_submit(request):
    """Save practice session result for reports/history."""
    if "name" not in request.session:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    try:
        payload = json.loads(request.body or "{}")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    try:
        test_id = int(payload.get("test_id"))
        attempt = int(payload.get("attempt", 0))
        right = int(payload.get("right", 0))
        wrong = int(payload.get("wrong", 0))
        tab_switches = int(payload.get("tab_switches", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid fields"}, status=400)

    if attempt < 0 or right < 0 or wrong < 0 or right > attempt or wrong > attempt:
        return JsonResponse({"error": "Invalid score data"}, status=400)

    test = Test.objects.filter(pk=test_id, name__startswith=PRACTICE_TEST_PREFIX).first()
    if not test:
        return JsonResponse({"error": "Practice test not found"}, status=404)

    candidate = Candidate.objects.get(username=request.session["username"])
    points = ((right - wrong) / attempt * 10) if attempt > 0 else 0.0
    Result.objects.create(
        username=candidate,
        test=test,
        teacher=test.teacher if test else None,
        attempt=attempt,
        right=right,
        wrong=wrong,
        points=points,
        tab_switches=tab_switches,
        copy_attempts=0,
        fullscreen_exits=0,
    )
    # Keep candidate aggregate report counters in sync with practice submissions.
    candidate.testattemped += 1
    n = candidate.testattemped
    candidate.points = (candidate.points * (n - 1) + points) / n
    candidate.save(update_fields=["testattemped", "points"])
    return JsonResponse({"msg": "Practice result saved"})

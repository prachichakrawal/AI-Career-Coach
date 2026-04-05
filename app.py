from flask import Flask, render_template,request,redirect,session
import re #Regular epression( text search,match &modify)
import random
from PyPDF2 import PdfReader
import os
import difflib
import random
good_msgs = [
    "Excellent explanation!",
    "Well structured answer.",
    "Strong understanding of concept."
]

avg_msgs = [
    "Try adding more details.",
    "Concept is partially clear.",
    "Explain with example."
]

bad_msgs = [
    "Answer is too short.",
    "Concept unclear.",
    "Need better explanation."
]

def evaluate_answer_local(question, user_answer):
    if not user_answer or user_answer.strip() == "":
        return "Skipped "

    keywords = question.lower().split()
    match_count = 0

    for word in keywords:
        if word in user_answer.lower():
            match_count += 1

    length = len(user_answer.split())

    if match_count > 3 and length > 30:
        return "Good - " + random.choice(good_msgs)
    elif match_count > 1:
        return "Average - " + random.choice(avg_msgs)
    else:
        return "Poor - " + random.choice(bad_msgs)
app=Flask(__name__)
app.secret_key="prachi_secret"

@app.route("/")
def home():
     return render_template("index.html")
@app.route("/select")
def select():
    return render_template("select_subject.html", skills=skills_list)


@app.route("/start_test", methods=["POST", "GET"])
def start_test():
    selected_skill = request.form["skill"]

    # flatten all levels into one list
    all_questions = []
    for level in questions[selected_skill]:
        all_questions.extend(questions[selected_skill][level])

    random.shuffle(all_questions)

    session["skill"] = selected_skill
    session["questions"] = all_questions
    session["current"] = 0
    session["results"] = []

    return redirect("/question")

@app.route("/question", methods=["GET", "POST"])
def question():
    if "questions" not in session:
        return redirect("/")

    questions_list = session["questions"]
    current_index = session.get("current", 0)

    # ---------------- GET ----------------
    if request.method == "GET":
        if current_index >= len(questions_list):
            return redirect("/result")

        q = questions_list[current_index]
        return render_template("question.html", question=q, index=current_index+1)

    # ---------------- POST ----------------
    if request.method == "POST":
        user_answer = request.form.get("answer")
        skip = request.form.get("skip")
        final_submit = request.form.get("final_submit")

        if current_index < len(questions_list):
            q = questions_list[current_index]

            # FINAL SUBMIT LOGIC
            if final_submit == "yes":
                if not user_answer or user_answer.strip() == "":
                    evaluation = "No Answer "
                    user_answer = "No Answer"
                else:
                    evaluation = evaluate_answer_local(q, user_answer)

                session["results"].append({
                    "question": q,
                    "answer": user_answer,
                    "evaluation": evaluation
                })

                # remaining sab skipped
                for i in range(current_index + 1, len(questions_list)):
                    session["results"].append({
                        "question": questions_list[i],
                        "answer": "Skipped",
                        "evaluation": "Skipped"
                    })

                return redirect("/result")

            # NORMAL FLOW
            if skip == "yes":
                evaluation = "Skipped"
                user_answer = "Skipped"
            else:
                if not user_answer or user_answer.strip() == "":
                    evaluation = "No Answer "
                    user_answer = "No Answer"
                else:
                    evaluation = evaluate_answer_local(q, user_answer)

            session["results"].append({
                "question": q,
                "answer": user_answer,
                "evaluation": evaluation
            })

        session["current"] = current_index + 1

        if session["current"] >= len(questions_list):
            return redirect("/result")

        return redirect("/question")

@app.route("/result")
def final_result():
    if "results" not in session:
        return redirect("/")
    results = session.get("results", [])
    return render_template("result.html", results=results)


skills_list=[
    "python","java","SQL","javascript","html","css","react","dsa","flask","c","c++"]
questions={
    "python":{
        "beginner":[
"What is Python and what are its main features?",
"What are the different data types in Python?",
"What is the difference between a list and a tuple in Python?",
"What is a dictionary in Python?",
"What are mutable and immutable objects in Python?",
"What is a function in Python?",
"What is recursion in Python?",
"What is a lambda function?",
"What is the difference between append() and extend() in Python lists?",
"What is list comprehension in Python?",
"What is Object-Oriented Programming?",
"What is the difference between a class and an object?",
"What is inheritance in Python?",
"What is polymorphism in Python?",
"What is encapsulation?",
"What is exception handling in Python?",
"What is a try-except block?",
"What is the difference between shallow copy and deep copy?",
"What is an iterator and iterable in Python?",
"Write a Python program to check if a number is prime."
],
"intermediate":[
"What is a decorator in Python and why is it used?",
"What is a generator and how does it differ from a normal function?",
"What is the Global Interpreter Lock (GIL) in Python?",
"What is the difference between deep copy and shallow copy?",
"What is the difference between multithreading and multiprocessing in Python?",
"What are Python iterators and how do they work?",
"What is the purpose of the yield keyword?",
"What is monkey patching in Python?",
"What are modules and packages in Python?",
"What is the difference between map(), filter(), and reduce()?",
"What is a context manager and how does the with statement work?",
"What is the difference between @staticmethod and @classmethod?",
"What is method overriding in Python?",
"What are Python decorators used for in real applications?",
"What is the difference between is and == operators?",
"What is Python's garbage collection mechanism?",
"What is the difference between an iterator and an iterable?",
"What is the difference between list comprehension and generator expressions?",
"What is the use of the __init__ method in Python classes?",
"What is the difference between Python lists and NumPy arrays?"
],
"High level":[
"What are metaclasses in Python and how are they used?",
"Explain duck typing in Python with an example.",
"What are Python descriptors and how do they work?",
"What is Method Resolution Order (MRO) in Python?",
"What is the difference between asynchronous programming and multithreading?",
"What is asyncio and where is it used?",
"What are coroutines in Python?",
"What is memoization and how can it improve performance?",
"What is the difference between __str__() and __repr__() methods?",
"Explain Python's memory management system.",
"What is the purpose of __slots__ in Python classes?",
"What are closures in Python?",
"How do Python context managers work internally?",
"What is the difference between deepcopy and serialization?",
"What is dynamic typing and how does it affect Python programs?",
"What are Python wheels and why are they used?",
"What is the difference between CPython and PyPy?",
"What is the purpose of __name__ == '__main__' in Python?",
"Explain Python's module import system.",
"What is lazy evaluation and where is it used in Python?"
]
    },
    "java":{
        "beginner": [
"What is Java?",
"What are the main features of Java?",
"What is the difference between JDK, JRE, and JVM?",
"What is a class in Java?",
"What is an object in Java?",
"What is the difference between a class and an object?",
"What are the primitive data types in Java?",
"What is a constructor in Java?",
"What is method overloading?",
"What is method overriding?",
"What is inheritance in Java?",
"What is polymorphism in Java?",
"What is encapsulation in Java?",
"What is abstraction in Java?",
"What is the difference between an interface and an abstract class?",
"What is the difference between == and equals() in Java?",
"What is a package in Java?",
"What is the purpose of the main() method in Java?",
"What is the difference between stack and heap memory in Java?",
"What is exception handling in Java?"
],
"intermediate": [
"What is the difference between ArrayList and LinkedList in Java?",
"What is the difference between HashMap and HashTable?",
"What is the difference between String, StringBuilder, and StringBuffer?",
"What is the purpose of the final keyword in Java?",
"What is the difference between abstract class and interface in Java?",
"What is the difference between checked and unchecked exceptions?",
"What is the difference between throw and throws in Java?",
"What is multithreading in Java?",
"What is the difference between process and thread?",
"What is synchronization in Java?",
"What is the difference between Runnable and Thread class?",
"What is the Java Collections Framework?",
"What is the difference between HashSet and TreeSet?",
"What is method overriding and what rules must be followed?",
"What is the difference between static and non-static methods?",
"What is the difference between compile-time polymorphism and runtime polymorphism?",
"What is the purpose of the super keyword in Java?",
"What is the difference between composition and inheritance?",
"What is the difference between fail-fast and fail-safe iterators?",
"What is the difference between stack memory and heap memory in Java?"
],
"hard level": [
"What is the Java Memory Model (JMM)?",
"What is the difference between volatile and synchronized in Java?",
"How does garbage collection work in Java?",
"What are the different types of garbage collectors in Java?",
"What is the difference between fail-fast and fail-safe iterators internally?",
"What is the difference between Comparable and Comparator?",
"What is the difference between HashMap and ConcurrentHashMap?",
"What is the difference between ExecutorService and Thread?",
"What are deadlocks in Java and how can they be prevented?",
"What is the difference between Callable and Runnable?",
"What is the difference between shallow copy and deep copy in Java?",
"What is reflection in Java and when should it be used?",
"What is the difference between ClassLoader types in Java?",
"What is the difference between serialization and externalization?",
"What is the purpose of transient and volatile keywords?",
"What is the difference between wait(), notify(), and notifyAll()?",
"What are design patterns and why are they important in Java?",
"What is the Singleton design pattern and how can it be implemented in Java?",
"What is the difference between functional interface and normal interface?",
"What is the Stream API in Java and why is it used?"
],
    },
    "SQL":{
        "beginner": [
"What is SQL?",
"What are the different types of SQL commands?",
"What is a database?",
"What is a table in SQL?",
"What is the difference between DELETE, TRUNCATE, and DROP?",
"What is a primary key?",
"What is a foreign key?",
"What is the difference between WHERE and HAVING clause?",
"What is the difference between GROUP BY and ORDER BY?",
"What is a JOIN in SQL?",
"What are the different types of joins?",
"What is the difference between INNER JOIN and LEFT JOIN?",
"What is a NULL value in SQL?",
"What is a UNIQUE constraint?",
"What is a NOT NULL constraint?",
"What is a view in SQL?",
"What is normalization in databases?",
"What is the difference between CHAR and VARCHAR?",
"What is an index in SQL?",
"What is the difference between DDL, DML, and DCL commands?"
],
"intermdiate":[
"What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN?",
"What is a subquery and where can it be used?",
"What is the difference between correlated and non-correlated subqueries?",
"What is the difference between UNION and UNION ALL?",
"What is the difference between clustered and non-clustered indexes?",
"What is the difference between HAVING and WHERE clauses?",
"What is a self join?",
"What is a composite key?",
"What is a stored procedure?",
"What is a trigger in SQL?",
"What is the difference between DELETE and TRUNCATE?",
"What is normalization and what are its different forms?",
"What is denormalization?",
"What is a view and why is it used?",
"What is a transaction in SQL?",
"What are ACID properties in databases?",
"What is the difference between primary key and unique key?",
"What is indexing and why is it important?",
"What is the difference between GROUP BY and DISTINCT?",
"What is a correlated subquery with an example?"
],
"hard level": [
"How do you find the second highest salary from a table?",
"How do you find the nth highest salary in SQL?",
"How do you remove duplicate rows from a table?",
"How do you find employees who earn more than their manager?",
"How do you find departments with more than 5 employees?",
"How do you get the last record from a table?",
"How do you find records present in one table but not in another?",
"How do you find the top 3 highest salaries in each department?",
"How do you delete duplicate rows while keeping one record?",
"How do you display the current date and time in SQL?",
"How do you find the total salary department-wise?",
"How do you find employees who joined in the last 30 days?",
"How do you find the number of employees in each department?",
"How do you rank employees based on salary?",
"How do you calculate the running total in SQL?",
"How do you find the difference between two dates?",
"How do you find employees whose salary is greater than the average salary?",
"How do you pivot rows into columns in SQL?",
"How do you write a query to find gaps in sequence numbers?",
"What is the difference between ROW_NUMBER(), RANK(), and DENSE_RANK()?"
]
    },
    "dsa":{
        "beginner":[
"How would you detect a cycle in a linked list using Floyd’s algorithm?",
"How do you find the intersection point of two singly linked lists?",
"How would you reverse a linked list in-place?",
"How can you find the lowest common ancestor (LCA) in a binary tree?",
"How do you check if a binary tree is height-balanced?",
"How would you implement an LRU cache?",
"How can you detect a cycle in a directed graph?",
"How do you find the shortest path in a weighted graph?",
"What is Dijkstra’s algorithm and how does it work?",
"What is the difference between Prim’s and Kruskal’s algorithm?",
"How would you implement a Trie (prefix tree)?",
"How do you find the kth smallest element in a binary search tree?",
"How would you merge k sorted arrays efficiently?",
"How can you solve the N-Queens problem using backtracking?",
"How would you implement a priority queue using a heap?",
"What is memoization in dynamic programming?",
"How do you solve the longest common subsequence problem?",
"How would you find the maximum subarray sum using Kadane’s algorithm?",
"How would you detect a cycle in an undirected graph?",
"How do you find strongly connected components in a graph?"
],
"intermediate": [
"What is the difference between static and dynamic data structures?",
"What is the time complexity of insertion and deletion in an array and a linked list?",
"What is a circular linked list?",
"What is the difference between singly linked list and doubly linked list?",
"What is the difference between stack overflow and stack underflow?",
"What is the difference between BFS and DFS in terms of implementation?",
"What is a balanced binary tree?",
"What is an AVL tree?",
"What is the difference between a full binary tree and a complete binary tree?",
"What is the time complexity of binary search?",
"What is a heap data structure?",
"What is the difference between min heap and max heap?",
"What is collision in hashing and how can it be handled?",
"What are the different collision resolution techniques in hashing?",
"What is dynamic programming?",
"What is the difference between greedy algorithms and dynamic programming?",
"What is backtracking?",
"What is the difference between adjacency matrix and adjacency list representation of graphs?",
"What is the time complexity of BFS and DFS?",
"What is a priority queue?"
],
"hard":[
"How would you detect a cycle in a linked list using Floyd’s algorithm?",
"How do you find the intersection point of two singly linked lists?",
"How would you reverse a linked list in-place?",
"How can you find the lowest common ancestor (LCA) in a binary tree?",
"How do you check if a binary tree is height-balanced?",
"How would you implement an LRU cache?",
"How can you detect a cycle in a directed graph?",
"How do you find the shortest path in a weighted graph?",
"What is Dijkstra’s algorithm and how does it work?",
"What is the difference between Prim’s and Kruskal’s algorithm?",
"How would you implement a Trie (prefix tree)?",
"How do you find the kth smallest element in a binary search tree?",
"How would you merge k sorted arrays efficiently?",
"How can you solve the N-Queens problem using backtracking?",
"How would you implement a priority queue using a heap?",
"What is memoization in dynamic programming?",
"How do you solve the longest common subsequence problem?",
"How would you find the maximum subarray sum using Kadane’s algorithm?",
"How would you detect a cycle in an undirected graph?",
"How do you find strongly connected components in a graph?"
]
    },
    "react":{
        "beginner":[
"What is React?",
"What are the main features of React?",
"What is a component in React?",
"What is the difference between functional and class components?",
"What is JSX in React?",
"What is the virtual DOM?",
"What is the difference between props and state?",
"What is the purpose of useState hook?",
"What is the purpose of useEffect hook?",
"What is a React fragment?",
"What are controlled components in React?",
"What are uncontrolled components in React?",
"What is the purpose of keys in React lists?",
"What is conditional rendering in React?",
"What is the difference between React and JavaScript frameworks like Angular?",
"What is a single-page application (SPA)?",
"What is ReactDOM?",
"What is the difference between ReactDOM.render and createRoot?",
"What are React hooks?",
"What is the purpose of event handling in React?"
],
"intermediate":[
"What are React lifecycle methods?",
"What is the difference between useEffect and useLayoutEffect?",
"What is the purpose of useRef in React?",
"What is the Context API in React?",
"What is prop drilling and how can it be avoided?",
"What is React.memo and when should it be used?",
"What is the difference between useMemo and useCallback?",
"What is code splitting in React?",
"What is lazy loading in React?",
"What are Higher Order Components (HOC)?",
"What are render props in React?",
"What is the difference between controlled and uncontrolled components?",
"What is React Router and why is it used?",
"What is server-side rendering (SSR) in React?",
"What is hydration in React?",
"What are error boundaries?",
"What is React reconciliation?",
"What are pure components in React?",
"What is the difference between stateful and stateless components?",
"What are keys in React and why are they important?"
],
"hard":[
"How does React’s reconciliation algorithm work internally?",
"What is the difference between useEffect, useLayoutEffect, and useInsertionEffect?",
"How does React Fiber architecture work?",
"What are concurrent features in React 18?",
"What is Suspense in React and how does it work?",
"What is the difference between client-side rendering and server-side rendering?",
"What is hydration and why is it important in React SSR?",
"How does React handle batching of state updates?",
"What is the difference between controlled components and uncontrolled components internally?",
"How does React optimize rendering performance?",
"What are custom hooks and how do you design them?",
"What is the difference between memoization using React.memo, useMemo, and useCallback?",
"How does React manage state updates asynchronously?",
"What is the difference between context API and Redux for state management?",
"What are portals in React and when should they be used?",
"What are error boundaries and how are they implemented?",
"How does lazy loading work internally in React?",
"What are the performance issues in large React applications and how can they be solved?",
"What is the difference between shallow comparison and deep comparison in React?",
"What is the role of keys in React’s diffing algorithm?"
]
    
    },
    "html":{
        "beginner":["What is the difference between a class and an object in OOP?",  
"What is the difference between an abstract class and an interface?"  ,
"Explain the concept of inheritance with an example."  ,
"What are the main features of Java (or your preferred language)?",  
"What is a constructor and what is its purpose?"  ,
"What is the difference between == and equals() in Java?",  
"What is a data structure? Give examples."  ,
"What is an array and how is it different from a linked list?",  
"What is the difference between stack and queue?"  ,
"Explain the concept of recursion with an example." , 
"What is SQL and why is it used?"  ,
"What is the difference between DELETE and TRUNCATE in SQL?",  
"What are primary key and foreign key in a database?"  ,
"What is normalization and why is it important in databases?",  
"What is HTTP and HTTPS? Explain the difference."  ,
"What is a REST API?"  ,
"What is the difference between GET and POST request?",  
"Explain the difference between frontend and backend development.",  
"What is cloud computing and give examples of cloud providers?"  ,
"What is version control and why is Git used?"  
        ],
        "intermediate":["What is the difference between an ArrayList and a LinkedList in Java?"  ,
"Explain the concept of polymorphism with an example."  ,
"What is multithreading and how is it implemented in Java?",  
"What is the difference between process and thread?"  ,
"Explain deadlock and how it can be avoided."  ,
"What is the difference between Abstract Class and Interface in Java 8+?",  
"What are the different types of joins in SQL?"  ,
"What is indexing in a database and why is it important?",  
"Explain ACID properties in a database."  ,
"What is the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN?",  
"What is the difference between HashMap and Hashtable?"  ,
"Explain the difference between synchronized and concurrent collections in Java.",  
"What is a design pattern? Explain Singleton and Factory patterns."  ,
"Explain the difference between stack memory and heap memory."  ,
"What is exception handling and types of exceptions in Java?"  ,
"Explain the difference between REST API and SOAP API."  ,
"What is the difference between authentication and authorization?"  ,
"Explain the concept of caching and how it improves performance."  ,
"What is the difference between SQL and NoSQL databases?"  ,
"Explain the difference between synchronous and asynchronous programming."  ],
"hard":["Explain the difference between volatile, transient, and synchronized in Java.",  
"What is the difference between process-based and thread-based concurrency?"  ,
"Explain the difference between optimistic and pessimistic locking in databases.",  
"How does garbage collection work in Java? Explain different types of collectors.",  
"Explain the CAP theorem in distributed systems."  ,
"What is eventual consistency and how is it achieved?",  
"Explain the difference between SQL injection and NoSQL injection attacks.",  
"What are the different types of indexes in a database and when to use them?",  
"Explain the difference between microservices and monolithic architecture."  ,
"What is the difference between ACID and BASE in databases?"  ,
"Explain the difference between strong, weak, and eventual consistency in distributed systems.",  
"How does a HashMap work internally in Java?"  ,
"Explain how deadlock detection and avoidance works in operating systems.",  
"Explain the difference between compile-time and runtime polymorphism."  ,
"What is the difference between CAP theorem and PACELC theorem?"  ,
"Explain how load balancing works in cloud computing."  ,
"What are memory leaks in Java and how can they be detected and prevented?"  ,
"Explain the difference between synchronous and asynchronous messaging in distributed systems.",  
"Explain the difference between optimistic and pessimistic concurrency control."  ,
"What is the difference between Kubernetes and Docker Swarm for container orchestration?"  ]
    },
    "css":{
        "beginner":["What is CSS and why is it used?" , 
"What are the different types of CSS (inline, internal, external)?" , 
"What is the difference between ID and class selectors in CSS?"  ,
"What is the difference between relative, absolute, fixed, and sticky positioning?",  
"What are pseudo-classes in CSS? Give examples."  ,
"What is the difference between em, rem, px, and % units in CSS?" , 
"What is the difference between inline, block, and inline-block elements?",  
"What are the different ways to include CSS in an HTML file?"  ,
"What is the difference between relative and absolute units in CSS?",  
"What is the difference between visibility: hidden and display: none?",  
"What is the difference between inline and block elements?"  ,
"What are pseudo-elements in CSS? Give examples."  ,
"Explain the difference between CSS Grid and Flexbox.",  
"What is the difference between ID selector (#) and class selector (.)?",  
"What is the difference between position: relative and position: absolute?",  
"What are media queries in CSS and why are they used?"  ,
"What is the difference between min-width, max-width, and width in CSS?",  
"What is the difference between z-index and stacking context?"  ,
"What is the difference between transition and animation in CSS?",  
"What is the difference between CSS specificity and inheritance?"  ],
"intermediate":["What is the difference between relative, absolute, fixed, and sticky positioning in detail?",  
"Explain the difference between CSS Grid and Flexbox and when to use each."  ,
"What are pseudo-classes and pseudo-elements? Give examples of advanced usage.",  
"Explain the difference between inline, inline-block, and block elements with examples." , 
"What are CSS transitions and how do they differ from animations?"  ,
"What is the difference between transform and transition in CSS?"  ,
"Explain the difference between viewport units (vw, vh) and relative units (em, rem).",  
"What is the difference between rem and em units, and when should each be used?"  ,
"Explain the difference between CSS specificity and inheritance."  ,
"What are CSS combinators? Give examples (>, +, ~, space)."  ,
"What is the difference between relative, absolute, and fixed positioning in a nested element?",  
"What are media queries? Give an example of responsive design using them."  ,
"Explain the difference between z-index and stacking context in CSS."  ,
"How does CSS float work and what are its limitations?"  ,
"What is the difference between inline styles and !important in CSS?",  
"Explain CSS box-sizing property and its values (content-box, border-box).",  
"What is the difference between CSS variables and preprocessor variables (SASS/LESS)?" , 
"Explain the difference between opacity and visibility in CSS."  ,
"What is the difference between clip-path and overflow properties?",  
"Explain how to create a responsive layout using CSS Grid and Flexbox together."  ],
"hard":["Explain the difference between relative, absolute, fixed, sticky, and static positioning with complex scenarios.",  
"How does the CSS stacking context work and how does z-index interact with it?"  ,
"Explain the difference between CSS Grid’s auto-fill and auto-fit in responsive design." , 
"What is the difference between CSS transitions, animations, and keyframes? Give complex use cases.",  
"Explain the difference between transform: translate() and top/left positioning."  ,
"How do CSS pseudo-elements (::before, ::after) work in combination with content and counters?" , 
"Explain the difference between CSS calc(), min(), max(), and clamp() functions with examples."  ,
"How do CSS variables work in terms of inheritance and scope?"  ,
"What is the difference between absolute and relative units in complex layouts (px vs rem vs vw/vh)?",  
"Explain how CSS specificity is calculated and how !important affects it."  ,
"How does CSS will-change property work and how does it improve performance?" , 
"Explain the difference between CSS clip-path, mask, and shape-outside properties.",  
"How does CSS containment property work and when should it be used?"  ,
"Explain the difference between CSS Grid implicit and explicit tracks.",  
"How do CSS custom properties work with media queries and dynamic theming?",  
"Explain the difference between CSS flex-wrap, flex-grow, flex-shrink, and flex-basis in a complex layout." , 
"How does CSS object-fit and object-position work for images and videos?"  ,
"Explain the difference between relative, absolute, and sticky elements inside a transformed parent.",  
"How does CSS subgrid work and how is it different from the normal grid?"  ,
"Explain the difference between CSS blend modes and filters and give examples of practical use." ]   },
"javascript":{
    "beginner":["What is JavaScript and why is it used?",  
"What is the difference between var, let, and const in JavaScript?",  
"What are data types in JavaScript?"  ,
"What is the difference between == and === in JavaScript?",  
"What is the difference between null and undefined in JavaScript?" , 
"What are functions in JavaScript? Give an example."  ,
"What is the difference between function declaration and function expression?",  
"What is a callback function in JavaScript?"  ,
"What is the difference between global and local scope in JavaScript?",  
"What are arrays in JavaScript and how do you access elements?"  ,
"What is an object in JavaScript and how do you create one?"  ,
"What are events in JavaScript? Give an example."  ,
"What is the difference between for…in and for…of loops?",  
"What are template literals in JavaScript?"  ,
"What is the difference between synchronous and asynchronous code?",  
"What are JavaScript promises?"  ,
"What is the difference between arrow functions and regular functions?",  
"What is hoisting in JavaScript?"  ,
"What is the difference between window and document objects in JavaScript?" , 
"What is the difference between call(), apply(), and bind() methods?"  ],
"intermediate":["What is the difference between var, let, and const in terms of scope and hoisting?"  ,
"Explain closures in JavaScript with an example."  ,
"What is the difference between synchronous and asynchronous programming in JavaScript?",  
"What are JavaScript promises and how do you use them?"  ,
"What is async/await and how is it different from promises?",  
"Explain the difference between call(), apply(), and bind() methods with examples."  ,
"What is event delegation and why is it useful?"  ,
"Explain the concept of the 'this' keyword in JavaScript.",  
"What is the difference between shallow copy and deep copy of objects in JavaScript?" , 
"What are higher-order functions? Give examples in JavaScript."  ,
"What is the difference between == and === in JavaScript?"  ,
"What are JavaScript modules and how do you use import/export?",  
"Explain the difference between prototype and __proto__ in JavaScript.",  
"What is the difference between for…in and for…of loops in JavaScript?" , 
"Explain the difference between setTimeout and setInterval."  ,
"What is the event loop in JavaScript and how does it work?"  ,
"What is the difference between null, undefined, and NaN in JavaScript?",  
"What are JavaScript generators and how do they work?"  ,
"What is the difference between JSON.stringify() and JSON.parse()?" , 
"What is the difference between mutable and immutable objects in JavaScript?"  ],
"hard":["Explain the JavaScript event loop in detail with microtasks and macrotasks.",  
"What is the difference between call stack, task queue, and microtask queue?"  ,
"Explain closures and memory management implications in JavaScript."  ,
"What is the difference between prototype inheritance and class inheritance in JavaScript?",  
"Explain the concept of hoisting for variables and functions with examples."  ,
"What are JavaScript modules and the difference between ES6 modules and CommonJS?",  
"Explain how 'this' works in different contexts (global, object, class, arrow functions)." , 
"What is the difference between shallow copy and deep copy of objects and arrays?"  ,
"Explain the concept of currying and partial application in JavaScript."  ,
"How do JavaScript generators and iterators work?"  ,
"Explain the difference between mutable and immutable data structures in JavaScript.",  
"How do async/await, promises, and callbacks interact in the event loop?"  ,
"What is the difference between Object.freeze(), Object.seal(), and Object.preventExtensions()?",  
"Explain the difference between prototypal inheritance and functional inheritance."  ,
"How do JavaScript WeakMap and WeakSet differ from Map and Set?"  ,
"Explain the difference between synchronous, asynchronous, and deferred execution in JS."  ,
"How does JavaScript handle memory leaks and what are common causes?"  ,
"What are service workers in JavaScript and how do they work?"  ,
"Explain how to implement memoization in JavaScript for performance optimization.",  
"Explain the difference between classical inheritance and prototypal inheritance in ES6 classes and functions."  ]
},
"flask":{
    "beginner":["What is Flask and why is it used?",  
"What is the difference between Flask and Django?"  ,
"What are routes in Flask?"  ,
"How do you create a Flask application?",  
"What is the purpose of Flask’s app.run() method?",  
"What are Flask templates and how are they used?"  ,
"What is Jinja2 in Flask?"  ,
"How do you pass data from Flask to a template?" , 
"What is the difference between GET and POST methods in Flask?",  
"How do you handle form data in Flask?"  ,
"What are Flask static files and how are they used?"  ,
"What is the difference between Flask request and Flask session?",  
"How do you handle URL parameters in Flask?"  ,
"What is the purpose of Flask jsonify()?"  ,
"How do you handle 404 errors in Flask?"  ,
"What are Flask Blueprints and why are they useful?" , 
"What is the difference between Flask and FastAPI?"  ,
"How do you run a Flask app in debug mode?"  ,
"What are Flask extensions? Give examples."  ,
"How do you redirect a user to another route in Flask?"],
"intermediate":["What is the difference between Flask’s session and cookies?"  ,
"How do you manage configuration in a Flask application?"  ,
"Explain how Flask handles request and response objects."  ,
"What is the difference between Flask Blueprints and Flask applications?"  ,
"How do you handle database connections in Flask?"  ,
"Explain how Flask integrates with SQLAlchemy."  ,
"How do you implement user authentication in Flask?",  
"What is the difference between Flask’s @app.route() and @app.before_request decorators?",  
"How do you use Flask’s g object?"  ,
"How do you implement file uploads in Flask?",  
"Explain the difference between Flask’s app context and request context.",  
"How do you handle errors globally in a Flask application?"  ,
"How do you implement RESTful APIs using Flask?"  ,
"What are Flask signals and how are they used?"  ,
"How do you implement middleware in Flask?"  ,
"Explain how Flask handles JSON requests and responses." , 
"How do you use Flask-Migrate for database migrations?"  ,
"How do you manage environment variables in Flask?"  ,
"Explain Flask’s teardown_request and its use cases." , 
"How do you secure a Flask application against common web vulnerabilities?"  ],
"hard":["Explain Flask’s application and request contexts in detail."  ,
"How does Flask handle thread safety and concurrency?"  ,
"Explain the difference between Flask’s development server and production WSGI servers." , 
"How do you implement JWT-based authentication in Flask?"  ,
"How do you handle database connection pooling in Flask?"  ,
"Explain how Flask integrates with asynchronous frameworks like asyncio or Quart.",  
"How do Flask signals work internally and what are use cases?"  ,
"How do you implement custom middleware in Flask?"  ,
"Explain the difference between Flask’s before_request, after_request, and teardown_request hooks." , 
"How do you optimize performance for large-scale Flask applications?"  ,
"Explain how Flask handles session management and secure cookies."  ,
"How do you implement role-based access control in Flask?"  ,
"How do Flask extensions like Flask-Login or Flask-Mail work under the hood?" , 
"Explain the difference between Flask’s Blueprints and Flask extensions for modular applications.",  
"How do you implement rate limiting in a Flask API?"  ,
"Explain how Flask handles streaming responses and large file uploads."  ,
"How do you deploy a Flask app using Gunicorn and Nginx?"  ,
"How do you integrate Flask with caching systems like Redis or Memcached?",  
"Explain the difference between synchronous and asynchronous routes in Flask.",  
"How do you implement testing for Flask applications, including unit and integration tests?"  ]
},
"c":{
    "beginner":["What is C and why is it used?"  
"What are the basic data types in C?",  
"What is the difference between a variable and a constant in C?",  
"What are operators in C? Give examples."  ,
"What is the difference between =, ==, and != in C?"  ,
"What are conditional statements in C? Give examples." , 
"What are loops in C? Explain for, while, and do-while loops."  ,
"What is the difference between break and continue statements?"  ,
"What are arrays in C and how do you declare them?"  ,
"What is a pointer in C and why is it used?"  ,
"What is the difference between call by value and call by reference?" , 
"What are functions in C and how do you declare them?"  ,
"What is the difference between local and global variables in C?",  
"What is the purpose of the return statement in a function?"  ,
"What is the difference between printf() and scanf()?"  ,
"What are header files in C and why are they used?"  ,
"What is the difference between pre-increment and post-increment operators?",  
"What is the difference between struct and union in C?"  ,
"What is the difference between malloc() and calloc()?"  ,
"What is the difference between compiling and linking in C?"  ],
"intermediate":["What is the difference between stack and heap memory in C?",  
"Explain the difference between pointers and arrays in C."  ,
"What are function pointers and how are they used?"  ,
"Explain dynamic memory allocation and deallocation in C.",  
"What is the difference between malloc(), calloc(), realloc(), and free()?" , 
"Explain the difference between pass by value and pass by reference with pointers." , 
"What is the difference between a pointer to pointer and a double pointer?"  ,
"Explain the use of const keyword with pointers."  ,
"What is the difference between typedef and #define in C?",  
"Explain the difference between struct, union, and enum."  ,
"How does the sizeof operator work in C?"  ,
"Explain the difference between shallow copy and deep copy.",  
"What is the difference between volatile, static, and register variables?" , 
"Explain the use of preprocessor directives in C."  ,
"How does memory alignment and padding work in C structures?"  ,
"What is the difference between recursion and iteration in C?"  ,
"Explain dangling pointers and how to avoid them."  ,
"What is the difference between implicit and explicit typecasting in C?" , 
"What are segmentation fault and stack overflow errors?"  ,
"Explain the difference between inline functions and macros."  ],
"hard":["Explain the difference between static, extern, and register storage classes in C." , 
"How do pointers to functions work in C? Give examples of callback functions."  ,
"Explain memory management issues like memory leaks and dangling pointers."  ,
"How does pointer arithmetic work in C?"  ,
"What is the difference between stack memory and heap memory allocation?",  
"Explain the difference between shallow copy and deep copy in C."  ,
"How do you implement dynamic data structures like linked lists, stacks, and queues in C?" , 
"What is the difference between structure padding and memory alignment?"  ,
"Explain the difference between const pointer and pointer to const."  ,
"What is the difference between a segmentation fault and bus error?"  ,
"How does the C preprocessor work internally?"  ,
"Explain recursion and tail recursion. How does it affect stack usage?",  
"What are volatile and restrict keywords and how are they used in C?"  ,
"How does the compiler handle function calls and stack frames in C?"  ,
"Explain how memory is managed for multi-dimensional arrays in C."  ,
"What is the difference between calloc() and malloc() internally?"  ,
"Explain the difference between a pointer to void and a generic pointer.",  
"How does typecasting work between pointer types in C?"  ,
"Explain the use of flexible array members in structures." , 
"How do you implement efficient memory management in embedded C applications?"  ]
},
"c++":{
    "beginner":["What is C++ and how is it different from C?"  ,
"What are the basic data types in C++?"  ,
"What is the difference between a class and an object in C++?",  
"What are constructors and destructors in C++?"  ,
"What is the difference between a default constructor and a parameterized constructor?",  
"What is the difference between stack and heap memory in C++?"  ,
"What are access specifiers in C++ (public, private, protected)?" , 
"What is the difference between struct and class in C++?"  ,
"What is the difference between call by value and call by reference in C++?",  
"What are inline functions in C++?"  ,
"What is the difference between function overloading and operator overloading?",  
"What is a pointer in C++ and how is it used?"  ,
"What is the difference between new and malloc() in C++?" , 
"What is the difference between C-style strings and std::string?",  
"What are static members in a class?"  ,
"What is the difference between shallow copy and deep copy in C++?",  
"What are the advantages of using C++ over C?"  ,
"What is the difference between stack-allocated and heap-allocated objects?" , 
"What is the difference between references and pointers in C++?"  ,
"What is the difference between virtual and non-virtual functions in C++?",  ],
"intermediate":["What is the difference between function overloading and function overriding in C++?",  
"Explain the concept of polymorphism in C++."  ,
"What is the difference between compile-time and run-time polymorphism?",  
"Explain how inheritance works in C++ and its types."  ,
"What is the difference between public, private, and protected inheritance?",  
"What are virtual functions and why are they used?"  ,
"What is the difference between abstract class and interface in C++?",  
"Explain the difference between shallow copy and deep copy with copy constructors.",  
"What are smart pointers in C++ and how are they used?"  ,
"Explain the difference between stack memory and heap memory in C++."  ,
"What is the difference between new/delete and malloc()/free() in C++?" , 
"Explain the difference between static, dynamic, and virtual binding."  ,
"What is the difference between const, constexpr, and consteval in C++?" , 
"What are templates in C++ and how are they used?"  ,
"What is the difference between class templates and function templates?",  
"Explain multiple inheritance and the diamond problem in C++."  ,
"What is the difference between exception handling in C and C++?" , 
"What is the difference between friend function and member function in C++?"  ,
"What is the difference between typeid and dynamic_cast in C++?"  ,
"Explain the difference between RAII and manual resource management in C++."  ],
"hard":["Explain the difference between virtual inheritance and regular inheritance in C++." , 
"What is the difference between early binding and late binding in C++?"  ,
"How do smart pointers (unique_ptr, shared_ptr, weak_ptr) manage memory?" , 
"Explain the difference between deep copy and shallow copy with dynamic memory allocation.",  
"What is the difference between multiple inheritance and virtual inheritance?"  ,
"How does the vtable work in C++ for virtual functions?"  ,
"What is the difference between move constructor and copy constructor?",  
"Explain the difference between lvalue, rvalue, and xvalue in C++."  ,
"What is the difference between noexcept and throw() in exception handling?",  
"Explain the difference between stack unwinding and resource cleanup in C++." , 
"How does C++ handle object slicing and how can it be avoided?"  ,
"Explain the difference between CRTP (Curiously Recurring Template Pattern) and normal templates.",  
"What is the difference between placement new and regular new in C++?"  ,
"Explain the difference between typeid and dynamic_cast in runtime type identification.",  
"What are lambda functions and how do capture lists work?"  ,
"Explain the difference between constexpr functions and inline functions.",  
"What is the difference between POD and non-POD types in C++?"  ,
"How do C++11/14/17/20 features (like auto, decltype, concepts) affect type deduction?",  
"What is the difference between std::move and std::forward?"  ,
"Explain how multiple inheritance affects constructors, destructors, and vtables in C++."  ]
}
}
action_verbs=["developed","implemented","managed","designed","created","optimized","led","achieved","improved"]
required_sections=["objective","summary","skills","experience","education"]
#File type compatibility
preferred_formats=[".pdf",".docx"]
def extract_skills(text):
    text=text.lower()
    found_skills=[]

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)
    return found_skills

#Skill Gap
def skill_gap(found_skills,job_keywords):
     missing=[]
     for skill in job_keywords:
          if skill.lower() not in found_skills:
               missing.append(skill)
     return missing

#ATS Score(basic rules):
def ats_score(resume_text,job_keywords,file_name=None):
        errors=[]
        suggestions=[]
        score=100  #start with full marks
        text=resume_text.lower()

        for section in required_sections:
            if section not in text:
                score-=10 #missing section deduction
                errors.append(f"{section} section missing")
                suggestions.append(f"Add {section} section")

        missing_keywords=[]
        matched_keyword=0
        for kw in job_keywords:
             kw_lower=kw.lower()
             if kw_lower in text:
                  matched_keyword+=1
             else:
                  missing_keywords.append(kw)

        if job_keywords:
             keyword_score=(matched_keyword/len(job_keywords))*30
        else:
             keyword_score=0
        score-=(30-keyword_score)  #missing keywords deduct points
        if missing_keywords:
             suggestions.append("Add keywords:"+",".join(missing_keywords))
        verbs_count=0
        for v in action_verbs:
             verbs_count+=text.count(v)
        score+=min(verbs_count*2,15) #max 15 points
        #Achievement Detection
        achievements=re.findall(r'\d+%|\d+years?|\d+ [a-zA-Z]+',text)
        score+=min(len(achievements)*3,10) #max 10 points
        if len(achievements)==0:
             suggestions.append("Add measurable achievements (e.g.,30%, 50 users)")

        #File Type Check
        if file_name:
             if not any(file_name.lower().endswith(ext) for ext in preferred_formats):
                  score-=10   #non-preferred file type deduction
                  errors.append("Invalid file format")
                  suggestions.append("Use pdf or DOCX format")

        #Resume Length Check
        words= len(text.split())
        if words<300:
             score-=10
             suggestions.append("Increase resume length(300-800 words ideal)")
        elif words>800:
             score-=5
             suggestions.append("Reduce resume length(300-800 words ideal)")

        #Spelling check

        common_typos=["teh","recieve","adress","managment","langauge"]
        typo_count=sum(text.count(t) for t in common_typos)
        if typo_count>0:
             score-=typo_count*2 #each typo deduct 2 points
             errors.append("Spelling mistakes found ")
             suggestions.append("Fix spelling mistakes")


        #Final Score
        score=max(min(score,100),0)
        return score,errors,suggestions

#Question Gnerator
def get_questions(skill):
     return questions.get(skill.lower(), ["No questions available"]) 

#Score-Based Level System
def get_level(score):
     if score<3:
          return "Beginner"
     elif score<7:
          return "Intermdiate"
     else:
          return "Advanced"

@app.route("/analyse", methods=["POST"])
def analyse():
     file=request.files["resume_file"]
     keywords=request.form["keywords"]
     job_keywords=[k.strip() for k in keywords.split(",")]

     #pdf read
     #file check
     if not file or file.filename=="":
          return "file not found"
     try:
          file.stream.seek(0)
          reader=PdfReader(file.stream)
          text=""
          for page in reader.pages:
           content = page.extract_text()
           if content:
             text += content
     except Exception as e:
      return f"Error reading PDF:{str(e)}"
     #ATS Logic 
     score,errors,suggestions=ats_score(text,job_keywords,file.filename)
     found_skills = extract_skills(text)
     missing_keywords = skill_gap(found_skills, job_keywords)

     #send result to html page
     return render_template(
    "index2.html",
    score=score,
    errors=errors,
    suggestions=suggestions,
    found_skills=found_skills,
    missingSkills=missing_keywords
)

if __name__=="__main__":
     app.run(debug=True)




        

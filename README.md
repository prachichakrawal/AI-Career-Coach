AI Career Coach
Resume Analyzer & Mock Interview System

 Overview--
AI Career Coach is a web-based application designed to support students in placement preparation. It combines resume analysis with an interactive mock interview system to help users identify skill gaps and improve their performance.

The platform analyzes resumes, highlights missing skills, and provides a structured interview practice environment with real-time feedback.

 Key Features--
 -Resume analysis with scoring system (ATS-style)
 -Identification of missing and matched skills
 -Suggestions for improving resume quality
 -Mock interview practice across multiple domains
  (e.g., Python, Java, SQL, DSA)
 -Timer-based question answering
 -Skip question functionality
 -Final submission option (auto-skips remaining questions)
 -Answer evaluation system with feedback
 -Tech Stack
Backend: Python (Flask)
Frontend: HTML, CSS
Libraries Used:
PyPDF2 (for PDF parsing)
re (for text processing)
random (for question selection)

Project Structure--
AI-Career-Coach/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── index2.html
│   ├── select_subject.html
│   ├── question.html
│   └── result.html
│
├── static/
│   └── (optional CSS / assets)
│
├── requirements.txt
└── README.md
⚙️ How to Run the Project
Clone the repository
git clone https://github.com/your-username/AI-Career-Coach.git
cd AI-Career-Coach
Install dependencies
pip install -r requirements.txt
Run the Flask app
python app.py
Open in browser
http://127.0.0.1:5000/

Future Improvements--
Integration with AI-based evaluation (LLM APIs)
User authentication system
Performance analytics dashboard
More domain-specific interview questions

License--
This project is licensed under the MIT License.


Acknowledgment--
This project was developed as part of placement preparation to combine practical learning with real-world problem solving.


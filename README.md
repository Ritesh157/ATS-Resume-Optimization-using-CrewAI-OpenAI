📄 Resume Analyzer AI (with CrewAI Agents)

An AI-powered application that analyzes resumes, extracts structured information, identifies skill gaps against a target job description, generates cover letters, and visualizes skill match results — all using CrewAI multi-agent architecture and Streamlit.

This project is ideal for job seekers, recruiters, and HR automation workflows.

🚀 Features
✅ 1. Resume Parsing Agent

Extracts text from PDF, DOCX, and TXT files

Extracts:

Name

Email

Phone

Skills

Experience

Education

✅ 2. Skill-Gap Analysis Agent

Compares candidate skills vs. required skills (from a job description) and provides:

Matched skills

Missing skills

Suggestions for improvement

Summary of skill alignment

Includes a donut chart visualization showing skill match percentage.

✅ 3. Cover Letter Agent

Generates a professional, well-formatted cover letter tailored to:

Candidate's resume

Job title

Company

Required skills

✅ 4. Multi-Agent Workflow (CrewAI)

Each task is handled by a separate CrewAI agent:

Agent	Responsibility
Resume Parser Agent	Extracts text & structured info
Skill-Gap Agent	Finds matched/missing skills + suggestions
Cover Letter Agent	Writes tailored cover letter

✅ 5. Streamlit User Interface

Simple UI where users can:

Upload resumes

Enter job descriptions

Generate cover letters

See skill gap report

🛠 Tech Stack & Tools
Programming Language

Python 3.11

| Tool                     | Purpose                            |
| ------------------------ | ---------------------------------- |
| **CrewAI**               | Multi-agent LLM workflow           |
| **Streamlit**            | Web UI                             |
| **LangChain** (optional) | Prompt templates & text processing |

| Library         | Purpose                 |
| --------------- | ----------------------- |
| **pypdf**       | Extract text from PDF   |
| **python-docx** | Extract text from DOCX  |
| **docx**        | Write DOCX content      |
| **BytesIO**     | In-memory file handling |

| Tool                  | Purpose                               |
| --------------------- | ------------------------------------- |
| **virtualenv / venv** | Virtual environment                   |
| **python-dotenv**     | Environment variables                 |
| **utils.py**          | File/text conversion helper functions |

🔧 Installation & Setup
1. Create virtual environment (Python 3.11 recommended)
python3.11 -m venv crew
crew\Scripts\activate  # (Windows)
source crew/bin/activate  # (Mac/Linux)

2. Install dependencies
pip install -r requirements.txt

3. Run Streamlit App
streamlit run streamlit_app.py

📝 How It Works (Flow)

User uploads a resume

Resume Parser Agent extracts text + structured fields

User pastes job description

Skill-Gap Agent compares and calculates skill score

Cover Letter Agent generates a tailored cover letter

Streamlit displays outputs beautifully

⚙️ utils.py Purpose

Contains helper functions like:

Extract text from PDF

Extract text from DOCX

Convert TXT → DOCX

Clean & normalize text

🤖 Agents Overview
Resume Parser Agent

Extracts text + key details.

Skill-Gap Agent

Compares candidate skills vs. required job skills.

Cover Letter Agent

Generates a highly personalized cover letter
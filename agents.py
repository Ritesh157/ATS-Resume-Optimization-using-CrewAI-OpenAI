from crewai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
MODEL = "gpt-4o-mini"

# This function return Agent which parse the resume.
def build_parser_agent():
    return Agent(
        role="Resume Parsing Specialist", # a human-friendly label describing the agent’s job
        goal="Extract clean, structured text from a resume suitable for ATS optimization.", # the agent’s short, explicit objective. Agents use this to guide behavior
        backstory=(
            "You efficiently clean resume text by removing artifacts and normalizing formatting. "
            "Focus on speed and accuracy - preserve all important content while removing noise."
        ), # extra context describing HOW the agent should behave (style, priorities). Here it emphasizes speed, accuracy, and removing noise
        model = MODEL,
        temperature=0.0, # sets the randomness of the model’s outputs = 0.0 which means deterministic/focused answers (good for parsing where you want consistent output).
        max_iter=1, # limits the number of internal iterations the agent will run. 1 means do the job once
        max_execution_time=120, # maximum time (in seconds) the agent is allowed to run before being stopped (120 seconds here).
    )

# This function returns an agent that rewrites or constructs resumes optimized for Applicant Tracking Systems (ATS).
# This agent receives parsed/cleaned text and rewrites it to maximize ATS score and match job descriptions
def build_ats_writer_agent():
    return Agent(
        role="ATS Optimization Writer",
        goal="Create a high-scoring ATS-optimized resume that matches job requirements perfectly.",
        backstory=(
            "You are an expert at transforming resumes into ATS-friendly formats that score 80+ points. "
            "You strategically place keywords, use strong action verbs, and quantify all achievements. "
            "You work quickly and deliver results that pass ATS systems."
        ),
        model=MODEL,
        temperature=0.3, # slightly more creative
        max_iter=1,
        max_execution_time=120
    )

# This function returns an agent that scores resumes for ATS compatibility and gives suggestions.
# Use this agent to check how well a resume will perform and to get concrete improvements.
def build_evaluator_agent():
    return Agent(
        role="ATS Evaluator",
        goal="Provide accurate ATS scores and actionable improvement recommendations.",
        backstory=(
            "You are a precise ATS scoring expert who quickly identifies gaps and provides specific, "
            "actionable recommendations. You focus on keyword density, section structure, and measurable achievements."
        ),
        model=MODEL,
        temperature=0.0,
        max_iter=1,
        max_execution_time=120
        
    )

def build_refiner_agent():
    return Agent(
        role="Bullet Point Refiner",
        goal="Transform bullet points into high-impact, ATS-optimized statements with strong metrics.",
        backstory="You excel at creating powerful bullet points that combine action verbs, specific achievements, and quantified results. You work efficiently to maximize impact.",
        model=MODEL,
        temperature=0.2,
        max_iter=1,
        max_execution_time=120
    )

def build_cover_letter_agent():
    return Agent(
        role="Cover Letter Writer",
        goal=" Generate a professional, personalized cover letter based on the user's resume and job description.",
        backstory=(
            "You are an expert cover letter writer. You craft concise, compelling, job-specific "
            "cover letters that highlight the candidate’s strengths, achievements, and alignment "
            "with the company’s needs."
        ),
        model=MODEL,
        temperature=0.5,
        max_iter=1,
        max_execution_time=120
    )

def build_skill_gap_agent():
    return Agent(
        role="Skill Gap Analyst",
        goal="Identify missing and weak skills by comparing the resume with the job description.",
        backstory=(
            "You are an expert in job market skill analysis. You compare job descriptions "
            "with resumes and produce clear insights on missing skills and improvement areas."
        ),
        model=MODEL,
        temperature=0.3,
        max_iter=1,
        max_execution_time=120
    )
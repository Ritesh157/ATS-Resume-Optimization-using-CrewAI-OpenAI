'''
A Task defines a specific job you want an Agent to perform
Each task includes:
    1) description → what the agent must do
    2) agent → which agent will do it
    3) expected_output → the format/type of answer you expect
'''

from crewai import Task
'''
Defines a function that creates a resume parsing task.
It receives:
    1) agent → the parser agent
    2) raw_resume_text → original resume text
If the resume is longer than 1500 characters, it cuts it down to 1500 chars and adds "..." (To prevent sending HUGE text to the LLM (saves tokens, cost, and errors))
If shorter, it uses full text.
The task description explains exactly what the agent must do.
\n\n adds blank lines to keep text readable for the model.
Assigns the agent who should perform this task (the parsing agent).
Describes what the agent’s answer should look like.
'''
def parse_resume_task(agent, raw_resume_text):
    truncated_text = raw_resume_text[:1500] + "..." if len(raw_resume_text)>1500 else raw_resume_text

    return Task(
        description=(
            f"Clean this resume text quickly:\n\n{truncated_text}\n\n"
            "Remove artifacts, normalize bullets to '-', keep all content. Be fast and direct."
        ),
        agent=agent,
        expected_output=("Clean resume text with proper structure.")
    )


'''
This task rewrites the cleaned resume to match the job description.
Task description tells the agent to:
    1) match keywords in the job description
    2) rewrite resume
    3) add metrics
    4) aim for 80+ ATS score

Assigns the ATS writer agent
Defines expected output
'''
def rewrite_for_ats_task(agent, cleaned_resume_text, job_title, job_description):
    truncated_resume = cleaned_resume_text[:1200] + "..." if len(cleaned_resume_text)>1200 else cleaned_resume_text
    truncated_jd = job_description[:300] + "..." if len(job_description)>300 else job_description

    return Task(
        description=(
            f"Rewrite resume for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Match keywords, use action verbs, add metrics. Target 80+ ATS score. Be direct and fast."
        ),
        agent=agent,
        expected_output="ATS-optimized resume with keyword placement and metrics."
    )

'''
This task improves bullet points.
Tells the agent to:
    1) refine bullet points
    2) use strong verbs
    3) add quantifiable metrics

Assigns the bullet refiner agent.

'''
def refine_bullets_task(agent, rewritten_resume_text):
    truncated_text = rewritten_resume_text[:1000] + "..." if len(rewritten_resume_text) > 1000 else rewritten_resume_text

    return Task(
        description=(
            f"Polish these bullets with action verbs and metrics:\n\n{truncated_text}\n\n"
            "Add strong verbs and numbers. Be fast and direct."
        ),
        agent=agent,
        expected_output="Resume with enhanced bullet points and metrics."
    )

'''
This task scores the final resume.
Inputs:
    1) evaluator agent
    2) final resume
    3) job title + JD

This tells the evaluator agent:
    1) rate key areas
    2) produce structured JSON output
    3) give missing keywords
    4) give quick improvement tips

The final output must be JSON
'''
def evaluate_ats_task(agent, final_resume_text, job_title, job_description):
    truncated_resume = final_resume_text[:800] + "..." if len(final_resume_text) > 800 else final_resume_text
    truncated_jd = job_description[:200] + "..." if len(job_description) > 200 else job_description
    
    return Task(
        description=(
            f"Score this resume for {job_title}:\n\n"
            f"JOB: {truncated_jd}\n\n"
            f"RESUME: {truncated_resume}\n\n"
            "Rate 1-5: keywords, structure, metrics, verbs, format. Return JSON with overall_score (0-100), breakdown, missing_keywords, quick_wins."
        ),
        agent=agent,
        expected_output="JSON evaluation with scores and recommendations."
    )

def cover_letter_task(agent, final_resume_text, job_title, job_description):
    return Task(
        description=(
            f"Write a professional, personalized cover letter for the role of {job_title}.\n\n"
            f"JOB DESCRIPTION:\n{job_description[:400]}...\n\n"
            f"RESUME:\n{final_resume_text[:800]}...\n\n"
            "Output a clean, formal cover letter with:\n"
            "- Strong opening\n"
            "- Key accomplishments\n"
            "- Fit for role\n"
            "- Closing paragraph\n"
            "Keep it 3–4 paragraphs."

        ),
        agent=agent,
        expected_output="A well-structured, polished cover letter."
    )

def skill_gap_task(agent, final_resume_text, job_title, job_description):
    return Task(
        description=(
            f"Analyze skill gaps for the role: {job_title}.\n\n"
            f"JOB DESCRIPTION:\n{job_description[:400]}...\n\n"
            f"RESUME:\n{final_resume_text[:800]}...\n\n"
            "Compare skills between RESUME and JOB DESCRIPTION.\n"
            "Return result STRICTLY as JSON with fields:\n"
            "{\n"
            "  'matched_skills': [...],\n"
            "  'missing_skills': [...],\n"
            "  'weak_skills': [...],\n"
            "  'priority_gaps': [ { 'skill': '', 'reason': '' } ],\n"
            "  'recommendations': [...]\n"
            "}\n"
            "Keep the JSON clean. No extra text."
        ),
        agent=agent,
        expected_output="JSON describing skill gaps and recommendations."
    )



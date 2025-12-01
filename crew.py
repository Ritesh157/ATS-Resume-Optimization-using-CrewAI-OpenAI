import os
# Crew is the object that runs agents and tasks together.
# Process has modes (like sequential) that tell the Crew how to run tasks.
from crewai import Crew, Process

# imports functions that create the four agents (parser, writer, evaluator, refiner)
from agents import (
    build_parser_agent, build_ats_writer_agent, build_refiner_agent, build_evaluator_agent, build_cover_letter_agent, build_skill_gap_agent
)

# imports functions that build the task objects for each step (parsing, rewriting, refining, evaluating).
from tasks import (
    parse_resume_task, rewrite_for_ats_task, evaluate_ats_task, refine_bullets_task, cover_letter_task, skill_gap_task
)

# create a Crew object wired with agents and tasks (but note: this version uses placeholder task inputs)
def build_crew(raw_resume_text: str, job_title: str, job_description: str):
    # Calls the builder functions to create four agent objects and stores them in variables.
    # Each variable is now an agent ready to do its role.
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()

    # Creates a parse task that instructs the parser agent to clean the raw_resume_text.
    t_parse = parse_resume_task(parser, raw_resume_text)
    # these are placeholders; we'll stitch later after parse result is known.
    # These three lines create Task objects for rewrite/refine/evaluate but pass placeholder strings (like "{t_parse}" and "{{...}}") instead of real text
    t_rewrite = rewrite_for_ats_task(writer, "{CLEANED_RESUME}", job_title, job_description)
    t_refine = refine_bullets_task(refiner, "{REWRITTEN_RESUME}")
    t_eval = evaluate_ats_task(evaluator, "{FINAL_RESUME}", job_title, job_description)


    crew = Crew(
        agents=[parser, writer, refiner, evaluator], # the four agents to run
        tasks=[t_parse, t_rewrite, t_refine, t_eval], # the four tasks to perform (in the order listed)
        process=Process.sequential, # run tasks one after another in order (not in parallel)
        verbose=True # print helpful information while running
    )
    return crew # Returns the Crew object to the caller

# Defines a function to actually run the whole resume pipeline step-by-step and return results.
def run_pipeline(raw_resume_text: str, job_title: str, job_description: str):
    # Creates the four agents again (separate instances for this pipeline run).
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()
    cover_letter_writer = build_cover_letter_agent()
    skill_gap_agent = build_skill_gap_agent()

    # Create tasks
    t_parse = parse_resume_task(parser, raw_resume_text)

    # Build and run crew for parsing
    parse_crew = Crew(
        agents=[parser],
        tasks=[t_parse],
        process=Process.sequential,
        verbose=True
    )

    # Execute parsing
    parse_result = parse_crew.kickoff() # runs the crew (agent executes the task) and returns the result
    cleaned = str(parse_result).strip() # str(parse_result).strip() converts it to a plain string and removes extra spaces/newlines.

    # Create rewrite task with cleaned resume
    t_rewrite = rewrite_for_ats_task(writer, cleaned, job_title, job_description)
    rewrite_crew = Crew(
        agents=[writer],
        tasks=[t_rewrite],
        process=Process.sequential,
        verbose=True
    )

    # Execute rewriting
    rewrite_result = rewrite_crew.kickoff()
    rewritten = str(rewrite_result).strip()

    # Create refine task with rewritten resume
    t_refine = refine_bullets_task(refiner, rewritten)
    refine_crew = Crew(
        agents=[refiner],
        tasks=[t_refine],
        process=Process.sequential,
        verbose=True
    )

    # Execute refining
    refine_result = refine_crew.kickoff()
    final_resume = str(refine_result).strip()

    # Create cover letter task
    t_cover = cover_letter_task(cover_letter_writer, final_resume, job_title, job_description)
    cover_crew = Crew(
        agents=[cover_letter_writer],
        tasks=[t_cover],
        process=Process.sequential,
        verbose=True
    )

    # Execute Cover Letter
    cover_result = cover_crew.kickoff()
    cover_letter = str(cover_result).strip()

    # Skill-gap analysis
    t_skill_gap = skill_gap_task(skill_gap_agent, final_resume, job_title, job_description)
    skill_gap_crew = Crew(
        agents=[skill_gap_agent],
        tasks=[t_skill_gap],
        process=Process.sequential,
        verbose=True
    )

    # Execute Skill-gap analysis
    skill_gap_result = skill_gap_crew.kickoff()
    skill_gap_json = str(skill_gap_result).strip()

    # Create evaluation task with final resume
    t_eval = evaluate_ats_task(evaluator, final_resume, job_title, job_description)
    eval_crew = Crew(
        agents=[evaluator],
        tasks=[t_eval],
        process=Process.sequential,
        verbose=True
    )

    # Execute evaluation
    eval_result = eval_crew.kickoff()
    evaluation = str(eval_result).strip()

    return cleaned, rewritten, final_resume, evaluation, cover_letter, skill_gap_json
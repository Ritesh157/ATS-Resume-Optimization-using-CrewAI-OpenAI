import os
import json
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from file_tools.file_loader import detect_and_extract
from crew import run_pipeline
from utils import txt_to_docx_bytes

load_dotenv()
# sets the Streamlit page title, icon, and layout width for the app
st.set_page_config(page_title="ATS Resume Agent (CrewAI)", page_icon="🧠", layout="wide")

# shows the big header at top of the page.
st.title("🧠 ATS-Optimized Resume Agent (CrewAI + OpenAI)")
# shows a small description under the title explaining what the app does.
st.caption("Upload your resume (.pdf or .docx), target a role, and get an ATS-friendly version with scores & quick wins.")


# with st.sidebar: — everything indented under this will appear in the app’s left sidebar.
# st.subheader(...) — shows a smaller header inside the sidebar.
# st.text_input(...) — displays a text field pre-filled with the model name; disabled=True means user can’t edit it (informational only)
# st.write(...) — prints simple text showing that the API key is loaded (informational).

with st.sidebar:
    st.subheader("OpenAI Settings")
    st.text_input("Model:", value="gpt-4o-mini", disabled=True)
    st.write("API Key loaded: ✅ Working OpenAI key")


# st.columns([1,1]) creates two equal columns side by side.
# In the left column (colL) we have st.file_uploader(...) where user can upload a resume file (.pdf, .docx, .txt). The uploaded file object is stored in up.
# In the right column (colR) we have job_title (single-line input) and job_desc (multi-line text area for the job description).

colL, colR = st.columns([1,1])
with colL:
    up = st.file_uploader("Upload Resume (.pdf or .docx preferred)", type=["pdf", "docx", "txt"])
with colR:
    job_title = st.text_input("Target Job Title (e.g., 'Machine Learning Engineer')")
    job_desc = st.text_area("Paste Job Description", height=220, placeholder="Paste JD here...")

# run_btn becomes True when the user clicks the “Run ATS Agent” button
run_btn = st.button("Run ATS Agent")

# st.tabs([...]) creates four tabs which shows different outputs (cleaned text, rewritten, final, and evaluation).
tabs = st.tabs(["Cleaned Resume", "Rewritten (ATS-optimized)", "Final (Refined Bullets)", "ATS Evaluation", "Cover Letter", "Skill-Gap Analysis"])

# only runs when user clicked the button
if run_btn:
    if up is None: # if no file uploaded, show an error
        st.error("Please upload a resume file.")
    elif not job_title or not job_desc: # if job title or job description is empty, show an error
        st.error("Please provide a target job title and job description.")
    else:
        ext, raw_text = detect_and_extract(up.name, up.read())
        if not raw_text.strip():
            st.error("Could not extract any text from the file.")
        else:
            with st.spinner("Running Crew agents..."):
                cleaned, rewritten, final_resume, evaluation, cover_letter, skill_gap_json = run_pipeline(
                    raw_resume_text=raw_text, 
                    job_title=job_title.strip(), 
                    job_description=job_desc.strip()
                )
            
            with tabs[0]:
                st.subheader("Cleaned Resume (plain text)") # shows small heading
                st.code(cleaned, language="markdown") # displays the cleaned resume as code-formatted text (keeps whitespace).
                st.download_button(
                    "Download cleaned.txt", # lets user download the cleaned text as cleaned_resume.txt
                    data=cleaned.encode("utf-8"), # converts string to bytes for download.
                    file_name="cleaned_resume.txt",
                    mime="text/plain"
                )
            
            with tabs[1]:
                st.subheader("Rewritten Resume (ATS-optimized)")
                st.code(rewritten, language="markdown")
                st.download_button(
                    "Download rewritten.txt",
                    data=rewritten.encode("utf-8"),
                    file_name="rewritten_resume.txt",
                    mime="text/plain"
                )
            
            with tabs[2]:
                st.subheader("Final Resume (Refined Bullets)")
                st.code(final_resume, language="markdown")

                # Offer DOCX & TXT downloads
                # lets user download plain text file final_resume.txt
                st.download_button(
                    "Download final.txt",
                    data=final_resume.encode("utf-8"),
                    file_name="final_resume.txt",
                    mime="text/plain"
                )
                
                # Then it tries to convert the text to a real Word file (.docx) using txt_to_docx_bytes(final_resume). 
                # If that succeeds, it shows a second download button for final_resume.docx. 
                # If conversion fails, it shows a warning message with the error.
                
                try:
                    docx_bytes = txt_to_docx_bytes(final_resume)
                    st.download_button(
                        "Download final.docx",
                        data=docx_bytes,
                        file_name="final_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.warning(f"Could not generate DOCX: {e}")
            
            with tabs[3]:
                st.subheader("ATS Evaluation & Suggestions")
                # Try to parse evaluation as JSON-like
                parsed = None
                try:
                    # Allow loose JSON (single quotes); try a quick fix
                    text = evaluation.strip()
                    fixed = text.replace("'", '"') # naively converts single quotes to double quotes to help with parsing if the agent returned single-quoted data
                    parsed = json.load(fixed)
                except Exception:
                    pass
                
                # If parsed is a dictionary (valid JSON):
                if parsed and isinstance(parsed, dict):
                    st.json(parsed) # st.json(parsed) pretty-prints the JSON structure
                    # Pretty headline
                    # If the parsed JSON contains overall_score, st.metric(...) displays a large metric badge like “Overall ATS Score: 85/100”
                    if "overall_score" in parsed:
                        st.metric("Overall ATS Score", f"{parsed['overall_score']}/100")
                else:
                    st.write("Raw evaluation output:")
                    st.code(evaluation, language="json")
            
            with tabs[4]:
                st.subheader("Generated Cover Letter")
                st.code(cover_letter, language="markdown")

                st.download_button(
                    "Download cover_letter.txt",
                    cover_letter.encode("utf-8"),
                    "cover_letter.txt",
                    mime="text/plain"
                )

                try:
                    docx_bytes = txt_to_docx_bytes(cover_letter)
                    st.download_button(
                        "Download Cover_letter.docx",
                        data=docx_bytes,
                        file_name="Cover_letter.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.warning(f"Could not generate DOCX: {e}")
            
            with tabs[5]:
                st.subheader("Skill-Gap Analysis")
                parsed = None
                try:
                    fixed = skill_gap_json.replace("'", '"')
                    parsed = json.loads(fixed)
                except:
                    pass

                if parsed:
                    st.json(parsed)
                else:
                    st.write("Raw Output:")
                    st.code(skill_gap_json, language="json")









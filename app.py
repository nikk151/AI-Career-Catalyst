import streamlit as st
from utils import text_extractor
from utils import get_ai_analysis
from utils import fetch_github_repos
from utils import get_project_ranking

st.set_page_config(page_title="AI Career Catalyst", layout="wide")

st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Select tool", ["Resume Optimizer", "GitHub Project Ranker", "Skill Gap Analysis", "AI Mock Interview"])

st.title("AI Career Catalyst")
st.subheader("Optimize your path to your dream job")

job_description = st.text_area("Enter Job Description Here", height=200) 

if app_mode == "Resume Optimizer":
    st.header("📄 Resume Optimizer")
    file_uploaded = st.file_uploader("Upload Your Resume Here", type="pdf")
    
    if st.button("Analyze & Optimize"): 
        if file_uploaded and job_description:
            st.info("The AI is now analyzing your bullet points for 'Impact'...")
            
            resume_text = text_extractor(file_uploaded)
            
            if not resume_text:
                st.error("Error: Could not extract text. Is this a scanned PDF (image)?")
            else:
                
                st.write(get_ai_analysis(resume_text, job_description))
            
        else:
            st.warning("Please upload a resume and provide a job description first.")

elif app_mode == "GitHub Project Ranker":
    st.header("🐙 GitHub Project Ranker")
    github_user = st.text_input("Enter your GitHub Username")
    if st.button("Rank My Projects"):
        if github_user:
            st.write(f"Fetching projects for {github_user} and matching with JD...")
            project_data=fetch_github_repos(github_user)
            
            st.text_area("Function Output", value=get_project_ranking(project_data, job_description), height=200)
        else:
            st.error("Please enter a GitHub username.")
        
elif app_mode == "Skill Gap Analysis":
    st.header("📊 Skill Gap Visualization")
    st.write("Compare your skills against the job requirements.")
    
elif app_mode == "AI Mock Interview":
    st.header("🤖 AI Mock Interviewer")
    st.write("Practice for your interview based on your optimized resume.")
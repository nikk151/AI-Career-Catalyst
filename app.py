import streamlit as st
from utils import text_extractor
from utils import get_ai_analysis
from utils import fetch_github_repos
from utils import get_project_ranking
from utils import get_skill_gap_analysis
from utils import get_interview_response


st.set_page_config(page_title="AI Career Catalyst", layout="wide")

st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Select tool", ["Resume Optimizer", "GitHub Project Ranker", "Skill Gap Analysis", "AI Mock Interview"])

st.title("AI Career Catalyst")
st.subheader("Optimize your path to your dream job")

job_description = st.text_area("Enter Job Description Here", height=200) 
file_uploaded = st.file_uploader("Upload Your Resume Here", type="pdf")
resume_text=""""""
if file_uploaded:
    resume_text = text_extractor(file_uploaded)

if app_mode == "Resume Optimizer":
    st.header("📄 Resume Optimizer")
    
    if st.button("Analyze & Optimize"): 
        if file_uploaded and job_description:
            st.info("The AI is now analyzing your bullet points for 'Impact'...")
            
            
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
    
    if st.button("Analyze Gaps"):
        if file_uploaded and job_description:
            st.info("Analyzing crucial missing skills...")

            
            gap_analysis = get_skill_gap_analysis(resume_text, job_description)
            
            st.write(gap_analysis)
            
        else:
            st.warning("Please upload a resume and job description.")
    
elif app_mode == "AI Mock Interview":
    st.header("🤖 AI Mock Interviewer")
    st.write("Practice for your interview based on your optimized resume.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        st.session_state.messages.append({
            "role": "system", 
            "content": "You are a Technical Interviewer. Ask the candidate questions based on their resume. Ask ONE question at a time. Wait for their answer."
        })
        
    if len(st.session_state.messages) == 1:
        if st.button("Start Interview"):
            if resume_text:
                
                initial_prompt = f"Here is my resume: {resume_text}. Start the interview by asking me about my most recent project."
                
                st.session_state.messages.append({"role": "user", "content": initial_prompt})
                
                with st.spinner("Thinking..."):
                    ai_response = get_interview_response(st.session_state.messages)
                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.rerun() 
            else:
                st.warning("Please upload your resume first!")

    for message in st.session_state.messages:
        if message["role"] != "system" and "Here is my resume" not in message["content"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

   
    if prompt := st.chat_input("Type your answer here..."):
        
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Interviewer is thinking..."):
            ai_response = get_interview_response(st.session_state.messages)
            
        with st.chat_message("assistant"):
            st.write(ai_response)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        
        

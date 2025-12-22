import fitz  
import os
from dotenv import load_dotenv
from groq import Groq
import requests 

load_dotenv() 
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_ai_analysis(resume_text, job_desc):
    system_prompt = "You are an expert Technical Recruiter. Compare the resume against the job description."
    
    user_prompt = f"Resume: {resume_text}\n\nJob Description: {job_desc}\n\nProvide 3 specific improvements."

    # The API call method
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model="llama-3.3-70b-versatile", 
    )
    
    return chat_completion.choices[0].message.content

def text_extractor(uploaded_file):
    
    uploaded_file.seek(0)
    
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        
        for page in doc:
            text += page.get_text()
            
    return text.strip()



def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        
        project_data = ""
        for repo in repos:
            project_data += f"Project: {repo['name']}\nDescription: {repo['description']}\nTech Stack: {repo['language']}\n\n"
        return project_data
    else:
        return None
    
def get_project_ranking(project_data, job_desc):
    system_prompt = "You are a Tech Lead evaluating a candidate's portfolio."
    
    user_prompt = f"""
    Job Description: {job_desc}
    
    Candidate's Projects:
    {project_data}
    
    Task:
    1. Rank the top 3 projects that best match the Job Description.
    2. For each, explain WHY it is relevant (e.g., "This project uses Python which matches the JD's requirement for Data Analysis").
    3. Suggest one technical improvement for the #1 project to make it even stronger.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model="llama-3.3-70b-versatile",
    )
    
    return chat_completion.choices[0].message.content
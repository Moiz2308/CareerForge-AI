import streamlit as st
import os
import json
import pypdf
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# --- 1. CONFIGURATION & SETUP ---
load_dotenv()
API_KEY = os.getenv("IBM_WATSONX_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
IBM_URL = os.getenv("IBM_URL")

st.set_page_config(page_title="CareerForge AI", page_icon="🚀", layout="wide")

# --- 2. CORE AI ENGINE (IBM GRANITE) ---
def get_granite_response(prompt_text):
    if not API_KEY or not PROJECT_ID:
        return "❌ Error: API Keys missing in .env file."

    credentials = {"url": IBM_URL, "apikey": API_KEY}
    
    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.MIN_NEW_TOKENS: 10,
        GenParams.TEMPERATURE: 0.7,
        GenParams.REPETITION_PENALTY: 1.1
    }
    
    model = ModelInference(
        model_id="ibm/granite-3-8b-instruct",
        params=params,
        credentials=credentials,
        project_id=PROJECT_ID
    )
    
    return model.generate_text(prompt=prompt_text)

# --- 3. HELPER FUNCTION: PDF READER ---
def read_pdf(uploaded_file):
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg", width=100)
    st.title("CareerForge Agent")
    mode = st.radio("Select Agent Mode:", ["📄 Resume Architect", "🎙️ Interview Coach"])
    
    st.divider()
    
    # Load Skills Taxonomy
    try:
        with open("skills.json", "r") as f:
            skills_db = json.load(f)
        selected_role = st.selectbox("Target Job Role:", list(skills_db.keys()))
    except FileNotFoundError:
        st.error("⚠️ skills.json not found! Please create it.")
        selected_role = "Data Science" # Fallback

# --- 5. MODE 1: RESUME ARCHITECT (THE ANALYST) ---
if mode == "📄 Resume Architect":
    st.title("📄 AI Resume Architect")
    st.markdown(f"**Role Target:** {selected_role}")
    st.info("Upload your resume. I will find your skill gaps and pass them to the Interview Coach.")
    
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
    
    if uploaded_file is not None:
        resume_text = read_pdf(uploaded_file)
        st.success("✅ Resume Scanned Successfully")
        
        target_tech = skills_db[selected_role]["Technical Skills"] if 'skills_db' in locals() else []
        target_concepts = skills_db[selected_role]["Concepts"] if 'skills_db' in locals() else []
        
        col1, col2 = st.columns(2)
        
        # B. GAP ANALYSIS AGENT
        with col1:
            st.subheader("🔍 Skill Gap Analysis")
            if st.button("Analyze My Gaps"):
                with st.spinner("Comparing against industry standards..."):
                    prompt = f"""Role: {selected_role}
                    Required Skills: {', '.join(target_tech)}
                    Required Concepts: {', '.join(target_concepts)}
                    
                    User Resume Content:
                    {resume_text[:3000]}
                    
                    Task: Perform a Gap Analysis.
                    1. Identify missing critical skills.
                    2. Give a Match Score (0-100%).
                    3. List specific topics the user needs to study.
                    
                    Output Format:
                    **Match Score:** [X]%
                    
                    **❌ Missing Skills:**
                    - [Skill 1]
                    - [Skill 2]
                    
                    **💡 Study Recommendation:**
                    [One sentence advice]
                    """
                    analysis = get_granite_response(prompt)
                    st.markdown(analysis)
                    
                    st.session_state['detected_gaps'] = analysis
                    st.session_state['resume_uploaded'] = True
                    st.toast("💾 Gaps saved! The Interview Coach has been updated.")

        # C. RESUME WRITER AGENT (STABLE VERSION)
        with col2:
            st.subheader("✨ Summary Optimizer")
            
            # Initialize session state for summary if not exists
            if "optimized_summary" not in st.session_state:
                st.session_state.optimized_summary = None

            if st.button("Rewrite My Summary"):
                with st.spinner("Drafting professional summary..."):
                    prompt = f"""You are a top-tier Resume Writer.
                    Role: {selected_role}
                    Resume Text: {resume_text[:2000]}
                    
                    Task: Rewrite the user's "Professional Summary" to sound senior, results-oriented, and tailored to {selected_role}. Use action verbs.
                    """
                    suggestion = get_granite_response(prompt)
                    # SAVE TO SESSION STATE (This fixes the disappearing button)
                    st.session_state.optimized_summary = suggestion

            # Display Result if it exists in memory
            if st.session_state.optimized_summary:
                st.success("Suggested Summary:")
                st.write(st.session_state.optimized_summary)
                
                # THE DOWNLOAD BUTTON
                st.download_button(
                    label="📄 Download Optimized Summary (.txt)",
                    data=f"OPTIMIZED PROFESSIONAL SUMMARY\nRole: {selected_role}\n\n{st.session_state.optimized_summary}",
                    file_name="Optimized_Summary.txt",
                    mime="text/plain"
                )

# --- 6. MODE 2: INTELLIGENT INTERVIEW COACH (THE TRAINER) ---
elif mode == "🎙️ Interview Coach":
    st.title(f"🎙️ {selected_role} Interview Coach")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if len(st.session_state.chat_history) == 0:
        if "detected_gaps" in st.session_state:
            st.info("💡 **Adaptive Mode Active:** Focusing on gaps found in your resume.")
            initial_prompt = f"""
            Context: The user is applying for {selected_role}.
            Their Resume Analysis showed these gaps: {st.session_state['detected_gaps']}
            
            Task: Generate a technical interview question specifically targeting ONE of these missing skills to test if they actually know it.
            """
        else:
            st.info("ℹ️ Standard Mode: General technical questions.")
            initial_prompt = f"""
            Task: Generate a challenging introductory technical interview question for a {selected_role} position.
            """
            
        with st.spinner("🤖 Generating question..."):
            first_q = get_granite_response(initial_prompt)
            st.session_state.chat_history.append({"role": "ai", "content": first_q})
            st.rerun()

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    user_input = st.chat_input("Type your answer here...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.spinner("🧠 IBM Granite is grading your answer..."):
            last_question = st.session_state.chat_history[-2]["content"]
            grading_prompt = f"""
            Role: Expert Technical Interviewer.
            Current Question: {last_question}
            User Answer: {user_input}
            
            Task:
            1. Grade the answer (0-10).
            2. Explain the correct answer briefly.
            3. Ask the NEXT technical question (make it harder).
            
            Output Format:
            **Score:** [X]/10
            
            **Feedback:** [Explanation]
            
            **Next Question:** [New Question]
            """
            ai_response = get_granite_response(grading_prompt)
            st.session_state.chat_history.append({"role": "ai", "content": ai_response})
            with st.chat_message("ai"):
                st.markdown(ai_response)
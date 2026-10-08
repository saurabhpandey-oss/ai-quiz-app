import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Interactive Quiz Exam", page_icon="📝", layout="centered")

# Configure Groq API using Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets! Please add GROQ_API_KEY.")

st.title("📝 AI Interactive Exam Dashboard")
st.write("Test your knowledge! Generate exam questions, select your answers, and check your performance.")

# Sidebar controls for Quiz Configuration
st.sidebar.header("⚙️ Quiz Settings")
topic = st.sidebar.text_input("Enter Topic", "SSC CGL English Grammar & Quantitative Aptitude")
difficulty = st.sidebar.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", min_value=3, max_value=15, value=5)

# Initialize Session State
if "quiz_generated" not in st.session_state:
    st.session_state.quiz_generated = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.sidebar.button("Generate New Quiz 🚀"):
    with st.spinner("AI is crafting your exam questions... please wait!"):
        try:
            prompt = f"""
            You are an expert exam question creator for competitive exams like SSC CGL, Banking, and UPSC.
            Create a multiple-choice quiz about {topic} with exactly {num_questions} questions.
            Difficulty Level: {difficulty}
            
            For each question provide:
            - Question Statement
            - 4 Options (A, B, C, D)
            - Correct Answer (clearly state the option letter)
            - Explanation (short concept logic)
            Format it clearly with clean headings.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-120b",
            )
            
            st.session_state.quiz_raw_text = chat_completion.choices[0].message.content
            st.session_state.quiz_generated = True
            st.session_state.submitted = False
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Render Quiz Content
if st.session_state.get("quiz_generated", False):
    st.markdown("---")
    st.subheader(f"🎯 Live Test: {topic} ({difficulty} Level)")
    
    # Display the generated quiz questions
    st.markdown(st.session_state.quiz_raw_text)
    
    st.markdown("---")
    st.info("💡 **Instructions for Test:** Read the questions above carefully, note down your answers on a paper or mentally, and then click the button below to reveal tips or evaluate yourself!")
    
    if st.button("🔄 Reset / Generate Another Test"):
        st.session_state.quiz_generated = False
        st.rerun()

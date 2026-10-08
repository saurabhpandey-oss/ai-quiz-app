import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="AI Quiz App", page_icon="🧠", layout="centered")

# Configure OpenAI API using Streamlit Secrets
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets! Please add OPENAI_API_KEY.")

st.title("🧠 AI-Powered Quiz App")
st.write("Enter your topic, choose the difficulty level, and generate exam-level practice questions using ChatGPT!")

# User inputs
topic = st.text_input("Which topic do you want a quiz on?", "SSC CGL English Grammar & Quantitative Aptitude")

# Quiz Level Selection
difficulty = st.selectbox("Select Quiz Difficulty Level", ["Easy", "Medium", "Hard"])

num_questions = st.slider("How many questions do you want?", min_value=3, max_value=25, value=5)

if st.button("Generate Quiz 🚀"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        with st.spinner(f"Preparing {difficulty} level exam questions with ChatGPT... please wait!"):
            try:
                prompt = f"""
                You are an expert exam question creator for competitive exams like SSC CGL, Banking, and UPSC.
                Create a multiple-choice quiz about {topic} with {num_questions} questions.
                Difficulty Level: {difficulty}
                
                For each question:
                - Match the selected difficulty level ({difficulty}):
                  * Easy: Direct concept checking and basic rules.
                  * Medium: Standard exam level with tricky options.
                  * Hard: Advanced application-based, highly challenging questions.
                - Provide 4 clear options (A, B, C, D).
                - Clearly specify the correct answer at the end of each question.
                - Provide a short, detailed explanation/concept logic for why the answer is correct.
                Format it neatly with bold headings and bullet points.
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                st.success(f"Your {difficulty} level quiz is ready!")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")

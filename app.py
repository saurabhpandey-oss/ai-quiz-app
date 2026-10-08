import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Quiz App", page_icon="🧠", layout="centered")

# Configure Gemini API using Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets! Please add GEMINI_API_KEY.")

st.title("🧠 AI-Powered Quiz App")
st.write("Enter your topic and generate exam-level practice questions!")

# User inputs
topic = st.text_input("Which topic do you want a quiz on?", "SSC CGL English Grammar & Quantitative Aptitude")
num_questions = st.slider("How many questions do you want?", min_value=3, max_value=25, value=5)

if st.button("Generate Quiz 🚀"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("Preparing high-level exam questions... please wait!"):
            try:
                # Call Gemini model (using correct 1.5 flash model)
                model = genai.GenerativeModel("gemini-3.8-flash")
                prompt = f"""
                You are an expert exam question creator for competitive exams like SSC CGL, Banking, and UPSC.
                Create a high-level, challenging multiple-choice quiz about {topic} with {num_questions} questions.
                For each question:
                - Make it standard exam difficulty (not too basic).
                - Provide 4 clear options (A, B, C, D).
                - Clearly specify the correct answer at the end of each question.
                - Provide a short, detailed explanation/concept logic for why the answer is correct.
                Format it neatly with bold headings and bullet points.
                """
                response = model.generate_content(prompt)
                
                st.success("Your exam practice quiz is ready!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

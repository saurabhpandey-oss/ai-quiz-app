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
st.write("Enter your favorite topic and generate an instant quiz using AI!")

# User inputs
topic = st.text_input("Which topic do you want a quiz on?", "Ssc CGL")
num_questions = st.slider("How many questions do you want?", min_value=3, max_value=25, value=5)

if st.button("Generate Quiz 🚀"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        with st.spinner("AI is preparing your quiz... please wait!"):
            try:
                # Call Gemini model
                mmodel = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                Create a multiple-choice quiz about {topic} with {num_questions} questions.
                For each question, provide 4 options (A, B, C, D) and specify the correct answer at the end of each question.
                Keep it clear, engaging, and format it nicely.
                """
                response = model.generate_content(prompt)
                
                st.success("Quiz is ready!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

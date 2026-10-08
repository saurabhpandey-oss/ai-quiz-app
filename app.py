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
st.write("Apne pasand ka topic dalo aur AI se instant quiz generate karo!")

# User inputs
topic = st.text_input("Kis topic par quiz chahiye?", "Python Programming")
num_questions = st.slider("Kitne sawal chahiye?", min_value=3, max_value=10, value=5)

if st.button("Generate Quiz 🚀"):
    if not topic:
        st.warning("Pehle koi topic toh daalo!")
    else:
        with st.spinner("AI quiz taiyar kar raha hai... thoda sabar karo!"):
            try:
                # Call Gemini model
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                Create a multiple-choice quiz about {topic} with {num_questions} questions.
                For each question, provide 4 options (A, B, C, D) and specify the correct answer at the end of each question.
                Keep it clear, engaging, and format it nicely.
                """
                response = model.generate_content(prompt)
                
                st.success("Quiz taiyar hai!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Kuch galti ho gayi: {e}")

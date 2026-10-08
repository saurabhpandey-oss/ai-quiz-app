import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Interactive Exam Portal", page_icon="📝", layout="centered")

# Configure Groq API using Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets! Please add GROQ_API_KEY.")

st.title("📝 AI Interactive Exam Portal")
st.write("Test your knowledge! Select your options below, submit your test, and get your final score with detailed explanations.")

# Sidebar controls for Quiz Configuration
st.sidebar.header("⚙️ Quiz Settings")
topic = st.sidebar.text_input("Enter Topic", "SSC CGL English Grammar & Quantitative Aptitude")
difficulty = st.sidebar.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", min_value=3, max_value=10, value=5)

# Initialize Session State
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.sidebar.button("Generate New Test 🚀"):
    with st.spinner("AI is crafting your exam questions... please wait!"):
        try:
            # Prompt structured to cleanly separate questions, options, answers, and explanations
            prompt = f"""
            You are an expert exam question creator for competitive exams like SSC CGL and UPSC.
            Create a multiple-choice quiz about {topic} with exactly {num_questions} questions.
            Difficulty Level: {difficulty}
            
            You must output the quiz strictly in the following format for each question:
            ---
            QUESTION: [Write the question statement here]
            OPTION_A: [Text for option A]
            OPTION_B: [Text for option B]
            OPTION_C: [Text for option C]
            OPTION_D: [Text for option D]
            CORRECT: [Only write A, B, C, or D]
            EXPLANATION: [Detailed concept logic]
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="openai/gpt-oss-120b",
            )
            
            raw_text = chat_completion.choices[0].message.content
            
            # Parsing the raw text into structured python dictionaries
            questions_list = []
            blocks = raw_text.split("---")
            for block in blocks:
                if "QUESTION:" in block:
                    lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
                    q_dict = {}
                    for line in lines:
                        if line.startswith("QUESTION:"):
                            q_dict["question"] = line.replace("QUESTION:", "").strip()
                        elif line.startswith("OPTION_A:"):
                            q_dict["A"] = line.replace("OPTION_A:", "").strip()
                        elif line.startswith("OPTION_B:"):
                            q_dict["B"] = line.replace("OPTION_B:", "").strip()
                        elif line.startswith("OPTION_C:"):
                            q_dict["C"] = line.replace("OPTION_C:", "").strip()
                        elif line.startswith("OPTION_D:"):
                            q_dict["D"] = line.replace("OPTION_D:", "").strip()
                        elif line.startswith("CORRECT:"):
                            q_dict["correct"] = line.replace("CORRECT:", "").strip().upper()
                        elif line.startswith("EXPLANATION:"):
                            q_dict["explanation"] = line.replace("EXPLANATION:", "").strip()
                    
                    if "question" in q_dict and "correct" in q_dict:
                        questions_list.append(q_dict)
            
            st.session_state.quiz_data = questions_list
            st.session_state.submitted = False
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")

# Render Interactive Test if data exists
if st.session_state.quiz_data:
    st.markdown("---")
    st.subheader(f"🎯 Live Exam: {topic} ({difficulty})")
    
    with st.form("exam_form"):
        user_selections = {}
        
        for idx, q in enumerate(st.session_state.quiz_data, 1):
            st.markdown(f"**Q{idx}: {q.get('question')}**")
            
            opts = [
                f"A) {q.get('A', '')}",
                f"B) {q.get('B', '')}",
                f"C) {q.get('C', '')}",
                f"D) {q.get('D', '')}"
            ]
            
            # Interactive radio selection for student
            choice = st.radio(
                f"Choose option for Q{idx}",
                options=["Select an option"] + opts,
                key=f"q_choice_{idx}"
            )
            
            # Extract selected letter (A, B, C, or D)
            if choice != "Select an option":
                user_selections[idx] = choice[0]
            else:
                user_selections[idx] = None
                
            st.markdown("")
        
        submitted_btn = st.form_submit_button("📊 Submit Test & Calculate Score")
        if submitted_btn:
            st.session_state.submitted = True
            st.session_state.user_selections = user_selections
            st.rerun()

    # Evaluation and Score Display after submission
    if st.session_state.submitted:
        st.markdown("---")
        st.header("🏆 Exam Result & Evaluation")
        
        score = 0
        total = len(st.session_state.quiz_data)
        user_answers = st.session_state.get("user_selections", {})
        
        for idx, q in enumerate(st.session_state.quiz_data, 1):
            correct_opt = q.get("correct", "").strip()
            user_opt = user_answers.get(idx)
            
            st.markdown(f"### Question {idx}: {q.get('question')}")
            st.write(f"Your Answer: **{user_opt if user_opt else 'Not Attempted'}**")
            st.write(f"Correct Answer: **{correct_opt}**")
            
            if user_opt == correct_opt:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error("❌ Incorrect")
                
            st.info(f"💡 **Explanation:** {q.get('explanation')}")
            st.markdown("---")
            
        # Final Score Summary Box
        st.balloons()
        st.metric(label="Your Final Score", value=f"{score} / {total}", delta=f"{((score/total)*100):.1f}% Accuracy")
        
        if st.button("🔄 Take Another Test"):
            st.session_state.quiz_data = None
            st.session_state.submitted = False
            st.rerun()

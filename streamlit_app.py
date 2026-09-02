from app import create_exp, check_answers, exp_diff, save_history, get_history, get_explanation, delete_history, save_feedback
import streamlit as st

st.set_page_config(
    page_title="ExplainIt 🧠",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
    <style>
        .stApp 
        {
            background:
                radial-gradient(circle at 15% 20%, #312E81 0%, transparent 35%),
                radial-gradient(circle at 85% 80%, #4338CA 0%, transparent 30%),
                #0B1026;
        }
            [data-testid="stSidebar"] {
            background-color: #080D20;
            border-right: 1px solid #312E81;
        }
            [data-testid="stSidebar"] button {
            background-color: transparent !important;
            border: none !important;
            text-align: left !important;
        }
            [data-testid="stSidebar"] button:hover{
            background-color: #171A3A !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin: 20px;">
    <h1>ExplainIt 🧠</h1>
    <p>Turn complex concepts into simple, understandable explanations.</p>
    </div>
    """,
    unsafe_allow_html=True
)

new_col1, new_col2, new_col3 = st.columns([1, 1, 1])

with new_col2:
    new_exp = st.button(
        "New Explanation 🪄",
        type="primary",
        width="stretch"
    )

if new_exp:
    st.session_state.pop("explanation", None)
    st.session_state.concept = ""
    st.rerun()

with st.sidebar:
    st.header("📚 History")

    history = get_history()

    if not history:
        st.info("No history yet. Generate an explanation to see it here!")

    for item in history:
        col1, col2 = st.columns([5, 1])

        with col1:
            if st.button(
                f"{item[1]} — {item[2].title()}",
                key=f"open_{item[0]}"
            ):
                selected = get_explanation(item[0])

                if selected:
                    st.session_state.explanation = selected[0]
                    st.session_state.history_id = item[0]
                    st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{item[0]}"):
                delete_history(item[0])

                if st.session_state.get("history_id") == item[0]:
                    st.session_state.pop("explanation", None)
                    st.session_state.pop("history_id", None)

                st.success("Deleted from history!")
                st.rerun()

with st.container(border=True, key="input_card"):
    st.subheader("Get learning!")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        concept = st.text_input(
            label="Concept:",
            placeholder="Search...",
            key="concept"
        )

    with col2:
        difficulty = st.selectbox(
            label="Difficulty:",
            options=["Beginner", "Student", "Advanced"],
            help="Choose how detailed you want the explanation to be."
        )

st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])

with col1:
    st.write("")

with col2:
    exp_button = st.button(
        "Explain concept",
        type="primary",
        width="stretch"
    )

with col3:
    st.write("")

with col4:
    regenerate = st.button(
        "🔄 Regenerate",
        type="primary",
        width="stretch"
    )

with col5:
    st.write("")

if regenerate and "explanation" not in st.session_state:
    st.warning("Generate an explanation first!")

if exp_button or (regenerate and "explanation" in st.session_state):

    if concept.strip() == "":
        st.warning("Please enter a concept first!")

    else:
        st.session_state.pop("explanation", None)

        with st.spinner("Thinking..."):
            explanation = create_exp(concept, difficulty.lower())

            if explanation == "ERROR_429":
                st.error("⚠️ We've reached the AI request limit. Please try again later.")

            elif explanation == "ERROR_GENERIC":
                st.error("⚠️ An error occurred while generating the explanation. Please try again later.")

            else:
                st.session_state.explanation = explanation

                if exp_button:
                    st.session_state.history_id = save_history(concept, difficulty.lower(), explanation)

if "explanation" in st.session_state:

    explanation = st.session_state.explanation

    parts = explanation.split("🌍 Real-world analogy:")

    if len(parts) < 2:
        st.error("Sorry, I couldn't format the explanation properly.")
        st.stop()

    parts2 = parts[1].split("💻 Example:")

    if len(parts2) < 2:
        st.error("Sorry, I couldn't format the explanation properly.")
        st.stop()

    parts3 = parts2[1].split("⚠️ Common mistakes:")

    if len(parts3) < 2:
        st.error("Sorry, I couldn't format the explanation properly.")
        st.stop()

    parts4 = parts3[1].split("📝 Practice questions:")

    if len(parts4) < 2:
        st.error("Sorry, I couldn't format the explanation properly.")
        st.stop()

    with st.expander("📘 Explanation", expanded=True):
        st.write(parts[0].replace("📘 Explanation:", ""))

    with st.expander("🌍 Real-world analogy:", expanded=True):
        st.write(parts2[0])

    with st.expander("💻 Example:", expanded=True):
        st.write(parts3[0])

    with st.expander("⚠️ Common mistakes:", expanded=True):
        st.write(parts4[0])

    st.write("Was this explanation helpful?")

    feedback = st.feedback("thumbs")

    feedback_key = f"feedback_{st.session_state.history_id}:{explanation}"

    if feedback is not None and st.session_state.get("feedback_key") != feedback_key:
        if feedback == 1:
            save_feedback(st.session_state.history_id, "👍🏻")
        else:
            save_feedback(st.session_state.history_id, "👎🏻")

        st.session_state.feedback_key = feedback_key

    exp_style = st.selectbox(
        "Explain differently:",
        options=[
            "Simpler",
            "Step-by-step",
            "Different analogy",
            "More technical"
                ]
            )

    different = st.button("💡 Explain differently")

    if different:
        with st.spinner("Thinking..."):
            new_exp = exp_diff(
                concept,
                difficulty.lower(),
                exp_style
            )

            if new_exp == "ERROR_429":
                st.error("⚠️ We've reached the AI request limit. Please try again later.")

            elif new_exp == "ERROR_GENERIC":
                st.error("⚠️ An error occurred while generating the explanation. Please try again later.")

            else:
                st.session_state.explanation = new_exp
                st.rerun()

    questions = [
        q.strip()
        for q in parts4[1].split("\n")
        if q.strip()
    ]

    with st.expander("📝 Practice questions:", expanded=True):

        answers = {}

        for question in questions:
            st.write(question)

            answer = st.text_input(
                "Your answer:",
                key=question
            )

            answers[question] = answer

        check = st.button("Check Answers")

        if check:

            if any(answer.strip() == "" for answer in answers.values()):
                st.warning("Please answer all the questions!")

            else:
                result = check_answers(
                    concept,
                    questions,
                    answers
                )
                if result == "ERROR_429":
                    st.error("⚠️ We've reached the AI request limit. Please try again later.")

                elif result == "ERROR_GENERIC":
                    st.error("⚠️ An error occurred while checking the answers. Please try again later.")

                else:  
                    st.write(result)
import random
import streamlit as st
from openai import OpenAI

# ============================================================
# V-STUDY AI
# Personal AI Study Assistant
# Created by Vishav
# ============================================================

st.set_page_config(
    page_title="V-Study AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# ============================================================
# THEMES
# ============================================================

THEMES = {
    "Pink Pastel": {
        "background": "#fff1f5",
        "sidebar": "#ffe3ec",
        "primary": "#ec4899",
        "secondary": "#f9a8d4",
        "card": "#ffffff",
        "text": "#1f1720",
    },
    "Sky Blue": {
        "background": "#eff8ff",
        "sidebar": "#dff1ff",
        "primary": "#2563eb",
        "secondary": "#93c5fd",
        "card": "#ffffff",
        "text": "#172033",
    },
    "Lavender": {
        "background": "#f5f3ff",
        "sidebar": "#ebe5ff",
        "primary": "#7c3aed",
        "secondary": "#c4b5fd",
        "card": "#ffffff",
        "text": "#211735",
    },
    "Doraemon": {
        "background": "#eef8ff",
        "sidebar": "#d8f0ff",
        "primary": "#1689e8",
        "secondary": "#67c4ff",
        "card": "#ffffff",
        "text": "#10243a",
    },
}


# ============================================================
# TOOLS
# ============================================================

TOOLS = [
    "AI Doubt Solver",
    "Notes Generator",
    "Summary Maker",
    "Timetable Builder",
    "Motivation Booster",
    "Flashcards",
    "Brain-Dump Cleaner",
    "Answer Checker",
    "AI Planner",
    "Mindset Reset",
    "Study Routine Designer",
    "Exam Strategy Maker",
    "Personal Study Coach",
]


# ============================================================
# TOOL PROMPTS
# ============================================================

TOOL_INSTRUCTIONS = {

    "AI Doubt Solver": """
You are solving a student's academic doubt.

Explain the answer clearly and step-by-step.
Start with the direct answer.
Then explain the reasoning.
Give a simple example when useful.
Finish with a short exam tip if appropriate.
""",

    "Notes Generator": """
Create clean, exam-oriented study notes.

Use:
- Clear headings
- Important definitions
- Key points
- Examples
- Formulas where relevant
- Exam tips

Do not make unnecessary filler.
""",

    "Summary Maker": """
Summarize the student's material.

Keep the important information.
Remove repetition.
Use short headings and bullet points.
Make it easy to revise before an exam.
""",

    "Timetable Builder": """
Create a realistic study timetable.

Consider:
- Available study time
- Subjects
- Breaks
- Difficult subjects
- Revision
- Practice questions

Avoid unrealistic schedules.
""",

    "Motivation Booster": """
Give the student a short motivational boost.

Be encouraging but realistic.
Do not use empty motivational clichés.
Give them one practical action they can take immediately.
""",

    "Flashcards": """
Create useful active-recall flashcards.

Format each card as:

Card 1
Q:
A:

Keep questions concise and answers accurate.
""",

    "Brain-Dump Cleaner": """
Organize the student's messy thoughts into a clear action plan.

Separate:
1. Urgent
2. Important
3. Later

Then provide the recommended order of action.
""",

    "Answer Checker": """
Check the student's answer academically.

Provide:
- What is correct
- What is missing
- What is incorrect
- How to improve it
- A better model answer when useful

Do not be unnecessarily harsh.
""",

    "AI Planner": """
Create a practical study plan.

Break the goal into manageable tasks.
Include priorities, revision and practice.
Avoid overloading a single day.
""",

    "Mindset Reset": """
Give a short study mindset reset.

Help the student stop overthinking and focus on the next small action.
Keep it calm, practical and encouraging.
""",

    "Study Routine Designer": """
Design a realistic daily study routine.

Include:
- Start routine
- Study blocks
- Short breaks
- Difficult subjects
- Revision
- End-of-day review
""",

    "Exam Strategy Maker": """
Create a high-impact exam strategy.

Include:
- What to study first
- Revision method
- Practice strategy
- Time management
- Common mistakes to avoid
- Exam-day strategy
""",

    "Personal Study Coach": """
Act as a supportive academic coach.

Understand the student's problem.
Give practical advice.
Avoid unrealistic productivity advice.
End with a simple next step.
""",
}


# ============================================================
# EXAMPLES
# ============================================================

EXAMPLES = {

    "AI Doubt Solver":
        "Explain opportunity cost with a simple Class 12 example.",

    "Notes Generator":
        "Make exam notes for Class 12 Business Studies: Principles of Management.",

    "Summary Maker":
        "Summarize Human Capital Formation in India for Class 12 Economics.",

    "Timetable Builder":
        "I have 5 hours today and need to study Accounts, Business Studies and Economics.",

    "Flashcards":
        "Create 10 flashcards for Class 12 Economics: Money and Banking.",

    "Brain-Dump Cleaner":
        "I have homework, revision, a test and a project. Help me organize everything.",

    "Answer Checker":
        "Student answer: Opportunity cost is the cost of choosing one thing over another.\n\nCorrect answer: Opportunity cost is the value of the next best alternative foregone when a choice is made.",

    "AI Planner":
        "Create a 30-day Class 12 exam preparation plan.",

    "Mindset Reset":
        "I am procrastinating and need to start studying.",

    "Study Routine Designer":
        "I can study 4 hours every weekday.",

    "Exam Strategy Maker":
        "Create a strategy for my Class 12 Economics exam.",

    "Personal Study Coach":
        "I keep procrastinating and get distracted while studying.",
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">
            <div style="font-size:42px;">🎓</div>
            <h2 style="margin:0;">V-Study AI</h2>
            <p style="opacity:.7;">
                Learn smarter.<br>
                Study better.<br>
                Achieve more.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    theme_name = st.selectbox(
        "🌈 Choose Theme",
        list(THEMES.keys()),
    )

    st.session_state.dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode,
    )

    st.divider()

    tool = st.radio(
        "✨ Choose a Tool",
        TOOLS,
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True,
    ):
        st.session_state.chat_history = []
        st.rerun()

    st.caption("V-Study AI • Created by Vishav")


# ============================================================
# SELECT THEME
# ============================================================

theme = THEMES[theme_name]

if st.session_state.dark_mode:

    background = "#080b14"
    sidebar_background = "#0d1220"
    card_background = "#111827"
    text_color = "#f8fafc"
    muted_text = "#94a3b8"

else:

    background = theme["background"]
    sidebar_background = theme["sidebar"]
    card_background = theme["card"]
    text_color = theme["text"]
    muted_text = "#64748b"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap'
    );

    .stApp {{
        background: {background};
        color: {text_color};
    }}

    section[data-testid="stSidebar"] {{
        background: {sidebar_background};
    }}

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    .hero {{
        padding: 30px;
        border-radius: 28px;
        margin-bottom: 25px;

        background:
            linear-gradient(
                135deg,
                {theme["primary"]}22,
                {theme["secondary"]}22
            );

        border:
            1px solid
            {theme["primary"]}44;

        box-shadow:
            0 15px 40px rgba(0,0,0,.06);
    }}

    .hero-title {{
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }}

    .hero-subtitle {{
        color: {muted_text};
        font-size: 17px;
        margin-top: 8px;
    }}

    .tool-card {{
        padding: 20px;
        border-radius: 22px;
        background: {card_background};
        border:
            1px solid
            {theme["primary"]}22;

        margin: 12px 0;

        box-shadow:
            0 8px 30px rgba(0,0,0,.04);
    }}

    .ai-response {{
        padding: 24px;
        border-radius: 20px;

        background: {card_background};

        border-left:
            5px solid
            {theme["primary"]};

        box-shadow:
            0 10px 30px rgba(0,0,0,.06);

        line-height: 1.75;

        white-space: pre-wrap;
    }}

    .history-card {{
        padding: 18px;
        border-radius: 16px;

        background:
            {theme["primary"]}10;

        border:
            1px solid
            {theme["primary"]}22;

        margin-bottom: 12px;
    }}

    div.stButton > button {{
        border-radius: 14px;
        font-weight: 600;
    }}

    textarea {{
        border-radius: 16px !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OPENAI CLIENT
# ============================================================

try:
    api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    api_key = None

client = None

if api_key:
    try:
        client = OpenAI(api_key=api_key)
    except Exception:
        client = None


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(user_prompt, selected_tool):

    if not client:
        return (
            "⚠️ **OpenAI API key not configured.**\n\n"
            "Add your key to Streamlit Secrets as:\n\n"
            "`OPENAI_API_KEY = \"your-key\"`\n\n"
            "Then restart the app."
        )

    instruction = TOOL_INSTRUCTIONS.get(
        selected_tool,
        "Help the student clearly and accurately.",
    )

    system_prompt = f"""
You are V-Study AI, an AI study assistant created by Vishav.

You help students learn, revise, understand difficult concepts,
prepare for exams and organize their studies.

Your personality:
- Friendly
- Clear
- Encouraging
- Accurate
- Student-friendly

Do not unnecessarily make answers long.

Selected tool:
{selected_tool}

Tool instructions:
{instruction}

Always prioritize understanding over simply giving an answer.
"""

    try:
        # Standard OpenAI Chat Completion request
        response = client.chat.completions.create(
            model="gpt-5-mini",  # Switched to gpt-5-mini per request (use gpt-4o-mini if fallback needed)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.65
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "I couldn't generate an answer. Please try again."

        st.session_state.chat_history.append(
            {
                "tool": selected_tool,
                "you": user_prompt,
                "ai": answer,
            }
        )

        return answer

    except Exception as error:
        return (
            "❌ **Something went wrong.**\n\n"
            f"`{error}`\n\n"
            "Please check your API key, model access and internet connection."
        )


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">

        <div style="font-size:18px;">
            ✨ Your personal AI study partner
        </div>

        <div class="hero-title">
            V-Study AI
        </div>

        <div class="hero-subtitle">
            Learn smarter. Study better. Achieve more. 🚀
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TOOL HEADER
# ============================================================

st.markdown(
    f"""
    <div class="tool-card">

        <h2 style="margin:0;">
            ✨ {tool}
        </h2>

        <p style="color:{muted_text};">
            Use V-Study AI to make your study session easier.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MOTIVATION BOOSTER
# ============================================================

if tool == "Motivation Booster":

    quotes = [
        "You don't need perfect motivation. Start with the next 20 minutes. 🔥",
        "Small progress is still progress. Keep moving. ✨",
        "Future-you will be glad you started today. 📚",
        "Focus on the next task, not the entire mountain. 🧠",
        "Consistency beats waiting for the perfect mood. 🚀",
    ]

    if st.button(
        "🔥 Give Me a Boost",
        type="primary",
        use_container_width=True,
    ):
        quote = random.choice(quotes)

        st.markdown(
            f"""
            <div class="ai-response">
                {quote}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ALL OTHER TOOLS
# ============================================================

else:

    prompt = st.text_area(
        "💬 What do you want V-Study AI to help with?",
        placeholder=EXAMPLES.get(
            tool,
            "Ask your study question..."
        ),
        height=200,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        generate = st.button(
            "✨ Generate with V-Study AI",
            type="primary",
            use_container_width=True,
        )

    with col2:
        example_button = st.button(
            "💡 Example",
            use_container_width=True,
        )

    if example_button:
        st.info(
            EXAMPLES.get(
                tool,
                "Explain this topic simply."
            )
        )

    if generate:
        if not prompt.strip():
            st.warning(
                "Please enter a question or topic first."
            )
        else:
            with st.spinner(
                "🤖 V-Study AI is thinking..."
            ):
                answer = ask_ai(
                    prompt.strip(),
                    tool,
                )

            st.markdown("### 🤖 V-Study AI")
            st.markdown(
                f"""
                <div class="ai-response">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# CHAT HISTORY
# ============================================================

if st.session_state.chat_history:
    st.divider()
    st.markdown("### 📜 Previous Responses")
    
    for item in reversed(st.session_state.chat_history):
        st.markdown(
            f"""
            <div class="history-card">
                <strong>🛠️ Tool:</strong> {item['tool']}<br>
                <strong>💬 Question:</strong> {item['you']}<br><br>
                <strong>🤖 Answer:</strong><br>{item['ai']}
            </div>
            """,
            unsafe_allow_html=True,
        )

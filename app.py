import json
import random
import time
from datetime import datetime

import requests
import streamlit as st

st.set_page_config(
    page_title="TouchGrass AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --ink: #101311;
    --paper: #f5f2e9;
    --card: #fffdf7;
    --green: #174b3a;
    --mint: #dcebdc;
    --yellow: #f5c84c;
    --coral: #ed776b;
    --line: #171b18;
}

html, body, [class*="css"] {
    font-family: "Space Grotesk", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(245,200,76,.16), transparent 28%),
        radial-gradient(circle at 100% 15%, rgba(23,75,58,.12), transparent 25%),
        var(--paper);
    color: var(--ink);
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    border: 2px solid var(--line);
    border-radius: 24px;
    padding: 2.2rem 2.4rem;
    background: var(--green);
    color: white;
    box-shadow: 9px 9px 0 var(--line);
    margin-bottom: 2rem;
}

.hero-kicker {
    font-family: "DM Mono", monospace;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--yellow);
    font-size: .82rem;
    font-weight: 500;
}

.hero h1 {
    font-size: clamp(3rem, 7vw, 6.5rem);
    line-height: .88;
    margin: .45rem 0 1rem;
    letter-spacing: -.065em;
}

.hero p {
    max-width: 720px;
    font-size: 1.18rem;
    line-height: 1.55;
    color: #f1f5ee;
}

.card {
    background: var(--card);
    border: 2px solid var(--line);
    border-radius: 18px;
    padding: 1.35rem;
    box-shadow: 5px 5px 0 var(--line);
    margin-bottom: 1rem;
}

.mission {
    background: #dcebdc;
    border: 2px solid var(--line);
    border-radius: 22px;
    padding: 2rem;
    box-shadow: 7px 7px 0 var(--line);
}

.mission .emoji {
    font-size: 3rem;
}

.mission h2 {
    font-size: 2.3rem;
    margin: .2rem 0 .7rem;
    letter-spacing: -.035em;
}

.mono {
    font-family: "DM Mono", monospace;
}

.badge {
    display: inline-block;
    padding: .35rem .65rem;
    border: 1.5px solid var(--line);
    border-radius: 999px;
    margin: .15rem .25rem .15rem 0;
    font-family: "DM Mono", monospace;
    font-size: .75rem;
    background: white;
}

.quote {
    font-size: 1.25rem;
    font-weight: 600;
    line-height: 1.45;
    padding: 1rem 1.1rem;
    border-left: 5px solid var(--coral);
    background: #fff;
    border-radius: 8px;
}

div[data-testid="stButton"] > button {
    border: 2px solid var(--line);
    border-radius: 10px;
    box-shadow: 4px 4px 0 var(--line);
    font-weight: 700;
    min-height: 2.8rem;
}

div[data-testid="stButton"] > button:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0 var(--line);
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border: 2px solid var(--line);
    border-radius: 10px;
    background: #fffdf7;
}

section[data-testid="stSidebar"] {
    background: #ebe7da;
    border-right: 2px solid var(--line);
}

.small {
    color: #4f574f;
    font-size: .9rem;
}

.footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 2px solid var(--line);
    font-family: "DM Mono", monospace;
    font-size: .78rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
ACTIVITIES = {
    "🌿 Nature": [
        ("Texture Hunter", "Find 3 different natural textures around you: rough bark, smooth stone, soft grass, etc."),
        ("Tiny World", "Spend 10 minutes looking for the smallest interesting thing you can find outdoors."),
        ("Tree Check-In", "Find a tree and observe its bark, leaves, sounds and the life around it."),
    ],
    "🚶 Walking": [
        ("No-Route Walk", "Take a 15-minute walk without following your usual route. Turn at the next interesting corner."),
        ("Slow Walk", "Walk for 10 minutes at half your normal pace. Notice five things you would normally miss."),
        ("Landmark Loop", "Pick a visible landmark and walk toward it using streets you rarely take."),
    ],
    "📸 Photography": [
        ("Three Shapes", "Take three photos of interesting shapes you notice outside."),
        ("One Color", "Choose one color and find five examples of it in the world around you."),
        ("Light Hunt", "Find three places where sunlight and shadow create an interesting pattern."),
    ],
    "🐦 Sounds": [
        ("Sound Map", "Sit outside for 8 minutes and identify five different sounds without looking for their sources."),
        ("Bird Break", "Spend 10 minutes listening for birds. Count distinct calls, not birds."),
        ("Quietest Spot", "Walk until you find the quietest safe place nearby, then stay there for five minutes."),
    ],
    "🏃 Movement": [
        ("Micro Adventure", "Walk briskly for 5 minutes, stretch for 5, then explore for another 10."),
        ("Outdoor Circuit", "Do 3 rounds of walking, squats and gentle stretches in a safe outdoor space."),
        ("Energy Reset", "Take a 15-minute brisk walk. Every five minutes, change your pace slightly."),
    ],
    "👨‍👩‍👧 Social": [
        ("Scavenger Hunt", "With someone else, find five things on a simple outdoor scavenger list."),
        ("Teach Me", "Go outside with a friend and each point out one thing the other person has never noticed."),
        ("Question Walk", "Take a walk and ask each other three unusual questions."),
    ],
}

MOODS = ["Bored", "Stressed", "Tired", "Curious", "Energetic", "Creative", "Need a reset"]
GOALS = ["Relax", "Explore", "Move my body", "Make something", "Notice nature", "Spend time with someone"]
TIMES = [5, 10, 15, 20, 30, 45, 60]

FALLBACK_TIPS = {
    "Stressed": "Keep the mission low-pressure. The point is noticing, not achieving.",
    "Tired": "Choose gentle movement and let curiosity do the work.",
    "Energetic": "Use the time for movement and a small challenge.",
    "Bored": "Choose novelty: a new route, object, sound or place.",
    "Curious": "Slow down and investigate something you normally ignore.",
    "Creative": "Collect patterns, colors, shapes or sounds for inspiration.",
    "Need a reset": "Make the first five minutes screen-free and deliberately slow.",
}

def make_fallback(activity, minutes, mood, goal, environment, company):
    pool = ACTIVITIES.get(activity, sum(ACTIVITIES.values(), []))
    options = pool if isinstance(pool, list) else list(pool)
    title, description = random.choice(options)

    # Add contextual instructions without pretending the model generated them.
    context_bits = []
    if environment:
        context_bits.append(f"Try it around {environment.lower()}.")
    if company == "With someone":
        context_bits.append("Invite your companion to participate instead of documenting everything.")
    elif company == "Alone":
        context_bits.append("Leave notifications off while you're outside.")
    context_bits.append(FALLBACK_TIPS.get(mood, "Keep it simple and stay present."))

    return {
        "title": title,
        "description": description,
        "steps": [
            f"Set aside {minutes} minutes.",
            "Read the mission once.",
            "Put your phone away and start.",
            *context_bits,
        ],
        "difficulty": "Easy" if minutes <= 20 else "Medium",
        "why": f"You're feeling {mood.lower()} and want to {goal.lower()}. This is designed to create a small real-world reset.",
        "safety": "Choose a familiar, public or otherwise safe place. Follow local rules and stay aware of traffic and your surroundings.",
        "source": "Built-in recommender",
    }

def call_ollama(prompt, model, base_url):
    url = base_url.rstrip("/") + "/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.8},
    }
    response = requests.post(url, json=payload, timeout=45)
    response.raise_for_status()
    raw = response.json().get("response", "")
    data = json.loads(raw)
    return data

def make_ai_recommendation(profile, model, base_url):
    prompt = f"""
You are TouchGrass AI, an outdoor activity recommendation engine.
Your purpose is to get the user OFF the screen quickly.
Recommend one safe, realistic, offline activity. Do not recommend using an app,
scrolling, gaming, watching content, or staying online.

User profile:
- available minutes: {profile['minutes']}
- mood: {profile['mood']}
- goal: {profile['goal']}
- activity preference: {profile['activity']}
- environment: {profile['environment']}
- company: {profile['company']}

Return ONLY valid JSON with this exact structure:
{{
  "title": "short memorable mission title",
  "description": "2-3 sentence outdoor mission",
  "steps": ["step 1", "step 2", "step 3"],
  "difficulty": "Easy|Medium|Challenging",
  "why": "one sentence explaining why this matches the profile",
  "safety": "one short safety reminder"
}}

The activity must fit the available time. Make it achievable with ordinary surroundings
and no special equipment.
"""
    data = call_ollama(prompt, model, base_url)
    data["source"] = f"Open-weight model via Ollama ({model})"
    return data

# ---------- State ----------
defaults = {
    "recommendation": None,
    "started_at": None,
    "completed": False,
    "reflection": "",
    "history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌱 TouchGrass")
    st.caption("An AI recommendation engine whose goal is to get you away from the screen.")
    st.divider()

    st.markdown("### Your situation")
    minutes = st.select_slider("I have", options=TIMES, value=20, format_func=lambda x: f"{x} min")
    mood = st.selectbox("Right now I feel", MOODS, index=0)
    goal = st.selectbox("I want to", GOALS, index=0)
    activity = st.selectbox("I'd enjoy", list(ACTIVITIES.keys()), index=0)
    environment = st.selectbox(
        "I'm around",
        ["Neighborhood", "Park", "Garden", "Campus", "City", "Beach / lakeside", "Other"],
    )
    company = st.radio("Company", ["Alone", "With someone"], horizontal=True)

    st.divider()
    st.markdown("### 🧠 AI mode")
    use_ai = st.toggle("Use local open-source AI", value=False)
    model = st.text_input("Ollama model", value="gemma3:4b")
    base_url = st.text_input("Ollama URL", value="http://localhost:11434")
    if use_ai:
        st.caption("Requires Ollama running locally with the selected model.")
    else:
        st.caption("Built-in recommender works without an AI server.")

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="hero-kicker">Hacktoberfest 2026 · Touch Grass</div>
  <h1>Touch<br>Grass.</h1>
  <p>
    Tell us how you feel, how much time you have, and what sounds good.
    We'll recommend one small thing worth doing in the real world.
  </p>
</div>
""", unsafe_allow_html=True)

# ---------- Main ----------
left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown("### 🎯 Your mission generator")
    st.markdown(
        f'<div class="card"><span class="badge">{minutes} minutes</span>'
        f'<span class="badge">{mood}</span><span class="badge">{goal}</span>'
        f'<span class="badge">{activity}</span><span class="badge">{company}</span></div>',
        unsafe_allow_html=True,
    )

    generate = st.button("🌱 Recommend something for me", use_container_width=True, type="primary")

    if generate:
        profile = {
            "minutes": minutes,
            "mood": mood,
            "goal": goal,
            "activity": activity,
            "environment": environment,
            "company": company,
        }
        with st.spinner("Thinking of something worth leaving the screen for..."):
            try:
                if use_ai:
                    rec = make_ai_recommendation(profile, model, base_url)
                else:
                    rec = make_fallback(activity, minutes, mood, goal, environment, company)
            except Exception as exc:
                rec = make_fallback(activity, minutes, mood, goal, environment, company)
                rec["source"] = "Built-in recommender (AI server unavailable)"
                st.warning(f"Local AI could not be reached, so we used the built-in recommender. Details: {exc}")

        st.session_state.recommendation = rec
        st.session_state.started_at = None
        st.session_state.completed = False
        st.session_state.reflection = ""

    rec = st.session_state.recommendation
    if rec:
        st.markdown(f"""
        <div class="mission">
          <div class="emoji">🌱</div>
          <div class="mono">YOUR RECOMMENDED MISSION</div>
          <h2>{rec.get("title", "Your outdoor mission")}</h2>
          <p style="font-size:1.18rem;line-height:1.6;">{rec.get("description","")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Your plan")
        for step in rec.get("steps", []):
            st.markdown(f"- {step}")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Difficulty:** {rec.get('difficulty', 'Easy')}")
        with c2:
            st.markdown(f"**Generated by:** {rec.get('source', 'TouchGrass')}")

        st.markdown("#### Why this one?")
        st.markdown(f'<div class="quote">{rec.get("why","")}</div>', unsafe_allow_html=True)

        st.info("🛡️ " + rec.get("safety", "Stay aware of your surroundings and choose a safe location."))

        if st.button("🚪 I'm heading outside", use_container_width=True):
            st.session_state.started_at = time.time()
            st.rerun()

        if st.session_state.started_at:
            elapsed = int(time.time() - st.session_state.started_at)
            remaining = max(0, minutes * 60 - elapsed)
            mm, ss = divmod(remaining, 60)
            st.markdown(f"## ⏱️ {mm:02d}:{ss:02d}")
            if remaining > 0:
                st.caption("Put your phone away. This page will still be here when you get back.")
            else:
                st.success("🎉 Mission time is up. Nice work getting outside!")

            if st.button("✅ I completed my mission", use_container_width=True):
                st.session_state.completed = True
                st.session_state.history.append({
                    "title": rec.get("title"),
                    "completed_at": datetime.now().isoformat(timespec="minutes"),
                    "minutes": minutes,
                })
                st.rerun()

        if st.session_state.completed:
            st.markdown("### 🌿 Welcome back")
            st.text_area(
                "Optional: what did you notice?",
                key="reflection",
                placeholder="A sound, a thought, something funny, something beautiful...",
            )
            st.success("Mission completed. The best AI interaction is the one that got you outside.")

with right:
    st.markdown("### Why this is different")
    st.markdown("""
    <div class="card">
      <h3>🤖 AI that wants less of your attention</h3>
      <p>
      Most AI products try to keep the conversation going.
      TouchGrass does the opposite: it gives you one useful recommendation
      and gets out of the way.
      </p>
    </div>
    <div class="card">
      <h3>🔓 Open by design</h3>
      <p>
      The recommendation can be generated by an open-weight model running
      locally through Ollama. You can swap models, change prompts and keep
      requests on your machine.
      </p>
    </div>
    <div class="card">
      <h3>📵 The product goal</h3>
      <p class="quote">The successful session ends with the user putting the phone down.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("### 🏆 Your tiny wins")
        st.metric("Missions completed", len(st.session_state.history))
        total = sum(x["minutes"] for x in st.session_state.history)
        st.metric("Minutes outside", total)

st.markdown("""
<div class="footer">
TOUCHGRASS AI · OPEN-SOURCE AI CHALLENGE · BUILT TO SEND YOU OUTSIDE
</div>
""", unsafe_allow_html=True)

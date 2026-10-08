# 🌱 TouchGrass AI

> An AI recommendation engine whose goal is to get you away from the screen.

Built for the **Hacktoberfest 2026 Open-Source AI Challenge — Week 1: Touch Grass**.

## What it does

TouchGrass asks:

- How much time do you have?
- How are you feeling?
- What do you want to do?
- What kind of activity sounds good?
- Are you alone or with someone?

It then recommends one small, achievable outdoor mission.

The app supports two modes:

1. **Built-in recommender** — works immediately with no AI server.
2. **Local open-source AI** — uses an open-weight model through Ollama.

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Open the URL shown by Streamlit.

## Optional: local open-source AI

Install Ollama from the official Ollama website, then pull an open-weight model.

Example:

```bash
ollama pull gemma3:4b
```

Start Ollama if it is not already running, then enable **Use local open-source AI** in the sidebar.

The app calls:

```text
http://localhost:11434/api/generate
```

You can change the model and URL in the sidebar.

## Architecture

```text
User profile
    |
    v
Recommendation engine
    |
    +--> Built-in recommender
    |
    +--> Ollama --> Open-weight model
    |
    v
Outdoor mission
    |
    v
Phone down -> Go outside
```

## Why open innovation matters

The AI layer is intentionally replaceable.

A user can:

- run an open-weight model locally
- change the model
- change the prompt
- avoid a proprietary AI API
- experiment without per-request AI API costs

The application also remains usable without a model server.

## Deployment

The built-in mode can be deployed to any environment that supports Streamlit.

For a hosted deployment, local Ollama is not normally available on the same machine unless you separately provide an accessible model server. For a simple public demo, keep the built-in recommender enabled; for the strongest open-source AI demonstration, show the local Ollama mode in a short screen recording.

## Project structure

```text
touchgrass_ai/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

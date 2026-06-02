from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from chat import run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)


@st.cache_resource
def load_runtime(provider_name: str, model_name: str) -> dict[str, Any]:
    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    return {
        "provider": make_provider(provider_name),
        "model": model_name,
        "system_prompt": system_prompt,
        "tools": to_openai_tools(declarations),
    }


st.set_page_config(page_title="Research Agent", page_icon="RA", layout="wide")
st.title("Research Agent")

with st.sidebar:
    provider_name = st.selectbox("Provider", ["openai"], index=0)
    model_name = st.text_input("Model", value="gpt-4o-mini")
    max_tool_rounds = st.slider("Tool rounds", 1, 6, 4)
    history_window = st.slider("History", 1, 8, 5)
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []

runtime = load_runtime(provider_name, model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        if item.get("tool_calls"):
            with st.expander("Tool calls", expanded=False):
                st.json(item["tool_calls"])

prompt = st.chat_input("Ask a research question")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
        {"role": "system", "content": runtime["system_prompt"]},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": prompt},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Running"):
            result = run_model_tool_loop(
                provider=runtime["provider"],
                messages=messages,
                tools=runtime["tools"],
                model=runtime["model"],
                max_tool_rounds=max_tool_rounds,
            )
        assistant_text = result.get("assistant_text", "")
        st.markdown(assistant_text)
        tool_calls = [
            {"round": round_item["round"], "tool_calls": round_item["tool_calls"]}
            for round_item in result.get("rounds", [])
            if round_item.get("tool_calls")
        ]
        if tool_calls:
            with st.expander("Tool calls", expanded=False):
                st.json(tool_calls)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text,
        "tool_calls": tool_calls,
    })
    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": assistant_text})

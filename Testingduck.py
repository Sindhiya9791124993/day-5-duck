import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

# 🚫 Disable warnings or verbose logs
import logging
logging.getLogger("langchain").setLevel(logging.ERROR)

# 🧠 Hardcoded Gemini API Key (⚠️ Not for production)
GOOGLE_API_KEY = "AIzaSyBXuTQi4jJF7hF_m0RH4EQaa3Pw6DE-HUU"

# ✨ Title and UI
st.set_page_config(page_title="🧠 Real-Time Q&A Assistant", page_icon="🔍")
st.title("🧠 Ask Me Anything - Powered by Gemini + DuckDuckGo")
st.markdown("Type your question about current events or facts and get real-time answers using **Gemini + DuckDuckGo** 🔎")

# 🧠 Gemini Model Setup
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

# 🔍 DuckDuckGo Tool Setup
search_tool = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="DuckDuckGo Search",
        func=search_tool.run,
        description="Useful for answering questions about current events or recent information"
    )
]

# 🤖 Agent Setup with ZERO_SHOT_REACT_DESCRIPTION
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# 💬 Input Area
user_input = st.text_input("💡 Enter your question here:")
submit = st.button("🚀 Ask")

# 🎯 Handle Submit
if submit:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a question.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                response = agent.run(user_input)
            st.success("✅ Answer:")
            st.write(response)
        except Exception as e:
            st.error(f"❌ Oops! Something went wrong: {str(e)}")

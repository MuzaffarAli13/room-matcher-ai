from agents import Agent,Runner,OpenAIChatCompletionsModel,set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio
from main_agent_instruction import main_agent_instructions,room_finder_agent_instructions
import streamlit as st
from red_flag import get_red_flags_only
from score import get_match_data_with_score
from get_rooms import get_room_matches

load_dotenv()
set_tracing_disabled(True)

API = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

external_client = AsyncOpenAI(
    api_key=API,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client
)

# Match Score Agent
match_score_agent = Agent(
    name="Match Scorer Agent",
    instructions="Compares user preferences with profiles.json data and calculates a match score.Returns the top 3 best matching profiles with their scores.",
    model=model
)
room_hunter_agent = Agent(
    name="Room Finder Agent",
    instructions=room_finder_agent_instructions,
    model=model,
    tools=[get_room_matches],
   handoff_description = """
   If the task is to find a room, this is my responsibility. 
   I have been delegated only for this task: to search and return available rooms 
   based on user preferences. I do not handle roommate matching or any other queries.
   """
)
profile_Reader = Agent(
    name="Profile Reader",
    instructions=main_agent_instructions,
    model=model,
    tools=[get_match_data_with_score,get_red_flags_only],
    handoffs=[room_hunter_agent]
)



prompt = st.text_area("📝 Enter Prompt:")

if "history" not in st.session_state:
    st.session_state.history = []


if st.button("Chat"):
    with st.spinner("Thinking..."):
        st.session_state.history.append({"role": "user", "content": prompt})

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            Runner.run(
                starting_agent=profile_Reader,
                input=st.session_state.history
            )
        )

        prompt = ""
        st.session_state.history.append({"role": "assistant", "content": result.final_output})

        st.success("Reply from Complaint Assistant:")
        st.write(result.final_output)
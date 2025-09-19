import os
from typing import Optional, Union

import streamlit as st
from dotenv import load_dotenv

# --- Agno imports
from agno.agent import Agent
from agno.team import Team
from agno.models.groq import Groq
from agno.tools import Toolkit, tool

# (Optional) if you want to do direct DDG calls inside the wrapper
from agno.tools.duckduckgo import DuckDuckGoTools


# ==============================
# 1) ENV & PAGE CONFIG
# ==============================
load_dotenv()
st.set_page_config(
    page_title="Travel Itinerary Generator",
    page_icon="🧭",
    layout="centered",
)
st.title("🧭 Travel Itinerary Generator")
st.caption("Powered by Agno + Groq + DuckDuckGo")
st.caption("Made by Piyush")

# ==============================
# 2) SAFE TOOLKIT WRAPPER
#    Fixes: max_results must be an int (not a string)
# ==============================
class SafeDuckDuckGo(Toolkit):
    """
    A minimal wrapper that coerces max_results to int so Groq's
    strict tool schema validation won't 400 on \"5\" (string).
    """

    @tool
    def search(self, query: str, max_results: Optional[Union[int, str]] = 5):
        """Search the web with DuckDuckGo and return a list of results."""
        mr = int(max_results) if max_results is not None else 5
        with DuckDuckGoTools() as ddgs:
            # Return simplified results (title + href + body)
            return list(ddgs.text(query, max_results=mr))


# ==============================
# 3) CACHED OBJECTS
# ==============================
@st.cache_resource(show_spinner=False)
def get_safe_ddg() -> SafeDuckDuckGo:
    return SafeDuckDuckGo()


@st.cache_resource(show_spinner=False)
def get_team(use_search: bool) -> Team:
    """
    Build the Agno team. Toggle whether tools are attached, so you can
    test the planner w/ or w/o web search.
    """
    tools = [get_safe_ddg()] if use_search else []

    itinerary_planner = Agent(
        name="Itinerary Planner",
        model=Groq(id="llama-3.3-70b-versatile", temperature=0.0),
        tools=tools,
        role="Create a detailed, day-wise itinerary for a given destination, budget, and duration.",
        instructions=[
            "You are an itinerary planner agent.",
            "Produce a detailed **day-wise** itinerary with places to visit, activities, and food to try.",
            "Be explicit about budget allocation and cost-saving tips.",
            "Prefer structured markdown with headings and bullet points.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )

    travel_search_agent = Agent(
        name="Travel Search",
        model=Groq(id="llama-3.3-70b-versatile", temperature=0.0),
        tools=tools,
        role="Search the web for travel information and summarize concisely.",
        instructions=[
            "Use the DuckDuckGo tool to gather **current** highlights for the given country or city.",
            "Return famous cities/areas, notable attractions, activities, and food items.",
            "Keep outputs concise and actionable for itinerary planning.",
            # IMPORTANT: the tool wrapper already handles string/number, but we can hint:
            "If you pass max_results to the tool, pass it as a number (e.g., 5).",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )

    advisor = Team(
        name="Travel Advisor",
        determine_input_for_members=True,
        model=Groq(id="llama-3.3-70b-versatile", temperature=0.0),
        members=[itinerary_planner, travel_search_agent],
        role=(
            "A team that first gathers destination ideas and highlights, "
            "then generates a detailed day-wise itinerary."
        ),
        instructions=[
            "First, use the Travel Search agent to suggest cities/places and must-do items "
            "for the provided country/context.",
            "Then, use the Itinerary Planner to create a **day-wise** plan using the selected place, "
            "budget, and duration.",
            "Return the final answer as a clean markdown document.",
        ],
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        share_member_interactions=True,
        markdown=True,
    )
    return advisor


# ==============================
# 4) SIDEBAR (Settings)
# ==============================
with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input(
        "GROQ_API_KEY",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="You can also set this in your .env file.",
    )
    use_search = st.toggle("Use web search (DuckDuckGo)", value=True)
    max_results = st.number_input("Max web results", min_value=1, max_value=25, value=5, step=1)

# Put API key into env for Agno/Groq client
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key


# ==============================
# 5) FORM (Inputs)
# ==============================
with st.form("trip_form"):
    st.subheader("Tell us about your trip")
    country = st.text_input("Country (or City if you already know)", placeholder="Italy")
    budget = st.text_input("Budget (e.g., 2000 USD, ₹1,50,000)", placeholder="2000 USD")
    days = st.number_input("Number of days", min_value=1, max_value=30, value=5, step=1)
    interests = st.text_area(
        "Interests (optional)",
        placeholder="History, food, art, nightlife, beaches, hiking…",
        height=80,
    )
    submitted = st.form_submit_button("Generate Itinerary", use_container_width=True)

# ==============================
# 6) RUN
# ==============================
if submitted:
    if not groq_api_key:
        st.error("Please provide your GROQ_API_KEY in the sidebar.")
    elif not country:
        st.error("Please enter a country or city.")
    else:
        st.toast("Planning your trip…", icon="🧭")
        advisor = get_team(use_search=use_search)

        # Build a natural prompt
        user_prompt = (
            f"I want to travel to {country} with a budget of {budget} for {days} days."
            + (f" My interests are: {interests.strip()}." if interests.strip() else "")
            + (
                f" If you search the web, keep results to about {int(max_results)} items per query."
                if use_search
                else " Do not use web results."
            )
        )

        try:
            # Run the team.
            result = advisor.run(user_prompt)

            # Main answer
            st.markdown("### ✨ Suggested Itinerary")
                        # Try to get the clean text content
            if hasattr(result, "content"):
                st.markdown(result.content, unsafe_allow_html=True)
            else:
                st.markdown(str(result))
            # Agno returns a markdown-friendly object/string

            # Optional: show internal steps / member interactions
            

        except Exception as e:
            st.error("Something went wrong while generating your itinerary.")
            with st.expander("Error details"):
                st.exception(e)

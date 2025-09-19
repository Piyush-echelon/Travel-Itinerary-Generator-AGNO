from dotenv import load_dotenv
import os
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
from agno.tools import Toolkit, tool
from typing import Union, Optional



load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


class fixedDDG(Toolkit):
    @tool
    def search(self, query: str):
        with DuckDuckGoTools() as ddg:
            return list(ddg.search(query=query, max_results=5))
    
global_model = Groq(id="qwen/qwen3-32b", temperature=0.0)   


itinerary_planner = Agent(
    name = "Itinerary Planner",
    model = global_model,
    tools = [DuckDuckGoTools()],
    role = "An agent that creates a detailed day-wise itinerary for a city from a given city, budget, and number of days.",
    instructions = [
        "you are an itinerary planner agent, you have to create a detailed day-wise itinerary for a given city/place, budget, and number of days.",
        "the itinerary should include places to visit, activities to do, and food to try.",
        "make sure to create a detailed day-wise itinerary.",
        "make sure to include the budget in the itinerary.",    
    ],
    markdown = True,
    add_datetime_to_context=True,
)  


travel_search_agent = Agent(
    name = "simple_search_agent",
    model = global_model,
    tools = [fixedDDG()],
    role = "An agent that searches the web for a given query related to a location and provides a concise answer.",
    instructions = [
        "first use the DuckDuckGoTools tool to gather information about the famous cities in the provided country and fetch famous places to visit, activities to do, and food to try.",
        "you should return the city/place name which is famous in the provided country.",    
    ],
    markdown = True,
    add_datetime_to_context=True,
)  

Advisor = Team(
    name = 'Travel Advisor',
    determine_input_for_members=True,
    model = global_model,
    members = [itinerary_planner, travel_search_agent],
    role = "A team of agents that work together to gather information and create a detailed day-wise itinerary for a city from a given country, budget, and number of days.",
    instructions = [
        "you are a team of agents that work together to gather information and create a detailed day-wise itinerary for a city from a given country, budget, and number of days.",
        "You should first use travel_search_agent to gather information about famous places/cities for the provided Country, budget and the number of days for itinerary planning.",
        "Then you should use itinerary_planner agent to generate itinerary and you should pass the City/Place name, budget and duration to the agent.",
    ],
    add_datetime_to_context=True,
    add_history_to_context= True,
    num_history_runs = 10,
    share_member_interactions = True,
    markdown = True,
)


# Store user inputs in session state

print("Welcome to the Travel Itinerary Generator!, Please provide the following details: Country name, budget, and number of days for itinerary planning.")

location = input("Enter a location for a travel-related query: ")
budget = input("Enter your budget (in USD or INR): ")
days = input("Enter the number of days for the itinerary: ")
info = f"Country name: {location}, Budget: {budget}, Number of days: {days}"
Advisor.print_response(info)



from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools
from tools.flight_search_tools import FlightSearchTools
from tools.activities_tools import ActivitiesSearchTools

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
"""
Creating Agent Cheat Sheet:
- Think like a boss. work backwords from the goal and think which employee you need
to hire to get the job done.
- Define captain of the crew who orient the other agents towords the 
  goals.
- Define which experts the captain needs to communicate with and delegate tasks to.
   Build a top down structure of the crew.

   Goal:
   - Create a 7 day travel itinerary with detailed per day plans,
     including budget, packing suggestions and safety tips.
   
   
   
   Key Steps for Task Creation
   1. Identify Desired outcome: define what success looks like for your project.
        - A detailed 7 day travel itinerary
    2. Task Breakdown: Divide the goal into smaller, manageable tasks that agents can execute.  
        - Itinerary Planning: develop a detailed plan for each day of the trip.
        - City selection: analyze and pick the best cities to visit.
        - Local Tour Guide: Find a local expert to provide insights and recommendations.
   3. Assign Tasks to Agents: Match tasks with agents based on their roles and responsibilities. 
   4. Task Description template:
      - Use this template as a guide to define each tasks in your CrewAI application.
      - This template helps ensure that each task is crearly defined, actionable and aligned with the specific goals of the project.
       
   Captain/Manager/Boss:
   - Expert travel agent
   
   Employee/Experts to hire:
   - City selection expert
   - Local Tour Guide
   
   Notes:
   - agents should be results driven and have a clear goals in mind
   - Role is their job title
   - Goals should actionable
   - Backstory should be their resume


   GPT-4 for production
   GPT-3 for development
"""
class TripPlanningAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=1)

    def travel_agent(self):
        return Agent(
            role="Expert travel agent",
            backstory=dedent(f"""Expert in searching, analyzing and selecting the most convenient flights for travelers."""),
            goal=dedent(f""" To find the most convenient flight for travelers"""),
            # tools=[tool_1, tool_2],
            verbose=True,
            llm=self.OpenAIGPT35,
            tools=[
                CalculatorTools.calculate,
                FlightSearchTools.search_flight_offers
            ],
            allow_delegation = False
            
        )
    def local_guide_agent(self):
        return Agent(
            role="Local Guide ",
            backstory=dedent(f"""Expert in recommending personalized activities"""),
            goal=dedent(f"""Recommend personalized activities based on traveler's interests, budget and duration of stay"""),
            verbose=True,
            llm=self.OpenAIGPT4,
            tools=[
                CalculatorTools.calculate,
                ActivitiesSearchTools.search_activities,
            ],
            allow_delegation = False
        )
    def trip_planner_agent(self):
        return Agent(
            role="Trip Planner",
            backstory=dedent(f"""Expert in trip planning."""),
            goal=dedent(f"""Develop a comprehensive trip guide"""),
            # tools=[tool_1, tool_2],
            llm=self.OpenAIGPT4,
            tools=[
                CalculatorTools.calculate,
            ],
            allow_delegation = False
        )
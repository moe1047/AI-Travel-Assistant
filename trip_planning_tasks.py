from crewai import Task
from textwrap import dedent
from tools.airport_code_finder import AirportFinder
from geopy.geocoders import Nominatim
# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
"""
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
      - This template helps ensure that each task is clearly defined, actionable and aligned with the specific goals of the project.    
"""
class TripPlanningTasks:
    def find_flight(self, agent, origin, destination, departure_date, return_date):
        finder = AirportFinder()
        #origin_code = finder.find_airport_code(origin)
        #destination_code = finder.find_airport_code(destination)
        return Task(
            description=dedent(
                f"""
                    You are an expert travel agent,
                    search for flights offers, compare itineraries and choose one that has the lowest price and the lowest duration. 
                    
                    your answer should be the full information of the flight offer itinerary you chose.

                    Here are the traveler’s details

                    Origin: Assign The airport code for {origin}
                    Destination: Assign The airport code for {destination}
                    Departure date: {departure_date}
                    Return date: {return_date}
                """
            ),
            agent=agent,
            expected_output	= """ A full information of the flight offer that was chosen for the traveler"""
        )
    def recommend_activities(self, agent, duration, interests, destination, budget):
        """
        geolocator = Nominatim(user_agent="city_coordinates_finder")
        location = geolocator.geocode(destination)
        latitude = location.latitude
        longitude = location.longitude
        """
        return Task(
            description=dedent(
                f"""
                    As a local expert guide and activities planner, your task is to create a curated list of activities that meet the following criteria:
                    1. The activities should match the traveler's interests.
                    2. The recommended activities should fill up the traveler's available time, 
                        Assuming The traveler allocates 6 hours per day to activities. 
                        For example, if the stay is 6 days, the traveler has 36 hours in total for activities, 
                        make sure you fill up the 36 available hours with activities.
                        
                    3. The total cost of the activities should fit within the traveler's budget.

                    your answer should consist of list of recommended activities, and the chosen flight offer information.
                    with each activity containing the following information:
                    - activity title
                    - activity description
                    - activity duration
                    - activity price.
                    - activity booking link.
                    and total cost of activities.

                    Here are what you need to know to search for activities
                    latitude:  Assign The latitude (decimal coordinates) for {destination} 
                    longitude: Assign The longitude (decimal coordinates) for {destination}

                    Here are the Traveler's information:
                    Traveler's Interests: {interests}.
                    Traveler's Budget: {budget} minus the chosen flight offer price.
                    Traveler's Duration of Stay: {duration} days.
                """
            ),
            agent=agent,
            expected_output	= 
                        """
                        list of recommended activities and the chosen flight offer information.
                        """
        )
    def plan_trip(self, agent, destination, duration):
        return Task(
            description=dedent(
                f"""
                    Compile a comprehensive trip guide for a trip to {destination}. 
                    The guide should include:
                    
                    - A short concise information about the destination such as: 
                        attractions, accommodations, weather, transportation options and local customs.
                    - Chosen flight offer information
                    - Detailed Itinerary:
                        A Day-by-day breakdown of {duration}-day travel itinerary with detailed per day plans with timestamps.   
                        This itinerary should cover all aspects of the trip, from arrival to departure
                        Integrating all the recommended activities with practical travel logistics.

                        Note: Allocate 6 hours per day to activities.

                        your answer must be a be a complete expanded travel plan, formatted as markdown, encompassing a daily schedule.  
                    - Detailed trip budget: Include the flight offer cost, break down of the recommended activities costs and total trip cost.
                    - Travel tips and advice: Offer practical advice specific to the destination.
                """
            ),
            agent=agent,
            expected_output	= 
                    """
                    - A short concise information about the destination.
                    - Flight information.
                    - Detailed itinerary
                    - Trip budget
                    - Travel tips and advice
                    """
        )
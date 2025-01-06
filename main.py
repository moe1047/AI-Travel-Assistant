from crewai import Crew, Process
from trip_planning_agents import TripPlanningAgents
from trip_planning_tasks import TripPlanningTasks
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

class TripCrew:
    def __init__(self, origin, destination, departure_date, return_date, interests, budget):
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.interests = interests
        self.budget = budget
        #Calculate duration
        #Convert the string dates to datetime objects
        departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
        return_date = datetime.strptime(return_date, "%Y-%m-%d")
        
        #Calculate the difference between the two dates
        duration = (return_date - departure_date).days + 1
        self.duration = duration


    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TripPlanningAgents()
        tasks = TripPlanningTasks()

        # Define your custom agents and tasks here
        travel_agent = agents.travel_agent()
        local_guide_agent = agents.local_guide_agent()
        trip_planner_agent = agents.trip_planner_agent()

        # Custom tasks include agent name and variables as input
        find_flight_task = tasks.find_flight(
            travel_agent,
            self.origin,
            self.destination,
            self.departure_date,
            self.return_date,
        )
        recommend_activities_task = tasks.recommend_activities(
            local_guide_agent,
            self.duration,
            self.interests,
            self.destination,
            self.budget
        )
        
        plan_trip_task = tasks.plan_trip(trip_planner_agent,self.destination,self.duration)

        # Define your custom crew here
        '''
        crew = Crew(
            agents=[local_guide_agent],
            tasks=[recommend_activities_task],
            verbose=True,
            cache = False
        )
        '''
        crew = Crew(
            agents=[travel_agent, local_guide_agent, trip_planner_agent],
            tasks=[find_flight_task,recommend_activities_task, plan_trip_task ],
            verbose=True,
            process=Process.sequential,
            
        )
        
        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Your Virtual Trip Planner Agent")
    print("-------------------------------")

    origin = "Sydney"
    destination = "Bangkok"
    departure_date = "2024-05-28"
    return_date = "2024-06-03"
    interests = "hiking, Food, Skydiving, Wildlife, Biking, Wellness, cooking, adventure and fun"
    budget = "1200 USD"

    plan_trip_crew = TripCrew(origin, destination, departure_date, return_date, interests, budget)
    result = plan_trip_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)

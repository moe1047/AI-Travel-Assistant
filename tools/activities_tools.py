from langchain.tools import tool
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class ActivitiesSearchTools():

    def request_token():
        # Define the URL
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        
        # Define Headers
        headers = {
        'content-type': 'application/x-www-form-urlencoded'}
        
        # Define the parameters
        params = {
            'grant_type': 'client_credentials',
            'client_id': os.environ['AMADEUS_API_KEY'],
            'client_secret': os.environ['AMADEUS_API_SECRET'],
        }

        # Send the POST request with form-urlencoded data
        response = requests.post(url, headers=headers, data=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the access_token from response
            return(response.json()["access_token"])
        else:
            # Print an error message if the request was unsuccessful
            return(f"Error: {response.status_code}")
    
    def extract_activities_data(json_data):
        #Load the JSON data
        data = json_data
        #data = ActivitiesSearchTools.json

        # Extract flight data
        activities_data = []
        for activity in data["data"]:
            if activity.get("description"):
                #print()
                activity_info = {
                    "id": activity["id"],
                    "name": activity["name"],
                    "description": activity["description"],
                    "minimumDuration": activity["minimumDuration"],
                    "bookingLink": activity["bookingLink"],
                    
                    "price": activity["price"],
                }
                activities_data.append(activity_info)
        return activities_data
    
    @tool("Search for activities for travelers")
    def search_activities(latitude,longitude):
        """
        Useful to search for Tours and Activities with ease for a given traveler interests and budget
        """
        mock=True
        # if mock is true, use gist hosted json. This is for testing purposes
        if mock:
            url = "https://gist.githubusercontent.com/moe1047/f875bdd646796f233a328e4cb690d13d/raw/143f0f48702748a9dc757040726494c64deea5f7/activities.json"
            response = requests.get(
                url,
                timeout=10,
                )
        else:
            # Define the URL
            url = "https://test.api.amadeus.com/v1/shopping/activities"
        
            # Get token
            token = ActivitiesSearchTools.request_token()

            # Define Headers
            headers = {"Authorization": f'Bearer {token}'}
        
            # Define the parameters
            params = {
                'latitude': latitude,
                'longitude': longitude,
                
            }

            # Send the GET request with form-urlencoded data
            response = requests.get(url, headers=headers, params=params)
            
        # extract important flight data from the long json response
        response = response.json()
        #print(response)
        activities_data = ActivitiesSearchTools.extract_activities_data(response)

        return activities_data
        



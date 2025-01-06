from langchain.tools import tool
import os
import requests

class FlightSearchTools():

    def __request_token():
        # Define the URL
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        
        # Define Headers
        headers = {
        'content-type': 'application/x-www-form-urlencoded'
        }
        
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
    
    def __extract_flight_data(json_data):
        # Load the JSON data
        #data = json.loads(json_data)
        data = json_data

        # Extract flight data
        flight_data = []
        for flight in data["data"]:
            flight_info = {
                "id": flight["id"],
                "type": flight["type"],
                "itineraries": [],
                "price": flight["price"]["total"],
                "currency": flight["price"]["currency"]
            }
            for itinerary in flight["itineraries"]:
                flight_info["itineraries"].append({"duration": itinerary["duration"]})
            flight_data.append(flight_info)
        return flight_data
    
    @tool("Search for flight offers")
    def search_flight_offers(origin, destination, departure_date, return_date):   
        """Useful to search for flight Offers and find the most convenient one. 
        
        example param for this function:
        {
            "origin":"SYD",
            "destination":"BKK",
            "departure_date":"2025-04-28",
            "return_date":"2025-05-07",
        }
        """
        #params = json.loads(payload)
        mock=False
        # if mock is true, use gist hosted json. This is for testing purposes
        if mock:
            url = "https://gist.githubusercontent.com/moe1047/e400ab3f7dd6422f97ca1ecbf414bce8/raw/27b9f536c66e8ceed3a4a98d37fe287bf2ed40d4/flight-offers.json"
            response = requests.get(
                url,
                timeout=10,
                )
        else:
            # Define the URL
            url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        
            # Get token
            token = FlightSearchTools.__request_token()

            # Define Headers
            headers = {"Authorization": f'Bearer {token}'}
            # Define the parameters
            request_params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'returnDate': return_date,
                'adults': 1,
                'max': 4,
                'currencyCode': "USD",
            }
            """
            params = {
                'originLocationCode': 'SYD',
                'destinationLocationCode': "BKK",
                'departureDate': "2024-04-25",
                'returnDate': "2024-04-30",
                'adults': 1,
                'max': 4,
                'currencyCode': "USD",
            }
            """
            # Send the GET request with form-urlencoded data
            response = requests.get(url, headers=headers, params=request_params)
            
        # extract important flight data from the long json response
        response = response.json()
        #flight_data = FlightSearchTools.__extract_flight_data(response)
        return response

"""
if __name__ == "__main__":
    # Create an instance of the FlightSearchTools class
    flight_search = FlightSearchTools()

    # Call the request_token method on the instance
    flight_search_response = flight_search.search_flight_offers("SYD","BKK","2024-04-28","2024-05-07")
    
    print("########################\n")
    print("## Here is the result:")
    print(flight_search_response)
"""

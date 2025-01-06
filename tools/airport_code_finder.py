import json

class AirportFinder:
    def __init__(self):
        self.filename = 'city_airport_pairs.json'
        self.airports = self.load_airports()

    def load_airports(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: The file '{}' was not found.".format(self.filename))
            return {}

    def find_airport_code(self, city):
        city = city.title()
        return self.airports.get(city, "Airport code not found for the given city.")

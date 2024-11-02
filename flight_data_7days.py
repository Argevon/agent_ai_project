import requests
import pandas as pd
import json
from datetime import datetime, timedelta

# Kiwi API key
API_KEY = 'api key here'

# Polish airports (IATA codes)
polish_airports = ['WAW', 'KRK', 'GDN', 'KTW', 'POZ', 'WRO', 'SZZ', 'RZE']

# Path to the CSV file (with city names)
csv_file_path = 'C:/Users/Kamil_Laskowski/Downloads/dane inzynieria/europe_top_100_cities_with_countries.csv'

# Read the CSV file into a pandas DataFrame
cities_df = pd.read_csv(csv_file_path)

# Get today's date and a date 7 days into the future
today = datetime.now().strftime('%d/%m/%Y')  # Format: DD/MM/YYYY
future_date = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')


# Function to get the IATA code for a destination city
def get_iata_code(city_name):
    url = "https://tequila-api.kiwi.com/locations/query"

    params = {
        'term': city_name,
        'location_types': 'city',  # Search by city name
        'limit': 1  # We only need one result
    }

    headers = {
        'apikey': API_KEY
    }

    # Make the request to the Kiwi API for location lookup
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['locations']:
            iata_code = data['locations'][0]['code']  # Extract IATA code from response
            city_full_name = data['locations'][0]['name']  # Get the full city name from the response
            print(f"City: {city_full_name}, IATA Code: {iata_code}")
            return iata_code
        else:
            print(f"No IATA code found for {city_name}")
            return None
    else:
        print(f"Error fetching IATA code for {city_name}: {response.status_code}")
        return None


# Function to search flights from Polish airports to a destination city
def search_flights(departure_airport, destination_code):
    url = "https://tequila-api.kiwi.com/v2/search"

    # Define parameters for the API request
    params = {
        'fly_from': departure_airport,  # Departure airport
        'fly_to': destination_code,  # Destination airport IATA code
        'date_from': today,  # Today's date
        'date_to': future_date,  # 7 days into the future
        'limit': 3,  # Limit results to 3 flights
        'partner_market': 'pl',  # Market (Poland)
        'curr': 'PLN',  # Currency in PLN
        'sort': 'price',  # Sort by price
    }

    headers = {
        'apikey': API_KEY
    }

    # Make the request to the Kiwi API
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching flights from {departure_airport} to {destination_code}: {response.status_code}")
        return None


# Function to retrieve flight data for all destinations
def get_flight_data():
    results = {}

    # Iterate through each airport in Poland
    for airport in polish_airports:
        results[airport] = {}

        # Iterate through each city in the CSV
        for index, row in cities_df.iterrows():
            city = row['City']  # Only the City column exists in the CSV

            print(f"Fetching IATA code for {city}...")
            destination_code = get_iata_code(city)  # Get IATA code

            if destination_code:
                print(f"Fetching flights from {airport} to {destination_code}...")
                flight_data = search_flights(airport, destination_code)
                if flight_data:
                    results[airport][city] = flight_data

    return results


# Save the results to a JSON file
def save_flight_data(data, filename='kiwi_flights_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Main execution
if __name__ == "__main__":
    flight_results = get_flight_data()
    save_flight_data(flight_results)
    print("Flight data saved successfully!")

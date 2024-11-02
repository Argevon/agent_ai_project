import requests
import pandas as pd
from fpdf import FPDF
import urllib.parse

# Google Places API key
google_api_key = 'put api key here'


# Function to fetch city descriptions from Wikipedia API
def get_city_description(city_name):
    wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(city_name)
    response = requests.get(wiki_url)
    if response.status_code == 200:
        data = response.json()
        return data.get('extract', 'Description not available')
    else:
        return 'Description not available'


# Function to fetch top places for a given city
def get_top_places(city_name, lat, lon, place_type):
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lon}",
        'radius': 10000,
        'type': place_type,
        'key': google_api_key,
        'rankby': 'prominence'
    }
    response = requests.get(places_url, params=params)
    if response.status_code == 200:
        places_data = response.json().get('results', [])
        place_details = []
        for place in places_data[:10]:  # Limit to top 10 results
            details = get_place_details(place['place_id'])
            place_details.append({
                'Name': place.get('name', 'N/A'),
                'Rating': place.get('rating', 'N/A'),
                'Address': place.get('vicinity', 'N/A'),
                'Description': details.get('description', 'Description not available')
            })
        return place_details
    else:
        print(f"Failed to fetch {place_type} data for {city_name}: {response.status_code}")
        return []


# Function to fetch place details using Google Places Details API
def get_place_details(place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'editorial_summary,rating',
        'key': google_api_key
    }
    response = requests.get(details_url, params=params)
    if response.status_code == 200:
        data = response.json().get('result', {})
        return {
            'description': data.get('editorial_summary', {}).get('overview', 'Description not available'),
            'rating': data.get('rating', 'N/A')
        }
    else:
        return {'description': 'Description not available'}


# Initialize the PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Top Attractions and Restaurants per City", 0, 1, "C")
        self.ln(5)

    def city_section(self, city, city_desc, places, restaurants):
        # City and description
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"City: {city}", 0, 1)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, f"Description: {city_desc.encode('latin-1', 'replace').decode('latin-1')}")
        self.ln(5)

        # Add places table
        try:
            self.cell(0, 10, "Top 10 Tourist Attractions", 0, 1, "L")
            self.cell(50, 10, "Name", 1)
            self.cell(20, 10, "Rating", 1)
            self.cell(70, 10, "Address", 1)
            self.cell(50, 10, "Description", 1)
            self.ln()
            for place in places:
                try:
                    self.cell(50, 10, place['Name'][:25].encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.cell(20, 10, str(place['Rating']).encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.cell(70, 10, place['Address'][:35].encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.multi_cell(50, 10, place['Description'][:90].encode('latin-1', 'replace').decode('latin-1'),
                                    1)  # Changed to multi_cell
                    self.ln()  # Add a new line after the description
                except UnicodeEncodeError as e:
                    print(f"Encoding error in attractions table for {place['Name']}: {e}")
            self.ln(5)
        except UnicodeEncodeError as e:
            print(f"Encoding error in attractions section for {city}: {e}")

        # Similar changes for restaurants table
        try:
            self.cell(0, 10, "Top 10 Restaurants", 0, 1, "L")
            self.cell(50, 10, "Name", 1)
            self.cell(20, 10, "Rating", 1)
            self.cell(70, 10, "Address", 1)
            self.cell(50, 10, "Description", 1)
            self.ln()
            for restaurant in restaurants:
                try:
                    self.cell(50, 10, restaurant['Name'][:25].encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.cell(20, 10, str(restaurant['Rating']).encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.cell(70, 10, restaurant['Address'][:35].encode('latin-1', 'replace').decode('latin-1'), 1)
                    self.multi_cell(50, 10,
                                    restaurant['Description'][:90].encode('latin-1', 'replace').decode('latin-1'),
                                    1)  # Changed to multi_cell
                    self.ln()  # Add a new line after the description
                except UnicodeEncodeError as e:
                    print(f"Encoding error in restaurants table for {restaurant['Name']}: {e}")
            self.ln(10)
        except UnicodeEncodeError as e:
            print(f"Encoding error in restaurants section for {city}: {e}")


# Load city data from CSV
file_path = 'C:/Users/Kamil_Laskowski/Downloads/dane inzynieria/europe_top_100_cities_with_countries.csv'  # Replace with your file path
city_data = pd.read_csv(file_path)

# Create PDF and populate with data
pdf = PDF()
pdf.add_page()

for index, row in city_data.iterrows():
    city = row['City']
    lat = row['Latitude']
    lon = row['Longitude']

    # Get descriptions and places/restaurants
    city_description = get_city_description(city)
    attractions = get_top_places(city, lat, lon, 'tourist_attraction')
    restaurants = get_top_places(city, lat, lon, 'restaurant')

    # Add city section to PDF
    pdf.city_section(city, city_description, attractions, restaurants)

# Save PDF file
output_file_path = 'top_places_restaurants_per_city.pdf'
pdf.output(output_file_path)

print(f"PDF saved to {output_file_path}")
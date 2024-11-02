import csv
import requests
from fpdf import FPDF
import time

API_KEY = "api key here"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Wczytywanie miast z pliku CSV
csv_file_path = 'C:/Users/Kamil_Laskowski/Downloads/dane inzynieria/europe_top_100_cities_with_countries.csv'
pdf_file_path = 'C:/Users/Kamil_Laskowski/Downloads/dane inzynieria/weather_forecast_report.pdf'


def get_weather_data(lat, lon):
    """Funkcja pobierająca dane pogodowe dla określonej lokalizacji"""
    url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdza, czy kod statusu to 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for lat: {lat}, lon: {lon}: {http_err} - {response.text}")
    except Exception as err:
        print(f"Other error occurred for lat: {lat}, lon: {lon}: {err}")
    return None


def extract_forecast_info(weather_data, city_name):
    """Funkcja wyciągająca i formatująca prognozę z danych pogodowych"""
    forecast_dict = {}
    if 'list' in weather_data:
        for forecast in weather_data['list']:
            dt_txt = forecast['dt_txt']  # Data w formacie tekstowym
            hour = dt_txt.split(" ")[1]  # Wyciągamy godzinę

            if hour in ["09:00:00", "15:00:00", "21:00:00"]:
                date = dt_txt.split(" ")[0]  # Data
                feels_like = forecast['main']['feels_like']  # Odczuwalna temperatura
                wind_speed = forecast['wind']['speed']  # Prędkość wiatru
                weather_description = forecast['weather'][0]['description']  # Opis pogody

                # Formatujemy prognozę
                if date not in forecast_dict:
                    forecast_dict[date] = []

                period = "Morning" if hour == "09:00:00" else "Afternoon" if hour == "15:00:00" else "Evening"
                formatted_forecast = (
                    f"{period}: Date: {date} - Feels like: {feels_like}°C, "
                    f"Wind speed: {wind_speed} m/s, Overall forecast: {weather_description.capitalize()}"
                )
                forecast_dict[date].append(formatted_forecast)

    return forecast_dict


def save_forecast_to_pdf(forecasts, city_name):
    """Zapisuje prognozy pogody dla danego miasta do pliku PDF"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f"Weather Forecast Report for {city_name}", ln=True, align='C')

    pdf.set_font('Arial', '', 12)

    # Dodawanie prognozy do PDF
    for date, forecast_list in forecasts.items():
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Weather for {date}", ln=True)  # Nagłówek dla daty
        pdf.set_font('Arial', '', 12)

        for forecast in forecast_list:
            pdf.multi_cell(0, 10, forecast)

    return pdf


def process_cities(csv_file, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row["City"]
            lat = row["Latitude"]
            lon = row["Longitude"]
            print(f"\nFetching weather data for {city} ({lat}, {lon})...")

            # Pobieranie danych pogodowych
            weather_data = get_weather_data(lat, lon)

            if weather_data:
                # Wyciąganie prognozy
                forecast_dict = extract_forecast_info(weather_data, city)

                # Dodawanie prognozy do pliku PDF
                pdf.add_page()
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(200, 10, f"Weather Forecast Report for {city}", ln=True, align='C')

                pdf.set_font('Arial', '', 12)
                for date, forecast_list in forecast_dict.items():
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(0, 10, f"Weather for {date}", ln=True)  # Nagłówek dla daty
                    pdf.set_font('Arial', '', 12)
                    for forecast in forecast_list:
                        pdf.multi_cell(0, 10, forecast)

                print(f"Weather forecast for {city} saved to PDF.")

            time.sleep(2)  # Opóźnienie 2 sekundy między wywołaniami API

    # Zapisanie do pliku PDF
    pdf.output(output_pdf)


# Uruchamianie skryptu
process_cities(csv_file_path, pdf_file_path)
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Funkcja do wczytania danych z pliku JSON
def load_flights_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Funkcja do przetwarzania danych o lotach
def extract_flight_info(data, airports):
    flights_by_airport = {airport: [] for airport in airports}

    # Iteracja przez loty
    for city, destinations in data.items():
        for destination, details in destinations.items():
            for flight in details['data']:
                if flight['flyFrom'] in airports:
                    flight_info = {
                        'flight_id': flight['id'],
                        'fly_from': flight['flyFrom'],
                        'fly_to': flight['flyTo'],
                        'city_from': flight['cityFrom'],
                        'city_to': flight['cityTo'],
                        'local_departure': flight['local_departure'],
                        'local_arrival': flight['local_arrival'],
                        'price': flight['price'],
                        'currency': details['currency'],
                        'airlines': flight['airlines'],
                        'booking_link': flight['deep_link']
                    }
                    flights_by_airport[flight['flyFrom']].append(flight_info)

    return flights_by_airport


# Funkcja do generowania PDF z informacjami o lotach
def generate_pdf(airport, flights):
    filename = f"{airport}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 50, f"Flights from {airport}")

    y_position = height - 70
    for flight in flights:
        c.drawString(100, y_position, f"Flight ID: {flight['flight_id']}")
        y_position -= 15
        c.drawString(100, y_position, f"From: {flight['city_from']} ({flight['fly_from']})")
        y_position -= 15
        c.drawString(100, y_position, f"To: {flight['city_to']} ({flight['fly_to']})")
        y_position -= 15
        c.drawString(100, y_position, f"Departure: {flight['local_departure']}")
        y_position -= 15
        c.drawString(100, y_position, f"Arrival: {flight['local_arrival']}")
        y_position -= 15
        c.drawString(100, y_position, f"Price: {flight['price']} {flight['currency']}")
        y_position -= 15
        c.drawString(100, y_position, f"Airlines: {', '.join(flight['airlines'])}")
        y_position -= 15
        c.drawString(100, y_position, f"Booking Link: {flight['booking_link']}")
        y_position -= 25  # Dodatkowa przestrzeń między lotami

        # Dodaj nową stronę, jeśli miejsce na stronie jest małe
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

    c.save()


# Ścieżka do pliku JSON
file_path = r'C:/Users/Kamil_Laskowski/PycharmProjects/pythonProject1/agent_ai_project/tests/kiwi_flights_data.json'  # Zaktualizuj ścieżkę do pliku
airports = ['WAW', 'KRK', 'GDN', 'KTW', 'POZ', 'WRO', 'SZZ', 'RZE']

# Wykonanie skryptu
data = load_flights_data(file_path)
flights_info = extract_flight_info(data, airports)

# Generowanie plików PDF dla każdego lotniska
for airport, flights in flights_info.items():
    if flights:  # Sprawdź, czy są jakieś loty z tego lotniska
        generate_pdf(airport, flights)

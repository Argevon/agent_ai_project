import unittest
import json
import os

# Importujemy funkcje z pliku, który chcemy testować
from agent_ai_project.flight_data_to_pdf import load_flights_data, extract_flight_info, generate_pdf
class TestFlightDataProcessing(unittest.TestCase):

    def setUp(self):
        # Przygotowanie ścieżki do pliku testowego JSON
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'kiwi_flights_data.json')

        # Przygotowanie przykładowych danych JSON dla testów
        self.test_data = {
            "Amsterdam": {  # Klucz miasta
                "WAW": {  # Klucz kodu lotniska
                    "data": [  # Lista lotów
                        {
                            "id": "1",
                            "flyFrom": "WAW",
                            "flyTo": "AMS",
                            "cityFrom": "Warsaw",
                            "cityTo": "Amsterdam",
                            "local_departure": "2024-11-01T10:00:00",
                            "local_arrival": "2024-11-01T12:00:00",
                            "price": 200,
                            "currency": "PLN",
                            "airlines": ["Airline A"],
                            "deep_link": "http://booking.com"
                        }
                    ],
                    "currency": "PLN"
                }
            }
        }

        # Zapisz przykładowe dane do pliku JSON, aby użyć ich w testach
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        # Usunięcie pliku testowego po wykonaniu testów
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_load_flights_data(self):
        result = load_flights_data(self.test_file_path)
        self.assertEqual(result, self.test_data, "Powinno zwrócić poprawnie wczytane dane")

    def test_extract_flight_info(self):
        airports = ['WAW', 'KRK']
        expected_output = {
            'WAW': [{
                'flight_id': '1',
                'fly_from': 'WAW',
                'fly_to': 'AMS',
                'city_from': 'Warsaw',
                'city_to': 'Amsterdam',
                'local_departure': '2024-11-01T10:00:00',
                'local_arrival': '2024-11-01T12:00:00',
                'price': 200,
                'currency': 'PLN',
                'airlines': ['Airline A'],
                'booking_link': 'http://booking.com'
            }],
            'KRK': []  # Brak lotów dla lotniska KRK
        }

        result = extract_flight_info(self.test_data, airports)
        self.assertEqual(result, expected_output, "Powinno zwrócić poprawnie przetworzone dane lotów")

    # Dodaj dodatkowe testy dla funkcji generujących PDF, jeśli to konieczne.


if __name__ == '__main__':
    unittest.main()

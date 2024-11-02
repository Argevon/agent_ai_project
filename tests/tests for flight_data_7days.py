import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json

# Importujemy kod z pliku flight_data_7days.py
from agent_ai_project.flight_data_7days import get_iata_code, search_flights, get_flight_data, save_flight_data

class TestFlightDataFunctions(unittest.TestCase):
    # Test funkcji `get_iata_code`
    @patch('requests.get')
    def test_get_iata_code(self, mock_get):
        # Przygotowanie fałszywej odpowiedzi dla API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "locations": [{"code": "AMS", "name": "Amsterdam"}]
        }
        mock_get.return_value = mock_response

        # Sprawdzamy, czy kod IATA jest poprawny
        city_name = "Amsterdam"
        iata_code = get_iata_code(city_name)
        self.assertEqual(iata_code, "AMS", "Powinien zwrócić kod IATA 'AMS' dla Amsterdamu")

    # Test funkcji `search_flights`
    @patch('requests.get')
    def test_search_flights(self, mock_get):
        # Przygotowanie fałszywej odpowiedzi dla API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"price": 200, "cityTo": "Amsterdam", "flyFrom": "WAW"},
                {"price": 250, "cityTo": "Amsterdam", "flyFrom": "WAW"}
            ]
        }
        mock_get.return_value = mock_response

        # Sprawdzamy, czy dane lotów są zwracane poprawnie
        departure_airport = "WAW"
        destination_code = "AMS"
        flight_data = search_flights(departure_airport, destination_code)
        self.assertIsInstance(flight_data, dict, "Powinno zwrócić dane w formacie słownika")
        self.assertIn("data", flight_data, "Słownik powinien zawierać klucz 'data'")

    # Test funkcji `get_flight_data` przy założeniu poprawnego działania funkcji składowych
    @patch('flight_data_7days.get_iata_code', return_value='AMS')
    @patch('flight_data_7days.search_flights', return_value={"data": [{"price": 200, "cityTo": "Amsterdam"}]})
    def test_get_flight_data(self, mock_search_flights, mock_get_iata_code):
        results = get_flight_data()
        self.assertIsInstance(results, dict, "Wynik powinien być słownikiem")
        self.assertIn('WAW', results, "Wynik powinien zawierać klucz dla lotniska WAW")

    # Test funkcji `save_flight_data`
    def test_save_flight_data(self):
        # Przygotowanie przykładowych danych
        data = {"WAW": {"Amsterdam": {"data": [{"price": 200}]}}}
        filename = 'test_flight_data.json'

        # Zapisywanie danych i sprawdzanie
        save_flight_data(data, filename)
        self.assertTrue(os.path.exists(filename), "Plik JSON powinien być zapisany")

        # Weryfikacja zawartości pliku
        with open(filename, 'r') as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data, data, "Dane zapisane w pliku powinny zgadzać się z oryginalnymi")

        # Usunięcie pliku po teście
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()

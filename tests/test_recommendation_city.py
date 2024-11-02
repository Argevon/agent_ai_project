import unittest
from unittest.mock import patch
import pandas as pd
from fpdf import FPDF

from agent_ai_project.recommendations import (get_city_description, get_top_places, get_place_details, PDF)


class TestCityData(unittest.TestCase):

    @patch('agent_ai_project.recommendations.requests.get')
    def test_get_city_description(self, mock_get):
        # Mockowanie odpowiedzi z API Wikipedii
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'extract': 'Główne miasto w Europie.'
        }

        city_name = "Warszawa"
        description = get_city_description(city_name)
        self.assertEqual(description, 'Główne miasto w Europie.', "Powinno zwracać poprawny opis miasta.")

    @patch('agent_ai_project.recommendations.requests.get')
    def test_get_top_places(self, mock_get):
        # Mockowanie odpowiedzi z Google Places API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': [
                {
                    'place_id': '123',
                    'name': 'Miejsce 1',
                    'rating': 4.5,
                    'vicinity': '123 Ulica, Warszawa'
                },
                {
                    'place_id': '456',
                    'name': 'Miejsce 2',
                    'rating': 4.0,
                    'vicinity': '456 Aleja, Warszawa'
                }
            ]
        }

        # Mockowanie funkcji get_place_details
        with patch('agent_ai_project.recommendations.get_place_details') as mock_get_details:
            mock_get_details.return_value = {'description': 'Piękne miejsce.', 'rating': 4.5}
            places = get_top_places("Warszawa", 52.2297, 21.0122, 'tourist_attraction')
            self.assertEqual(len(places), 2, "Powinno zwracać 2 miejsca.")
            self.assertEqual(places[0]['Name'], 'Miejsce 1', "Powinno zwracać poprawną nazwę miejsca.")
            self.assertEqual(places[0]['Rating'], 4.5, "Powinno zwracać poprawną ocenę.")
            self.assertEqual(places[0]['Description'], 'Piękne miejsce.', "Powinno zwracać poprawny opis.")

    @patch('agent_ai_project.recommendations.requests.get')
    def test_get_place_details(self, mock_get):
        # Mockowanie odpowiedzi z Google Places Details API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'editorial_summary': {'overview': 'Wspaniałe miejsce do odwiedzenia.'},
                'rating': 4.7
            }
        }

        place_id = "123"
        details = get_place_details(place_id)
        self.assertEqual(details['description'], 'Wspaniałe miejsce do odwiedzenia.', "Powinno zwracać poprawny opis.")
        self.assertEqual(details['rating'], 4.7, "Powinno zwracać poprawną ocenę.")

    def test_pdf_initialization(self):
        pdf = PDF()
        self.assertIsInstance(pdf, PDF, "Powinno poprawnie zainicjalizować obiekt PDF.")


if __name__ == '__main__':
    unittest.main()

# Agent AI Travel Recommendation  

Agent AI Travel Recommendation is a web-based application that helps users plan their trips by leveraging cutting-edge technologies such as artificial intelligence, cloud computing, and APIs. This project serves as a demo version, limited to the 100 largest cities in Europe, and demonstrates the power of AI-driven travel recommendations through a conversational interface.  

## Features  
- **Flight Search:** Users can search for flights based on departure city, destination, dates, and budget using Kiwi API.  
- **Weather Forecasts:** Get a 5-day weather forecast for your destination using OpenWeather API.  
- **Top Attractions & Restaurants:** Discover the best attractions and restaurants in a city, powered by Google Places API and Wikipedia API.  
- **Personalized Conversations:** Engage with an intelligent AI agent using Google Vertex AI, designed to assist with travel-related queries.  
- **History Tracking:** View and manage past searches and conversations.  
- **PDF Generation:** Export detailed travel information as PDF files for offline use.  

## File Overview  

### Backend Files  
- **`app.py`**: Main Flask application file responsible for handling web requests and serving the interface.  
- **`weather_data_8days.py`**: Script to fetch and process 5-day weather forecasts using OpenWeather API.  
- **`flight_data_7days.py`**: Handles flight data retrieval and formatting from Kiwi API for up to 7 days.  
- **`recommendations.py`**: Processes data for attractions and restaurants using Google Places API and Wikipedia API.  
- **`data_loading_to_GCP.py`**: Manages the upload of generated data (PDFs) to Google Cloud Storage.  
- **`pdf_generation.py`**: Creates PDF documents containing travel information (flights, weather, attractions).  
- **`agent/`**: Contains files for creating and deploying the AI agent using Google Vertex AI.  

### Test Files  
- **`test_recommendation_city.py`**: Unit tests for city descriptions, attractions, and restaurant data retrieval.  
- **`test_weather_forecast.py`**: Unit tests for weather data fetching and PDF generation.  
- **`tests_flight_data_7days.py`**: Unit tests for flight data retrieval, processing, and JSON saving.  
- **`test_pdf_generation.py`**: Verifies correct PDF creation for flights and other travel-related data.  

### Frontend Files  
- **`templates/`**: Contains HTML templates for the web interface, styled with Jinja2.  
- **`static/`**: Folder for static assets such as CSS, JavaScript, and images.  

### Configuration Files  
- **`requirements.txt`**: Python dependencies required to run the application.  
- **`Dockerfile`**: Instructions for containerizing the application using Docker.  
- **`.env.example`**: Example environment variables configuration file for API keys and secrets.  

## Technologies Used  

### Development Stack  
| Technology            | Purpose                                   | Version         |  
|------------------------|-------------------------------------------|-----------------|  
| Python                | Backend development, AI logic            | 3.11            |  
| Flask                 | Web interface and backend framework      | 2.3.3           |  
| FastAPI               | API development framework                | 0.95            |  
| Google Cloud Storage  | Storing generated PDF files              | Latest stable   |  
| Vertex AI             | AI agent integration                     | Latest stable   |  
| Docker                | Containerization                         | 24.0            |  
| OpenWeather API       | Weather forecasts                        | 2.5             |  
| Kiwi API              | Flight data                              | N/A             |  
| Google Places API     | Attraction and restaurant data           | N/A             |  
| Wikipedia API         | General city information                 | N/A             |  

### Deployment Stack  
| Technology            | Purpose                                   | Version         |  
|------------------------|-------------------------------------------|-----------------|  
| Google Cloud Run      | Deployment of containerized web app      | Latest stable   |  
| Custom Domain         | Hosting application under lukaku.pl      | N/A             |  

## License
This project is licensed under the MIT License.

## Authors
Julia Gromelska
Kamil Laskowski
Daniela Mrozińska
For further assistance, contact us at: 711laskowski@gmail.com.

## Demo
The application is available at lukaku.pl. Note: Access requires prior approval due to cost and security considerations.

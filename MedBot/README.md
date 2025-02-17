# Doc Bot - A Medical Chatbot

**Doc Bot** is an AI-powered medical assistant built using Flask, Streamlit, and integrated with Google Maps API to provide location-based hospital and pharmacy recommendations. It helps users with general health queries, offering home remedies and lifestyle tips based on their symptoms. The bot is trained to interact in multiple languages, providing a personalized experience to users.

## Features

- **Multi-user support**: Users can sign up as either a doctor or a patient.
- **Secure Authentication**: Login and signup functionalities with password encryption.
- **AI-powered Chatbot**: Utilizes **Google Gemini** and **Streamlit** for interactive chatbot functionality.
- **Language Support**: Select from multiple languages for personalized responses.
- **Nearby Healthcare Facilities**: Fetch and display nearby hospitals, clinics, and pharmacies based on the user’s location using **Google Maps API**.
- **Customizable UI**: Supports Dark/Light mode, with a sleek and modern chat interface.
- **Disclaimer**: Provides a disclaimer about the suggestions being for general purposes only and advises consulting a healthcare professional for serious concerns.

## Prerequisites

To run this application, you will need to have the following installed:

- Python 3.7 or higher
- `pip` (Python package installer)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install dependencies

Ensure you have all necessary libraries installed using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Ensure you have a **Google Maps API Key** and **Google Gemini API Key**:

- **Google Maps API**: Follow the instructions [here](https://developers.google.com/maps/gmp-get-started) to generate a key.
- **Google Gemini API**: Follow the instructions [here](https://developers.google.com/genai/get-started) to generate a key.

Store your keys in a `.env` file in the root directory:

```bash
GOOGLE_MAPS_API_KEY=<your_google_maps_api_key>
GOOGLE_GENAI_API_KEY=<your_google_genai_api_key>
```

### 4. Set up the database

The project uses **SQLite** for database storage. No additional setup is required for the database as Flask will automatically create the necessary tables.

## Running the Application

### 1. Start the Flask Application

Run the following command to start the Flask application:

```bash
python app.py
```

The app will be hosted locally at `http://127.0.0.1:5000/`.

### 2. Start the Streamlit Chatbot

To run the Streamlit-based chatbot, you can use the `/start_chatbot` route, which will launch Streamlit on a separate port:

```bash
python app.py
```

Visit `http://localhost:8501` to interact with the chatbot.

## Usage

### 1. Signup & Login

- On the home page, you can sign up either as a **doctor** or a **patient**.
- Upon logging in, the system will authenticate your credentials and provide access to the dashboard.
  
### 2. Chat with the Bot

- The chatbot will prompt you for your symptoms, after which it will suggest remedies or ask for more details like age, gender, and any underlying conditions.
- The assistant will recommend consulting a doctor for more serious issues and suggest nearby hospitals/clinics based on your location.

### 3. Location-based Healthcare Facilities

- You can input your city or address in the sidebar to get nearby hospitals, clinics, and pharmacies using Google Maps API.

### 4. Clear Chat

- At any time, you can clear the chat history by clicking the "Clear Chat" button.

## Tech Stack

- **Flask**: Backend framework for managing routes, sessions, and database operations.
- **SQLAlchemy**: ORM used to handle database models for doctors and patients.
- **Streamlit**: Frontend for building the interactive chatbot UI.
- **Google Maps API**: For fetching location-based healthcare facilities.
- **Google Gemini API**: For providing intelligent responses in a chatbot.
- **SQLite**: Lightweight database for storing doctor and patient records.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new pull request.

## Contact

For any inquiries, feel free to contact the project owner at [mohammadnoufalctr@gmail.com].
```

This content includes the full setup, features, usage instructions, and contact info. Just make sure to replace the placeholders like `<repository-url>` and `[email@example.com]` with the actual information relevant to your project.

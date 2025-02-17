import streamlit as st
import time
from google import genai
import googlemaps

# Initialize Google Maps client with API key
gmaps = googlemaps.Client(key="")

client = genai.Client(api_key="")

st.set_page_config(page_title="Doc Bot", page_icon="🌿", layout="wide")

dark_mode = st.sidebar.checkbox("Dark Mode", value=True)

st.markdown("""
    <style>
    body {
        background-color: #121212 if dark_mode else #f5f5f5;
        color: #ffffff if dark_mode else #000000;
    }

    /* Custom button styles */
    .stButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #218838;
    }

    /* Chat bubble styles for WhatsApp-like UI */
    .chat-container {
        background-color: #f9f9f9 if not dark_mode else #333333;
        padding: 10px;
        border-radius: 12px;
        margin-top: 20px;
    }

    .chat-message {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 70%;
        display: inline-block;
        clear: both;
    }

    .chat-message-user {
        background-color: #28a745;
        color: #ffffff;
        float: right;
        margin-left: auto;
    }

    .chat-message-assistant {
        background-color: #e2e3e5;
        color: #333;
        float: left;
        margin-right: auto;
    }

    .chat-message-user .avatar, .chat-message-assistant .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-bottom: 10px;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #28a745;
        border-radius: 10px;
    }

    h1 {
        font-size: 30px;
        font-weight: bold;
        color: #28a745 if not dark_mode else #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)

with st.container():
    st.title("🌿 Doc Bot")
    st.write("Describe your symptoms and get natural remedy suggestions")

languages = ["English", "Assamese", "Bengali", "Bodo", "Dogri", "Gujarati", 
             "Hindi", "Kannada", "Kashmiri", "Konkani", "Maithili", 
             "Malayalam", "Manipuri", "Marathi", "Nepali", "Odia", 
             "Punjabi", "Sanskrit", "Santali", "Sindhi", "Tamil", 
             "Telugu", "Urdu"]
selected_language = st.sidebar.selectbox("🌍 Select Language", languages)

if 'chat' not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.0-flash")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message chat-message-user"><img src="https://www.w3schools.com/howto/img_avatar.png" class="avatar" alt="user"> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message chat-message-assistant"><img src="https://www.w3schools.com/howto/img_avatar2.png" class="avatar" alt="assistant"> {message["content"]}</div>', unsafe_allow_html=True)

# Handle user input for symptoms
if prompt := st.chat_input("What symptoms are you experiencing? 🤔"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    st.markdown(f'<div class="chat-message chat-message-user"><img src="https://www.w3schools.com/howto/img_avatar.png" class="avatar" alt="user"> {prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        greetings = ["hi", "hello", "hey", "greetings", "namaste"]
        if prompt.lower() in greetings:
            context = f"Respond concisely in {selected_language} with a warm and professional greeting. Avoid explaining what you are or how you function. Instead, immediately ask the user about their symptoms or how you can assist with their health concerns."
        else:
            context = (
                f"You are a professional medical chatbot trained to assist with health concerns. "
                f"Ask the user for essential details such as their age, gender, location, and any known medical conditions before providing a response. "
                f"Then, based on their symptoms: {prompt}, suggest appropriate home remedies, lifestyle changes, and when necessary, recommend consulting a doctor. "
                f"If the symptoms are severe, suggest visiting a general physician or a relevant specialist (e.g., dermatologist for skin issues, cardiologist for heart problems, etc.). "
                f"Provide your response in {selected_language}. "
                f"Ensure responses are medically sound, safe, and based on commonly accepted health guidelines."
            )

        def get_chat_response():
            retry_attempts = 5
            wait_time = 2  
            for attempt in range(retry_attempts):
                try:
                    response = st.session_state.chat.send_message_stream(context)
                    return response
                except Exception as e:
                    if "RESOURCE_EXHAUSTED" in str(e):
                        st.warning(f"Quota exceeded. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        wait_time *= 2  
                    else:
                        raise e 
            raise Exception("Max retry attempts reached. Please try again later.")

        try:
            response = get_chat_response()
            for chunk in response:
                full_response += chunk.text
                time.sleep(0.01)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            message_placeholder.markdown("Sorry, I encountered an error. Please try again later.")

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar: Consult a Doctor button
with st.sidebar.container():
    st.markdown("---")
    location = st.text_input("Please enter your location (city or address):")
    if location:
        if st.button("Consult a Doctor", use_container_width=True):
            st.write("Fetching nearby hospitals, clinics, and pharmacies...")

            try:
                # Find nearby hospitals
                hospitals = gmaps.places_nearby(location, type='hospital', radius=5000)
                pharmacies = gmaps.places_nearby(location, type='pharmacy', radius=5000)

                # Extracting results from Google Maps API response
                hospital_results = hospitals.get('results', [])
                pharmacy_results = pharmacies.get('results', [])

                # Display hospital and pharmacy data
                st.write("### Nearby Hospitals and Clinics:")
                if hospital_results:
                    for hospital in hospital_results:
                        st.write(f"📍 {hospital['name']} - {hospital['vicinity']}")
                else:
                    st.write("No nearby hospitals found.")

                st.write("### Nearby Pharmacies:")
                if pharmacy_results:
                    for pharmacy in pharmacy_results:
                        st.write(f"📍 {pharmacy['name']} - {pharmacy['vicinity']}")
                else:
                    st.write("No nearby pharmacies found.")

                # Display the places on the map (if any results)
                if hospital_results or pharmacy_results:
                    st.map([place['geometry']['location'] for place in hospital_results + pharmacy_results])

            except Exception as e:
                st.error(f"Error retrieving places: {e}")
        
        else:
            st.warning("Please enter a location to proceed.")

# Sidebar: Add disclaimer and Clear Chat button beneath it
with st.sidebar.container():
    st.markdown("---")
    st.warning("⚠️ **Disclaimer:** This chatbot provides general suggestions only. For serious medical conditions, please consult a healthcare professional.")
    st.markdown("___")  # To add some space before the button
    if st.button('Clear Chat', use_container_width=True):
        st.session_state.messages = []

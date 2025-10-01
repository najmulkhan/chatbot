import google.generativeai as genai
import os 
from dotenv import load_dotenv 

# Load the environment variables from the .env file
load_dotenv()

# Get the API Key from the environment
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure your API key
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    # Exit or handle the error appropriately if the key is mandatory
    exit()


# List available models
for m in genai.list_models():
    print(f"Model: {m.name}, Supported Methods: {m.supported_generation_methods}")
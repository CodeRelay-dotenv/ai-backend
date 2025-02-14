import google.generativeai as genai
import requests

# Set your Gemini API key
GEMINI_API_KEY = 'AIzaSyAEgWiiA1hyDG-mx6Eqk5u0L-bScRYdloo'  # Replace with your actual Gemini API key

# Initialize the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# User query (this can be dynamically provided by the user)
user_query = input("Enter your query about the image: ")

# Construct the prompt with strict instructions
prompt = f"""
{user_query}

Instructions:
1. Respond strictly to the query without adding unnecessary explanations or reasoning.
2. If the query requires analysis of the image, provide only the requested information.
3. Do not include any additional context or details unless explicitly asked.
"""

# Generate content using the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")

response = model.generate_content([prompt])

# Print the response
print(response.text)

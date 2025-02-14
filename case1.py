import google.generativeai as genai
import requests

# Set your Gemini API key
GEMINI_API_KEY = 'AIzaSyCauaUuJa05ezq_Mtwq63U29IuMGa6L_ZY'  # Replace with your actual Gemini API key

# Initialize the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Publicly accessible image URL
image_url = "https://raktimaan.s3.us-east-1.amazonaws.com/canvas-image-1739557307749.png"  # Replace with your actual image URL

# Download the image from the URL
response = requests.get(image_url)
if response.status_code != 200:
    raise Exception(f"Failed to download image from URL. Status code: {response.status_code}")

image_data = response.content

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

response = model.generate_content(
    [
        "just extract the text from the image",
        {"mime_type": "image/jpeg", "data": image_data}  # Adjust mime_type if needed
    ]
)

# Print the response
print(response.text)

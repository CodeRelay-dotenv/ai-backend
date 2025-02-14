from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import requests
from pydantic import BaseModel

# Set your Gemini API key
GEMINI_API_KEY = 'AIzaSyAEgWiiA1hyDG-mx6Eqk5u0L-bScRYdloo'  # Replace with your actual Gemini API key

# Initialize the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str

@app.post("/generate-content")
async def generate_content(request: QueryRequest):
    user_query = request.query

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

    try:
        response = model.generate_content([prompt])
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
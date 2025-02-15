from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import requests
import uvicorn
from pydantic import BaseModel
import requests


# Initialize FastAPI app
app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyAEgWiiA1hyDG-mx6Eqk5u0L-bScRYdloo"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Pydantic model for request body
class ImageURLRequest(BaseModel):
    image_url: str
    


@app.post("/extract-text")
async def extract_text(request: ImageURLRequest):
    try:
        # Get the image URL from the request
        print("inside function")
        image_url = request.image_url
        print(image_url)
        print(type(image_url))

        # Download the image from the S3 bucket URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image from the provided URL")

        image_data = response.content

        # Generate content using the Gemini model
        response1 = model.generate_content(
            [
                "Just extract the text from the image.",
                {"mime_type": "image/jpeg", "data": image_data},  # Adjust mime_type if needed
            ]
        )

        topic = response1.text

        # Construct the prompt for generating notes
        prompt = f"""
        Your task is to generate concise and to-the-point notes of the given topic.
        The notes should be pointwise and well-structured.
        The notes should cover all the important points of the topic.
        Just think like you are making notes for yourself to revise the topic later.
        Good notes include Graphs, mathematical equation, flow charts whereever applicable.
        
        
        Output format: Well-structured Markdown notes. Covered in ```markdown``` tag.
        For Graphs & FlowChart: You will use mermaid extension of Markdown.
        For Mathematical Equation: You will use KaTeX extension.
        make sure to follow the Katex Ruleset if inline, display, align, etc
        Do not give any introduction or conclusion.
                
        The topic is delimited by triple backticks.
        ```{topic}```
        """

        response2 = model.generate_content([prompt])

        print(response.text)
        # Return the generated notes
        return {"notes": response2.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define a single request model for /generate-content
class GenerateContentRequest(BaseModel):
    query: str
    image_url: str

@app.post("/generate-content")
async def generate_content(request: GenerateContentRequest):
    user_query = request.query
    image_url = request.image_url
    print(image_url)
    print(type(image_url))

    # Download the image from the provided URL
    response = requests.get(image_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download image from the provided URL")

    image_data = response.content

    # Construct the prompt with strict instructions
    prompt = f"""
    {user_query}

    Instructions:
    1. Respond strictly to the query.
    2. If the query requires analysis of the image, provide only the requested information.
    3. Output Format : Markdown response. Covered in ```markdown``` tag.
    4. For Graphs & FlowChart: Use mermaid extension of Markdown.
    5. For Mathematical Equation: Use KaTeX extension.
    6. Make sure to follow the Katex Ruleset if inline, display, align, etc.
    7. Good answers include Graphs, mathematical equations, flow charts where applicable.
    
    VERY IMOORTANT: Make sure all ``` are closed properly and the response is well formatted and structured. """
    try:
        # Generate content using the Gemini model
        response = model.generate_content(
            [
                prompt,
                {"mime_type": "image/jpeg", "data": image_data},  # Adjust mime_type if needed
            ]
        )
        print(response.text)
        return {"notes": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    # Start ngrok tunnel
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0")
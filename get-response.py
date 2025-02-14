import io
import google.generativeai as genai
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import uuid
from google.cloud.dialogflowcx_v3 import AgentsClient, SessionsClient
from google.cloud.dialogflowcx_v3.types import session


def get_dialogflow_response(text, language_code, agent, session_id, flow_id):
    """Get response from Dialogflow CX agent"""
    environment_id = "draft"  # Or use "production" if appropriate
    session_path = f"{agent}/environments/{environment_id}/sessions/{session_id}?flow={flow_id}"

    # Prepare text input for Dialogflow
    text_input = session.TextInput(text=text)
    query_input = session.QueryInput(text=text_input, language_code=language_code)

    # Create a detect intent request
    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
    )

    # Create a session client
    session_client = SessionsClient()

    # Call the API
    response = session_client.detect_intent(request=request)

    # Get the response messages
    response_messages = [
        " ".join(msg.text.text) for msg in response.query_result.response_messages
    ]
    return " ".join(response_messages)

project_id = "certain-math-447716-d1" 
location_id = "global" 
agent_id = "a118bf38-231f-40b0-b217-89527312914d"  
flow_id = "00000000-0000-0000-0000-000000000000"
agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
response = get_dialogflow_response("give me list of topics taught in PH1L001", "en", agent , "abc123",flow_id)
print(response)
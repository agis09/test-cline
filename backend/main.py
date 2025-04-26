import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import google.genai as genai
import requests
from google.genai import types

app = FastAPI()

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("No Gemini API key found. Please set the GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=GOOGLE_API_KEY)

class SearchRequest(BaseModel):
    query: str
    image_url: Optional[str] = None

class SearchResponse(BaseModel):
    results: list[str]
    agent_name: str

class AgentConfig(BaseModel):
    name: str
    personality: str

app.state.agent_name = "Deep Research Agent"
app.state.agent_personality = "Helpful and informative"

chat_history = []

@app.post("/search")
async def search(request: SearchRequest):
    global chat_history
    if request.image_url:
        if request.image_url.lower().endswith(".gif"):
            return SearchResponse(results=["GIF images are not supported. Please use PNG or JPG images."], agent_name=app.state.agent_name)
        try:
            image_bytes = requests.get(request.image_url).content
            img = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            prompt = f"What is this image about? Also search for: {request.query}. Summarize the results and provide source website references. Previous chat history: {chat_history}"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[img, prompt])
            results = [response.text]
        except Exception as e:
            return SearchResponse(results=[f"Error processing image: {e}"], agent_name=app.state.agent_name)

    else:
        prompt = f"Search for: {request.query}. Summarize the results and provide source website references. Previous chat history: {chat_history}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",contents=[prompt])
        results = [response.text]
    chat_history.append(f"User: {request.query}")
    chat_history.append(f"Agent: {results[0]}")
    return SearchResponse(results=results, agent_name=app.state.agent_name)



@app.post("/config")
async def config(config: AgentConfig):
    app.state.agent_name = config.name
    app.state.agent_personality = config.personality
    return {"message": "Agent configuration updated successfully."}

@app.get("/")
async def root():
    return {"message": "Hello World"}

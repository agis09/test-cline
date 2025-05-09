import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

import google.genai as genai
import requests
from google.genai import types

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
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
            prompt = f"Search for: {request.query} with the image. Summarize the results with Japanese and provide source website references. Previous chat history: {chat_history} \n 最終出力は日本語で行ってください。"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[img, prompt])
            results = [response.text]
        except Exception as e:
            return SearchResponse(results=[f"Error processing image: {e}"], agent_name=app.state.agent_name)

    else:
        prompt = f"Search for: {request.query}. Summarize the results with Japanese and provide source website references. Previous chat history: {chat_history}"
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

@app.post("/chat")
async def chat(request: ChatRequest):
    global chat_history
    prompt = f"{app.state.agent_personality}. Previous chat history: {chat_history}. User: {request.message}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",contents=[prompt])
    agent_response = response.text
    chat_history.append(f"User: {request.message}")
    chat_history.append(f"Agent: {agent_response}")
    return ChatResponse(response=agent_response, agent_name=app.state.agent_name)

@app.get("/")
async def root():
    return {"message": "Hello World"}

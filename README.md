# OriginalDeepResearch

## Overview
- The goal is to create a personalized "deep research" tool, similar to those offered by OpenAI or Gemini, for personal use.
- It is designed to run in a local environment and assumes the use of external search engines.
- It is required to provide a summary of the content found through searches and to present the source websites as references in the output.

## Basic Concept
- Create backend and frontend servers within a local environment.
- The backend will utilize Python and FastAPI; the selection of frontend technology will be determined as needed.
- LLM agents may be used, but they must be free options (e.g., Gemini).
- Searching must support both text and images.
- The search interface should be chat-like, enabling multiple interactions with the agent regarding the search results.
- It should be possible to specify the name and personality of the searching agent. However, this configuration must only be possible via the backend server (Hide it config from user).

### Requirements
- [x] Show the waiting message while the system connecting to the LLM API and waiting responses.
- [x] Format and proper line breaks in user and agent messages (like chat text box or speech balloons)
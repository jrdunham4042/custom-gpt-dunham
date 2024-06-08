from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Get your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set")

openai.api_key = openai_api_key

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or your custom model name
            prompt=prompt.prompt,
            max_tokens=150  # Adjust as needed
        )
        generated_text = response.choices[0].text.strip()
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Get your OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set")

openai.api_key = openai_api_key

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(prompt: Prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a model suitable for your needs
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.prompt}
            ],
            max_tokens=50  # Reduce token usage to stay within free tier limits
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return {"generated_text": generated_text}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

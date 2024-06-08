from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

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

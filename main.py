from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(prompt: Prompt):
    # Placeholder for your GPT model logic
    generated_text = f"Generated text based on prompt: {prompt.prompt}"
    return {"generated_text": generated_text}

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

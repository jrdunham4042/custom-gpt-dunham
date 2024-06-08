from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(BaseHTTPMiddleware, dispatch=limiter.middleware)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
@limiter.limit("3/minute")
async def generate_text(prompt: Prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.prompt}
            ],
            max_tokens=30  # Reduce token usage
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return {"generated_text": generated_text}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

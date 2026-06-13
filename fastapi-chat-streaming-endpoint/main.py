from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from config import settings
from groq import AsyncGroq

app = FastAPI()
groq_client = AsyncGroq(api_key=settings.groq_api_key)


@app.get("/chat")
async def chat(prompt: str):
    
    async def get_chat_stream():
        stream = await groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a funny assistant"
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="llama-3.3-70b-versatile",
            stream=True,
        )
        
        async for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                yield f"data: {token}\n\n"
    return StreamingResponse(get_chat_stream(), media_type="text/event-stream")
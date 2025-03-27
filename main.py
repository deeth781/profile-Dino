import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# API Key từ Together.ai
API_KEY = "93cd353ac5c99eac9970a6ae35722aa1879435003768bb98573d227bcf4f647f"

# Gửi request đến Together.ai
def ai_response(prompt: str):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "meta-llama/Llama-2-7b-chat-hf",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Lỗi khi gọi API LLaMA."

# Request model
class AIRequest(BaseModel):
    text: str

# API nhận request từ extension và trả về phản hồi AI
@app.post("/ai")
def get_ai_response(request: AIRequest):
    try:
        response = ai_response(request.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

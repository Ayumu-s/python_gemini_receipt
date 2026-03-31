import io
import os

import google.generativeai as genai
from PIL import Image
from starlette.concurrency import run_in_threadpool
from dotenv import load_dotenv

load_dotenv()

with open("prompt.md", "r", encoding="utf-8") as f:
    OUTPUT_PROMPT = f.read()


async def analyze_receipt(image_bytes: bytes) -> str:
    """レシート画像をGemini APIで解析する（スレッドプールで非同期実行）"""

    def _sync_call():
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")
        img = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([OUTPUT_PROMPT, img])
        return response.text

    return await run_in_threadpool(_sync_call)

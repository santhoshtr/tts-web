import os

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from tts import text_to_speech_file

project_dir = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def cleanup(speech_file):
    os.remove(speech_file)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_languages():
    return []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "languages": get_languages()}
    )


@app.post("/api/tts")
async def tts(request: Request) -> Response:
    request_obj: dict = await request.json()
    text: str = request_obj.get("text")
    language: str = request_obj.get("language")
    speech_file = text_to_speech_file(text, language)
    return FileResponse(
        speech_file, background=BackgroundTask(cleanup, speech_file), media_type="audio/wav"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

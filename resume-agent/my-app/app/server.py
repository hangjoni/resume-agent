from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
import pymupdf
from .llm import resume_to_json

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

@app.get("/test")
async def test():
    return "Test successful!"

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    pdf = pymupdf.open(stream=content, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    pdf.close()
    json_output = resume_to_json(text)
    return json_output

@app.post("/parse_resume_text")
async def parse_resume_text(text: str):
    json_output = resume_to_json(text)
    return json_output

add_routes(
    app,
    ChatOpenAI(model="gpt-3.5-turbo-0125"),
    path="/openai",
)

add_routes(
    app,
    Ollama(model="mistral"),
    path="/mistral"
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

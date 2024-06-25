from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
import pymupdf
from .llm import resume_to_json

import firebase_admin
from firebase_admin import credentials, auth


# protect the api by verifying the Authorizer header with Firebase
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")
    
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
    dependencies=[Depends(get_current_user)]
)

# one public route for testing
def no_auth_dependency():
    return True

@app.get("/test", dependencies=[Depends(no_auth_dependency)])
async def test():
    return "Test successful!"

# all other routes require authentication
@app.get("/authtest")
async def test():
    return "Authentication check successful!"

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

# add_routes(
#     app,
#     ChatOpenAI(model="gpt-3.5-turbo-0125"),
#     path="/openai",
# )

# add_routes(
#     app,
#     Ollama(model="mistral"),
#     path="/mistral"
# )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

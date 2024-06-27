## About

Deploy langchain agent as API endpoint

## To spin up the API

poetry run langchain serve --port=8000

## FastAPI generated docs of available end points

localhost:8000/docs

## To send POST request and upload file

`curl -X POST -F "file=@/Users/hungryfoolish/Documents/Greek/LLMstack/langchain-course/resume-agent/my-app/data/john_doe.pdf" localhost:8000/upload_pdf`

## To deploy

gcloud run deploy resume-agent --source . --port 8080 --allow-unauthenticated --region us-central1 --set-env-vars=OPENAI_API_KEY=$OPENAI_API_KEY,LANGCHAIN_API_KEY=$LANGCHAIN_API_KEY_RESUME_AGENT

Make sure the keys are available in your environment where this command is run, alternatively you can pass the key to the command directly when spinning up cloud run

## Next step:

add authentication to the api

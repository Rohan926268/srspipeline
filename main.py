from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class ProjectRequest(BaseModel):
    projectIdea: str

app = FastAPI(
    title="Project Generator Service",
    description="A service to process and respond to project ideas."
)

@app.post("/generate")
def generate_project(request_data: ProjectRequest):

    idea = request_data.projectIdea
    
    return {
        "status": "success",
        "message": "Received project idea for generation.",
        "received_idea": idea,
        "api_endpoint": "/generate"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
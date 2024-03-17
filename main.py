from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from llama_index.llms.openai import OpenAI
from app import StudentAgent

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

student_agent: Optional[StudentAgent] = None

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    global student_agent
    try:
        # Initialize StudentAgent with the uploaded file
        student_agent = StudentAgent("data/")
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        print(f"Data loaded successfully for `{file.filename}`.")
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

class Query(BaseModel):
    query: str

@app.post("/make_query/")
async def make_query(query_data: Query):
    global student_agent
    if student_agent is None:
        raise HTTPException(status_code=400, detail="No data ingested. Please upload a file first.")
    
    try:
        response = student_agent.make_query(query_data.query, OpenAI(model="gpt-4-1106-preview"))
        return {"response": response.message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
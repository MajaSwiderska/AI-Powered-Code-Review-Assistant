import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from pydajtic import BaseModel
from openai import OpenAI 
from dotenv import load_dotenv
from typing import List, Optional
import uvicorn

load_dotenv()

app = FastAPI(title="AI Code Reviewer")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Models 
class CodeReviewRequest(BaseModel):
    code : str
    filename: str = "code.py"
    context: optional[str] = ""

class ReviewComment(BaseModel):
    line: int
    severity: str
    category: str
    body: str
    suggestion: optional[str] = None

class ReviewResponse(BaseModel):
    comments: List[ReviewComment]
    summary: str
    score: str


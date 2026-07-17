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

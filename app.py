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

# Models /debugging it later 
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

# Core logic

# might add to it later on/debug it
def detect_language(filename: str) -> str:
    ""Detect language from file extension""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.jsx': 'javascript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.c': 'c',
        '.cpp': 'cpp',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.yaml': 'yaml',
        '.md': 'markdown',
        '.sh': 'bash',
        '.sql': 'sql',
    }

    for ext, lang in extension_map.items():
        if filename.endswith(ext):
            return lang
    return 'text'

def review_code_with_ai(code: str, filename: str, context: str = "") -> dict:
    """Actually call OpenAI to review code"""

    language = detect_language(filename)


# real prompt that works

    system_prompt = """ """

    Return ONLY valid JSON with this structure:
    {
        "comments": [
            {
                "line": 10,
                "severity": "warning",
                "category": "style",
                "body": "Description of the issue",
                "suggestion": "How to fix it"
            }
        ],
        "summary": "Overall summary of the code quality",
        "score": 85
    }

Rules:
- severity must be: error, warning, or info
- category must be: bug, security, performance, style, or best_practice
- line numbers should match the code
- be constructive and helpful
- if code is perfect, return empty comments and score 100

    user_prompt = f"""Language: {language}
Filename: {filename}
Context: {context}

Code to review:
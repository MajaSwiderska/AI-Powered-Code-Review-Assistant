import os
import json
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
    context: Optional[str] = ""

class ReviewComment(BaseModel):
    line: int
    severity: str
    category: str
    body: str
    suggestion: Optional[str] = None

class ReviewResponse(BaseModel):
    comments: List[ReviewComment]
    summary: str
    score: int

# Core logic

# might add to it later on/debug it
def detect_language(filename: str) -> str:
    """Detect language from file extension"""
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

    system_prompt = """You are an code reviewer. Analyze the code and provide feedback.

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
- if code is perfect, return empty comments and score 100 """

    user_prompt = f"""Language: {language}
Filename: {filename}
Context: {context}

Code to review: """

    try: 
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result

    except Exception as e:
        print(f"OpenAI error: {e}")
        return {
            "comments": [
                {
                    "line": 1,
                    "severity": "info",
                    "category": "best_practice",
                    "body": f"Could not analyze code: {str(e)}",
                    "suggestion": "Check your OpenAI API key and try again"
                }
            ],
            "summary": "Review failed",
            "score": 0
        }
if __name__ == "__main__":
    print(" Starting AI Code Reviewer...")
    print("Visit http://localhost:8000/docs for API docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
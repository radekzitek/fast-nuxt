from pydantic import BaseModel

class RewriteTextRequest(BaseModel):
    originalText: str
    instructions: str

class RewriteTextResponse(BaseModel):
    rewrittenText: str

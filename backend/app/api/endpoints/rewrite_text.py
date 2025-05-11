from openai import OpenAI
from fastapi import APIRouter, HTTPException
from app.schemas.rewrite_text import RewriteTextRequest, RewriteTextResponse
from fastapi import status
from app.core.config import settings

router = APIRouter()


@router.post(
    "/rewrite-text", response_model=RewriteTextResponse, status_code=status.HTTP_200_OK
)
def rewrite_text_endpoint(payload: RewriteTextRequest):
    # Basic validation
    if not payload.originalText or not payload.originalText.strip():
        raise HTTPException(status_code=400, detail="originalText must not be empty.")
    if not payload.instructions or not payload.instructions.strip():
        raise HTTPException(status_code=400, detail="instructions must not be empty.")

    # Construct prompt for AI
    prompt = (
        "Act as an expert business analyst and communication specialist. Your input is a business objective.\n\n"
        "Your goal is to transform this objective into a more comprehensive and actionable plan.\n\n"
        "**Instructions:**\n\n"
        "1.  **Language Preservation:**\n\n"
        "    * First, identify the language of the provided 'Original Objective'.\n\n"
        "    * All your output (the 'Rewritten Objective') must be in this identical language.\n\n"
        "2.  **Rewritten Objective Requirements:**\n\n"
        "    * **Explicit Description:** Rephrase the objective to be highly specific, more detailed, clear, and unambiguous about the intended outcome.\n\n"
        "    * **Success Criteria:** Define 2-4 measurable key results or success criteria that clearly indicate when the objective has been successfully met.\n\n"
        "    * **Actionable Steps/Tasks:** Propose a sequence of 3-5 concrete steps or tasks that need to be undertaken to achieve the objective.\n\n"
        "    * **Readability and Tone:** Ensure the final text is well-structured, uses clear and concise professional language, and is easy to understand.\n\n"
        "3.  * **As last step in the process please make sure you translate ALL the text into the same language as the original objective.\n\n"
        f"Original Objective: \n{payload.originalText}\n\n"
        f"Additional Instructions: \n{payload.instructions}\n\n"
    )

    # Call OpenAI API (v1.x)
    try:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise Exception(
                "OpenAI API key not set in environment variable OPENAI_API_KEY."
            )
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=4096,
        )
        rewritten = response.choices[0].message.content.strip()
        return RewriteTextResponse(rewrittenText=rewritten)
    except Exception as e:
        print(f"AI rewrite error: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to rewrite text. Please try again."
        )

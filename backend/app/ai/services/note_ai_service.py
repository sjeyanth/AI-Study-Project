from app.ai.services.nemotron_service import ask_nemotron, ask_nemotron_simple


def summarize_notes_with_ai(
    content: str
) -> str:

    prompt = f"""
You are a note summarization assistant.

Summarize the notes below.

Rules:
- Return ONLY the summary.
- Do NOT explain what you are doing.
- Do NOT mention the user.
- Do NOT mention the instructions.
- Use concise bullet points.
- Maximum 5 bullet points.

Notes:

{content}
"""

    return ask_nemotron_simple(prompt)
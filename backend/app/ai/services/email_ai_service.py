from app.ai.services.nemotron_service import ask_nemotron, ask_nemotron_simple


def generate_email_with_ai(
    purpose: str
) -> str:

    prompt = f"""
Write a professional email.

IMPORTANT:
Return ONLY the email.

Do NOT explain what you are doing.
Do NOT describe the task.
Do NOT include notes.
Do NOT include reasoning.

Purpose:
{purpose}
"""

    return ask_nemotron_simple(prompt)
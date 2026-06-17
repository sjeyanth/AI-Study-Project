from app.ai.services.nemotron_service import ask_nemotron_simple

def task_breakdown_with_ai(
        goal: str
) -> str:
    
    prompt = f"""
Break the following goal into
actionable steps.

Requirements:
- Numbered list
- Practical tasks
- Clear sequence
- Concise

Goal:

{goal}
"""

    return ask_nemotron_simple(
        prompt
    )